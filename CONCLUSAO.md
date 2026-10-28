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
