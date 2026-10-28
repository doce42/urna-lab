"""F3 / E2: curvas de apuração 2022 e 2026 (1º e 2º turno) sob três modelos nulos. Ver PREREG.md."""
import json, sys, time
import numpy as np, pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; OUT = RAIZ + "/fase3/resultados"
NPERM = 200; T0 = time.time()


def carrega(ano, t):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
    c = f"DT_BU_RECEBIDO_{t}"
    b = b[b[c].notna() & b[f"validos_{t}"].notna() & (b[f"validos_{t}"] > 0)].copy()
    b = b.sort_values([c]).reset_index(drop=True)
    return b


def estat(L, A, V, grade):
    """L, A, V: votos de Lula, adversário e válidos na ordem; devolve estatísticas S1-S5."""
    n = len(L); CL, CA, CV = np.cumsum(L), np.cumsum(A), np.cumsum(V)
    m = (CL - CA) / CV * 100                       # margem relativa acumulada, pp
    ini = int(0.10 * n)
    s = np.sign(m[ini:]); s = s[s != 0]
    inv = np.nonzero(np.diff(s))[0]
    S1 = int(len(inv)); idx_nz = np.nonzero(np.sign(m[ini:]) != 0)[0]
    S2 = float((ini + idx_nz[inv[-1] + 1]) / n) if S1 else 0.0
    pts = np.unique((np.arange(grade, 100 + grade / 2, grade) / 100 * n).astype(int).clip(1, n) - 1)
    mg = m[pts]; fr = (pts + 1) / n; sel = fr >= 0.10
    mg_s = mg[sel]
    S3 = float((np.maximum.accumulate(mg_s) - mg_s).max())
    d = np.diff(mg_s); S4 = int((np.diff(np.sign(d[d != 0])) != 0).sum())
    # S5: maior trecho linear (em número de faixas) com desvio máximo da reta entre as pontas <= 0,02 pp
    best = 0; k = len(mg_s)
    for i in range(k - 2):
        for j in range(i + 2, k):
            x = np.arange(i, j + 1); lin = mg_s[i] + (mg_s[j] - mg_s[i]) * (x - i) / (j - i)
            if np.abs(mg_s[i:j + 1] - lin).max() <= 0.02: best = max(best, j - i + 1)
            else: break
    return {"S1_inversoes": S1, "S2_fracao_ultima_inversao": S2, "S3_maior_vale_pp": S3, "S4_oscilacoes": S4, "S5_maior_trecho_linear_faixas": int(best),
            "_margem_final_pp": float(m[-1])}


def perm_A(n, rng): return rng.permutation(n)


def perm_grupo(rotulo, rng):
    """mantém a sequência real de rótulos e permuta as urnas dentro do rótulo"""
    n = len(rotulo); pos = np.arange(n)
    cod = pd.factorize(rotulo)[0]
    ordem_pos = np.lexsort((pos, cod))              # posições agrupadas por rótulo, em ordem real
    ordem_urna = np.lexsort((rng.random(n), cod))  # urnas agrupadas por rótulo, em ordem aleatória
    novo = np.empty(n, int); novo[ordem_pos] = ordem_urna
    return novo


def eta2(rotulo, valor):
    g = pd.Series(valor).groupby(rotulo)
    return float(((g.transform("mean") - valor.mean()) ** 2).sum() / ((valor - valor.mean()) ** 2).sum())


R = {"pergunta": "E2 curvas", "nperm": NPERM, "resultados": {}}
for ano in ("2026", "2022"):
    for t in (1, 2):
        b = carrega(ano, t); n = len(b)
        L = b[f"v13_{t}"].values.astype(float); A = b[f"v22_{t}"].values.astype(float); V = b[f"validos_{t}"].values.astype(float)
        uf = b["SG_UF"].values; mun = (b["SG_UF"] + b["CD_MUNICIPIO"]).values
        rk = np.arange(n) / n
        obs = estat(L, A, V, 1.0)
        # tempos das inversões (fração apurada) para descrever
        CL, CA, CV = np.cumsum(L), np.cumsum(A), np.cumsum(V); m = (CL - CA) / CV * 100; ini = int(0.10 * n)
        sg = np.sign(m[ini:]); nz = np.nonzero(sg != 0)[0]; ss = sg[nz]; ch = nz[np.nonzero(np.diff(ss))[0] + 1]
        R_ = {"urnas": n, "observado": obs, "primeiras_inversoes_fracao_apurada": [float((ini + c) / n) for c in ch[:15]],
              "eta2_ordem_de_chegada_por_UF": eta2(uf, rk), "eta2_ordem_de_chegada_por_municipio": eta2(mun, rk),
              "margem_aos_10pct_pp": float(m[ini]), "lider_aos_10pct": "Lula" if m[ini] > 0 else "adversário", "lider_final": "Lula" if m[-1] > 0 else "adversário"}
        rng = np.random.default_rng(3001 + (0 if ano == "2026" else 100) + t)
        for nome, f in (("A_permutacao_irrestrita", lambda: perm_A(n, rng)), ("B_dentro_de_UF", lambda: perm_grupo(uf, rng)), ("C_dentro_de_municipio", lambda: perm_grupo(mun, rng))):
            sims = [estat(L[o], A[o], V[o], 1.0) for o in (f() for _ in range(NPERM))]
            res = {}
            for k in obs:
                if k.startswith("_"): continue
                a = np.array([s[k] for s in sims], float); o = obs[k]
                res[k] = {"observado": o, "sim_media": float(a.mean()), "sim_p2_5_p97_5": [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))],
                          "p_bilateral": float(min(1, 2 * min((1 + (a >= o).sum()) / (NPERM + 1), (1 + (a <= o).sum()) / (NPERM + 1))))}
            R_[nome] = res
        # sensibilidade: grade 0,5% e 2% contra o modelo B
        sens = {}
        for g in (0.5, 2.0):
            ob = estat(L, A, V, g); sb = [estat(L[o], A[o], V[o], g) for o in (perm_grupo(uf, rng) for _ in range(NPERM))]
            sens[str(g)] = {k: {"observado": ob[k], "sim_media": float(np.mean([s[k] for s in sb])), "p_bilateral": float(min(1, 2 * min((1 + (np.array([s[k] for s in sb]) >= ob[k]).sum()) / (NPERM + 1), (1 + (np.array([s[k] for s in sb]) <= ob[k]).sum()) / (NPERM + 1))))}
                            for k in ob if not k.startswith("_") and k in ("S3_maior_vale_pp", "S4_oscilacoes", "S5_maior_trecho_linear_faixas")}
        R_["sensibilidade_grade_modelo_B"] = sens
        R["resultados"][f"{ano}_{t}t"] = R_
        print(ano, t, "ok", round(time.time() - T0), "s", flush=True)
R["tempo_s"] = round(time.time() - T0, 1)
json.dump(R, open(f"{OUT}/E2_curvas.json", "w"), indent=1, ensure_ascii=False, default=float)
