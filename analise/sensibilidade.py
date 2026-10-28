"""Sensibilidade (DIRETRIZ, nível 3, passo 6): os resultados do T02 e do T03 mudam com as escolhas do analista?

Varia, uma de cada vez e em combinação:
  - mínimo de votos válidos por seção nos dois turnos: 20 (padrão), 50, 100
  - limiar de desvios: 3, 4, 5 (padrão), 6
  - escala do z: MAD robusto (padrão) x desvio-padrão clássico
  - nível do efeito fixo: município (padrão) x zona eleitoral
Saída: resultado_sensibilidade_<ano>.json. Uso: python sensibilidade.py <ano>
"""
import itertools
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"
b0 = pd.read_parquet(os.path.join(AQUI, "base.parquet" if ANO == "2026" else f"base_{ANO}.parquet"))
b0["mun"] = b0["SG_UF"] + b0["CD_MUNICIPIO"]
b0["zona"] = b0["SG_UF"] + "-" + b0["NR_ZONA"]
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
saida = []
for minimo, nivel, escala in itertools.product((20, 50, 100), ("mun", "zona"), ("mad", "dp")):
    b = b0[(b0["validos_1"] >= minimo) & (b0["validos_2"] >= minimo)]
    x1, n1, x2, n2 = b["v13_1"], b["validos_1"], b["v13_2"], b["validos_2"]
    sw = lg(x2, n2) - lg(x1, n1)
    res = sw - sw.groupby(b[nivel]).transform("median")
    z = res / np.sqrt(1 / (x1 + .5) + 1 / (n1 - x1 + .5) + 1 / (x2 + .5) + 1 / (n2 - x2 + .5))
    z = (z - z.median()) / (1.4826 * (z - z.median()).abs().median() if escala == "mad" else z.std())
    linha = {"minimo_validos": minimo, "nivel": nivel, "escala": escala, "secoes": int(len(b))}
    for lim in (3, 4, 5, 6):
        linha[f"acima_{lim}_lula"] = int((z > lim).sum())
        linha[f"acima_{lim}_adversario"] = int((z < -lim).sum())
    g = b[b.groupby(nivel)[nivel].transform("size") >= 20]
    pos = g.groupby(nivel)["DT_BU_RECEBIDO_2"].rank(pct=True)
    linha["T03_spearman"] = float(stats.spearmanr(pos, res[g.index])[0])
    saida.append(linha)
R = {"ano": ANO, "combinacoes": saida}
json.dump(R, open(os.path.join(AQUI, f"resultado_sensibilidade_{ANO}.json"), "w"), ensure_ascii=False, indent=1)
t = pd.DataFrame(saida)
print(t[["minimo_validos", "nivel", "escala", "secoes", "acima_5_lula", "acima_5_adversario", "T03_spearman"]].to_string(index=False))
