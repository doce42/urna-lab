"""T58 e T59: análise dos números digitados nos nulos (pré-registro em fase3/PREREG_RDV_NULOS.md).
Lê fase3/resultados/rdv_nulos_<ano>_<turno>t.parquet (extração de fase3/rdv_nulos.py)."""
import glob, json, re
import numpy as np, pandas as pd
from scipy.optimize import minimize

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; RES = RAIZ + "/fase3/resultados"
CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
GOV2 = {"2022": {"AL", "AM", "BA", "ES", "MS", "PB", "PE", "RO", "RS", "SC", "SE", "SP"}, "2026": {"AC", "AM", "DF", "ES", "RN", "TO"}}
R = {"pre_registro": "fase3/PREREG_RDV_NULOS.md"}


def base(ano):
    return pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet").astype({c: str for c in CH})


def nulos(ano, t):
    d = pd.read_parquet(f"{RES}/rdv_nulos_{ano}_{t}t.parquet").astype({c: str for c in CH})
    gov = json.load(open(f"{RES}/rdv_nulos_{ano}_{t}t_gov.json"))["governador_nominal_por_uf"]
    return d, {u: set(g) for u, g in gov.items()}


def classe(dig, uf, govs, elim):
    if dig == "":
        return "sem_numero"
    if re.fullmatch(r"0+", dig):
        return "zeros"
    if dig in govs.get(uf, ()):
        return "governador"
    if dig in elim:
        return "presidente_eliminado"
    return "outros"


# ---------------- T58 ----------------
t58 = {}
P = {}
for ano in ("2022", "2026"):
    b = base(ano)
    elim = {c[1:-2] for c in b.columns if re.fullmatch(r"v\d+_1", c)} - {"13", "22"}
    for t in (1, 2):
        d, govs = nulos(ano, t)
        p = d[(d.cargo == 1) & (d.tipo != 3)].copy()            # nulos de presidente (tipo 4 com número, 6 sem número)
        p["classe"] = [classe(x, u, govs, elim if t == 2 else set()) for x, u in zip(p.digitos, p.SG_UF)]
        P[(ano, t)] = p
        # conferência com o leitor original (rdv_nulo por seção; em 2026 o tipo 6 fica à parte no leitor original)
        u = pd.concat([pd.read_parquet(f, columns=CH + ["rdv_nulo", "rdv_branco"]) for f in
                       glob.glob(f"{AN}/brutos/{(str(t) + 't') if ano == '2026' else f'2022_{t}t'}/urnas_*.parquet")]).astype({c: str for c in CH})
        # correção 1: em 2022 o leitor original soma o tipo 6 ao nulo; seções só com tipo 6 ficavam fora da conferência
        mine = (p if ano == "2022" else p[p.tipo == 4]).groupby(CH).n.sum()
        br = d[(d.cargo == 1) & (d.tipo == 3)].groupby(CH).n.sum()
        cmp = u.set_index(CH)[["rdv_nulo", "rdv_branco"]].fillna(0).join(mine.rename("nulo_novo")).join(br.rename("branco_novo")).fillna(0)
        tot = b[f"total_{t}"].sum()
        cls = p.groupby("classe").n.sum()
        top = p[p.tipo == 4].groupby("digitos").n.sum().nlargest(15)
        g = p.assign(gov=p.SG_UF.isin(GOV2[ano]) if t == 2 else False).groupby(["gov", "classe"]).n.sum().unstack(fill_value=0)
        totg = b.assign(gov=b.SG_UF.isin(GOV2[ano]) if t == 2 else False).groupby("gov")[f"total_{t}"].sum()
        t58[f"{ano}_{t}t"] = {"conferencia_secoes_nulo_diferente": int((cmp.rdv_nulo != cmp.nulo_novo).sum()),
                              "conferencia_secoes_branco_diferente": int((cmp.rdv_branco != cmp.branco_novo).sum()),
                              "nulos_presidente": int(p.n.sum()), "por_classe": cls.astype(int).to_dict(),
                              "por_classe_pct_dos_nulos": (100 * cls / cls.sum()).round(2).to_dict(),
                              "top15_numeros": top.astype(int).to_dict(),
                              "por_grupo_uf_pp_do_total": {("com_governador_2t" if k else "sem_governador_2t"): (100 * g.loc[k] / totg[k]).round(3).to_dict() for k in g.index}}
R["T58"] = t58

# T56: o excesso de nulos do 1º turno de 2026 onde Lula é forte, por classe (seções pareadas com 2022)
b26, b22 = base("2026"), base("2022")
def por_secao(p):
    return p.groupby(CH + ["classe"]).n.sum().unstack(fill_value=0)
s26, s22 = por_secao(P[("2026", 1)]), por_secao(P[("2022", 1)])
m = b26[CH + ["total_1"]].merge(b22[CH + ["total_1", "v13_2", "validos_2"]], on=CH, suffixes=("", "_22"))
m = m[(m.SG_UF != "ZZ") & (m.total_1 >= 50) & (m.total_1_22 >= 50)].set_index(CH)
cls = sorted(set(s26.columns) | set(s22.columns))
a = s26.reindex(m.index, fill_value=0).reindex(columns=cls, fill_value=0).div(m.total_1, axis=0)
c = s22.reindex(m.index, fill_value=0).reindex(columns=cls, fill_value=0).div(m.total_1_22, axis=0)
q = pd.qcut(m.v13_2 / m.validos_2, 5, labels=["Q1 (menos Lula)", "Q2", "Q3", "Q4", "Q5 (mais Lula)"])
R["T58_excesso_1t_2026_por_classe_pp"] = (100 * (a - c).groupby(q.values, observed=True).mean()).round(3).to_dict("index")

# 2º turno: o efeito do governador (T57) vem da classe "governador"?
R["T58_resumo_2t_governador"] = {ano: R["T58"][f"{ano}_2t"]["por_grupo_uf_pp_do_total"] for ano in ("2022", "2026")}


# ---------------- T59 ----------------
def restrito(Xm, Ym, wm):
    k, mm = Xm.shape[1], Ym.shape[1]
    wm = wm / wm.sum(); XtX = (Xm * wm[:, None]).T @ Xm; XtY = (Xm * wm[:, None]).T @ Ym
    f = lambda v: float(np.sum(v.reshape(k, mm) * (XtX @ v.reshape(k, mm))) - 2 * np.sum(v.reshape(k, mm) * XtY))
    gr = lambda v: (2 * (XtX @ v.reshape(k, mm)) - 2 * XtY).ravel()
    cons = [{"type": "eq", "fun": (lambda v, i=i: v.reshape(k, mm)[i].sum() - 1)} for i in range(k)]
    res = minimize(f, np.full(k * mm, 1.0 / mm), jac=gr, bounds=[(0, 1)] * (k * mm), constraints=cons, method="SLSQP", options={"maxiter": 2000, "ftol": 1e-12})
    return res.x.reshape(k, mm), bool(res.success)


t59 = {}
ALVOS = {"2026": ["14", "70", "55"], "2022": ["12", "15"]}
for ano in ("2026", "2022"):
    b = base(ano); b = b[(b.SG_UF != "ZZ") & (b.QT_APTOS_1 >= 50) & (b.QT_APTOS_2 >= 50) & b.total_1.notna() & b.total_2.notna()].copy()
    p2 = P[(ano, 2)]; p2 = p2[p2.tipo == 4]
    alvo_cols = []
    for k in ALVOS[ano]:
        s = p2[p2.digitos == k].groupby(CH).n.sum().rename(f"nulo{k}_2")
        b = b.merge(s, left_on=CH, right_index=True, how="left"); b[f"nulo{k}_2"] = b[f"nulo{k}_2"].fillna(0); alvo_cols.append(f"nulo{k}_2")
    a1, a2 = b.QT_APTOS_1, b.QT_APTOS_2
    X = pd.DataFrame({"Lula": b.v13_1 / a1, "Adversario": b.v22_1 / a1})
    for k in ALVOS[ano]:
        X[k] = b[f"v{k}_1"].fillna(0) / a1
    outros = [c for c in b.columns if re.fullmatch(r"v\d+_1", c) and c[1:-2] not in {"13", "22", *ALVOS[ano]}]
    X["Outros"] = b[outros].fillna(0).sum(axis=1) / a1
    X["BrancoNulo"] = (b.branco_1 + b.nulo_1) / a1
    X["Abstencao"] = 1 - b.QT_COMPARECIMENTO_1 / a1
    Y = pd.DataFrame({"Lula": b.v13_2 / a2, "Adversario": b.v22_2 / a2})
    for k in ALVOS[ano]:
        Y[f"nulo{k}"] = b[f"nulo{k}_2"] / a2
    Y["OutrosBN"] = (b.branco_2 + b.nulo_2 - b[alvo_cols].sum(axis=1)) / a2
    Y["Abstencao"] = 1 - b.QT_COMPARECIMENTO_2 / a2
    ok = X.notna().all(axis=1) & Y.notna().all(axis=1)
    X, Y, w, uf = X[ok].values, Y[ok].values, a1[ok].values.astype(float), b.SG_UF[ok].values
    cols_x, cols_y = list(pd.DataFrame(columns=["Lula", "Adversario", *ALVOS[ano], "Outros", "BrancoNulo", "Abstencao"]).columns), None
    acerto_uf, Ms, Pw, conv = {}, [], [], 0
    for u in np.unique(uf):
        s = uf == u
        if s.sum() < 200:
            continue
        Bu, okc = restrito(X[s], Y[s], w[s]); conv += okc
        pw = (X[s] * w[s][:, None]).sum(axis=0)
        Ms.append(Bu); Pw.append(pw)
        fl = pw[:, None] * Bu                                  # eleitores do grupo i que vão ao destino j, no estado
        acerto_uf[u] = {k: float(fl[2 + i, 2 + i] / fl[:, 2 + i].sum()) if fl[:, 2 + i].sum() > 0 else None for i, k in enumerate(ALVOS[ano])}
    fl = sum(pw[:, None] * Bu for pw, Bu in zip(Pw, Ms))
    obs = {k: int(b.loc[ok, f"nulo{k}_2"].sum()) for k in ALVOS[ano]}
    nac = {k: float(fl[2 + i, 2 + i] / fl[:, 2 + i].sum()) for i, k in enumerate(ALVOS[ano])}
    maioria = {k: sum(1 for v in acerto_uf.values() if v[k] is not None and v[k] >= .5) for k in ALVOS[ano]}
    origem_principal = {k: ["Lula", "Adversario", *ALVOS[ano], "Outros", "BrancoNulo", "Abstencao"][int(np.argmax(fl[:, 2 + i]))] for i, k in enumerate(ALVOS[ano])}
    t59[ano] = {"destinos_observados_votos": obs, "fracao_atribuida_a_origem_certa_nacional": nac, "ufs_com_50pct_ou_mais": maioria, "ufs": len(acerto_uf),
                "origem_mais_atribuida": origem_principal, "convergiu": f"{conv}/{len(acerto_uf)}",
                "veredito": {k: ("passa" if nac[k] >= .5 and maioria[k] > len(acerto_uf) / 2 else "falha" if nac[k] < .25 else "parcial") for k in ALVOS[ano]},
                "por_uf": acerto_uf}
R["T59"] = t59
json.dump(R, open(f"{RES}/rdv_nulos_analise.json", "w"), ensure_ascii=False, indent=1, default=str)
for k in ("T58", "T58_excesso_1t_2026_por_classe_pp", "T58_resumo_2t_governador"):
    print(k, json.dumps(R[k], ensure_ascii=False, default=str)[:3000])
for ano, v in t59.items():
    print("T59", ano, json.dumps({x: y for x, y in v.items() if x != "por_uf"}, ensure_ascii=False))
