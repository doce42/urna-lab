"""Rodada 7 (T58, T59): extrai do RDV os votos brancos e nulos (com o número digitado) de presidente e governador, por seção,
e os números com voto nominal para governador por UF. Pré-registro em fase3/PREREG_RDV_NULOS.md.
Uso: rdv_nulos.py <ano> <turno> [processos]   →   fase3/resultados/rdv_nulos_<ano>_<turno>t.parquet e ..._gov.json"""
import collections, json, os, re, sys, zipfile
from concurrent.futures import ProcessPoolExecutor
import pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, RAIZ + "/analise")
import der  # noqa: E402

ANO, TURNO = sys.argv[1], int(sys.argv[2]); PROC = int(sys.argv[3]) if len(sys.argv) > 3 else 12
BRUTOS = RAIZ + ("/dados/brutos" if ANO == "2026" else f"/dados/{ANO}/brutos")
ELEICOES = {"2026": {1: (6257, 6259), 2: (6258, 6260)}, "2022": {1: (544, 546), 2: (545, 547)}}[ANO][TURNO]  # (federal, estadual)
UFS = "AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO ZZ".split()
NOME_2026 = re.compile(r"o\d{5}([a-z]{2})(\d{5})(\d{4})(\d{4})-rdv\.dat$")
NOME_2022 = re.compile(r"o00\d{3}-(\d{5})(\d{4})(\d{4})\.rdv$")
OUT = f"{RAIZ}/fase3/resultados/rdv_nulos_{ANO}_{TURNO}t"


def chave(n, uf):
    if ANO == "2022":
        m = NOME_2022.search(n)
        return m and (uf, str(int(m.group(1))), str(int(m.group(2))), str(int(m.group(3))))
    m = NOME_2026.search(n)
    return m and (m.group(1).upper(), str(int(m.group(2))), str(int(m.group(3))), str(int(m.group(4))))


def fontes(uf):
    pasta = ("1turno" if TURNO == 1 else "2turno_pacotes") if ANO == "2026" else f"{TURNO}turno"
    pac = f"{BRUTOS}/{pasta}/bu_imgbu_logjez_rdv_vscmr_{ANO}_{TURNO}t_{uf}.zip"
    if os.path.exists(pac):
        z = zipfile.ZipFile(pac)
        return [(n, z.read) for n in z.namelist() if n.endswith((".rdv", "-rdv.dat"))]
    d = f"{BRUTOS}/2turno/{uf}"
    if ANO == "2026" and TURNO == 2 and os.path.isdir(d):
        return [(n, lambda n, d=d: open(f"{d}/{n}", "rb").read()) for n in os.listdir(d) if n.endswith("-rdv.dat")]
    return []


def uf_job(uf):
    linhas = collections.Counter(); gov = collections.Counter(); erros = 0
    for n, ler in fontes(uf):
        k = chave(n, uf)
        if not k:
            continue
        try:
            raiz, _ = der.ler(ler(n)); corpo = raiz["f"][2]
            for ele in corpo["f"][3 if ANO == "2022" else 4]["f"]:
                eid = int.from_bytes(ele["f"][0]["v"], "big")
                if eid not in ELEICOES:
                    continue
                for cargo in ele["f"][1]["f"]:
                    c = int.from_bytes(cargo["f"][0]["v"], "big")
                    if c not in (1, 3):           # 1 presidente, 3 governador
                        continue
                    for v in cargo["f"][2]["f"]:
                        t = int.from_bytes(v["f"][0]["v"], "big")
                        dig = v["f"][1]["v"].decode() if len(v["f"]) > 1 else ""
                        if t == 2:
                            if c == 3:
                                gov[dig] += 1
                            continue
                        linhas[k + (c, t, dig)] += 1
        except Exception:
            erros += 1
    return uf, linhas, gov, erros


if __name__ == "__main__":
    rows, govs, err = [], {}, {}
    with ProcessPoolExecutor(PROC) as ex:
        for uf, linhas, gov, erros in ex.map(uf_job, UFS):
            rows += [(*k, q) for k, q in linhas.items()]; govs[uf] = dict(gov); err[uf] = erros
            print(uf, len(linhas), erros, flush=True)
    df = pd.DataFrame(rows, columns=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "cargo", "tipo", "digitos", "n"])
    df.to_parquet(OUT + ".parquet", index=False)
    json.dump({"governador_nominal_por_uf": govs, "erros_leitura": err}, open(OUT + "_gov.json", "w"))
    print("ok", len(df))
