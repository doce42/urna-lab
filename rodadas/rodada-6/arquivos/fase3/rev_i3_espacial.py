"""F3 em revisão / I3: significância dos locais de votação do E02 contra o entorno (zona ou município), com nulo empírico
por faixa de tamanho; robustez dos locais de São Paulo capital (2022) e dependência da seleção. Ver fase3/PREREG_REVISAO.md."""
import json, time
import numpy as np, pandas as pd
from scipy import stats

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; OUT = RAIZ + "/fase3/resultados"
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
T0 = time.time()
FAIXAS = [(3, 5), (6, 9), (10, 14), (15, 10 ** 6)]


def bh(p, q=0.05):
    n = len(p); o = np.argsort(p); passa = p[o] <= q * np.arange(1, n + 1) / n
    k = np.max(np.where(passa)[0]) + 1 if passa.any() else 0
    s = np.zeros(n, bool); s[o[:k]] = True; return s


def prepara(ano):
    """mesmo universo e mesmo modelo 'completo' do P9 (fase2/f2_completa.py), mais o z do T02 (mediana municipal) usado no P20"""
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
    b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20) & (b.SG_UF != "ZZ")].copy().reset_index(drop=True)
    b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"].astype(str); b["zona"] = b["mun"] + "-" + b["NR_ZONA"].astype(str)
    b["local"] = b["zona"] + "-" + b["NR_LOCAL_VOTACAO_2"].astype(str)
    b["k_sec"] = b["SG_UF"] + "/" + b["CD_MUNICIPIO"].astype(str) + "/" + b["NR_ZONA"].astype(str) + "/" + b["NR_SECAO"].astype(str)
    x1, n1, x2, n2 = b["v13_1"], b["validos_1"], b["v13_2"], b["validos_2"]
    b["sw"] = lg(x2, n2) - lg(x1, n1); sd = np.sqrt(1/(x1+.5) + 1/(n1-x1+.5) + 1/(x2+.5) + 1/(n2-x2+.5))
    z = (b["sw"] - b.groupby("mun")["sw"].transform("median")) / sd; b["z_t02"] = z / (1.4826 * (z - z.median()).abs().median())
    b["p1"] = x1 / n1; b["orf"] = 1 - (b["v13_1"] + b["v22_1"]) / n1
    elim = [c for c in b.columns if c.startswith("v") and c.endswith("_1") and c not in ("v13_1", "v22_1", "validos_1")]
    cols = [np.ones(len(b)), b.p1, b.p1 ** 2, b.orf] + [b[c].fillna(0) / n1 for c in elim] + [(b["branco_1"] + b["nulo_1"]) / b["total_1"],
            b["QT_COMPARECIMENTO_2"] / b["QT_APTOS_2"] - b["QT_COMPARECIMENTO_1"] / b["QT_APTOS_1"], np.log(b.groupby("mun")["QT_APTOS_2"].transform("sum"))]
    X = np.nan_to_num(np.column_stack([np.asarray(c, float) for c in cols])); esp = np.zeros(len(b))
    for uf, ix in b.groupby("SG_UF").indices.items():
        beta, *_ = np.linalg.lstsq(X[ix], b["sw"].values[ix], rcond=None); esp[ix] = X[ix] @ beta
    zz = (b["sw"].values - esp) / sd; b["zz"] = (zz - np.median(zz)) / (1.4826 * np.median(np.abs(zz - np.median(zz))))
    return b


def locais(b, ref, excluir=None):
    """d = média do zz do local − média do zz das demais seções da referência (zona ou município); fallback zona → município.
    excluir: máscara de seções retiradas do local (não da referência), para o teste de dependência da seleção."""
    use = np.ones(len(b), bool) if excluir is None else ~excluir
    g = b.groupby("local")["zz"].agg(["size", "sum"]); g.columns = ["k_total", "s_total"]
    gu = b[use].groupby("local")["zz"].agg(["size", "mean"]); g = g.join(gu, how="inner")
    lz = b.groupby("local")[["zona", "mun"]].first(); g = g.join(lz)
    out = {}
    for nivel in (["zona", "mun"] if ref == "zona" else ["mun"]):
        s = b.groupby(nivel)["zz"].agg(["size", "sum"]); s.columns = [f"n_{nivel}", f"s_{nivel}"]; g = g.join(s, on=nivel)
        g[f"o_{nivel}"] = g[f"n_{nivel}"] - g["k_total"]; g[f"m_{nivel}"] = (g[f"s_{nivel}"] - g["s_total"]) / g[f"o_{nivel}"].replace(0, np.nan)
    if ref == "zona": g["ref"] = g["m_zona"].where(g["o_zona"] >= 3, g["m_mun"].where(g["o_mun"] >= 3))
    else: g["ref"] = g["m_mun"].where(g["o_mun"] >= 3)
    g["d"] = g["mean"] - g["ref"]
    return g


def nulo_empirico(g, escala=None):
    """escala robusta de d por faixa de tamanho (tamanho = seções usadas no local); escala pode vir de outra tabela"""
    g = g[g["size"] >= 3].copy(); g["faixa"] = -1
    for i, (a, c) in enumerate(FAIXAS): g.loc[(g["size"] >= a) & (g["size"] <= c), "faixa"] = i
    if escala is None:
        h = g.dropna(subset=["d"]); escala = {i: (float(h[h.faixa == i]["d"].median()), float(1.4826 * (h[h.faixa == i]["d"] - h[h.faixa == i]["d"].median()).abs().median())) for i in range(len(FAIXAS))}
    g["z_esp"] = [(d - escala[f][0]) / escala[f][1] if not np.isnan(d) else np.nan for d, f in zip(g["d"], g["faixa"])]
    return g, escala


R = {"pre_registro": "fase3/PREREG_REVISAO.md (I3)"}
bases = {ano: prepara(ano) for ano in ("2026", "2022")}
print("bases", round(time.time() - T0), "s", flush=True)
for ref in ("zona", "mun"):                     # mun = sensibilidade
    Rr = {}
    for ano, b in bases.items():
        g, esc = nulo_empirico(locais(b, ref))
        h = g.dropna(subset=["z_esp"]); p = 2 * stats.norm.sf(np.abs(h["z_esp"].values)); s = bh(p)
        # mesmo universo, correção por ρ do P9 (sem referência espacial), para comparar
        zl = b[b.local.isin(g.index)]; k = g["k_total"].values.astype(float); gm = zl.groupby("local")["zz"]
        grand = zl["zz"].mean(); mean_all = g["s_total"] / g["k_total"]
        ssb = (k * (mean_all.values - grand) ** 2).sum(); sst = ((zl["zz"] - gm.transform("mean")) ** 2).sum(); ng = len(g); Nn = k.sum()
        msb = ssb / (ng - 1); msw = sst / (Nn - ng); k0 = (Nn - (k ** 2).sum() / Nn) / (ng - 1); rho = max(0, (msb - msw) / (msb + (k0 - 1) * msw))
        zadj = mean_all.values * np.sqrt(k) / np.sqrt(1 + (k - 1) * rho); s_rho = bh(2 * stats.norm.sf(np.abs(zadj)))
        Rr[ano] = {"locais": int(len(g)), "sem_referencia": int(g["z_esp"].isna().sum()), "escala_por_faixa": {f"{a}-{c}": esc[i] for i, (a, c) in enumerate(FAIXAS)},
                   "significativos_nulo_espacial": int(s.sum()), "pro_lula": int((s & (h["z_esp"].values > 0)).sum()), "pro_adversario": int((s & (h["z_esp"].values < 0)).sum()),
                   "comparacao_rho_P9_mesmo_universo": {"rho": float(rho), "significativos": int(s_rho.sum()), "pro_lula": int((s_rho & (zadj > 0)).sum()), "pro_adversario": int((s_rho & (zadj < 0)).sum())},
                   "sobreposicao_rho_e_espacial": int(len(set(h.index[s]) & set(g.index[s_rho])))}
        if ano == "2022":
            sp = b[b.mun == "SP71072"]; sel = (b.mun == "SP71072") & (b.z_t02 > 5); loc_at = b[sel]["local"].value_counts()
            sig_set = set(h.index[s])
            gx, _ = nulo_empirico(locais(b, ref, excluir=sel.values), esc)
            b26 = bases["2026"]; g26, _ = nulo_empirico(locais(b26, ref))
            mapa26 = b26.set_index("k_sec")["local"]
            lst = []
            for l, nsel in loc_at.items():
                secs = b[b.local == l]["k_sec"]; l26 = mapa26.reindex(secs).dropna()
                l26m = l26.mode().iloc[0] if len(l26) else None
                lst.append({"local": l, "secoes": int(g.loc[l, "k_total"]) if l in g.index else int((b.local == l).sum()), "selecionadas": int(nsel),
                            "z_esp": float(g.loc[l, "z_esp"]) if l in g.index else None, "BH_significativo": l in sig_set,
                            "z_esp_sem_selecionadas": float(gx.loc[l, "z_esp"]) if l in gx.index and not np.isnan(gx.loc[l, "z_esp"]) else None,
                            "secoes_restantes": int(gx.loc[l, "size"]) if l in gx.index else 0,
                            "local_2026": l26m, "z_esp_2026": float(g26.loc[l26m, "z_esp"]) if l26m in g26.index and not np.isnan(g26.loc[l26m, "z_esp"]) else None})
            for x in lst:
                x["resiste_ao_nulo_espacial"] = bool(x["BH_significativo"] and (x["z_esp_sem_selecionadas"] or 0) > 3)
                x["persiste_2026"] = None if x["z_esp_2026"] is None else bool(x["z_esp_2026"] > 2)
            Rr["sp_capital_2022"] = {"secoes_selecionadas": int(sel.sum()), "locais": len(lst), "por_local": lst,
                                     "resistem": sum(x["resiste_ao_nulo_espacial"] for x in lst), "persistem_2026": sum(bool(x["persiste_2026"]) for x in lst),
                                     "sem_correspondencia_2026": sum(x["z_esp_2026"] is None for x in lst)}
        print(ref, ano, {k: v for k, v in Rr[ano].items() if k != "escala_por_faixa"}, round(time.time() - T0), "s", flush=True)
    if "sp_capital_2022" in Rr: print(ref, "SP", {k: v for k, v in Rr["sp_capital_2022"].items() if k != "por_local"}, flush=True)
    R["principal_referencia_zona" if ref == "zona" else "sensibilidade_referencia_municipio"] = Rr
R["tempo_s"] = round(time.time() - T0, 1)
json.dump(R, open(f"{OUT}/rev_i3.json", "w"), indent=1, ensure_ascii=False, default=str)
