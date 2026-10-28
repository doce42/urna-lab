"""Junta os resultados para a página de relatório (grafico/web/relatorio_dados.json)
e gera os votos por minuto dos logs das urnas para o gráfico principal (grafico/web/logs.json).

Rodar depois de: montar_base.py, curva.py, poder.py, biometria.py e (para os logs) processar_brutos.py.
"""
import glob
import json
import os

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(AQUI, "..", "grafico", "web")
b = pd.read_parquet(os.path.join(AQUI, "base.parquet"))
b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
out = {}

# Totais oficiais por turno
for n in (1, 2):
    cols = [c for c in b.columns if c.endswith(f"_{n}") and (c.startswith("v") and c != f"validos_{n}" or c in (f"branco_{n}", f"nulo_{n}"))]
    out[f"totais_{n}"] = {c.rsplit("_", 1)[0]: int(b[c].sum()) for c in cols}
    out[f"urnas_{n}"] = int(b[f"total_{n}"].notna().sum())

# T02: distribuição do z robusto da virada (logit, resíduo do município)
s = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20)].copy()
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
x1, n1, x2, n2 = s["v13_1"], s["validos_1"], s["v13_2"], s["validos_2"]
s["sw"] = lg(x2, n2) - lg(x1, n1)
s["res"] = s["sw"] - s.groupby("mun")["sw"].transform("median")
z = s["res"] / np.sqrt(1/(x1+.5) + 1/(n1-x1+.5) + 1/(x2+.5) + 1/(n2-x2+.5))
z = z / (1.4826 * (z - z.median()).abs().median())
bordas = np.arange(-8, 8.5, 0.5)
h, _ = np.histogram(z.clip(-8, 8), bordas)
out["z_hist"] = {"bordas": bordas.tolist(), "contagem": h.tolist(), "n": int(len(z)),
                 "acima5_lula": int((z > 5).sum()), "acima5_flavio": int((z < -5).sum())}

# T10: curva real x prevista (2º turno, por minuto)
c = pd.read_csv(os.path.join(AQUI, "curva_2turno_por_minuto.csv"), sep=";", parse_dates=["min"])
c = c[c["min"] >= "2026-10-25 17:00"].set_index("min")
# todos os minutos da noite (sem urna chegando, a curva acumulada fica parada): tempo proporcional no eixo
c = c[["acum", "acum_prev", "acum_prev_uf"]].reindex(pd.date_range(c.index.min(), c.index.max(), freq="1min")).ffill()
c = c.rename_axis("min").reset_index()
depois19 = c[c["min"] >= "2026-10-25 19:00"]
out["curva_max_desvio"] = {"noite_toda": float(100 * (c.acum - c.acum_prev).abs().max()),
                           "depois_19h": float(100 * (depois19.acum - depois19.acum_prev).abs().max())}
out["curva"] = {"hora": c["min"].dt.strftime("%H:%M").tolist(), "real": (100 * c["acum"]).round(4).tolist(),
                "prev_mun": (100 * c["acum_prev"]).round(4).tolist(), "prev_uf": (100 * c["acum_prev_uf"]).round(4).tolist()}

# T13 e T12
out["poder"] = json.load(open(os.path.join(AQUI, "resultado_poder.json")))
out["biometria"] = json.load(open(os.path.join(AQUI, "resultado_biometria.json")))

# Logs das urnas: votos por minuto no horário de Brasília (fuso do município pela abertura às 8h de Brasília)
logs, log_resumo = {}, {}
for n in (1, 2):
    arqs = sorted(glob.glob(os.path.join(AQUI, "brutos", f"{n}t", "minutos_*.parquet")))
    if not arqs:
        continue
    m = pd.concat([pd.read_parquet(a) for a in arqs])
    ab = b[f"DT_ABERTURA_{n}"]
    ok = ab.dt.hour.between(6, 8) & (ab.dt.minute < 15)
    fz = (8 - ab.dt.hour)[ok].groupby(b["mun"][ok]).agg(lambda v: v.mode().iloc[0])
    m["mun"] = m["SG_UF"] + m["CD_MUNICIPIO"]
    m["fuso"] = m["mun"].map(fz)
    m = m[m["SG_UF"] != "ZZ"].dropna(subset=["fuso"])  # exterior: cada país tem seu fuso
    dia = pd.Timestamp("2026-10-04" if n == 1 else "2026-10-25")
    t = pd.to_datetime(m["minuto"], format="%d/%m/%Y %H:%M") + pd.to_timedelta(m["fuso"], unit="h")
    m["s"] = ((t - dia).dt.total_seconds()).astype(int)
    g = m.groupby("s")["votos"].sum().sort_index()
    g = g[(g.index >= 6 * 3600) & (g.index <= 22 * 3600)]  # dia da eleição (descarta testes de preparação)
    logs[f"t{n}"] = {"t": g.index.tolist(), "votos": g.values.tolist(), "urnas": [0] * len(g)}
    u = pd.concat([pd.read_parquet(a) for a in glob.glob(os.path.join(AQUI, "brutos", f"{n}t", "urnas_*.parquet"))])
    votaveis = [c for c in b.columns if c.endswith(f"_{n}") and (c[0] == "v" and c != f"validos_{n}" or c in (f"branco_{n}", f"nulo_{n}"))]
    u = u.merge(b[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", f"QT_COMPARECIMENTO_{n}", f"total_{n}"] + votaveis],
                on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"], how="left")
    r = {"urnas": int(len(u)), "votos_log": int(u["computado"].sum()),
         "log_igual_comparecimento": int((u["computado"] == u[f"QT_COMPARECIMENTO_{n}"]).sum()),
         "modelos": u["modelo"].value_counts().to_dict()}
    if "conf_presidente" in u and "img_total" in u:
        tot = u["conf_presidente"] + u["nulo_suspensao_presidente"]
        r["confirmacoes_igual_total"] = int((tot == u["img_total"]).sum())
        r["urnas_com_imgbu"] = int(u["img_total"].notna().sum())
    if "rdv_branco" in u or "rdv_nulo" in u:
        # recontagem pelo RDV x boletim, votável por votável (nulo do RDV inclui os outros tipos, como nulo por suspensão)
        ok = pd.Series(True, index=u.index)
        for c in votaveis:
            k = c.rsplit("_", 1)[0]
            if k == "nulo":
                rdv = u.get("rdv_nulo", 0).fillna(0) + u.filter(like="rdv_tipo").fillna(0).sum(axis=1)
            else:
                rdv = u.get(f"rdv_{k}", pd.Series(0, index=u.index)).fillna(0)
            ok &= rdv == u[c].fillna(0)
        r["rdv_igual_boletim"] = int(ok.sum())
        r["urnas_com_rdv"] = int(u.filter(like="rdv_").notna().any(axis=1).sum())
    for t in ("bu", "rdv", "imgbu", "log"):
        for pre in ("hash_ok", "assin_ok"):
            if f"{pre}_{t}" in u:
                r[f"{pre}_{t}"] = [int(u[f"{pre}_{t}"].fillna(False).astype(bool).sum()), int(u[f"{pre}_{t}"].notna().sum())]
    if "assin_lista_ok" in u:
        r["assin_lista_ok"] = int(u["assin_lista_ok"].fillna(False).astype(bool).sum())
        r["algoritmos"] = u["algoritmo"].value_counts().to_dict()
        r["emissores"] = u["cert_emissor"].value_counts().to_dict()
        r["cert_aparece_no_log"] = int(u["cert_igual_log"].fillna(False).astype(bool).sum())
        r["urnas_substituidas"] = int((u["urnas_com_voto_no_log"] > 1).sum())
        r["erros_leitura"] = int(u["erro"].notna().sum()) if "erro" in u else 0
    log_resumo[f"t{n}"] = r
if logs:
    json.dump(logs, open(os.path.join(WEB, "logs.json"), "w"), separators=(",", ":"))
out["logs"] = {k: {"hora": [f"{s // 3600:02d}:{s % 3600 // 60:02d}" for s in v["t"]], "votos": v["votos"]} for k, v in logs.items()}
out["log_resumo"] = log_resumo
out["bateria"] = {a: json.load(open(os.path.join(AQUI, f"resultado_bateria_{a}.json")))
                  for a in ("2022", "2026") if os.path.exists(os.path.join(AQUI, f"resultado_bateria_{a}.json"))}

# ---- resultados novos (logs, casos de integridade, correspondência, divergências, sensibilidade) ----
def _j(nome):
    f = os.path.join(AQUI, nome)
    return json.load(open(f)) if os.path.exists(f) else None


novos = {}
for t in (1, 2):
    r = _j(f"resultado_logs_{t}t.json")
    if r:
        r["T28"].pop("exemplos", None)
        r.pop("CONF_T02_lista", None)
        novos[f"logs_{t}t"] = r
    r = _j(f"resultado_casos_integridade_{t}t.json")
    if r:
        novos[f"casos_{t}t"] = r
    r = _j(f"resultado_correspondencia_{t}t.json")
    if r:
        r.pop("T34_exemplos_diferenca", None)
        novos[f"correspondencia_{t}t"] = r
for a in ("2022", "2026"):
    r = _j(f"resultado_divergencias_{a}_completo.json")
    if r:
        r["E03"] = {n: v[:10] for n, v in r["E03"].items()}
        novos[f"divergencias_{a}"] = r
    r = _j(f"resultado_sensibilidade_{a}.json")
    if r:
        novos[f"sensibilidade_{a}"] = r
    r = _j(f"resultado_ml_{a}.json")
    if r:
        novos[f"ml_{a}"] = r
out["novos"] = novos

def _limpa(x):
    """NaN e infinito não existem em JSON válido: viram null (o navegador recusa o arquivo inteiro se aparecerem)."""
    if isinstance(x, float):
        return None if (x != x or x in (float("inf"), float("-inf"))) else x
    if isinstance(x, dict):
        return {k: _limpa(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_limpa(v) for v in x]
    return x


json.dump(_limpa(out), open(os.path.join(WEB, "relatorio_dados.json"), "w"), ensure_ascii=False, separators=(",", ":"), allow_nan=False)
print("ok", list(out), {k: v["urnas"] for k, v in log_resumo.items()})
