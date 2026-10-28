"""T57: nulos de presidente e 2º turno de governador (pré-registro em fase3/PREREG_NULOS_GOVERNADOR.md)."""
import json
import numpy as np, pandas as pd

AN = "analise"; OUT = "fase3/resultados/nulos_governador.json"
CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
GOV = {"2022": {"AL", "AM", "BA", "ES", "MS", "PB", "PE", "RO", "RS", "SC", "SE", "SP"}, "2026": {"AC", "AM", "DF", "ES", "RN", "TO"}}
R = {"pre_registro": "fase3/PREREG_NULOS_GOVERNADOR.md", "ufs_com_governador": {k: sorted(v) for k, v in GOV.items()}}
B = {}
for ano in ("2022", "2026"):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet"); b = b[b.SG_UF != "ZZ"].astype({c: str for c in CH}); B[ano] = b
    b["gov"] = b.SG_UF.isin(GOV[ano])
    r = {}
    for t in (1, 2):
        g = b.groupby("gov")[[f"branco_{t}", f"nulo_{t}", f"total_{t}"]].sum()
        r[f"{t}t"] = {("com_governador" if k else "sem_governador"): {"brancos_pct": float(100 * x[f"branco_{t}"] / x[f"total_{t}"]), "nulos_pct": float(100 * x[f"nulo_{t}"] / x[f"total_{t}"]),
                                                                      "total": int(x[f"total_{t}"])} for k, x in g.iterrows()}
    uf = b.groupby("SG_UF")[["nulo_1", "total_1", "nulo_2", "total_2"]].sum()
    r["nulos_2t_menos_1t_pp_por_uf"] = (100 * (uf.nulo_2 / uf.total_2 - uf.nulo_1 / uf.total_1)).round(2).to_dict()
    R[ano] = r
# (b) contrafactual de composição: taxas de 2026 por grupo aplicadas à composição de 2022 (participação dos votos nas UFs com governador)
t26 = R["2026"]["2t"]; share22 = R["2022"]["2t"]["com_governador"]["total"] / (R["2022"]["2t"]["com_governador"]["total"] + R["2022"]["2t"]["sem_governador"]["total"])
# a mesma UF muda de grupo; usa-se a diferença média de nulos entre os grupos em cada ano como efeito do 2º turno de governador
ef = {a: R[a]["2t"]["com_governador"]["nulos_pct"] - R[a]["2t"]["sem_governador"]["nulos_pct"] for a in ("2022", "2026")}
share26 = R["2026"]["2t"]["com_governador"]["total"] / (R["2026"]["2t"]["com_governador"]["total"] + R["2026"]["2t"]["sem_governador"]["total"])
tot26 = R["2026"]["2t"]["com_governador"]["total"] + R["2026"]["2t"]["sem_governador"]["total"]
R["b_composicao"] = {"efeito_governador_nulos_pp": ef, "fracao_votos_em_ufs_com_governador": {"2022": share22, "2026": share26},
                     "nulos_explicados_pela_composicao": int(np.mean(list(ef.values())) / 100 * (share22 - share26) * tot26)}
# (c) UFs sem governador nos dois anos, seções pareadas
sem = set(B["2026"].SG_UF) - GOV["2022"] - GOV["2026"]
m = B["2026"].merge(B["2022"], on=CH, suffixes=("", "_22")); m = m[m.SG_UF.isin(sem) & (m.total_2 >= 50) & (m.total_2_22 >= 50)]
bn2 = (m.branco_2 + m.nulo_2) / m.total_2 - (m.branco_2_22 + m.nulo_2_22) / m.total_2_22
q = pd.qcut(m.v13_2_22 / m.validos_2_22, 5, labels=["Q1 (menos Lula)", "Q2", "Q3", "Q4", "Q5 (mais Lula)"])
tot = lambda d, s: int((d[f"branco_{s}"] + d[f"nulo_{s}"]).sum())
R["c_sem_governador_nos_dois_anos"] = {"ufs": sorted(sem), "secoes": int(len(m)), "bn_2t_2022": tot(m, "2_22"), "bn_2t_2026": tot(m, "2"),
                                       "queda_2t_pp_media": float(100 * bn2.mean()), "queda_2t_por_quintil_lula22_pp": (100 * bn2.groupby(q, observed=True).mean()).round(2).to_dict()}
json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k not in ("2022", "2026")}, ensure_ascii=False))
print({a: {u: R[a]["nulos_2t_menos_1t_pp_por_uf"][u] for u in sorted(GOV["2022"] | GOV["2026"])} for a in ("2022", "2026")})
