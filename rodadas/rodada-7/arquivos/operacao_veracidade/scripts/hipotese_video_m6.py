"""T65 M6 (exploratório): ganho observado × ganho previsto se eliminados e extras se dividissem entre os finalistas na proporção do 1º turno, por município."""
import json
import numpy as np, pandas as pd
R = "."; OP = R + "/operacao_veracidade"; out = {}
for ano, arq in (("2026", "base.parquet"), ("2022", "base_2022.parquet")):
    b = pd.read_parquet(f"{R}/analise/{arq}"); b = b[b.SG_UF != "ZZ"].copy(); b["mun"] = b.SG_UF + "|" + b.CD_MUNICIPIO.astype(str)
    g = b.groupby(["SG_UF", "mun"]).agg(L1=("v13_1", "sum"), L2=("v13_2", "sum"), D1=("v22_1", "sum"), D2=("v22_2", "sum"), val1=("validos_1", "sum"), T1=("QT_COMPARECIMENTO_1", "sum"), T2=("QT_COMPARECIMENTO_2", "sum"),
                                         b1=("branco_1", "sum"), n1=("nulo_1", "sum"), b2=("branco_2", "sum"), n2=("nulo_2", "sum")).reset_index()
    g["E1"] = g.val1 - g.L1 - g.D1; g["X"] = (g.T2 - g.T1) - ((g.b2 + g.n2) - (g.b1 + g.n1)); g["p"] = g.L1 / (g.L1 + g.D1).replace(0, np.nan)
    g = g.dropna(subset=["p"]); disp = g.E1 + g.X
    g["pred_L"] = disp * g.p; g["pred_D"] = disp * (1 - g.p); g["gL"] = g.L2 - g.L1; g["gD"] = g.D2 - g.D1
    r = {"ganho_L_observado": float(g.gL.sum()), "ganho_L_previsto_proporcional": float(g.pred_L.sum()), "residual_L": float((g.gL - g.pred_L).sum()),
         "ganho_direita_observado": float(g.gD.sum()), "ganho_direita_previsto": float(g.pred_D.sum()), "residual_direita": float((g.gD - g.pred_D).sum()),
         "extras_para_Lula_se_proporcional_pct": float(100 * (g.X * g.p).sum() / g.X.sum()), "eliminados_para_Lula_se_proporcional_pct": float(100 * (g.E1 * g.p).sum() / g.E1.sum()),
         "disponivel_total": float(disp.sum()), "residual_L_pct_do_disponivel": float(100 * (g.gL - g.pred_L).sum() / disp.sum()), "residual_direita_pct_do_disponivel": float(100 * (g.gD - g.pred_D).sum() / disp.sum())}
    u = g.groupby("SG_UF")[["gL", "pred_L", "gD", "pred_D"]].sum(); u["res_L_pct_do_ganho_L"] = 100 * (u.gL - u.pred_L) / u.gL
    r["ufs_com_residual_de_Lula_positivo"] = int(((u.gL - u.pred_L) > 0).sum()); r["ufs"] = int(len(u))
    out[ano] = r
json.dump(out, open(f"{OP}/resultados/hipotese_video_m6.json", "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1))
