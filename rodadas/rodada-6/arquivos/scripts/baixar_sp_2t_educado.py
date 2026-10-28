"""Baixa os arquivos das urnas de São Paulo no 2º turno respeitando o limite do site de resultados do TSE.

O site devolve 429 quando um endereço pede rápido demais. Este downloader controla a taxa (pedidos por segundo):
sobe devagar enquanto não há recusa e corta pela metade (com pausa) a cada recusa — o mesmo controle de
congestionamento do TCP (AIMD). Retoma de onde parou: índices em dados/brutos/2turno/aux_sp, arquivos em
dados/brutos/2turno/SP. Para quando não falta nada; seções agregadas (índice 404) não têm urna própria.

Enquanto roda, confere a cada 10 minutos se o TSE publicou o pacote oficial de SP; se sim, para e avisa.
"""
import asyncio
import json
import os
import time

import httpx

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
B = "https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221"
A = f"{P}/dados/brutos/2turno/aux_sp"
D = f"{P}/dados/brutos/2turno/SP"
PACOTE = "https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/arqurnatot/bu_imgbu_logjez_rdv_vscmr_2026_2t_SP.zip"


class Ritmo:
    def __init__(self, inicial=5.0, minimo=1.0, maximo=200.0):
        self.taxa, self.minimo, self.maximo = inicial, minimo, maximo
        self.proximo = time.monotonic()
        self.pausa_ate = 0.0
        self.ok = self.recusas = 0

    async def vez(self):
        while True:
            agora = time.monotonic()
            espera = max(self.proximo, self.pausa_ate) - agora
            if espera <= 0:
                self.proximo = max(self.proximo, agora) + 1.0 / self.taxa
                return
            await asyncio.sleep(espera)

    def sucesso(self):
        self.ok += 1
        self.seguidas = 0
        self.taxa = min(self.maximo, self.taxa + 1.0 / self.taxa)  # +1 pedido/s a cada ~taxa sucessos (~1 s)

    def recusa(self):
        # recusas seguidas = o site está punindo o endereço: espera cada vez mais (15 s, 30 s, ... até 5 min),
        # porque continuar pedindo só prolonga a punição
        self.recusas += 1
        self.seguidas = getattr(self, "seguidas", 0) + 1
        self.taxa = max(self.minimo, self.taxa / 2)
        espera = 5 if self.seguidas < 3 else min(300, 15 * 2 ** (self.seguidas - 3))
        self.pausa_ate = max(self.pausa_ate, time.monotonic() + espera)


async def pega(cli, ritmo, url):
    for _ in range(30):
        await ritmo.vez()
        try:
            r = await cli.get(url)
        except httpx.HTTPError:
            await asyncio.sleep(2)
            continue
        if r.status_code == 200:
            ritmo.sucesso()
            return r.content
        if r.status_code == 404:
            ritmo.sucesso()
            return None
        if r.status_code == 429:
            ritmo.recusa()
            continue
        await asyncio.sleep(2)
    raise RuntimeError(f"desisti: {url}")


def grava(caminho, dado):
    with open(caminho + ".tmp", "wb") as o:
        o.write(dado)
    os.replace(caminho + ".tmp", caminho)


async def trabalhador(cli, ritmo, fila, pend, stats):
    while True:
        item = await fila.get()
        try:
            tipo, mu, zo, se, extra = item
            base = f"{B}/dados/sp/{mu}/{zo}/{se}"
            if tipo == "aux":
                nome = f"p003221-sp-m{mu}-z{zo}-s{se}-aux.json"
                dado = await pega(cli, ritmo, f"{base}/{nome}")
                if dado is None:
                    stats["agregadas"] += 1
                else:
                    grava(f"{A}/{nome}", dado)
                    for arq in arquivos_do_aux(json.loads(dado)):
                        await fila.put(("arq", mu, zo, se, arq))
                        pend[0] += 1
            else:
                h, nm = extra
                if not os.path.exists(f"{D}/{nm}"):
                    dado = await pega(cli, ritmo, f"{base}/{h}/{nm}")
                    if dado is None:
                        stats["sem_arquivo"] += 1
                    else:
                        grava(f"{D}/{nm}", dado)
                        stats["arquivos"] += 1
        except Exception as e:
            stats["erros"] += 1
            stats["ultimo_erro"] = str(e)[:200]
        finally:
            pend[0] -= 1
            fila.task_done()


def arquivos_do_aux(a):
    hs = [h for h in a.get("hashes", []) if h.get("st") == "Totalizado"] or a.get("hashes", [])
    if not hs:
        return []
    h = hs[-1]
    return [(h["hash"], x["nm"]) for x in h["arq"] if not os.path.exists(f"{D}/{x['nm']}")]


async def relatorio(ritmo, pend, stats, cli):
    ultimo_pacote = 0
    while pend[0] > 0:
        await asyncio.sleep(30)
        print(f"{time.strftime('%T')} taxa {ritmo.taxa:5.1f}/s | ok {ritmo.ok} | recusas {ritmo.recusas} | "
              f"pendentes {pend[0]} | arquivos novos {stats['arquivos']} | agregadas {stats['agregadas']} | erros {stats['erros']}", flush=True)
        if time.monotonic() - ultimo_pacote > 600:
            ultimo_pacote = time.monotonic()
            try:
                r = await cli.head(PACOTE)
                if r.status_code == 200:
                    print("PACOTE_SP_PUBLICADO", flush=True)
            except httpx.HTTPError:
                pass


async def main():
    os.makedirs(A, exist_ok=True); os.makedirs(D, exist_ok=True)
    async with httpx.AsyncClient(http2=True, timeout=60, limits=httpx.Limits(max_connections=2)) as cli:
        ritmo = Ritmo()
        cs = json.loads(await pega(cli, ritmo, f"{B}/config/sp/sp-p003221-cs.json"))
        fila, pend = asyncio.Queue(), [0]
        stats = {"arquivos": 0, "agregadas": 0, "sem_arquivo": 0, "erros": 0}
        for ab in cs["abr"]:
            for m in ab["mu"]:
                for z in m["zon"]:
                    for s in z["sec"]:
                        nome = f"{A}/p003221-sp-m{m['cd']}-z{z['cd']}-s{s['ns']}-aux.json"
                        if os.path.exists(nome):
                            for arq in arquivos_do_aux(json.load(open(nome))):
                                fila.put_nowait(("arq", m["cd"], z["cd"], s["ns"], arq)); pend[0] += 1
                        else:
                            fila.put_nowait(("aux", m["cd"], z["cd"], s["ns"], None)); pend[0] += 1
        print(f"início {time.strftime('%T')}: {pend[0]} pedidos na fila", flush=True)
        trab = [asyncio.create_task(trabalhador(cli, ritmo, fila, pend, stats)) for _ in range(64)]
        await asyncio.gather(fila.join(), relatorio(ritmo, pend, stats, cli))
        for t in trab:
            t.cancel()
        print(f"FIM_SP {time.strftime('%T')} arquivos novos {stats['arquivos']} agregadas {stats['agregadas']} "
              f"sem_arquivo {stats['sem_arquivo']} erros {stats['erros']} {stats.get('ultimo_erro', '')}", flush=True)


asyncio.run(main())
