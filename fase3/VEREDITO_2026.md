# Apuração de 2026: o que os dados públicos mostram

> **O que este estudo é, e o que não é**
>
> - É uma auditoria metodológica dos dados públicos oficiais da apuração: confere se os registros do TSE são coerentes entre si e se os padrões estatísticos têm explicação, com critérios fixados antes de rodar e poder medido com fraude simulada.
> - Não parte de suspeita nem de acusação: parte dos dados. A pergunta sobre fraude é uma das perguntas que os testes respondem, a mais feita pelo público; não é a premissa nem o motivo do estudo.
> - É independente, não é auditoria oficial e não é veredito sobre a eleição. Anomalia estatística não é fraude, e ausência de sinal não prova ausência onde os dados públicos não alcançam.

**Nota do autor:** Não quero provar nem refutar nada. Também não afirmo nem nego que os dados oficiais sejam verdadeiros: peguei o que está disponível publicamente e analisei o que dava para analisar. A gente vê muita coisa sobre urna na internet e quase ninguém para e analisa os dados de verdade. Então eu fiz essa análise até onde os dados públicos permitiram ir. Daqui em diante é com vocês: em vez de reclamar, usem o projeto, rodem os dados, coloquem nos seus agentes de IA, contribuam com o que encontrarem e tirem as suas próprias conclusões.

**Pergunta testada:** A apuração presidencial de 2026 tem sinais de fraude capaz de mudar o resultado?

**Resposta:** Não encontramos. Para inverter o resultado seria preciso trocar ~2,2 milhões de votos de lado. Os mecanismos que os dados públicos permitem examinar foram contrariados ou deixariam sinais muito maiores do que os encontrados. As anomalias reais que achamos somam dezenas de milhares de votos, não milhões, e não têm causa demonstrada. Restam dois caminhos que nenhum dado público consegue examinar: um deslocamento pequeno e uniforme em quase todas as urnas, e uma alteração da urna antes de gerar os registros. Ambos só podem ser checados com evidência de fora do sistema, como boletins impressos coletados por fiscais ou auditoria independente da urna.

## Dedução

1. Inverter 2026 exige trocar ~2,22 mi votos (metade da margem de 4,43 mi).
2. Isso não aconteceu depois da apuração: os totais divulgados ao vivo, guardados por terceiro, batem com a base final (H1).
3. Também não na soma: boletins, tabela e total oficial coincidem em todas as seções (H2).
4. Se tivesse sido feito trocando muitos votos em poucas urnas, locais, municípios ou numa grande cidade, os testes simulados veriam a partir de ~31 mil (2% numa grande cidade inteira) a ~123 mil votos (troca dispersa), e ~62 mil concentrados em locais ou municípios; o que aparece são ~740 votos em seções atípicas, ~0,1% de locais com dezenas a centenas de votos, e ~30 mil votos em Salvador (H3, H4, H5).
5. Encher urnas ou apagar votos do adversário também deixaria rastro, que não aparece além de ~100 votos e de zeros no nível previsto (H6, H7).
6. Sobram os mecanismos que não deixam rastro nos dados públicos: deslocamento pequeno e uniforme (H9) e alteração da urna antes dos registros (H10). Não podemos excluí-los nem confirmá-los com estes dados.

**O que fecharia o que resta:** Para fechar H9 e H10: comparar com boletins impressos afixados nas seções (coletados por fiscais ou terceiros) em amostra aleatória, auditoria independente do software e da urna, e a cadeia de certificados até a raiz do TSE.

## Hipóteses de fraude examinadas

| Id | Mecanismo | O que deixaria | Resultado | Situação | Em votos |
|---|---|---|---|---|---|
| H1 | Alterar os votos depois da apuração (base publicada diferente do que foi divulgado na noite) | Totais divulgados ao vivo diferentes da soma das seções publicadas depois | 39 capturas independentes (Internet Archive) dos totais divulgados ao vivo batem com a base final; diferença 0 no fim. | **Contrariada pela evidência** | 0 voto de diferença no total final. |
| H2 | Trocar votos na totalização (boletins certos, soma errada) | Soma dos boletins diferente do total oficial | Soma das urnas = total oficial em 638/638 itens; tabela = boletim em todas as seções; decodificação de terceiro igual. | **Contrariada pela evidência** | 0 voto de diferença. |
| H3 | Trocar votos no boletim de urnas espalhadas (algumas urnas com muitos votos trocados) | Excesso de seções com virada fora do padrão do município (T02, T13) | Há excesso real de seções pró-Lula (T02), mas soma ~740 votos em 2026; uma troca do tamanho necessário para inverter seria ~18 vezes maior que o limite de detecção simulado. | **Sinal encontrado, sem causa** | ~740 votos na cauda pró-Lula (0,02% da margem). |
| H4 | Trocar votos concentrados em locais de votação ou municípios pequenos | Locais ou municípios com virada muito fora do entorno (E02, I3) | Cerca de 0,1% dos locais são atípicos, com dezenas a poucas centenas de votos cada; sem assinatura de enchimento. | **Sinal encontrado, sem causa** | Dezenas a centenas de votos por local. |
| H5 | Trocar votos na cidade inteira de uma grande cidade | Virada da cidade fora do previsto pelo histórico de 2022 e pelo perfil (T44) | São Paulo, Rio, Brasília e Fortaleza dentro do esperado; Salvador ~30 mil votos de Lula acima do previsto, em todas as zonas, a única entre as 27 capitais; o perfil do eleitorado não explica; Fortaleza mostra deslocamento de tamanho parecido no sentido oposto (Lula abaixo), então variações desse porte numa cidade inteira ocorrem nos dois sentidos. | **Sinal encontrado, sem causa** | Salvador: ~30 mil votos (0,7% da margem). |
| H6 | Encher urnas (votos de eleitores que não votaram) | Comparecimento subindo nas seções pró-Lula; log com mais votos que habilitações; rajadas sem biometria | Sem assinatura de enchimento: nas 33 seções pró-Lula extremas o comparecimento caiu; 8 urnas com rajada sem biometria (99 votos), 6 delas com Lula abaixo do município, padrão também em 2022; 2 votos sem habilitação em 1 urna com log corrompido. | **Sinal encontrado, sem causa** | ~100 votos com sinal. |
| H7 | Apagar votos do adversário em seções inteiras (zeros) | Mais seções com zero votos do que o perfil local prevê | 79 e 106 seções com zero para Flávio, exatamente o previsto fora da amostra (79,1 e 101,5); registros conferem. | **Sem sinal no alcance testado** | No máximo ~4.800 votos se fosse anomalia (0,11% da margem). |
| H8 | Manipular a ordem ou o ritmo da divulgação (virada 'fabricada') | Sequência divulgada diferente da base; curva impossível de reproduzir | A sequência divulgada é reproduzida pela base nos 39 instantes capturados; a virada tardia também ocorre em 2022; o modelo de chegada não explica o momento da virada. | **Sem sinal no alcance testado** | A ordem não altera nenhum voto. |
| H9 | Deslocar um pouco de votos em quase todas as urnas (uniforme) | Nada estatístico: um deslocamento pequeno e uniforme é indistinguível de uma mudança real de opinião | Não testável com dados agregados. Só boletins impressos coletados por fiscais (amostra) ou auditoria independente da urna examinam isto. | **Ponto cego dos dados públicos** | Até ~2,2 mi votos sem rastro estatístico. |
| H10 | Comprometer o software ou a urna antes de gerar os registros (BU, RDV e log já nascem alterados e coerentes) | Nada nos arquivos: tudo concorda entre si | Assinaturas válidas até a AC emissora, sem âncora do TSE verificada (busca externa sem resultado); erros de verificação de assinatura do software no log seguidos de sucesso registrado, sem efeito em votos. | **Ponto cego dos dados públicos** | Até o total; sem rastro nos dados públicos. |

## Anomalias reais em 2026

| O que | Votos | Sinal | Teste |
|---|---|---|---|
| Salvador: virada de Lula acima do previsto | ~30 mil | S3 | T44 |
| 33 seções com virada pró-Lula muito fora do padrão, em locais diferentes e com comparecimento em queda | ~773 | S3 | T02 |
| 8 urnas com rajada sem biometria no fim do dia | 99 | S3 | T28 |
| Log com contagem diferente do comparecimento | 113 | S4 | T14 |
| 2 votos sem habilitação em urna com log corrompido | 2 | S4 | T31 |
| Erros de verificação de assinatura do software no log, seguidos de sucesso | não se traduz (sem efeito nos votos) | S2 | T33 |
| Cerca de 0,1% dos locais com virada atípica | dezenas a centenas por local | S3 | E02 |

## Escala de sinal

- **S0 Sem sinal:** O teste tinha poder para ver o problema e o esperado foi observado.
- **S1 Explicado por fator verificável:** Houve diferença, explicada por algo que não depende do próprio sistema eleitoral (perfil do eleitor, estrutura da eleição, mesmo padrão em 2022).
- **S2 Compatível só com o registro do sistema:** Houve algo fora do comum, e a explicação vem do próprio log ou de declaração do TSE. Compatível, não verificado de forma independente.
- **S3 Anomalia sem causa:** Padrão estatisticamente real e fora do esperado, sem causa demonstrada. Não é prova de fraude, mas é suspeita registrada.
- **S4 Divergência ou lacuna objetiva:** Registros que discordam entre si ou arquivos que faltam. Fato, com causa não demonstrada.
- **S5 Indício de irregularidade:** Anomalia + divergência objetiva + efeito em votos, juntos e sem explicação. Nenhum caso hoje.
- **PC Ponto cego:** O teste não consegue decidir ou não alcança o mecanismo. Nada se conclui, nem a favor nem contra.
- **M Método ou descrição:** Teste de poder, de método ou descritivo; não é sinal sobre a eleição.

## Sinal de cada teste

| Teste | Sinal | Motivo |
|---|---|---|
| T01 | S0 | Tabelas do TSE iguais voto a voto (consistência interna). |
| T02 | S3 | Excesso de seções com virada pró-Lula muito acima do esperado: em 2026, 33 seções em 33 locais diferentes, com comparecimento caindo (−3,0 pp; contrário de enchimento), ~773 votos; em 2022, 90 seções, ~2.600 votos. Real, sem causa. |
| T03 | S0 | Efeito desprezível da hora de chegada. |
| T04 | S0 | Urna trocada vota igual (equivalência). |
| T05 | S0 | Dígitos uniformes. |
| T07 | S0 | Sem assinatura de enchimento. |
| T08 | S0 | Nenhum boletim antes do fim da votação. |
| T09 | S1 | Prorrogação em 6.748 seções; virada igual com e sem. |
| T10 | PC | Curva sem modelo de chegada validado; não decide. |
| T11 | PC | Idem. |
| T12 | S1 | Associação some ao controlar idade. |
| T13 | M | Poder dos testes (simulação). |
| T13b | M | Poder dos testes de log. |
| T14 | S4 | Log com contagem diferente do comparecimento: 16 seções-turno em 2026 (113 votos); 153 em 2022 (5.287 votos sem registro). |
| T15 | S4 | Imagem do boletim diferente do boletim digital em RS 88013/2/199 (2022, 92 votos); em 2026, 1 caso compatível com contingência registrada. |
| T16 | S0 | Assinaturas válidas até a AC emissora; a raiz do TSE é ponto cego. |
| T16c | M | Teste da implementação criptográfica. |
| T17 | S0 | RDV = boletim (consistência interna). |
| T17b | S0 | bu.dat = RDV = tabela em todas as urnas (consistência interna). |
| T19 | M | Bateria em 2022. |
| T20 | S0 | Modelo de urna sem efeito. |
| T21 | S0 | Sem excesso de percentuais inteiros. |
| T22 | S0 | Sem assinatura de fraude incremental. |
| T23 | M | Classificador; poder medido. |
| T24 | S2 | Urnas substituídas no meio do dia, conforme o log. |
| T25 | S0 | Impressão digital como 2022. |
| T26 | M | Método excluído (inadequado). |
| T27 | S0 | Dígitos de comparecimento uniformes. |
| T28 | S3 | 8 urnas com rajada de liberação sem biometria no fim do dia (99 votos, 2026 1º turno); em 6 delas Lula tem proporção abaixo do município; o mesmo método marca 18 urnas em 2022. |
| T29 | S1 | Muitos votos rápidos no 2º turno: há só um cargo; mesma diferença em 2022. |
| T30 | S2 | 1 urna por turno com voto antes da abertura registrada, com troca de urna no log. |
| T31 | S4 | 2 votos sem habilitação em 1 urna (RJ 60011/8/61, log corrompido pela urna). |
| T32 | S0 | Soma das urnas = total oficial (638/638). |
| T33 | S2 | Linhas 'Verificação de assinatura … [ERRO]' no log de 128 e 162 urnas, quase todas fora do dia da eleição; as 19 e 8 do dia da eleição (inclusive em arquivos de sistema) são seguidas de verificação com sucesso do mesmo arquivo; urnas sem deslocamento de votos. Compatível com nova tentativa registrada, não verificado de forma independente. |
| T34 | S2 | Urna usada ≠ preparada em 3.060 seções, declaradas pelo TSE como contingência. |
| T35 | S4 | 3 máquinas de geração de mídia sem log publicado (2026). |
| C01 | M | Descritivo. |
| C02 | M | Descritivo. |
| C03 | M | Descritivo. |
| C06 | M | Estimativa de fluxos; frágil na magnitude. |
| C06b | M | Limites matemáticos. |
| C07 | M | Descritivo. |
| C08 | M | Descritivo. |
| E01 | S0 | Agrupamento local, como em 2022. |
| E02 | S3 | Cerca de 0,1% dos locais de votação atípicos; lista depende do método; dezenas a centenas de votos cada. |
| E03 | S3 | Casos extremos listados, sem confirmação. |
| INC | M | Incerteza dos negativos. |
| T36 | S2 | 186 e 75 urnas com contas que não fecham, explicadas pelo próprio sistema; 1 sem explicação (RJ 60011/8/61). |
| T37 | M | Teste do estimador. |
| T38 | S0 | Sem assinatura de enchimento nas seções pró-Lula atípicas. |
| T39 | S0 | 20 seções sem divergência (amostra). |
| T40 | PC | Curvas: nenhum modelo de chegada validado. |
| T41 | PC | Zeros: sem modelo calibrado; sem excesso agregado na descrição. |
| T42 | M | Dependência espacial (estrutura, não sinal). |
| T43 | S0 | Decodificação independente igual (implementação de terceiro). |
| T45 | S1 | 2022: ID fixo 67305985 no log de todas as urnas pré-2020 (bug); log ligado ao BU e ao RDV pela assinatura e pelo certificado em 279.285 de 279.291 seções; 6 são trocas de urna ou arquivos faltantes já catalogados. Em 2026 o bug não aparece. |
| T46 | S1 | O 51,05% de Bolsonaro só nas UE2020 (2022) se reproduz; é o voto das cidades que tinham UE2020. Dentro do município, Lula continua vencendo (Bolsonaro 49,25%). |
| T47 | S1 | Lula teve mais votos nas urnas antigas (50,3% × 46,0%, 1º turno de 2022), também dentro do município; dentro do mesmo local de votação a diferença é equivalente a zero nos dois turnos: é localização, não modelo. |
| T48 | S0 | Mesmo software (8.26.0.0) em todos os modelos em 2022; seções unânimes proporcionais à presença de cada modelo. |
| T49 | S0 | 106 seções com zero para Flávio (14.860 votos de Lula) reproduzidas; eram 141 em 2022; mesmas regiões e seções que já votavam quase só em Lula; arquivos íntegros. |
| T50 | S0 | Contagens da thread reproduzidas; voto de Lula menos concentrado em 2026 (35.591 seções > 80%) que em 2022 (40.046). |
| T51 | S0 | Lula cresceu mais que Flávio em 93,8% dos municípios e nas 27 UFs; em 2022 Bolsonaro cresceu mais em 87,1% e nas 27 UFs; em proporção, 2022 foi até mais uniforme. |
| T52 | S1 | Recebimento de BUs parado das 17:07 às 19:03 no 2º turno de 2026, só em 2026; volta junto com o fechamento das urnas prorrogadas; o conteúdo do BU é assinado na emissão e confere. |
| T53 | S0 | Liberação sem biometria menor que em 2022 (6,8% × 8,1%) e com relação levemente negativa com a virada de Lula. |
| T54 | S0 | Flávio perdeu votos em 937 municípios; em 2022 Lula perdeu em 981: mesmo padrão de 2º turno. |
| T55 | S0 | Cabo Frio: ganho de Lula (+9.169) cabe nos 9.511 votos disponíveis; percentil 89 do país; 28 casos espelhados a favor de Bolsonaro em 2022. |
| T56 | S1 | Brancos e nulos do 1º turno → Lula no estimador (C06); em parte explicado: excesso de brancos e nulos no 1º turno de 2026 onde Lula é forte (~0,47 de 1,82 mi); o resto é queda geral no 2º turno; fluxo individual não identificável. |
| T44 | S3 | Salvador: virada de Lula ~30 mil votos acima do previsto, em todas as 19 zonas; única capital desviante entre as 27 (z 6,1); não explicada pelo perfil do eleitorado; Fortaleza tem desvio por seção de tamanho parecido no sentido oposto. |
