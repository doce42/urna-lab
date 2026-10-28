# Conclusão do estudo (baseline V1.0, com atualização da Fase 2)

> **Estado:** **baseline V1.0 aprovada** pelo responsável em 28/10/2026, depois da **revisão independente R1** (Codex). Os critérios de [`revisoes/README.md`](revisoes/README.md) foram conferidos: achados respondidos ou adiados, `make verificar` passando, proveniência completa. A conclusão original da rodada 1 (**V1.0-rc1**) está congelada, sem alteração, em [`rodadas/rodada-1/CONCLUSAO.md`](rodadas/rodada-1/CONCLUSAO.md) e na tag `rodada-1`; esta versão está congelada em [`rodadas/rodada-2/`](rodadas/rodada-2/) e na tag `v1.0`. As frases que mudaram, e por quê, estão em [Mudanças em relação à V1.0-rc1](#mudanças-em-relação-à-v10-rc1). Resultados novos entram na Fase 2 (rodada 3) sem reescrever esta versão.

**Escopo:** eleição presidencial brasileira de 2026, 1º turno (04/10) e 2º turno (25/10), com 2022 como referência histórica. Não cobre outros cargos nem outros anos. **Fonte:** só dados oficiais do TSE: tabelas de dados abertos e os arquivos gravados por cada urna (boletim `bu.dat`, registro digital do voto `RDV`, log, imagem do boletim e assinaturas). São 51.846 arquivos, cerca de 405 GB, com SHA-256 no manifesto. Só 331 deles tinham hash SHA-512 oficial publicado pelo TSE para conferir, e todos conferiram.

A pergunta "houve fraude?" reúne hipóteses diferentes: em que fase, por qual mecanismo, em que escala, com que intenção. Esta conclusão responde só ao que os testes alcançam, em três níveis: **o que os registros disponíveis mostram de forma exata**, **o que a estatística mostra e com que alcance**, e **o que fica fora do alcance dos dados públicos**. Cada afirmação aponta para o teste do [registro](testes/registro.json) que a sustenta.

## Atualização da Fase 2 (28/10/2026, concluída na rodada 3, V1.1)
Resultados novos, com o que significam em votos. A baseline V1.0 abaixo permanece como foi congelada (`rodadas/rodada-2/`).
- **Crescimento de Lula entre turnos (C06, T37):** em 2026 Lula somou +10,33 mi de votos (adversário +3,69 mi) com +2,92 mi de comparecimento; em 2022, +3,07 mi e +7,11 mi, com +0,56 mi. As contas fecham exatamente. A razão "4:1 para Lula" entre abstencionistas é estimativa frágil na magnitude: sob heterogeneidade sintética varia de 1,7 a 11,8 (verdade 3 a 4), erro de ±0,5 a ±1,5 mi de votos. A ordem em 2026 e o contraste com 2022 resistem.
- **Hipótese de enchimento para Lula (T38):** a assinatura prevista, comparecimento subindo nas seções pró-Lula atípicas, não aparece. Excesso de cerca de 740 votos (2026) e 2.600 (2022) contra a margem de 4,43 mi. A assimetria de cauda do T02 persiste, sem causa, e não exclui troca em urna sem alteração de comparecimento.
- **Verificação de 20 seções (T39):** nenhuma divergência objetiva nova nas 19 com arquivos de urna; vale só para a amostra. Não houve confronto independente (sem material externo disponível).
- **Fase 2 completa (V1.1):** o E02 original superestimava o agrupamento (766 e 683 locais viram 102 e 55 após corrigir a correlação dentro do local); a regra do T13 só enxerga troca a favor de Lula (10% dos válidos em 1% das urnas: 100% contra 0% no sentido contrário); a diferença de eleitorado do exterior (−495 e −525) está explicada (423 de seções não instaladas mais 72 e 30 de boletins só nos arquivos das urnas); em 200 seções e 200 certificados sorteados tudo concorda, mas a âncora de certificados e fontes externas continuam sem verificação. A assimetria de cauda do T02 é estatisticamente real, sem causa, e em 2022 concentrada na capital de São Paulo.

## Operação Veracidade Geral (28/10/2026, rodada 7, V1.5)
Auditoria adversarial dos dados e do próprio veredito. Pergunta: **os dados oficiais usados pelo estudo são fiéis ao que aconteceu?** Resposta direta: o que se pôde testar não mostra adulteração; o que não se pôde testar é exatamente a parte que responderia à pergunta. Testes T60a a T65, perguntas Q42 a Q50.
- **Cadeia de certificados em 100% das urnas (T60a):** 1.942.246 pares seção × turno, 0 falhas, todos válidos no dia, nenhuma chave repetida (antes, 200 seções). Reforça a integridade dos arquivos, não a veracidade dos votos; a raiz do TSE não é pública.
- **404 boletins de terceiros iguais ao TSE (T61):** 2º turno de 2026, 22 UFs, assinatura, cadeia e votos iguais em 404 de 404; os 404 arquivos são idênticos entre downloads independentes. Amostra de conveniência (0,08%).
- **Pontos cegos (T62, T63):** escala de UF, região, lote ou uniforme passa sem alarme abaixo de ~0,5 a 2,2 milhões de votos; registros coerentes gerados pela própria fonte passam em todas as verificações internas; o poder, medido sobre uma base que pode já conter alteração, é assimétrico entre os sentidos.
- **Revisões do veredito:** H7 passa a "não determinado (ponto cego)"; T05 passa a ponto cego (o dígito final não tinha poder); a frase "deixariam sinais muito maiores" passa a valer só para os mecanismos em que a bateria tem poder; "restam dois caminhos" passa a "restam caminhos fora do alcance". Lista completa em [`operacao_veracidade/09_IMPACTO_NOS_VEREDITOS_ANTERIORES.md`](operacao_veracidade/09_IMPACTO_NOS_VEREDITOS_ANTERIORES.md).

Relatório executivo: [`operacao_veracidade/OPERACAO_VERACIDADE_GERAL.md`](operacao_veracidade/OPERACAO_VERACIDADE_GERAL.md). Simulações: [`03_SIMULACOES_ADVERSARIAIS.md`](operacao_veracidade/03_SIMULACOES_ADVERSARIAIS.md). Criptografia: [`02_AUDITORIA_DOCUMENTAL_CRIPTOGRAFICA.md`](operacao_veracidade/02_AUDITORIA_DOCUMENTAL_CRIPTOGRAFICA.md).

## Rodada 8 (aberta, 28/10/2026): relatório pericial e alegações públicas
Rodada **em andamento, não congelada**: testes T66 a T70, perguntas Q51 a Q56, pré-registro `fase3/PREREG_RELATORIO_PERICIAL.md`. Não muda a resposta central nem os pontos cegos.
- **Alegações públicas testadas** (a live de 2022, o vídeo dos "votos extras" e o relatório pericial): reproduzem quase todos os números, mas as conclusões não se sustentam (Q27 a Q30, Q42, Q51 a Q56).
- **Prorrogação (T66, T09, T52):** o corte das 17h00 do relatório mistura fusos (as 32.025 seções encerradas antes das 17h00 locais estão em MT, AM, MS, RO, AC e RR) e conta o encerramento de rotina (17:01 a 17:15) como prorrogação. A prorrogação de fato (encerramento depois das 17:30: 7.604 seções, 2,21 mi de votantes) deu a Lula +228.095 votos de vantagem, 5,1% da margem de 4.430.191; sem essas seções, Lula lidera por 4.202.096.
- **Biometria, unanimidade, Benford, microdados (T67 a T70):** liberação sem biometria menor que em 2022 e sem relação com Lula dentro do município; razão de unanimidade menor que em 2022; Benford do primeiro dígito sem poder neste dado; arquivos por urna publicados na noite de 25/10 (o CSV BWeb não é testável aqui).

## A pergunta e a resposta (28/10/2026, revista na V1.5)
**A apuração presidencial de 2026 tem sinais de fraude capaz de mudar o resultado?** Não encontramos sinal de fraude nos mecanismos que os dados públicos conseguem examinar, com o poder medido para cada um.
- **Escala:** inverter o resultado exigiria trocar ~2,2 milhões de votos de lado.
- **O que a bateria vê:** troca dispersa, em poucas seções, em locais, zonas ou municípios (fora os 5 maiores), de dezenas de milhares de votos (a partir de 25 a 50 mil, T63), e numa grande cidade, uma por vez, a partir de 2% dos válidos (T44). Alteração depois da publicação e troca na totalização foram contrariadas.
- **O que ela só vê em escala grande ou nunca:** UFs inteiras, os cinco grandes municípios juntos, macrorregião, lote tardio, conversão de brancos e nulos, enchimento abaixo de 250 mil e deslocamento uniforme, a partir de ~0,5 a 2,2 milhões de votos, ou nunca (T63). O poder é assimétrico entre os sentidos.
- **Anomalias reais:** as encontradas somam dezenas de milhares de votos, sem causa demonstrada; a maior é Salvador, com ~30 mil. Isso descreve o que foi achado e não limita o que pode ter passado sem alarme.
- **O que resta fora do alcance:** um deslocamento pequeno e uniforme em quase todas as urnas (H9), uma alteração da urna antes de gerar os registros (H10) e as alterações de escala listadas acima. Só boletins impressos de uma amostra sorteada de seções, uma auditoria independente da urna e a raiz da cadeia de certificados os examinam.
- **Zeros de votos (H7):** não determinado; nenhum modelo de cauda baixa calibrou (T41, T64).

Hipótese por hipótese, com o sinal de cada teste, em [`fase3/VEREDITO_2026.md`](fase3/VEREDITO_2026.md).

## Fase 3 (concluída em 28/10/2026, V1.3; histórico da revisão abaixo)
> **Estado:** concluída e congelada na rodada 5 (V1.3) com aprovação do responsável. Histórico: a F3 foi encerrada e congelada como V1.2 (rodada 4, tag `v1.2`) **antes** de uma auditoria científica. A auditoria ([`fase3/AUDITORIA_F3.md`](fase3/AUDITORIA_F3.md)) encontrou afirmações acima da evidência e falhas de registro, e a fase voltou a **em revisão**. O texto congelado está em `rodadas/rodada-4/CONCLUSAO.md`. Abaixo, primeiro o que mudou na revisão, depois o texto da V1.2 com as frases corrigidas marcadas. Não há conclusão definitiva da F3.

**O que a revisão mudou (investigações I1 a I3, pré-registro em [`fase3/PREREG_REVISAO.md`](fase3/PREREG_REVISAO.md)):**
- **Alcance da detecção (I1, corrigido pelo A2):** os votos das simulações são sintéticos, não encontrados nos dados. Contando só alarmes no sentido certo, a bateria:
  - **Detecta:** troca dispersa de ~123 mil votos (10% dos válidos em 1% das seções), nos dois sentidos. Também ~62 mil votos concentrados em locais ou municípios de até ~5 mil seções, só pelo E02.
  - **Não detecta:** ~25 mil votos em nenhuma forma testada; ~62 mil dispersos; troca no município inteiro das 5 maiores cidades (São Paulo, Rio, Brasília, Fortaleza, Salvador), nem a 10%, que chega a ~700 mil votos em São Paulo.
  - **Incerta:** região a 5%.
  - **Limites de leitura:** o T02 é cego a trocas que cobrem um município ou uma região inteiros. Um sinal do E02 não identifica sozinho o beneficiário. **Uma manipulação abaixo desses tamanhos, nessas cidades ou de mecanismo não testado não pode ser excluída.** *(A versão anterior desta frase contava alarmes em qualquer direção e excluía as 5 maiores cidades.)*
- **Zeros (I2):** nenhum modelo de frequência de zeros passou na calibração. **Nem excesso nem ausência de excesso foram demonstrados.** Os arquivos dessas seções conferem em todas, inclusive a seção de 2022 cujo BU não tinha sido lido (verificada depois: boletim do Sistema de Apuração, igual à tabela publicada).
- **Arquivos de 2022 (verificação documental):** 173 arquivos assinados pelas urnas (RDV, log e imagem do BU de 64 seções, 54 delas do exterior) não estão no pacote de dados abertos do TSE, nem na cópia baixada pelo projeto nem na do DataUrnas-BR. O boletim dessas 64 seções está presente e confere com a tabela publicada. Além disso, 159 seções-turno de 2022 apuradas pelo Sistema de Apuração tinham ficado fora das verificações por arquivo do projeto (lacuna do leitor). Lidas uma a uma depois, todas conferem com a tabela publicada, com assinatura válida. Essa conferência é interna, da mesma origem.
- **Locais atípicos (I3):** com o entorno como referência, há 61 (2026) e 84 (2022) locais significativos, cerca de 0,1% do total, mas a lista depende do método. Os locais de São Paulo de 2022 não são atípicos contra a própria zona: o deslocamento é regional e a causa não é conhecida.
- **Reconciliação independente de 2022 (A1):** as 191 e 176 seções do Brasil sem par no DataUrnas-BR foram explicadas: 27 do Sistema de Apuração, 333 numa lacuna do acervo do terceiro em 5 zonas da Bahia e 7 que ele registra fora do banco. Os boletins delas conferem com a tabela. Cobertura independente em 2022: 99,96%. O 2º turno de 2026 não tem comparação independente.

**Perguntas que continuam abertas** (detalhe e evidência por item em [`fase3/INVENTARIO.md`](fase3/INVENTARIO.md)):
- **Curvas de apuração (C1, C1a, C1b, C2, P4):** viradas, periodicidade, trechos lineares e diferenças entre 2022 e 2026. Só foram descritas na ordem de recebimento dos boletins, uma reconstrução que não é a curva divulgada. Não há modelo de chegada validado nem snapshots datados, então nada foi explicado, refutado ou comprovado.
- **Zeros de votos (Z1):** sem modelo calibrado. Nem excesso nem normalidade estatística foram demonstrados. O modelo subestima toda a cauda baixa (0 a 5 votos), com o mesmo formato em 2022 e 2026.
- **Zona 251 de São Paulo, 2022 (P14, P20):** o desvio está no nível da zona (2º maior z médio das 58 zonas da capital), não dos locais. A causa não foi investigada.
- **Autenticidade externa (P3, P6, P11, P21, A173):** a cadeia de certificados foi conferida só até a AC emissora. Não há boletins de terceiros nem versões datadas dos arquivos. A situação dos 173 arquivos ausentes do pacote não foi confirmada por outro canal do TSE.
- **Transferência individual de votos entre turnos (M1):** não identificável com dados agregados. Os limites de Fréchet admitem de ~0 a 1,7 mi para a razão entre abstencionistas.
- **Mecanismos sem poder medido (P2, P18):** trocas abaixo de ~25 mil votos, trocas que preservam medianas ou mexem no comparecimento, o município inteiro das grandes cidades e alterações anteriores à geração do boletim.

**Texto da V1.2, com correções:** duas sessões, sem novos dados do TSE. A baseline V1.0 e a V1.1 permanecem congeladas.
- **Decodificação independente (T43):** a base do projeto e os votos decodificados dos BUs pelo DataUrnas-BR (terceiro) coincidem em todas as seções comparadas: 0 diferenças em 119,3 mi de votos (2026, 1º turno) e em cerca de 118 mi por turno (2022). Origem comum (TSE) e uma só versão de publicação continuam como limite.
- **Curvas de apuração (T40):** nenhum modelo de chegada testado (cinco nulos, até UF × hora de fechamento × tamanho) reproduz a ordem real nem mesmo em 2022. As curvas não permitem concluir compatibilidade nem incompatibilidade; T10 e T11 valem como descrição. 2026 e 2022 diferem: em 2026 (2º turno) a liderança muda duas vezes, em 2022 o adversário lidera até 67,6% apurado.
- **Zeros de votos (T41):** os zeros de Flávio (79 e 106 seções) e de Bolsonaro em 2022 (160 e 141) ficam 1,2 a 1,7 vez acima do esperado por um modelo de local de votação; o controle com Lula erra por 2 vezes. *(Corrigido na revisão: "não há evidência de excesso" excedia o teste; ver I2.)* Dezenas a poucos milhares de votos em jogo, conforme o modelo; 0 divergências entre BU, RDV, imagem e tabela, exceto 1 seção de 2022 com BU não lido.
- **Regra do T13 simétrica (P18):** com duas caudas, 10% dos válidos movidos em 1% das urnas (~125 mil votos) são vistos em 30 de 30 réplicas nos dois sentidos; 5% (~62 mil votos), em 0 de 30. Correção minha: na F2 eu havia escrito ~250 mil votos. *(Revisão: esse alcance vale só para troca dispersa; ver I1.)*
- **Dependência espacial (T42):** Moran's I de 0,16 a 0,20 nos resíduos municipais: há dependência espacial; o teste não distingue a causa.
- **São Paulo 2022 (P20):** o deslocamento é de locais de votação inteiros; com controle de tamanho e histórico, 4 das 29 seções continuam atípicas.
- **Sem solução com estes dados:** certificados AC URNA v2 e AC RAIZ UE, snapshots históricos e boletins de terceiros com dados primários (P4, P6, P11, P21). Nenhum teste chegou às classes E ou F.

## Resposta curta

- **Os registros:** nos registros públicos examinados, as igualdades e verificações listadas abaixo se confirmam. As duas tabelas do TSE conferem seção a seção. A soma das urnas confere com o total oficial. Os arquivos de cada urna conferem com a assinatura que a própria urna apresenta. A recontagem pelo RDV dá o mesmo boletim.
- **Nenhum teste chegou às classes E ou F:** nenhum registrou evidência de possível irregularidade ou de manipulação. Há anomalias estatísticas pequenas e exploratórias (classe B), sem causa identificada e sem direção que favoreça um candidato.
- **Isso não demonstra ausência de fraude.** Três limites ficam abertos:
  - a autenticidade das chaves das urnas não foi validada até uma raiz do TSE;
  - o software que roda na urna não é auditável a partir destes arquivos;
  - os testes estatísticos só enxergam as formas de intervenção que deixam rastro distinguível nos dados. Uma alteração igual em todas as urnas, ou absorvida pelos ajustes dos modelos, não seria vista.

## 1. O que os registros disponíveis mostram de forma exata

| O que foi conferido | 1º turno | 2º turno | Teste |
|---|---|---|---|
| Boletim de Urna na Web = votação por seção, seção × votável | 3.800.511 pares iguais, 0 diferenças | 1.931.103 pares iguais, 0 diferenças | T01 (método v2) |
| Soma das urnas = total oficial (BR, UFs, exterior) | 638 de 638 itens de voto e comparecimento iguais; eleitorado do exterior com diferença de −495 e −525 eleitores, sem explicação, que não envolve votos | | T32 |
| Assinatura e hash do BU e da lista de arquivos | todas as 499.176 urnas eletrônicas com arquivos | todas as 499.178 | T14, T16 |
| Log com assinatura conferida | 499.176 | 499.177 (1 log na lista assinada e não publicado) | T14, T36 |
| Recontagem pelo RDV = boletim | 499.176 (1 RDV obtido do site de resultados) | 499.180 (inclui recuperação de dados) | T17 |
| `bu.dat` (o que é somado) = RDV = publicado | todas as urnas eletrônicas | todas | T17b |
| Urna do boletim = urna do cadastro de correspondências | 499.206 de 499.206 | 499.205 de 499.205 | T34 |

**Sobre a assinatura:** "confere" quer dizer que os bytes de cada arquivo conferem com a chave contida no certificado que a própria urna apresenta. O certificado não foi validado até uma raiz do TSE, porque a cadeia não está no material público obtido. Assinaturas também não impediriam a omissão de arquivos nem a troca de um pacote inteiro por outro validamente assinado. Nenhum desses eventos foi identificado, mas eles ficam fora do que esta verificação prova (R1-01). O verificador Ed521 foi endurecido em 28/10, porque aceitava entradas degeneradas (R1-02). Refeita com o verificador corrigido, a verificação continua válida em todas as listas (499.176 e 499.178), e nenhuma chave real é degenerada.

**Contas que não fecham exatamente (T36):** foram 186 casos no 1º turno e 75 no 2º, em cerca de 499 mil urnas por turno. Os totais gravados conferem, mas as causas têm graus diferentes de demonstração:

| Grau | 1º turno | 2º turno |
|---|---|---|
| Demonstrado: o próprio dado mostra a causa | 0 | 1 (log de SP na lista assinada e não publicado) |
| Declarado pelo TSE no cadastro de correspondências | 38 | 30 |
| Compatível: um evento no log combina, mas não prova a diferença inteira | 5 | 3 |
| Inferido: uma confirmação sem voto computado | 142 | 41 |
| Sem explicação | 1 (RJ 60011/8/61, log corrompido pela própria urna; hash, assinatura e totais conferem) | 0 |

**O que isso sustenta:** os registros examinados (tabelas publicadas, boletins, RDV e logs disponíveis) são coerentes entre si, e a soma deles é o total divulgado.
**O que não sustenta:** que cada urna registrou corretamente o que cada eleitor digitou. Todos esses registros saem do mesmo equipamento e do mesmo software, e coerência entre eles não é verificação independente da escolha individual.

## 2. Evidência estatística e seu alcance

**Resultados sem sinal relevante, cada um com seu limite:**
- **T03:** a virada quase não depende da hora de chegada do boletim (r = +0,004). Em 2022 o valor foi −0,028, pequeno e de sinal oposto. O intervalo não considera a dependência entre seções do mesmo município, e por isso é otimista.
- **T04:** as urnas trocadas entre turnos não mostram diferença clara. Isso **não** prova que votaram igual, porque falta uma margem de equivalência definida antes.
- **T05, T27:** os dígitos finais não mostram excesso. No T27, só o comparecimento chegou a ser testado.
- **T07, T25:** sem assinatura de enchimento de urna.
- **T21, T22:** sem padrão de percentuais inteiros nem de fraude incremental. No 2º turno, os dados de um candidato determinam os do outro, então não contam como indícios independentes.
- **T10, T11:** a curva da apuração segue a reconstrução feita a partir do 1º turno e da virada do próprio município, com desvio máximo de 0,08 ponto percentual depois das 19h. Essa reconstrução usa dados do 2º turno, então não é previsão independente, e uma intervenção comum a um município inteiro seria absorvida.
- **T30:** nenhuma urna tem o último evento lido do log depois do encerramento do boletim, com tolerância de 60 segundos.
- **T33:** a mesma versão do software aparece declarada no log de todas as urnas. Isso não demonstra que o programa executado seja o mesmo.

**Anomalias registradas (classe B, exploratórias, sem causa identificada):**
- **T02:** 46 seções se afastam mais de 5 desvios das vizinhas (33 pró-Lula e 13 pró-Flávio), contra cerca de 17 esperadas pelo modelo t ajustado. Em 2022 o excesso pró-Lula também aparece. É um sinal de que o modelo de virada se ajusta mal em algumas seções, não de causa.
- **T28, 1º turno:** 13 urnas tiveram mais habilitações sem biometria nos últimos 30 minutos que no resto do dia. Somam cerca de 140 votos, em 7 estados, sem direção de voto. São achados a explicar, não falsos positivos. Em 2022 foram 23 e 25 urnas.
- **E02 e E03:** divergências agrupadas por local de votação, com lados equilibrados. Os p-valores supõem independência entre seções do mesmo local.

**Poder: o que os testes conseguiriam ver (T13, T13b, T23).** Simulações sobre os próprios dados reais mostram que os testes sinalizam algumas formas de intervenção:
- trocas concentradas em parte das urnas;
- trocas em estados inteiros a partir de 1% a 2% dos válidos;
- enchimento com eleitores ausentes;
- rajadas grandes de habilitação sem biometria no fim do dia.

O T13 é uma **grade de 37 cenários, com uma realização cada**: 25 foram sinalizados, e nenhum dos 3 de troca uniforme nacional. Isso descreve a grade, não uma probabilidade geral de detecção. **Não se pode afirmar que uma intervenção capaz de mudar o vencedor "muito provavelmente apareceria"**, como dizia a V1.0-rc1. Intervenções heterogêneas, alinhadas ao perfil do eleitorado ou absorvidas pelos ajustes, não foram simuladas. Medir o poder com réplicas e mecanismos especificados é pergunta da Fase 2.

## 3. Fora do alcance dos dados públicos

Detalhes em [AUTOAUDITORIA §6](AUTOAUDITORIA.md):
- **Software da urna:** só se vê o que a urna gravou, não o que ela executou. Uma alteração igual em todas as urnas, que produza arquivos coerentes e assinados, passaria por todos os testes deste estudo.
- **Autenticidade das chaves:** a cadeia de certificados até a raiz não foi validada.
- **Especificação de 2026:** a obtida é a de 2022. Ela confere com a estrutura lida, e os campos novos de 2026 foram validados pelos totais.
- **Máquinas de carga:** 3 no 1º turno e 2 no 2º estão sem log do GEDAI publicado (T35). Isso é ausência de dado, sem inferência.
- **Comportamento do eleitor:** "abstencionistas do 1º turno foram 4:1 para Lula" é estimativa sob o pressuposto de taxas homogêneas dentro de cada UF (C06), não fluxo observado. O voto individual é secreto.
- **Garantia probabilística de auditoria:** um limite de risco, como na literatura de auditorias pós-eleitorais, exige trilha independente e protocolo de amostragem que estes dados não oferecem.
- **Reprodução a partir de clone limpo:** não foi executada ponta a ponta.

## Mudanças em relação à V1.0-rc1

| Frase da V1.0-rc1 | Agora | Achado |
|---|---|---|
| "Não foi encontrada evidência de manipulação" | Nenhum teste chegou às classes E/F, com universo, hipóteses alcançadas e validações abertas declarados | R1-19 |
| "O resultado publicado é exatamente o que as urnas gravaram e assinaram" | Os registros disponíveis examinados apresentam as igualdades listadas, sob os pressupostos declarados | R1-19, R1-01 |
| "As fraudes que os testes conseguiriam ver não aparecem" | Descrição da grade simulada e do que ela cobre | R1-04 |
| T01 "voto a voto" | Refeito seção × votável, 0 diferenças | R1-18 |
| Logs válidos em "todas as 499.178" no 2º turno | 499.177 (1 não publicado) | R1-15 |
| "Nenhum voto depois do encerramento" | Último evento lido do log até o encerramento + 60 s | R1-11 |
| "O software foi o mesmo" | A mesma versão declarada no log | R1-11 |
| Uma fraude localizada que mudasse o vencedor "muito provavelmente" apareceria | **Retirada**: a grade não sustenta essa probabilidade | R1-04 |
| "13 urnas... falsos positivos" (T13b) | Detecções na referência não modificada: achados a explicar | R1-05 |
| T36: "185 com explicação operacional" | Graus: demonstrado, declarado, compatível, inferido | R1-12 |
| "4:1" como padrão | Estimativa condicionada ao modelo | R1-06 |
| Hash oficial "conferido" | 331 arquivos com hash oficial conferido; 173 marcados por engano, porque o TSE não publicou hash | R1-03 |
| 3 máquinas sem log do GEDAI | 3 no 1º turno e 2 no 2º | R1-11 |

## Como discordar

Tudo é reproduzível: código MIT, documentos CC BY 4.0, comandos no `Makefile` e no [registro](testes/registro.json). Uma contestação a qualquer teste entra no campo `provas` dele, com o resultado (resistiu, caiu, ajustado), e não apaga a versão anterior. Ver [`RODADAS.md`](RODADAS.md) e [`CONTRIBUTING.md`](CONTRIBUTING.md).
