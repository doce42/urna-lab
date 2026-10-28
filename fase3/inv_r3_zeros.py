"""F3 / R3: zeros de votos com regressão logística de I(y=0) e I(y<=2), ajustada numa metade dos municípios e avaliada na outra
(e vice-versa). Critério de calibração e leitura fixados em fase3/PREREG_RESPOSTAS.md (R3). Saída: fase3/resultados/r3_zeros.json."""
import json
import numpy as np, pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; NSIM, NBOOT = 4000, 1000
logit = lambda p: np.log(p / (1 - p))


def carrega(ano):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
    b = b[(b["SG_UF"] != "ZZ") & (b["validos_1"].fillna(0) > 0) & (b["validos_2"].fillna(0) > 0)].reset_index(drop=True)
    b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"].astype(str); b["zona"] = b["mun"] + "-" + b["NR_ZONA"].astype(str)
    return b


def loo(y, n, g):
    gy = pd.Series(y).groupby(g).transform("sum").values - y; gn = pd.Series(n).groupby(g).transform("sum").values - n
    return logit((gy + 0.5) / (gn + 1.0))


def X_de(b, col, t, com_1t=True):
    y = b[f"{col}_{t}"].fillna(0).values.astype(float); n = b[f"validos_{t}"].values.astype(float)
    loc = (b["zona"] + "-" + b[f"NR_LOCAL_VOTACAO_{t}"].astype(str)).values
    cols = [np.ones(len(b)), np.log(n), loo(y, n, loc), loo(y, n, b["zona"].values), loo(y, n, b["mun"].values)]
    if t == 2 and com_1t and f"{col}_1" in b:
        y1, n1 = b[f"{col}_1"].fillna(0).values.astype(float), b["validos_1"].values.astype(float); cols.append(logit((y1 + 0.5) / (n1 + 1)))
    return np.column_stack(cols), y


def irls(X, y, it=50):
    beta = np.zeros(X.shape[1])
    for _ in range(it):
        eta = np.clip(X @ beta, -30, 30); p = 1 / (1 + np.exp(-eta)); w = p * (1 - p) + 1e-9
        z = eta + (y - p) / w; XtW = X.T * w
        nb = np.linalg.solve(XtW @ X + 1e-6 * np.eye(X.shape[1]), XtW @ z)
        if np.max(np.abs(nb - beta)) < 1e-8: beta = nb; break
        beta = nb
    return beta


def fora_da_amostra(b, X, alvo, metade):
    p = np.zeros(len(b))
    for h in (0, 1):
        tr, te = metade != h, metade == h
        p[te] = 1 / (1 + np.exp(-np.clip(X[te] @ irls(X[tr], alvo[tr]), -30, 30)))
    return p


def avalia(b, p, alvo, rng):
    obs, esp = int(alvo.sum()), float(p.sum())
    sims = (rng.random((NSIM // 4, len(p))) < p).sum(1) if esp < 2000 else rng.normal(esp, np.sqrt((p * (1 - p)).sum()), NSIM)
    dec = pd.qcut(pd.Series(p).rank(method="first"), 10, labels=False)
    tab = pd.DataFrame({"d": dec, "o": alvo, "e": p}).groupby("d").sum()
    hl = float((((tab.o - tab.e) ** 2) / (tab.e * (1 - tab.e / pd.Series(dec).value_counts().sort_index().values) + 1e-9)).sum())
    from scipy import stats
    om = pd.Series(alvo).groupby(b["mun"].values).sum().values; em = pd.Series(p).groupby(b["mun"].values).sum().values
    ix = rng.integers(0, len(om), (NBOOT, len(om))); rb = om[ix].sum(1) / np.maximum(em[ix].sum(1), 1e-9)
    return {"observado": obs, "esperado": esp, "razao_obs_esp": obs / esp if esp else None, "ic_predicao_95": [float(np.percentile(sims, 2.5)), float(np.percentile(sims, 97.5))],
            "ic95_razao_bootstrap_mun": [float(np.percentile(rb, 2.5)), float(np.percentile(rb, 97.5))],
            "hosmer_lemeshow": hl, "hl_p": float(stats.chi2.sf(hl, 8)), "razao_3_decis_superiores": [float(tab.o.iloc[k] / tab.e.iloc[k]) if tab.e.iloc[k] > 0 else None for k in (7, 8, 9)]}


def calibrado(a):
    ok_tot = a["esperado"] > 0 and abs(a["observado"] - a["esperado"]) / a["esperado"] <= 0.15
    ok_dec = a["hl_p"] >= 0.01 or all(r is not None and 0.8 <= r <= 1.25 for r in a["razao_3_decis_superiores"])
    return bool(ok_tot and ok_dec), bool(ok_tot), bool(ok_dec)


R = {"pre_registro": "fase3/PREREG_RESPOSTAS.md (R3)"}
CONJ = {"2026": {"alvo": "v22", "controles": [("Lula", "v13", (1, 2)), ("cand. 70", "v70", (1,)), ("cand. 14", "v14", (1,))]},
        "2022": {"alvo": "v22", "controles": [("Lula", "v13", (1, 2)), ("Tebet", "v15", (1,)), ("Ciro", "v12", (1,))]}}
for com_1t in (True, False):                       # False = sensibilidade (sem a covariável do 1º turno)
    chave = "principal" if com_1t else "sensibilidade_sem_1T"; R[chave] = {}
    for ano, cfg in CONJ.items():
        b = carrega(ano); rng = np.random.default_rng(9300 + int(ano) % 100)
        muns = b["mun"].unique(); sorteio = dict(zip(muns, np.random.default_rng(9300).integers(0, 2, len(muns))))
        metade = b["mun"].map(sorteio).values
        Ra = {"controles": {}, "alvo": {}}
        for nome, col, turnos in cfg["controles"]:
            for t in turnos:
                X, y = X_de(b, col, t, com_1t); p = fora_da_amostra(b, X, (y == 0).astype(float), metade)
                a = avalia(b, p, (y == 0).astype(float), rng); a["calibrado"] = calibrado(a); Ra["controles"][f"{nome} {t}T zeros"] = a
        for t in (1, 2):
            X, y = X_de(b, cfg["alvo"], t, com_1t)
            p2 = fora_da_amostra(b, X, (y <= 2).astype(float), metade); a2 = avalia(b, p2, (y <= 2).astype(float), rng); a2["calibrado"] = calibrado(a2)
            Ra["controles"][f"alvo {t}T y<=2 (verificação preditiva)"] = a2
            p0 = fora_da_amostra(b, X, (y == 0).astype(float), metade); a0 = avalia(b, p0, (y == 0).astype(float), rng)
            Ra["alvo"][f"{t}T zeros"] = a0
        valid = all(v["calibrado"][0] for v in Ra["controles"].values())
        Ra["validado"] = valid
        Ra["controles_que_falharam"] = [k for k, v in Ra["controles"].items() if not v["calibrado"][0]]
        for k, a0 in Ra["alvo"].items():
            if not valid: a0["leitura"] = "não determinado (modelo não validado pelo critério pré-registrado)"
            elif a0["observado"] > a0["ic_predicao_95"][1]: a0["leitura"] = "incomum"
            else: a0["leitura"] = "não incomum"
        R[chave][ano] = Ra
        print(chave, ano, "validado", valid, "falharam", Ra["controles_que_falharam"], {k: (v["observado"], round(v["esperado"], 1), [round(x, 1) for x in v["ic_predicao_95"]], v.get("leitura")) for k, v in Ra["alvo"].items()}, flush=True)
        for k, v in Ra["controles"].items(): print("   ", k, v["observado"], round(v["esperado"], 1), "HLp", round(v["hl_p"], 3), [None if r is None else round(r, 2) for r in v["razao_3_decis_superiores"]], v["calibrado"])
json.dump(R, open(f"{RAIZ}/fase3/resultados/r3_zeros.json", "w"), ensure_ascii=False, indent=1, default=float)
