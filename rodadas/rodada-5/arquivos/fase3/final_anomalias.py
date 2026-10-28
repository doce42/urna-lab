"""Z3 (fase3/PREREG_FINAL.md): as anomalias pequenas de 2026, descritas. (a) as 8 urnas da rajada sem biometria (regra do P10
reproduzida): votos no fim do dia, proporção de Lula na urna × município. (b) seções com |z| > 5 no T02: local, vizinhas do mesmo
local, comparecimento. Validação: mesmas medidas em 2022. Saída: fase3/resultados/final_anomalias.json."""
import glob, json
import numpy as np, pandas as pd
from scipy import stats

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"
src = open(RAIZ + "/fase3/adv_casos.py").read().split('R = {"pre_registro"')[0]; exec(src)   # base(), K


def bh(p, q=0.05):
    p = np.asarray(p); n = len(p); o = np.argsort(p); passa = p[o] <= q * np.arange(1, n + 1) / n
    k = np.max(np.where(passa)[0]) + 1 if passa.any() else 0; s = np.zeros(n, bool); s[o[:k]] = True; return s


R = {"pre_registro": "fase3/PREREG_FINAL.md (Z3)"}
for ano, pas, t in (("2026", "1t", 1), ("2022", "2022_1t", 1)):
    b = base(ano).set_index("k")
    u = pd.concat([pd.read_parquet(f, columns=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "modelo", "seq_ult30_votos", "seq_ult30_sem_biometria", "seq_resto_votos", "seq_resto_sem_biometria", "ultimo_voto"]) for f in glob.glob(f"{AN}/brutos/{pas}/urnas_*.parquet")], ignore_index=True)
    u = u.dropna(subset=["seq_ult30_votos"]); u = u[u.seq_ult30_votos > 0].copy()
    n, x, N, y = u.seq_resto_votos.values, u.seq_resto_sem_biometria.values, u.seq_ult30_votos.values.astype(int), u.seq_ult30_sem_biometria.values.astype(int)
    u["g"] = u.SG_UF.astype(str) + "|" + u.modelo.astype(str); p = np.ones(len(u))
    for gname, ix in u.groupby("g").indices.items():
        nn, xx = n[ix], x[ix]; ok = nn > 0
        if ok.sum() < 30: a_, b_ = 1.0, 7.0
        else:
            m = xx[ok].sum() / nn[ok].sum(); rr = xx[ok] / nn[ok]; vb = max(np.var(rr) - np.mean(m * (1 - m) / nn[ok]), 1e-6); s = max(m * (1 - m) / vb - 1, 2.0); a_, b_ = m * s, (1 - m) * s
        p[ix] = stats.betabinom.sf(y[ix] - 1, N[ix], a_ + xx, b_ + nn - xx)
    u["sig"] = bh(p); sel = u[u.sig].copy(); sel["k"] = [K(*r) for r in zip(sel.SG_UF, sel.CD_MUNICIPIO, sel.NR_ZONA, sel.NR_SECAO)]
    urnas = []
    for _, r in sel.iterrows():
        if r.k not in b.index: continue
        s_ = b.loc[r.k]; mun = b[b.mun == s_.mun]
        urnas.append({"secao": r.k, "votos_ult30": int(r.seq_ult30_votos), "sem_biometria_ult30": int(r.seq_ult30_sem_biometria), "resto_do_dia": int(r.seq_resto_votos), "sem_biometria_resto": int(r.seq_resto_sem_biometria),
                      "ultimo_voto": r.ultimo_voto, "lula_1T_secao": float(s_.v13_1 / s_.validos_1), "lula_1T_municipio": float(mun.v13_1.sum() / mun.validos_1.sum()), "z_virada_T02": float(s_.z)})
    R[f"T28_{ano}"] = {"urnas": urnas, "votos_ult30_total": int(sum(x["votos_ult30"] for x in urnas)),
                       "lula_acima_do_municipio": sum(1 for x in urnas if x["lula_1T_secao"] > x["lula_1T_municipio"]), "lula_abaixo": sum(1 for x in urnas if x["lula_1T_secao"] < x["lula_1T_municipio"])}
    print("T28", ano, len(urnas), "votos", R[f"T28_{ano}"]["votos_ult30_total"], "Lula acima/abaixo do município:", R[f"T28_{ano}"]["lula_acima_do_municipio"], R[f"T28_{ano}"]["lula_abaixo"], flush=True)
    # (b) T02 extremos
    bb = b.copy(); bb["local"] = bb.mun + "-" + bb.NR_ZONA.astype(str) + "-" + bb.NR_LOCAL_VOTACAO_2.astype(str)
    bb["loo"] = (bb.groupby("local").z.transform("sum") - bb.z) / (bb.groupby("local").z.transform("size") - 1).replace(0, np.nan)
    bb["dcomp"] = bb.QT_COMPARECIMENTO_2 / bb.QT_APTOS_2 - bb.QT_COMPARECIMENTO_1 / bb.QT_APTOS_1
    bb["sw"] = lg(bb.v13_2, bb.validos_2) - lg(bb.v13_1, bb.validos_1); bb["swmed"] = bb.groupby("mun").sw.transform("median")
    ext = bb[bb.z.abs() > 5]
    for lado, e in (("pro_lula", ext[ext.z > 0]), ("pro_adversario", ext[ext.z < 0])):
        R[f"T02_{ano}_{lado}"] = {"secoes": int(len(e)), "locais_distintos": int(e.local.nunique()), "ufs": e.SG_UF.value_counts().head(6).to_dict(),
                                   "z_medio_das_outras_secoes_do_local": float(e.loo.mean()), "dcomparecimento_medio_pp": float(100 * e.dcomp.mean()), "dcomparecimento_geral_pp": float(100 * bb.dcomp.mean()),
                                   "excesso_votos_lula": float((e.v13_2 - (1 / (1 + np.exp(-(lg(e.v13_1, e.validos_1) + e.swmed)))) * e.validos_2).sum())}
        print("T02", ano, lado, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in R[f"T02_{ano}_{lado}"].items()}, flush=True)
json.dump(R, open(RAIZ + "/fase3/resultados/final_anomalias.json", "w"), ensure_ascii=False, indent=1, default=str)
