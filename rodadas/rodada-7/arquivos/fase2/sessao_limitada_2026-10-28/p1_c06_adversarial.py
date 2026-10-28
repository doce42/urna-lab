"""P1: C06 sob heterogeneidade. Uso: p1_c06_adversarial.py <principal|sensibilidade> [--fumaca]
Estimador = cópia literal de analise/comportamento.py (restrito, por UF, combinação ponderada)."""
import json, os, sys, time
import numpy as np, pandas as pd
from scipy.optimize import minimize

AN = "analise"
AQUI = os.path.dirname(os.path.abspath(__file__))
MODO = sys.argv[1]; FUMACA = "--fumaca" in sys.argv
SEED, GAMMA, NREP = (1001, 0.5, 10) if MODO == "principal" else (2002, 1.0, 10)
CEN = [("S0", 0, "none"), ("S1", 1, "iid"), ("S2+", 1, "ctx+"), ("S2-", 1, "ctx-")] if MODO == "principal" else \
      [("S0", 0, "none"), ("S1", 1, "iid"), ("S2+", 1, "ctx+"), ("S2-", 1, "ctx-")]
if FUMACA: NREP = 1


def carrega(ANO):
    b = pd.read_parquet(f"{AN}/base.parquet" if ANO == "2026" else f"{AN}/base_{ANO}.parquet")
    b = b[b["total_1"].notna() & b["total_2"].notna() & (b["SG_UF"] != "ZZ")].copy()
    b = b[(b["QT_APTOS_1"] >= 50) & (b["QT_APTOS_2"] >= 50)]
    b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
    cands1 = [c for c in b.columns if c.startswith("v") and c.endswith("_1") and c != "validos_1"]
    total1 = {c: b[c].sum() for c in cands1}
    principais = [c for c in sorted(cands1, key=lambda c: -total1[c]) if c not in ("v13_1", "v22_1")][:4]
    outros = [c for c in cands1 if c not in principais + ["v13_1", "v22_1"]]
    apt1, apt2 = b["QT_APTOS_1"], b["QT_APTOS_2"]
    X = pd.DataFrame({"Lula (1º)": b["v13_1"] / apt1, "Adversário (1º)": b["v22_1"] / apt1})
    for c in principais: X[c[:-2]] = b[c] / apt1
    X["Outros candidatos (1º)"] = b[outros].sum(axis=1) / apt1
    X["Branco/nulo (1º)"] = (b["branco_1"] + b["nulo_1"]) / apt1
    X["Abstenção (1º)"] = 1 - b["QT_COMPARECIMENTO_1"] / apt1
    Y = pd.DataFrame({"Lula": b["v13_2"] / apt2, "Adversário": b["v22_2"] / apt2,
                      "Branco/nulo": (b["branco_2"] + b["nulo_2"]) / apt2, "Abstenção": 1 - b["QT_COMPARECIMENTO_2"] / apt2})
    ok = X.notna().all(axis=1) & Y.notna().all(axis=1)
    return b[ok], X[ok], Y[ok], apt1[ok].values.astype(float), apt2[ok].values.astype(float)


def restrito(Xm, Ym, wm):  # cópia literal de comportamento.py
    k, m = Xm.shape[1], Ym.shape[1]
    wm = wm / wm.sum()
    XtX = (Xm * wm[:, None]).T @ Xm
    XtY = (Xm * wm[:, None]).T @ Ym
    f = lambda v: float(np.sum(v.reshape(k, m) * (XtX @ v.reshape(k, m))) - 2 * np.sum(v.reshape(k, m) * XtY))
    g = lambda v: (2 * (XtX @ v.reshape(k, m)) - 2 * XtY).ravel()
    cons = [{"type": "eq", "fun": (lambda v, i=i: v.reshape(k, m)[i].sum() - 1)} for i in range(k)]
    v0 = np.full(k * m, 1.0 / m)
    res = minimize(f, v0, jac=g, bounds=[(0, 1)] * (k * m), constraints=cons, method="SLSQP", options={"maxiter": 2000, "ftol": 1e-12})
    return res.x.reshape(k, m), res.success


def c06(Xv, Yv, w, uf, ufs=None):
    por, pes, nc = {}, {}, 0
    for u in np.unique(uf):
        sel = uf == u
        if sel.sum() < 200 or (ufs is not None and u not in ufs): continue
        por[u], s = restrito(Xv[sel], Yv[sel], w[sel]); nc += (not s)
        pes[u] = (Xv[sel] * w[sel][:, None]).sum(axis=0)
    Pw = np.array([pes[u] for u in por]); Ms = np.array([por[u] for u in por])
    return (Ms * Pw[:, :, None]).sum(axis=0) / Pw.sum(axis=0)[:, None], list(por), nc


def softmax_pert(B0, shift):  # B0 (k,m); shift (n,) -> (n,k,m)
    d = np.array([1, -1, 0, 0.0])
    lg = np.log(np.maximum(B0, 1e-9))[None] + shift[:, None, None] * d[None, None, :]
    e = np.exp(lg - lg.max(axis=2, keepdims=True)); return e / e.sum(axis=2, keepdims=True)


def contabil(ANO, b, X, Y, w, uf, Bgrav, R):
    s = lambda c: float(b[c].sum())
    L1, A1, L2, A2 = s("v13_1"), s("v22_1"), s("v13_2"), s("v22_2")
    apt = float(b["QT_APTOS_1"].sum()); c1, c2 = s("QT_COMPARECIMENTO_1"), s("QT_COMPARECIMENTO_2")
    bn1, bn2 = s("branco_1") + s("nulo_1"), s("branco_2") + s("nulo_2")
    v1, v2 = s("validos_1"), s("validos_2")
    outros = v1 - L1 - A1
    pool = outros + (bn1 - bn2) + (c2 - c1)  # eliminados + queda de branco/nulo + queda de abstenção
    ac = {"aptos_1t": apt, "aptos_2t": float(b["QT_APTOS_2"].sum()), "comparecimento_1t": c1, "comparecimento_2t": c2,
          "lula_1t": L1, "lula_2t": L2, "adv_1t": A1, "adv_2t": A2, "outros_candidatos_1t": outros, "branco_nulo_1t": bn1, "branco_nulo_2t": bn2,
          "delta_lula": L2 - L1, "delta_adv": A2 - A1, "delta_comparecimento": c2 - c1,
          "identidade_validos_ok": abs((v2 - v1) - ((c2 - c1) - (bn2 - bn1))) < 1,
          "reservatorio_liquido_(outros+queda_BN+queda_abstencao)": pool,
          "delta_lula_mais_delta_adv": (L2 - L1) + (A2 - A1),
          "identidade_reservatorio_ok": abs(pool - ((L2 - L1) + (A2 - A1))) < 1,
          "fracao_ganho_lula_dentro_do_reservatorio": (L2 - L1) / pool,
          "abstencao_1t": apt - c1,
          "limite_abs_para_voto_2t": {"minimo_pela_conta": max(0.0, c2 - c1), "maximo": min(apt - c1, c2)},
          "limite_abs_para_lula": {"minimo": 0.0, "maximo": min(apt - c1, L2)}}
    ab = apt - c1; i = list(X.columns).index("Abstenção (1º)")
    ac["estimativa_c06_abstencao_1t"] = {"para_lula": float(Bgrav[i, 0] * ab), "para_adv": float(Bgrav[i, 1] * ab), "razao": float(Bgrav[i, 0] / Bgrav[i, 1])}
    ac["estimativa_c06_origem_do_voto_lula_2t"] = {n: float(Bgrav[j, 0] * (X.values[:, j] * w).sum()) for j, n in enumerate(X.columns)}
    R["contabilidade"] = ac


def roda(ANO):
    t0 = time.time()
    b, X, Y, apt1, apt2 = carrega(ANO)
    uf = b["SG_UF"].values; mun = b["mun"].values
    ufs = None
    if FUMACA: ufs = {"AC", "RR", "SE"}
    out = {"ano": ANO, "secoes": int(len(b))}
    grav = json.load(open(f"{AN}/resultado_comportamento_{ANO}.json"))["C06"]
    Bgrav = np.array(grav["matriz"])
    # A. reprodução do C06 gravado
    Bhat, ufl, nc = c06(X.values, Y.values, apt1, uf, ufs)
    if not FUMACA:
        out["reproducao_c06"] = {"max_diferenca_matriz": float(np.abs(Bhat - Bgrav).max()), "nao_convergiu_ufs": int(nc), "ufs": len(ufl)}
        contabil(ANO, b, X, Y, apt1, uf, Bgrav, out)
    # B. adversarial
    B0 = Bgrav
    rng = np.random.default_rng(SEED + (0 if ANO == "2026" else 7))
    um = pd.Series(mun).astype("category"); codm = um.cat.codes.values; nm = codm.max() + 1
    p1 = (b["v13_1"] / b["validos_1"]).values
    mm = pd.Series(p1).groupby(codm).mean()  # % de Lula médio do município
    ufm = pd.Series(uf).groupby(codm).first().values
    zctx = ((mm - mm.groupby(ufm).transform("mean")) / mm.groupby(ufm).transform("std").replace(0, 1)).fillna(0).values
    keys = list(X.columns); iab = keys.index("Abstenção (1º)"); ibn = keys.index("Branco/nulo (1º)")
    res = []
    for nome, usa, tipo in CEN:
        for r in range(NREP):
            g = GAMMA * usa
            if tipo == "iid": z = rng.standard_normal(nm)
            elif tipo == "ctx+": z = zctx
            elif tipo == "ctx-": z = -zctx
            else: z = np.zeros(nm)
            Bi = softmax_pert(B0, g * z[codm])           # (n,9,4)
            Pexp = np.einsum("nj,njk->nk", X.values, Bi)
            Pexp = Pexp / Pexp.sum(axis=1, keepdims=True)
            cnt = rng.multinomial(apt2.astype(int), Pexp)
            Ys = cnt / apt2[:, None]
            Bh, _, nc2 = c06(X.values, Ys, apt1, uf, ufs)
            sel = np.isin(uf, ufl)
            Wt = X.values[sel] * apt1[sel, None]
            T = np.einsum("nj,njk->jk", Wt, Bi[sel]) / Wt.sum(axis=0)[:, None]
            err = Bh - T
            prev = (X.values[sel] * apt1[sel, None]).sum(axis=0) @ Bh; obs = (Ys[sel] * apt1[sel, None]).sum(axis=0)
            res.append({"cenario": nome, "rep": r, "gamma": g,
                        "abs_lula": [float(T[iab, 0]), float(Bh[iab, 0])], "abs_adv": [float(T[iab, 1]), float(Bh[iab, 1])],
                        "bn_lula": [float(T[ibn, 0]), float(Bh[ibn, 0])],
                        "razao_abs": [float(T[iab, 0] / T[iab, 1]), float(Bh[iab, 0] / max(Bh[iab, 1], 1e-9))],
                        "eam_36": float(np.abs(err).mean()), "eam_abs_row": float(np.abs(err[iab]).mean()),
                        "erro_total_2t_lula_rel": float((prev[0] - obs[0]) / obs[0]), "nao_convergiu": int(nc2)})
        print(ANO, nome, f"{time.time()-t0:.0f}s", flush=True)
    out["adversarial"] = res; out["seed"] = SEED; out["gamma"] = GAMMA; out["nrep"] = NREP
    out["tempo_s"] = time.time() - t0
    return out


R = {"modo": MODO, "fumaca": FUMACA, "anos": {a: roda(a) for a in ("2026", "2022")}}
nome = f"p1_resultado_{MODO}{'_fumaca' if FUMACA else ''}.json"
json.dump(R, open(os.path.join(AQUI, nome), "w"), indent=1, ensure_ascii=False, default=float)
print("gravado", nome)
