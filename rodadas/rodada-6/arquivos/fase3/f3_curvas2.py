"""F3 sessão 2 / E2b: curvas com nulos condicionados em UF × hora de encerramento (D) e UF × hora × tamanho (F). Ver PREREG.md (adendo sessão 2)."""
import json, time
import numpy as np, pandas as pd
src = open("fase3/f3_curvas.py").read().split("R = {\"pergunta\"")[0]
exec(src)
T0 = time.time(); R = {"pergunta": "E2b curvas, nulos condicionados", "nperm": NPERM, "resultados": {}}
for ano in ("2026", "2022"):
    for t in (1, 2):
        b = carrega(ano, t); n = len(b)
        L = b[f"v13_{t}"].values.astype(float); A = b[f"v22_{t}"].values.astype(float); V = b[f"validos_{t}"].values.astype(float)
        enc = pd.to_datetime(b[f"DT_ENCERRAMENTO_{t}"], errors="coerce", dayfirst=False)
        hora = (enc.dt.hour.fillna(-1).astype(int) * 2 + (enc.dt.minute.fillna(0) >= 30).astype(int)).values   # faixa de 30 min
        tam = pd.qcut(b[f"QT_APTOS_{t}"].rank(method="first"), 3, labels=False).values
        uf = b["SG_UF"].values
        rD = pd.Series(uf).astype(str) + "|" + pd.Series(hora).astype(str); rF = rD + "|" + pd.Series(tam).astype(str)
        obs = estat(L, A, V, 1.0); rng = np.random.default_rng(4001 + (0 if ano == "2026" else 100) + t)
        R_ = {"urnas": n, "observado": obs, "eta2_ordem_por_UF_hora": eta2(rD.values, np.arange(n) / n), "eta2_ordem_por_UF_hora_tamanho": eta2(rF.values, np.arange(n) / n),
              "grupos_D": int(rD.nunique()), "grupos_F": int(rF.nunique())}
        for nome, rot in (("D_UF_x_hora_encerramento", rD.values), ("F_UF_x_hora_x_tamanho", rF.values)):
            sims = [estat(L[o], A[o], V[o], 1.0) for o in (perm_grupo(rot, rng) for _ in range(NPERM))]
            res = {}
            for k in obs:
                if k.startswith("_"): continue
                a = np.array([s[k] for s in sims], float); o = obs[k]
                res[k] = {"observado": o, "sim_media": float(a.mean()), "sim_p2_5_p97_5": [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))],
                          "p_bilateral": float(min(1, 2 * min((1 + (a >= o).sum()) / (NPERM + 1), (1 + (a <= o).sum()) / (NPERM + 1))))}
            R_[nome] = res
        R["resultados"][f"{ano}_{t}t"] = R_
        print(ano, t, round(time.time() - T0), "s", {nm: {k: R_[nm][k]["p_bilateral"] for k in R_[nm]} for nm in ("D_UF_x_hora_encerramento", "F_UF_x_hora_x_tamanho")}, "eta2", round(R_["eta2_ordem_por_UF_hora"], 2), round(R_["eta2_ordem_por_UF_hora_tamanho"], 2), flush=True)
json.dump(R, open(f"{OUT}/E2b_curvas.json", "w"), indent=1, ensure_ascii=False, default=float)
