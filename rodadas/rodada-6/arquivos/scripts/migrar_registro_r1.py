"""Migração única do registro de testes para o formato com versões, e resposta da revisão R1 (Codex) no registro vivo.

Não toca em rodadas/rodada-1/ (o retrato V1.0-rc1 fica como está). Para cada teste:
  - "historico" (formato da rodada 1) vira "versoes": a V1.0-rc1 copiada sem alteração, com commit e manifesto de dados;
  - campos novos do estado atual: metodo_versao, evidencia, interpretacao, pre_especificacao, revisoes (ids dos achados),
    mudancas (o que mudou desde a última versão congelada, com a causa) e provas (as contestações e o resultado);
  - correções de texto e de rastreabilidade motivadas pelos achados da R1, cada uma com causa e origem.
Causas de mudança: dados | codigo | metodo | nova_evidencia | interpretacao | redacao | rastreabilidade.
Uso (uma vez): python scripts/migrar_registro_r1.py
"""
import json
import os

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = os.path.join(R, "testes", "registro.json")
reg = json.load(open(P, encoding="utf-8"))
if any("versoes" in t for t in reg["testes"]):
    raise SystemExit("registro já migrado")
prov = json.load(open(os.path.join(R, "rodadas", "rodada-1", "proveniencia.json"), encoding="utf-8"))
achados = {a["id"]: a for a in json.load(open(os.path.join(R, "revisoes", "R1-codex", "achados.json"), encoding="utf-8"))["achados"]}
HOJE = "2026-10-28"
ANTES_DO_PROTOCOLO = {"T01", "T02", "T03", "T04", "T05", "T07", "T08", "T09", "T10", "T11", "T12", "T13", "T19", "T21", "T22"}

# --- respostas por teste: (achados, mudanças no texto, provas) ---------------------------------------------------------
X = {}


def resp(tid, revisoes, evidencia=None, interpretacao=None, provas=(), mudancas=(), **outros):
    X[tid] = dict(revisoes=list(revisoes), evidencia=evidencia, interpretacao=interpretacao, provas=list(provas), mudancas=list(mudancas), outros=outros)


def pv(achado, alvo, resultado, descricao):
    return {"data": HOJE, "rodada": 2, "tipo": f"revisão independente R1 (Codex), achado {achado}", "alvo": alvo, "resultado": resultado, "descricao": descricao}


def md(campo, causa, origem, justificativa):
    return {"campo": campo, "causa": causa, "origem": origem, "justificativa": justificativa}


INTEG_EVID = ("1º turno 2026: 499.176 urnas eletrônicas com arquivos; hash e assinatura do BU, do log e da lista conferem em todas; RDV no pacote "
              "e conferindo em 499.175, e o que faltava (MA 7846/74/228) baixado do site de resultados e conferido; recontagem do RDV = boletim em 499.176. "
              "2º turno 2026: 499.178 urnas eletrônicas; BU, RDV, imagem do BU e lista conferem em todas; log conferido em 499.177 (1 log de SP na lista "
              "assinada e não publicado); RDV = boletim em 499.180 (inclui recuperação de dados). Seções do exterior por Sistema de Apuração (31 e 29) não "
              "têm arquivos de urna. Verificador Ed521 endurecido em 28/10 (rejeita chaves e pontos degenerados).")
INTEG_INTERP = ("Os arquivos disponíveis são coerentes entre si e com a assinatura apresentada pela própria urna. Isso não autentica a chave: o "
                "certificado não foi validado até uma raiz do TSE (cadeia não publicada no material obtido). Assinaturas também não impedem omissão de "
                "arquivos nem substituição por outro pacote validamente assinado; esses eventos não foram identificados, mas ficam fora do alcance da prova.")
for t in ("T14", "T15", "T16", "T17"):
    resp(t, ["R1-01", "R1-14", "R1-15"] + (["R1-02"] if t == "T16" else []), INTEG_EVID, INTEG_INTERP,
         provas=[pv("R1-01", "interpretacao", "ajustado", "A assinatura demonstra coerência com a chave apresentada pela urna, não autenticidade da chave; a afirmação foi restringida."),
                 pv("R1-15", "redacao", "ajustado", "Log do 2º turno conferido em 499.177 urnas, não em 499.178 (1 não publicado).")]
         + ([pv("R1-02", "metodo", "em_andamento", "Verificador aceitava chave e R degenerados; corrigido e com controles novos. Varredura de todas as chaves reais em andamento.")] if t == "T16" else []),
         mudancas=[md("interpretacao", "interpretacao", "R1-01", "Alcance da assinatura restringido à chave apresentada."), md("evidencia", "redacao", "R1-15", "Universo por tipo de arquivo.")]
         + ([md("metodo_versao", "codigo", "R1-02", "Verificador Ed521 rejeita entradas degeneradas.")] if t == "T16" else []))
resp("T01", ["R1-18"],
     "Seção a seção (versão 2 do método): Boletim de Urna na Web × votação por seção, as duas tabelas públicas do TSE: 3.800.511 pares seção × votável iguais no 1º turno e 1.931.103 no 2º, nenhuma diferença; mesmos conjuntos de seções (499.206 e 499.205).",
     "As duas publicações do TSE são coerentes em cada seção. Ambas vêm do mesmo sistema: é coerência de publicação, não verificação independente da contagem.",
     provas=[pv("R1-18", "metodo", "resistiu", "A versão da rodada 1 só comparava a soma nacional por votável e o texto dizia 'voto a voto'. Refeito seção a seção: nenhuma diferença.")],
     mudancas=[md("metodo_versao", "metodo", "R1-18", "Comparação passou de soma nacional para seção × votável."), md("evidencia", "codigo", "R1-18", "Novo script analise/t01_secao.py.")],
     script="grafico/montar_dados.py, analise/t01_secao.py", comando="python analise/t01_secao.py", saida="analise/resultado_t01_secao.json", metodo_versao=2)
resp("T03", ["R1-07"], None, "Efeito estimado pequeno. O intervalo e o MDE usam o número de seções sem ajuste pela dependência dentro do município, então subestimam a incerteza. Em 2022 o sinal é oposto (−0,028 contra +0,004): não é 'igual', é pequeno nos dois anos.",
     provas=[pv("R1-07", "interpretacao", "ajustado", "'2022 igual' substituído pelos números; incerteza declarada como subestimada."), pv("R1-07", "metodo", "em_andamento", "Intervalo com dependência municipal fica para a Fase 2.")],
     mudancas=[md("interpretacao", "interpretacao", "R1-07", "Comparação 2022 × 2026 quantitativa; limitação do intervalo.")])
resp("T04", ["R1-07"], None, "Não rejeitar a diferença não prova que as urnas trocadas votaram igual. Falta uma margem de equivalência definida antes; o intervalo de 95% e o MDE (α = 0,01) têm funções diferentes.",
     provas=[pv("R1-07", "interpretacao", "ajustado", "'Votaram igual' substituído por estimativa com intervalo."), pv("R1-07", "metodo", "em_andamento", "Teste de equivalência com margem pré-definida na Fase 2.")],
     mudancas=[md("interpretacao", "interpretacao", "R1-07", "Não detecção não é equivalência.")])
resp("T10", ["R1-10"], None, "A curva 'prevista' é reconstrução com informação do próprio 2º turno (virada das outras seções do município e mediana da UF), não previsão ex ante. Uma intervenção comum a um município inteiro pode ser absorvida.",
     provas=[pv("R1-10", "interpretacao", "ajustado", "Deixa de ser apresentada como previsão independente.")], mudancas=[md("interpretacao", "interpretacao", "R1-10", "Natureza retrospectiva do ajuste.")])
resp("T11", ["R1-10"], None, "A permutação nacional dos resíduos não preserva tamanho, heteroscedasticidade nem agrupamento territorial; a contagem de oscilações não é diagnóstico calibrado até isso ser verificado.",
     provas=[pv("R1-10", "metodo", "em_andamento", "Calibração da simulação na Fase 2.")], mudancas=[md("interpretacao", "interpretacao", "R1-10", "Pressupostos da permutação.")])
resp("T13", ["R1-04", "R1-05"], "Grade de 37 cenários em 4 grupos, uma realização cada, deslocamentos sempre a favor do candidato 13: 25 cenários sinalizados por pelo menos um teste; os 3 de troca uniforme nacional, nenhum.",
     "Descreve a grade executada. Não estima probabilidade geral de detecção, e o maior cenário não sinalizado não é limite para alterações possíveis. A referência são os dados reais não modificados, não um mundo sabidamente sem fraude.",
     provas=[pv("R1-04", "interpretacao", "caiu", "A frase 'uma fraude localizada que mudasse o vencedor muito provavelmente apareceria' não é sustentada por 37 realizações de uma grade escolhida pelo analista."),
             pv("R1-05", "redacao", "ajustado", "'Dados reais (sem fraude)' trocado por 'referência não modificada'.")],
     mudancas=[md("evidencia", "redacao", "R1-04", "Descrição exata da grade."), md("interpretacao", "interpretacao", "R1-04", "Retirada a leitura probabilística.")])
resp("T13b", ["R1-05", "R1-04"], "Poder do T28 com conversão sintética (5 repetições por cenário). Na referência não modificada: 0 urnas sinalizadas no 2º turno e 13 no 1º (as mesmas do T28). Com 10% dos votos dos últimos 30 min convertidos, recall ≈ 0%; com 50%, de 18% a 88% conforme turno e fração de urnas; com 100%, de 76% a 98%.",
     "Vale só para o T28 e só para fraude que deixe rastro 'sem biometria'. As sinalizações na referência são achados a explicar, não falsos positivos demonstrados.",
     provas=[pv("R1-05", "redacao", "ajustado", "'Falsos positivos' trocado por 'detecções na referência não modificada'; chave de saída renomeada em poder_logs.py.")],
     mudancas=[md("evidencia", "redacao", "R1-05", "Terminologia.")])
resp("T20", ["R1-07", "R1-17"], None, "Diferença pequena entre modelos de urna, com modelos distribuídos de forma desigual pelo território; não detectar diferença prática não prova equivalência.",
     provas=[pv("R1-17", "rastreabilidade", "ajustado", "Script e comando registrados.")], mudancas=[md("script", "rastreabilidade", "R1-17", "Script real registrado.")],
     script="analise/analise_logs.py", comando="python analise/analise_logs.py 2", saida="analise/resultado_logs_2t.json")
for t in ("T21", "T22"):
    resp(t, ["R1-09"], None, "No 2º turno as participações dos dois candidatos entre os válidos somam 1: os resultados de um determinam os do outro. Não são dois indícios independentes.",
         provas=[pv("R1-09", "interpretacao", "ajustado", "Dependência matemática declarada.")], mudancas=[md("interpretacao", "interpretacao", "R1-09", "Dependência entre candidatos.")])
resp("T23", ["R1-13"], None, "Validação condicionada ao gerador: os resíduos reais do país inteiro calibram o gerador, e o conjunto de teste também define o limiar de 1%. A fração real marcada (0,35%) não estima a fração de irregularidades.",
     provas=[pv("R1-13", "interpretacao", "ajustado", "Alcance do classificador restringido.")], mudancas=[md("interpretacao", "interpretacao", "R1-13", "Reuso de dados na calibração.")])
resp("T26", ["R1-05"], None, "Excluído do veredito por rejeitar nos dois anos e para os dois candidatos. Essa exclusão não confirma os demais testes por contraste; o critério de calibração passa a ser definido antes de olhar os resultados.",
     provas=[pv("R1-05", "metodo", "ajustado", "Regra de exclusão reescrita como critério de calibração prévio.")], mudancas=[md("interpretacao", "interpretacao", "R1-05", "Exclusão não valida os outros testes.")])
resp("T27", ["R1-13"], "Só o comparecimento passou no filtro de execução (mais de mil contagens ≥ 100): p = 0,57 (1º turno) e 0,34 (2º). Brancos e nulos não foram testados.", None,
     provas=[pv("R1-13", "evidencia", "caiu", "A rodada 1 citava dígitos de brancos e nulos; esses não foram executados. Fica só o comparecimento.")],
     mudancas=[md("evidencia", "redacao", "R1-13", "Alcance real da execução.")])
resp("T28", ["R1-05", "R1-11"], None, "As 13 urnas sinalizadas no 1º turno são achados a explicar, não falsos positivos. O teste usa a taxa do resto do dia como parâmetro fixo, sem a incerteza dessa taxa nem a composição do eleitorado por horário.",
     provas=[pv("R1-05", "redacao", "ajustado", "Sinalizações tratadas como achados."), pv("R1-11", "metodo", "em_andamento", "Incluir a incerteza da taxa na Fase 2.")],
     mudancas=[md("interpretacao", "interpretacao", "R1-05", "Terminologia e alcance.")])
resp("T30", ["R1-11"], "0 urnas cujo último evento lido passa do encerramento do BU + 60 s; 1 urna por turno com primeiro voto 2 a 4 min antes da abertura registrada, ambas com urna substituída antes do primeiro voto.",
     "A afirmação sustentada é sobre o último evento lido, com tolerância de 60 s, e depende da ordem e da segmentação do log.",
     provas=[pv("R1-11", "redacao", "ajustado", "'Nenhum voto depois do encerramento' trocado pelo enunciado que o código sustenta.")], mudancas=[md("evidencia", "redacao", "R1-11", "Enunciado exato.")])
resp("T32", ["R1-16"], "638 de 638 itens de voto e comparecimento iguais ao total oficial (BR, 27 UFs e exterior; dois turnos). Eleitorado: 4 diferenças, só no exterior e propagadas ao BR (−495 no 1º turno, −525 no 2º), sem explicação até agora; não são votos.", None,
     provas=[pv("R1-16", "evidencia", "em_andamento", "Diferença de eleitorado do exterior registrada; causa a investigar.")], mudancas=[md("evidencia", "redacao", "R1-16", "Eleitorado incluído no resultado.")])
resp("T33", ["R1-11"], None, "Observa-se a mesma versão textual do software declarada nos logs de todas as urnas. Isso não demonstra que o binário executado seja o mesmo nem que a autoverificação seja eficaz.",
     provas=[pv("R1-11", "interpretacao", "ajustado", "'O software foi o mesmo' trocado por 'mesma versão declarada no log'.")], mudancas=[md("interpretacao", "interpretacao", "R1-11", "Alcance.")])
resp("T34", ["R1-17"], None, None, provas=[pv("R1-17", "rastreabilidade", "ajustado", "Script e comando registrados.")], mudancas=[md("script", "rastreabilidade", "R1-17", "Script real registrado.")],
     script="analise/correspondencia.py", comando="python analise/correspondencia.py 2", saida="analise/resultado_correspondencia_{1,2}t.json")
resp("T35", ["R1-11", "R1-17"], "Máquinas de geração de mídia com log do GEDAI publicado: 2.450 de 2.453 (1º turno) e 2.477 de 2.479 (2º); versão 8.23 e fase OFICIAL nos logs lidos.",
     "Verifica a disponibilidade do log por máquina, não reconcilia cada carga de urna (código, data, seção). As máquinas sem log são ausência de dado.",
     provas=[pv("R1-11", "evidencia", "ajustado", "Incluídas as 2 máquinas sem log do 2º turno, que faltavam no texto; alcance restringido.")],
     mudancas=[md("evidencia", "redacao", "R1-11", "2º turno incluído."), md("script", "rastreabilidade", "R1-17", "Script real registrado.")],
     script="analise/correspondencia.py", comando="python analise/correspondencia.py 1", saida="analise/resultado_correspondencia_{1,2}t.json")
resp("T36", ["R1-12", "R1-15"], "1º turno: 186 casos — 38 declarados pelo TSE (CEFT), 5 com evento compatível no log, 142 inferidos (uma confirmação sem voto computado) e 1 sem explicação (RJ 60011/8/61, log corrompido pela urna). 2º turno: 75 casos — 1 demonstrado (D1: log de SP na lista assinada e não publicado), 30 declarados, 3 compatíveis, 41 inferidos, 0 sem explicação.",
     "Os totais gravados conferem; as causas operacionais têm graus diferentes de demonstração e a maioria é inferência a partir da contagem.",
     provas=[pv("R1-12", "interpretacao", "ajustado", "'Explicado' desdobrado em graus (demonstrado, declarado, compatível, inferido); a maioria é inferência.")],
     mudancas=[md("evidencia", "codigo", "R1-12", "casos_integridade.py grava o grau de cada caso."), md("interpretacao", "interpretacao", "R1-12", "Graus de demonstração.")], metodo_versao=2)
resp("C06", ["R1-06"], None, "'Abstencionistas do 1º turno foram 4:1 para Lula' é estimativa sob o pressuposto de taxas homogêneas dentro de cada UF; reproduzir os totais não valida os fluxos. A faixa entre UFs é heterogeneidade geográfica, não intervalo de confiança. A função com efeito fixo municipal existe no código mas não é a usada.",
     provas=[pv("R1-06", "interpretacao", "ajustado", "Estimativa sempre apresentada como condicionada ao modelo."), pv("R1-06", "metodo", "em_andamento", "Desafio adversarial do C06 na Fase 2 (pergunta P1).")],
     mudancas=[md("interpretacao", "interpretacao", "R1-06", "Identificação ecológica.")])
resp("C06b", ["R1-17", "R1-06"], None, None, provas=[pv("R1-17", "rastreabilidade", "em_andamento", "O cálculo ainda não está num script; incorporar na Fase 2.")], mudancas=[])
for t in ("E01", "E02", "E03"):
    resp(t, ["R1-08", "R1-17"], None,
         "Mede agrupamento por local de votação, não autocorrelação espacial (Moran's I, citado no protocolo, não foi implementado). Os p-valores supõem independência entre seções do mesmo local; com correlação positiva ficam otimistas. 2022 e 2026 usam modelos diferentes (perfil só em 2026)." if t == "E02" else None,
         provas=[pv("R1-17", "rastreabilidade", "ajustado", "Script e comando registrados.")] + ([pv("R1-08", "metodo", "em_andamento", "Calibrar sob correlação intralocal e comparar anos com o mesmo modelo, na Fase 2.")] if t == "E02" else []),
         mudancas=[md("script", "rastreabilidade", "R1-17", "Script real registrado.")] + ([md("interpretacao", "interpretacao", "R1-08", "O que o teste mede.")] if t == "E02" else []),
         script="analise/divergencias.py", comando="python analise/divergencias.py 2026 completo", saida="analise/resultado_divergencias_<ano>_completo.json")
resp("T17b", ["R1-17"], None, None, provas=[pv("R1-17", "rastreabilidade", "ajustado", "Script e comando registrados.")], mudancas=[md("script", "rastreabilidade", "R1-17", "Script real registrado.")],
     script="analise/processar_brutos.py", comando="ANO=2026 python analise/processar_brutos.py 2", saida="analise/brutos/<t>t/urnas_<UF>.parquet")
for t in ANTES_DO_PROTOCOLO:
    X.setdefault(t, dict(revisoes=[], evidencia=None, interpretacao=None, provas=[], mudancas=[], outros={}))
    X[t]["revisoes"] = sorted(set(X[t]["revisoes"]) | {"R1-13"})
    X[t]["mudancas"].append(md("pre_especificacao", "rastreabilidade", "R1-13", "Executado antes do protocolo (19h55 de 27/10): não é pré-registrado."))

# --- migração -----------------------------------------------------------------------------------------------------------
for t in reg["testes"]:
    hist = t.pop("historico", [])
    t["versoes"] = [{"versao": "V1.0-rc1", "rodada": h["rodada"], "data": h["data"], "git_tag": prov["git"]["tag"], "commit": prov["git"]["commit"],
                     "manifesto_dados_sha256": prov["dados"]["manifesto_sha256"], "metodo_versao": 1, "situacao": h["situacao"],
                     "classe_evidencia": h["classe_evidencia"], "natureza": h["natureza"], "resultado": h["resultado_atual"],
                     "nota": "na V1.0-rc1 evidência, interpretação e conclusão estavam juntas no campo 'resultado'"} for h in hist]
    x = X.get(t["id"], {})
    t["metodo_versao"] = x.get("outros", {}).get("metodo_versao", 1)
    t["pre_especificacao"] = "anterior_ao_protocolo" if t["id"] in ANTES_DO_PROTOCOLO else "protocolo_ou_emenda"
    t["evidencia"] = x.get("evidencia") or t["resultado_atual"]
    t["interpretacao"] = x.get("interpretacao")
    t["revisoes"] = x.get("revisoes", [])
    t["mudancas"] = x.get("mudancas", [])
    t["provas"] = t.get("provas", []) + x.get("provas", [])
    for k in ("script", "comando", "saida"):
        if x.get("outros", {}).get(k):
            t[k] = x["outros"][k]
    if x.get("evidencia"):
        t["resultado_atual"] = x["evidencia"]
    for a in t["revisoes"]:
        if a not in achados:
            raise SystemExit(f"{t['id']}: achado {a} não existe")
json.dump(reg, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"migrados {len(reg['testes'])} testes; {sum(bool(t['revisoes']) for t in reg['testes'])} com achados da R1; "
      f"{sum(len(t['provas']) for t in reg['testes'])} provas registradas")
