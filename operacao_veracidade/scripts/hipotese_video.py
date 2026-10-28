"""T65: hipótese do vídeo (98,12% dos votos extras). Pré-registro em PROTOCOLO_PRE_EXECUCAO.md."""
import json
import numpy as np, pandas as pd
R = "."; OP = R + "/operacao_veracidade"
out = {}
def totais(ano, arq, finalistas):
    b = pd.read_parquet(f"{R}/analise/{arq}")
    a, c = finalistas
    d = {"L1": b.v13_1.sum(), "L2": b.v13_2.sum(), "D1": b[a + "_1"].sum(), "D2": b[a + "_2"].sum(), "val1": b.validos_1.sum(), "T1": b.QT_COMPARECIMENTO_1.sum(), "T2": b.QT_COMPARECIMENTO_2.sum(),
         "BN1": (b.branco_1 + b.nulo_1).sum(), "BN2": (b.branco_2 + b.nulo_2).sum(), "A1": b.QT_APTOS_1.sum(), "A2": b.QT_APTOS_2.sum()}
    d["E1"] = d["val1"] - d["L1"] - d["D1"]; d["X"] = (d["T2"] - d["T1"]) - (d["BN2"] - d["BN1"])
    d["dL"] = d["L2"] - d["L1"]; d["dD"] = d["D2"] - d["D1"]; d["dcomp"] = d["T2"] - d["T1"]; d["dBN"] = d["BN2"] - d["BN1"]
    d["abst1_pct"] = 100 * (1 - d["T1"] / d["A1"]); d["abst2_pct"] = 100 * (1 - d["T2"] / d["A2"])
    d["identidade"] = float(d["dL"] + d["dD"] - (d["E1"] + d["X"]))
    return {k: float(v) for k, v in d.items()}, b
t26, b26 = totais("2026", "base.parquet", ("v22", "Flavio")); t22, b22 = totais("2022", "base_2022.parquet", ("v22", "Bolsonaro"))
out["totais"] = {"2026": t26, "2022": t22}
# M1
e26 = (t26["dL"] - .6 * t26["E1"]) / t26["X"]
out["M1"] = {"outros_1t": t26["E1"], "extras": t26["X"], "dcomp": t26["dcomp"], "reducao_bn": -t26["dBN"], "ganho_lula": t26["dL"], "60pct_dos_outros": .6 * t26["E1"], "faltam": t26["dL"] - .6 * t26["E1"],
             "fracao_dos_extras_com_numeros_exatos": e26, "fracao_com_os_numeros_arredondados_do_video": (10.3 - 5.5) / 4.8, "ganho_flavio": t26["dD"], "flavio_igual_a_40pct_dos_outros": .4 * t26["E1"]}
# M2
s = np.arange(.5, 1.0001, .05)
out["M2"] = {"s_minimo_para_extras_no_maximo_100pct": (t26["dL"] - t26["X"]) / t26["E1"], "tabela": [{"parcela_dos_outros_para_Lula": round(float(x), 2), "fracao_dos_extras_para_Lula": float((t26["dL"] - x * t26["E1"]) / t26["X"]),
             "ganho_de_Flavio_conferido": float((1 - x) * t26["E1"] + (1 - (t26["dL"] - x * t26["E1"]) / t26["X"]) * t26["X"])} for x in s]}
# M3
e22 = (t22["dD"] - .6 * t22["E1"]) / t22["X"]
out["M3"] = {"ano": 2022, "candidato": "Bolsonaro", "ganho": t22["dD"], "outros": t22["E1"], "extras": t22["X"], "60pct_dos_outros": .6 * t22["E1"], "faltam": t22["dD"] - .6 * t22["E1"], "fracao_dos_extras_com_60pct": e22,
             "s_minimo_para_extras_no_maximo_100pct": (t22["dD"] - t22["X"]) / t22["E1"], "extras_de_2022_sao_so_o_saldo_de_comparecimento_e_brancos_e_nulos": {"dcomp": t22["dcomp"], "dBN": t22["dBN"]}}
# M4
out["M4"] = {"2022": {"abst_1t_pct": t22["abst1_pct"], "abst_2t_pct": t22["abst2_pct"], "queda_de_comparecimento_negativa_ou_positiva": t22["dcomp"]}, "2026": {"abst_1t_pct": t26["abst1_pct"], "abst_2t_pct": t26["abst2_pct"], "dcomp": t26["dcomp"]},
             "nota": "o projeto só tem 2022 e 2026; a alegação 'nunca aconteceu' não é testável além de 2022 com os dados do projeto"}
# M5: regressão ecológica por município
def reg(b, cand, nome, seed=65):
    b = b[b.SG_UF != "ZZ"].copy(); b["mun"] = b.SG_UF + "|" + b.CD_MUNICIPIO.astype(str)
    g = b.groupby(["SG_UF", "mun"]).agg(L1=("v13_1", "sum"), L2=("v13_2", "sum"), D1=(cand + "_1", "sum"), D2=(cand + "_2", "sum"), val1=("validos_1", "sum"), T1=("QT_COMPARECIMENTO_1", "sum"), T2=("QT_COMPARECIMENTO_2", "sum"),
                                         BN1=("branco_1", "sum"), nb1=("nulo_1", "sum"), BN2=("branco_2", "sum"), nb2=("nulo_2", "sum"), A=("QT_APTOS_1", "sum")).reset_index()
    g["BN1"] += g.nb1; g["BN2"] += g.nb2; g = g[g.A > 0]
    g["E1"] = (g.val1 - g.L1 - g.D1) / g.A; g["X"] = ((g.T2 - g.T1) - (g.BN2 - g.BN1)) / g.A; g["gL"] = (g.L2 - g.L1) / g.A; g["gD"] = (g.D2 - g.D1) / g.A
    def ajusta(d, y):
        U = pd.get_dummies(d.SG_UF).astype(float).values; Xm = np.column_stack([d.E1.values, d.X.values, U]); w = np.sqrt(d.A.values)
        coef, *_ = np.linalg.lstsq(Xm * w[:, None], d[y].values * w, rcond=None); return coef[:2]
    rng = np.random.default_rng(seed); est = {y: ajusta(g, y) for y in ("gL", "gD")}; bs = {y: [] for y in est}
    for _ in range(200):
        d = g.iloc[rng.integers(0, len(g), len(g))]
        for y in est: bs[y].append(ajusta(d, y))
    r = {"municipios": int(len(g))}
    for y, nm in (("gL", "Lula"), ("gD", nome)):
        e = est[y]; q = np.percentile(np.array(bs[y]), [2.5, 97.5], axis=0)
        r[nm] = {"coef_dos_eliminados": float(e[0]), "ic95_eliminados": [float(q[0][0]), float(q[1][0])], "coef_dos_extras": float(e[1]), "ic95_extras": [float(q[0][1]), float(q[1][1])]}
    r["soma_dos_coeficientes_extras_(deve_ser_perto_de_1_pela_identidade)"] = r["Lula"]["coef_dos_extras"] + r[nome]["coef_dos_extras"]
    return r
out["M5"] = {"2026": reg(b26, "v22", "Flavio"), "2022": reg(b22, "v22", "Bolsonaro")}
json.dump(out, open(f"{OP}/resultados/hipotese_video.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "totais"}, ensure_ascii=False, indent=1))
