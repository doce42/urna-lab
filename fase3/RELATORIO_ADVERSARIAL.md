# Auditoria adversarial das explicações baseadas em registros oficiais (28/10/2026)

Pré-registro: [`PREREG_ADVERSARIAL.md`](PREREG_ADVERSARIAL.md). Scripts e resultados:
- `fase3/adv_casos.py` → `fase3/resultados/adv_casos.json`;
- contagem do log × comparecimento → `fase3/resultados/adv_log_x_comparecimento.json`;
- o R2 (`fase3/inv_r2_curva_publica.py` → `r2_curva_publica.json`, com as capturas brutas em `fase3/externos/wayback_capturas/`).

**Regra aplicada:** compatibilidade com o log ou com outro registro do mesmo sistema não é verificação independente da causa. BU, RDV, imagem e log são gerados pela mesma urna, com o mesmo software, e assinados pela mesma chave. Tabela, totalização, cadastro de correspondências e declarações vêm do mesmo TSE. Esses registros não são testemunhas independentes entre si.

**Hipóteses:**
- **H0:** funcionamento legítimo.
- **H1:** registro ou explicação incorretos.
- **H2:** comprometimento anterior à geração dos registros.
- **H3:** alteração posterior à geração.

São hipóteses de trabalho, não afirmações.

## Levantamento
Conclusões do projeto que se apoiam em concordância de registros da mesma origem ou em explicação registrada pelo próprio sistema:
- **Concordância:** T01, T14, T15, T16, T17, T17b, T32, T39, T41 (parte de arquivos), T43, P16, R1, SA22, BU1 e A173 (votos).
- **Explicação operacional:** T30, T31, T33 (declarado), T34, T36.

Foram escolhidos os três casos de maior impacto sobre a integridade dos votos.

## Matriz
| Anomalia ou afirmação | Explicação atual do projeto | Dependência entre as fontes | Hipóteses concorrentes | Evidência independente disponível | Teste adversarial | Resultado | Conclusão revisada | Não identificável |
|---|---|---|---|---|---|---|---|---|
| **A. Votos iguais em BU, RDV, imagem, tabela e totalização** (2022 e 2026) | "Os votos conferem" (T01, T14 a T17b, T32, R1) | Mesma urna, software e chave; mesma instituição publica tabela e totais; DataUrnas-BR só relê os mesmos arquivos | H0; H2 (registros coerentes desde a origem); H3 (base por seção alterada depois da divulgação) | Capturas do Internet Archive dos totais nacionais **divulgados durante a apuração** (custódia independente do TSE) | R2: recompor, pela base final, o total no mesmo número de seções de cada captura | 39 capturas (2022: 2 + 27; 2026: 6 + 4); diferença máxima de 0,083 ponto percentual na proporção de Lula; mesmo líder em todas; votos nunca diminuem; última captura igual ao total oficial (2022 2T e 2026 2T) | **H3 em escala nacional contrariada por evidência independente:** a base publicada depois reproduz os totais divulgados ao vivo nos 39 instantes capturados. **A concordância entre arquivos da urna continua sendo consistência interna**, não verificação de autenticidade | H2 (comprometimento anterior que gera registros e totais coerentes); trocas entre seções que preservem o total nacional nos instantes capturados; o que acontece entre capturas |
| **B. Contas de integridade que não fecham** (T36, 2026: 186 casos no 1º turno, 75 no 2º) | "Explicadas": 38 declaradas pelo TSE, 5 com evento compatível no log, 142 inferidas, 1 sem explicação | Explicações vindas do próprio log ou de declaração do próprio TSE; inferência do projeto sobre o mesmo log | H0; H1 (log errado ou incompleto); H1 ou H2 usados para alterar votos nessas seções | Nenhuma fonte externa. O teste usa só a votação das seções contra o resto da UF | Média do z robusto da virada (T02) nessas seções contra a UF; permutação estratificada (10.000); limiar de relevância 0,3 | 1º turno: 185 seções, diferença de +0,039 (p = 0,60); 2º turno (validação): 73, +0,040 (p = 0,73); nenhum subgrupo (declarado, compatível, inferido) deslocado | **"Explicadas" passa a "compatíveis com os registros".** Uma alteração de votos concentrada nessas seções, com deslocamento de 0,3 desvio ou mais, foi contrariada | H1 sem efeito sobre os votos; deslocamentos menores que ~0,3 desvio; H2 global; se os eventos registrados de fato ocorreram |
| **C. Contingências de urna** (troca, recuperação de dados, Sistema de Apuração) | "Justificadas" pelo log (mais de uma urna), pelo certificado ou pela origem do boletim (T34, T16, T30) | Todos os marcadores vêm do próprio sistema | H0; contingência usada como cobertura para alterar votos (H1 ou H2); H3 | Nenhuma externa; teste de votação | Mesmo teste, no 2º turno; limiar 0,1 | 2026: 1.448 seções, −0,039 (p = 0,16), sem deslocamento. **2022 (validação): o critério falhou:** "certificado ≠ urna do log" ocorre em 279.282 seções (59%), então nesse ano não indica contingência. Com só "duas urnas no log" (439 seções): +0,022 (p = 0,66) | Em 2026, alteração de votos concentrada nas contingências com deslocamento ≥ 0,1 foi contrariada. Em 2022, **"certificado diferente do log" não indica troca de urna**, e qualquer inferência baseada nele perde sustentação | Se as contingências aconteceram como registradas; H1 sem efeito em votos; H2 |
| **C1. RS 88013/2/199** (2022, 1º turno) | Antes: "troca de urna compatível (certificado ≠ log)" | Imagem, log e boletim estão na mesma lista assinada; tabela do TSE | H0 (urna 2215062 falhou depois de 196 votos, e a substituta 2228407 completou); H1; H3 | Nenhuma | Documental: comparação dos arquivos da seção | Log da urna 2215062: **196 votos, último às 13:53**; seção encerrada às 17:18. Imagem do boletim: 196. Boletim digital assinado pelo certificado da 2228407 (a "urna efetivada" da tabela) e tabela: **288 comparecimentos**. Uma só urna com votos no log publicado | **Divergência objetiva preservada:** 92 votos da tabela sem registro no log publicado, e uma imagem do boletim (196) diferente do boletim digital (288) na mesma seção. A troca de urna é **compatível** com os registros, não verificada. O apoio "certificado ≠ log" foi retirado (não informa nada em 2022) | O que ocorreu entre 13:53 e 17:18; o log da urna substituta, que não está publicado; o boletim impresso afixado na seção |
| **C2. Log com menos ou mais votos que o comparecimento do boletim** (achado novo, 2022) | Nunca examinado em 2022 (o T14 cobre só 2026) | Log e boletim da mesma urna; tabela do TSE | H0 (troca de urna com log da substituta ausente, reinício); H1; H3 | Nenhuma | Contagem determinística; teste de votação exploratório (critério definido depois de ver os dados) | Log com **menos** votos: 70 seções no 1º turno (3.618 votos) e 36 no 2º (1.669). Log com **mais**: 34 e 13. Em 2026: 9 e 7 seções (59 e 54 votos), já no T36. Sem deslocamento de votos nesses grupos (p de 0,12 a 0,87), com poder baixo | **Achado objetivo de cobertura:** em 2022, 5.287 votos de comparecimento não têm registro correspondente no log publicado da seção. Causa não determinada | Causa em cada seção; se os logs das urnas substitutas existem |
| **C3. MG 50075/47/41** (2026, 1º turno) | Imagem da urna (258) ≠ tabela "explicada" pela imagem do Sistema de Apuração (278) | As duas imagens e o boletim do Sistema de Apuração vêm do mesmo sistema | H0 (urna falhou, cédulas completaram); H1 | Nenhuma | Documental | Imagem da urna: 258; imagem do Sistema de Apuração: 278 = tabela | **"Compatível com contingência registrada"**, não "explicada". A assinatura dos arquivos do Sistema de Apuração de 2026 não foi conferida pelo leitor (hash e assinatura falsos por falta de leitura do `.vsc` de SA de 2026) | Ocorrência real da falha e das cédulas |
| **RDV de 2022 = tabela** (R1) | "0 diferenças" depois de corrigir a regra do nulo por suspensão | O RDV é gravado pela mesma urna e pelo mesmo software que geram o BU | H0; H2 | Nenhuma | — | 0 diferenças em 471.851 e 471.980 seções | **Consistência interna:** a recontagem pelo RDV não é contagem independente dos votos | H2 |

## O que resistiu, o que enfraqueceu e o que depende só da confiança nos registros
**Resistiu a uma prova com evidência independente:**
- **Totais divulgados ao vivo:** batem com a base publicada depois em 39 instantes capturados por terceiro, nas quatro eleições. Uma alteração posterior da base por seção que mudasse os totais nacionais nesses instantes está contrariada.

**Resistiu a um teste que não depende do conteúdo do log** (mas usa os mesmos dados de votação):
- Nas seções com contas de integridade "explicadas" (T36, 2026) e com contingências (2026), não há deslocamento de votos acima de 0,3 e 0,1 desvio. Uma manipulação concentrada nessas seções, com esse tamanho, foi contrariada.

**Enfraqueceu:**
- **"Explicado pelo log":** toda explicação desse tipo (T36, T34, T30, T31, C3) passa a "compatível com os registros", sem verificação independente.
- **Certificado diferente do log:** em 2022 não indica troca de urna. A explicação de RS 88013/2/199 perdeu esse apoio e a seção fica como divergência objetiva.
- **Cobertura do log em 2022:** é menor do que se supunha. 153 seções-turno têm log com contagem diferente do comparecimento, 5.287 votos sem registro no log publicado, nunca examinados antes.
- **"Registros conferem":** concordância entre BU, RDV, imagem, log e tabela é consistência interna. Não pode ser apresentada como várias testemunhas.

**Depende só da confiança nos registros oficiais:**
- **H2 global:** comprometimento anterior à geração dos registros.
- **Softwares e preparo:** T33 (software declarado) e T35 (log das máquinas de geração de mídia).
- **Horários:** os horários de T30 e T31 vêm do relógio do próprio equipamento.
- **Contingências:** a ocorrência real das registradas.
- **Assinaturas:** a ligação delas a uma âncora do TSE (P11).

Distinguir qualquer um desses itens de H0 exige evidência fora do sistema: boletins impressos coletados por terceiros na seção, logs das urnas substitutas, auditoria de código e de hardware, e a cadeia de certificados até uma raiz verificada.

## Testes que precisam ser relidos à luz desta regra
No registro, as seguintes afirmações do tipo "passou" passam a ser lidas como **consistência interna**: T01, T14, T15, T16, T17, T17b, T32, T39, P16, R1, SA22, BU1, A173 (votos). Elas continuam corretas como contas, mas **não demonstram autenticidade** do que foi votado. A única verificação de custódia independente disponível até agora é o R2.

## Fila (não executada)
- **Classificar as 153 seções-turno de 2022** com log diferente do comparecimento, como o T36 faz para 2026, e procurar os logs das urnas substitutas no pacote.
- **Conferir a assinatura das seções do Sistema de Apuração de 2026** (`.vsc` de SA), lacuna do leitor de 2026.
- **Ampliar o R2:** capturas por UF e outras janelas, quando o Internet Archive voltar a responder.

## Adendo da execução da fila (28/10/2026)
- **Campo "urna" do log em 2022:** em parte dos logs de 2022, o terceiro campo da linha não é o número da urna. O valor 67305985 aparece em seções de vários estados. A contagem "urnas com voto no log" de 2022 não é válida, e o subconjunto "duas urnas no log" da validação de 2022 do caso C também não (resultado retirado). A conclusão de 2026 não muda, porque em 2026 o certificado e o log identificam a urna.
- **Log × comparecimento em 2022 (fila F1):**
  - **Recontagem:** confirmada em 153/153.
  - **Log com mais votos que o comparecimento (47 seções):** em 29, um subconjunto exato das partes arquivadas soma o comparecimento. Isso é compatível com partes de outra sessão incluídas no log publicado, não verificado.
  - **Log com menos votos (106 seções):** 5.287 votos sem registro no log publicado.
  - **Causa:** não demonstrada em nenhum dos casos.
- **Sistema de Apuração de 2026 (fila F2):**
  - lista assinada válida em 60/60 e boletim igual à tabela, como consistência interna;
  - a imagem parcial da urna em MG 50075/47/41 não consta de nenhuma lista assinada publicada.
