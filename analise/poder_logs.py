"""T13b: poder do teste T28 (rajada de habilitações sem biometria no fim do dia) com fraude sintética sobre as urnas reais.

Para cada cenário (fração de urnas alteradas x fração dos votos dos últimos 30 min convertidos em "sem biometria") sorteia
as urnas, altera as contagens e aplica o MESMO teste do T28 (binomial contra a taxa da própria urna no resto do dia,
Benjamini-Hochberg a 5% sobre todas as urnas). Mede: recall (urnas alteradas que o teste acusa) e falsos positivos.
Limite assumido: só mede o que deixa rastro "sem biometria" no log; um voto lançado com habilitação biométrica forjada no
log não é visto por este teste. Uso: python poder_logs.py <turno> ; saída resultado_poder_logs_<turno>t.json
"""
import glob
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
T = sys.argv[1] if len(sys.argv) > 1 else "2"
rng = np.random.default_rng(2026)
cols = ["seq_ult30_votos", "seq_ult30_sem_biometria", "seq_resto_votos", "seq_resto_sem_biometria"]
u = pd.concat(pd.read_parquet(f, columns=cols) for f in sorted(glob.glob(os.path.join(AQUI, "brutos", f"{T}t", "urnas_*.parquet"))))
u = u.fillna(0).astype(float).reset_index(drop=True)


def bh(p, q=0.05):
    n = len(p); o = np.argsort(p); passa = p[o] <= q * np.arange(1, n + 1) / n
    k = np.max(np.where(passa)[0]) + 1 if passa.any() else 0
    s = np.zeros(n, bool); s[o[:k]] = True
    return s


def t28(ult, ult_sb, res, res_sb):
    taxa = (res_sb + 0.5) / (res + 1)
    p = stats.binom.sf(ult_sb - 1, ult.astype(int), taxa)
    return bh(np.where(ult > 0, p, 1.0))


ult, usb, res, rsb = (u[c].to_numpy() for c in cols)
base = t28(ult, usb, res, rsb)
R = {"turno": int(T), "urnas": int(len(u)), "urnas_com_votos_ult30": int((ult > 0).sum()), "falsos_positivos_sem_fraude": int(base.sum()), "cenarios": []}
elig = np.where(ult > 0)[0]
for frac_urnas in (0.001, 0.01, 0.05, 0.2):
    for frac_votos in (0.1, 0.2, 0.3, 0.5, 1.0):
        rec = []
        for _ in range(5):
            idx = rng.choice(elig, size=max(1, int(frac_urnas * len(elig))), replace=False)
            sb2 = usb.copy()
            bio = ult[idx] - usb[idx]                                  # votos biométricos que podem ser convertidos
            sb2[idx] = usb[idx] + np.minimum(np.ceil(frac_votos * ult[idx]), bio)
            sig = t28(ult, sb2, res, rsb)
            rec.append((sig[idx].mean(), sig.sum() - sig[idx].sum()))
        R["cenarios"].append({"frac_urnas_alteradas": frac_urnas, "frac_votos_ult30_convertidos": frac_votos,
                              "recall_medio": round(float(np.mean([r[0] for r in rec])), 4), "falsos_positivos_medio": round(float(np.mean([r[1] for r in rec])), 2)})
json.dump(R, open(os.path.join(AQUI, f"resultado_poder_logs_{T}t.json"), "w"), indent=1)
for c in R["cenarios"]:
    print(c)
print("sem fraude: falsos positivos", R["falsos_positivos_sem_fraude"], "de", R["urnas_com_votos_ult30"], "urnas")
