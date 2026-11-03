"""Operação Estresse Estatístico — Famílias A–F.

Uso: python -u estresse.py [2026|2022]
Saída: ../resultados/resultado_estresse_<ano>.json
"""
import json, os, sys, warnings
import numpy as np
import pandas as pd
from scipy import stats
warnings.filterwarnings("ignore", category=RuntimeWarning)

P = print
def pr(*a, **kw): P(*a, **kw, flush=True)

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"
rng = np.random.default_rng(42)
lg = lambda x, n: np.log((x + 0.5) / (n - x + 0.5))

pr(f"=== Estresse Estatístico — {ANO} ===")
pr("Carregando dados...")

df = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/secoes_{ANO}.parquet"))
df = df[df["SG_UF"] != "ZZ"].copy()
perfil = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/perfil_por_secao_{ANO}.parquet"))
for c in ("CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"):
    perfil[c] = perfil[c].astype(str)
df = df.merge(perfil, on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"], how="left")
df["mun"] = df["SG_UF"] + df["CD_MUNICIPIO"]
df["local_2"] = df["mun"] + "_" + df["NR_ZONA"] + "_" + df["NR_LOCAL_VOTACAO_2"].astype(str)
df["zona"] = df["SG_UF"] + "_" + df["NR_ZONA"]
pr(f"  {len(df)} seções carregadas")

R = {"ano": ANO, "data": "2026-11-02", "operacao": "estresse_estatistico"}

# ============================================================
# FAMÍLIA A — IMPRESSÕES DIGITAIS DOS NÚMEROS
# ============================================================
pr("\n--- Família A: Impressões digitais ---")

# EA1: Últimos dígitos condicionados ao tamanho (versão vetorizada)
pr("EA1: Últimos dígitos...")
NSIM_A = 500

def ea1(votos_col, validos_col, turno, nome):
    mask = df[validos_col].fillna(0).astype(int) >= 20
    if turno == 2:
        mask &= df[validos_col].notna()
    v = df.loc[mask, votos_col].fillna(0).astype(int).values
    n = df.loc[mask, validos_col].astype(int).values
    ult = v % 10
    # Faixas de 100 (menos faixas = mais rápido)
    faixas = np.arange(20, n.max() + 100, 100)
    fi = np.digitize(n, faixas)
    chi2_obs = 0.0
    chi2_sim = np.zeros(NSIM_A)
    nf = 0
    for f in range(1, len(faixas)):
        sel = fi == f
        if sel.sum() < 200:
            continue
        nf += 1
        obs_d = np.bincount(ult[sel], minlength=10).astype(float)
        p_local = v[sel] / n[sel]
        # Esperado: média de 200 simulações
        esp_d = np.zeros(10)
        for _ in range(200):
            sim_v = rng.binomial(n[sel], p_local)
            esp_d += np.bincount(sim_v % 10, minlength=10).astype(float)
        esp_d /= 200
        esp_d = np.maximum(esp_d, 1.0)
        chi2_obs += float(np.sum((obs_d - esp_d)**2 / esp_d))
        for s in range(NSIM_A):
            sim_v = rng.binomial(n[sel], p_local)
            sim_d = np.bincount(sim_v % 10, minlength=10).astype(float)
            chi2_sim[s] += float(np.sum((sim_d - esp_d)**2 / esp_d))
    p_val = float((chi2_sim >= chi2_obs).mean()) if nf > 0 else 1.0
    return {"chi2_obs": round(chi2_obs, 2), "chi2_sim_media": round(float(chi2_sim.mean()), 2),
            "p": round(p_val, 4), "n_faixas": nf, "n_secoes": int(mask.sum())}

R["EA1"] = {}
for t in (1, 2):
    for col, nome in [("v13", "lula"), ("v22", "adversario")]:
        c = f"{col}_{t}"
        vc = f"validos_{t}"
        if c not in df.columns or df[vc].isna().all():
            continue
        r = ea1(c, vc, t, nome)
        R["EA1"][f"{t}t_{nome}"] = r
        pr(f"  {t}t {nome}: chi2={r['chi2_obs']}, p={r['p']}")

# EA2: Colisões de proporções v/n
pr("EA2: Colisões de proporções...")
NSIM_EA2 = 200

def ea2(votos_col, validos_col, turno):
    mask = (df[validos_col].fillna(0).astype(int) >= 20) & (df[validos_col].fillna(0).astype(int) <= 500)
    if df[validos_col].isna().all():
        return None
    v = df.loc[mask, votos_col].fillna(0).astype(int).values
    n = df.loc[mask, validos_col].astype(int).values
    mun = df.loc[mask, "mun"].values
    # Colisões: pares com mesma fração v/n
    fracs = v * 10000 // n  # discretizar a 0.01%
    from collections import Counter
    cnt = Counter(fracs)
    col_obs = sum(c*(c-1)//2 for c in cnt.values())
    # Simular com proporção municipal
    mun_p = {}
    for m in np.unique(mun):
        idx = mun == m
        mun_p[m] = v[idx].sum() / n[idx].sum()
    p_arr = np.array([mun_p[m] for m in mun]).clip(0.001, 0.999)
    col_sim = np.zeros(NSIM_EA2)
    for s in range(NSIM_EA2):
        sim_v = rng.binomial(n, p_arr)
        sim_fracs = sim_v * 10000 // n
        cnt_s = Counter(sim_fracs)
        col_sim[s] = sum(c*(c-1)//2 for c in cnt_s.values())
    z = (col_obs - col_sim.mean()) / (col_sim.std() or 1)
    p_val = float((col_sim >= col_obs).mean())
    return {"colisoes_obs": int(col_obs), "colisoes_sim_media": round(float(col_sim.mean()), 1),
            "z": round(float(z), 2), "p": round(p_val, 4), "n": int(mask.sum())}

R["EA2"] = {}
for t in (1, 2):
    for col, nome in [("v13", "lula"), ("v22", "adversario")]:
        c = f"{col}_{t}"
        vc = f"validos_{t}"
        if c not in df.columns or df[vc].isna().all():
            continue
        r = ea2(c, vc, t)
        if r:
            R["EA2"][f"{t}t_{nome}"] = r
            pr(f"  {t}t {nome}: col={r['colisoes_obs']}, z={r['z']}, p={r['p']}")


# ============================================================
# FAMÍLIA B — SUAVIDADE EXCESSIVA
# ============================================================
pr("\n--- Família B: Suavidade excessiva ---")

# EB1: Dispersão intra-local (beta-binomial)
pr("EB1: Dispersão intra-local...")

def estimar_rho_uf(grp, turno):
    v = grp[f"v13_{turno}"].fillna(0).values.astype(int)
    n = grp[f"validos_{turno}"].fillna(0).values.astype(int)
    m = n >= 20; v, n = v[m], n[m]
    if len(v) < 50: return 0.01
    p = v.sum() / n.sum()
    var_obs = np.var(v/n)
    var_bin = np.mean(p*(1-p)/n)
    if var_obs <= var_bin: return 0.001
    return float(np.clip((var_obs - var_bin) / (p*(1-p) - var_bin + 1e-12), 0.001, 0.5))

R["EB1"] = {}
for turno in (1, 2):
    vc = f"validos_{turno}"
    v13c = f"v13_{turno}"
    if df[vc].isna().all():
        continue
    rho_uf = {uf: estimar_rho_uf(g, turno) for uf, g in df.groupby("SG_UF")}
    sub_count, sobre_count, total_loc = 0, 0, 0
    p_sub_list, p_sobre_list = [], []
    sub_top, sobre_top = [], []
    for loc, grp in df.groupby("local_2"):
        v = grp[v13c].fillna(0).values.astype(int)
        n = grp[vc].fillna(0).values.astype(int)
        m = n >= 20; v, n = v[m], n[m]
        if len(v) < 5: continue
        total_loc += 1
        p_loc = v.sum() / n.sum()
        rho = rho_uf.get(grp["SG_UF"].iloc[0], 0.01)
        var_obs = np.var(v/n, ddof=1)
        var_esp = np.mean(p_loc*(1-p_loc)/n) * (1 + rho*(np.mean(n)-1))
        var_esp = max(var_esp, 1e-12)
        ratio = var_obs / var_esp
        k = len(v)
        chi2 = (k-1) * ratio
        p_sub = float(stats.chi2.cdf(chi2, k-1))
        p_sobre = 1 - p_sub
        p_sub_list.append(p_sub)
        p_sobre_list.append(p_sobre)
        if p_sub < 0.01:
            sub_top.append({"local": str(loc), "n": k, "ratio": round(ratio, 3), "p": round(p_sub, 6)})
        if p_sobre < 0.01:
            sobre_top.append({"local": str(loc), "n": k, "ratio": round(ratio, 3), "p": round(p_sobre, 6)})
    # BH
    if p_sub_list:
        ps = np.array(p_sub_list); nt = len(ps)
        lim = 0.05 * np.arange(1, nt+1) / nt
        sub_bh = int((np.sort(ps) <= lim).sum())
        ps2 = np.array(p_sobre_list)
        sobre_bh = int((np.sort(ps2) <= lim).sum())
    else:
        sub_bh, sobre_bh = 0, 0
    sub_top.sort(key=lambda x: x["p"]); sobre_top.sort(key=lambda x: x["p"])
    R["EB1"][f"{turno}t"] = {
        "total_locais": total_loc,
        "subdispersos_bh": sub_bh, "sobredispersos_bh": sobre_bh,
        "subdispersos_p001": len([x for x in sub_top]),
        "sobredispersos_p001": len([x for x in sobre_top]),
        "top_subdispersos": sub_top[:15], "top_sobredispersos": sobre_top[:15],
        "rho_por_uf": {k: round(v, 4) for k, v in rho_uf.items()},
    }
    pr(f"  {turno}t: {total_loc} locais, sub_BH={sub_bh}, sobre_BH={sobre_bh}")

# EB2: Entropia condicional por município
pr("EB2: Entropia condicional...")
NSIM_ENT = 200

def entropy_sec(v, n):
    p = (v / n.clip(min=1)).clip(1e-8, 1-1e-8)
    return float(-np.mean(p*np.log(p) + (1-p)*np.log(1-p)))

R["EB2"] = {}
for turno in (1, 2):
    vc = f"validos_{turno}"
    v13c = f"v13_{turno}"
    if df[vc].isna().all():
        continue
    rho_uf = {uf: estimar_rho_uf(g, turno) for uf, g in df.groupby("SG_UF")}
    mun_z = []
    for mun, grp in df.groupby("mun"):
        v = grp[v13c].fillna(0).values.astype(int)
        n = grp[vc].fillna(0).values.astype(int)
        m = n >= 20; v, n = v[m], n[m]
        if len(v) < 10: continue
        h_obs = entropy_sec(v, n)
        p_mun = v.sum() / n.sum()
        rho = rho_uf.get(grp["SG_UF"].iloc[0], 0.01)
        a = max(p_mun * (1/rho - 1), 0.1)
        b = max((1-p_mun) * (1/rho - 1), 0.1)
        h_sim = np.zeros(NSIM_ENT)
        for s in range(NSIM_ENT):
            ps = rng.beta(a, b, size=len(v)).clip(1e-8, 1-1e-8)
            sv = rng.binomial(n, ps)
            h_sim[s] = entropy_sec(sv, n)
        z = (h_obs - h_sim.mean()) / (h_sim.std() or 1)
        mun_z.append({"mun": str(mun), "n": len(v), "h_obs": round(h_obs, 5),
                       "h_sim": round(float(h_sim.mean()), 5), "z": round(float(z), 2)})
    z_arr = np.array([m["z"] for m in mun_z])
    mun_z.sort(key=lambda x: x["z"])
    R["EB2"][f"{turno}t"] = {
        "n_mun": len(mun_z), "z_media": round(float(z_arr.mean()), 3),
        "z_dp": round(float(z_arr.std()), 3),
        "frac_abaixo_menos2": round(float((z_arr < -2).mean()), 4),
        "frac_acima_2": round(float((z_arr > 2).mean()), 4),
        "top_regulares": mun_z[:10], "top_irregulares": mun_z[-10:],
    }
    pr(f"  {turno}t: {len(mun_z)} mun, z_med={z_arr.mean():.3f}, <-2={float((z_arr<-2).mean()):.4f}, >2={float((z_arr>2).mean()):.4f}")


# ============================================================
# FAMÍLIA C — DEPENDÊNCIAS E CORRELAÇÕES RESIDUAIS
# ============================================================
pr("\n--- Família C: Dependências residuais ---")

# EC1: Modelo condicional + resíduos
pr("EC1: Modelo condicional...")
R["EC1"] = {}
for turno in (1, 2):
    vc = f"validos_{turno}"; v13c = f"v13_{turno}"
    if df[vc].isna().all(): continue
    d = df[df[vc].fillna(0).astype(int) >= 20].copy()
    d["logit"] = lg(d[v13c].fillna(0).astype(int), d[vc].astype(int))
    d["comp"] = d[f"QT_COMPARECIMENTO_{turno}"] / d[f"QT_APTOS_{turno}"].clip(lower=1)
    d["la"] = np.log(d[f"QT_APTOS_{turno}"].clip(lower=1))
    feats = ["comp", "la"]
    for c in ["fem", "idade_60mais", "esc_7"]:
        if c in d.columns:
            d[c] = d[c].fillna(d[c].mean())
            feats.append(c)
    if turno == 2 and "v13_1" in df.columns:
        d["p1"] = df.loc[d.index, "v13_1"].fillna(0) / df.loc[d.index, "validos_1"].clip(lower=1)
        feats.append("p1")
    res = np.zeros(len(d))
    for uf, idx in d.groupby("SG_UF").groups.items():
        sub = d.loc[idx]
        X = np.column_stack([np.ones(len(sub))] + [sub[f].values for f in feats])
        X = np.nan_to_num(X)
        y = sub["logit"].values
        try:
            beta, *_ = np.linalg.lstsq(X, y, rcond=None)
            res[d.index.get_indexer(idx)] = y - X @ beta
        except: pass
    d["res"] = res
    sd = np.sqrt(1/(d[v13c].clip(lower=0.5)+0.5) + 1/((d[vc]-d[v13c]).clip(lower=0.5)+0.5))
    d["zr"] = d["res"] / sd
    # Aggregar por local
    loc_z = []
    for loc, grp in d.groupby("local_2"):
        if len(grp) < 3: continue
        r = grp["zr"].values
        if np.std(r) < 1e-8: continue
        loc_z.append(float(r.mean() * np.sqrt(len(r))))
    loc_z = np.array(loc_z)
    R["EC1"][f"{turno}t"] = {
        "n_sec": len(d),
        "r2": round(float(1 - np.var(res)/np.var(d["logit"].values)), 4),
        "res_assimetria": round(float(stats.skew(d["zr"].dropna())), 3),
        "res_curtose": round(float(stats.kurtosis(d["zr"].dropna())), 3),
        "n_locais": len(loc_z),
        "locais_z_gt3": int((loc_z > 3).sum()),
        "locais_z_lt_m3": int((loc_z < -3).sum()),
        "loc_z_media": round(float(loc_z.mean()), 3) if len(loc_z) else 0,
    }
    pr(f"  {turno}t: R²={R['EC1'][f'{turno}t']['r2']}, locais z>3={R['EC1'][f'{turno}t']['locais_z_gt3']}, z<-3={R['EC1'][f'{turno}t']['locais_z_lt_m3']}")

# EC2: Correlação Lula × comparecimento dentro do município
pr("EC2: Correlação Lula × comparecimento...")
R["EC2"] = {}
NPERM = 100
for turno in (1, 2):
    vc = f"validos_{turno}"; v13c = f"v13_{turno}"
    comp_c = f"QT_COMPARECIMENTO_{turno}"; apt_c = f"QT_APTOS_{turno}"
    if df[vc].isna().all(): continue
    d = df[[vc, v13c, comp_c, apt_c, "mun"]].dropna().copy()
    d = d[d[vc] >= 20]
    d["p13"] = d[v13c] / d[vc]
    d["cr"] = d[comp_c] / d[apt_c].clip(lower=1)
    d["p13d"] = d["p13"] - d.groupby("mun")["p13"].transform("mean")
    d["crd"] = d["cr"] - d.groupby("mun")["cr"].transform("mean")
    fin = np.isfinite(d["p13d"]) & np.isfinite(d["crd"])
    corr_obs = float(stats.spearmanr(d.loc[fin, "p13d"], d.loc[fin, "crd"])[0])
    # Permutação vetorizada: embaralhar dentro do município usando sorting trick
    mun_arr = d["mun"].values
    p13d = d["p13d"].values
    crd = d["crd"].values
    mun_codes, mun_inv = np.unique(mun_arr, return_inverse=True)
    starts = np.searchsorted(np.sort(mun_inv), np.arange(len(mun_codes)))
    sorted_idx = np.argsort(mun_inv)
    mun_sizes = np.bincount(mun_inv)
    corr_perm = np.zeros(NPERM)
    for s in range(NPERM):
        pp = p13d.copy()
        for mi in range(len(mun_codes)):
            st = starts[mi]; sz = mun_sizes[mi]
            real_idx = sorted_idx[st:st+sz]
            pp[real_idx] = rng.permutation(pp[real_idx])
        f = np.isfinite(pp) & np.isfinite(crd)
        corr_perm[s] = stats.spearmanr(pp[f], crd[f])[0]
    p_val = float((np.abs(corr_perm) >= abs(corr_obs)).mean())
    R["EC2"][f"{turno}t"] = {
        "corr_obs": round(corr_obs, 4), "perm_media": round(float(corr_perm.mean()), 4),
        "perm_dp": round(float(corr_perm.std()), 4), "p": round(p_val, 4), "n": len(d),
    }
    pr(f"  {turno}t: corr={corr_obs:.4f}, p={p_val:.4f}")


# ============================================================
# FAMÍLIA D — VARREDURA TERRITORIAL
# ============================================================
pr("\n--- Família D: Varredura territorial ---")
pr("ED1: Scan por município...")
R["ED1"] = {}
NPERM_D = 200
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
    max_perm = np.zeros(NPERM_D)
    for s in range(NPERM_D):
        zp = z_arr.copy()
        for uv in np.unique(uf_arr):
            ix = uf_arr == uv; zp[ix] = rng.permutation(zp[ix])
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
# FAMÍLIA E — PRIMEIRO VS SEGUNDO TURNO
# ============================================================
pr("\n--- Família E: Turnos ---")

# EE1: Linearidade entre turnos
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
# Simulação beta-binomial para referência (amostra de 100 municípios)
r2_sim_all = []
sample_muns = rng.choice(d["mun"].unique(), min(100, d["mun"].nunique()), replace=False)
for _ in range(100):
    for m in sample_muns:
        g = d[d["mun"] == m]
        if len(g) < 10: continue
        n2 = g["validos_2"].astype(int).values
        pm = g["v13_2"].sum() / g["validos_2"].sum()
        a, b = max(pm*99, 0.1), max((1-pm)*99, 0.1)
        ps = rng.beta(a, b, size=len(n2)).clip(0.001, 0.999)
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
    "r2_sim_p90": round(float(np.percentile(r2_sim, 90)), 4),
}
pr(f"  R² mediano obs={np.median(r2a):.4f}, sim={np.median(r2_sim):.4f}")

# EE2: Resíduos modulares
pr("EE2: Resíduos modulares...")
d["dif"] = (d["v13_2"] - d["v13_1"]).astype(int)
R["EE2"] = {}
for k in [2, 5, 10]:
    obs = np.bincount(d["dif"].values % k, minlength=k)
    esp = np.full(k, len(d)/k)
    chi2 = float(np.sum((obs - esp)**2 / esp))
    # Referência: simulação com proporção municipal
    mun_p = d.groupby("mun")["v13_2"].sum() / d.groupby("mun")["validos_2"].sum()
    pm = d["mun"].map(mun_p).values.clip(0.001, 0.999)
    chi2_s = np.zeros(200)
    for s in range(200):
        sv = rng.binomial(d["validos_2"].astype(int).values, pm)
        sd = sv - d["v13_1"].astype(int).values
        sc = np.bincount(sd % k, minlength=k).astype(float)
        chi2_s[s] = float(np.sum((sc - esp)**2 / esp))
    p_val = float((chi2_s >= chi2).mean())
    R["EE2"][f"mod_{k}"] = {"contagens": obs.tolist(), "chi2": round(chi2, 2),
                             "chi2_sim_media": round(float(chi2_s.mean()), 2), "p": round(p_val, 4)}
    pr(f"  mod {k}: chi2={chi2:.1f}, p={p_val:.4f}")


# ============================================================
# FAMÍLIA F — ALEATORIEDADE E TEMPORALIDADE
# ============================================================
pr("\n--- Família F: Temporalidade ---")
pr("EF1: Autocorrelação na ordem de recebimento...")
R["EF1"] = {}
for turno in (1, 2):
    vc = f"validos_{turno}"; v13c = f"v13_{turno}"; rc = f"DT_BU_RECEBIDO_{turno}"
    if df[vc].isna().all(): continue
    d = df[["mun", vc, v13c, rc]].dropna(subset=[vc, v13c, rc]).copy()
    d = d[d[vc] >= 20]
    d["logit"] = lg(d[v13c].astype(int), d[vc].astype(int))
    d["med_mun"] = d.groupby("mun")["logit"].transform("median")
    d["r"] = d["logit"] - d["med_mun"]
    d = d.sort_values(rc)
    acs, ws = [], []
    for mun, grp in d.groupby("mun"):
        if len(grp) < 5: continue
        r = grp["r"].values
        if r.std() < 1e-8: continue
        ac = np.corrcoef(r[:-1], r[1:])[0, 1]
        if np.isfinite(ac): acs.append(ac); ws.append(len(grp))
    ac_obs = float(np.average(acs, weights=ws)) if acs else 0
    # Permutação
    ac_perm = np.zeros(200)
    for s in range(200):
        acs_s, ws_s = [], []
        for mun, grp in d.groupby("mun"):
            if len(grp) < 5: continue
            r = rng.permutation(grp["r"].values)
            if r.std() < 1e-8: continue
            ac = np.corrcoef(r[:-1], r[1:])[0, 1]
            if np.isfinite(ac): acs_s.append(ac); ws_s.append(len(grp))
        if acs_s: ac_perm[s] = np.average(acs_s, weights=ws_s)
    p_val = float((np.abs(ac_perm) >= abs(ac_obs)).mean())
    R["EF1"][f"{turno}t"] = {
        "autocorr": round(ac_obs, 4), "perm_media": round(float(ac_perm.mean()), 4),
        "perm_dp": round(float(ac_perm.std()), 4), "p": round(p_val, 4),
        "n_mun": len(acs),
    }
    pr(f"  {turno}t: autocorr={ac_obs:.4f}, p={p_val:.4f}")

# ============================================================
out = os.path.join(AQUI, "..", "resultados", f"resultado_estresse_{ANO}.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(R, open(out, "w"), ensure_ascii=False, indent=1, default=str)
pr(f"\nSalvo em {out}")
pr("=== Fim ===")
