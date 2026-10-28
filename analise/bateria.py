"""A mesma bateria de testes para qualquer eleição (2026 e 2022), com o mesmo código, para a comparação ser justa.

Uso: python bateria.py <ano>    (lê base.parquet para 2026, base_<ano>.parquet para os outros)
Saída: resultado_bateria_<ano>.json e resumo na tela.
Testes (numeração do CATALOGO.md):
  T02 seções fora do padrão do município (logit, z robusto > 5), nos dois sentidos
  T03 virada x ordem de chegada ao TSE dentro do município (Spearman)
  T04 urna trocada entre turnos x resto (Mann-Whitney no z)
  T05 último dígito (>= 100 votos) contra o esperado pela inclinação local
  T07 impressão digital: comparecimento >= 95% e >= 90% dos válidos para um candidato
  T10 curva real x prevista pelo 1º turno (município, sem a própria seção; e estado), máximo desvio
      depois que 5% dos votos foram apurados
  T11 mudanças de direção minuto a minuto: real x 200 simulações (previsto + ruído real embaralhado)
  T21 percentuais inteiros (Kobak, Shpilkin e Pshenichnikov 2016; nulo por reamostragem como em Rozenas 2017):
      seções cujo comparecimento ou % do candidato é um inteiro exato, contra 200 sorteios binomiais com o mesmo
      tamanho e a mesma proporção de cada seção
  T22 assinatura de fraude incremental (Klimek et al. 2012; CSH Viena, Brasil 2022): correlação entre comparecimento
      e % de cada candidato dentro do município, nos dois turnos
  T25 impressão digital 2D (Klimek et al. 2012): histograma comparecimento x % do candidato (para o relatório) e
      momentos da "taxa logarítmica de voto" nu = ln((1 - v) / v) por seção (assimetria e curtose em excesso)
  T26 2º dígito de Benford (Mebane, 2BL): contagens >= 10, qui-quadrado e média do 2º dígito (esperado 4,187);
      com ressalva: a literatura mostra que o 2BL também reage a comportamento estratégico, não só a fraude
  T27 último dígito de branco, nulo e comparecimento (mesmo método do T05)
  INC incerteza e poder dos resultados negativos (revisão cega externa, 27/10):
      T02: nulo realista — distribuição t de Student ajustada aos z (caudas pesadas): quantas seções o modelo espera além
           de ±5, e de que lado; T03: intervalo de 95% (Fisher) e menor correlação detectável (80% de poder, α = 0,01);
      T04: diferença de médias com intervalo de 95% por bootstrap de municípios (semente 5) e menor efeito detectável
"""
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"
b = pd.read_parquet(os.path.join(AQUI, "base.parquet" if ANO == "2026" else f"base_{ANO}.parquet"))
b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20)].copy()
b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
inv = lambda z: 1 / (1 + np.exp(-z))
R = {"ano": ANO, "secoes": int(len(b))}

x1, n1, x2, n2 = b["v13_1"], b["validos_1"], b["v13_2"], b["validos_2"]
b["sw"] = lg(x2, n2) - lg(x1, n1)
b["res"] = b["sw"] - b.groupby("mun")["sw"].transform("median")
z = b["res"] / np.sqrt(1/(x1+.5) + 1/(n1-x1+.5) + 1/(x2+.5) + 1/(n2-x2+.5))
b["z"] = z / (1.4826 * (z - z.median()).abs().median())
R["T02"] = {"acima5_lula": int((b.z > 5).sum()), "acima5_outro": int((b.z < -5).sum()), "assimetria": float(stats.skew(b.z))}

g = b[b.groupby("mun")["mun"].transform("size") >= 20].copy()
g["ord"] = g.groupby("mun")["DT_BU_RECEBIDO_2"].rank(pct=True)
R["T03"] = {"spearman": float(stats.spearmanr(g["ord"], g["res"])[0])}

tr = b["NR_URNA_EFETIVADA_1"] != b["NR_URNA_EFETIVADA_2"]
R["T04"] = {"trocadas": int(tr.sum()), "z_trocadas": float(b[tr].z.mean()), "z_outras": float(b[~tr].z.mean()),
            "p": float(stats.mannwhitneyu(b[tr].z, b[~tr].z).pvalue)}


def digito(v):
    h = np.bincount(v, minlength=v.max() + 30).astype(float)
    esp = np.zeros(10)
    for dec in range(10, v.max() // 10 + 1):
        ini = dec * 10
        jan = np.arange(ini - 15, ini + 25); jan = jan[(jan >= 0) & (jan < len(h))]
        if h[jan].sum() < 50:
            continue
        a, _ = np.polyfit(jan, np.log(h[jan] + 1), 1)
        e = np.exp(a * np.arange(ini, ini + 10))
        esp += e / e.sum() * h[ini:ini + 10].sum()
    obs = np.bincount(v[v >= 100] % 10, minlength=10).astype(float)
    return float(stats.chisquare(obs, esp / esp.sum() * obs.sum()).pvalue)


R["T05"] = {f"{n}t_{c}": digito(b[f"{c}_{n}"].astype(int).values) for n in (1, 2) for c in ("v13", "v22")}

R["T07"] = {}
for n in (1, 2):
    x = b[b[f"validos_{n}"] >= 50]
    comp = x[f"QT_COMPARECIMENTO_{n}"] / x[f"QT_APTOS_{n}"]
    for c in ("v13", "v22"):
        R["T07"][f"{n}t_{c}"] = int(((comp >= .95) & (x[f"{c}_{n}"] / x[f"validos_{n}"] >= .9)).sum())
    R["T07"][f"{n}t_acima_100pct"] = int((comp > 1).sum())

# T10/T11: curva do 2º turno
g = b.groupby("mun")["sw"]; n = g.transform("size")
sw_uf = b.groupby("SG_UF")["sw"].transform("median")
sw_m = np.where(n > 1, (g.transform("sum") - b["sw"]) / (n - 1).clip(lower=1), sw_uf)
b["prev_m"] = inv(lg(x1, n1) + sw_m) * n2
b["prev_e"] = inv(lg(x1, n1) + sw_uf) * n2
b = b.sort_values("DT_BU_RECEBIDO_2")
b["min"] = b["DT_BU_RECEBIDO_2"].dt.floor("1min")
w = b.groupby("min")[["v13_2", "validos_2", "prev_m", "prev_e"]].sum().cumsum()
w = w[w["validos_2"] >= .05 * w["validos_2"].iloc[-1]]
real = w.v13_2 / w.validos_2
R["T10"] = {"max_desvio_mun_pp": float(100 * (real - w.prev_m / w.validos_2).abs().max()),
            "max_desvio_estado_pp": float(100 * (real - w.prev_e / w.validos_2).abs().max()),
            "inicio_contagem": str(w.index[0])}
mud = lambda a: int((np.sign(a.diff()).diff().fillna(0) != 0).sum())
rng = np.random.default_rng(7)
res = (b["v13_2"] - b["prev_m"]).values
sims = []
for _ in range(200):
    s = pd.Series(b["prev_m"].values + rng.permutation(res), index=b.index).groupby(b["min"]).sum().cumsum()
    a = (s / b.groupby("min")["validos_2"].sum().cumsum()).loc[w.index]
    sims.append(mud(a))
R["T11"] = {"real": mud(real), "simulado_media": float(np.mean(sims)), "simulado_dp": float(np.std(sims))}

# T21: percentuais inteiros exatos
def inteiros(k, n):
    k, n = k.astype(np.int64), n.astype(np.int64)
    return int(((100 * k) % n == 0).sum())


rng = np.random.default_rng(11)
R["T21"] = {}
for n_ in (1, 2):
    x = b[b[f"validos_{n_}"] >= 100]
    for nome, k, n in (("comparecimento", x[f"QT_COMPARECIMENTO_{n_}"], x[f"QT_APTOS_{n_}"]),
                       ("lula", x[f"v13_{n_}"], x[f"validos_{n_}"]), ("adversario", x[f"v22_{n_}"], x[f"validos_{n_}"])):
        k, n = k.fillna(0).values, n.fillna(0).values
        ok = n > 0
        k, n = k[ok], n[ok]
        obs = inteiros(k, n)
        sims = [inteiros(rng.binomial(n.astype(np.int64), k / n), n) for _ in range(200)]
        R["T21"][f"{n_}t_{nome}"] = {"observado": obs, "esperado": float(np.mean(sims)), "dp": float(np.std(sims)),
                                     "z": float((obs - np.mean(sims)) / (np.std(sims) or 1))}

# T22: comparecimento x voto dentro do município
R["T22"] = {}
for n_ in (1, 2):
    x = b.copy()
    comp = x[f"QT_COMPARECIMENTO_{n_}"] / x[f"QT_APTOS_{n_}"]
    for nome, c in (("lula", "v13"), ("adversario", "v22")):
        sh = x[f"{c}_{n_}"] / x[f"validos_{n_}"]
        dc = comp - comp.groupby(x["mun"]).transform("mean")
        ds = sh - sh.groupby(x["mun"]).transform("mean")
        R["T22"][f"{n_}t_{nome}"] = float(stats.spearmanr(dc, ds, nan_policy="omit")[0])

# T25: impressão digital 2D e momentos de nu
R["T25"] = {}
for n_ in (1, 2):
    x = b[b[f"validos_{n_}"] >= 50]
    comp = (x[f"QT_COMPARECIMENTO_{n_}"] / x[f"QT_APTOS_{n_}"]).clip(0, 1)
    for nome, c in (("lula", "v13"), ("adversario", "v22")):
        v = (x[f"{c}_{n_}"] / x[f"validos_{n_}"]).clip(1e-4, 1 - 1e-4)
        nu = np.log((1 - v) / v)
        H, _, _ = np.histogram2d(comp, v, bins=[np.linspace(0, 1, 51), np.linspace(0, 1, 51)])
        R["T25"][f"{n_}t_{nome}"] = {"assimetria_nu": float(stats.skew(nu)), "curtose_excesso_nu": float(stats.kurtosis(nu)),
                                     "fracao_canto_95_95": float(((comp >= .95) & (v >= .95)).mean()),
                                     "hist2d": H.astype(int).tolist()}

# T26: 2º dígito de Benford
benford2 = np.array([sum(np.log10(1 + 1 / (10 * k + d)) for k in range(1, 10)) for d in range(10)])
R["T26"] = {}
for n_ in (1, 2):
    for c, nome in (("v13", "lula"), ("v22", "adversario")):
        v = b[f"{c}_{n_}"].astype(int).values
        v = v[v >= 10]
        d2 = np.array([int(str(k)[1]) for k in v])
        obs = np.bincount(d2, minlength=10)
        R["T26"][f"{n_}t_{nome}"] = {"n": int(len(v)), "media": float(d2.mean()), "media_esperada": float((benford2 * np.arange(10)).sum()),
                                     "p": float(stats.chisquare(obs, benford2 * obs.sum()).pvalue)}

# T27: último dígito de branco, nulo e comparecimento
R["T27"] = {}
for n_ in (1, 2):
    for c in (f"branco_{n_}", f"nulo_{n_}", f"QT_COMPARECIMENTO_{n_}"):
        v = b[c].dropna().astype(int).values
        if (v >= 100).sum() > 1000:
            R["T27"][c] = digito(v)

# INC: incerteza e poder
INC = {}
zz = b["z"].values
df_t, loc_t, esc_t = stats.t.fit(zz[np.isfinite(zz)])
esp_cauda = len(zz) * stats.t.sf(5, df_t, loc_t, esc_t), len(zz) * stats.t.cdf(-5, df_t, loc_t, esc_t)
INC["T02_t_student"] = {"graus_liberdade": float(df_t), "esperado_acima_5": float(esp_cauda[0]), "esperado_abaixo_menos5": float(esp_cauda[1]),
                        "observado_acima_5": int((zz > 5).sum()), "observado_abaixo_menos5": int((zz < -5).sum())}
# n do T03: seções em municípios com >= 20 seções (o mesmo filtro do teste)
nn = int((b.groupby("mun")["mun"].transform("size") >= 20).sum())
r3 = R["T03"]["spearman"]
zf, se = np.arctanh(r3), 1 / np.sqrt(nn - 3)
INC["T03"] = {"r": r3, "ic95": [float(np.tanh(zf - 1.96 * se)), float(np.tanh(zf + 1.96 * se))], "n": int(nn),
              "menor_r_detectavel_80pct_alfa001": float(np.tanh((stats.norm.ppf(0.995) + stats.norm.ppf(0.8)) * se))}
rng5 = np.random.default_rng(5)
muns = b["mun"].values
um = np.unique(muns)
dif = []
idx_por_mun = pd.Series(np.arange(len(b))).groupby(muns).apply(np.array)
# a base foi reordenada no T10: recalcula o marcador de urna trocada na ordem atual (alinhado às linhas)
tr_atual = (b["NR_URNA_EFETIVADA_1"] != b["NR_URNA_EFETIVADA_2"]).values
for _ in range(200):
    pick = rng5.choice(um, len(um))
    ii = np.concatenate([idx_por_mun[m_] for m_ in pick])
    t_, zb = tr_atual[ii], b["z"].values[ii]
    dif.append(np.nanmean(zb[t_]) - np.nanmean(zb[~t_]))
d0 = float(np.nanmean(b["z"].values[tr_atual]) - np.nanmean(b["z"].values[~tr_atual]))
sd_d = float(np.std(dif))
INC["T04"] = {"diferenca_z": float(d0), "ic95": [float(np.percentile(dif, 2.5)), float(np.percentile(dif, 97.5))],
              "menor_diferenca_detectavel_80pct_alfa001": float((stats.norm.ppf(0.995) + stats.norm.ppf(0.8)) * sd_d),
              "nota": "em unidades de z robusto (1 = um desvio típico da virada de uma seção)"}
R["INC"] = INC

json.dump(R, open(os.path.join(AQUI, f"resultado_bateria_{ANO}.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
