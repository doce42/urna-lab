"""Módulo E: divergências em vários níveis (E01), agrupamento (E02) e lista das maiores (E03).

Ideia: uma manipulação real age num lugar (local de votação, zona, município). Se ela existir, as seções desse lugar
divergem do próprio histórico NA MESMA DIREÇÃO, mais do que o acaso explica.

E01  resíduo da virada de cada seção (logit; modelo N2 com a virada do ESTADO, para que divergências de município
     inteiro também apareçam) e decomposição da variância por nível (seção / local / zona / município / UF)
E02  para cada local de votação, zona e município: teste de excesso de divergência em relação ao ruído esperado das
     próprias seções (estatística z da média dos z das seções; sob o nulo, média de k z independentes ~ N(0, 1/k));
     Benjamini-Hochberg (q = 0,05) dentro de cada nível
E03  lista dos locais/zonas/municípios significativos, com características para explicar (tamanho, % no 1º turno,
     voto órfão, mudança de comparecimento, sem biometria)
Uso: python divergencias.py [2026|2022] [simples|completo]
"""
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"
b = pd.read_parquet(os.path.join(AQUI, "base.parquet" if ANO == "2026" else f"base_{ANO}.parquet"))
b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20) & (b["SG_UF"] != "ZZ")].copy()
b["mun"] = b["SG_UF"] + "-" + b["CD_MUNICIPIO"]
b["zona"] = b["SG_UF"] + "-" + b["NR_ZONA"]
b["local"] = b["mun"] + "-" + b["NR_ZONA"] + "-" + b["NR_LOCAL_VOTACAO_2"].astype(str)  # local de votação
x1, n1, x2, n2 = b["v13_1"], b["validos_1"], b["v13_2"], b["validos_2"]
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
b["sw"] = lg(x2, n2) - lg(x1, n1)
# esperado (por UF):
#  modelo "simples":  % no 1º turno (e quadrado) + voto órfão total
#  modelo "completo": + % de CADA candidato eliminado (transferências diferentes), branco/nulo no 1º turno,
#                     mudança de comparecimento, porte do município (log eleitores) e, em 2026, perfil do eleitorado
MODELO = sys.argv[2] if len(sys.argv) > 2 else "simples"
b["p1"] = x1 / n1
b["orf"] = 1 - (b["v13_1"] + b["v22_1"]) / n1
cols = [np.ones(len(b)), b.p1, b.p1 ** 2, b.orf]
if MODELO == "completo":
    elim = [c for c in b.columns if c.startswith("v") and c.endswith("_1") and c not in ("v13_1", "v22_1", "validos_1")]
    cols += [b[c].fillna(0) / n1 for c in elim]
    cols += [(b["branco_1"] + b["nulo_1"]) / b["total_1"],
             b["QT_COMPARECIMENTO_2"] / b["QT_APTOS_2"] - b["QT_COMPARECIMENTO_1"] / b["QT_APTOS_1"],
             np.log(b.groupby("mun")["QT_APTOS_2"].transform("sum"))]
    if ANO == "2026" and os.path.exists(os.path.join(AQUI, "perfil.parquet")):
        p = pd.read_parquet(os.path.join(AQUI, "perfil.parquet"))
        b = b.reset_index(drop=True).merge(p[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "p_idoso", "p_jovem", "p_baixa_esc", "p_superior", "p_mulher"]],
                                           on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"], how="left")
        for c in ("p_idoso", "p_jovem", "p_baixa_esc", "p_superior", "p_mulher"):
            b[c] = b[c].fillna(b[c].mean())
        x1, n1, x2, n2 = b["v13_1"], b["validos_1"], b["v13_2"], b["validos_2"]
        cols = [np.ones(len(b)), b.p1, b.p1 ** 2, b.orf] + [b[c].fillna(0) / n1 for c in elim] + [
            (b["branco_1"] + b["nulo_1"]) / b["total_1"],
            b["QT_COMPARECIMENTO_2"] / b["QT_APTOS_2"] - b["QT_COMPARECIMENTO_1"] / b["QT_APTOS_1"],
            np.log(b.groupby("mun")["QT_APTOS_2"].transform("sum"))] + [b[c] for c in ("p_idoso", "p_jovem", "p_baixa_esc", "p_superior", "p_mulher")]
X = np.column_stack([np.asarray(c, float) for c in cols])
X = np.nan_to_num(X)
b["esp"] = 0.0
for uf, idx in b.groupby("SG_UF").groups.items():
    beta, *_ = np.linalg.lstsq(X[b.index.get_indexer(idx)], b.loc[idx, "sw"].values, rcond=None)
    b.loc[idx, "esp"] = X[b.index.get_indexer(idx)] @ beta
sd = np.sqrt(1/(x1+.5) + 1/(n1-x1+.5) + 1/(x2+.5) + 1/(n2-x2+.5))
z = (b["sw"] - b["esp"]) / sd
escala = 1.4826 * (z - z.median()).abs().median()   # dispersão real entre seções (eleitores mudam entre turnos)
b["z"] = (z - z.median()) / escala
R = {"ano": ANO, "modelo": MODELO, "secoes": int(len(b)), "escala_z": float(escala)}

# E01: decomposição da variância dos resíduos por nível (entre grupos / total)
tot = b["z"].var()
R["E01"] = {}
for nivel in ("local", "zona", "mun", "SG_UF"):
    medias = b.groupby(nivel)["z"].transform("mean")
    R["E01"][nivel] = {"fracao_variancia_entre_grupos": float(medias.var() / tot), "grupos": int(b[nivel].nunique())}

# E02: excesso por grupo, com BH
def bh(p, q=0.05):
    p = np.asarray(p); n = len(p); ordem = np.argsort(p)
    lim = q * np.arange(1, n + 1) / n
    passa = p[ordem] <= lim
    k = np.max(np.where(passa)[0]) + 1 if passa.any() else 0
    sig = np.zeros(n, bool); sig[ordem[:k]] = True
    return sig


R["E02"] = {}
listas = {}
for nivel in ("local", "zona", "mun"):
    g = b.groupby(nivel).agg(k=("z", "size"), media=("z", "mean"), uf=("SG_UF", "first"), mun=("NM_MUNICIPIO_2", "first"),
                             eleitores=("QT_APTOS_2", "sum"), p1=("p1", "mean"), orf=("orf", "mean"),
                             sw=("sw", "mean"), esp=("esp", "mean"))
    g = g[g["k"] >= 3]
    g["zg"] = g["media"] * np.sqrt(g["k"])          # sob o nulo ~ N(0, 1)
    g["p"] = 2 * stats.norm.sf(g["zg"].abs())
    g["sig"] = bh(g["p"].values)
    # sob o nulo, quantos grupos esperaríamos acima de |zg| > 4 por acaso?
    R["E02"][nivel] = {"grupos": int(len(g)), "significativos_BH": int(g["sig"].sum()),
                       "sig_pro_lula": int((g["sig"] & (g["zg"] > 0)).sum()), "sig_pro_adversario": int((g["sig"] & (g["zg"] < 0)).sum()),
                       "dp_zg": float(g["zg"].std()), "esperado_dp_sem_agrupamento": 1.0}
    listas[nivel] = g[g["sig"]].sort_values("zg", key=np.abs, ascending=False)
    if nivel == "mun":  # tabela completa por município, para os mapas
        g[["uf", "mun", "k", "eleitores", "zg", "p", "sig", "sw", "esp"]].to_csv(
            os.path.join(AQUI, f"divergencias_municipios_{ANO}_{MODELO}.csv"), sep=";")

# E03: maiores divergências, com características
R["E03"] = {}
for nivel, g in listas.items():
    R["E03"][nivel] = [{"grupo": i, "uf": r.uf, "municipio": r.mun, "secoes": int(r.k), "eleitores": int(r.eleitores),
                        "z_grupo": round(float(r.zg), 2), "virada_obs_logit": round(float(r.sw), 3), "virada_esp_logit": round(float(r.esp), 3),
                        "lula_1t": round(float(r.p1), 3), "voto_orfao_1t": round(float(r.orf), 3)}
                       for i, r in g.head(40).iterrows()]
json.dump(R, open(os.path.join(AQUI, f"resultado_divergencias_{ANO}_{MODELO}.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: R[k] for k in ("secoes", "escala_z", "E01", "E02")}, ensure_ascii=False, indent=1))
for nivel in ("mun", "zona", "local"):
    print(f"\n== maiores divergências por {nivel}")
    for r in R["E03"][nivel][:8]:
        print(f"  {r['uf']} {r['municipio'][:28]:28} {r['grupo'][-22:]:22} seções {r['secoes']:4} z {r['z_grupo']:+6.1f} "
              f"virada obs {r['virada_obs_logit']:+.3f} esp {r['virada_esp_logit']:+.3f} | Lula 1º {r['lula_1t']:.2f} órfão {r['voto_orfao_1t']:.2f}")
