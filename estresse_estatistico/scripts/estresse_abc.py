"""Famílias A, B, C do Estresse Estatístico (separado para salvar sem D/E/F).
Uso: python -u estresse_abc.py [2026|2022]
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

pr(f"=== Estresse A/B/C — {ANO} ===")
df = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/secoes_{ANO}.parquet"))
df = df[df["SG_UF"] != "ZZ"].copy()
df["mun"] = df["SG_UF"] + df["CD_MUNICIPIO"]
df["local_2"] = df["mun"] + "_" + df["NR_ZONA"] + "_" + df["NR_LOCAL_VOTACAO_2"].astype(str)
pr(f"  {len(df)} seções")

perfil = os.path.join(RAIZ, f"dados_leves/perfil_por_secao_{ANO}.parquet")
if os.path.exists(perfil):
    pf = pd.read_parquet(perfil)
    for c in ["CD_MUNICIPIO","NR_ZONA","NR_SECAO"]:
        if c in pf.columns:
            pf[c] = pf[c].astype(str)
        if c in df.columns:
            df[c] = df[c].astype(str)
    df = df.merge(pf, on=["SG_UF","CD_MUNICIPIO","NR_ZONA","NR_SECAO"], how="left")

R = {}

# --- FAMÍLIA A ---
pr("\n--- Família A: Impressões digitais ---")
pr("EA1: Últimos dígitos...")
R["EA1"] = {}
for turno in (1, 2):
    vc = f"validos_{turno}"
    for cand, nome in [("v13", "lula"), ("v22", "adversario")]:
        cc = f"{cand}_{turno}"
        if cc not in df.columns: continue
        d = df[[vc, cc]].dropna()
        d = d[d[vc] >= 20]
        v = d[cc].astype(int).values
        ult = v % 10
        faixas = {}
        for lo in range(0, max(d[vc].astype(int)) + 1, 100):
            hi = lo + 100
            m = (d[vc].astype(int) >= lo) & (d[vc].astype(int) < hi)
            if m.sum() < 50: continue
            faixas[f"{lo}-{hi}"] = ult[m.values]
        chi2_obs = 0
        for _, digs in faixas.items():
            obs = np.bincount(digs, minlength=10)
            esp = np.full(10, len(digs)/10)
            chi2_obs += float(np.sum((obs - esp)**2 / esp))
        chi2_sim = np.zeros(500)
        for s in range(500):
            c = 0
            for _, digs in faixas.items():
                sd = rng.integers(0, 10, len(digs))
                obs = np.bincount(sd, minlength=10)
                esp = np.full(10, len(digs)/10)
                c += float(np.sum((obs - esp)**2 / esp))
            chi2_sim[s] = c
        p = float((chi2_sim >= chi2_obs).mean())
        R["EA1"][f"{turno}t_{nome}"] = {"chi2": round(chi2_obs, 2), "p": round(p, 3), "n_faixas": len(faixas)}
        pr(f"  {turno}t {nome}: chi2={chi2_obs:.2f}, p={p:.3f}")

pr("EA2: Colisões de proporções...")
R["EA2"] = {}
for turno in (1, 2):
    vc = f"validos_{turno}"
    for cand, nome in [("v13", "lula"), ("v22", "adversario")]:
        cc = f"{cand}_{turno}"
        if cc not in df.columns: continue
        d = df[[vc, cc]].dropna()
        d = d[d[vc] >= 20]
        v = d[cc].astype(int).values; n = d[vc].astype(int).values
        frac = np.round(v / n, 4)
        _, counts = np.unique(frac, return_counts=True)
        col_obs = int((counts * (counts - 1) / 2).sum())
        col_sim = np.zeros(200)
        for s in range(200):
            p_mean = v.sum() / n.sum()
            sv = rng.binomial(n, p_mean)
            sf = np.round(sv / n, 4)
            _, sc = np.unique(sf, return_counts=True)
            col_sim[s] = int((sc * (sc - 1) / 2).sum())
        z = (col_obs - col_sim.mean()) / (col_sim.std() or 1)
        p = float((col_sim <= col_obs).mean())
        R["EA2"][f"{turno}t_{nome}"] = {"col": col_obs, "z": round(z, 2), "p": round(p, 3)}
        pr(f"  {turno}t {nome}: col={col_obs}, z={z:.2f}, p={p:.3f}")

# --- FAMÍLIA B ---
pr("\n--- Família B: Suavidade excessiva ---")
pr("EB1: Dispersão intra-local...")
R["EB1"] = {}
for turno in (1, 2):
    vc = f"validos_{turno}"; v13c = f"v13_{turno}"
    if df[vc].isna().all(): continue
    sub_count, sobre_count, total = 0, 0, 0
    p_vals_sub, p_vals_sobre = [], []
    for loc, grp in df.groupby("local_2"):
        v = grp[v13c].fillna(0).values.astype(int)
        n = grp[vc].fillna(0).values.astype(int)
        m = n >= 20; v, n = v[m], n[m]
        if len(v) < 5: continue
        total += 1
        uf = grp["SG_UF"].iloc[0]
        uf_mask = df["SG_UF"] == uf
        uf_v = df.loc[uf_mask, v13c].fillna(0).values.astype(int)
        uf_n = df.loc[uf_mask, vc].fillna(0).values.astype(int)
        uf_m = uf_n >= 20
        p_uf = uf_v[uf_m].sum() / uf_n[uf_m].sum()
        var_obs_uf = np.var(uf_v[uf_m]/uf_n[uf_m])
        var_bin_uf = np.mean(p_uf*(1-p_uf)/uf_n[uf_m])
        rho = max(float(np.clip((var_obs_uf - var_bin_uf) / (p_uf*(1-p_uf) - var_bin_uf + 1e-12), 0.001, 0.5)), 0.001)
        p_loc = v.sum() / n.sum()
        var_obs = np.var(v/n, ddof=1)
        var_esp = np.mean(p_loc*(1-p_loc)/n) * (1 + rho*(np.mean(n)-1))
        var_esp = max(var_esp, 1e-12)
        ratio = var_obs / var_esp
        k = len(v)
        chi2 = (k-1) * ratio
        p_sub = float(stats.chi2.cdf(chi2, k-1))
        p_sobre = 1 - p_sub
        p_vals_sub.append(p_sub)
        p_vals_sobre.append(p_sobre)
    pa_sub = np.array(p_vals_sub); pa_sobre = np.array(p_vals_sobre)
    nt = len(pa_sub)
    lim = 0.05 * np.arange(1, nt+1) / nt
    sub_bh = int((np.sort(pa_sub) <= lim).sum())
    sobre_bh = int((np.sort(pa_sobre) <= lim).sum())
    R["EB1"][f"{turno}t"] = {"total": total, "sub_BH": sub_bh, "sobre_BH": sobre_bh}
    pr(f"  {turno}t: {total} locais, sub_BH={sub_bh}, sobre_BH={sobre_bh}")

pr("EB2: Entropia condicional...")
R["EB2"] = {}
for turno in (1, 2):
    vc = f"validos_{turno}"; v13c = f"v13_{turno}"
    if df[vc].isna().all(): continue
    d = df[["mun", "SG_UF", vc, v13c]].dropna()
    d = d[d[vc] >= 20]
    d["p"] = d[v13c].astype(int) / d[vc].astype(int)
    z_vals = []
    for mun, g in d.groupby("mun"):
        if len(g) < 10: continue
        ps = g["p"].values
        bins = np.histogram(ps, bins=10, range=(0,1))[0]
        probs = bins / bins.sum()
        probs = probs[probs > 0]
        h_obs = -float(np.sum(probs * np.log(probs)))
        h_sim = np.zeros(200)
        p_mun = float(g[v13c].sum() / g[vc].sum())
        ns = g[vc].astype(int).values
        uf = g["SG_UF"].iloc[0]
        uf_m = d["SG_UF"] == uf
        p_uf = float(d.loc[uf_m, v13c].sum() / d.loc[uf_m, vc].sum())
        var_obs_uf = np.var(d.loc[uf_m, "p"].values)
        var_bin_uf = np.mean(p_uf*(1-p_uf)/d.loc[uf_m, vc].astype(int).values)
        rho = max(float(np.clip((var_obs_uf - var_bin_uf)/(p_uf*(1-p_uf)-var_bin_uf+1e-12), 0.001, 0.5)), 0.001)
        a = max(p_mun * (1/rho - 1), 0.1)
        b = max((1-p_mun) * (1/rho - 1), 0.1)
        for s in range(200):
            sp = rng.beta(a, b, size=len(ns)).clip(0.001, 0.999)
            sv = rng.binomial(ns, sp)
            sps = sv / ns
            sb = np.histogram(sps, bins=10, range=(0,1))[0]
            sprobs = sb / sb.sum()
            sprobs = sprobs[sprobs > 0]
            h_sim[s] = -float(np.sum(sprobs * np.log(sprobs)))
        z = (h_obs - h_sim.mean()) / (h_sim.std() or 1)
        z_vals.append(z)
    za = np.array(z_vals)
    R["EB2"][f"{turno}t"] = {
        "n_mun": len(za), "z_mediana": round(float(np.median(za)), 3),
        "frac_lt_m2": round(float((za < -2).mean()), 4),
        "frac_gt_2": round(float((za > 2).mean()), 4),
    }
    pr(f"  {turno}t: {len(za)} mun, z_med={np.median(za):.3f}, <-2={float((za<-2).mean()):.4f}, >2={float((za>2).mean()):.4f}")

# --- FAMÍLIA C ---
pr("\n--- Família C: Dependências residuais ---")
pr("EC1: Modelo condicional...")
R["EC1"] = {}
for turno in (1, 2):
    vc = f"validos_{turno}"; v13c = f"v13_{turno}"
    if df[vc].isna().all(): continue
    d = df[["SG_UF", "mun", vc, v13c, "QT_COMPARECIMENTO", "QT_APTOS"]].dropna()
    d = d[d[vc] >= 20].copy()
    for col in ["fem","idade_60mais","esc_7"]:
        if col in df.columns:
            d[col] = df.loc[d.index, col]
    d["logit"] = lg(d[v13c].astype(int), d[vc].astype(int))
    d["comp"] = d["QT_COMPARECIMENTO"] / d["QT_APTOS"]
    d["log_aptos"] = np.log1p(d["QT_APTOS"])
    feats = ["comp", "log_aptos"]
    for col in ["fem","idade_60mais","esc_7"]:
        if col in d.columns: feats.append(col)
    if turno == 2 and "v13_1" in df.columns:
        d["p1"] = df.loc[d.index, "v13_1"].fillna(0).astype(int) / df.loc[d.index, "validos_1"].fillna(1).astype(int)
        feats.append("p1")
    r2s = []
    resids = []
    for uf, g in d.groupby("SG_UF"):
        if len(g) < 50: continue
        X = g[feats].fillna(0).values
        y = g["logit"].values
        X = np.column_stack([np.ones(len(X)), X])
        try:
            b, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
            pred = X @ b
            r = y - pred
            ss_res = (r**2).sum()
            ss_tot = ((y - y.mean())**2).sum()
            r2s.append(1 - ss_res/ss_tot if ss_tot > 0 else 0)
            resids.extend(r.tolist())
        except: pass
    ra = np.array(resids)
    z = (ra - np.median(ra)) / (1.4826 * np.median(np.abs(ra - np.median(ra))) or ra.std() or 1)
    R["EC1"][f"{turno}t"] = {
        "R2_mediano": round(float(np.median(r2s)), 4),
        "z_gt3": int((z > 3).sum()),
        "z_lt_m3": int((z < -3).sum()),
        "n": len(ra),
    }
    pr(f"  {turno}t: R²={np.median(r2s):.4f}, z>3={int((z>3).sum())}, z<-3={int((z<-3).sum())}")

pr("EC2: Correlação Lula × comparecimento...")
R["EC2"] = {}
for turno in (1, 2):
    vc = f"validos_{turno}"; v13c = f"v13_{turno}"
    if df[vc].isna().all(): continue
    d = df[["mun", vc, v13c, "QT_COMPARECIMENTO", "QT_APTOS"]].dropna()
    d = d[d[vc] >= 20].copy()
    d["p13"] = d[v13c].astype(int) / d[vc].astype(int)
    d["comp"] = d["QT_COMPARECIMENTO"] / d["QT_APTOS"]
    d["p13_mun"] = d.groupby("mun")["p13"].transform("mean")
    d["comp_mun"] = d.groupby("mun")["comp"].transform("mean")
    d["rp"] = d["p13"] - d["p13_mun"]
    d["rc"] = d["comp"] - d["comp_mun"]
    corr_obs = float(np.corrcoef(d["rp"].values, d["rc"].values)[0,1])
    mun_arr = d["mun"].values
    mun_codes, mun_inv = np.unique(mun_arr, return_inverse=True)
    sorted_idx = np.argsort(mun_inv)
    starts = np.searchsorted(mun_inv[sorted_idx], np.arange(len(mun_codes)))
    sizes = np.bincount(mun_inv)
    rp = d["rp"].values; rc = d["rc"].values
    corr_perm = np.zeros(100)
    for s in range(100):
        rpp = rp.copy()
        for mi in range(len(mun_codes)):
            st = starts[mi]; sz = sizes[mi]
            ri = sorted_idx[st:st+sz]
            rpp[ri] = rng.permutation(rpp[ri])
        corr_perm[s] = float(np.corrcoef(rpp, rc)[0,1])
    p = float((np.abs(corr_perm) >= abs(corr_obs)).mean())
    R["EC2"][f"{turno}t"] = {"corr": round(corr_obs, 4), "p": round(p, 4)}
    pr(f"  {turno}t: corr={corr_obs:.4f}, p={p:.4f}")

out = os.path.join(AQUI, "..", "resultados", f"resultado_estresse_abc_{ANO}.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(R, open(out, "w"), ensure_ascii=False, indent=1, default=str)
pr(f"\nSalvo em {out}")
pr("=== Fim A/B/C ===")
