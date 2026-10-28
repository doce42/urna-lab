"""Controles da implementação Ed521 (analise/ed521.py) com arquivos reais de urnas (pacote do Acre, 1º turno).
Positivos: assinatura legítima com a chave da própria urna → válida.
Negativos: (1) 1 bit da assinatura alterado; (2) 1 bit do hash alterado; (3) chave de OUTRA urna; (4) mensagem aleatória;
(5) assinatura de outro arquivo da mesma urna. Todos têm que falhar. Também roda os mesmos controles no ECDSA (UE2013/2015).
Uso: python analise/controles/ed521_controles.py [n_urnas]
"""
import base64
import glob
import os
import random
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, ".."))
import der  # noqa: E402
import ed521  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
random.seed(2026)
z = zipfile.ZipFile(glob.glob(os.path.join(AQUI, "..", "..", "dados", "brutos", "1turno", "*_1t_AC.zip"))[0])
vscs = [n for n in z.namelist() if n.endswith("vota.vsc")]
random.shuffle(vscs)
amostra = []
for n in vscs:
    v, _ = der.ler(z.read(n))
    ue = next(b for b in v["f"] if b["k"] and len(b["f"]) >= 5 and b["f"][2]["k"] and b["f"][2]["f"][0]["f"][0]["v"][:4].upper() == b"UEAO")
    cert = ue["f"][4]["v"]
    if not cert.startswith(b"-----BEGIN"):
        continue  # este controle é do Ed521 (UE2020/2022)
    c, _ = der.ler(base64.b64decode(b"".join(l for l in cert.splitlines() if not l.startswith(b"-"))))
    pub = c["f"][0]["f"][6]["f"][1]["v"][1:]
    lista, _ = der.ler(ue["f"][3]["v"])
    itens = [(i["f"][1]["f"][1]["v"], i["f"][1]["f"][2]["v"]) for i in lista["f"][0]["f"]]
    amostra.append((pub, itens))
    if len(amostra) >= N:
        break
flip = lambda b, k: bytes(x ^ (1 if j == k else 0) for j, x in enumerate(b))
res = {"positivo": 0, "bit_assinatura": 0, "bit_hash": 0, "chave_de_outra_urna": 0, "mensagem_aleatoria": 0, "assinatura_de_outro_arquivo": 0}
for k, (pub, itens) in enumerate(amostra):
    h, s = itens[0]
    res["positivo"] += ed521.verifica(pub, s, h)
    res["bit_assinatura"] += ed521.verifica(pub, flip(s, random.randrange(132)), h)
    res["bit_hash"] += ed521.verifica(pub, s, flip(h, random.randrange(64)))
    res["chave_de_outra_urna"] += ed521.verifica(amostra[(k + 1) % len(amostra)][0], s, h)
    res["mensagem_aleatoria"] += ed521.verifica(pub, s, os.urandom(64))
    res["assinatura_de_outro_arquivo"] += ed521.verifica(pub, itens[1][1], h)
print(f"urnas testadas (Ed521): {len(amostra)}")
for k, v in res.items():
    esperado = len(amostra) if k == "positivo" else 0
    print(f"  {k:28} válidas: {v:4}  (esperado {esperado})  {'OK' if v == esperado else 'FALHOU'}")

# controles de entradas degeneradas (revisão R1, achado R1-02): têm que falhar todos
I = (1).to_bytes(66, "little")  # identidade (0, 1)
h0 = os.urandom(64)
degenerados = {"chave_e_R_identidade_S_zero": ed521.verifica(I, I + bytes(66), h0), "chave_vazia": ed521.verifica(b"", I + bytes(66), h0),
               "chave_curta": ed521.verifica(I[:65], I + bytes(66), h0), "assinatura_curta": ed521.verifica(amostra[0][0], bytes(131), h0) if amostra else False}
for k, v in degenerados.items():
    print(f"  {k:28} aceita: {v}  (esperado False)  {'OK' if not v else 'FALHOU'}")
