"""Gera 07_RESPOSTAS_TODAS_AS_PERGUNTAS.md a partir de fase3/respostas_f3.json (respostas já registradas, nenhuma alterada) e acrescenta, por item, independência, cobertura,
validação e próxima evidência decisiva. As perguntas novas desta operação (N1 a N9) vêm de resultados/respostas_novas.json."""
import json
R = "."; OP = R + "/operacao_veracidade"
d = json.load(open(R + "/fase3/respostas_f3.json"))
novas = json.load(open(OP + "/resultados/respostas_novas.json")) if __import__("os").path.exists(OP + "/resultados/respostas_novas.json") else []
INT = "Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)"
EST = "Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados"
ARI = "Aritmética exata sobre totais do TSE"
SIN = "Sintética (simulação; nenhum voto real alterado)"
EXT = "Externa parcial (terceiro preservou ou leu conteúdo do TSE; não é a urna)"
IMP = "Independente na implementação, não na origem (decodificação de terceiro sobre o dado do TSE)"
INDEP = {**{k: INT for k in ["Q1", "Q2", "Q3", "Q4", "Q15", "Q16", "Q17", "Q20", "Q31", "BU1", "A173", "AUT", "P3", "P16"]},
         "Q5": "Interna (lista assinada) + cadeia até a AC emissora (T60a, N1); raiz não pública", "P11": "Interna + cadeia até a AC emissora (T60a, N1); raiz não pública",
         "Q6": EXT, "P4": EXT, "P21": EXT, "Q14": EXT, "Q9": EXT, "R1-20": IMP, "SA22": INT + "; decodificação por leitor próprio", "P6": "Externa (boletins de terceiros): obtida só em T61, N3",
         "Q7": SIN, "P2": SIN, "P18": SIN, "MET": SIN, "P1": SIN, "Q24": ARI, "Q26": ARI, "M1": ARI, "P13": ARI, "P15": ARI, "Q21": ARI, "Q22": ARI, "Q23": ARI}
for k in [f"Q{i}" for i in (8, 10, 11, 12, 13)] + ["C1", "C1a", "C1b", "C2"]: INDEP[k] = "Interna (hora de recebimento registrada pelo próprio TSE) + capturas de terceiro (externa parcial)"
for k in ["Q18", "Q19", "Z1", "P5", "P7", "P8", "P9", "P10", "P14", "P17", "P19", "P20", "Q25", "P12"]: INDEP[k] = EST
for k in [f"Q{i}" for i in range(27, 42)]: INDEP.setdefault(k, EST + "; alegação pública (a origem da pergunta não é fonte)")
INDEP["Q34"] = "Mista: relógio do TSE (interno) e boletins de terceiros (externa parcial, relógio do app não auditado)"
PROX = {"Q5": "AC RAIZ UE e AC URNA v2 obtidas por canal oficial verificável (página do TSE responde HTTP 403 a este ambiente)", "P11": "idem Q5",
        "Q6": "Boletins impressos de amostra probabilística, coletados por fiscais de partidos ou observadores, com lista de seções sorteada antes", "P6": "idem Q6", "P21": "idem Q6",
        "Q7": "Mais mecanismos (UF inteira, região, lote) com poder medido por detector; ver 03_SIMULACOES_ADVERSARIAIS.md", "H9": "Amostra probabilística de boletins impressos ou auditoria independente do software",
        "Q10": "Registro de recebimento do sistema de totalização do TSE e capturas da divulgação com resolução de minutos", "Q12": "idem Q10", "Q13": "idem Q10", "C1": "idem Q10", "C1b": "idem Q10", "C2": "idem Q10",
        "Q11": "idem Q10", "Q18": "Modelo de cauda baixa que passe no critério fixado (nenhum das 3 famílias testadas em T64 passou)", "Q19": "idem Q18", "Z1": "idem Q18",
        "Q24": "Dado individual (inexistente por sigilo) ou pesquisa de painel", "Q26": "idem Q24", "M1": "idem Q24", "P15": "idem Q24", "P1": "idem Q24",
        "Q25": "Covariáveis externas por zona (renda, migração, campanha); fiscalização presencial das zonas citadas", "P14": "idem Q25", "P20": "idem Q25", "P9": "idem Q25",
        "A173": "Segunda via dos 173 arquivos ausentes por canal do TSE", "P3": "Versões datadas dos arquivos (não existem localmente)", "AUT": "Cadeia até a raiz e auditoria do software"}
def proxima(i, cls):
    if i in PROX: return PROX[i]
    if cls.startswith(("Demonstrado", "Refutado")): return "Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)"
    return "Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado"
L = ["# 07. Resposta científica a cada pergunta de todas as fases", "",
     "Fonte: `fase3/respostas_f3.json` (gerado por `fase3/f3_respostas.py`; as respostas anteriores não foram alteradas aqui), com os campos extras abaixo e as perguntas novas desta operação (N1 a N9). Cada item diz o que foi tentado e por que a resposta não é mais forte.", "",
     "Mapa fase → pergunta: Q1 a Q26 e os 33 itens do inventário são da F2 e F3 (V1.1 a V1.3); Q27 a Q39 são da rodada 6 (V1.4); Q40 e Q41 são da rodada 7 (registro vivo); N1 a N9 são desta operação (no site, N9 é a Q42 e N1 a N9 são Q43 a Q50).", ""]
def item(i, perg, resp, estado, evid, cob, val, indep, dem, ndem, votos, prox):
    return [f"### {i}. {perg}", f"- **Resposta direta:** {resp}", f"- **Estado:** {estado}", f"- **Evidência:** {', '.join('`'+e+'`' for e in evid) if evid else '—'}", f"- **Cobertura:** {cob}",
            f"- **Validação:** {val}", f"- **Independência:** {indep}", f"- **O que demonstra:** {dem}", f"- **O que não demonstra:** {ndem}", f"- **Impacto em votos:** {votos}", f"- **Próxima evidência decisiva:** {prox}", ""]
L += ["## Parte A. Perguntas do capítulo de respostas (Q1 a Q41)", ""]
for cap in d["capitulos"]:
    L += [f"### Capítulo: {cap['titulo']}", ""]
    for p in cap["perguntas"]:
        L += item(p["id"], p["pergunta"], p["resposta"], p["classificacao"], p["evidencias"], p["alcance"], p["validacao"], INDEP.get(p["id"], INT), p["demonstra"], p["nao_demonstra"], p["em_votos"], proxima(p["id"], p["classificacao"]))
L += ["## Parte B. Itens do inventário (33)", ""]
for it in d["inventario"]:
    L += item(it["id"], it["pergunta"] or it["id"], it["resposta"], it["classificacao"], it.get("evidencias", []), "ver as perguntas relacionadas: " + (", ".join(it.get("perguntas_relacionadas", [])) or "—"),
              it.get("detalhe") or it["fechamento"], INDEP.get(it["id"], INT), it["resposta"].split("? ", 1)[-1], it.get("limitacao") or "—", it["em_votos"], proxima(it["id"], it["classificacao"]))
L += ["## Parte C. As perguntas desta operação com o rótulo N (mesmo conteúdo das Q42 a Q50 da Parte A; N9 = Q42 e N1 a N8 = Q43 a Q50)", ""]
for n in novas:
    L += item(n["id"], n["pergunta"], n["resposta"], n["estado"], n["evidencia"], n["cobertura"], n["validacao"], n["independencia"], n["demonstra"], n["nao_demonstra"], n["votos"], n["proxima"])
open(OP + "/07_RESPOSTAS_TODAS_AS_PERGUNTAS.md", "w").write("\n".join(L) + "\n")
print(len(L), "linhas;", sum(len(c["perguntas"]) for c in d["capitulos"]), "perguntas Q;", len(d["inventario"]), "itens do inventário;", len(novas), "novas")
