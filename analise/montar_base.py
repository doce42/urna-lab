"""Junta 1º e 2º turno numa linha por seção, a partir do Boletim de Urna (só Presidente).

Uso: python montar_base.py [2026|2022]   (2026 -> base.parquet; outro ano -> base_<ano>.parquet)
"""
import glob
import os
import sys

import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"
DADOS = os.path.join(AQUI, "..", "dados") if ANO == "2026" else os.path.join(AQUI, "..", "dados", ANO)
# 2022 usa outros nomes em duas colunas
RENOMEIA = {"DS_AGREGADAS": "DS_SECOES_AGREGADAS", "QT_ELEITORES_BIOMETRIA_NH": "QT_ELEI_BIOM_SEM_HABILITACAO"}
CHAVE = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
META = ["NM_MUNICIPIO", "NR_LOCAL_VOTACAO", "QT_APTOS", "QT_COMPARECIMENTO", "NR_URNA_EFETIVADA",
        "DT_CARGA_URNA_EFETIVADA", "DS_SECOES_AGREGADAS", "DT_ABERTURA", "DT_ENCERRAMENTO",
        "DT_EMISSAO_BU", "DT_BU_RECEBIDO", "QT_ELEI_BIOM_SEM_HABILITACAO", "DS_TIPO_URNA"]


def turno(n):
    arqs = sorted(glob.glob(os.path.join(DADOS, f"{n}turno", f"bweb_{n}t_*_presidente.csv")))
    usa = lambda c: c in CHAVE + META + ["DS_TIPO_VOTAVEL", "NR_VOTAVEL", "QT_VOTOS"] + list(RENOMEIA)
    df = pd.concat([pd.read_csv(a, sep=";", dtype=str, usecols=usa).rename(columns=RENOMEIA) for a in arqs], ignore_index=True)
    df["QT_VOTOS"] = df["QT_VOTOS"].astype(int)
    df["col"] = df["NR_VOTAVEL"].where(df["DS_TIPO_VOTAVEL"].str.lower() == "nominal", df["DS_TIPO_VOTAVEL"].str.lower())
    votos = df.pivot_table(index=CHAVE, columns="col", values="QT_VOTOS", aggfunc="sum", fill_value=0)
    votos.columns = [("v" + c if c[0].isdigit() else c) for c in votos.columns]
    meta = df.drop_duplicates(CHAVE).set_index(CHAVE)[META]
    out = meta.join(votos)
    for c in ["QT_APTOS", "QT_COMPARECIMENTO", "QT_ELEI_BIOM_SEM_HABILITACAO"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    for c in ["DT_ABERTURA", "DT_ENCERRAMENTO", "DT_EMISSAO_BU", "DT_BU_RECEBIDO"]:
        out[c] = pd.to_datetime(out[c], errors="coerce", format="ISO8601" if ANO == "2026" else "%d/%m/%Y %H:%M:%S")
    cand = [c for c in out.columns if c.startswith("v")]
    out["validos"] = out[cand].sum(axis=1)
    out["total"] = out["validos"] + out["branco"] + out["nulo"]
    return out.add_suffix(f"_{n}")


b = turno(1).join(turno(2), how="outer")
b.reset_index().to_parquet(os.path.join(AQUI, "base.parquet" if ANO == "2026" else f"base_{ANO}.parquet"))
print(b.shape)
print("só no 1º:", b["total_2"].isna().sum(), " só no 2º:", b["total_1"].isna().sum())
print("votos 1º:", int(b["total_1"].sum()), " 2º:", int(b["total_2"].sum()))
