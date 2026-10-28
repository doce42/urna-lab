"""Liberação sem biometria x virada, controlando pelo perfil do eleitorado, dentro do município."""
import json
import os

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
b = pd.read_parquet(os.path.join(AQUI, "base.parquet"))
p = pd.read_parquet(os.path.join(AQUI, "perfil.parquet"))
b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20) & (b["SG_UF"] != "ZZ")].copy()
b = b.merge(p, on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"], how="inner")
print(f"seções com perfil: {len(b):,}")
b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
b["sw"] = lg(b["v13_2"], b["validos_2"]) - lg(b["v13_1"], b["validos_1"])
b["sem_bio"] = b["QT_ELEI_BIOM_SEM_HABILITACAO_2"] / b["QT_COMPARECIMENTO_2"]
b["p1"] = b["v13_1"] / b["validos_1"]
b["orf"] = 1 - (b["v13_1"] + b["v22_1"]) / b["validos_1"]
b["comp_var"] = b["QT_COMPARECIMENTO_2"] / b["QT_APTOS_2"] - b["QT_COMPARECIMENTO_1"] / b["QT_APTOS_1"]
ctrl = ["p_idoso", "p_jovem", "p_baixa_esc", "p_superior", "p_mulher", "p_biometria", "p1", "orf", "comp_var"]
cols = ["sw", "sem_bio"] + ctrl
b = b.dropna(subset=cols)
d = b[cols] - b.groupby("mun")[cols].transform("mean")   # tudo dentro do município
y = d["sw"].values


def reg(xs):
    X = np.column_stack([d[c].values for c in xs])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    # erro-padrão agrupado por município (seções do mesmo município não são independentes)
    g = pd.factorize(b["mun"])[0]
    XtX = np.linalg.inv(X.T @ X)
    meat = np.zeros((len(xs), len(xs)))
    for idx in pd.Series(np.arange(len(g))).groupby(g).indices.values():
        s = X[idx].T @ res[idx]
        meat += np.outer(s, s)
    se = np.sqrt(np.diag(XtX @ meat @ XtX))
    return beta, se


SAIDA = {}
for nome, xs in (("sem controles", ["sem_bio"]), ("com perfil do eleitorado", ["sem_bio"] + ctrl)):
    beta, se = reg(xs)
    SAIDA[nome] = {"coef": float(beta[0]), "erro": float(se[0]), "t": float(beta[0] / se[0]), "pp_1dp": float(100 * beta[0] * d["sem_bio"].std() * 0.25)}
    efeito = beta[0] * d["sem_bio"].std()
    print(f"{nome:26}: coef sem biometria {beta[0]:+.4f} (erro {se[0]:.4f}, t={beta[0]/se[0]:+.1f}); "
          f"efeito de 1 desvio-padrão na virada: {efeito:+.4f} logit ≈ {100*efeito*0.25:+.3f} pp")
beta, se = reg(["sem_bio"] + ctrl)
print("  controles (t):", ", ".join(f"{c} {b_/s_:+.1f}" for c, b_, s_ in zip(ctrl, beta[1:], se[1:])))
print("correlação dentro do município: sem biometria x idosos", round(np.corrcoef(d.sem_bio, d.p_idoso)[0, 1], 3),
      "| x baixa escolaridade", round(np.corrcoef(d.sem_bio, d.p_baixa_esc)[0, 1], 3),
      "| x biometria cadastrada", round(np.corrcoef(d.sem_bio, d.p_biometria)[0, 1], 3))
SAIDA["controles_t"] = {c: float(b_ / s_) for c, b_, s_ in zip(ctrl, beta[1:], se[1:])}
SAIDA["corr_sem_bio_idosos"] = float(np.corrcoef(d.sem_bio, d.p_idoso)[0, 1])
json.dump(SAIDA, open(os.path.join(AQUI, "resultado_biometria.json"), "w"), ensure_ascii=False, indent=1)
