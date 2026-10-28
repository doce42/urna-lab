"""Quebras e reversões na curva do 2º turno: cada lote que chegou votou como o 1º turno dele indicava?"""
import os

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
b = pd.read_parquet(os.path.join(AQUI, "base.parquet"))
b = b[b["total_2"].notna() & b["total_1"].notna() & (b["validos_2"] > 0) & (b["validos_1"] > 0)].copy()
b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
inv = lambda z: 1 / (1 + np.exp(-z))
b["sw"] = lg(b["v13_2"], b["validos_2"]) - lg(b["v13_1"], b["validos_1"])

# Previsão de cada urna: o % dela no 1º turno + a virada típica. Duas versões:
#  - virada do estado (mais conservadora: diferenças regionais dentro do estado viram "surpresa")
#  - virada do município sem a própria seção (leave-one-out), para não usar a resposta na pergunta
b["sw_uf"] = b.groupby("SG_UF")["sw"].transform("median")
g = b.groupby("mun")["sw"]
n = g.transform("size")
b["sw_mun"] = np.where(n > 1, (g.transform("sum") - b["sw"]) / (n - 1).clip(lower=1), b["sw_uf"])
for k in ("uf", "mun"):
    b[f"prev_{k}"] = inv(lg(b["v13_1"], b["validos_1"]) + b[f"sw_{k}"]) * b["validos_2"]
b["res_mun"] = b["v13_2"] - b["prev_mun"]
b["res_uf"] = b["v13_2"] - b["prev_uf"]

b = b.sort_values("DT_BU_RECEBIDO_2")
b["min"] = b["DT_BU_RECEBIDO_2"].dt.floor("1min")
w = b.groupby("min").agg(urnas=("v13_2", "size"), lula=("v13_2", "sum"), val=("validos_2", "sum"),
                         prev_uf=("prev_uf", "sum"), prev_mun=("prev_mun", "sum"),
                         res_mun=("res_mun", "sum"), res_uf=("res_uf", "sum"),
                         ufs=("SG_UF", lambda s: ", ".join(f"{k} {v}" for k, v in s.value_counts().head(3).items())))
w["acum"] = w["lula"].cumsum() / w["val"].cumsum()
w["lote"] = w["lula"] / w["val"]

# Quanto um lote de k urnas sorteadas ao acaso erraria a previsão: escala o desvio por urna
for k in ("mun", "uf"):
    r = b[f"res_{k}"]
    w[f"z_{k}"] = (w[f"res_{k}"] - w["urnas"] * r.mean()) / np.sqrt(w["urnas"] * r.var())
    w[f"erro_{k}_pp"] = 100 * w[f"res_{k}"] / w["val"]

print(f"minutos com urnas chegando: {len(w)}; urnas {int(w.urnas.sum()):,}")
print(f"% do Lula na curva acumulada: começou {100*w.acum.iloc[0]:.2f}%, mín {100*w.acum.min():.2f}% às {w.acum.idxmin().time()}, "
      f"máx {100*w.acum.max():.2f}% às {w.acum.idxmax().time()}, final {100*w.acum.iloc[-1]:.2f}%")

print("\n== Reversões da curva acumulada (mudança de direção de pelo menos 0,05 pp, depois das 19h)")
c = w[w.index >= "2026-10-25 19:00"]["acum"]
piv, dirn, ext, ext_t = [], 0, c.iloc[0], c.index[0]
for t, v in c.items():
    if dirn >= 0 and v > ext or dirn <= 0 and v < ext:
        ext, ext_t = v, t
    if dirn >= 0 and v < ext - .0005 or dirn <= 0 and v > ext + .0005:
        if dirn != 0:
            piv.append((ext_t, ext, "topo" if dirn > 0 else "fundo"))
        dirn = -1 if v < ext else 1
        ext, ext_t = v, t
print(f"  {len(piv)} reversões")
for t, v, tipo in piv:
    lo = w.loc[t]
    prox = w.loc[t:].iloc[1:6]
    print(f"  {t.time()} {tipo:5} {100*v:.2f}% | lotes seguintes: {100*prox.lula.sum()/prox.val.sum():.1f}% Lula, "
          f"previsto pelo 1º turno {100*prox.prev_mun.sum()/prox.val.sum():.1f}% | de: {prox.iloc[0].ufs}")

print("\n== Cada minuto: o lote votou como o 1º turno dele indicava?")
print(f"  erro da previsão por minuto (pp do Lula), previsão pelo município: mediana {w.erro_mun_pp.abs().median():.2f}, "
      f"pior {w.erro_mun_pp.abs().max():.2f}")
for k, nome in (("mun", "município"), ("uf", "estado")):
    z = w[f"z_{k}"]
    print(f"  previsão pelo {nome}: minutos com |z|>3: {int((z.abs()>3).sum())} de {len(z)} "
          f"(ao acaso ~{0.0027*len(z):.0f}); |z|>4: {int((z.abs()>4).sum())}; desvio do z {z.std():.2f}")
print("  correlação entre o erro do minuto e a hora (tendência ao longo da noite):",
      round(np.corrcoef(np.arange(len(w)), w.erro_mun_pp)[0, 1], 3))
print("\n  10 minutos mais fora do previsto (previsão pelo município):")
top = w.reindex(w["z_mun"].abs().sort_values(ascending=False).index).head(10)
for t, r in top.iterrows():
    print(f"   {t.time()} urnas {r.urnas:>5} | Lula {100*r.lote:5.1f}% previsto {100*r.prev_mun/r.val:5.1f}% "
          f"(erro {r.erro_mun_pp:+.2f} pp, z {r.z_mun:+.1f}) | {r.ufs}")

# Simulação: a mesma ordem de chegada, mas cada urna votando exatamente o previsto + ruído sorteado dos resíduos reais
rng = np.random.default_rng(7)
sims = []
res = b["res_mun"].values
for _ in range(200):
    lula_sim = b["prev_mun"].values + rng.permutation(res)
    s = pd.Series(lula_sim, index=b.index).groupby(b["min"]).sum()
    a = s.cumsum() / w["val"].cumsum()
    a = a[a.index >= "2026-10-25 19:00"]
    sims.append(int((np.sign(a.diff()).diff().fillna(0) != 0).sum()))
real = w[w.index >= "2026-10-25 19:00"]["acum"]
print(f"\nmudanças de direção minuto a minuto depois das 19h: real {int((np.sign(real.diff()).diff().fillna(0) != 0).sum())}; "
      f"simulado com votos previstos + ruído: {np.mean(sims):.0f} ± {np.std(sims):.0f}")
w.to_csv(os.path.join(AQUI, "curva_2turno_por_minuto.csv"), sep=";")

print("\n== Curva real x curva prevista pelo 1º turno de cada urna (mesma ordem de chegada)")
w["acum_prev"] = w["prev_mun"].cumsum() / w["val"].cumsum()
w["acum_prev_uf"] = w["prev_uf"].cumsum() / w["val"].cumsum()
d = w[w.index >= "2026-10-25 19:00"]
print(f"  diferença real − prevista (município): máx {100*(d.acum-d.acum_prev).abs().max():.2f} pp, mediana {100*(d.acum-d.acum_prev).abs().median():.2f} pp")
print(f"  diferença real − prevista (só virada do estado): máx {100*(d.acum-d.acum_prev_uf).abs().max():.2f} pp")
print(f"  correlação dos movimentos minuto a minuto (real x previsto): {np.corrcoef(d.acum.diff().dropna(), d.acum_prev.diff().dropna())[0,1]:.3f}")
reg = {**{u: "NE" for u in "AL BA CE MA PB PE PI RN SE".split()}, **{u: "N" for u in "AC AM AP PA RO RR TO".split()},
       **{u: "CO" for u in "DF GO MS MT".split()}, **{u: "SE" for u in "ES MG RJ SP".split()}, **{u: "S" for u in "PR RS SC".split()}, "ZZ": "EX"}
b["reg"] = b["SG_UF"].map(reg)
for t in ["17:05", "19:05", "19:30", "20:00", "20:02", "20:15", "20:30", "21:00", "21:30", "23:21"]:
    ts = pd.Timestamp(f"2026-10-25 {t}")
    r = w.loc[:ts]
    if not len(r):
        continue
    x = b[b["DT_BU_RECEBIDO_2"] <= ts + pd.Timedelta(seconds=59)]
    mix = (x.groupby("reg")["validos_2"].sum() / x["validos_2"].sum()).round(2).to_dict()
    print(f"  {t}  real {100*r.acum.iloc[-1]:.2f}%  previsto {100*r.acum_prev.iloc[-1]:.2f}%  | votos apurados até aqui por região: {mix}")

print("\n== Reversões (zigue-zague de pelo menos 0,05 pp na curva acumulada, depois das 19h)")
c = w[w.index >= "2026-10-25 19:00"]["acum"]
piv = []
topo_v = fundo_v = c.iloc[0]; topo_t = fundo_t = c.index[0]; dirn = 0
for t, v in c.items():
    if v > topo_v: topo_v, topo_t = v, t
    if v < fundo_v: fundo_v, fundo_t = v, t
    if dirn >= 0 and v < topo_v - .0005:
        if dirn == 1: piv.append((topo_t, topo_v, "topo"))
        dirn, fundo_v, fundo_t = -1, v, t
    elif dirn <= 0 and v > fundo_v + .0005:
        if dirn == -1: piv.append((fundo_t, fundo_v, "fundo"))
        dirn, topo_v, topo_t = 1, v, t
print(f"  {len(piv)} reversões")
for t, v, tipo in piv:
    prox = w.loc[t:].iloc[1:6]
    print(f"  {t.time()} {tipo:5} {100*v:.2f}% | 5 min seguintes: Lula {100*prox.lula.sum()/prox.val.sum():.1f}%, previsto {100*prox.prev_mun.sum()/prox.val.sum():.1f}% | {prox.iloc[0].ufs}")
w.to_csv(os.path.join(AQUI, "curva_2turno_por_minuto.csv"), sep=";")
