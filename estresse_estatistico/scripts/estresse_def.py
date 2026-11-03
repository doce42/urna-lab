"""Famílias D, E, F do Estresse Estatístico (separado para velocidade).
Merge com o resultado principal depois.

Uso: python -u estresse_def.py [2026|2022]
"""
import json, os, sys, warnings
import numpy as np
import pandas as pd
from scipy import stats
warnings.filterwarnings("ignore", category=RuntimeWarning)
pr = lambda *a, **kw: print(*a, **kw, flush=True)

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"
rng = np.random.default_rng(42)
lg = lambda x, n: np.log((x + 0.5) / (n - x + 0.5))

pr(f"=== Estresse D/E/F — {ANO} ===")
df = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/secoes_{ANO}.parquet"))
df = df[df["SG_UF"] != "ZZ"].copy()
df["mun"] = df["SG_UF"] + df["CD_MUNICIPIO"]
pr(f"  {len(df)} seções")

R = {}

# ============================================================
# FAMÍLIA D — VARREDURA TERRITORIAL
# ============================================================
pr("\n--- Família D ---")
pr("ED1: Scan por município...")
R["ED1"] = {}
for turno in (1, 2):
    vc = f"validos_{turno}"; v13c = f"v13_{turno}"
    if df[vc].isna().all(): continue
    d = df[["SG_UF", "mun", vc, v13c]].dropna().copy()
    d = d[d[vc] >= 20]
    d["logit"] = lg(d[v13c].astype(int), d[vc].astype(int))
    d["z"] = 0.0
    for uf, idx in d.groupby("SG_UF").groups.items():
        s = d.loc[idx, "logit"]
        med = s.median(); mad = 1.4826 * (s - med).abs().median()
        d.loc[idx, "z"] = (s - med) / (mad if mad > 1e-8 else s.std() or 1)
    g = d.groupby("mun")["z"]; scan = g.mean() * np.sqrt(g.size())
    max_obs = float(scan.abs().max())
    z_arr = d["z"].values; uf_arr = d["SG_UF"].values; mun_arr = d["mun"].values
    # Pre-compute UF indices
    uf_codes, uf_inv = np.unique(uf_arr, return_inverse=True)
    uf_starts = np.searchsorted(np.sort(uf_inv), np.arange(len(uf_codes)))
    uf_sorted = np.argsort(uf_inv)
    uf_sizes = np.bincount(uf_inv)
    max_perm = np.zeros(200)
    for s in range(200):
        zp = z_arr.copy()
        for ui in range(len(uf_codes)):
            st = uf_starts[ui]; sz = uf_sizes[ui]
            ri = uf_sorted[st:st+sz]
            zp[ri] = rng.permutation(zp[ri])
        pdf = pd.Series(zp).groupby(mun_arr)
        sc = pdf.mean() * np.sqrt(pdf.size())
        max_perm[s] = float(sc.abs().max())
    p_val = float((max_perm >= max_obs).mean())
    top_p = scan.nlargest(10); top_n = scan.nsmallest(10)
    R["ED1"][f"{turno}t"] = {
        "max_scan": round(max_obs, 2), "p": round(p_val, 4),
        "perm_media": round(float(max_perm.mean()), 2),
        "top_pro_lula": [{"mun": str(i), "scan": round(float(v), 2)} for i, v in top_p.items()],
        "top_contra_lula": [{"mun": str(i), "scan": round(float(v), 2)} for i, v in top_n.items()],
    }
    pr(f"  {turno}t: max_scan={max_obs:.2f}, p={p_val:.4f}")

# ============================================================
# FAMÍLIA E — TURNOS
# ============================================================
pr("\n--- Família E ---")
pr("EE1: Linearidade entre turnos...")
d = df[["mun", "SG_UF", "validos_1", "v13_1", "validos_2", "v13_2"]].dropna().copy()
d = d[(d["validos_1"] >= 20) & (d["validos_2"] >= 20)]
d["l1"] = lg(d["v13_1"].astype(int), d["validos_1"].astype(int))
d["l2"] = lg(d["v13_2"].astype(int), d["validos_2"].astype(int))
r2s = []
for mun, grp in d.groupby("mun"):
    if len(grp) < 10: continue
    x, y = grp["l1"].values, grp["l2"].values
    if x.std() < 1e-8: continue
    b = np.polyfit(x, y, 1)
    ss_res = ((y - np.polyval(b, x))**2).sum()
    ss_tot = ((y - y.mean())**2).sum()
    r2s.append(1 - ss_res/ss_tot if ss_tot > 0 else 0)
r2a = np.array(r2s)
# Sim beta-binomial (amostrada)
r2_sim_all = []
sample_muns = rng.choice(d["mun"].unique(), min(100, d["mun"].nunique()), replace=False)
for _ in range(50):
    for m in sample_muns:
        g = d[d["mun"] == m]
        if len(g) < 10: continue
        n2 = g["validos_2"].astype(int).values
        pm = g["v13_2"].sum() / g["validos_2"].sum()
        a, b_ = max(pm*99, 0.1), max((1-pm)*99, 0.1)
        ps = rng.beta(a, b_, size=len(n2)).clip(0.001, 0.999)
        sv = rng.binomial(n2, ps)
        l1 = g["l1"].values; l2s = lg(sv, n2)
        if l1.std() < 1e-8: continue
        bf = np.polyfit(l1, l2s, 1)
        ss = ((l2s - np.polyval(bf, l1))**2).sum(); st = ((l2s - l2s.mean())**2).sum()
        r2_sim_all.append(1 - ss/st if st > 0 else 0)
r2_sim = np.array(r2_sim_all) if r2_sim_all else np.array([0])
R["EE1"] = {
    "n_mun": len(r2s), "r2_mediana": round(float(np.median(r2a)), 4),
    "r2_p90": round(float(np.percentile(r2a, 90)), 4),
    "r2_p99": round(float(np.percentile(r2a, 99)), 4),
    "r2_sim_mediana": round(float(np.median(r2_sim)), 4),
}
pr(f"  R² mediano obs={np.median(r2a):.4f}, sim={np.median(r2_sim):.4f}")

pr("EE2: Resíduos modulares...")
d["dif"] = (d["v13_2"] - d["v13_1"]).astype(int)
R["EE2"] = {}
mun_p = d.groupby("mun")["v13_2"].sum() / d.groupby("mun")["validos_2"].sum()
pm = d["mun"].map(mun_p).values.clip(0.001, 0.999)
for k in [2, 5, 10]:
    obs = np.bincount(d["dif"].values % k, minlength=k)
    esp = np.full(k, len(d)/k)
    chi2 = float(np.sum((obs - esp)**2 / esp))
    chi2_s = np.zeros(200)
    n2v = d["validos_2"].astype(int).values
    v1v = d["v13_1"].astype(int).values
    for s in range(200):
        sv = rng.binomial(n2v, pm)
        sd = sv - v1v
        sc = np.bincount(sd % k, minlength=k).astype(float)
        chi2_s[s] = float(np.sum((sc - esp)**2 / esp))
    p_val = float((chi2_s >= chi2).mean())
    R["EE2"][f"mod_{k}"] = {"contagens": obs.tolist(), "chi2": round(chi2, 2), "p": round(p_val, 4)}
    pr(f"  mod {k}: chi2={chi2:.1f}, p={p_val:.4f}")

# ============================================================
# FAMÍLIA F — TEMPORALIDADE (otimizada)
# ============================================================
pr("\n--- Família F ---")
pr("EF1: Autocorrelação na ordem de recebimento...")
R["EF1"] = {}
NPERM_F = 50  # menos permutações mas mais rápido
for turno in (1, 2):
    vc = f"validos_{turno}"; v13c = f"v13_{turno}"; rc = f"DT_BU_RECEBIDO_{turno}"
    if df[vc].isna().all(): continue
    d = df[["mun", vc, v13c, rc]].dropna(subset=[vc, v13c, rc]).copy()
    d = d[d[vc] >= 20].sort_values(rc)
    d["logit"] = lg(d[v13c].astype(int), d[vc].astype(int))
    d["med_mun"] = d.groupby("mun")["logit"].transform("median")
    d["r"] = d["logit"] - d["med_mun"]
    # Pré-computar índices por município
    mun_arr = d["mun"].values
    r_arr = d["r"].values
    mun_codes, mun_inv = np.unique(mun_arr, return_inverse=True)
    sorted_idx = np.argsort(mun_inv)
    starts = np.searchsorted(mun_inv[sorted_idx], np.arange(len(mun_codes)))
    sizes = np.bincount(mun_inv)
    # Calcular autocorrelação observada
    ac_obs_sum, w_sum = 0.0, 0
    valid_muns = []
    for mi in range(len(mun_codes)):
        st = starts[mi]; sz = sizes[mi]
        if sz < 5: continue
        ri = sorted_idx[st:st+sz]
        rv = r_arr[ri]
        if rv.std() < 1e-8: continue
        ac = np.corrcoef(rv[:-1], rv[1:])[0, 1]
        if np.isfinite(ac):
            ac_obs_sum += ac * sz; w_sum += sz
            valid_muns.append(mi)
    ac_obs = ac_obs_sum / w_sum if w_sum > 0 else 0
    # Permutação
    ac_perm = np.zeros(NPERM_F)
    for s in range(NPERM_F):
        ac_sum_s, w_sum_s = 0.0, 0
        for mi in valid_muns:
            st = starts[mi]; sz = sizes[mi]
            ri = sorted_idx[st:st+sz]
            rv = rng.permutation(r_arr[ri])
            ac = np.corrcoef(rv[:-1], rv[1:])[0, 1]
            if np.isfinite(ac):
                ac_sum_s += ac * sz; w_sum_s += sz
        ac_perm[s] = ac_sum_s / w_sum_s if w_sum_s > 0 else 0
    p_val = float((np.abs(ac_perm) >= abs(ac_obs)).mean())
    R["EF1"][f"{turno}t"] = {
        "autocorr": round(ac_obs, 4), "perm_media": round(float(ac_perm.mean()), 4),
        "perm_dp": round(float(ac_perm.std()), 4), "p": round(p_val, 4),
        "n_mun": len(valid_muns),
    }
    pr(f"  {turno}t: autocorr={ac_obs:.4f}, p={p_val:.4f}")

# Salvar
out = os.path.join(AQUI, "..", "resultados", f"resultado_estresse_def_{ANO}.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(R, open(out, "w"), ensure_ascii=False, indent=1, default=str)
pr(f"\nSalvo em {out}")
pr("=== Fim D/E/F ===")
