"""T01 seção a seção (revisão R1, achado R1-18): o Boletim de Urna na Web e a votação por seção, as duas tabelas
oficiais do TSE, dão o mesmo número de votos para cada votável em cada seção? A versão da rodada 1 só comparava a soma
nacional por votável. Chave: (UF, município, zona, seção, votável); branco = 95 e nulo = 96 na votação por seção.
Uso: python analise/t01_secao.py   saída: resultado_t01_secao.json
"""
import glob
import json
import os

import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "..", "dados")
K = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_VOTAVEL"]
R = {}
for t in (1, 2):
    bu = pd.concat(pd.read_csv(f, sep=";", encoding="utf-8", dtype=str, usecols=K[:4] + ["DS_TIPO_VOTAVEL", "NR_VOTAVEL", "QT_VOTOS"])
                   for f in sorted(glob.glob(os.path.join(D, f"{t}turno", f"bweb_{t}t_*_presidente.csv"))))
    bu.loc[bu["DS_TIPO_VOTAVEL"] == "Branco", "NR_VOTAVEL"] = "95"
    bu.loc[bu["DS_TIPO_VOTAVEL"] == "Nulo", "NR_VOTAVEL"] = "96"
    sec = pd.read_csv(os.path.join(D, f"{t}turno", f"presidente_{t}turno_secao.csv"), sep=";", encoding="utf-8", dtype=str, usecols=K + ["QT_VOTOS"])
    for x in (bu, sec):
        x["QT_VOTOS"] = x["QT_VOTOS"].astype(int)
        for c in K:
            x[c] = x[c].str.strip().str.lstrip("0").replace("", "0") if c != "SG_UF" else x[c].str.strip()
    a = bu.groupby(K)["QT_VOTOS"].sum().rename("bu")
    b = sec.groupby(K)["QT_VOTOS"].sum().rename("secao")
    m = pd.concat([a, b], axis=1)
    so_bu, so_sec = m["secao"].isna(), m["bu"].isna()
    dif = m[(~so_bu) & (~so_sec) & (m["bu"] != m["secao"])]
    secoes_bu = set(map(tuple, a.reset_index()[K[:4]].drop_duplicates().values))
    secoes_sec = set(map(tuple, b.reset_index()[K[:4]].drop_duplicates().values))
    R[f"{t}t"] = {"pares_secao_votavel": int(len(m)), "iguais": int((m["bu"] == m["secao"]).sum()), "diferentes": int(len(dif)),
                  "so_no_bu": int(so_bu.sum()), "so_na_votacao_por_secao": int(so_sec.sum()),
                  "secoes_bu": len(secoes_bu), "secoes_votacao_por_secao": len(secoes_sec), "secoes_em_comum": len(secoes_bu & secoes_sec),
                  "exemplos_diferentes": dif.head(10).reset_index().to_dict("records"),
                  "exemplos_so_bu": m[so_bu].head(5).reset_index().drop(columns="secao").to_dict("records"),
                  "exemplos_so_secao": m[so_sec].head(5).reset_index().drop(columns="bu").to_dict("records")}
    print(t, {k: v for k, v in R[f"{t}t"].items() if not k.startswith("exemplos")})
json.dump(R, open(os.path.join(AQUI, "resultado_t01_secao.json"), "w"), ensure_ascii=False, indent=1, default=str)
