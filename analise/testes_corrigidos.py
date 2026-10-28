"""Refaz os testes de virada numa escala que respeita o teto de 0% e 100% (logit com correção de continuidade)."""
import os

import numpy as np
import pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
b = pd.read_parquet(os.path.join(AQUI, "base.parquet"))
b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20)].copy()
b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
x1, n1, x2, n2 = b["v13_1"], b["validos_1"], b["v13_2"], b["validos_2"]
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
b["sw"] = lg(x2, n2) - lg(x1, n1)
b["sd"] = np.sqrt(1/(x1+.5) + 1/(n1-x1+.5) + 1/(x2+.5) + 1/(n2-x2+.5))
b["res"] = b["sw"] - b.groupby("mun")["sw"].transform("median")
b["z"] = b["res"] / b["sd"]
b["z_rob"] = b["z"] / (1.4826 * (b["z"] - b["z"].median()).abs().median())  # z escalado pela dispersão real
un = ((x1 == 0) | (x1 == n1)) & ((x2 == 0) | (x2 == n2))
print(f"seções {len(b):,}; unânimes nos dois turnos (fora da escala): {int(un.sum())}")
print(f"dispersão do z: {b['z'].std():.2f} (1 seria só sorteio; >1 = eleitores diferentes entre turnos, normal)")
for k in (4, 5, 6):
    a, z = (b["z_rob"] > k).sum(), (b["z_rob"] < -k).sum()
    print(f"  |z robusto|>{k}: pró-Lula {a:,}  pró-Flávio {z:,}")
print(f"  assimetria do z: {stats.skew(b['z']):+.3f}")
b.reindex(b["z_rob"].abs().sort_values(ascending=False).index)[["SG_UF", "NM_MUNICIPIO_1", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO_1",
    "validos_1", "validos_2", "v13_1", "v22_1", "v13_2", "v22_2", "QT_COMPARECIMENTO_1", "QT_COMPARECIMENTO_2", "z_rob"]].head(300)\
    .to_csv(os.path.join(AQUI, "secoes_mais_fora_do_padrao.csv"), sep=";", index=False)
f = b[b["z_rob"].abs() > 5]
print("  as mais fora do padrão, por UF:", f["SG_UF"].value_counts().head(8).to_dict())
f2 = f.copy(); f2["c1"] = f2["QT_COMPARECIMENTO_1"]; f2["c2"] = f2["QT_COMPARECIMENTO_2"]
print("  mudança de comparecimento mediana nessas seções:", f2.eval("c2 - c1").median(), "eleitores | no Brasil:", b.eval("QT_COMPARECIMENTO_2 - QT_COMPARECIMENTO_1").median())

g = b[b.groupby("mun")["mun"].transform("size") >= 20].copy()
for n in (1, 2):
    g[f"o{n}"] = g.groupby("mun")[f"DT_BU_RECEBIDO_{n}"].rank(pct=True)
    print(f"virada x ordem de chegada no {n}º (dentro do município): Spearman {stats.spearmanr(g[f'o{n}'], g['res'])[0]:+.4f}")
g["dec"] = pd.qcut(g["o2"], 10, labels=False, duplicates="drop")
print("  resíduo médio por décimo da chegada no 2º:", " ".join(f"{v:+.3f}" for v in g.groupby("dec")["z"].mean()), "(em z)")
b["trocou"] = b["NR_URNA_EFETIVADA_1"] != b["NR_URNA_EFETIVADA_2"]
print(f"urna trocada: z médio {b[b.trocou]['z'].mean():+.3f} x {b[~b.trocou]['z'].mean():+.3f}; Mann-Whitney p={stats.mannwhitneyu(b[b.trocou]['z'], b[~b.trocou]['z']).pvalue:.2g}")
bio = b["QT_ELEI_BIOM_SEM_HABILITACAO_2"] / b["QT_COMPARECIMENTO_2"]
print(f"sem biometria x virada: Spearman {stats.spearmanr(bio, b['res'])[0]:+.4f}; "
      f"controlando pelo % do Lula no 1º: {stats.spearmanr(bio - bio.groupby(pd.qcut(b['v13_1']/b['validos_1'], 20, duplicates='drop')).transform('mean'), b['res'])[0]:+.4f}")
print("virada por faixa do % do Lula no 1º (mediana do resíduo, logit):",
      b.groupby(pd.cut(b["v13_1"]/b["validos_1"], [0, .2, .4, .6, .8, .95, 1.0001], include_lowest=True), observed=True)["res"].median().round(3).to_dict())

print("\nÚltimo dígito: observado x esperado pela inclinação local (ajuste exponencial por janela), em pontos percentuais")
for n in (1, 2):
    for c, nome in (("v13", "Lula"), ("v22", "Flávio")):
        v = b[f"{c}_{n}"].astype(int).values
        h = np.bincount(v, minlength=v.max() + 30).astype(float)
        esp = np.zeros(10)
        for dec in range(10, v.max() // 10 + 1):
            ini = dec * 10
            jan = np.arange(ini - 15, ini + 25)
            jan = jan[(jan >= 0) & (jan < len(h))]
            w = h[jan]
            if w.sum() < 50:
                continue
            a, bb = np.polyfit(jan, np.log(w + 1), 1)  # densidade local ~ exp(a·k)
            e = np.exp(a * np.arange(ini, ini + 10))
            esp += e / e.sum() * h[ini:ini + 10].sum()
        obs = np.bincount(v[v >= 100] % 10, minlength=10).astype(float)
        dif = 100 * (obs / obs.sum() - esp / esp.sum())
        p = stats.chisquare(obs, esp / esp.sum() * obs.sum()).pvalue
        print(f"  {n}º {nome:6}: diferença por dígito 0-9: {' '.join(f'{d:+.2f}' for d in dif)}  p={p:.3f}")
