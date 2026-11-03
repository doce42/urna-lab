"""Validação do EB1: a subdispersão intra-local é artefato do rho estimado por UF?

Compara três estimativas de rho:
  1. rho por UF (o que o EB1 usou)
  2. rho por ZONA (intermediário)
  3. rho por LOCAL (dentro do próprio local, excluindo a seção)

Se com rho_local a subdispersão desaparece, é H7 (eleitores do mesmo local são parecidos).
Se persiste, é anomalia robusta.

Uso: python -u validar_eb1.py [2026|2022]
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

pr(f"=== Validação EB1 — {ANO} ===")
df = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/secoes_{ANO}.parquet"))
df = df[df["SG_UF"] != "ZZ"].copy()
df["mun"] = df["SG_UF"] + df["CD_MUNICIPIO"]
df["local_2"] = df["mun"] + "_" + df["NR_ZONA"] + "_" + df["NR_LOCAL_VOTACAO_2"].astype(str)
df["zona"] = df["SG_UF"] + "_" + df["NR_ZONA"]

def estimar_rho(v, n):
    if len(v) < 10: return 0.01
    p = v.sum() / n.sum()
    if p < 0.001 or p > 0.999: return 0.01
    var_obs = np.var(v/n)
    var_bin = np.mean(p*(1-p)/n)
    if var_obs <= var_bin: return 0.001
    return float(np.clip((var_obs - var_bin) / (p*(1-p) - var_bin + 1e-12), 0.001, 0.5))

R = {"ano": ANO}

for turno in (2,):  # focar no 2t
    vc = f"validos_{turno}"; v13c = f"v13_{turno}"
    if df[vc].isna().all(): continue
    pr(f"\nTurno {turno}:")

    # Estimar rho em três escalas
    rho_uf = {}
    for uf, g in df.groupby("SG_UF"):
        v = g[v13c].fillna(0).values.astype(int)
        n = g[vc].fillna(0).values.astype(int)
        m = n >= 20
        rho_uf[uf] = estimar_rho(v[m], n[m])

    rho_zona = {}
    for z, g in df.groupby("zona"):
        v = g[v13c].fillna(0).values.astype(int)
        n = g[vc].fillna(0).values.astype(int)
        m = n >= 20
        if m.sum() >= 10:
            rho_zona[z] = estimar_rho(v[m], n[m])

    rho_local = {}
    for loc, g in df.groupby("local_2"):
        v = g[v13c].fillna(0).values.astype(int)
        n = g[vc].fillna(0).values.astype(int)
        m = n >= 20
        if m.sum() >= 5:
            rho_local[loc] = estimar_rho(v[m], n[m])

    pr(f"  rho_UF mediano: {np.median(list(rho_uf.values())):.4f}")
    pr(f"  rho_zona mediano: {np.median(list(rho_zona.values())):.4f}" if rho_zona else "  rho_zona: vazio")
    pr(f"  rho_local mediano: {np.median(list(rho_local.values())):.4f}" if rho_local else "  rho_local: vazio")

    # Refazer o teste com cada escala de rho
    for escala_nome, rho_dict, fallback_dict in [
        ("UF", rho_uf, None),
        ("zona", rho_zona, rho_uf),
        ("local", rho_local, rho_zona if rho_zona else rho_uf),
    ]:
        sub_count, total = 0, 0
        p_vals = []
        for loc, grp in df.groupby("local_2"):
            v = grp[v13c].fillna(0).values.astype(int)
            n = grp[vc].fillna(0).values.astype(int)
            m = n >= 20; v, n = v[m], n[m]
            if len(v) < 5: continue
            total += 1
            p_loc = v.sum() / n.sum()
            if escala_nome == "UF":
                rho = rho_dict.get(grp["SG_UF"].iloc[0], 0.01)
            elif escala_nome == "zona":
                rho = rho_dict.get(grp["zona"].iloc[0], fallback_dict.get(grp["SG_UF"].iloc[0], 0.01) if fallback_dict else 0.01)
            else:
                rho = rho_dict.get(loc, fallback_dict.get(grp["zona"].iloc[0], 0.01) if fallback_dict else 0.01)
            rho = max(rho, 0.001)
            var_obs = np.var(v/n, ddof=1)
            var_esp = np.mean(p_loc*(1-p_loc)/n) * (1 + rho*(np.mean(n)-1))
            var_esp = max(var_esp, 1e-12)
            ratio = var_obs / var_esp
            k = len(v)
            chi2 = (k-1) * ratio
            p_sub = float(stats.chi2.cdf(chi2, k-1))
            p_vals.append(p_sub)

        pa = np.array(p_vals)
        nt = len(pa)
        lim = 0.05 * np.arange(1, nt+1) / nt
        sub_bh = int((np.sort(pa) <= lim).sum())
        frac_p001 = float((pa < 0.01).mean())
        pr(f"  rho_{escala_nome}: {total} locais, sub_BH={sub_bh} ({100*sub_bh/total:.1f}%), p<0.01={100*frac_p001:.1f}%")

        R[f"{turno}t_rho_{escala_nome}"] = {
            "total": total, "sub_bh": sub_bh,
            "frac_sub_bh": round(sub_bh/total, 4) if total else 0,
            "frac_p001": round(frac_p001, 4),
        }

out = os.path.join(AQUI, "..", "resultados", f"validacao_eb1_{ANO}.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(R, open(out, "w"), ensure_ascii=False, indent=1, default=str)
pr(f"\nSalvo em {out}")
