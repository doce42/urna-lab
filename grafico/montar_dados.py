"""Monta os dados do gráfico a partir dos arquivos oficiais do TSE (Presidente, 1º e 2º turno de 2026).

Entrada (em ../dados/<n>turno/):
  bweb_<n>t_<UF>_presidente.csv     Boletim de Urna, uma linha por votável por urna, com os horários
  presidente_<n>turno_secao.csv     votação por seção, só para conferir os totais
Saída:
  ../dados/<n>turno/presidente_<n>turno_horarios_por_urna.csv
  ./web/dados.json
"""
import collections
import csv
import glob
import json
import os
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "..", "dados")
T = ["DT_ABERTURA", "DT_ENCERRAMENTO", "DT_EMISSAO_BU", "DT_BU_RECEBIDO"]
DIA = {1: "2026-10-04", 2: "2026-10-25"}


def chave(tipo, nr):
    if tipo == "Branco":
        return "branco"
    if tipo == "Nulo":
        return "nulo"
    return "c" + nr


def ler_urnas(turno):
    urnas, nomes = {}, {}
    for f in sorted(glob.glob(os.path.join(DADOS, f"{turno}turno", f"bweb_{turno}t_*_presidente.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8"), delimiter=";"):
            k = (r["SG_UF"], r["CD_MUNICIPIO"], r["NR_ZONA"], r["NR_SECAO"])
            u = urnas.get(k)
            if u is None:
                u = urnas[k] = {"SG_UF": k[0], "CD_MUNICIPIO": k[1], "NM_MUNICIPIO": r["NM_MUNICIPIO"],
                                "NR_ZONA": k[2], "NR_SECAO": k[3], **{t: r[t] for t in T},
                                "QT_APTOS": r["QT_APTOS"], "QT_COMPARECIMENTO": r["QT_COMPARECIMENTO"],
                                "votos": collections.Counter()}
            c = chave(r["DS_TIPO_VOTAVEL"], r["NR_VOTAVEL"])
            if c.startswith("c"):
                nomes[c] = r["NM_VOTAVEL"]
            u["votos"][c] += int(r["QT_VOTOS"])
    return list(urnas.values()), nomes


def conferir(turno, urnas):
    """Os totais do Boletim de Urna têm que bater com a votação por seção, votável por votável."""
    sec = collections.Counter()
    for r in csv.DictReader(open(os.path.join(DADOS, f"{turno}turno", f"presidente_{turno}turno_secao.csv"),
                                 encoding="utf-8"), delimiter=";"):
        nr = r["NR_VOTAVEL"]
        sec["branco" if nr == "95" else "nulo" if nr == "96" else "c" + nr] += int(r["QT_VOTOS"])
    bu = collections.Counter()
    for u in urnas:
        bu.update(u["votos"])
    ok = True
    for k in sorted(set(sec) | set(bu), key=lambda k: -sec[k]):
        bate = sec[k] == bu[k]
        ok &= bate
        print(f"  {k:>7}: boletim {bu[k]:>12,}  seção {sec[k]:>12,}  {'ok' if bate else 'DIFERENTE'}")
    return ok


def seg_do_dia(s, turno):
    """Segundos desde a meia-noite do dia da eleição (passa de 86400 se entrar na madrugada)."""
    d = datetime.strptime(s, "%Y-%m-%d %H:%M:%S") - datetime.strptime(DIA[turno], "%Y-%m-%d")
    return int(d.total_seconds())


def serie(pontos, chaves):
    acc = collections.defaultdict(collections.Counter)
    for t, votos in pontos:
        acc[t].update(votos)
        acc[t]["_urnas"] += 1
    ts = sorted(acc)
    out = {"t": ts, "urnas": [acc[t]["_urnas"] for t in ts]}
    for c in chaves:
        out[c] = [acc[t][c] for t in ts]
    return out


def montar(turno):
    urnas, nomes = ler_urnas(turno)
    print(f"{turno}º turno: {len(urnas)} urnas")
    cands = sorted(nomes)
    with open(os.path.join(DADOS, f"{turno}turno", f"presidente_{turno}turno_horarios_por_urna.csv"),
              "w", encoding="utf-8", newline="") as o:
        w = csv.writer(o, delimiter=";")
        campos = [k for k in urnas[0] if k != "votos"]
        w.writerow(campos + [nomes[c] for c in cands] + ["BRANCO", "NULO"])
        for u in urnas:
            w.writerow([u[k] for k in campos] + [u["votos"][c] for c in cands + ["branco", "nulo"]])
    if not conferir(turno, urnas):
        raise SystemExit("totais não batem, parei")

    # Fuso do município: a abertura é às 8h de Brasília, então a hora local de abertura dá o fuso.
    # Vale o mais comum entre as urnas do município que abriram nos primeiros 15 minutos: urna atrasada não conta.
    # Município sem nenhuma urna no horário usa o fuso mais comum do estado.
    moda = collections.defaultdict(collections.Counter)
    moda_uf = collections.defaultdict(collections.Counter)
    for u in urnas:
        h, mi = u["DT_ABERTURA"][11:13], u["DT_ABERTURA"][14:16]
        if h in ("06", "07", "08") and mi < "15":
            moda[(u["SG_UF"], u["CD_MUNICIPIO"])][8 - int(h)] += 1
            moda_uf[u["SG_UF"]][8 - int(h)] += 1

    receb, emis, fora = [], [], 0
    for u in urnas:
        receb.append((seg_do_dia(u["DT_BU_RECEBIDO"], turno), u["votos"]))
        # Exterior: cada país tem seu fuso e o boletim não diz qual, então fica só no eixo de recebimento.
        if u["SG_UF"] == "ZZ" or not u["DT_EMISSAO_BU"]:
            fora += 1
            continue
        dif = (moda.get((u["SG_UF"], u["CD_MUNICIPIO"])) or moda_uf[u["SG_UF"]]).most_common(1)[0][0]
        emis.append((seg_do_dia(u["DT_EMISSAO_BU"], turno) + dif * 3600, u["votos"]))

    total = collections.Counter()
    for u in urnas:
        total.update(u["votos"])
    chaves = sorted(nomes, key=lambda c: -total[c]) + ["branco", "nulo"]
    nomes.update(branco="Branco", nulo="Nulo")
    return {"data": DIA[turno], "chaves": chaves, "nomes": {c: nomes[c] for c in chaves},
            "recebido": serie(receb, chaves), "emissao": serie(emis, chaves),
            "fora_emissao": fora, "total_urnas": len(urnas)}


def main():
    saida = {"t1": montar(1), "t2": montar(2)}
    os.makedirs(os.path.join(AQUI, "web"), exist_ok=True)
    with open(os.path.join(AQUI, "web", "dados.json"), "w") as o:
        json.dump(saida, o, separators=(",", ":"))
    print("ok")


if __name__ == "__main__":
    main()
