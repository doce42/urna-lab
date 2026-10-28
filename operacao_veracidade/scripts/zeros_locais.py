"""T64 (exploratório, descritivo): os zeros de um finalista no 2º turno se concentram em locais de votação? (feito depois de ver o resultado dos modelos)"""
import json
import numpy as np, pandas as pd
R = "."; out = {"rotulo": "exploratorio_pos_hoc"}
for ano, arq, col, nome in (("2022", "base_2022.parquet", "v22_2", "Bolsonaro"), ("2026", "base.parquet", "v22_2", "Flavio")):
    b = pd.read_parquet(f"{R}/analise/{arq}"); b = b[(b.SG_UF != "ZZ") & (b.validos_2 > 0)].copy()
    b["loc"] = b.SG_UF + "|" + b.CD_MUNICIPIO.astype(str) + "|" + b.NR_ZONA.astype(str) + "|" + b.NR_LOCAL_VOTACAO_2.astype(str)
    b["x"] = b[col].fillna(0); z = b[b.x == 0]
    g = b.groupby("loc").agg(n_sec=("x", "size"), zeros=("x", lambda s: int((s == 0).sum())), x=("x", "sum"), v=("validos_2", "sum"))
    gz = g.loc[z.loc.unique()] if hasattr(z, "loc") and False else g[g.zeros > 0]
    z_por_loc = z.groupby("loc").size()
    out[ano] = {"candidato": nome, "secoes_zero": int(len(z)), "locais_com_zero": int(len(gz)), "zeros_em_locais_com_mais_de_um_zero": int(z_por_loc[z_por_loc > 1].sum()),
                "zeros_em_locais_onde_todas_as_secoes_sao_zero": int(gz[gz.zeros == gz.n_sec].zeros.sum()), "zeros_em_locais_com_participacao_total_menor_que_1pct": int(gz[gz.x / gz.v < .01].zeros.sum()),
                "mediana_votos_validos_da_secao_zero": float(z.validos_2.median()), "mediana_votos_validos_todas": float(b.validos_2.median()),
                "secoes_zero_com_menos_de_100_validos": int((z.validos_2 < 100).sum())}
json.dump(out, open(f"{R}/operacao_veracidade/resultados/zeros_locais.json", "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1))
