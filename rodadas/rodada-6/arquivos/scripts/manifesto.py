"""Manifesto de proveniência (DIRETRIZ, nível 1): SHA-256 de todos os arquivos de dados oficiais baixados.

Saída: dados/listas/MANIFESTO.csv com caminho, tamanho, data de modificação (do arquivo, não do download), SHA-256,
situação do hash oficial do TSE e a URL de origem (pelo nome do arquivo nas listas dados/listas/*.txt).
hash_oficial (revisão R1, achado R1-03), lida das linhas "ok hash" / "ok sem-hash" / "HASH ERRADO" dos logs de download:
  conferido | nao_publicado_pelo_tse | errado_rebaixado | sem_registro_de_download. A coluna antiga sha512_oficial_conferido
  (existência da marca .ok) foi retirada: ela ficava verdadeira também quando o TSE não publicava hash.
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
import re  # noqa: E402
hash_oficial = {}
for log in glob.glob(os.path.join(DADOS, "listas", "*.log")):
    for l in open(log, errors="ignore"):
        m = re.match(r"(ok hash|ok sem-hash|HASH ERRADO) (\S+)", l.strip())
        if m and hash_oficial.get(m.group(2)) != "conferido":
            hash_oficial[m.group(2)] = {"ok hash": "conferido", "ok sem-hash": "nao_publicado_pelo_tse", "HASH ERRADO": "errado_rebaixado"}[m.group(1)]
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
            "hash_oficial": hash_oficial.get(n, "sem_registro_de_download"), "url_origem": urls.get(n, "")}


with ThreadPoolExecutor(4) as ex:
    linhas = list(ex.map(linha, sorted(arquivos)))
destino = os.path.join(DADOS, "listas", "MANIFESTO.csv")
with open(destino, "w", newline="") as o:
    w = csv.DictWriter(o, fieldnames=list(linhas[0]))
    w.writeheader()
    w.writerows(linhas)
print(f"{len(linhas)} arquivos, {sum(l['bytes'] for l in linhas) / 1e9:.1f} GB → {destino}")
