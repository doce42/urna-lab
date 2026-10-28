"""Módulos B e C do PROTOCOLO: comportamento do eleitor e o que mudou entre os turnos.

Uso: python comportamento.py [2026|2022]   (perfil demográfico só existe para 2026)
Saída: resultado_comportamento_<ano>.json

C01 comparecimento por região, tamanho de município e perfil (2026)
C03 voto x perfil demográfico (2026), dentro do município
C04 voto e virada por região e por tamanho de município
C06 matriz de transferência de votos 1º -> 2º turno (Goodman com efeito fixo de município, ponderada pelo eleitorado),
    com intervalo por bootstrap de municípios
C07 mudança de comparecimento x perfil (2026)
C08 virada por UF e por região
"""
import json
import os
import sys

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"
b = pd.read_parquet(os.path.join(AQUI, "base.parquet" if ANO == "2026" else f"base_{ANO}.parquet"))
b = b[b["total_1"].notna() & b["total_2"].notna() & (b["SG_UF"] != "ZZ")].copy()
b = b[(b["QT_APTOS_1"] >= 50) & (b["QT_APTOS_2"] >= 50)]
b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
REG = {**{u: "Nordeste" for u in "AL BA CE MA PB PE PI RN SE".split()}, **{u: "Norte" for u in "AC AM AP PA RO RR TO".split()},
       **{u: "Centro-Oeste" for u in "DF GO MS MT".split()}, **{u: "Sudeste" for u in "ES MG RJ SP".split()}, **{u: "Sul" for u in "PR RS SC".split()}}
b["regiao"] = b["SG_UF"].map(REG)
R = {"ano": ANO}

cands1 = [c for c in b.columns if c.startswith("v") and c.endswith("_1") and c != "validos_1"]
total1 = {c: b[c].sum() for c in cands1}
principais = [c for c in sorted(cands1, key=lambda c: -total1[c]) if c not in ("v13_1", "v22_1")][:4]  # 4 maiores eliminados
outros = [c for c in cands1 if c not in principais + ["v13_1", "v22_1"]]

# ---------- C06 transferência de votos (base: eleitorado apto) ----------
apt1, apt2 = b["QT_APTOS_1"], b["QT_APTOS_2"]
X = pd.DataFrame({"Lula (1º)": b["v13_1"] / apt1, "Adversário (1º)": b["v22_1"] / apt1})
for c in principais:
    X[c[:-2]] = b[c] / apt1
X["Outros candidatos (1º)"] = b[outros].sum(axis=1) / apt1
X["Branco/nulo (1º)"] = (b["branco_1"] + b["nulo_1"]) / apt1
X["Abstenção (1º)"] = 1 - b["QT_COMPARECIMENTO_1"] / apt1
Y = pd.DataFrame({"Lula": b["v13_2"] / apt2, "Adversário": b["v22_2"] / apt2,
                  "Branco/nulo": (b["branco_2"] + b["nulo_2"]) / apt2, "Abstenção": 1 - b["QT_COMPARECIMENTO_2"] / apt2})
# nome legível dos eliminados
nomes = {}
for c in principais:
    col = [k for k in b.columns if k == c]
    nomes[c[:-2]] = c[1:-2]
w = apt1.values
ok = X.notna().all(axis=1) & Y.notna().all(axis=1)
X, Y, w, mun = X[ok], Y[ok], w[ok.values], b.loc[ok, "mun"].values


def goodman(X, Y, w, mun):
    """Regressão de Goodman: Y_k = soma_j beta_jk * X_j, sem intercepto (as frações de X somam 1),
    com efeito fixo de município aplicado como desvio da média ponderada do município."""
    Xd, Yd = X.copy(), Y.copy()
    g = pd.Series(mun)
    for df in (Xd, Yd):
        for c in df.columns:
            m = (df[c] * w).groupby(g.values).transform("sum").values / pd.Series(w).groupby(g.values).transform("sum").values
            df[c] = df[c].values - m
    # sem intercepto com efeito fixo: estima os coeficientes nos desvios; o nível vem da restrição de soma 1 por linha
    sw = np.sqrt(w)
    A = Xd.values * sw[:, None]
    out = {}
    for k in Y.columns:
        beta, *_ = np.linalg.lstsq(A, Yd[k].values * sw, rcond=None)
        out[k] = beta
    B = pd.DataFrame(out, index=X.columns)
    # o efeito fixo remove o nível comum; reancora para que a soma das linhas dê 1 e o total previsto bata com o observado
    return B


# Goodman com restrição (cada fração entre 0 e 1; cada linha soma 1), estimado estado por estado (reduz o viés de
# agregação) e combinado pelo peso de cada grupo em cada estado. Programa quadrático: min ||W^½ (Y − X B)||².
from scipy.optimize import minimize

uf = b.loc[ok, "SG_UF"].values


def restrito(Xm, Ym, wm):
    k, m = Xm.shape[1], Ym.shape[1]
    wm = wm / wm.sum()  # pesos normalizados: sem isso o objetivo chega a 1e12 e o otimizador não converge
    XtX = (Xm * wm[:, None]).T @ Xm
    XtY = (Xm * wm[:, None]).T @ Ym
    f = lambda v: float(np.sum(v.reshape(k, m) * (XtX @ v.reshape(k, m))) - 2 * np.sum(v.reshape(k, m) * XtY))
    g = lambda v: (2 * (XtX @ v.reshape(k, m)) - 2 * XtY).ravel()
    cons = [{"type": "eq", "fun": (lambda v, i=i: v.reshape(k, m)[i].sum() - 1)} for i in range(k)]
    v0 = np.full(k * m, 1.0 / m)
    res = minimize(f, v0, jac=g, bounds=[(0, 1)] * (k * m), constraints=cons, method="SLSQP",
                   options={"maxiter": 2000, "ftol": 1e-12})
    if not res.success:
        print("   não convergiu:", res.message)
    return res.x.reshape(k, m)


por_uf, pesos = {}, {}
for u in np.unique(uf):
    sel = uf == u
    if sel.sum() < 200:
        continue
    por_uf[u] = restrito(X.values[sel], Y.values[sel], w[sel])
    pesos[u] = (X.values[sel] * w[sel][:, None]).sum(axis=0)  # eleitores de cada grupo no estado
Pw = np.array([pesos[u] for u in por_uf])                    # estados x grupos
Ms = np.array([por_uf[u] for u in por_uf])                   # estados x grupos x destinos
B = pd.DataFrame((Ms * Pw[:, :, None]).sum(axis=0) / Pw.sum(axis=0)[:, None], index=X.columns, columns=Y.columns)
lo = np.array([[np.percentile(Ms[:, i, j], 10) for j in range(Ms.shape[2])] for i in range(Ms.shape[1])])
hi = np.array([[np.percentile(Ms[:, i, j], 90) for j in range(Ms.shape[2])] for i in range(Ms.shape[1])])
tot_x = (X.values * w[:, None]).sum(axis=0) / w.sum()
# conferência: a matriz reproduz o total observado do 2º turno?
prev = (X.values * w[:, None]).sum(axis=0) @ B.values
obs = (Y.values * w[:, None]).sum(axis=0)
nomes_cand = ({"v70": "Augusto Cury", "v14": "Renan Santos", "v55": "Ronaldo Caiado", "v30": "Romeu Zema"} if ANO == "2026" else
              {"v15": "Simone Tebet", "v12": "Ciro Gomes", "v44": "Soraya Thronicke", "v30": "Felipe d'Ávila"})
B.index = [nomes_cand.get(i, i) + (" (1º)" if i in nomes_cand else "") for i in B.index]
R["C06"] = {"linhas": list(B.index), "colunas": list(B.columns), "matriz": B.round(4).values.tolist(),
            "faixa_estados_p10": np.round(lo, 4).tolist(), "faixa_estados_p90": np.round(hi, 4).tolist(),
            "eleitores_1t": dict(zip(B.index, [int(round(v * w.sum())) for v in tot_x])),
            "conferencia_total_previsto": dict(zip(Y.columns, [int(v) for v in prev])),
            "conferencia_total_observado": dict(zip(Y.columns, [int(v) for v in obs])),
            "por_uf": {u: {"matriz": np.round(por_uf[u], 4).tolist(), "eleitores_por_grupo": [int(v) for v in pesos[u]]} for u in por_uf},
            "metodo": "Goodman com restrição (0 a 1, linhas somam 1), por UF, ponderado; faixa = percentis 10 e 90 entre UFs",
            "nota": "Inferência ecológica: estimativa média de grupos, não comportamento individual."}

# ---------- C04/C08 região, UF e tamanho do município ----------
def pct(df, n):
    return 100 * df[f"v13_{n}"].sum() / df[f"validos_{n}"].sum()


tam = b.groupby("mun")["QT_APTOS_2"].transform("sum")
b["porte"] = pd.cut(tam, [0, 10_000, 50_000, 200_000, 1_000_000, 1e9],
                    labels=["até 10 mil eleitores", "10–50 mil", "50–200 mil", "200 mil–1 milhão", "mais de 1 milhão"])
for nome, chave in (("regiao", "regiao"), ("porte", "porte"), ("uf", "SG_UF")):
    g = b.groupby(chave, observed=True)
    R[f"C08_{nome}"] = {str(k): {"lula_1t": round(pct(x, 1), 2), "lula_2t": round(pct(x, 2), 2),
                                 "virada_pp": round(pct(x, 2) - pct(x, 1), 2),
                                 "comparecimento_1t": round(100 * x.QT_COMPARECIMENTO_1.sum() / x.QT_APTOS_1.sum(), 2),
                                 "comparecimento_2t": round(100 * x.QT_COMPARECIMENTO_2.sum() / x.QT_APTOS_2.sum(), 2),
                                 "eleitores": int(x.QT_APTOS_2.sum())} for k, x in g}

# ---------- C01/C03/C07 perfil demográfico (2026) ----------
if ANO == "2026" and os.path.exists(os.path.join(AQUI, "perfil.parquet")):
    p = pd.read_parquet(os.path.join(AQUI, "perfil.parquet"))
    x = b.merge(p, on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"], how="inner")
    vars_ = ["p_idoso", "p_jovem", "p_baixa_esc", "p_superior", "p_mulher"]
    rot = {"p_idoso": "60 anos ou mais", "p_jovem": "até 24 anos", "p_baixa_esc": "até fundamental incompleto",
           "p_superior": "superior (completo ou incompleto)", "p_mulher": "mulheres"}
    alvos = {"lula_1t": x.v13_1 / x.validos_1, "lula_2t": x.v13_2 / x.validos_2,
             "comparecimento_1t": x.QT_COMPARECIMENTO_1 / x.QT_APTOS_1, "comparecimento_2t": x.QT_COMPARECIMENTO_2 / x.QT_APTOS_2}
    alvos["virada"] = alvos["lula_2t"] - alvos["lula_1t"]
    alvos["mudanca_comparecimento"] = alvos["comparecimento_2t"] - alvos["comparecimento_1t"]
    D = x[vars_].copy()
    for k, v in alvos.items():
        D[k] = v.values
    D = D.dropna()
    g = x.loc[D.index, "mun"]
    Dd = D - D.groupby(g).transform("mean")  # dentro do município
    out = {}
    for k in alvos:
        Xm = Dd[vars_].values
        beta, *_ = np.linalg.lstsq(Xm, Dd[k].values, rcond=None)
        # efeito de passar de 0 a 100% do grupo, em pontos percentuais, controlando os outros e o município
        out[k] = {rot[v]: round(100 * bt, 2) for v, bt in zip(vars_, beta)}
    R["C03_C07_perfil"] = {"secoes": int(len(D)), "efeitos_pp_por_100pct": out,
                           "nota": "Coeficientes de regressão dentro do município (associação, não causa): diferença em pontos "
                                   "percentuais entre uma seção com 0% e outra com 100% daquele grupo, mantidos os demais."}
    # quintis de idosos e escolaridade (descritivo, fácil de ler)
    for v in ("p_idoso", "p_baixa_esc", "p_superior"):
        q = pd.qcut(x[v], 5, labels=["1º quinto (menos)", "2º", "3º", "4º", "5º quinto (mais)"], duplicates="drop")
        R[f"C03_quintis_{v}"] = {str(k): {"lula_1t": round(pct(z, 1), 2), "lula_2t": round(pct(z, 2), 2),
                                          "comparecimento_2t": round(100 * z.QT_COMPARECIMENTO_2.sum() / z.QT_APTOS_2.sum(), 2)}
                                 for k, z in x.groupby(q, observed=True)}

json.dump(R, open(os.path.join(AQUI, f"resultado_comportamento_{ANO}.json"), "w"), ensure_ascii=False, indent=1)
M = pd.DataFrame(R["C06"]["matriz"], index=R["C06"]["linhas"], columns=R["C06"]["colunas"])
print(f"== {ANO} C06 transferência (linhas: 1º turno; colunas: destino no 2º), %:")
print((100 * M).round(1).to_string())
print("conferência total previsto x observado:", R["C06"]["conferencia_total_previsto"], R["C06"]["conferencia_total_observado"])
print("C08 região:", {k: (v["lula_1t"], v["lula_2t"], v["virada_pp"]) for k, v in R["C08_regiao"].items()})
print("C08 porte:", {k: (v["lula_2t"], v["virada_pp"], v["comparecimento_2t"]) for k, v in R["C08_porte"].items()})
if "C03_C07_perfil" in R:
    for k, v in R["C03_C07_perfil"]["efeitos_pp_por_100pct"].items():
        print("perfil", k, v)
