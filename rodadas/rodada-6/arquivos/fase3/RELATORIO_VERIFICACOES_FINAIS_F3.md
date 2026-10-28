# F3: verificações finais A1, A2 e A4 (28/10/2026)

**Pré-registro:** adendo em `fase3/PREREG_REVISAO.md`, escrito antes de rodar.

**Execuções:**
- **A1:** `fase3/ver_a1.py`, uma execução, com a segunda contagem no mesmo script como validação.
- **A2:** `fase3/rev_a2_poder.py`, com 2026 como execução principal e 2022 como validação.
- **A4:** checagem determinística, com resultado em `fase3/resultados/a4_t28.json`.

**Sem:** correção, repetição, subagente, download, reprocessamento nacional, publicação ou deploy. As versões congeladas não foram tocadas.

**Os votos das simulações do A2 são sintéticos.** Medem o que a bateria veria se uma troca daquele tamanho existisse; não são votos encontrados nos dados.

## A. A1: seções de 2022 sem par no DataUrnas-BR
O resultado por seção está em `fase3/resultados/a1.csv` e os totais em `a1.json`.

| Categoria (regra fixa, na ordem) | 1º turno | 2º turno | Boletim local × tabela |
|---|---|---|---|
| Sistema de Apuração (SA22) | 17 | 10 | iguais |
| Seção agregada a outra | 0 | 0 | — |
| No DataUrnas-BR sem nenhum voto de Presidente | 167 | 166 | iguais |
| Fora do DataUrnas-BR, com arquivos no pacote local ("seção fora do banco" na lista dele) | 7 | 0 | iguais |
| Sem arquivos no pacote local | 0 | 0 | — |
| **Total** | **191** | **176** | **367 lidos, 0 divergências** |

- **Bahia:** as 333 seções da categoria 3 estão todas na Bahia, em 5 zonas e 5 municípios, os mesmos nos dois turnos. São 167 das 769 seções dessas zonas na tabela do DataUrnas-BR, e nenhuma tem voto nem total por cargo no acervo dele.
  - **Conclusão permitida:** é uma lacuna do acervo do terceiro, de motivo não identificado. Não é ausência no TSE: o pacote local tem os arquivos, e os boletins conferem com a tabela.
- **Validação (segunda contagem):** o cruzamento das listas de seções dá os mesmos totais: 191 e 176 sem par, todas com arquivos no pacote, 167 e 167 na tabela de seções do DataUrnas-BR. No 2º turno, a 167ª é uma do Sistema de Apuração.
- **Cobertura da comparação com implementação independente em 2022:**
  - 1º turno: 470.819 de 471.010 seções do Brasil.
  - 2º turno: 470.834 de 471.010.
  - Em ambos: 99,96%.
  - As 191 e 176 restantes foram conferidas só pelo leitor do projeto, mais o texto impresso no caso do Sistema de Apuração, com 0 divergências.
  - O exterior (1.018 seções) não está no acervo dele.
- **Exceções não resolvidas:** o motivo da lacuna da Bahia no DataUrnas-BR.

## B. A2: poder no sentido correto, grandes municípios e E02 completo
Resultados completos em `fase3/resultados/rev_a2_2026.json` e `rev_a2_2022.json`. Leitura pelo critério pré-registrado, com limiar calibrado e só o sentido correto:
- **D (detectável):** pelo menos 90%, limite inferior do IC de Wilson acima de 75% e falso alarme de até 10%.
- **N (não detectável):** limite superior do IC abaixo de 25%.
- **I (incerta):** o resto.

**Falso alarme no sentido correto:** 0/30 em 2026 e em 2022, com IC de 95% até 11%. **Na regra "qualquer alarme":** 1/30 (2026) e 3/30 (2022).

**2026, 2º turno**, com detecção correta em réplicas de 30. Onde há duas entradas, a primeira é o sentido "adversário → Lula" e a segunda "Lula → adversário". Votos movidos por réplica entre parênteses:

| Mecanismo | 2% | 5% | 10% |
|---|---|---|---|
| Disperso | 0, 0 (N) (~25 mil) | 0, 0 (N) (~62 mil) | 30, 30 (D) (~123 mil) |
| Locais inteiros | 0, 0 (N) | 30, 30 (D) | 30, 30 (D) |
| Municípios inteiros, até ~5 mil seções | 0 a 1 (N) | 30, 30 (D) | 30, 30 (D) |
| Região contígua, E02 simples | 0, 0 (N) | 26, 23 (I) | 30, 30 (D) |
| Região contígua, E02 completo | 0, 0 (N) | 27, 25 (I) | 30, 30 (D) |
| **5 maiores municípios inteiros, E02 simples** | 3, 0 (I/N) (31 mil a 140 mil) | 13, 21 (I) (77 mil a 348 mil) | 24, 24 (I) (155 mil a 696 mil) |
| **5 maiores municípios inteiros, E02 completo** | 0, 0 (N) | 1, 0 (N) | 10, 13 (I) |

**E02 completo por cidade**, a 10% e 6 réplicas por cidade e sentido, de 2026:

| Cidade | Votos movidos | Detecção |
|---|---|---|
| São Paulo | 696 mil | 0/6 e 1/6 |
| Rio de Janeiro | 368 mil | 4/6 e 6/6 |
| Brasília | 180 mil | 0/6 e 0/6 |
| Fortaleza | 155 mil | 0/6 e 0/6 |
| Salvador | 158 mil | 6/6 e 6/6 |

Brasília é o único município do DF, e a regressão por UF, ajustada com as seções alteradas, absorve a troca inteira. São Paulo pesa cerca de 25% das seções do estado.

**2022 (validação):**
- **Mesmo padrão:** os mesmos D e N.
- **Região a 5%:** 30/30 no sentido para Lula; no outro, 27/30 (simples, I) e 28/30 (completo, D).
- **Grandes municípios a 10%:** E02 completo 17 e 9 de 30; simples 21 e 24 de 30; todos I.

**Respostas às cinco perguntas do A2:**
1. **A regra considera o sentido correto?** A regra do I1 não considerava, e contava também T2 e T4. Com a regra correta, os casos "detectáveis" do I1 se mantêm, exceto a região a 5%, que passa a incerta. Era o que a auditoria tinha antecipado, agora com E02 completo e simples.
2. **Grandes municípios:** a afirmação "troca concentrada em municípios é detectada a partir de ~62 mil votos" vale só para municípios de até ~5 mil seções. No município inteiro das 5 maiores cidades, a bateria não detecta com confiabilidade nem 10% dos válidos, isto é, 155 mil a 696 mil votos. Em Brasília e Fortaleza não detecta nada pelo E02 completo.
3. **E02 simples × completo:** iguais nos mecanismos do I1. Nas grandes cidades, o completo detecta menos, porque inclui o tamanho do município e outras covariáveis e é ajustado por UF com os dados alterados. Como a F2 usa o completo nas contagens de locais, é o resultado do completo que vale para as conclusões publicadas.
4. **Falso alarme e incerteza:** com 30 réplicas, 0/30 tem limite superior de 11%, e 30/30 tem limite inferior de 89%. Nas grandes cidades, 6 réplicas por cidade são pouco: as taxas por cidade são indicativas.
5. **Afirmações que restam:** a lista está na seção E. Fica restrita "concentrada em municípios" (só municípios de até ~5 mil seções). Fica corrigida "região a 5% detectável" (incerta). Fica acrescentado que o sinal do E02 não identifica o beneficiário: a 10% concentrado há alarmes opostos em 10% a 80% das réplicas.

**Fora do alcance (não simulado):**
- trocas que preservam medianas;
- trocas que mexem no comparecimento;
- alterações anteriores ao boletim;
- outras coberturas.

## C. A4: cobertura do T28 de 2022
| | 1º turno | 2º turno |
|---|---|---|
| Linhas em `urnas_*.parquet` (total declarado "urnas") | 472.024 | 472.027 |
| Com sequência do log | 471.859 | 471.983 |
| Com votos nos últimos 30 min (denominador efetivo do T28) | 471.851 | 471.979 |
| Seções do Sistema de Apuração no total declarado | 116 | 43 |
| Seções do Sistema de Apuração sem sequência de log | 109 | 39 |
| Seções do Sistema de Apuração no denominador efetivo | 5 | 4 |
| Sinalizadas (reprodução literal da regra) | 23, igual ao gravado | 25, igual ao gravado |
| Sinalizadas que são do Sistema de Apuração | 0 | 0 |

- O denominador efetivo já estava certo.
- O total "urnas" incluía 148 seções do Sistema de Apuração sem log. A limitação foi registrada no T28. Na seção 2 do parecer de consolidação eu tinha escrito 150, e corrigi.
- Não houve classificação de falso positivo.

## D. Matriz da F3
O detalhe por pergunta está em `fase3/inventario.json` e `fase3/INVENTARIO.md`: 33 itens, com evidência, estado, resposta, limitação, próximo passo e histórico.

Estados: R = respondida, RP = parcialmente respondida, EXT = depende de evidência externa, NDM = não decidível com os modelos disponíveis.

| Id | Estado | Conclusão mais forte permitida (resumo) |
|---|---|---|
| P1 | R | Ordem dos fluxos 2026 e contraste com 2022 resistem; razão "4:1" frágil |
| M1 | RP | Contas fecham; fluxos individuais não identificáveis (limites de Fréchet, P15) |
| P15 | R | Razão entre abstencionistas não identificada (0 a 1,7 mi) |
| P13 | R | C06b reproduzido |
| P2 | RP | Ver P18 |
| P18 | RP | Sentido correto: dispersa ~123 mil D; locais e municípios até ~5 mil seções ~62 mil D; região 5% I; 2% N; 5 maiores cidades inteiras não detectadas com confiabilidade até ~700 mil |
| P10 | R | 8 de 13 urnas (2026, 1º turno) seguem sinalizadas; 2022 sinaliza 23 e 25 (T28), nenhuma do Sistema de Apuração |
| P5 | R | Modelo de urna sem efeito (±0,02 logit) |
| P7 | R | Urna trocada equivalente (±0,10 z) |
| P8 | R | T03 desprezível com bootstrap |
| P9 | RP | ~0,1% dos locais atípicos em 3 métodos; lista depende do método |
| P17 | R | Assimetria de cauda do T02 é real |
| P14 | RP | Localização em SP 2022 no nível da zona (251 e 259); causa não demonstrada |
| P20 | RP | Locais de SP não atípicos contra a própria zona; arquivos 29/29 conferem |
| P19 | R | Dependência espacial entre municípios (I 0,16 a 0,20) |
| C1 | NDM | Nenhum nulo de chegada calibrado; forma da curva sem leitura |
| C1a | RP | Viradas descritas na ordem de recebimento (2026 2T: 13,5% e 47,2%; 2022 2T: 67,6%) |
| C1b | NDM | Periodicidade, vales e trechos lineares sem leitura possível |
| C2 | RP | 2022 e 2026 diferem na descrição |
| Z1 | RP | Arquivos conferem em 486/486; nenhum modelo estatístico calibrado; cauda baixa acima do modelo nos dois anos |
| P3 | RP | Tabela = BU decodificado por terceiro nas seções comuns; uma só versão de cada arquivo |
| R1-20 | RP | 0 diferenças; cobertura independente 99,96% em 2022, sem o 2º turno de 2026 |
| P16 | R | 200/200 no 1º turno de 2026; 2º turno coberto nacionalmente pelo T17b |
| AUT | RP | Íntegros e assinados até a AC emissora; lacunas de publicação em 2022; não alcança alteração anterior ao boletim |
| P11 | EXT | Elo AC → raiz do TSE não verificado |
| P21 | EXT | Nada obtido |
| P4 | EXT | Sem curva histórica |
| P6 | EXT | Sem boletins de terceiros |
| P12 | R | Diferença do exterior explicada |
| A173 | RP | 173 arquivos assinados ausentes do pacote de dados abertos; votos conferem |
| BU1 | R | Confere |
| SA22 | R | 159/159 conferem (interno) |
| MET | RP | Limites de T02, E02, T10/T11 e zeros registrados; a regra de detecção válida é a do sentido correto |

**Contagem por estado** (denominador: 33 itens do inventário; fonte: campo `estado_final` de `fase3/inventario.json`): 14 respondida parcialmente; 13 respondida; 4 bloqueada por evidência externa; 2 não decidível com os modelos disponíveis. Os rótulos curtos da tabela acima seguem a leitura deste relatório; em caso de diferença, vale o inventário.

## E. Parecer final de aceitação
**Há condições para encerrar a F3 com limitações explícitas, se o responsável aceitar a lista abaixo como limites registrados.** Nenhuma falha encontrada nesta sessão impede a aprovação. A2 e A1 mudaram o alcance de afirmações, não a direção de nenhuma conclusão central, e o que mudou foi corrigido com histórico.

**O que resiste:**
- Contas e correspondência entre tabela, BU e RDV: em 2026 nacional; em 2022 com cobertura independente de 99,96%.
- Integridade criptográfica até a AC emissora.
- Lacunas de publicação de 2022, objetivas: 173 arquivos assinados e 485 auxiliares fora do pacote, sem divergência de votos.
- Assimetria de cauda do T02, com SP 2022 no nível da zona.
- Dependência espacial.
- Poder no sentido correto para os mecanismos e tamanhos da tabela B.

**O que mudou nesta sessão:**
- Região a 5% passou de detectável a incerta.
- "Municípios inteiros" ficou restrito aos de até ~5 mil seções. As 5 maiores cidades inteiras estão fora do alcance da bateria, mesmo a 10%.
- O E02 completo é menos sensível que o simples nesse caso.
- O sinal do E02 não identifica o beneficiário.
- O denominador do T28 de 2022 foi corrigido.
- A lacuna de 333 seções da Bahia é do terceiro, não do TSE.

**Limites que ficam:**
- **Fonte externa:** P4, P6, P11, P21; A173 em outro canal do TSE; R1-20 no 2º turno de 2026.
- **Método não validado:** C1, C1a, C1b, Z1.
- **Impossibilidade demonstrada:** M1, para os fluxos individuais.
- **Fora do alcance dos dados públicos:** alteração anterior ao boletim.
- **Mecanismos sem poder medido:** grandes cidades inteiras, mecanismos não simulados e trocas abaixo de ~25 mil votos.

**Pendências locais não executadas,** que são investigações novas e não verificações:
- A3: perfil do eleitorado da zona 251.
- C3: modelo de cauda baixa para os zeros.
- Repetir o I1 com mais réplicas nas grandes cidades.

**Antes de aprovar,** duas coisas dependem do responsável:
1. **Publicar as correções:** as correções desta sessão estão só locais. Não foi feito push nem deploy.
2. **Desvio de processo:** os pré-registros da F3 ficaram fora do PROTOCOLO, e a emenda 6 foi feita depois. Isso é transparência, não falha de resultado, mas deve constar da aprovação.

A F3 continua **em revisão**, e esta sessão não a concluiu.
