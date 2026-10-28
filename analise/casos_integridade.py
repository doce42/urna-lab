"""T36: classificação, caso a caso, das urnas cujas verificações de integridade não fecham exatamente (DIRETRIZ, nível 3).

Para cada urna com divergência em (a) votos no log x comparecimento, (b) confirmações para Presidente + nulos por
suspensão x total do BU, (c) certificado x urnas que registraram votos no log, (d) seção com arquivos mas fora do BU
na Web, testa explicações operacionais conhecidas, nesta ordem:
  E1 urna de contingência reaproveitada: a diferença do log é exatamente o comparecimento de OUTRA seção da mesma zona
     em que uma das urnas do log foi a urna efetivada
  E2 recuperação de dados (RED) ou correspondência alterada: o CEFT declara origem "BU gerado por RED" ou divergência
  E3 urna substituída no meio do dia (log com votos de 2+ urnas)
  E4 diferença de 1 confirmação sem voto computado (voto interrompido)
  E5 queda de energia/reinício da urna entre a confirmação do voto e o registro "computado" no log (o voto está no
     RDV e no BU; só a linha do log se perdeu): eleitor habilitado e voto confirmado seguidos de "Urna ligada"
  D1 arquivo listado na lista assinada pela urna mas ausente da publicação oficial (pacote e site de resultados)
O que não se encaixa fica como "sem explicação" e entra no relatório como classe D (inconsistência verificável).
Uso: python casos_integridade.py <turno>
"""
import glob
import json
import os
import sys
import zipfile

import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
T = int(sys.argv[1]) if len(sys.argv) > 1 else 2
u = pd.concat([pd.read_parquet(a) for a in glob.glob(os.path.join(AQUI, "brutos", f"{T}t", "urnas_*.parquet"))], ignore_index=True)
b = pd.read_parquet(os.path.join(AQUI, "base.parquet"))
b = b[b[f"total_{T}"].notna()]
k = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
x = u.merge(b, on=k, how="outer", indicator=True)
# CEFT
ceft = []
for z in glob.glob(os.path.join(AQUI, "..", "dados", "correspondencias_gedai", f"CEFT_{T}t_*.zip")):
    with zipfile.ZipFile(z) as zf:
        ceft.append(pd.read_csv(zf.open([n for n in zf.namelist() if n.endswith(".csv")][0]), sep=";", encoding="latin1", dtype=str))
c = pd.concat(ceft)
c["CD_MUNICIPIO"] = c["CD_MUNICIPIO"].astype(int).astype(str)
c = c.sort_values("DT_GERACAO").drop_duplicates(k, keep="last")[k + ["DS_ORIGEM_VOTO", "TP_DIVERGENCIA", "NR_URNA_ESPERADA", "NR_URNA_EFETIVADA"]]
x = x.merge(c, on=k, how="left")
comp = x[f"QT_COMPARECIMENTO_{T}"]
tot = x[["bu_v13", "bu_v22", "bu_branco", "bu_nulo"]].fillna(0).sum(axis=1) if "bu_v13" in x else None
sa = x["origem"].eq("sistema_de_apuracao") if "origem" in x else pd.Series(False, index=x.index)
casos = []
# índice: comparecimento das seções por (UF, município, zona, urna efetivada)
comp_por_urna = {}
for r in x[x["_merge"] == "both"].itertuples():
    comp_por_urna.setdefault((r.SG_UF, r.CD_MUNICIPIO, r.NR_ZONA), {})[int(getattr(r, f"NR_URNA_EFETIVADA_{T}"))] = int(getattr(r, f"QT_COMPARECIMENTO_{T}"))

import sys as _s
_s.path.insert(0, AQUI)
import processar_brutos as pb  # noqa: E402


def _zip(r, T):
    return zipfile.ZipFile(os.path.join(AQUI, "..", "dados", "brutos", "1turno" if T == 1 else "2turno_pacotes",
                                        f"bu_imgbu_logjez_rdv_vscmr_2026_{T}t_{r.SG_UF}.zip"))


def _prefixo(r, T):
    return f"o0322{T - 1}{r.SG_UF.lower()}{int(r.CD_MUNICIPIO):05d}{int(r.NR_ZONA):04d}{int(r.NR_SECAO):04d}"


def explica_energia(r, T):
    try:
        linhas, _ = pb.linhas_do_log(_zip(r, T).read(_prefixo(r, T) + "-log.jez"))
    except KeyError:
        return []
    ev = [l.split("\t")[4] for l in linhas if l.startswith(pb.DIA[T]) and len(l.split("\t")) > 4]
    for i, m in enumerate(ev):
        if m.startswith("Eleitor foi habilitado"):
            j = i + 1
            while j < len(ev) and not ev[j].startswith(("O voto do eleitor foi computado", "Eleitor foi habilitado")):
                if ev[j].startswith("Urna ligada em"):
                    return ["E5 queda de energia/reinício entre a confirmação e o registro do voto no log"]
                j += 1
    return []


def explica_publicacao(r, T):
    z = _zip(r, T); pre = _prefixo(r, T)
    try:
        lista, _, _ = pb.ler_vsc(z.read(pre + "-vota.vsc"))
    except KeyError:
        return []
    publicados = {n for n in z.namelist() if n.startswith(pre)}
    faltam = [n.split("-")[-1] for n in lista if n.endswith(("log.jez", "imgbu.dat")) and n not in publicados]
    return [f"D1 arquivo(s) {faltam} na lista assinada pela urna, mas ausente(s) da publicação oficial"] if faltam else []


for i, r in x.iterrows():
    tipos = []
    if r["_merge"] == "left_only":
        tipos.append("d_fora_do_bu")
    elif not sa[i]:
        if pd.notna(r.get("computado")) and r["computado"] != comp[i]:
            tipos.append("a_log_x_comparecimento")
        if tot is not None and pd.notna(r.get("conf_presidente")) and r["conf_presidente"] + r["nulo_suspensao_presidente"] != tot[i]:
            tipos.append("b_confirmacoes_x_total")
        if not bool(r.get("cert_igual_log")) and pd.notna(r.get("cert_urna")):
            tipos.append("c_certificado_x_log")
    if not tipos:
        continue
    exp = []
    ids = [int(v) for v in str(r.get("ids_urna_log") or "").split(",") if v.isdigit()]
    if "a_log_x_comparecimento" in tipos and pd.notna(r.get("computado")):
        dif = int(r["computado"] - comp[i])
        outras = comp_por_urna.get((r.SG_UF, r.CD_MUNICIPIO, r.NR_ZONA), {})
        efet = int(r[f"NR_URNA_EFETIVADA_{T}"]) if pd.notna(r.get(f"NR_URNA_EFETIVADA_{T}")) else None
        if dif > 0 and any(outras.get(j) == dif for j in ids if j != efet):
            exp.append("E1 urna de contingência reaproveitada (diferença = comparecimento de outra seção da zona)")
    if str(r.get("DS_ORIGEM_VOTO", "")).startswith("BU gerado por RED") or (pd.notna(r.get("TP_DIVERGENCIA")) and r.get("TP_DIVERGENCIA")):
        exp.append(f"E2 CEFT: origem '{r.get('DS_ORIGEM_VOTO')}', divergência '{r.get('TP_DIVERGENCIA')}'")
    if pd.notna(r.get("urnas_com_voto_no_log")) and r["urnas_com_voto_no_log"] > 1:
        exp.append("E3 urna substituída no meio do dia")
    if tipos == ["b_confirmacoes_x_total"] and tot is not None and r["conf_presidente"] + r["nulo_suspensao_presidente"] - tot[i] == 1:
        exp.append("E4 uma confirmação sem voto computado (voto interrompido)")
    if not exp and "a_log_x_comparecimento" in tipos and pd.notna(r.get("computado")) and r["computado"] < comp[i]:
        exp += explica_energia(r, T)
    if not exp and "c_certificado_x_log" in tipos and pd.isna(r.get("computado")):
        exp += explica_publicacao(r, T)
    casos.append({"uf": r.SG_UF, "municipio": r.CD_MUNICIPIO, "zona": r.NR_ZONA, "secao": r.NR_SECAO, "tipos": tipos,
                  "log": None if pd.isna(r.get("computado")) else int(r["computado"]), "comparecimento": None if pd.isna(comp[i]) else int(comp[i]),
                  "cert": r.get("cert_urna"), "urnas_log": r.get("ids_urna_log"), "origem_ceft": r.get("DS_ORIGEM_VOTO"),
                  "explicacoes": exp, "explicado": bool(exp)})
R = {"turno": T, "urnas_avaliadas": int((x["_merge"] == "both").sum()), "casos": len(casos),
     "explicados_operacionais": sum(c_["explicado"] and not any(e.startswith("D1") for e in c_["explicacoes"]) for c_ in casos),
     "inconsistencias_de_publicacao_D1": sum(any(e.startswith("D1") for e in c_["explicacoes"]) for c_ in casos),
     "sem_explicacao": sum(not c_["explicado"] for c_ in casos),
     "por_tipo": pd.Series([t for c_ in casos for t in c_["tipos"]]).value_counts().to_dict(),
     "por_explicacao": pd.Series([e.split(" ")[0] for c_ in casos for e in c_["explicacoes"]]).value_counts().to_dict(),
     "casos_lista": casos}
json.dump(R, open(os.path.join(AQUI, f"resultado_casos_integridade_{T}t.json"), "w"), ensure_ascii=False, indent=1, default=str)
print({k_: v for k_, v in R.items() if k_ != "casos_lista"})
for c_ in casos:
    if not c_["explicado"]:
        print("  SEM EXPLICAÇÃO:", c_["uf"], c_["municipio"], c_["zona"], c_["secao"], c_["tipos"], "log", c_["log"], "comp", c_["comparecimento"], "cert", c_["cert"], "urnas", c_["urnas_log"], "origem", c_["origem_ceft"])
