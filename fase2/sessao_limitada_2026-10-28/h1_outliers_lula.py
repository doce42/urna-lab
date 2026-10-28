"""Adendo 1: hipótese 'enchimento/transferência localizada para Lula'. Dados já preparados; T02 (def. de bateria.py/poder.py) + assinatura de comparecimento."""
import json, os, numpy as np, pandas as pd
AN = "analise"; AQ = os.path.dirname(os.path.abspath(__file__))
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
out = {}
for ano in ("2026", "2022"):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
    b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20) & (b["SG_UF"] != "ZZ")].reset_index(drop=True)
    b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
    L1, V1, L2, V2 = (b[c].values.astype(float) for c in ("v13_1", "validos_1", "v13_2", "validos_2"))
    sw = lg(L2, V2) - lg(L1, V1)
    res = sw - pd.Series(sw).groupby(b["mun"].values).transform("median").values
    sd = np.sqrt(1/(L1+.5) + 1/(V1-L1+.5) + 1/(L2+.5) + 1/(V2-L2+.5))
    z = res / sd; zr = z / (1.4826 * np.median(np.abs(z - np.median(z))))
    dc = (b["QT_COMPARECIMENTO_2"] / b["QT_APTOS_2"] - b["QT_COMPARECIMENTO_1"] / b["QT_APTOS_1"]).values
    dcr = dc - pd.Series(dc).groupby(b["mun"].values).transform("median").values
    r = {"n": int(len(b))}
    r["cauda"] = {str(t): {"pro_lula": int((zr > t).sum()), "pro_outro": int((zr < -t).sum())} for t in (2, 3, 4, 5, 6, 8)}
    r["assimetria_corpo"] = {"mediana_zr": float(np.median(zr)), "q01": float(np.quantile(zr, .01)), "q99": float(np.quantile(zr, .99)),
                             "razao_q99_q01": float(np.quantile(zr, .99) / abs(np.quantile(zr, .01)))}
    for nome, m in (("pro_lula", zr > 5), ("pro_outro", zr < -5), ("todas", np.ones(len(b), bool))):
        r[nome] = {"n": int(m.sum()), "validos_2_mediana": float(np.median(V2[m])), "dcomp_res_media_pp": float(100 * dcr[m].mean()),
                   "dcomp_res_mediana_pp": float(100 * np.median(dcr[m])), "votos_extra_lula_aprox": float(((res[m] > 0) * 0).sum())}
    # votos líquidos "extra" nas pro-Lula: L2 - esperado pela virada do município
    p_exp = 1 / (1 + np.exp(-(lg(L1, V1) + pd.Series(sw).groupby(b["mun"].values).transform("median").values)))
    ex = L2 - p_exp * V2
    m = zr > 5; mo = zr < -5
    r["pro_lula"]["votos_excedentes_total"] = float(ex[m].sum()); r["pro_outro"]["votos_excedentes_total_lula"] = float(ex[mo].sum())
    r["saldo_lula_total_2t_menos_1t"] = float(L2.sum() - L1.sum())
    r["pro_lula"]["uf_top"] = b.loc[m, "SG_UF"].value_counts().head(6).to_dict()
    r["pro_outro"]["uf_top"] = b.loc[mo, "SG_UF"].value_counts().head(6).to_dict()
    # sentido inverso: corpo (|zr|>3) excluindo tamanho pequeno
    grande = V2 >= np.median(V2)
    r["cauda5_so_secoes_acima_da_mediana_de_tamanho"] = {"pro_lula": int(((zr > 5) & grande).sum()), "pro_outro": int(((zr < -5) & grande).sum())}
    # fração da cauda com dcomp_res > 0 (previsão do enchimento: comparecimento sobe junto)
    r["pro_lula"]["frac_dcomp_res_positivo"] = float((dcr[m] > 0).mean()); r["pro_outro"]["frac_dcomp_res_positivo"] = float((dcr[mo] > 0).mean())
    r["todas"]["frac_dcomp_res_positivo"] = float((dcr > 0).mean())
    out[ano] = r
json.dump(out, open(AQ + "/h1_resultado.json", "w"), indent=1)
print(json.dumps(out, indent=1))
