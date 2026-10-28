"""T50: thread 'concentração do voto no PT' (pré-registro em fase3/PREREG_THREAD_CONCENTRACAO.md)."""
import json
import pandas as pd

AN = "analise"; OUT = "fase3/resultados/thread_concentracao.json"
CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
NNE = {"AC", "AM", "AP", "PA", "RO", "RR", "TO", "AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"}
b26 = pd.read_parquet(f"{AN}/base.parquet").astype({c: str for c in CH})
b22 = pd.read_parquet(f"{AN}/base_2022.parquet").astype({c: str for c in CH})
R = {"pre_registro": "fase3/PREREG_THREAD_CONCENTRACAO.md"}
for nome, b in (("2026", b26), ("2022", b22)):
    for escopo, q in (("brasil", b[b.SG_UF != "ZZ"]), ("com_exterior", b)):
        q = q[q.validos_2 > 0]; p13 = q.v13_2 / q.validos_2; p22 = q.v22_2.fillna(0) / q.validos_2
        alta = q[p13 > .8]; dif = q.v13_2 - q.v22_2.fillna(0)
        R[f"{nome}_{escopo}"] = {"secoes_13_acima_80": int(len(alta)), "secoes_22_acima_80": int((p22 > .8).sum()),
                                 "frac_13_acima_80_norte_nordeste": float(alta.SG_UF.isin(NNE).mean()),
                                 "secoes_13_vence": int((dif > 0).sum()), "vantagem_13_onde_vence": int(dif[dif > 0].sum()),
                                 "vantagem_22_onde_vence_ou_empata": int(-dif[dif <= 0].sum()), "saldo": int(dif.sum()),
                                 "saldo_das_secoes_13_acima_80": int(dif[p13 > .8].sum())}
x = b26[(b26.SG_UF != "ZZ") & (b26.validos_2 > 0)]; x = x[x.v13_2 / x.validos_2 > .8][CH].merge(
    b22[CH + ["v13_2", "validos_2"]], on=CH, how="left")
R["continuidade_2026_com_2022"] = {"secoes": int(len(x)), "com_par": int(x.v13_2.notna().sum()),
                                   "ja_acima_80_em_2022": int((x.v13_2 / x.validos_2 > .8).sum()),
                                   "frac_sobre_todas": float((x.v13_2 / x.validos_2 > .8).sum() / len(x)),
                                   "frac_sobre_pareadas": float((x.v13_2 / x.validos_2 > .8).sum() / x.v13_2.notna().sum())}
json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
