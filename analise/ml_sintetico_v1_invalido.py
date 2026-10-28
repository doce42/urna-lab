"""VERSÃO 1 — INVÁLIDA (circular): a classe "limpa" do treino eram os próprios dados reais e o limiar foi calibrado neles;
qualquer fraude presente nos dados reais seria aprendida como normal, e "~1% marcadas" sai por construção. Mantido só
como registro. Versão válida: ml_sintetico.py (classe limpa simulada por modelo gerador).

T23: classificador treinado com fraude sintética (Zhang, Alvarez e Levin, PLOS ONE 2019), aplicado às seções reais.

1. Dados reais por seção (2º turno, com o 1º turno da mesma seção como referência).
2. Cópias com fraude injetada em parte das seções sorteadas (semente 23):
   - troca: move uma fração f dos votos do adversário para o candidato 13 (ou o contrário, para ser simétrico);
   - enchimento: acrescenta votos ao candidato com uma fração das abstenções (sobe o comparecimento).
3. Variáveis (só observáveis, sem o rótulo): comparecimento 1º/2º e mudança; % do 13 no 1º e 2º; virada em logit e
   seu resíduo em relação ao município; branco+nulo; habilitação biográfica / comparecimento; tamanho.
4. Treino (HistGradientBoosting) em metade dos municípios; teste na outra metade (sem vazamento de município).
5. Limiar calibrado para 1% de falso alarme nas seções limpas de teste; aplicado às seções reais (sem injeção).
   Esperado sem fraude: ~1% marcadas. Também reporta o poder (fração de seções fraudadas detectadas) por cenário.
Uso: python ml_sintetico.py [2026|2022]
"""
import json
import os
import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score

AQUI = os.path.dirname(os.path.abspath(__file__))
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"
rng = np.random.default_rng(23)
b = pd.read_parquet(os.path.join(AQUI, "base.parquet" if ANO == "2026" else f"base_{ANO}.parquet"))
b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20) & (b["SG_UF"] != "ZZ")].reset_index(drop=True)
b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
lg = lambda x, n: np.log((x + .5) / (n - x + .5))


def variaveis(L2, F2, comp2, df):
    """Variáveis observáveis por seção, dados os votos do 2º turno (possivelmente manipulados)."""
    V2 = L2 + F2
    x = pd.DataFrame({
        "comp1": df["QT_COMPARECIMENTO_1"] / df["QT_APTOS_1"], "comp2": comp2 / df["QT_APTOS_2"],
        "p1": df["v13_1"] / df["validos_1"], "p2": L2 / V2,
        "sw": lg(L2, V2) - lg(df["v13_1"], df["validos_1"]),
        "bn2": (df["branco_2"] + df["nulo_2"]) / comp2,
        "bio": df["QT_ELEI_BIOM_SEM_HABILITACAO_2"] / comp2, "aptos": np.log(df["QT_APTOS_2"]),
    })
    x["dcomp"] = x["comp2"] - x["comp1"]
    x["sw_res"] = x["sw"] - x.groupby(df["mun"].values)["sw"].transform("median")
    x["p2_res"] = x["p2"] - x.groupby(df["mun"].values)["p2"].transform("median")
    x["dcomp_res"] = x["dcomp"] - x.groupby(df["mun"].values)["dcomp"].transform("median")
    return x.replace([np.inf, -np.inf], np.nan).fillna(0)


L, F, C = b["v13_2"].values.astype(float), b["v22_2"].values.astype(float), b["QT_COMPARECIMENTO_2"].values.astype(float)
aptos = b["QT_APTOS_2"].values.astype(float)
X0 = variaveis(L, F, C, b)

# cenários de fraude (frações por seção), aplicados a 10% das seções sorteadas
CENARIOS = [("troca 5%", "troca", 0.05), ("troca 10%", "troca", 0.10), ("troca 20%", "troca", 0.20),
            ("enchimento 30% das abstenções", "encher", 0.30), ("enchimento 60% das abstenções", "encher", 0.60)]
Xs, ys, cen = [X0], [np.zeros(len(b), int)], [np.full(len(b), "limpo", object)]
for nome, tipo, f in CENARIOS:
    sel = rng.random(len(b)) < 0.10
    lado = rng.random(len(b)) < 0.5  # metade a favor do 13, metade a favor do adversário (simétrico)
    L2, F2, C2 = L.copy(), F.copy(), C.copy()
    if tipo == "troca":
        mov_a = np.minimum(np.round(f * (L + F)), F); mov_b = np.minimum(np.round(f * (L + F)), L)
        L2[sel & lado] += mov_a[sel & lado]; F2[sel & lado] -= mov_a[sel & lado]
        F2[sel & ~lado] += mov_b[sel & ~lado]; L2[sel & ~lado] -= mov_b[sel & ~lado]
    else:
        add = np.round(f * (aptos - C))
        L2[sel & lado] += add[sel & lado]; F2[sel & ~lado] += add[sel & ~lado]; C2[sel] += add[sel]
    Xs.append(variaveis(L2, F2, C2, b)); ys.append(sel.astype(int)); cen.append(np.where(sel, nome, "limpo"))
X = pd.concat(Xs, ignore_index=True); y = np.concatenate(ys); cenario = np.concatenate(cen)
mun = np.tile(b["mun"].values, len(Xs))
muns = np.unique(b["mun"].values)
treino_m = set(rng.choice(muns, len(muns) // 2, replace=False))
tr = np.array([m in treino_m for m in mun])
clf = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.1, random_state=23)
clf.fit(X[tr], y[tr])
p = clf.predict_proba(X[~tr])[:, 1]
yt, ct = y[~tr], cenario[~tr]
lim = np.quantile(p[yt == 0], 0.99)  # 1% de falso alarme nas seções limpas de teste
R = {"ano": ANO, "secoes": int(len(b)), "auc_teste": float(roc_auc_score(yt, p)), "limiar_1pct": float(lim),
     "poder_por_cenario": {c: float((p[ct == c] > lim).mean()) for c in np.unique(ct) if c != "limpo"}}
# aplicação às seções reais (sem injeção), só nos municípios de teste (o modelo não as viu)
real = ~np.array([m in treino_m for m in b["mun"].values])
pr = clf.predict_proba(X0[real])[:, 1]
marcadas = pr > lim
R["reais"] = {"secoes_avaliadas": int(real.sum()), "fracao_marcada": float(marcadas.mean()), "esperado_sem_fraude": 0.01,
              "marcadas": int(marcadas.sum())}
mm = b[real][marcadas]
R["reais"]["marcadas_por_lado"] = {"virada_maior_que_municipio": int((X0[real][marcadas]["sw_res"] > 0).sum()),
                                    "virada_menor_que_municipio": int((X0[real][marcadas]["sw_res"] < 0).sum())}
R["reais"]["marcadas_por_uf_top"] = mm["SG_UF"].value_counts().head(10).to_dict()
json.dump(R, open(os.path.join(AQUI, f"resultado_ml_{ANO}.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
