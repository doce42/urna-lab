"""Acrescenta ao web/dados.json a curva PREVISTA do 2º turno (rodar depois do montar_dados.py, com o .venv).

Cada urna "vota" o % que ela deu ao Lula no 1º turno mais a virada típica:
  p13m/p22m: virada das OUTRAS seções do mesmo município (sem a própria seção)
  p13e/p22e: virada mediana do estado (mais independente; diferenças dentro do estado aparecem como desvio)
A soma é feita no mesmo segundo que a curva real, nos dois eixos de tempo.
"""
import json
import os

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
b = pd.read_parquet(os.path.join(AQUI, "..", "analise", "base.parquet"))
b = b[b["total_2"].notna()].copy()
b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
inv = lambda z: 1 / (1 + np.exp(-z))
tem1 = b["validos_1"].fillna(0) > 0
b["sw"] = np.where(tem1 & (b["validos_2"] > 0), lg(b["v13_2"], b["validos_2"]) - lg(b["v13_1"].fillna(0), b["validos_1"].fillna(0)), np.nan)
b["sw_e"] = b.groupby("SG_UF")["sw"].transform("median")
g = b.groupby("mun")["sw"]
n = g.transform("count")
b["sw_m"] = np.where(n > 1, (g.transform("sum") - b["sw"].fillna(0)) / (n - b["sw"].notna()).clip(lower=1), b["sw_e"])
for k in ("m", "e"):
    p = inv(lg(b["v13_1"].fillna(0), b["validos_1"].fillna(0)) + b[f"sw_{k}"])
    # seção sem 1º turno comparável: previsto = real (não inventa nada)
    b[f"p13{k}"] = np.where(tem1, p * b["validos_2"], b["v13_2"])
    b[f"p22{k}"] = b["validos_2"] - b[f"p13{k}"]

dia = pd.Timestamp("2026-10-25")
seg = lambda s: (s - dia).dt.total_seconds().astype("Int64")
b["t_recebido"] = seg(b["DT_BU_RECEBIDO_2"])
# fuso igual ao montar_dados.py: urnas que abriram nos primeiros 15 min, moda do município (senão do estado)
ab = b["DT_ABERTURA_2"]
ok = ab.dt.hour.between(6, 8) & (ab.dt.minute < 15)
fz = 8 - ab.dt.hour
f_m = fz[ok].groupby(b["mun"][ok]).agg(lambda s: s.mode().iloc[0])
f_e = fz[ok].groupby(b["SG_UF"][ok]).agg(lambda s: s.mode().iloc[0])
fuso = b["mun"].map(f_m).fillna(b["SG_UF"].map(f_e))
b["t_emissao"] = seg(b["DT_EMISSAO_BU_2"] + pd.to_timedelta(fuso, unit="h"))
b.loc[b["SG_UF"] == "ZZ", "t_emissao"] = pd.NA

arq = os.path.join(AQUI, "web", "dados.json")
d = json.load(open(arq))
for eixo in ("recebido", "emissao"):
    s = d["t2"][eixo]
    x = b[b[f"t_{eixo}"].notna()]
    soma = x.groupby(f"t_{eixo}")[["p13m", "p22m", "p13e", "p22e", "v13_2"]].sum()
    soma = soma.reindex(s["t"])
    if soma.isna().any().any():
        raise SystemExit(f"{eixo}: segundos da previsão não batem com a curva real")
    if not np.array_equal(soma["v13_2"].round().astype(int).values, np.array(s["c13"])):
        raise SystemExit(f"{eixo}: votos reais não batem segundo a segundo, parei")
    for k in ("p13m", "p22m", "p13e", "p22e"):
        s[k] = [round(v, 2) for v in soma[k]]
    print(f"{eixo}: ok, previsto final Lula {soma['p13m'].sum()/(soma['p13m'].sum()+soma['p22m'].sum()):.4%} (município) "
          f"{soma['p13e'].sum()/(soma['p13e'].sum()+soma['p22e'].sum()):.4%} (estado)")
json.dump(d, open(arq, "w"), separators=(",", ":"))
