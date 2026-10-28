"""Rodadas do estudo: congela o estado de todos os testes num ponto da linha do tempo, para comparar depois.

Uma rodada é um retrato fixo: cópia do registro de testes e de todos os resultados pequenos (analise/resultado_*.json),
com SHA-256 de cada arquivo, um resumo (placar por classe e por situação) e, em cada teste do registro, uma entrada em
"versoes" com o rótulo da versão (ex.: V1.0, V1.1), situação, classe, evidência, interpretação, versão do método e as
mudanças desde a versão anterior com a causa (dados, código, método, nova evidência, interpretação, redação). Depois de
congelar, o campo "mudancas" do teste é esvaziado: começa a contar de novo. O que muda entre rodadas fica visível teste a teste
(site: página Linha do tempo e gaveta de cada teste). As fases e os marcos ficam em rodadas/linha_do_tempo.json.

Uso:  python scripts/rodada.py fechar 2 V1.0 "Baseline aprovada"  congela a rodada 2 com o rótulo V1.0 (recusa se já existir)
      python scripts/rodada.py comparar 1 2                      lista os testes que mudaram entre duas rodadas
      python scripts/rodada.py prova T02 "tipo" "alvo" "descrição" "resistiu|caiu|ajustado|em_andamento"
                                                                 registra uma prova (contestação) feita a um teste;
                                                                 alvo = evidencia | metodo | interpretacao | redacao | rastreabilidade
"""
import datetime
import glob
import hashlib
import json
import os
import shutil
import sys

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
REG = os.path.join(RAIZ, "testes", "registro.json")
DIR = os.path.join(RAIZ, "rodadas")
CAMPOS = ("situacao", "classe_evidencia", "natureza", "evidencia", "interpretacao", "metodo_versao")


def ler(p):
    return json.load(open(p, encoding="utf-8"))


def gravar(p, d):
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def fechar(n, rotulo, titulo):
    destino = os.path.join(DIR, f"rodada-{n}")
    if os.path.exists(destino):
        sys.exit(f"a rodada {n} já foi fechada ({destino}); rodadas fechadas não se reescrevem")
    hoje = datetime.date.today().isoformat()
    reg = ler(REG)
    os.makedirs(os.path.join(destino, "resultados"))
    arquivos = {}
    for p in sorted(glob.glob(os.path.join(RAIZ, "analise", "resultado_*.json"))):
        alvo = os.path.join(destino, "resultados", os.path.basename(p))
        shutil.copy2(p, alvo)
        arquivos["resultados/" + os.path.basename(p)] = sha(alvo)
    placar = {"testes": len(reg["testes"]), "classes": {}, "situacoes": {}, "natureza": {}}
    for t in reg["testes"]:
        for k, campo in (("classes", "classe_evidencia"), ("situacoes", "situacao"), ("natureza", "natureza")):
            placar[k][t.get(campo)] = placar[k].get(t.get(campo), 0) + 1
        t.setdefault("versoes", []).append({"versao": rotulo, "rodada": n, "data": hoje, **{c: t.get(c) for c in CAMPOS},
                                            "resultado": t.get("resultado_atual"), "mudancas": t.get("mudancas", [])})
        t["mudancas"] = []
        t.setdefault("provas", [])
    gravar(REG, reg)
    gravar(os.path.join(destino, "registro.json"), reg)
    arquivos["registro.json"] = sha(os.path.join(destino, "registro.json"))
    gravar(os.path.join(destino, "resumo.json"), {"rodada": n, "versao": rotulo, "titulo": titulo, "data": hoje, "placar": placar, "arquivos_sha256": arquivos})
    print(f"rodada {n} fechada em {destino}: {len(reg['testes'])} testes, {len(arquivos)} arquivos com SHA-256")


def comparar(a, b):
    ra, rb = (ler(os.path.join(DIR, f"rodada-{x}", "registro.json")) for x in (a, b))
    ta = {t["id"]: t for t in ra["testes"]}
    for t in rb["testes"]:
        v = ta.get(t["id"])
        if v is None:
            print(f"{t['id']}: novo na rodada {b}")
            continue
        mud = [c for c in CAMPOS if c in v and v.get(c) != t.get(c)]
        causas = sorted({m["causa"] for x in t.get("versoes", []) if x["rodada"] == b for m in x.get("mudancas", [])})
        if mud or causas:
            print(f"{t['id']}: mudou {', '.join(mud) or '(só registro)'}" + (f" (classe {v.get('classe_evidencia')} → {t.get('classe_evidencia')})" if "classe_evidencia" in mud else "")
                  + (f"; causas: {', '.join(causas)}" + ("  [mais de uma causa: a mudança não se atribui a uma só]" if len(causas) > 1 else "") if causas else ""))
    for i in set(ta) - {t["id"] for t in rb["testes"]}:
        print(f"{i}: saiu na rodada {b}")


def prova(tid, tipo, alvo, descricao, resultado):
    reg = ler(REG)
    t = next((x for x in reg["testes"] if x["id"] == tid), None)
    if t is None:
        sys.exit(f"teste {tid} não existe no registro")
    if resultado not in ("resistiu", "caiu", "ajustado", "em_andamento"):
        sys.exit("resultado deve ser resistiu, caiu, ajustado ou em_andamento")
    rodadas = [int(os.path.basename(p).split("-")[1]) for p in glob.glob(os.path.join(DIR, "rodada-*"))]
    t.setdefault("provas", []).append({"data": datetime.date.today().isoformat(), "rodada": max(rodadas, default=0) + 1,
                                       "tipo": tipo, "alvo": alvo, "descricao": descricao, "resultado": resultado})
    gravar(REG, reg)
    print(f"prova registrada em {tid}")


if __name__ == "__main__":
    acao = sys.argv[1] if len(sys.argv) > 1 else ""
    if acao == "fechar" and len(sys.argv) >= 5:
        fechar(int(sys.argv[2]), sys.argv[3], sys.argv[4])
    elif acao == "comparar" and len(sys.argv) == 4:
        comparar(int(sys.argv[2]), int(sys.argv[3]))
    elif acao == "prova" and len(sys.argv) == 7:
        prova(*sys.argv[2:7])
    else:
        sys.exit(__doc__)
