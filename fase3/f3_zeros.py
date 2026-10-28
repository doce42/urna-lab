"""F3 / E3: seções com zero votos para um finalista, 2022 e 2026, por turno. Ver PREREG.md."""
import glob, json, time
import numpy as np, pandas as pd
from scipy import stats

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; OUT = RAIZ + "/fase3/resultados"; T0 = time.time()
K = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]


def brutos(ano, t):
    pas = f"{t}t" if ano == "2026" else f"{ano}_{t}t"
    fs = glob.glob(f"{AN}/brutos/{pas}/urnas_*.parquet")
    cols = K + ["bu_v13", "bu_v22", "rdv_v13", "rdv_v22", "img_v13", "img_v22", "bu_comparecimento", "origem"]
    out = []
    for f in fs:
        d = pd.read_parquet(f); out.append(d[[c for c in cols if c in d.columns]])
    return pd.concat(out, ignore_index=True).astype({k: str for k in K})


def rho_global(v, n, p_i, grupo):
    """sobredispersão (ρ) por momentos: Var(v/n) = p(1−p)/n·(1+(n−1)ρ), pooled em seções com n ≥ 100 de municípios com ≥ 10 seções"""
    ok = (n >= 100) & (grupo >= 10) & (p_i > 0.02) & (p_i < 0.98)
    r = (v[ok] / n[ok] - p_i[ok]) ** 2; esp = p_i[ok] * (1 - p_i[ok]) / n[ok]
    num = (r - esp).sum(); den = (esp * (n[ok] - 1)).sum()
    return float(max(num / den, 1e-6))


def analisa(b, cand, t, nivel="mun"):
    v = b[f"{cand}_{t}"].values.astype(float); n = b[f"validos_{t}"].values.astype(float); comp = b[f"QT_COMPARECIMENTO_{t}"].values.astype(float)
    g = (b["SG_UF"] + b["CD_MUNICIPIO"]).values if nivel == "mun" else b["SG_UF"].values
    if nivel == "local":
        g = (b["SG_UF"] + b["CD_MUNICIPIO"] + "-" + b["NR_ZONA"].astype(str) + "-" + b[f"NR_LOCAL_VOTACAO_{t}"].astype(str)).values
    if nivel == "proprio1t":      # correção única: a própria seção no 1º turno como previsor do 2º
        g = (b["SG_UF"] + b["CD_MUNICIPIO"]).values
    gs = pd.Series(g)
    Vg = pd.Series(v).groupby(g).transform("sum").values; Ng = pd.Series(n).groupby(g).transform("sum").values; cnt = gs.groupby(g).transform("size").values
    p_loo = np.where(Ng - n > 0, (Vg - v) / np.maximum(Ng - n, 1), np.nan)
    ufp = pd.Series(v).groupby(b["SG_UF"].values).transform("sum").values / pd.Series(n).groupby(b["SG_UF"].values).transform("sum").values
    p_loo = np.where(np.isnan(p_loo), ufp, p_loo).clip(1e-4, 1 - 1e-4)
    if nivel == "proprio1t" and t == 2:
        p_loo = ((b[f"{cand}_1"].values + 1) / (b["validos_1"].values + 2)).clip(1e-4, 1 - 1e-4)
    rho = rho_global(v, n, p_loo, np.full(len(v), 99) if nivel in ("local", "proprio1t") else cnt)
    a = p_loo * (1 - rho) / rho; bb = (1 - p_loo) * (1 - rho) / rho
    ok = (n > 0)
    P0_bb = np.where(ok, stats.betabinom.pmf(0, n.astype(int), a, bb), 0.0); P0_bi = np.where(ok, (1 - p_loo) ** n, 0.0)
    zero = ok & (v == 0)
    faixas = pd.qcut(n[ok], [0, .1, .25, .5, .75, .9, .99, 1], duplicates="drop")
    tab = []
    for f in faixas.categories:
        s = (faixas == f); idx = np.nonzero(ok)[0][s]
        tab.append({"faixa_validos": str(f), "secoes": int(len(idx)), "zeros_observados": int(zero[idx].sum()), "zeros_esperados_beta_binomial": float(P0_bb[idx].sum()), "zeros_esperados_binomial": float(P0_bi[idx].sum())})
    return zero, {"rho_sobredispersao": rho, "zeros_observados": int(zero.sum()), "esperado_beta_binomial": float(P0_bb[ok].sum()), "esperado_binomial_homogeneo": float(P0_bi[ok].sum()), "por_faixa": tab}, P0_bb


R = {"pergunta": "E3 zeros", "anos": {}}
for ano, nomes in (("2026", {"v22": "Flávio Bolsonaro", "v13": "Lula (controle)"}), ("2022", {"v22": "Bolsonaro", "v13": "Lula"})):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
    b = b[b["SG_UF"] != "ZZ"].copy(); b = b[(b["validos_1"].fillna(0) > 0) & (b["validos_2"].fillna(0) > 0)].reset_index(drop=True)
    b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
    RA = {"secoes_com_votos_validos_nos_2_turnos": int(len(b))}
    zeros = {}
    for cand, nome in nomes.items():
        RC = {}
        for t in (1, 2):
            z, res, p0 = analisa(b, cand, t); zeros[(cand, t)] = z
            _, res_uf, _ = analisa(b, cand, t, "uf")
            _, res_loc, _ = analisa(b, cand, t, "local")
            _, res_p1, _ = analisa(b, cand, t, "proprio1t") if t == 2 else (None, None, None)
            zz = b[z]
            res.update({"validos_mediana_nas_zero": float(zz[f"validos_{t}"].median()) if len(zz) else None, "validos_mediana_geral": float(b[f"validos_{t}"].median()),
                        "comparecimento_positivo_nas_zero": int((zz[f"QT_COMPARECIMENTO_{t}"] > 0).sum()), "votos_do_outro_finalista_nessas_secoes": int(zz["v13_%d" % t if cand == "v22" else "v22_%d" % t].sum()),
                        "ufs_top": zz["SG_UF"].value_counts().head(6).to_dict(), "municipios_distintos": int(zz["mun"].nunique()),
                        "sensibilidade_prior_por_UF": {"esperado_beta_binomial": res_uf["esperado_beta_binomial"], "rho": res_uf["rho_sobredispersao"]},
                        "correcao_prior_por_local_de_votacao": {"esperado_beta_binomial": res_loc["esperado_beta_binomial"], "rho": res_loc["rho_sobredispersao"]},
                        "correcao_previsor_proprio_1t": ({"esperado_beta_binomial": res_p1["esperado_beta_binomial"], "rho": res_p1["rho_sobredispersao"]} if res_p1 else None)})
            RC[f"{t}t"] = res
        z1, z2 = zeros[(cand, 1)], zeros[(cand, 2)]
        RC["transicao_entre_turnos"] = {"0_para_positivo": int((z1 & ~z2).sum()), "positivo_para_0": int((~z1 & z2).sum()), "0_nos_dois": int((z1 & z2).sum())}
        RA[nome] = RC
    # divergências nos arquivos das urnas para as seções com zero do finalista "v22"
    for t in (1, 2):
        bu = brutos(ano, t); z = b[zeros[("v22", t)]][K + [f"v22_{t}", f"v13_{t}"]].astype(dict.fromkeys(K, str))
        m = z.merge(bu, on=K, how="left", indicator=True)
        col = lambda c: m[c].fillna(0) if c in m else pd.Series(0, index=m.index)
        RA[f"arquivos_das_urnas_nas_zeros_{t}t"] = {"secoes": int(len(m)), "sem_linha_de_urna": int((m._merge == "left_only").sum()),
            "bu_v22_diferente_de_0": int((col("bu_v22") != 0).sum()), "rdv_v22_diferente_de_0": int(((col("rdv_v22") > 0)).sum()), "imagem_v22_diferente_de_0": int(((col("img_v22") > 0)).sum()),
            "bu_v13_diferente_da_tabela_publicada": int(((col("bu_v13") != m[f"v13_{t}"]) & (m._merge == "both")).sum()), "origem_nao_urna": m["origem"].value_counts(dropna=False).to_dict() if "origem" in m else None}
    R["anos"][ano] = RA
    print(ano, "ok", round(time.time() - T0), "s", flush=True)
R["tempo_s"] = round(time.time() - T0, 1)
json.dump(R, open(f"{OUT}/E3_zeros.json", "w"), indent=1, ensure_ascii=False, default=float)
