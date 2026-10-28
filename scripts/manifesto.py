"""Manifesto de proveniência (DIRETRIZ, nível 1): SHA-256 de todos os arquivos de dados oficiais baixados.

Saída: dados/listas/MANIFESTO.csv com caminho, tamanho, data de modificação, SHA-256, se o .sha512 oficial do TSE foi
conferido (marca .ok do baixar_lista.sh) e a URL de origem (pelo nome do arquivo nas listas dados/listas/*.txt).
Pula as pastas de arquivos soltos (urna a urna) e temporários. Roda com 4 threads; use nice/ionice.
Uso: python scripts/manifesto.py
"""
import csv
import glob
import hashlib
import os
import time
from concurrent.futures import ThreadPoolExecutor

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DADOS = os.path.join(RAIZ, "dados")
EXCLUIR = {"aux", "aux_sp", "SP_parcial_urna_a_urna", "listas", "sp_tmp"}
urls = {}
for lista in glob.glob(os.path.join(DADOS, "listas", "*.txt")):
    for u in open(lista).read().split():
        urls.setdefault(os.path.basename(u.removesuffix(".sha512")), u.removesuffix(".sha512"))
arquivos = []
for pasta, dirs, nomes in os.walk(DADOS):
    dirs[:] = [d for d in dirs if d not in EXCLUIR]
    for n in nomes:
        if n.endswith((".tmp", ".ok", ".ruim")) or ".parte" in n:
            continue
        arquivos.append(os.path.join(pasta, n))


def sha(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def linha(caminho):
    st = os.stat(caminho)
    n = os.path.basename(caminho)
    return {"caminho": os.path.relpath(caminho, DADOS), "bytes": st.st_size,
            "modificado": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)), "sha256": sha(caminho),
            "sha512_oficial_conferido": os.path.exists(caminho + ".ok"), "url_origem": urls.get(n, "")}


with ThreadPoolExecutor(4) as ex:
    linhas = list(ex.map(linha, sorted(arquivos)))
destino = os.path.join(DADOS, "listas", "MANIFESTO.csv")
with open(destino, "w", newline="") as o:
    w = csv.DictWriter(o, fieldnames=list(linhas[0]))
    w.writeheader()
    w.writerows(linhas)
print(f"{len(linhas)} arquivos, {sum(l['bytes'] for l in linhas) / 1e9:.1f} GB → {destino}")
