"""Copia só as linhas de Presidente (CD_CARGO_PERGUNTA = 1) de um CSV do Boletim de Urna do TSE, em UTF-8."""
import csv
import sys

ent, sai = sys.argv[1], sys.argv[2]
with open(ent, encoding="latin1", newline="") as f, open(sai, "w", encoding="utf-8", newline="") as o:
    rd = csv.reader(f, delimiter=";")
    cab = next(rd)
    w = csv.writer(o, delimiter=";", quoting=csv.QUOTE_ALL)
    w.writerow(cab)
    i = cab.index("CD_CARGO_PERGUNTA")
    n = 0
    for r in rd:
        if r[i] == "1":
            w.writerow(r)
            n += 1
print(ent.rsplit("/", 1)[-1], n)
