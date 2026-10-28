"""Conferências rápidas de sanidade do estudo (rodar depois de qualquer mudança). Sai com erro se algo falhar.
  1. registro: todo script citado existe
  2. totalização (T32): todos os votos da soma das urnas = total oficial
  3. cobertura: urnas processadas (arquivos das urnas) x urnas no Boletim de Urna, por turno
  4. documentação: os arquivos de método existem
"""
import glob
import json
import os
import sys

import pandas as pd

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
falhas = []
reg = json.load(open(f"{R}/testes/registro.json"))
for t in reg["testes"]:
    for s in [x.strip() for x in t["script"].split(",")]:
        if s and not s.startswith("(") and not os.path.exists(f"{R}/{s}"):
            falhas.append(f"registro: {t['id']} cita {s}, que não existe")
print(f"[1] registro: {len(reg['testes'])} testes")

f = f"{R}/analise/resultado_totalizacao.csv"
if os.path.exists(f):
    t = pd.read_csv(f, sep=";")
    votos = t[t["item"] != "eleitorado"]
    ruins = votos[~votos["igual"]]
    print(f"[2] totalização: {len(votos) - len(ruins)} de {len(votos)} itens de voto/comparecimento iguais ao oficial")
    if len(ruins):
        falhas.append(f"totalização: {len(ruins)} itens diferentes")
else:
    print("[2] totalização: ainda não rodada (make totalizacao)")

b = pd.read_parquet(f"{R}/analise/base.parquet")
for turno in (1, 2):
    arqs = glob.glob(f"{R}/analise/brutos/{turno}t/urnas_*.parquet")
    if not arqs:
        print(f"[3] cobertura {turno}º turno: sem arquivos processados")
        continue
    u = pd.concat([pd.read_parquet(a, columns=["SG_UF"]) for a in arqs])
    esperado = int(b[f"total_{turno}"].notna().sum())
    print(f"[3] cobertura {turno}º turno: {len(u):,} urnas processadas de {esperado:,} no Boletim de Urna ({100*len(u)/esperado:.2f}%)")

for d in ["DIRETRIZ.md", "AGENTS.md", "PROTOCOLO.md", "METODOLOGIA.md", "AUTOAUDITORIA.md", "CATALOGO.md", "PIPELINE.md", "REFERENCIAS.md", "MAPA_SKILLS.md"]:
    if not os.path.exists(f"{R}/{d}"):
        falhas.append(f"documentação: falta {d}")
print("[4] documentação conferida")
if falhas:
    print("FALHAS:\n  " + "\n  ".join(falhas)); sys.exit(1)
print("tudo ok")
