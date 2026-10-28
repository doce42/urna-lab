"""Veredito de 2026 (fonte única): pergunta central, dedução, catálogo de hipóteses de fraude com o que cada uma deixaria nos
dados e o resultado, e o nível de sinal (suspeita) de cada teste, separado de "passou/não passou". Gera fase3/veredito_2026.json
(lido pelo site: Home, Respostas, Testes) e fase3/VEREDITO_2026.md."""
import json

R = "."
MARGEM_2026, PRECISO = 4430191, 2215096   # inverter o resultado: trocar metade da margem de lado
NIVEIS = [
 {"id": "S0", "nome": "Sem sinal", "cor": "ok", "o_que_e": "O teste tinha poder para ver o problema e o esperado foi observado."},
 {"id": "S1", "nome": "Explicado por fator verificável", "cor": "ok2", "o_que_e": "Houve diferença, explicada por algo que não depende do próprio sistema eleitoral (perfil do eleitor, estrutura da eleição, mesmo padrão em 2022)."},
 {"id": "S2", "nome": "Compatível só com o registro do sistema", "cor": "amarelo", "o_que_e": "Houve algo fora do comum, e a explicação vem do próprio log ou de declaração do TSE. Compatível, não verificado de forma independente."},
 {"id": "S3", "nome": "Anomalia sem causa", "cor": "laranja", "o_que_e": "Padrão estatisticamente real e fora do esperado, sem causa demonstrada. Não é prova de fraude, mas é suspeita registrada."},
 {"id": "S4", "nome": "Divergência ou lacuna objetiva", "cor": "vermelho", "o_que_e": "Registros que discordam entre si ou arquivos que faltam. Fato, com causa não demonstrada."},
 {"id": "S5", "nome": "Indício de irregularidade", "cor": "vermelho_forte", "o_que_e": "Anomalia + divergência objetiva + efeito em votos, juntos e sem explicação. Nenhum caso hoje."},
 {"id": "PC", "nome": "Ponto cego", "cor": "cinza", "o_que_e": "O teste não consegue decidir ou não alcança o mecanismo. Nada se conclui, nem a favor nem contra."},
 {"id": "M", "nome": "Método ou descrição", "cor": "neutro", "o_que_e": "Teste de poder, de método ou descritivo; não é sinal sobre a eleição."},
]
S = lambda n, m: {"nivel": n, "motivo": m}
SINAL = {
 "T01": S("S0", "Tabelas do TSE iguais voto a voto (consistência interna)."), "T02": S("S3", "Excesso de seções com virada pró-Lula muito acima do esperado: em 2026, 33 seções em 33 locais diferentes, com comparecimento caindo (−3,0 pp; contrário de enchimento), ~773 votos; em 2022, 90 seções, ~2.600 votos. Real, sem causa."),
 "T03": S("S0", "Efeito desprezível da hora de chegada."), "T04": S("S0", "Urna trocada vota igual (equivalência)."), "T05": S("S0", "Dígitos uniformes."), "T07": S("S0", "Sem assinatura de enchimento."),
 "T08": S("S0", "Nenhum boletim antes do fim da votação."), "T09": S("S1", "Prorrogação em 6.748 seções; virada igual com e sem."), "T10": S("PC", "Curva sem modelo de chegada validado; não decide."),
 "T11": S("PC", "Idem."), "T12": S("S1", "Associação some ao controlar idade."), "T13": S("M", "Poder dos testes (simulação)."), "T13b": S("M", "Poder dos testes de log."),
 "T14": S("S4", "Log com contagem diferente do comparecimento: 16 seções-turno em 2026 (113 votos); 153 em 2022 (5.287 votos sem registro)."),
 "T15": S("S4", "Imagem do boletim diferente do boletim digital em RS 88013/2/199 (2022, 92 votos); em 2026, 1 caso compatível com contingência registrada."),
 "T16": S("S0", "Assinaturas válidas até a AC emissora; a raiz do TSE é ponto cego."), "T16c": S("M", "Teste da implementação criptográfica."), "T17": S("S0", "RDV = boletim (consistência interna)."),
 "T17b": S("S0", "bu.dat = RDV = tabela em todas as urnas (consistência interna)."), "T19": S("M", "Bateria em 2022."), "T20": S("S0", "Modelo de urna sem efeito."), "T21": S("S0", "Sem excesso de percentuais inteiros."),
 "T22": S("S0", "Sem assinatura de fraude incremental."), "T23": S("M", "Classificador; poder medido."), "T24": S("S2", "Urnas substituídas no meio do dia, conforme o log."), "T25": S("S0", "Impressão digital como 2022."),
 "T26": S("M", "Método excluído (inadequado)."), "T27": S("S0", "Dígitos de comparecimento uniformes."), "T28": S("S3", "8 urnas com rajada de liberação sem biometria no fim do dia (99 votos, 2026 1º turno); em 6 delas Lula tem proporção abaixo do município; o mesmo método marca 18 urnas em 2022."),
 "T29": S("S1", "Muitos votos rápidos no 2º turno: há só um cargo; mesma diferença em 2022."), "T30": S("S2", "1 urna por turno com voto antes da abertura registrada, com troca de urna no log."),
 "T31": S("S4", "2 votos sem habilitação em 1 urna (RJ 60011/8/61, log corrompido pela urna)."), "T32": S("S0", "Soma das urnas = total oficial (638/638)."),
 "T33": S("S2", "Linhas 'Verificação de assinatura … [ERRO]' no log de 128 e 162 urnas, quase todas fora do dia da eleição; as 19 e 8 do dia da eleição (inclusive em arquivos de sistema) são seguidas de verificação com sucesso do mesmo arquivo; urnas sem deslocamento de votos. Compatível com nova tentativa registrada, não verificado de forma independente."),
 "T34": S("S2", "Urna usada ≠ preparada em 3.060 seções, declaradas pelo TSE como contingência."), "T35": S("S4", "3 máquinas de geração de mídia sem log publicado (2026)."),
 "C01": S("M", "Descritivo."), "C02": S("M", "Descritivo."), "C03": S("M", "Descritivo."), "C06": S("M", "Estimativa de fluxos; frágil na magnitude."), "C06b": S("M", "Limites matemáticos."),
 "C07": S("M", "Descritivo."), "C08": S("M", "Descritivo."), "E01": S("S0", "Agrupamento local, como em 2022."), "E02": S("S3", "Cerca de 0,1% dos locais de votação atípicos; lista depende do método; dezenas a centenas de votos cada."),
 "E03": S("S3", "Casos extremos listados, sem confirmação."), "INC": S("M", "Incerteza dos negativos."), "T36": S("S2", "186 e 75 urnas com contas que não fecham, explicadas pelo próprio sistema; 1 sem explicação (RJ 60011/8/61)."),
 "T37": S("M", "Teste do estimador."), "T38": S("S0", "Sem assinatura de enchimento nas seções pró-Lula atípicas."), "T39": S("S0", "20 seções sem divergência (amostra)."),
 "T40": S("PC", "Curvas: nenhum modelo de chegada validado."), "T41": S("PC", "Zeros: sem modelo calibrado; sem excesso agregado na descrição."), "T42": S("M", "Dependência espacial (estrutura, não sinal)."),
 "T43": S("S0", "Decodificação independente igual (implementação de terceiro)."),
 "T44": S("S3", "Salvador: virada de Lula ~30 mil votos acima do previsto, em todas as 19 zonas; única capital desviante entre as 27 (z 6,1); não explicada pelo perfil do eleitorado; Fortaleza tem desvio por seção de tamanho parecido no sentido oposto."),
}
H = lambda id, mec, deixaria, escala, testes, resultado, status, votos: {"id": id, "mecanismo": mec, "o_que_deixaria": deixaria, "escala_necessaria": escala, "testes": testes, "resultado": resultado, "status": status, "em_votos": votos}
CONTR, SEMS, SINALC, CEGO = "Contrariada pela evidência", "Sem sinal no alcance testado", "Sinal encontrado, sem causa", "Ponto cego dos dados públicos"
HIP = [
 H("H1", "Alterar os votos depois da apuração (base publicada diferente do que foi divulgado na noite)", "Totais divulgados ao vivo diferentes da soma das seções publicadas depois",
   "Qualquer escala", ["R2", "T32"], "39 capturas independentes (Internet Archive) dos totais divulgados ao vivo batem com a base final; diferença 0 no fim.", CONTR, "0 voto de diferença no total final."),
 H("H2", "Trocar votos na totalização (boletins certos, soma errada)", "Soma dos boletins diferente do total oficial", "Qualquer escala", ["T32", "T17b", "R1", "T43"],
   "Soma das urnas = total oficial em 638/638 itens; tabela = boletim em todas as seções; decodificação de terceiro igual.", CONTR, "0 voto de diferença."),
 H("H3", "Trocar votos no boletim de urnas espalhadas (algumas urnas com muitos votos trocados)", "Excesso de seções com virada fora do padrão do município (T02, T13)",
   "Para inverter: ~2,2 mi votos; nos cenários simulados, ~123 mil já são vistos (10% dos válidos em 1% das urnas)", ["T02", "T13", "A2"],
   "Há excesso real de seções pró-Lula (T02), mas soma ~740 votos em 2026; uma troca do tamanho necessário para inverter seria ~18 vezes maior que o limite de detecção simulado.", SINALC, "~740 votos na cauda pró-Lula (0,02% da margem)."),
 H("H4", "Trocar votos concentrados em locais de votação ou municípios pequenos", "Locais ou municípios com virada muito fora do entorno (E02, I3)", "Nos cenários simulados, ~62 mil já são vistos",
   ["E02", "I3", "A2", "T38"], "Cerca de 0,1% dos locais são atípicos, com dezenas a poucas centenas de votos cada; sem assinatura de enchimento.", SINALC, "Dezenas a centenas de votos por local."),
 H("H5", "Trocar votos na cidade inteira de uma grande cidade", "Virada da cidade fora do previsto pelo histórico de 2022 e pelo perfil (T44)", "Troca de 2% dos válidos já seria vista nas 5 maiores cidades (31 mil a 139 mil votos)",
   ["T44", "A2"], "São Paulo, Rio, Brasília e Fortaleza dentro do esperado; Salvador ~30 mil votos de Lula acima do previsto, em todas as zonas, a única entre as 27 capitais; o perfil do eleitorado não explica; Fortaleza mostra deslocamento de tamanho parecido no sentido oposto (Lula abaixo), então variações desse porte numa cidade inteira ocorrem nos dois sentidos.", SINALC, "Salvador: ~30 mil votos (0,7% da margem)."),
 H("H6", "Encher urnas (votos de eleitores que não votaram)", "Comparecimento subindo nas seções pró-Lula; log com mais votos que habilitações; rajadas sem biometria", "Proporcional ao enchimento",
   ["T38", "T07", "T14", "T28", "T31"], "Sem assinatura de enchimento: nas 33 seções pró-Lula extremas o comparecimento caiu; 8 urnas com rajada sem biometria (99 votos), 6 delas com Lula abaixo do município, padrão também em 2022; 2 votos sem habilitação em 1 urna com log corrompido.", SINALC, "~100 votos com sinal."),
 H("H7", "Apagar votos do adversário em seções inteiras (zeros)", "Mais seções com zero votos do que o perfil local prevê", "Dezenas a milhares de votos", ["T41", "R3", "E3"],
   "79 e 106 seções com zero para Flávio, exatamente o previsto fora da amostra (79,1 e 101,5); registros conferem.", SEMS, "No máximo ~4.800 votos se fosse anomalia (0,11% da margem)."),
 H("H8", "Manipular a ordem ou o ritmo da divulgação (virada 'fabricada')", "Sequência divulgada diferente da base; curva impossível de reproduzir", "Não muda votos", ["R2", "T40", "F4"],
   "A sequência divulgada é reproduzida pela base nos 39 instantes capturados; a virada tardia também ocorre em 2022; o modelo de chegada não explica o momento da virada.", SEMS, "A ordem não altera nenhum voto."),
 H("H9", "Deslocar um pouco de votos em quase todas as urnas (uniforme)", "Nada estatístico: um deslocamento pequeno e uniforme é indistinguível de uma mudança real de opinião",
   "~4 a 5 votos por urna bastariam para inverter", ["T13"], "Não testável com dados agregados. Só boletins impressos coletados por fiscais (amostra) ou auditoria independente da urna examinam isto.", CEGO, "Até ~2,2 mi votos sem rastro estatístico."),
 H("H10", "Comprometer o software ou a urna antes de gerar os registros (BU, RDV e log já nascem alterados e coerentes)", "Nada nos arquivos: tudo concorda entre si", "Qualquer escala",
   ["T16", "T33", "auditoria adversarial"], "Assinaturas válidas até a AC emissora, sem âncora do TSE verificada (busca externa sem resultado); erros de verificação de assinatura do software no log seguidos de sucesso registrado, sem efeito em votos.", CEGO, "Até o total; sem rastro nos dados públicos."),
]
# Aviso que vem antes da pergunta em todo lugar (site, VEREDITO, README, release): a pergunta é testada, não é a premissa.
AVISO = {
 "titulo": "O que este estudo é, e o que não é",
 "itens": [
   "É uma auditoria metodológica dos dados públicos oficiais da apuração: confere se os registros do TSE são coerentes entre si e se os padrões estatísticos têm explicação, com critérios fixados antes de rodar e poder medido com fraude simulada.",
   "Não parte de suspeita nem de acusação: parte dos dados. A pergunta sobre fraude é uma das perguntas que os testes respondem, a mais feita pelo público; não é a premissa nem o motivo do estudo.",
   "É independente, não é auditoria oficial e não é veredito sobre a eleição. Anomalia estatística não é fraude, e ausência de sinal não prova ausência onde os dados públicos não alcançam.",
 ],
}
RESPOSTA = {
 "aviso": AVISO,
 "pergunta": "A apuração presidencial de 2026 tem sinais de fraude capaz de mudar o resultado?",
 "resposta": "Não encontramos. Para inverter o resultado seria preciso trocar ~2,2 milhões de votos de lado. Os mecanismos que os dados públicos permitem examinar foram contrariados ou deixariam sinais muito maiores do que os encontrados. As anomalias reais que achamos somam dezenas de milhares de votos, não milhões, e não têm causa demonstrada. Restam dois caminhos que nenhum dado público consegue examinar: um deslocamento pequeno e uniforme em quase todas as urnas, e uma alteração da urna antes de gerar os registros. Ambos só podem ser checados com evidência de fora do sistema, como boletins impressos coletados por fiscais ou auditoria independente da urna.",
 "deducao": [
   "Inverter 2026 exige trocar ~2,22 mi votos (metade da margem de 4,43 mi).",
   "Isso não aconteceu depois da apuração: os totais divulgados ao vivo, guardados por terceiro, batem com a base final (H1).",
   "Também não na soma: boletins, tabela e total oficial coincidem em todas as seções (H2).",
   "Se tivesse sido feito trocando muitos votos em poucas urnas, locais, municípios ou numa grande cidade, os testes simulados veriam a partir de ~31 mil (2% numa grande cidade inteira) a ~123 mil votos (troca dispersa), e ~62 mil concentrados em locais ou municípios; o que aparece são ~740 votos em seções atípicas, ~0,1% de locais com dezenas a centenas de votos, e ~30 mil votos em Salvador (H3, H4, H5).",
   "Encher urnas ou apagar votos do adversário também deixaria rastro, que não aparece além de ~100 votos e de zeros no nível previsto (H6, H7).",
   "Sobram os mecanismos que não deixam rastro nos dados públicos: deslocamento pequeno e uniforme (H9) e alteração da urna antes dos registros (H10). Não podemos excluí-los nem confirmá-los com estes dados.",
 ],
 "o_que_seria_preciso": "Para fechar H9 e H10: comparar com boletins impressos afixados nas seções (coletados por fiscais ou terceiros) em amostra aleatória, auditoria independente do software e da urna, e a cadeia de certificados até a raiz do TSE.",
 "anomalias_2026": [
   {"o_que": "Salvador: virada de Lula acima do previsto", "votos": "~30 mil", "sinal": "S3", "teste": "T44"},
   {"o_que": "33 seções com virada pró-Lula muito fora do padrão, em locais diferentes e com comparecimento em queda", "votos": "~773", "sinal": "S3", "teste": "T02"},
   {"o_que": "8 urnas com rajada sem biometria no fim do dia", "votos": "99", "sinal": "S3", "teste": "T28"},
   {"o_que": "Log com contagem diferente do comparecimento", "votos": "113", "sinal": "S4", "teste": "T14"},
   {"o_que": "2 votos sem habilitação em urna com log corrompido", "votos": "2", "sinal": "S4", "teste": "T31"},
   {"o_que": "Erros de verificação de assinatura do software no log, seguidos de sucesso", "votos": "não se traduz (sem efeito nos votos)", "sinal": "S2", "teste": "T33"},
   {"o_que": "Cerca de 0,1% dos locais com virada atípica", "votos": "dezenas a centenas por local", "sinal": "S3", "teste": "E02"},
 ],
}
OUT = {"gerado": "2026-10-28", "situacao": "F3 em revisão; não congelado", "margem_2026": MARGEM_2026, "votos_para_inverter": PRECISO, "niveis": NIVEIS, "sinal_por_teste": SINAL, "hipoteses": HIP, "resposta_central": RESPOSTA}
json.dump(OUT, open(R + "/fase3/veredito_2026.json", "w"), ensure_ascii=False, indent=1)
L = ["# Apuração de 2026: o que os dados públicos mostram", "", f"> **{AVISO['titulo']}**", ">"] + [f"> - {a}" for a in AVISO["itens"]] + ["", f"**Pergunta testada:** {RESPOSTA['pergunta']}", "", f"**Resposta:** {RESPOSTA['resposta']}", "", "## Dedução", ""] + [f"{i+1}. {d}" for i, d in enumerate(RESPOSTA["deducao"])] + ["", f"**O que fecharia o que resta:** {RESPOSTA['o_que_seria_preciso']}", "",
     "## Hipóteses de fraude examinadas", "", "| Id | Mecanismo | O que deixaria | Resultado | Situação | Em votos |", "|---|---|---|---|---|---|"]
L += [f"| {h['id']} | {h['mecanismo']} | {h['o_que_deixaria']} | {h['resultado']} | **{h['status']}** | {h['em_votos']} |" for h in HIP]
L += ["", "## Anomalias reais em 2026", "", "| O que | Votos | Sinal | Teste |", "|---|---|---|---|"] + [f"| {a['o_que']} | {a['votos']} | {a['sinal']} | {a['teste']} |" for a in RESPOSTA["anomalias_2026"]]
L += ["", "## Escala de sinal", ""] + [f"- **{n['id']} {n['nome']}:** {n['o_que_e']}" for n in NIVEIS]
L += ["", "## Sinal de cada teste", "", "| Teste | Sinal | Motivo |", "|---|---|---|"] + [f"| {k} | {v['nivel']} | {v['motivo']} |" for k, v in SINAL.items()]
open(R + "/fase3/VEREDITO_2026.md", "w").write("\n".join(L) + "\n")
print("ok", len(SINAL), len(HIP))
