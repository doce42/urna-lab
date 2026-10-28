"""T32: soma das urnas (Boletim de Urna) x totais oficiais divulgados pelo site de resultados do TSE (BR, UFs e exterior).

Os arquivos oficiais ficam em dados/totais_oficiais/ (baixados um a um, com pausa, para não pesar no site).
Compara votos de cada candidato, brancos, nulos e comparecimento.
"""
import json
import os
import time
import urllib.request

import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(AQUI, "..", "dados", "totais_oficiais")
os.makedirs(DEST, exist_ok=True)
B = "https://resultados.tse.jus.br/oficial/ele2026"
ABR = ["br"] + "ac al am ap ba ce df es go ma mg ms mt pa pb pe pi pr rj rn ro rr rs sc se sp to zz".split()
ELE = {1: "6257", 2: "6258"}


def baixa(turno, ab):
    f = os.path.join(DEST, f"{ab}-e00{ELE[turno]}-u.json")
    if not os.path.exists(f):
        url = f"{B}/{ELE[turno]}/dados/{ab}/{ab}-c0001-e00{ELE[turno]}-u.json"
        for tentativa in range(6):
            try:
                with urllib.request.urlopen(url, timeout=60) as r:
                    open(f, "wb").write(r.read())
                break
            except Exception:
                time.sleep(5 * (tentativa + 1))
        time.sleep(0.5)
    return json.load(open(f))


def oficial(d):
    """Votos por candidato (número), brancos, nulos, comparecimento, do arquivo oficial."""
    out = {}
    for ag in d["carg"][0].get("agr", []):
        for par in ag.get("par", []):
            for c in par.get("cand", []):
                out["v" + c["n"]] = int(c["vap"])
    v, e = d.get("v", {}), d.get("e", {})
    out["branco"] = int(v["vb"])
    out["nulo"] = int(v["vn"])
    # votos em candidato com registro indeferido/anulado: o TSE não os conta como válidos (nulos técnicos, anulados, sub judice)
    out["votos_candidato_invalido"] = int(v.get("vnt", 0)) + int(v.get("van", 0)) + int(v.get("vansj", 0))
    out["comparecimento"] = int(e["c"])
    out["eleitorado"] = int(e["te"])
    out["_v"] = v
    return out


b = pd.read_parquet(os.path.join(AQUI, "base.parquet"))
linhas = []
for turno in (1, 2):
    for ab in ABR:
        d = baixa(turno, ab)
        of = oficial(d)
        x = b if ab == "br" else b[b["SG_UF"] == ab.upper()]
        x = x[x[f"total_{turno}"].notna()]
        soma = {c.rsplit("_", 1)[0]: int(x[c].sum()) for c in x.columns
                if c.endswith(f"_{turno}") and (c.startswith("v") and c != f"validos_{turno}" or c in (f"branco_{turno}", f"nulo_{turno}"))}
        soma["comparecimento"] = int(x[f"QT_COMPARECIMENTO_{turno}"].sum())
        soma["eleitorado"] = int(x[f"QT_APTOS_{turno}"].sum())
        # candidatos que estão nas urnas mas não na lista oficial de candidatos válidos
        invalidos = [k for k in list(soma) if k.startswith("v") and k not in of]
        soma["votos_candidato_invalido"] = sum(soma.pop(k) for k in invalidos)
        for k in sorted(set(soma) | {k for k in of if not k.startswith("_")}):
            if k.startswith("_"):
                continue
            linhas.append({"turno": turno, "abrangencia": ab.upper(), "item": k, "soma_urnas": soma.get(k), "oficial": of.get(k),
                           "igual": soma.get(k) == of.get(k)})
t = pd.DataFrame(linhas)
t.to_csv(os.path.join(AQUI, "resultado_totalizacao.csv"), sep=";", index=False)
print("comparações:", len(t), "| iguais:", int(t["igual"].sum()))
print(t[~t["igual"]].head(30).to_string())
print("chaves do bloco 'v' do arquivo oficial (BR):", list(of["_v"].keys())[:40])
