"""F3 / fila F4: modelo de chegada dos boletins. Atraso = recebimento − emissão do BU (log de minutos) regredido em UF, log do
tamanho do município, capital e faixa de 30 min da emissão; ordens simuladas = emissão real + previsão + resíduo sorteado dentro
da UF. Estatísticas: V (trocas de liderança na grade de 1% a partir de 10%), U (fração na última troca), S3 (maior vale, pp).
Validação em 2022 (observado entre os percentis 2,5 e 97,5) e nas capturas do R2 de 2022 2º turno. Ver fase3/PREREG_FILA.md (F4).
Saída: fase3/resultados/fila_f4_chegada.json."""
import json
import numpy as np, pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); NSIM = 200


def estat(L, A, grade=1.0):
    CL, CA = np.cumsum(L), np.cumsum(A); n = len(L)
    pts = np.unique((np.arange(grade, 100 + grade / 2, grade) / 100 * n).astype(int).clip(1, n) - 1)
    m = (CL[pts] - CA[pts]) / (CL[pts] + CA[pts]) * 100; fr = (pts + 1) / n; sel = fr >= 0.10
    ms, fs = m[sel], fr[sel]; sg = np.sign(ms); nz = sg != 0; sgn, fsn = sg[nz], fs[nz]
    trocas = np.nonzero(np.diff(sgn))[0]
    V = int(len(trocas)); U = float(fsn[trocas[-1] + 1]) if V else 0.0
    S3 = float((np.maximum.accumulate(ms) - ms).max())
    return V, U, S3


def carrega(ano, t):
    b = pd.read_parquet(f"{RAIZ}/analise/base.parquet" if ano == "2026" else f"{RAIZ}/analise/base_{ano}.parquet")
    b = b[b[f"total_{t}"].notna() & b[f"DT_BU_RECEBIDO_{t}"].notna()].copy()
    b["mun"] = b.SG_UF + b.CD_MUNICIPIO.astype(str)
    rec = pd.to_datetime(b[f"DT_BU_RECEBIDO_{t}"]); emi = pd.to_datetime(b[f"DT_EMISSAO_BU_{t}"], errors="coerce")
    b["rec"] = (rec - rec.min()).dt.total_seconds() / 60; b["emi"] = (emi - rec.min()).dt.total_seconds() / 60
    return b.sort_values("rec").reset_index(drop=True)


R = {"pre_registro": "fase3/PREREG_FILA.md (F4)", "nsim": NSIM, "eleicoes": {}}
cap = json.load(open(RAIZ + "/fase3/resultados/r2_curva_publica.json"))["eleicoes"]
for ano, t in (("2022", 1), ("2022", 2), ("2026", 1), ("2026", 2)):
    b = carrega(ano, t); L, A = b[f"v13_{t}"].fillna(0).values, b[f"v22_{t}"].fillna(0).values
    obs = estat(L, A)
    ok = b.emi.notna() & (b.rec >= b.emi)
    y = np.log1p((b.rec - b.emi)[ok].values)
    tam = b.groupby("mun")["mun"].transform("size"); cap_ = tam == b.groupby("SG_UF")["mun"].transform(lambda s: s.map(s.value_counts()).max())
    faixa = (b.emi // 30).fillna(-1).astype(int)
    X = pd.get_dummies(pd.DataFrame({"uf": b.SG_UF, "fx": faixa.astype(str)}), drop_first=True).astype(float)
    X["log_tam"] = np.log(tam.values); X["capital"] = cap_.astype(float).values; X["c"] = 1.0
    Xo = X[ok.values].values; beta, *_ = np.linalg.lstsq(Xo, y, rcond=None); pred = X.values @ beta
    res = y - Xo @ beta; r2 = float(1 - (res ** 2).sum() / ((y - y.mean()) ** 2).sum())
    uf_ok = b.SG_UF[ok].values; pools = {u: res[uf_ok == u] for u in np.unique(uf_ok)}
    rng = np.random.default_rng(9800 + int(ano) % 100 + t); sims = []; faixas = []
    for _ in range(NSIM):
        sr = b.rec.values.copy()
        for u, pool in pools.items():
            ix = np.where(ok.values & (b.SG_UF.values == u))[0]
            sr[ix] = b.emi.values[ix] + np.expm1(pred[ix] + pool[rng.integers(0, len(pool), len(ix))])
        o = np.argsort(sr, kind="stable"); sims.append(estat(L[o], A[o])); faixas.append((np.cumsum(L[o]), np.cumsum(A[o])))
    S = np.array(sims, float); nomes = ["V_trocas", "U_ultima_troca", "S3_maior_vale_pp"]
    E = {"secoes": len(b), "com_emissao": int(ok.sum()), "r2_modelo_atraso": r2, "observado": dict(zip(nomes, obs)),
         "simulado_p2_5_p97_5": {n: [float(np.percentile(S[:, i], 2.5)), float(np.percentile(S[:, i], 97.5))] for i, n in enumerate(nomes)},
         "simulado_mediana": {n: float(np.median(S[:, i])) for i, n in enumerate(nomes)},
         "dentro": {n: bool(np.percentile(S[:, i], 2.5) <= obs[i] <= np.percentile(S[:, i], 97.5)) for i, n in enumerate(nomes)},
         "fracao_sims_com_V_menor_ou_igual": float((S[:, 0] <= obs[0]).mean()), "fracao_sims_com_V_maior_ou_igual": float((S[:, 0] >= obs[0]).mean())}
    chave = f"{ano}_{t}T"
    if chave == "2022_2T":   # validação pela divulgação: proporção divulgada dentro da faixa de 95% das simulações no mesmo número de seções
        dent = []
        for c in cap[chave]["sequencia"]:
            st = min(max(int(c["secoes_totalizadas"]), 1), len(b)) - 1
            shares = [cl[st] / (cl[st] + ca[st]) * 100 for cl, ca in faixas]
            dent.append({"hora": c["hora"], "secoes": c["secoes_totalizadas"], "publicado": c["pct_lula_publicado"], "faixa95": [float(np.percentile(shares, 2.5)), float(np.percentile(shares, 97.5))],
                         "dentro": bool(np.percentile(shares, 2.5) <= c["pct_lula_publicado"] <= np.percentile(shares, 97.5))})
        E["validacao_capturas"] = {"capturas": len(dent), "dentro": sum(d["dentro"] for d in dent), "detalhe": dent}
    R["eleicoes"][chave] = E
    print(chave, "r2", round(r2, 3), "obs", obs, "faixas", E["simulado_p2_5_p97_5"], "dentro", E["dentro"], E.get("validacao_capturas", {}).get("dentro"), flush=True)
v22 = all(all(R["eleicoes"][k]["dentro"].values()) for k in ("2022_1T", "2022_2T")) and R["eleicoes"]["2022_2T"]["validacao_capturas"]["dentro"] == R["eleicoes"]["2022_2T"]["validacao_capturas"]["capturas"]
R["validado"] = bool(v22)
for k in ("2026_1T", "2026_2T"):
    e = R["eleicoes"][k]
    e["leitura"] = ("não determinado (modelo não validado)" if not v22 else ("não incomum sob o modelo" if all(e["dentro"].values()) else "incomum sob o modelo em: " + ", ".join(n for n, d in e["dentro"].items() if not d)))
print("validado", v22, {k: R["eleicoes"][k].get("leitura") for k in ("2026_1T", "2026_2T")})
json.dump(R, open(RAIZ + "/fase3/resultados/fila_f4_chegada.json", "w"), ensure_ascii=False, indent=1, default=float)
