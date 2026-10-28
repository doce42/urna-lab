"""Gera as listas de download (dados/listas/*.txt) a partir do portal de dados abertos do TSE, para reproduzir o estudo do zero.

Armadilhas tratadas: o portal às vezes lista o .sha512 no lugar do zip (usa-se o endereço sem .sha512) e não lista
pacotes que já estão no CDN (arquivos das urnas do 2º turno de 2026: endereço montado direto).
Uso: python scripts/listas_tse.py
"""
import json
import os
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
L = os.path.join(AQUI, "..", "dados", "listas")
os.makedirs(L, exist_ok=True)
UFS = "AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO ZZ".split()
CDN = "https://cdn.tse.jus.br/estatistica/sead"


def busca(q):
    url = "https://dadosabertos.tse.jus.br/api/3/action/package_search?rows=50&q=" + urllib.parse.quote(q)
    return json.load(urllib.request.urlopen(url, timeout=60))["result"]["results"]


def zips(titulo_contem, filtro):
    s = set()
    for p in busca(titulo_contem):
        for r in p["resources"]:
            u = r["url"].removesuffix(".sha512")
            if u.endswith(".zip") and filtro(u):
                s.add(u)
    return sorted(s)


def grava(nome, urls):
    open(os.path.join(L, nome), "w").write("\n".join(urls) + "\n")
    print(f"{nome}: {len(urls)}")


grava("votacao_secao.txt", [f"{CDN}/odsele/votacao_secao/votacao_secao_{a}_BR.zip" for a in (2026, 2022)])
grava("bweb_2026.txt", zips("2026 Boletim de Urna", lambda u: "/eleicoes2026/buweb/bweb_" in u))
grava("bweb_2022.txt", zips("2022 Boletim de Urna", lambda u: "/eleicoes2022/buweb/bweb_" in u)
      + [f"{CDN}/odsele/votacao_secao/votacao_secao_2022_BR.zip"])
grava("perfil_2026.txt", [f"{CDN}/odsele/perfil_eleitor_secao/perfil_eleitor_secao_2026_{u}.zip" for u in UFS])
grava("brutos_1t.txt", [f"{CDN}/eleicoes/eleicoes2026/arqurnatot/bu_imgbu_logjez_rdv_vscmr_2026_1t_{u}.zip" for u in UFS])
# 2º turno: pacote por UF no CDN (SP pode não existir; nesse caso usar scripts/baixar_sp_2t_educado.py)
grava("brutos_2t_pacotes.txt", [f"{CDN}/eleicoes/eleicoes2026/arqurnatot/bu_imgbu_logjez_rdv_vscmr_2026_2t_{u}.zip" for u in UFS])
# 2022: arquivos brutos das urnas e perfil do eleitorado (para a comparação ser simétrica)
for t in ("1t", "2t"):
    grava(f"brutos_2022_{t}.txt", [f"{CDN}/eleicoes/eleicoes2022/arqurnatot/bu_imgbu_logjez_rdv_vscmr_2022_{t}_{u}.zip" for u in UFS])
grava("perfil_2022.txt", [f"{CDN}/odsele/perfil_eleitor_secao/perfil_eleitor_secao_2022_{u}.zip" for u in UFS])
grava("corresp_gedai_2026.txt", zips("Correspondências esperadas 2026", lambda u: "2026" in u)
      + zips("Gedai 2026", lambda u: "2026" in u))
