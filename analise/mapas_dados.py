"""Dados da página de mapas (grafico/web/mapas.html) → grafico/web/mapas_dados.json.

Por município (código IBGE, via tabela oficial do TSE cd → cdi) e por UF, em 2026 e 2022:
  % Lula 1º e 2º turno (válidos), virada (pp), comparecimento 1º e 2º e mudança (pp), eleitores,
  divergência em relação ao esperado (z do município, modelo completo, módulo E).
Fluxo de votos 1º → 2º turno (C06, Goodman com restrição): nacional e por UF, em votos.
Mapas de calor de Klimek (T25): histograma comparecimento x % do candidato.
Fontes: analise/base*.parquet, resultado_comportamento_<ano>.json, divergencias_municipios_<ano>_completo.csv,
resultado_bateria_<ano>.json; malha do IBGE em grafico/web/geo/ (só para desenhar).
"""
import json
import os

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(AQUI, "..", "grafico", "web")
tse = json.load(open(os.path.join(WEB, "geo", "tse_municipios_2026.json")))
ibge = {}
for ab in tse["abr"]:
    for m in ab["mu"]:
        ibge[(ab["cd"].upper(), str(int(m["cd"])))] = (m["cdi"], m["nm"])
out = {"fonte": "TSE (dados abertos e resultados); malha IBGE só para desenho", "anos": {}}

for ano in ("2026", "2022"):
    b = pd.read_parquet(os.path.join(AQUI, "base.parquet" if ano == "2026" else f"base_{ano}.parquet"))
    b = b[(b["SG_UF"] != "ZZ") & b["total_1"].notna() & b["total_2"].notna()]
    cols = ["v13_1", "v22_1", "validos_1", "v13_2", "v22_2", "validos_2", "QT_COMPARECIMENTO_1", "QT_APTOS_1",
            "QT_COMPARECIMENTO_2", "QT_APTOS_2", "branco_2", "nulo_2", "branco_1", "nulo_1"]

    def metr(g):
        r = pd.DataFrame({
            "lula1": 100 * g.v13_1 / g.validos_1, "lula2": 100 * g.v13_2 / g.validos_2,
            "comp1": 100 * g.QT_COMPARECIMENTO_1 / g.QT_APTOS_1, "comp2": 100 * g.QT_COMPARECIMENTO_2 / g.QT_APTOS_2,
            "bn2": 100 * (g.branco_2 + g.nulo_2) / g.QT_COMPARECIMENTO_2, "eleitores": g.QT_APTOS_2,
            "votos_lula2": g.v13_2, "votos_adv2": g.v22_2,
            "ganho_lula": g.v13_2 - g.v13_1, "ganho_adv": g.v22_2 - g.v22_1})
        r["virada"] = r.lula2 - r.lula1
        r["dcomp"] = r.comp2 - r.comp1
        return r.round(3)

    mun = b.groupby(["SG_UF", "CD_MUNICIPIO"])[cols].sum()
    mm = metr(mun).reset_index()
    nac_virada = 100 * (b.v13_2.sum() / b.validos_2.sum() - b.v13_1.sum() / b.validos_1.sum())
    mm["virada_rel"] = (mm["virada"] - nac_virada).round(3)
    dv = os.path.join(AQUI, f"divergencias_municipios_{ano}_completo.csv")
    if os.path.exists(dv):
        d = pd.read_csv(dv, sep=";", dtype={"mun": str})
        d["SG_UF"] = d["mun"].str.split("-").str[0]
        d["CD_MUNICIPIO"] = d["mun"].str.split("-").str[1]
        mm = mm.merge(d[["SG_UF", "CD_MUNICIPIO", "zg", "sig"]].rename(columns={"zg": "z_div", "sig": "div_sig"}), how="left",
                      on=["SG_UF", "CD_MUNICIPIO"])
    mm["ibge"] = [ibge.get((u, c), (None, None))[0] for u, c in zip(mm.SG_UF, mm.CD_MUNICIPIO)]
    mm["nome"] = [ibge.get((u, c), (None, None))[1] for u, c in zip(mm.SG_UF, mm.CD_MUNICIPIO)]
    sem = mm["ibge"].isna().sum()
    mm = mm[mm["ibge"].notna()]
    municipios = {r.ibge: {k: (None if pd.isna(getattr(r, k)) else (bool(getattr(r, k)) if k == "div_sig" else
                                                                       (round(float(getattr(r, k)), 3) if k not in ("eleitores", "ganho_lula", "ganho_adv", "votos_lula2", "votos_adv2") else int(getattr(r, k)))))
                           for k in ("lula1", "lula2", "virada", "virada_rel", "comp1", "comp2", "dcomp", "bn2", "eleitores", "z_div", "div_sig",
                                     "ganho_lula", "ganho_adv", "votos_lula2", "votos_adv2")
                           if k in mm.columns} | {"nome": r.nome, "uf": r.SG_UF} for r in mm.itertuples()}
    uf = metr(b.groupby("SG_UF")[cols].sum())
    uf["virada_rel"] = uf["virada"] - nac_virada
    ufs = {u: {k: float(v) for k, v in row.items()} for u, row in uf.round(3).to_dict("index").items()}  # inclui ganhos e eleitores
    nac = metr(b[cols].sum().to_frame().T).iloc[0].to_dict()

    # fluxos de votos (C06)
    comp = json.load(open(os.path.join(AQUI, f"resultado_comportamento_{ano}.json")))["C06"]
    linhas, colunas = comp["linhas"], comp["colunas"]
    M = np.array(comp["matriz"])
    eleit = np.array([comp["eleitores_1t"][l] for l in linhas])
    fluxo_nac = (eleit[:, None] * M).round(0)
    fluxos_uf = {}
    for u, dd in comp.get("por_uf", {}).items():
        fluxos_uf[u] = (np.array(dd["eleitores_por_grupo"])[:, None] * np.array(dd["matriz"])).round(0).astype(int).tolist()
    bat = json.load(open(os.path.join(AQUI, f"resultado_bateria_{ano}.json")))
    klimek = {k: v["hist2d"] for k, v in bat.get("T25", {}).items() if "hist2d" in v}
    # versão em bolinhas: grade 20 x 20 (comparecimento x % do candidato), contagem de seções por célula
    klimek20 = {}
    for k, H in klimek.items():
        H = np.array(H)  # 50 x 50, classes de 2%
        bordas = np.linspace(0, 50, 21).astype(int)
        G = np.array([[H[bordas[i]:bordas[i + 1], bordas[j]:bordas[j + 1]].sum() for j in range(20)] for i in range(20)])
        klimek20[k] = G.astype(int).tolist()
    out["anos"][ano] = {"nacional": {k: round(float(v), 3) for k, v in nac.items()}, "virada_nacional": round(float(nac_virada), 3),
                        "municipios": municipios, "ufs": ufs, "municipios_sem_codigo_ibge": int(sem),
                        "fluxo": {"linhas": linhas, "colunas": colunas, "votos": fluxo_nac.astype(int).tolist(), "por_uf": fluxos_uf,
                                  "conferencia_previsto": comp.get("conferencia_total_previsto"), "conferencia_observado": comp.get("conferencia_total_observado")},
                        "klimek": klimek, "klimek20": klimek20}
    print(ano, "municípios no mapa:", len(municipios), "| sem código IBGE:", sem, "| virada nacional", round(nac_virada, 2), "pp")
json.dump(out, open(os.path.join(WEB, "mapas_dados.json"), "w"), ensure_ascii=False, separators=(",", ":"))
print("ok", round(os.path.getsize(os.path.join(WEB, "mapas_dados.json")) / 1e6, 1), "MB")
