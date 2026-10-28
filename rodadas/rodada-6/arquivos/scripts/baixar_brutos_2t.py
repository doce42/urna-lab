"""Baixa os arquivos de cada urna do 2º turno direto do site de resultados do TSE, urna por urna.

Usado só para o que não saiu em pacote por estado (em 27/10/2026: São Paulo). Os outros estados vêm dos pacotes
oficiais (scripts/baixar_lista.sh com dados/listas/brutos_2t_pacotes.txt).

Para cada seção: lê o aux.json (lista o hash e os arquivos daquela urna) e baixa bu.dat, rdv.dat, vota.vsc e log.jez
(os 4 em paralelo). Retoma de onde parou: arquivo que já existe com tamanho > 0 não é baixado de novo.
HTTP/2 multiplexado (poucas conexões, muitos pedidos em cada): o site recusa (429) muitas conexões simultâneas do mesmo
endereço, mas não muitos pedidos numa conexão HTTP/2. Se vier 429, espera a janela renovar (1 s) e tenta de novo.
Saída: dados/brutos/2turno/<UF>/<arquivo>   e   dados/brutos/2turno/aux/<UF>.jsonl (o aux de cada seção)
Uso: python baixar_brutos_2t.py [UF ...]
"""
import asyncio
import json
import os
import sys

import httpx

BASE = "https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221"
AQUI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(AQUI, "..", "dados", "brutos", "2turno")
UFS = sys.argv[1:] or ["SP"]
SECOES_PARALELAS = 48   # cada seção faz até 5 pedidos: ~100-200 pedidos em voo, em 2 conexões HTTP/2
RECUSAS = 0


async def pega(cli, url, tentativas=8):
    global RECUSAS
    t = 0
    while t < tentativas:
        try:
            r = await cli.get(url)
            if r.status_code == 200:
                return r.content
            if r.status_code == 404:
                return None
            if r.status_code == 429:
                RECUSAS += 1
                await asyncio.sleep(float(r.headers.get("x-ratelimit-reset", 1)) + 0.2)
                continue
        except (httpx.HTTPError, asyncio.TimeoutError):
            pass
        await asyncio.sleep(min(2 ** t, 10)); t += 1
    raise RuntimeError(f"falhou: {url}")


async def arquivo(cli, base, h, nome, pasta, erros):
    f = os.path.join(pasta, nome)
    if os.path.exists(f) and os.path.getsize(f) > 0:
        return
    dado = await pega(cli, f"{base}/{h}/{nome}")
    if dado is None:
        erros.append(f"sem arquivo {nome}")
        return
    with open(f + ".tmp", "wb") as o:
        o.write(dado)
    os.replace(f + ".tmp", f)


async def secao(cli, sem, uf, mu, zo, se, pasta, aux_out, erros):
    async with sem:
        try:
            base = f"{BASE}/dados/{uf.lower()}/{mu}/{zo}/{se}"
            aux = await pega(cli, f"{base}/p003221-{uf.lower()}-m{mu}-z{zo}-s{se}-aux.json")
            if aux is None:  # seção agregada: vota na urna de outra seção, não tem arquivos próprios
                erros.append(f"sem aux {uf} {mu} {zo} {se}")
                return
            a = json.loads(aux)
            aux_out.write(json.dumps({"uf": uf, "mu": mu, "zo": zo, "se": se, "aux": a}) + "\n")
            # urna totalizada: o hash com status Totalizado (se houver mais de um envio, fica o último totalizado)
            hs = [h for h in a.get("hashes", []) if h.get("st") == "Totalizado"] or a.get("hashes", [])
            if not hs:
                erros.append(f"sem hash {uf} {mu} {zo} {se}")
                return
            h = hs[-1]
            await asyncio.gather(*(arquivo(cli, base, h["hash"], arq["nm"], pasta, erros) for arq in h["arq"]))
        except Exception as e:  # registra e segue; a próxima execução retoma
            erros.append(f"erro {uf} {mu} {zo} {se}: {e}")


async def main():
    os.makedirs(os.path.join(DEST, "aux"), exist_ok=True)
    limites = httpx.Limits(max_connections=2, max_keepalive_connections=2)
    async with httpx.AsyncClient(http2=True, limits=limites, timeout=httpx.Timeout(120, pool=None)) as cli:
        for uf in UFS:
            cfg = json.loads(await pega(cli, f"{BASE}/config/{uf.lower()}/{uf.lower()}-p003221-cs.json"))
            secoes = [(m["cd"], z["cd"], s["ns"]) for ab in cfg["abr"] for m in ab["mu"] for z in m["zon"] for s in z["sec"]]
            pasta = os.path.join(DEST, uf)
            os.makedirs(pasta, exist_ok=True)
            erros, sem = [], asyncio.Semaphore(SECOES_PARALELAS)
            with open(os.path.join(DEST, "aux", f"{uf}.jsonl"), "w") as aux_out:
                await asyncio.gather(*(secao(cli, sem, uf, *s, pasta, aux_out, erros) for s in secoes))
            agregadas = sum(e.startswith("sem aux") for e in erros)
            print(f"{uf}: {len(secoes)} seções ({agregadas} agregadas, sem urna própria), {len(os.listdir(pasta))} arquivos, "
                  f"{len(erros) - agregadas} problemas, {RECUSAS} recusas 429 acumuladas", flush=True)
            for e in [e for e in erros if not e.startswith("sem aux")][:20]:
                print("   ", e, flush=True)


asyncio.run(main())
print("FIM")
