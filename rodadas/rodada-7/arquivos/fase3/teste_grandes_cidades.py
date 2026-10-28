"""Teste H-GC (fase3/PREREG_GRANDES_CIDADES.md): a virada de 2026 das 5 maiores cidades está fora do previsto pelo histórico
de 2022 e pelo perfil do 1º turno, comparada às outras cidades grandes? Poder determinístico e falso alarme por deixar-um-fora.
Saída: fase3/resultados/teste_grandes_cidades.json."""
import json
import numpy as np, pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
ALVOS = ["SP71072", "RJ60011", "DF97012", "CE13897", "BA38490"]
NOMES = {"SP71072": "São Paulo", "RJ60011": "Rio de Janeiro", "DF97012": "Brasília", "CE13897": "Fortaleza", "BA38490": "Salvador"}


def mun(ano):
    b = pd.read_parquet(f"{RAIZ}/analise/base.parquet" if ano == "2026" else f"{RAIZ}/analise/base_{ano}.parquet")
    b = b[b.SG_UF != "ZZ"].copy(); b["mun"] = b.SG_UF + b.CD_MUNICIPIO.astype(int).astype(str)
    cols = ["v13_1", "v22_1", "validos_1", "v13_2", "v22_2", "validos_2", "QT_APTOS_2"]
    g = b.groupby("mun")[cols].sum(); g["uf"] = b.groupby("mun").SG_UF.first()
    g["sw"] = lg(g.v13_2, g.validos_2) - lg(g.v13_1, g.validos_1)
    return g


m26, m22 = mun("2026"), mun("2022")
d = m26.join(m22[["sw"]].rename(columns={"sw": "sw22"}), how="inner")
d["pL"], d["pA"] = d.v13_1 / d.validos_1, d.v22_1 / d.validos_1; d["pO"] = 1 - d.pL - d.pA
d["lele"] = np.log(d.QT_APTOS_2)
UFD = pd.get_dummies(d.uf, drop_first=True).astype(float)
X = np.column_stack([np.ones(len(d)), d.sw22, d.pL, d.pA, d.lele, UFD.values]); y = d.sw.values; w = d.QT_APTOS_2.values.astype(float)
alvo = d.index.isin(ALVOS)
grandes = d[~alvo].sort_values("QT_APTOS_2", ascending=False).index[:200]


def ajusta(fora_mask):
    sw_ = np.sqrt(w[fora_mask]); beta, *_ = np.linalg.lstsq(X[fora_mask] * sw_[:, None], y[fora_mask] * sw_, rcond=None); return beta


beta = ajusta(~alvo); res = y - X @ beta
gi = d.index.get_indexer(grandes); r_g = res[gi]; esc = float(1.4826 * np.median(np.abs(r_g - np.median(r_g)))); cen = float(np.median(r_g))
LIM = 3.0
R = {"pre_registro": "fase3/PREREG_GRANDES_CIDADES.md", "municipios": int(len(d)), "escala_robusta_200_maiores": esc, "centro": cen, "limiar_desvios": LIM, "cidades": {}}
for c in ALVOS:
    i = d.index.get_loc(c); z = (res[i] - cen) / esc
    pred_share = 1 / (1 + np.exp(-(lg(d.v13_1.iloc[i], d.validos_1.iloc[i]) + X[i] @ beta)))
    votos_dif = float(d.v13_2.iloc[i] - pred_share * d.validos_2.iloc[i])
    # poder determinístico: deslocamento do logit por troca de m dos válidos (adversário → Lula)
    pod = {}
    for mg in (0.02, 0.05, 0.10):
        L2, V2 = d.v13_2.iloc[i], d.validos_2.iloc[i]; L2m = min(L2 + mg * V2, V2)
        dlog = float(lg(L2m, V2) - lg(L2, V2)); pod[f"{int(mg*100)}pct"] = {"votos": float(L2m - L2), "deslocamento_logit": dlog, "em_desvios": dlog / esc, "testavel": bool(dlog / esc > LIM)}
    R["cidades"][NOMES[c]] = {"z": float(z), "desviante": bool(abs(z) > LIM), "virada_observada": float(y[i]), "virada_prevista": float(X[i] @ beta),
                              "votos_de_lula_acima_do_previsto": votos_dif, "validos_2T": int(d.validos_2.iloc[i]), "poder": pod}
    print(NOMES[c], round(z, 2), round(votos_dif), {k: (int(v["votos"]), round(v["em_desvios"], 1), v["testavel"]) for k, v in pod.items()}, flush=True)
# validação: deixar-um-fora nos 200 maiores não alvo
marc = 0
for g in grandes:
    msk = ~alvo & (d.index != g); bb = ajusta(msk); rr = y - X @ bb
    others = [x for x in grandes if x != g]; ro = rr[d.index.get_indexer(others)]; e2 = 1.4826 * np.median(np.abs(ro - np.median(ro)))
    if abs((rr[d.index.get_loc(g)] - np.median(ro)) / e2) > LIM: marc += 1
R["validacao_falso_alarme"] = {"municipios": len(grandes), "marcados": marc, "taxa": marc / len(grandes), "regra_valida": marc / len(grandes) <= 0.05}
R["r2_ponderado"] = float(1 - (w * res ** 2)[~alvo].sum() / (w * (y - np.average(y, weights=w)) ** 2)[~alvo].sum())
print("falso alarme", marc, "/", len(grandes), "r2", round(R["r2_ponderado"], 3))
json.dump(R, open(RAIZ + "/fase3/resultados/teste_grandes_cidades.json", "w"), ensure_ascii=False, indent=1)
