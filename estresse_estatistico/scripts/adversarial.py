"""Operação Adversarial: assumindo que os dados são fabricados, buscar vestígios.

Premissa: os números publicados NÃO refletem a votação real.
Busca: inconsistências que um gerador teria dificuldade em preservar.

Uso: python -u adversarial.py [2026|2022]
"""
import json, os, sys, warnings
import numpy as np
import pandas as pd
from scipy import stats
from collections import Counter
warnings.filterwarnings("ignore", category=RuntimeWarning)
pr = lambda *a, **kw: print(*a, **kw, flush=True)

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"
rng = np.random.default_rng(42)
lg = lambda x, n: np.log((x + 0.5) / (n - x + 0.5))

pr(f"=== Operação Adversarial — {ANO} ===")
pr("Premissa: dados fabricados. Buscando vestígios.\n")

df = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/secoes_{ANO}.parquet"))
df = df[df["SG_UF"] != "ZZ"].copy()
df["mun"] = df["SG_UF"] + df["CD_MUNICIPIO"]
df["local"] = df["mun"] + "_" + df["NR_ZONA"] + "_" + df.get("NR_LOCAL_VOTACAO_2", df.get("NR_LOCAL_VOTACAO_1", "0")).astype(str)
pr(f"  {len(df)} seções")

perfil = os.path.join(RAIZ, f"dados_leves/perfil_por_secao_{ANO}.parquet")
if os.path.exists(perfil):
    pf = pd.read_parquet(perfil)
    for c in ["CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]:
        pf[c] = pf[c].astype(str)
        df[c] = df[c].astype(str)
    df = df.merge(pf, on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"], how="left")

R = {"ano": ANO, "premissa": "dados fabricados"}

# ============================================================
# FAMÍLIA P — PHANTOM VOTERS
# ============================================================
pr("--- Família P: Phantom Voters ---")

pr("P1: Comparecimento > Aptos...")
p1 = {}
for t in (1, 2):
    comp = f"QT_COMPARECIMENTO_{t}"; apt = f"QT_APTOS_{t}"
    if df[comp].isna().all(): continue
    d = df[[comp, apt]].dropna()
    exceed = d[d[comp] > d[apt]]
    p1[f"{t}t"] = {
        "secoes_excedentes": len(exceed),
        "total_secoes": len(d),
        "frac": round(len(exceed) / len(d), 6) if len(d) > 0 else 0,
        "max_excesso": int(exceed[comp].sub(exceed[apt]).max()) if len(exceed) > 0 else 0,
    }
    pr(f"  {t}t: {len(exceed)} seções com comparecimento > aptos ({100*len(exceed)/len(d):.4f}%)")
R["P1"] = p1

pr("P2: Mudança radical de comparecimento entre turnos...")
d = df[["mun", "QT_COMPARECIMENTO_1", "QT_COMPARECIMENTO_2", "QT_APTOS_2"]].dropna()
d = d[d["QT_APTOS_2"] > 0]
d["delta_comp"] = (d["QT_COMPARECIMENTO_2"] - d["QT_COMPARECIMENTO_1"]).abs() / d["QT_APTOS_2"]
d["mun_med"] = d.groupby("mun")["delta_comp"].transform("median")
d["mun_mad"] = d.groupby("mun")["delta_comp"].transform(lambda x: 1.4826 * (x - x.median()).abs().median())
d["z_delta"] = (d["delta_comp"] - d["mun_med"]) / d["mun_mad"].clip(lower=0.001)
outliers = d[d["z_delta"].abs() > 5]
R["P2"] = {
    "secoes_z_gt5": len(outliers),
    "frac": round(len(outliers) / len(d), 4),
    "z_max": round(float(d["z_delta"].abs().max()), 2),
    "delta_comp_p99": round(float(d["delta_comp"].quantile(0.99)), 4),
}
pr(f"  Seções com |z_delta_comp| > 5: {len(outliers)} ({100*len(outliers)/len(d):.2f}%)")

# ============================================================
# FAMÍLIA Q — QUANTIZAÇÃO E ARITMÉTICA
# ============================================================
pr("\n--- Família Q: Quantização e Aritmética ---")

pr("Q1: Benford nos resíduos da regressão entre turnos...")
d = df[["mun", "validos_1", "v13_1", "validos_2", "v13_2"]].dropna()
d = d[(d["validos_1"] >= 20) & (d["validos_2"] >= 20)]
d["p1"] = d["v13_1"].astype(int) / d["validos_1"].astype(int)
d["n2"] = d["validos_2"].astype(int)
d["e_v13_2"] = d.groupby("mun").apply(
    lambda g: g["p1"] * (g["v13_2"].sum() / g["validos_2"].sum()) / (g["p1"].mean() or 1) * g["n2"]
).explode().astype(float).values
d["residuo"] = (d["v13_2"].astype(float) - d["e_v13_2"]).abs()
d = d[d["residuo"] >= 1]
primeiro_digito = d["residuo"].apply(lambda x: int(str(int(abs(x)))[0]) if x != 0 else 0)
primeiro_digito = primeiro_digito[primeiro_digito > 0]
obs = np.bincount(primeiro_digito.values, minlength=10)[1:]
benford_esp = np.log10(1 + 1/np.arange(1, 10)) * len(primeiro_digito)
chi2_benford = float(np.sum((obs - benford_esp)**2 / benford_esp))
p_benford = 1 - float(stats.chi2.cdf(chi2_benford, 8))
R["Q1"] = {
    "chi2": round(chi2_benford, 2),
    "p": round(p_benford, 6),
    "n": int(len(primeiro_digito)),
    "obs": obs.tolist(),
    "esperado": [round(x, 1) for x in benford_esp.tolist()],
}
pr(f"  chi2={chi2_benford:.2f}, p={p_benford:.6f}, n={len(primeiro_digito)}")

pr("Q2: Quarto dígito da razão v13/(v13+v22)...")
d = df[["validos_2", "v13_2", "v22_2"]].dropna()
d = d[d["validos_2"] >= 50]
ratio = d["v13_2"].astype(float) / (d["v13_2"].astype(float) + d["v22_2"].astype(float))
ratio_str = ratio.apply(lambda x: f"{x:.4f}")
quarto = ratio_str.str[5].astype(int)
obs_q = np.bincount(quarto.values, minlength=10)
esp_q = np.full(10, len(quarto) / 10)
chi2_q = float(np.sum((obs_q - esp_q)**2 / esp_q))
p_q = 1 - float(stats.chi2.cdf(chi2_q, 9))
R["Q2"] = {"chi2": round(chi2_q, 2), "p": round(p_q, 6), "n": int(len(quarto)), "obs": obs_q.tolist()}
pr(f"  chi2={chi2_q:.2f}, p={p_q:.6f}")

pr("Q3: Digital root (soma de dígitos mod 9)...")
d = df[["v13_2", "v22_2"]].dropna()
d = d[(d["v13_2"] >= 1) & (d["v22_2"] >= 1)]
dr13 = d["v13_2"].astype(int) % 9
dr22 = d["v22_2"].astype(int) % 9
obs13 = np.bincount(dr13.values, minlength=9)
obs22 = np.bincount(dr22.values, minlength=9)
esp = np.full(9, len(dr13) / 9)
chi2_dr13 = float(np.sum((obs13 - esp)**2 / esp))
chi2_dr22 = float(np.sum((obs22 - esp)**2 / esp))
p_dr13 = 1 - float(stats.chi2.cdf(chi2_dr13, 8))
p_dr22 = 1 - float(stats.chi2.cdf(chi2_dr22, 8))
R["Q3"] = {
    "chi2_lula": round(chi2_dr13, 2), "p_lula": round(p_dr13, 6),
    "chi2_adv": round(chi2_dr22, 2), "p_adv": round(p_dr22, 6),
}
pr(f"  Lula: chi2={chi2_dr13:.2f}, p={p_dr13:.6f}; Adv: chi2={chi2_dr22:.2f}, p={p_dr22:.6f}")

# ============================================================
# FAMÍLIA R — RELAÇÕES CRUZADAS
# ============================================================
pr("\n--- Família R: Relações Cruzadas ---")

pr("R1: Biometria sem habilitação vs resíduo do voto...")
d = df[["mun", "SG_UF", "validos_2", "v13_2", "QT_ELEI_BIOM_SEM_HABILITACAO_2", "QT_COMPARECIMENTO_2"]].dropna()
d = d[(d["validos_2"] >= 20) & (d["QT_COMPARECIMENTO_2"] > 0)]
d["p13"] = d["v13_2"].astype(int) / d["validos_2"].astype(int)
d["bio_frac"] = d["QT_ELEI_BIOM_SEM_HABILITACAO_2"] / d["QT_COMPARECIMENTO_2"]
d["p13_mun"] = d.groupby("mun")["p13"].transform("mean")
d["r_p13"] = d["p13"] - d["p13_mun"]
d["bio_mun"] = d.groupby("mun")["bio_frac"].transform("mean")
d["r_bio"] = d["bio_frac"] - d["bio_mun"]
corr_obs = float(np.corrcoef(d["r_p13"].values, d["r_bio"].values)[0, 1])
# permutation
corr_perm = np.zeros(200)
mun_arr = d["mun"].values
r_p13 = d["r_p13"].values
r_bio = d["r_bio"].values
mun_codes, mun_inv = np.unique(mun_arr, return_inverse=True)
sorted_idx = np.argsort(mun_inv)
starts = np.searchsorted(mun_inv[sorted_idx], np.arange(len(mun_codes)))
sizes = np.bincount(mun_inv)
for s in range(200):
    rp = r_p13.copy()
    for mi in range(len(mun_codes)):
        st = starts[mi]; sz = sizes[mi]
        ri = sorted_idx[st:st+sz]
        rp[ri] = rng.permutation(rp[ri])
    corr_perm[s] = float(np.corrcoef(rp, r_bio)[0, 1])
p_r1 = float((np.abs(corr_perm) >= abs(corr_obs)).mean())
R["R1"] = {"corr": round(corr_obs, 6), "p": round(p_r1, 4), "n": len(d)}
pr(f"  corr(resíduo_p13, resíduo_bio) = {corr_obs:.6f}, p={p_r1:.4f}")

pr("R2: Rapidez do encerramento vs resultado...")
for t in (2,):
    enc = f"DT_ENCERRAMENTO_{t}"; emi = f"DT_EMISSAO_BU_{t}"
    vc = f"validos_{t}"; v13c = f"v13_{t}"
    d = df[["mun", enc, emi, vc, v13c]].dropna()
    d = d[d[vc] >= 20]
    d[enc] = pd.to_datetime(d[enc], errors="coerce")
    d[emi] = pd.to_datetime(d[emi], errors="coerce")
    d = d.dropna(subset=[enc, emi])
    d["delta_s"] = (d[emi] - d[enc]).dt.total_seconds()
    d = d[(d["delta_s"] > 0) & (d["delta_s"] < 3600)]
    d["p13"] = d[v13c].astype(int) / d[vc].astype(int)
    d["p13_mun"] = d.groupby("mun")["p13"].transform("mean")
    d["r_p13"] = d["p13"] - d["p13_mun"]
    d["delta_mun"] = d.groupby("mun")["delta_s"].transform("mean")
    d["r_delta"] = d["delta_s"] - d["delta_mun"]
    corr = float(np.corrcoef(d["r_p13"].values, d["r_delta"].values)[0, 1])
    R["R2"] = {
        "corr_residuo_delta_vs_p13": round(corr, 6),
        "n": len(d),
        "delta_s_mediana": round(float(d["delta_s"].median()), 1),
        "delta_s_p99": round(float(d["delta_s"].quantile(0.99)), 1),
    }
    pr(f"  corr(resíduo_tempo_bu, resíduo_p13) = {corr:.6f}, n={len(d)}")

pr("R3: Mudança de urna entre turnos vs mudança de resultado...")
if "NR_URNA_EFETIVADA_1" in df.columns and "NR_URNA_EFETIVADA_2" in df.columns:
    d = df[["mun", "NR_URNA_EFETIVADA_1", "NR_URNA_EFETIVADA_2", "validos_1", "v13_1", "validos_2", "v13_2"]].dropna()
    d = d[(d["validos_1"] >= 20) & (d["validos_2"] >= 20)]
    d["mesma_urna"] = d["NR_URNA_EFETIVADA_1"] == d["NR_URNA_EFETIVADA_2"]
    d["p1"] = d["v13_1"].astype(int) / d["validos_1"].astype(int)
    d["p2"] = d["v13_2"].astype(int) / d["validos_2"].astype(int)
    d["swing"] = d["p2"] - d["p1"]
    d["swing_mun"] = d.groupby("mun")["swing"].transform("mean")
    d["r_swing"] = d["swing"] - d["swing_mun"]
    mesma = d[d["mesma_urna"]]["r_swing"]
    diff = d[~d["mesma_urna"]]["r_swing"]
    if len(diff) > 30:
        t_stat, p_val = stats.mannwhitneyu(mesma.values, diff.values, alternative="two-sided")
        R["R3"] = {
            "mesma_urna_n": len(mesma), "diff_urna_n": len(diff),
            "mesma_swing_med": round(float(mesma.median()), 6),
            "diff_swing_med": round(float(diff.median()), 6),
            "U": float(t_stat), "p": round(float(p_val), 6),
        }
        pr(f"  Mesma urna: n={len(mesma)}, swing_med={mesma.median():.6f}; Diff: n={len(diff)}, swing_med={diff.median():.6f}, p={p_val:.6f}")
    else:
        R["R3"] = {"nota": "Poucas seções com urna diferente"}
        pr(f"  Poucas seções com urna diferente entre turnos ({len(diff)})")
else:
    R["R3"] = {"nota": "Colunas de urna não disponíveis"}
    pr("  Colunas de urna não disponíveis")

# ============================================================
# FAMÍLIA T — CONSISTÊNCIA TEMPORAL
# ============================================================
pr("\n--- Família T: Consistência Temporal ---")

pr("T-alpha: Correlação entre ordem de emissão e recebimento do BU...")
for t in (2,):
    emi = f"DT_EMISSAO_BU_{t}"; rec = f"DT_BU_RECEBIDO_{t}"
    d = df[["mun", emi, rec]].dropna()
    d[emi] = pd.to_datetime(d[emi], errors="coerce")
    d[rec] = pd.to_datetime(d[rec], errors="coerce")
    d = d.dropna()
    d["lat"] = (d[rec] - d[emi]).dt.total_seconds()
    d = d[(d["lat"] > 0) & (d["lat"] < 86400)]
    corrs = []
    for mun, g in d.groupby("mun"):
        if len(g) < 10: continue
        emi_rank = g[emi].rank()
        rec_rank = g[rec].rank()
        c = float(np.corrcoef(emi_rank, rec_rank)[0, 1])
        if np.isfinite(c):
            corrs.append(c)
    ca = np.array(corrs)
    R["T_alpha"] = {
        "corr_mediana_emissao_recepcao": round(float(np.median(ca)), 4),
        "corr_p05": round(float(np.percentile(ca, 5)), 4),
        "corr_p95": round(float(np.percentile(ca, 95)), 4),
        "n_mun": len(ca),
        "lat_mediana_s": round(float(d["lat"].median()), 1),
        "lat_p99_s": round(float(d["lat"].quantile(0.99)), 1),
    }
    pr(f"  Correlação emissão×recepção: mediana={np.median(ca):.4f}, p5={np.percentile(ca,5):.4f}")

pr("T-beta: Distribuição do tempo emissão-encerramento...")
for t in (2,):
    enc = f"DT_ENCERRAMENTO_{t}"; emi = f"DT_EMISSAO_BU_{t}"
    vc = f"validos_{t}"
    d = df[[enc, emi, vc]].dropna()
    d[enc] = pd.to_datetime(d[enc], errors="coerce")
    d[emi] = pd.to_datetime(d[emi], errors="coerce")
    d = d.dropna()
    d["delta_s"] = (d[emi] - d[enc]).dt.total_seconds()
    d = d[(d["delta_s"] > 0) & (d["delta_s"] < 3600)]
    d["n"] = d[vc].astype(int)
    corr_n_delta = float(np.corrcoef(d["n"].values, d["delta_s"].values)[0, 1])
    cv = float(d["delta_s"].std() / d["delta_s"].mean()) if d["delta_s"].mean() > 0 else 0
    R["T_beta"] = {
        "corr_tamanho_tempo_bu": round(corr_n_delta, 4),
        "cv_delta": round(cv, 4),
        "mediana_s": round(float(d["delta_s"].median()), 1),
        "p01_s": round(float(d["delta_s"].quantile(0.01)), 1),
        "p99_s": round(float(d["delta_s"].quantile(0.99)), 1),
        "n": len(d),
    }
    pr(f"  corr(tamanho, tempo_BU)={corr_n_delta:.4f}, CV={cv:.4f}, mediana={d['delta_s'].median():.1f}s")

# ============================================================
# FAMÍLIA U — UNIVERSALIDADE ESTATÍSTICA
# ============================================================
pr("\n--- Família U: Universalidade Estatística ---")

pr("U1: Taylor's Law (média vs variância por grupo)...")
d = df[["mun", "validos_2", "v13_2"]].dropna()
d = d[d["validos_2"] >= 20]
d["p13"] = d["v13_2"].astype(int) / d["validos_2"].astype(int)
g = d.groupby("mun")["p13"]
stats_mun = pd.DataFrame({"media": g.mean(), "var": g.var(), "n": g.size()})
stats_mun = stats_mun[stats_mun["n"] >= 10]
stats_mun = stats_mun[stats_mun["var"] > 0]
log_m = np.log(stats_mun["media"].clip(0.001).values)
log_v = np.log(stats_mun["var"].clip(1e-12).values)
slope, intercept, r_value, p_value, std_err = stats.linregress(log_m, log_v)
R["U1"] = {
    "taylor_expoente": round(slope, 4),
    "r2": round(r_value**2, 4),
    "n_mun": len(stats_mun),
    "intercept": round(intercept, 4),
}
pr(f"  Taylor's Law: expoente={slope:.4f}, R²={r_value**2:.4f}, n={len(stats_mun)}")

pr("U2: Mahalanobis — distribuição multivariada...")
feats = []
d = df[["mun", "validos_2", "v13_2", "QT_COMPARECIMENTO_2", "QT_APTOS_2", "QT_ELEI_BIOM_SEM_HABILITACAO_2"]].dropna()
d = d[(d["validos_2"] >= 20) & (d["QT_APTOS_2"] > 0)]
d["p13"] = d["v13_2"].astype(int) / d["validos_2"].astype(int)
d["comp"] = d["QT_COMPARECIMENTO_2"] / d["QT_APTOS_2"]
d["bio"] = d["QT_ELEI_BIOM_SEM_HABILITACAO_2"] / d["QT_COMPARECIMENTO_2"].clip(lower=1)
d["logn"] = np.log1p(d["QT_APTOS_2"])
X = d[["p13", "comp", "bio", "logn"]].values
X = X[np.isfinite(X).all(axis=1)]
mu = X.mean(axis=0)
cov = np.cov(X.T)
try:
    cov_inv = np.linalg.inv(cov)
    diff = X - mu
    maha = np.sqrt(np.sum(diff @ cov_inv * diff, axis=1))
    # Compare with chi-squared(k) distribution
    k = X.shape[1]
    ks_stat, ks_p = stats.kstest(maha**2, stats.chi2(k).cdf)
    R["U2"] = {
        "ks_stat": round(float(ks_stat), 4),
        "ks_p": round(float(ks_p), 6),
        "maha_mediana": round(float(np.median(maha)), 4),
        "maha_p99": round(float(np.percentile(maha, 99)), 4),
        "n": len(X),
        "k": k,
    }
    pr(f"  KS test: D={ks_stat:.4f}, p={ks_p:.6f} (H0: Mahalanobis² ~ chi2({k}))")
except np.linalg.LinAlgError:
    R["U2"] = {"erro": "Matriz de covariância singular"}
    pr("  Matriz de covariância singular")

# ============================================================
# FAMÍLIA W — WORST-CASE
# ============================================================
pr("\n--- Família W: Worst-Case ---")

pr("W1: Independência condicional (comp,voto) entre turnos...")
d = df[["mun", "QT_COMPARECIMENTO_1", "v13_1", "validos_1", "QT_COMPARECIMENTO_2", "v13_2", "validos_2", "QT_APTOS_1"]].dropna()
d = d[(d["validos_1"] >= 20) & (d["validos_2"] >= 20) & (d["QT_APTOS_1"] > 0)]
d["comp1"] = d["QT_COMPARECIMENTO_1"] / d["QT_APTOS_1"]
d["p13_1"] = d["v13_1"].astype(int) / d["validos_1"].astype(int)
d["comp2"] = d["QT_COMPARECIMENTO_2"] / d["QT_APTOS_1"]
d["p13_2"] = d["v13_2"].astype(int) / d["validos_2"].astype(int)
# residuals within municipality
for col in ["comp1", "p13_1", "comp2", "p13_2"]:
    d[f"r_{col}"] = d[col] - d.groupby("mun")[col].transform("mean")
# cross-correlation of residual pairs
# H_real: corr(r_comp1, r_comp2) and corr(r_p13_1, r_p13_2) are both high AND corr(r_comp1-r_comp2, r_p13_1-r_p13_2) is nonzero
# H_fake: comp and vote fabricated independently → cross-difference correlation ≈ 0
r_dc = d["r_comp2"].values - d["r_comp1"].values
r_dp = d["r_p13_2"].values - d["r_p13_1"].values
corr_cross = float(np.corrcoef(r_dc, r_dp)[0, 1])
# permutation
corr_perm_w = np.zeros(200)
for s in range(200):
    idx = rng.permutation(len(r_dc))
    corr_perm_w[s] = float(np.corrcoef(r_dc[idx], r_dp)[0, 1])
p_w1 = float((np.abs(corr_perm_w) >= abs(corr_cross)).mean())
R["W1"] = {
    "corr_delta_comp_vs_delta_p13": round(corr_cross, 6),
    "p": round(p_w1, 4),
    "perm_media": round(float(corr_perm_w.mean()), 6),
    "perm_dp": round(float(corr_perm_w.std()), 6),
    "n": len(d),
    "corr_comp1_comp2": round(float(np.corrcoef(d["r_comp1"].values, d["r_comp2"].values)[0, 1]), 4),
    "corr_p13_1_p13_2": round(float(np.corrcoef(d["r_p13_1"].values, d["r_p13_2"].values)[0, 1]), 4),
}
pr(f"  corr(Δcomp, Δp13) = {corr_cross:.6f}, p={p_w1:.4f}")
pr(f"  corr(comp1, comp2) = {R['W1']['corr_comp1_comp2']:.4f}, corr(p13_1, p13_2) = {R['W1']['corr_p13_1_p13_2']:.4f}")

pr("W2: PCA dos resíduos — redondeza...")
d = df[["mun", "SG_UF", "validos_2", "v13_2", "QT_COMPARECIMENTO_2", "QT_APTOS_2", "QT_ELEI_BIOM_SEM_HABILITACAO_2"]].dropna()
d = d[(d["validos_2"] >= 20) & (d["QT_APTOS_2"] > 0)]
d["p13"] = d["v13_2"].astype(int) / d["validos_2"].astype(int)
d["comp"] = d["QT_COMPARECIMENTO_2"] / d["QT_APTOS_2"]
d["bio"] = d["QT_ELEI_BIOM_SEM_HABILITACAO_2"] / d["QT_COMPARECIMENTO_2"].clip(lower=1)
for col in ["p13", "comp", "bio"]:
    d[f"r_{col}"] = d[col] - d.groupby("SG_UF")[col].transform("mean")
X = d[["r_p13", "r_comp", "r_bio"]].values
X = X[np.isfinite(X).all(axis=1)]
X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-12)
cov = np.cov(X.T)
eigvals = np.linalg.eigvalsh(cov)[::-1]
var_explained = eigvals / eigvals.sum()
R["W2"] = {
    "var_pc1": round(float(var_explained[0]), 4),
    "var_pc2": round(float(var_explained[1]), 4),
    "var_pc3": round(float(var_explained[2]), 4),
    "n": len(X),
}
pr(f"  PCA variância: PC1={var_explained[0]:.4f}, PC2={var_explained[1]:.4f}, PC3={var_explained[2]:.4f}")

# ============================================================
# FAMÍLIA V — VERIFICAÇÃO CRUZADA 2022 × 2026
# ============================================================
pr("\n--- Família V: Verificação Cruzada 2022×2026 ---")
if ANO == "2026":
    try:
        df22 = pd.read_parquet(os.path.join(RAIZ, "dados_leves/secoes_2022.parquet"))
        df22 = df22[df22["SG_UF"] != "ZZ"].copy()
        df22["mun"] = df22["SG_UF"] + df22["CD_MUNICIPIO"]
        df22["chave"] = df22["SG_UF"] + "_" + df22["CD_MUNICIPIO"] + "_" + df22["NR_ZONA"] + "_" + df22["NR_SECAO"]
        df["chave"] = df["SG_UF"] + "_" + df["CD_MUNICIPIO"] + "_" + df["NR_ZONA"] + "_" + df["NR_SECAO"]

        pr("V1: Estabilidade do resíduo por seção entre eleições...")
        d22 = df22[["chave", "mun", "validos_2", "v13_2"]].dropna()
        d22 = d22[d22["validos_2"] >= 20].copy()
        d22["p13_22"] = d22["v13_2"].astype(int) / d22["validos_2"].astype(int)
        d22["r22"] = d22["p13_22"] - d22.groupby("mun")["p13_22"].transform("mean")

        d26 = df[["chave", "mun", "validos_2", "v13_2"]].dropna()
        d26 = d26[d26["validos_2"] >= 20].copy()
        d26["p13_26"] = d26["v13_2"].astype(int) / d26["validos_2"].astype(int)
        d26["r26"] = d26["p13_26"] - d26.groupby("mun")["p13_26"].transform("mean")

        merged = d22[["chave", "r22"]].merge(d26[["chave", "r26"]], on="chave")
        corr_v1 = float(np.corrcoef(merged["r22"].values, merged["r26"].values)[0, 1])

        # If data were fabricated independently, this correlation would be near 0
        # If copied from 2022, it would be near 1
        # Real: somewhere in between (same voters, some turnover)
        R["V1"] = {
            "corr_residuo_2022_2026": round(corr_v1, 4),
            "n_secoes_pareadas": len(merged),
        }
        pr(f"  corr(resíduo_2022, resíduo_2026) = {corr_v1:.4f}, n={len(merged)}")

        pr("V2: Ranktest — ordenação das seções dentro do município...")
        rank_corrs = []
        for mun in merged["chave"].str.rsplit("_", n=2).str[0].unique():
            # reconstruct mun from chave
            pass
        # better: merge with mun
        d22m = d22[["chave", "mun", "p13_22"]].copy()
        d26m = d26[["chave", "mun", "p13_26"]].copy()
        m = d22m.merge(d26m, on=["chave", "mun"])
        for mun, g in m.groupby("mun"):
            if len(g) < 10: continue
            r22_rank = g["p13_22"].rank()
            r26_rank = g["p13_26"].rank()
            c = float(np.corrcoef(r22_rank, r26_rank)[0, 1])
            if np.isfinite(c):
                rank_corrs.append(c)
        ra = np.array(rank_corrs)
        R["V2"] = {
            "rank_corr_mediana": round(float(np.median(ra)), 4),
            "rank_corr_p05": round(float(np.percentile(ra, 5)), 4),
            "rank_corr_p95": round(float(np.percentile(ra, 95)), 4),
            "n_mun": len(ra),
        }
        pr(f"  Rank correlation: mediana={np.median(ra):.4f}, p5={np.percentile(ra,5):.4f}, p95={np.percentile(ra,95):.4f}")
    except Exception as e:
        R["V1"] = R["V2"] = {"erro": str(e)[:200]}
        pr(f"  Erro: {e}")
else:
    R["V1"] = R["V2"] = {"nota": "Família V só roda na comparação (ANO=2026)"}
    pr("  Família V só roda com ANO=2026")

# Salvar
out = os.path.join(AQUI, "..", "resultados", f"resultado_adversarial_{ANO}.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(R, open(out, "w"), ensure_ascii=False, indent=1, default=str)
pr(f"\nSalvo em {out}")
pr("=== Fim Operação Adversarial ===")
