"""Revisão R1, achado R1-02: refaz a verificação da assinatura da lista (vota.vsc) de TODAS as urnas de 2026 com o
verificador Ed521 endurecido (rejeita chave e R degenerados e tamanhos errados) e conta as chaves Ed521 degeneradas.
Se alguma chave real fosse degenerada, a assinatura dela deixaria de valer aqui. Só lê; não altera resultados antigos.
Uso: python analise/varrer_chaves.py <turno>   saída: resultado_varrer_chaves_<turno>t.json
"""
import glob
import json
import os
import sys
import zipfile
from concurrent.futures import ProcessPoolExecutor

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import processar_brutos as pb  # noqa: E402

T = int(sys.argv[1])
PASTA = os.path.join(AQUI, "..", "dados", "brutos", "1turno" if T == 1 else "2turno_pacotes")


def uf(arq):
    z = zipfile.ZipFile(arq)
    r = {"urnas": 0, "Ed521": 0, "ECDSA-P521": 0, "lista_ok": 0, "lista_falhou": [], "sem_bloco": 0}
    for n in z.namelist():
        if not n.endswith("-vota.vsc"):
            continue
        r["urnas"] += 1
        try:
            _, resumo, _ = pb.ler_vsc(z.read(n))
        except Exception:
            r["sem_bloco"] += 1
            continue
        r[resumo["algoritmo"]] = r.get(resumo["algoritmo"], 0) + 1
        if resumo["assin_lista_ok"]:
            r["lista_ok"] += 1
        else:
            r["lista_falhou"].append(n)
    return os.path.basename(arq), r


if __name__ == "__main__":
    arqs = sorted(glob.glob(os.path.join(PASTA, f"*_2026_{T}t_*.zip")))
    tot = {"turno": T, "pacotes": len(arqs), "urnas": 0, "Ed521": 0, "ECDSA-P521": 0, "lista_ok": 0, "lista_falhou": [], "sem_bloco": 0}
    with ProcessPoolExecutor(int(os.environ.get("NPROC", 12))) as ex:
        for nome, r in ex.map(uf, arqs):
            for k in ("urnas", "Ed521", "ECDSA-P521", "lista_ok", "sem_bloco"):
                tot[k] += r.get(k, 0)
            tot["lista_falhou"] += r["lista_falhou"]
    json.dump(tot, open(os.path.join(AQUI, f"resultado_varrer_chaves_{T}t.json"), "w"), indent=1)
    print({k: (v if not isinstance(v, list) else len(v)) for k, v in tot.items()})
