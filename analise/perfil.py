"""Agrega o perfil do eleitorado (TSE) por seção: idade, escolaridade, sexo, biometria cadastrada.
Uso: python perfil.py [2026|2022]  → perfil.parquet (2026) ou perfil_2022.parquet
"""
import glob
import os
import sys
import zipfile

import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"
DADOS = os.path.join(AQUI, "..", "dados", "perfil_eleitorado") if ANO == "2026" else os.path.join(AQUI, "..", "dados", ANO, "perfil_eleitorado")
COLS = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_GENERO", "CD_FAIXA_ETARIA", "CD_GRAU_ESCOLARIDADE",
        "QT_ELEITORES", "QT_ELEITORES_BIOMETRIA"]
partes = []
for z in sorted(glob.glob(os.path.join(DADOS, f"perfil_eleitor_secao_{ANO}_*.zip"))):
    with zipfile.ZipFile(z) as zf:
        nome = [n for n in zf.namelist() if n.endswith(".csv")][0]
        for ch in pd.read_csv(zf.open(nome), sep=";", encoding="latin1", chunksize=2_000_000,
                              usecols=lambda c: c in COLS or c == "QT_ELEITORES_PERFIL"):
            ch = ch.rename(columns={"QT_ELEITORES_PERFIL": "QT_ELEITORES"})  # nome em 2022
            fx = ch["CD_FAIXA_ETARIA"]
            ch["idoso"] = ch["QT_ELEITORES"] * (fx >= 6064)              # 60 anos ou mais (códigos 6064, 6569, ...)
            ch["jovem"] = ch["QT_ELEITORES"] * (fx <= 2024)              # até 24 anos
            ch["baixa_esc"] = ch["QT_ELEITORES"] * ch["CD_GRAU_ESCOLARIDADE"].isin([1, 2, 3])  # analfabeto, lê e escreve, fund. incompleto
            ch["superior"] = ch["QT_ELEITORES"] * ch["CD_GRAU_ESCOLARIDADE"].isin([7, 8])
            ch["mulher"] = ch["QT_ELEITORES"] * (ch["CD_GENERO"] == 4)
            g = ch.groupby(["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"])[
                ["QT_ELEITORES", "QT_ELEITORES_BIOMETRIA", "idoso", "jovem", "baixa_esc", "superior", "mulher"]].sum()
            partes.append(g)
    print(os.path.basename(z), flush=True)
p = pd.concat(partes).groupby(level=[0, 1, 2, 3]).sum()
for c in ["QT_ELEITORES_BIOMETRIA", "idoso", "jovem", "baixa_esc", "superior", "mulher"]:
    p["p_" + c.lower().replace("qt_eleitores_", "")] = p[c] / p["QT_ELEITORES"]
p = p.reset_index()
p["CD_MUNICIPIO"] = p["CD_MUNICIPIO"].astype(int).astype(str)
p["NR_ZONA"] = p["NR_ZONA"].astype(str)
p["NR_SECAO"] = p["NR_SECAO"].astype(str)
p.to_parquet(os.path.join(AQUI, "perfil.parquet" if ANO == "2026" else f"perfil_{ANO}.parquet"))
print(p.shape, p[["p_biometria", "p_idoso", "p_baixa_esc"]].describe().round(3).to_string())
