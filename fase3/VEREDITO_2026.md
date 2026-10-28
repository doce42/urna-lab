# Apuração de 2026: o que os dados públicos mostram

> **O que este estudo é, e o que não é**
>
> - É uma auditoria metodológica dos dados públicos oficiais da apuração: confere se os registros do TSE são coerentes entre si e se os padrões estatísticos têm explicação, com critérios fixados antes de rodar e poder medido com fraude simulada.
> - Não parte de suspeita nem de acusação: parte dos dados. A pergunta sobre fraude é uma das perguntas que os testes respondem, a mais feita pelo público; não é a premissa nem o motivo do estudo.
> - É independente, não é auditoria oficial e não é veredito sobre a eleição. Anomalia estatística não é fraude, e ausência de sinal não prova ausência onde os dados públicos não alcançam.

**Nota do autor:** Não quero provar nem refutar nada. Também não afirmo nem nego que os dados oficiais sejam verdadeiros: peguei o que está disponível publicamente e analisei o que dava para analisar. A gente vê muita coisa sobre urna na internet e quase ninguém para e analisa os dados de verdade. Então eu fiz essa análise até onde os dados públicos permitiram ir. Daqui em diante é com vocês: em vez de reclamar, usem o projeto, rodem os dados, coloquem nos seus agentes de IA, contribuam com o que encontrarem e tirem as suas próprias conclusões.

**Pergunta testada:** A apuração presidencial de 2026 tem sinais de fraude capaz de mudar o resultado?

**Resposta:** Não encontramos sinal de fraude nos mecanismos que os dados públicos conseguem examinar, com o poder medido para cada um. Para inverter o resultado seria preciso trocar ~2,2 milhões de votos de lado. Troca dispersa, em locais, zonas ou municípios, de dezenas de milhares de votos deixaria sinal; troca de escala de UF, região ou lote, ou deslocamento uniforme, só seria vista a partir de algumas centenas de milhares a milhões de votos. As anomalias que encontramos somam dezenas de milhares de votos e não têm causa demonstrada; isso descreve o que foi achado e não limita o que pode ter passado sem alarme. Restam caminhos fora do alcance: um deslocamento pequeno e uniforme em quase todas as urnas (H9), uma alteração da urna antes de gerar os registros (H10) e alterações de escala regional, de UF, de lote ou uniformes abaixo de ~0,5 a 2,2 milhões de votos (T63). Só evidência de fora do sistema resolve: boletins impressos de uma amostra sorteada de seções, auditoria independente da urna e a raiz da cadeia de certificados.

**Leia junto com os resultados:**

- O poder de detecção é medido sobre uma base real que pode já conter alteração; o experimento não consegue dizer que a base está limpa.
- O poder é assimétrico entre os sentidos, por causa da cauda pró-Lula presente na base nos dois anos.
- Registros internamente coerentes gerados por uma fonte comprometida passam por todas as verificações internas; só evidência de fora distingue.
- Os 404 boletins de terceiros são uma amostra de conveniência (0,08%).

## Dedução

1. Inverter 2026 exige trocar ~2,22 mi votos (metade da margem de 4,43 mi).
2. Não há diferença entre o que o TSE divulgou na noite e o que publicou depois: 39 capturas guardadas por terceiro batem com a base final, e 404 arquivos são iguais entre downloads independentes (H1). Isso não testa o que aconteceu antes da primeira publicação.
3. Também não na soma: boletins, tabela e total oficial coincidem em todas as seções, e 404 boletins impressos lidos por terceiros são iguais ao TSE, numa amostra de conveniência de 0,08% (H2).
4. Troca em seções dispersas, em poucas seções, em locais, zonas ou municípios (fora os 5 maiores) seria vista a partir de 25 a 50 mil votos (T63), e numa grande cidade, uma por vez, a partir de 2% dos válidos (31 mil a 139 mil, T44). O que aparece são ~740 votos em seções atípicas, ~0,1% de locais com dezenas a centenas de votos e ~30 mil votos em Salvador (H3, H4, H5). Em 2022, a favor de Lula, a troca dispersa só é vista a partir de 500 mil: o poder é assimétrico entre os sentidos.
5. Encher urnas só é visto pela bateria a partir de 250 mil votos (T63); abaixo disso, o rastro que aparece não passa de ~100 votos com sinal (H6). Os zeros de votos ficam não determinados: nenhum modelo de cauda baixa calibrou (H7).
6. Ficam fora do alcance: deslocamento uniforme (H9; em logit, nunca visto), alteração da urna antes dos registros (H10; registros coerentes assinados pela própria fonte passam por todas as verificações internas, T62) e alterações em UFs inteiras, nos cinco grandes municípios juntos, numa macrorregião, num lote tardio ou por conversão de brancos e nulos, vistas só a partir de ~0,5 a 2,2 mi votos, ou nunca (T63). Não podemos excluí-las nem confirmá-las com estes dados.

**O que fecharia o que resta:** Boletins impressos afixados nas seções, de uma amostra sorteada (os 404 de terceiros são amostra de conveniência); auditoria independente do software e da urna; a raiz da cadeia de certificados do TSE (a cadeia já fecha até a AC emissora em 100% das urnas); e o resultado do teste de integridade com votos conhecidos, que não foi obtido.

## Hipóteses de fraude examinadas

| Id | Mecanismo | O que deixaria | Resultado | Situação | Em votos |
|---|---|---|---|---|---|
| H1 | Alterar os votos depois da apuração (base publicada diferente do que foi divulgado na noite) | Totais divulgados ao vivo diferentes da soma das seções publicadas depois | Não há diferença entre o que o TSE divulgou na noite e o que publicou depois: 39 capturas independentes (Internet Archive) dos totais divulgados ao vivo batem com a base final, e 404 arquivos bu.dat são iguais entre dois downloads independentes (T61). Isso não testa alteração antes da primeira publicação. | **Contrariada pela evidência** | 0 voto de diferença no total final. |
| H2 | Trocar votos na totalização (boletins certos, soma errada) | Soma dos boletins diferente do total oficial | Soma das urnas = total oficial em 638/638 itens; tabela = boletim em todas as seções; decodificação de terceiro igual. 404 boletins impressos lidos por terceiros no 2º turno de 2026 são iguais à tabela e ao BU do TSE, com assinatura e cadeia válidas (T61; amostra de conveniência, 0,08% das seções). | **Contrariada pela evidência** | 0 voto de diferença. |
| H3 | Trocar votos no boletim de urnas espalhadas (algumas urnas com muitos votos trocados) | Excesso de seções com virada fora do padrão do município (T02, T13, T63) | Há excesso real de seções pró-Lula (T02), mas soma ~740 votos em 2026. Em 2026, uma troca do tamanho necessário para inverter seria ~44 vezes maior que o limite de detecção de seções dispersas (~50 mil). O poder é assimétrico entre os sentidos: em 2022, a favor de Lula, o limite é 500 mil (4,4 vezes menor que 2,22 mi), porque a base já tem uma cauda pró-Lula pesada. | **Sinal encontrado, sem causa** | ~740 votos na cauda pró-Lula (0,02% da margem). |
| H4 | Trocar votos concentrados em locais de votação ou municípios pequenos | Locais ou municípios com virada muito fora do entorno (E02, I3) | Cerca de 0,1% dos locais são atípicos, com dezenas a poucas centenas de votos cada; sem assinatura de enchimento. | **Sinal encontrado, sem causa** | Dezenas a centenas de votos por local. |
| H5 | Trocar votos na cidade inteira de uma grande cidade (uma por vez) | Virada da cidade fora do previsto pelo histórico de 2022 e pelo perfil (T44) | São Paulo, Rio, Brasília e Fortaleza dentro do esperado; Salvador ~30 mil votos de Lula acima do previsto, em todas as zonas, a única entre as 27 capitais; o perfil do eleitorado não explica; Fortaleza mostra deslocamento de tamanho parecido no sentido oposto (Lula abaixo), então variações desse porte numa cidade inteira ocorrem nos dois sentidos. | **Sinal encontrado, sem causa** | Salvador: ~30 mil votos (0,7% da margem). |
| H6 | Encher urnas (votos de eleitores que não votaram) | Comparecimento subindo nas seções pró-Lula; log com mais votos que habilitações; rajadas sem biometria | Sem assinatura de enchimento: nas 33 seções pró-Lula extremas o comparecimento caiu; 8 urnas com rajada sem biometria (99 votos), 6 delas com Lula abaixo do município, padrão também em 2022; 2 votos sem habilitação em 1 urna com log corrompido. Enchimento abaixo de 250 mil votos não é excluído pela bateria estatística (T63). | **Sinal encontrado, sem causa** | ~100 votos com sinal. |
| H7 | Apagar votos do adversário em seções inteiras (zeros) | Mais seções com zero votos do que o perfil local prevê | Não determinado: nenhum modelo de cauda baixa passou na calibração (T41, R3). As três famílias novas do T64 também falham: o modelo por município prevê 1,3 zeros contra 106 observados (2022: 4,3 contra 141); o por local de votação, 66,7 contra 106. Descritivamente, os zeros são locais de uma só seção, com menos de 1% do total, em 2022 (141) e em 2026 (106); os registros dessas seções conferem. | **Não determinado (ponto cego)** | Se fossem anomalia, de ~44 a ~4.800 votos conforme o modelo (no máximo 0,11% da margem); nenhum modelo calibrou. |
| H8 | Manipular a ordem ou o ritmo da divulgação (virada 'fabricada') | Sequência divulgada diferente da base; curva impossível de reproduzir | A sequência divulgada é reproduzida pela base nos 39 instantes capturados; a virada tardia também ocorre em 2022; o modelo de chegada não explica o momento da virada, e a curva continua não determinada. Fato medido: o TSE não registrou recebimento de boletins das 17:07 às 19:03 (116 minutos) no 2º turno de 2026, só em 2026; 77 boletins de terceiros estavam registrados fora do TSE entre 18:10 e 18:47 (T52, T61). Isso não altera votos; a causa não está nos dados. A prorrogação de fato (encerramento depois das 17:30: 7.604 seções, 2,21 mi de votantes) deu a Lula +228.095 votos de vantagem, 5,1% da margem de 4.430.191; sem essas seções, Lula lidera por 4.202.096 (T66, T09, T52). | **Sem sinal no alcance testado** | A ordem não altera nenhum voto. As seções da prorrogação de fato somam +228.095 votos de vantagem para Lula (5,1% da margem); sem elas, Lula lidera por 4.202.096. |
| H9 | Deslocar um pouco de votos em quase todas as urnas (uniforme) | Nada estatístico: um deslocamento pequeno e uniforme é indistinguível de uma mudança real de opinião | Não testável com dados agregados. Quantificado no T63: um deslocamento uniforme em logit nunca é visto, em nenhuma magnitude, nos dois anos; em fatia de voto, só a partir de 1 a 2,22 mi votos, e nunca no sentido contrário. Só boletins impressos coletados em amostra sorteada ou auditoria independente da urna examinam isto. | **Ponto cego dos dados públicos** | Até ~2,2 mi votos sem rastro estatístico (em logit, nunca visto). |
| H10 | Comprometer o software ou a urna antes de gerar os registros (BU, RDV e log já nascem alterados e coerentes) | Nada nos arquivos: tudo concorda entre si | A cadeia de certificados verifica até a AC emissora em 100% das urnas (1.942.246 pares seção × turno, 0 falhas, T60a), sem âncora do TSE: a raiz não é pública. Registros coerentes gerados e assinados pela própria fonte passam por todas as verificações internas (T62). Erros de verificação de assinatura do software no log seguidos de sucesso registrado, sem efeito em votos. | **Ponto cego dos dados públicos** | Até o total; sem rastro nos dados públicos. |

## Alegações públicas testadas

As alegações públicas testadas (a live de 2022, o vídeo dos "votos extras" e o relatório pericial) reproduzem quase todos os números, mas as conclusões não se sustentam (Q27 a Q30, Q42, Q51 a Q56).

_Q51 a Q56 e T66 a T70 são da rodada 8, em aberto: registro vivo, ainda não congelado._

- **Houve duas eleições no mesmo dia: Flávio venceu até as 17h00 e Lula virou na prorrogação.** Os números se reproduzem, mas o corte das 17h00 mistura fusos (as 32.025 seções encerradas antes das 17h00 locais estão em MT, AM, MS, RO, AC e RR, onde o horário legal local é 16h ou 15h) e conta como prorrogação o encerramento de rotina (17:01 a 17:15; 98% das seções fecham até 17:15). A prorrogação de fato (depois das 17:30: 7.604 seções, 2,21 mi de votantes) deu a Lula +228.095 votos de vantagem, 5,1% da margem de 4.430.191; sem essas seções, Lula lidera por 4.202.096. (Q51, Q52, T66, T09, T52)
- **98,12% dos "votos extras" do 2º turno foram para Lula, o que não fecha.** A aritmética está certa, mas o 98% é a premissa de 60% devolvida: é o mínimo possível e deixa Flávio sem nenhum voto dos extras. O mesmo método dá 370% para Bolsonaro em 2022. (Q42, T65)
- **A liberação sem biometria (8,6 milhões, quase o dobro da margem) mostra fraude, e Lula "dispara" onde ela é maior.** Foi menor que em 2022 (6,73% contra 8,06% do comparecimento). A relação com o voto em Lula tem a mesma forma no 1º turno de 2026 e em 2022 e é nula dentro do mesmo município. (Q53, Q35, T67, T53)
- **Unanimidades pró-Lula: 106 seções com 100% contra 4 de Flávio.** Os números se reproduzem; a razão é menor que em 2022 (141 contra 2). As seções com mais de 90% para Lula ficam onde ele é forte e as seções são menores (94% no Norte e Nordeste). (Q54, Q31, T68, T49)
- **O teste de Benford do primeiro dígito acusa manipulação.** Em contagens de poucas centenas por seção, o primeiro dígito não segue Benford; o desvio observado cabe nas referências simuladas sem manipulação. O teste não discrimina neste dado. (Q55, T69)
- **Urnas anteriores a 2020 deram mais votos a Lula em 2022 (live de 4/11/2022).** Deram mais (50,3% contra 46,0% no 1º turno de 2022), também dentro do município; dentro do mesmo local de votação a diferença é equivalente a zero: é localização, não modelo de urna. O 51,05% de Bolsonaro só nas UE2020 é o voto das cidades que tinham UE2020. (Q27, Q29, T47, T46)
- **Os boletins ficaram parados duas horas antes de chegar ao TSE no 2º turno de 2026.** É fato medido: nenhum recebimento das 17:07 às 19:03 (116 minutos), só em 2026, coincidindo com a prorrogação. O conteúdo do boletim é assinado na emissão e confere; a causa da pausa não está nos dados. (Q34, T52)
- **Os microdados das urnas ficaram trancados por 72 horas.** Para os arquivos por urna, não: estavam publicados na noite de 25/10. Para o CSV BWeb, este projeto não tem registro da primeira publicação; não é testável aqui. (Q56, T70)

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
| 106 seções com zero voto para Flávio, sem modelo calibrado para dizer se é muito ou pouco | 14.860 votos de Lula nessas seções | PC | T64 |
| 17 seções com certificado de outra urna que a da tabela (votos iguais) | não se traduz (votos iguais) | S4 | T60a |
| Recebimento de boletins parado das 17:07 às 19:03 (116 minutos), fato medido; coincide com a prorrogação e a regra que o acionou não está nos dados | não altera votos | S1 | T52 |

_Nenhuma tem causa demonstrada. A soma descreve o que foi achado e não limita o que pode ter passado sem alarme: há mecanismos em que centenas de milhares de votos passam sem alarme (T63)._

## Operação Veracidade Geral (V1.5, rodada 7, 28/10/2026)

**Os dados oficiais usados pelo estudo são fiéis ao que aconteceu?** O que se pôde testar não mostra adulteração; o que não se pôde testar é exatamente a parte que responderia à pergunta.

- **Cadeia de certificados em 100% das urnas (T60a):** 1.942.246 pares seção × turno de 2022 e 2026, 0 falhas, todos válidos no dia, nenhuma chave repetida. Reforça a integridade dos arquivos, não a veracidade dos votos; a raiz do TSE não é pública.
- **404 boletins de terceiros iguais ao TSE (T61):** Boletins impressos lidos por terceiros no 2º turno de 2026 (22 UFs): assinatura, cadeia e votos iguais em 404 de 404; os 404 arquivos também são iguais entre downloads independentes. Amostra de conveniência (0,08%).
- **Pontos cegos da bateria maiores do que o veredito dizia (T63):** UFs inteiras, os cinco grandes juntos, macrorregião, lote tardio, conversão de brancos e nulos, enchimento abaixo de 250 mil e deslocamento uniforme só são vistos a partir de 0,5 a 2,2 milhões de votos, ou nunca. O poder é assimétrico entre os sentidos.
- **Registros coerentes passam em tudo (T62):** Registros coerentes assinados pelo próprio gerador passam por todas as verificações internas; alterar só a tabela, ou tudo sem reassinar, é visto.
- **Zeros sem modelo calibrado (T64):** Três famílias de modelo falham a calibração; os zeros são locais de uma seção só, com menos de 1% do total, nos dois anos.

**Pontos cegos:**

- Escala de UF, região, lote ou deslocamento uniforme: sem alarme abaixo de ~0,5 a 2,2 milhões de votos (T63).
- Registros coerentes gerados por fonte comprometida antes da assinatura passam por todas as verificações internas (H10, T62).
- Poder assimétrico: em 2022, troca dispersa a favor de Lula só é vista a partir de 500 mil votos; a favor de Bolsonaro, de 50 mil (T63).
- Raiz da cadeia de certificados e teste de integridade com votos conhecidos: não obtidos.

Perguntas Q42 a Q50 em `fase3/RESPOSTAS_F3.md`; documentos em `operacao_veracidade/` (comece por `OPERACAO_VERACIDADE_GERAL.md` e `09_IMPACTO_NOS_VEREDITOS_ANTERIORES.md`).

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
| T05 | PC | Dígitos uniformes, mas o teste não tinha poder para quase nenhum mecanismo: na grade do T63 o dígito final só reage a alterações escancaradas (21% a 27% das réplicas de 'poucas seções' com 250 mil votos ou mais, onde os outros detectores já têm 100%) e é nulo nos demais. |
| T07 | S0 | Sem assinatura de enchimento. |
| T08 | S0 | Nenhum boletim antes do fim da votação. |
| T09 | S1 | Prorrogação em 6.748 seções pelo critério deste teste; virada igual com e sem. Pelo horário de encerramento depois das 17:30 (T66), a prorrogação de fato tem 7.604 seções e deu +228.095 votos de vantagem a Lula (5,1% da margem). |
| T10 | PC | Curva sem modelo de chegada validado; não decide. |
| T11 | PC | Idem. |
| T12 | S1 | Associação some ao controlar idade. |
| T13 | M | Poder dos testes (simulação). |
| T13b | M | Poder dos testes de log. |
| T14 | S4 | Log com contagem diferente do comparecimento: 16 seções-turno em 2026 (113 votos); 153 em 2022 (5.287 votos sem registro). |
| T15 | S4 | Imagem do boletim diferente do boletim digital em RS 88013/2/199 (2022, 92 votos); em 2026, 1 caso compatível com contingência registrada. |
| T16 | S0 | Assinaturas válidas até a AC emissora (cadeia conferida em 100% das urnas no T60a); a raiz do TSE é ponto cego. |
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
| T56 | S1 | Brancos e nulos do 1º turno → Lula no estimador (C06); explicado em grande parte: excesso no 1º turno de 2026 onde Lula é forte (~0,47 mi) e menos 2º turno de governador (T57, ~0,69 mi); resto uniforme; fluxo individual não identificável. |
| T57 | S1 | 2º turno de governador eleva nulos de presidente (+1,58 ponto em 2022, +0,78 em 2026); 53% dos votos nessas UFs em 2022 contra 8% em 2026: ~0,69 mi da queda de nulos; resto uniforme. |
| T58 | S1 | Nulos com número de governador no campo de presidente explicam o excesso de nulos nas UFs com governador no 2º turno e a marca do 1º turno de 2026 onde Lula é forte (erro de campo). |
| T59 | M | Calibração do C06 com origem conhecida: acerta 14 (90%) e 70 (69%) de 2026, erra 55, 12 e 15; magnitudes de fluxo só como direção. |
| T60a | S4 | Cadeia de certificados verifica em 1.942.246 de 1.942.246 pares seção × turno (0 falhas). Lacunas objetivas pequenas, sem efeito em votos: 98 certificados emitidos depois da validade do certificado público da AC URNA; certificado de outra urna que a da tabela em 17 seções de 2026 e 22 de 2022; a raiz não é pública. |
| T60b | M | Controles do verificador: 0 falso positivo; mutações rejeitadas em 40 de 40; a assinatura do arquivo sozinha não detecta alteração, o hash detecta; só a cadeia rejeita certificado forjado. |
| T61 | S0 | 404 boletins impressos lidos por terceiros iguais à tabela e ao BU do TSE, com assinatura e cadeia válidas; 404 arquivos iguais entre downloads independentes (amostra de conveniência, 0,08%). |
| T62 | M | Identificabilidade: registros coerentes assinados pelo próprio gerador passam por todas as verificações internas; alterar só a tabela, ou tudo sem reassinar, é visto. |
| T63 | M | Poder da bateria contra 15 mecanismos: visto a partir de 25 a 50 mil votos em seções, locais, zonas e municípios; só a partir de 0,5 a 2,2 mi, ou nunca, em UFs, cinco grandes juntos, região, lote, conversão de brancos e nulos, enchimento e deslocamento uniforme; poder assimétrico entre sentidos. |
| T64 | PC | Zeros: três famílias de modelo falham a calibração; os zeros são locais de uma seção só com menos de 1% do total, em 2022 e em 2026. |
| T65 | S1 | O '98,12% dos votos extras' do vídeo é a premissa de 60% devolvida (mínimo possível); o mesmo método dá 370% para Bolsonaro em 2022; a abstenção também caiu em 2022; resíduo acima do proporcional de sinal conhecido (Lula +3,68 mi em 2026, Bolsonaro +1,99 mi em 2022). |
| T66 | S1 | Divisão por hora de encerramento: números do relatório reproduzidos, mas o corte das 17h00 mistura fusos e o bloco de rotina (17:01 a 17:15, 339 mil seções); a prorrogação de fato (depois das 17:30) deu +228 mil a Lula; dentro do município, +0,2 ponto. |
| T67 | S1 | Liberação sem biometria: 8.632.488 (6,73%), menor que em 2022 (8,06%); relação com Lula igual no 1º turno e em 2022 e nula dentro do município. |
| T68 | S1 | Unanimidade: 106 contra 4 reproduzido; razão menor que em 2022; concentrada no Norte e Nordeste. |
| T69 | S1 | Benford do primeiro dígito: desvio explicado pelo limite das contagens; cabe entre as referências simuladas; teste sem poder neste dado. |
| T70 | PC | Disponibilidade dos microdados: arquivos por urna publicados na noite de 25/10; CSV BWeb não testável aqui. |
| T44 | S3 | Salvador: virada de Lula ~30 mil votos acima do previsto, em todas as 19 zonas; única capital desviante entre as 27 (z 6,1); não explicada pelo perfil do eleitorado; Fortaleza tem desvio por seção de tamanho parecido no sentido oposto. |
