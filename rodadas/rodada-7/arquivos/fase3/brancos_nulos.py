"""T56: brancos e nulos entre turnos (pré-registro em fase3/PREREG_BRANCOS_NULOS.md)."""
import json
import numpy as np, pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; OUT = RAIZ + "/fase3/resultados/brancos_nulos.json"
CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
R = {"pre_registro": "fase3/PREREG_BRANCOS_NULOS.md"}
# (a) C06 já gravado
for ano in ("2022", "2026"):
    c = json.load(open(f"{AN}/resultado_comportamento_{ano}.json"))["C06"] if "C06" in json.load(open(f"{AN}/resultado_comportamento_{ano}.json")) else None
    c = c or json.load(open(f"{AN}/resultado_comportamento_{ano}.json"))
    i = [k for k, l in enumerate(c["linhas"]) if l.startswith("Branco")][0]
    linha = dict(zip(c["colunas"], c["matriz"][i]))
    uf = {u: dict(zip(c["colunas"], v["matriz"][i])) if isinstance(v, dict) and "matriz" in v else v for u, v in c["por_uf"].items()}
    R[f"a_{ano}"] = {"nacional": linha, "ufs_adversario_menor_5pct": sum(1 for v in uf.values() if isinstance(v, dict) and v.get("Adversário", 1) < .05),
                     "ufs": len(uf), "por_uf_adversario": {u: round(v.get("Adversário", float("nan")), 3) for u, v in uf.items() if isinstance(v, dict)}}
# (b) e (d) totais
for ano in ("2022", "2026"):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
    R[f"b_{ano}"] = {f"{t}t": {"brancos": int(b[f"branco_{t}"].sum()), "nulos": int(b[f"nulo_{t}"].sum()), "soma": int((b[f"branco_{t}"] + b[f"nulo_{t}"]).sum()),
                                "pct_do_total": float((b[f"branco_{t}"] + b[f"nulo_{t}"]).sum() / b[f"total_{t}"].sum())} for t in (1, 2)}
# (c) seções pareadas
b26 = pd.read_parquet(f"{AN}/base.parquet").astype({c: str for c in CH}); b22 = pd.read_parquet(f"{AN}/base_2022.parquet").astype({c: str for c in CH})
m = b26.merge(b22, on=CH, suffixes=("", "_22"))
m = m[(m.SG_UF != "ZZ") & (m.total_1 >= 50) & (m.total_2 >= 50) & (m.total_1_22 >= 50) & (m.total_2_22 >= 50)].copy()
m["mun"] = m.SG_UF + m.CD_MUNICIPIO
bn = lambda d, s: (d[f"branco_{s}"] + d[f"nulo_{s}"]) / d[f"total_{s}"]
m["exc1"] = bn(m, "1") - bn(m, "1_22"); m["exc2"] = bn(m, "2") - bn(m, "2_22")
m["lula22"] = m.v13_2_22 / m.validos_2_22
def incl(y):
    yd = y - y.groupby(m.mun).transform("mean"); xd = m.lula22 - m.lula22.groupby(m.mun).transform("mean")
    return float((yd * xd).sum() / (xd ** 2).sum())
q = pd.qcut(m.lula22, 5, labels=["Q1 (menos Lula)", "Q2", "Q3", "Q4", "Q5 (mais Lula)"])
R["c_pareadas"] = {"secoes": int(len(m)), "excesso_1t_medio_pp": float(100 * m.exc1.mean()), "excesso_2t_medio_pp": float(100 * m.exc2.mean()),
                   "inclinacao_exc1_por_lula22_dentro_mun": incl(m.exc1), "inclinacao_exc2_por_lula22_dentro_mun": incl(m.exc2),
                   "exc1_por_quintil_lula22_pp": (100 * m.exc1.groupby(q, observed=True).mean()).round(2).to_dict(),
                   "exc2_por_quintil_lula22_pp": (100 * m.exc2.groupby(q, observed=True).mean()).round(2).to_dict(),
                   "votos_exc1_quintil5": int((m.exc1 * m.total_1)[q == "Q5 (mais Lula)"].sum()), "votos_exc1_total": int((m.exc1 * m.total_1).sum())}
json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: v for k, v in R.items()}, ensure_ascii=False, indent=1, default=str)[:5000])
