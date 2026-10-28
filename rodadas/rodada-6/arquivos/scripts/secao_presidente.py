"""Separa da votação por seção (TSE, todos os cargos) só Presidente, um arquivo por turno, em UTF-8.
Uso: unzip -p votacao_secao_<ano>_BR.zip ... | python secao_presidente.py /dev/stdin <pasta_destino>
Saída: <pasta>/1turno/presidente_1turno_secao.csv e <pasta>/2turno/presidente_2turno_secao.csv
"""
import csv
import os
import sys

ent, dest = sys.argv[1], sys.argv[2]
rd = csv.DictReader(open(ent, encoding="latin1"), delimiter=";")
out, w = {}, {}
for t in "12":
    os.makedirs(os.path.join(dest, f"{t}turno"), exist_ok=True)
    out[t] = open(os.path.join(dest, f"{t}turno", f"presidente_{t}turno_secao.csv"), "w", encoding="utf-8", newline="")
    w[t] = csv.DictWriter(out[t], fieldnames=rd.fieldnames, delimiter=";", quoting=csv.QUOTE_ALL)
    w[t].writeheader()
for r in rd:
    if r["CD_CARGO"] == "1" and r["NR_TURNO"] in w:
        w[r["NR_TURNO"]].writerow(r)
