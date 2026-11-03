"""Família H — Busca sistemática de anomalias desconhecidas (Isolation Forest).

Uso: python anomalias.py [2026|2022]
Saída: ../resultados/resultado_anomalias_<ano>.json
"""
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import IsolationForest

warnings.filterwarnings("ignore")

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"

print(f"=== Anomalias desconhecidas — {ANO} ===", flush=True)

df = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/secoes_{ANO}.parquet"))
df = df[df["SG_UF"] != "ZZ"].copy()

perfil = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/perfil_por_secao_{ANO}.parquet"))
perfil["CD_MUNICIPIO"] = perfil["CD_MUNICIPIO"].astype(str)
perfil["NR_ZONA"] = perfil["NR_ZONA"].astype(str)
perfil["NR_SECAO"] = perfil["NR_SECAO"].astype(str)
df = df.merge(perfil, on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"], how="left")

df["mun"] = df["SG_UF"] + df["CD_MUNICIPIO"]
df["local_2"] = df["mun"] + "_" + df["NR_ZONA"] + "_" + df["NR_LOCAL_VOTACAO_2"].astype(str)

lg = lambda x, n: np.log((x + 0.5) / (n - x + 0.5))

# Construir features para o 2º turno
print("Construindo features...", flush=True)

d = df.copy()
d = d.dropna(subset=["validos_2", "v13_2"])
d = d[d["validos_2"] >= 20].copy()

# z de virada (T02)
x1, n1 = d["v13_1"].fillna(0).astype(int), d["validos_1"].fillna(1).astype(int)
x2, n2 = d["v13_2"].astype(int), d["validos_2"].astype(int)
d["sw"] = lg(x2, n2) - lg(x1, n1)
d["sw_med_mun"] = d.groupby("mun")["sw"].transform("median")
d["res_sw"] = d["sw"] - d["sw_med_mun"]
sd = np.sqrt(1/(x1+.5) + 1/(n1-x1+.5) + 1/(x2+.5) + 1/(n2-x2+.5))
d["z_virada"] = d["res_sw"] / sd

# Comparecimento relativo
d["comp_2"] = d["QT_COMPARECIMENTO_2"] / d["QT_APTOS_2"].clip(lower=1)
d["comp_1"] = d["QT_COMPARECIMENTO_1"] / d["QT_APTOS_1"].clip(lower=1)
d["delta_comp"] = d["comp_2"] - d["comp_1"]
d["delta_comp_mun"] = d["delta_comp"] - d.groupby("mun")["delta_comp"].transform("median")

# Proporção de Lula no 2t
d["p13_2"] = d["v13_2"] / d["validos_2"]
d["p13_2_mun"] = d.groupby("mun")["p13_2"].transform("mean")
d["p13_2_res"] = d["p13_2"] - d["p13_2_mun"]

# Biometria
d["frac_sem_bio"] = d["QT_ELEI_BIOM_SEM_HABILITACAO_2"].fillna(0) / d["QT_COMPARECIMENTO_2"].clip(lower=1)
d["frac_sem_bio_mun"] = d.groupby("mun")["frac_sem_bio"].transform("median")
d["delta_bio"] = d["frac_sem_bio"] - d["frac_sem_bio_mun"]

# Brancos+nulos
d["bn_2"] = (d["branco_2"].fillna(0) + d["nulo_2"].fillna(0)) / d["total_2"].clip(lower=1)
d["bn_2_mun"] = d.groupby("mun")["bn_2"].transform("median")
d["delta_bn"] = d["bn_2"] - d["bn_2_mun"]

# Tamanho da seção (log)
d["log_aptos"] = np.log(d["QT_APTOS_2"].clip(lower=1))

features = ["z_virada", "delta_comp_mun", "p13_2_res", "delta_bio", "delta_bn", "log_aptos"]
X = d[features].values
X = np.nan_to_num(X, nan=0.0, posinf=3, neginf=-3)

print(f"Dataset: {X.shape[0]} seções, {X.shape[1]} features", flush=True)

# Isolation Forest
print("Rodando Isolation Forest...", flush=True)
iso = IsolationForest(n_estimators=200, contamination=0.005, random_state=42, n_jobs=-1)
d["anomaly_score"] = iso.fit_predict(X)
d["score_raw"] = -iso.decision_function(X)

anomalas = d[d["anomaly_score"] == -1].copy()
print(f"  Anomalias detectadas: {len(anomalas)} ({100*len(anomalas)/len(d):.2f}%)", flush=True)

# Agrupar por local
anomalas_por_local = anomalas.groupby("local_2").agg(
    n_anomalas=("anomaly_score", "size"),
    n_total_local=("local_2", lambda x: len(d[d["local_2"] == x.iloc[0]])),
    score_medio=("score_raw", "mean"),
    z_virada_medio=("z_virada", "mean"),
    p13_2_medio=("p13_2", "mean"),
    delta_comp_medio=("delta_comp_mun", "mean"),
    uf=("SG_UF", "first"),
    mun=("mun", "first"),
).sort_values("n_anomalas", ascending=False)

# Agrupar por município
anomalas_por_mun = anomalas.groupby("mun").agg(
    n_anomalas=("anomaly_score", "size"),
    n_total_mun=("mun", lambda x: len(d[d["mun"] == x.iloc[0]])),
    score_medio=("score_raw", "mean"),
    z_virada_medio=("z_virada", "mean"),
    uf=("SG_UF", "first"),
).sort_values("n_anomalas", ascending=False)
anomalas_por_mun["frac"] = anomalas_por_mun["n_anomalas"] / anomalas_por_mun["n_total_mun"]

# Top anomalias individuais
top_ind = anomalas.nlargest(50, "score_raw")[
    ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "mun", "local_2",
     "score_raw", "z_virada", "p13_2", "p13_2_res", "delta_comp_mun", "delta_bio", "delta_bn"]
]

# Direção das anomalias
n_pro_lula = int((anomalas["z_virada"] > 0).sum())
n_contra_lula = int((anomalas["z_virada"] < 0).sum())

R = {
    "ano": ANO,
    "n_secoes": int(len(d)),
    "n_anomalas": int(len(anomalas)),
    "frac_anomalas": float(len(anomalas) / len(d)),
    "direcao": {"pro_lula": n_pro_lula, "contra_lula": n_contra_lula},
    "score_stats": {
        "media": float(d["score_raw"].mean()),
        "dp": float(d["score_raw"].std()),
        "p99": float(d["score_raw"].quantile(0.99)),
        "max": float(d["score_raw"].max()),
    },
    "top_locais": anomalas_por_local.head(20).reset_index().to_dict(orient="records"),
    "top_municipios": anomalas_por_mun.head(20).reset_index().to_dict(orient="records"),
    "top_individuais": top_ind.reset_index(drop=True).to_dict(orient="records"),
    "features_usadas": features,
    "nota": "Isolation Forest com contamination=0.5%, 200 árvores, semente=42. Scores NÃO são probabilidade de fraude.",
}

out_path = os.path.join(AQUI, "..", "resultados", f"resultado_anomalias_{ANO}.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
json.dump(R, open(out_path, "w"), ensure_ascii=False, indent=1, default=str)
print(f"\nSalvo em {out_path}", flush=True)
print("=== Fim anomalias ===", flush=True)
