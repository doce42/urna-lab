# Respostas científicas da F3 (28/10/2026)

> Votos de simulações são sintéticos. Concordância entre registros da mesma origem é consistência interna, não verificação independente. Nenhuma resposta é veredito global sobre fraude.
> Margem do 2º turno: 4.430.191 votos em 2026 e 2.139.645 em 2022.
> A F3 está em revisão; estas respostas não são versão congelada.

## Integridade dos resultados oficiais

### Q1. Os votos oficiais por seção são iguais aos boletins de urna?
**Resposta:** Sim, em todas as seções cujo boletim foi lido, nos dois anos e nos dois turnos: 0 diferenças entre a tabela publicada e o bu.dat.
**Classificação:** Demonstrado no escopo definido
**Em votos:** 0 voto de diferença entre a tabela e os boletins em todos os ~128 milhões de votos de 2026 (2º turno) e ~124 milhões de 2022 conferidos. As 5 seções de 2022 sem arquivo somam 5 votos de comparecimento.
- **2022:** 0 diferenças em 471.907 + 471.980 seções + 159 do Sistema de Apuração; 10 sem boletim lido.
- **2026:** 0 diferenças em 499.198 + 499.201 seções.
- **Números:** 2026: 499.198 de 499.206 (1º turno) e 499.201 de 499.205 (2º) boletins lidos, 0 diferenças. 2022: 471.907 (1º) e 471.980 (2º) lidos, 0 diferenças, mais 159 seções-turno do Sistema de Apuração lidas à parte (0 diferenças); 10 seções-turno de 2022 sem boletim lido pelo projeto (7 do exterior, 2 do Pará, 1 do Rio Grande do Sul), na fila.
- **Demonstra:** Os votos da tabela publicada são os mesmos dos boletins digitais assinados pelas urnas.
- **Não demonstra:** Consistência interna: BU, RDV, imagem e log são gerados pela mesma urna e assinados pela mesma chave; tabela e totais vêm do mesmo TSE. A concordância não verifica de forma independente o que foi votado. Não exclui comprometimento anterior à geração do boletim (H2).
- **Robustez:** Releitura direta de 100 seções sorteadas dos zips: 100/100 idênticas. Decodificação independente de terceiro (DataUrnas-BR): 0 diferenças em 2026 1º turno e em 99,96% das seções do Brasil em 2022.
- **Causa:** não aplicável · **Alcance:** Todas as seções com boletim publicado; votos de Presidente.
- **O que mudaria a resposta:** Uma seção com boletim lido e votos diferentes da tabela; boletim impresso coletado por terceiro com valores diferentes.
- **Validação:** Executado e reproduzido (R1, releitura).
- **Evidências:** `fase3/inv_r1_integridade.py`, `fase3/resultados/r1_integridade.json`, `fase3/resultados/sa22.json`, `fase3/resultados/R1_20_dataurnas.json`

### Q2. Os votos publicados podem ser reconstruídos a partir dos RDVs disponíveis?
**Resposta:** Sim, em todas as seções com RDV lido: a recontagem voto a voto dá os mesmos totais de candidatos, brancos e nulos da tabela.
**Classificação:** Demonstrado no escopo definido
**Em votos:** 0 voto de diferença entre a recontagem pelo RDV e a tabela, nos dois anos.
- **2022:** 0 diferenças em 471.851 + 471.980 seções.
- **2026:** 0 diferenças em 499.167 + 499.174 seções.
- **Números:** 2026: 499.167 (1º) e 499.174 (2º) RDVs lidos, 0 diferenças. 2022: 471.851 e 471.980, 0 diferenças (o leitor de 2022 já soma o nulo por suspensão no nulo; a primeira comparação somava de novo e acusou 42.764 e 7.410 diferenças falsas; corrigido e declarado).
- **Demonstra:** A tabela pode ser recomposta voto a voto pelo RDV publicado.
- **Não demonstra:** O RDV é gravado pela mesma urna e pelo mesmo software que geram o boletim: a recontagem não é contagem independente do que o eleitor digitou.
- **Robustez:** Duas correções do comparador declaradas (R1); releitura direta 100/100.
- **Causa:** não aplicável · **Alcance:** Seções com RDV publicado.
- **O que mudaria a resposta:** Divergência RDV × tabela com o arquivo lido; RDV ausente em seções relevantes.
- **Validação:** Executado (R1).
- **Evidências:** `fase3/resultados/r1_integridade.json`, `testes/registro.json (T17, T17b)`

### Q3. Existem divergências verificáveis entre boletins, RDV, logs, tabelas e totalização?
**Resposta:** Nos votos, não. Entre arquivos e entre log e comparecimento, sim: há divergências objetivas pontuais, preservadas como achados, sem efeito demonstrado sobre votos.
**Classificação:** Parcialmente demonstrado
**Em votos:** Nenhuma divergência muda um voto da tabela. Divergências de registro: 2022, 5.287 votos sem registro no log publicado e 2.503 a mais no log (0,25% e 0,12% da margem de 2022); RS 88013/2/199, 92 votos entre a imagem do boletim (196) e o boletim digital (288); 2026, 113 votos em 16 seções-turno do T36 (0,003% da margem).
- **2022:** Votos: 0. Log × comparecimento: 153 seções-turno; imagem × boletim: 1 seção.
- **2026:** Votos: 0. Log × comparecimento: 16 seções-turno (T36); imagem da urna × tabela: 1 seção explicada como contingência registrada (Sistema de Apuração), compatível, não verificada.
- **Números:** Totalização: 638 de 638 itens iguais ao total oficial (T32). Log × comparecimento: 2022, log com menos votos em 70 (1º) e 36 (2º) seções (3.618 e 1.669 votos sem registro no log publicado) e com mais em 34 e 13 (fila F1: recontagem confirmada em 153/153; em 29 das 47 com log maior, um subconjunto exato das partes arquivadas do log soma o comparecimento, compatível com partes de outra sessão no log publicado); 2026, 9 e 7 seções (59 e 54 votos), no T36. Imagem × boletim: RS 88013/2/199 (2022): imagem assinada com 196 votos, boletim e tabela com 288; log da urna 2215062 com 196 votos (último às 13:53). T36 (2026): 186 e 75 casos de contas que não fecham, compatíveis com registros (troca de urna, RED, reinício), 1 sem explicação (RJ 60011/8/61).
- **Demonstra:** Há divergências documentais objetivas, todas pequenas e sem deslocamento de votos detectável nas seções envolvidas.
- **Não demonstra:** A causa de cada divergência. As explicações operacionais vêm do próprio sistema (compatíveis, não verificadas).
- **Robustez:** Teste de votação nas seções com explicação registrada (T36, contingências): sem deslocamento (adv_casos.json). Exploratório em 2022 (log ≠ comparecimento): sem deslocamento, poder baixo.
- **Causa:** não demonstrada · **Alcance:** Seções com arquivos; Presidente.
- **O que mudaria a resposta:** Logs das urnas substitutas; boletins impressos da seção; esclarecimento do TSE por seção.
- **Validação:** Executado (R1, auditoria adversarial).
- **Evidências:** `fase3/resultados/r1_integridade.json`, `fase3/resultados/adv_log_x_comparecimento.json`, `fase3/RELATORIO_ADVERSARIAL.md`, `analise/resultado_casos_integridade_1t.json`, `testes/registro.json (T32, T36)`

### Q4. Existem arquivos ausentes, seções não cobertas ou versões conflitantes? Qual o alcance?
**Resposta:** Sim, arquivos ausentes e algumas seções não cobertas; versões conflitantes não foram encontradas no que foi possível comparar.
**Classificação:** Parcialmente demonstrado
**Em votos:** Seções com arquivos ausentes: 64 seções com 21.112 comparecimentos em 2022 (boletim presente e igual à tabela); o Sistema de Apuração soma 27.692 votos em 2022 e as seções de 2026 também conferem; as 5 seções sem arquivo somam 5 votos.
- **2022:** 173 + 485 arquivos ausentes; 10 seções sem boletim lido.
- **2026:** 1 log ausente; assinatura do Sistema de Apuração não conferida pelo leitor.
- **Números:** 2022: 173 arquivos assinados (RDV, log, imagem; 64 seções, 54 do exterior) e 485 auxiliares fora do pacote de dados abertos; das 10 seções sem boletim lido, 5 foram lidas na fila F3 (conferem) e 5 do exterior não têm arquivo nenhum no pacote. 2026: 1 log assinado e não publicado (SP, 2º turno); seções do Sistema de Apuração (31 e 29) conferidas na fila F2: lista assinada válida em 60/60, boletim = tabela; 3 seções do exterior fora da tabela com comparecimento 0 (P12); a imagem parcial da urna em MG 50075/47/41 não consta de lista assinada publicada. Versões: uma só captura de cada arquivo; os totais divulgados ao vivo (39 capturas) batem com a base final.
- **Demonstra:** Ausências de publicação objetivas e de alcance pequeno; os boletins dessas seções coincidem com a tabela.
- **Não demonstra:** O conteúdo dos arquivos ausentes; republicação de arquivos entre datas (só há uma versão local).
- **Robustez:** Duas cópias do pacote de 2022 (14/10 e 27/10/2026) com as mesmas ausências.
- **Causa:** não demonstrada · **Alcance:** Pacotes de dados abertos do TSE.
- **O que mudaria a resposta:** Os 173 arquivos por outro canal; versões datadas dos pacotes.
- **Validação:** Executado (A173, SA22, R1, R2).
- **Evidências:** `fase3/resultados/a173.json`, `fase3/resultados/sa22.json`, `fase3/resultados/a1.json`, `fase3/resultados/r1_integridade.json`, `fase3/resultados/r2_curva_publica.json`

### Q5. Os registros foram autenticados criptograficamente até uma fonte de confiança apropriada?
**Resposta:** Não até a raiz: as assinaturas das urnas são válidas até a autoridade certificadora emissora, mas a ligação dessa autoridade a uma âncora do TSE não foi verificada.
**Classificação:** Parcialmente demonstrado
**Em votos:** Alcança todos os votos: nenhum voto, de 2022 ou 2026, tem a assinatura verificada até a raiz do TSE; todos estão verificados até a AC emissora.
- **2022:** Assinatura válida até a AC emissora nos arquivos presentes.
- **2026:** Idem.
- **Números:** 2026: hash e assinatura válidos em 499.176 (1º) e 499.178 (2º) boletins. 2022: 471.908 e 471.984 boletins e as 159 seções do Sistema de Apuração. Certificados de AC obtidos de terceiro (DataUrnas-BR); AC URNA v2 e AC RAIZ UE não obtidas por canal do TSE.
- **Demonstra:** Os arquivos presentes não foram alterados depois de assinados pela chave da urna.
- **Não demonstra:** Que a chave pertence a uma urna autêntica do TSE (sem âncora); qualquer coisa anterior à assinatura.
- **Robustez:** Verificação Ed521 e ECDSA P-521 própria; chaves degeneradas rejeitadas.
- **Causa:** não aplicável · **Alcance:** Arquivos presentes.
- **O que mudaria a resposta:** Certificados raiz obtidos do TSE por canal verificável.
- **Validação:** Bloqueado no elo final (fonte externa).
- **Evidências:** `testes/registro.json (T16)`, `fase2/resultados/P11.json`, `fase3/resultados/sa22.json`, `fase3/resultados/r1_integridade.json`

### Q6. Existem evidências externas independentes que confirmem ou contradigam os registros publicados?
**Resposta:** Sim, uma: capturas do Internet Archive dos totais nacionais divulgados durante a apuração confirmam a base publicada nos instantes capturados. Não há boletins de terceiros nem outra fonte de origem independente.
**Classificação:** Parcialmente demonstrado
**Em votos:** Na captura final de cada eleição, 0 voto de diferença entre o total divulgado ao vivo e a base. A maior diferença em capturas parciais equivale a ~1,7 mil a ~3 mil votos naquele instante (seções com o mesmo horário de recebimento ordenadas de forma diferente), e não muda o líder.
- **2022:** 29 capturas consistentes.
- **2026:** 10 capturas consistentes.
- **Números:** 39 capturas (2022: 2 e 27; 2026: 6 e 4): diferença máxima de 0,083 ponto percentual entre a proporção divulgada e a recomposta pela base final no mesmo número de seções; mesmo líder em todas; votos nunca diminuem; a última captura é igual ao total oficial onde existe.
- **Demonstra:** Que a base publicada depois corresponde ao que foi divulgado ao vivo, no agregado nacional e nos instantes capturados (contraria alteração posterior que mudasse esses totais).
- **Não demonstra:** Correspondência seção a seção com fonte externa; o que aconteceu antes da divulgação; instantes não capturados.
- **Robustez:** Custódia de terceiro (Internet Archive); escopo de busca fixado antes; capturas brutas guardadas com SHA-256.
- **Causa:** não aplicável · **Alcance:** Totais nacionais de Presidente em 39 instantes.
- **O que mudaria a resposta:** Boletins impressos fotografados por terceiros; capturas por UF.
- **Validação:** Executado (R2), com bloqueio parcial do Internet Archive registrado.
- **Evidências:** `fase3/inv_r2_curva_publica.py`, `fase3/resultados/r2_curva_publica.json`, `fase3/externos/wayback_capturas/`

### Q7. Os testes conseguem detectar mecanismos plausíveis de alteração, e em quais condições falham?
**Resposta:** Detectam alguns, em condições limitadas: nos cenários simulados, trocas dispersas de ~123 mil votos e concentradas de ~62 mil em locais ou municípios de até ~5 mil seções foram detectadas no sentido certo; trocas de ~25 mil não foram detectadas; no município inteiro das 5 maiores cidades, a bateria original não detecta, mas o teste T44 (histórico de 2022 e perfil do 1º turno) detecta a partir de 2% dos válidos (31 mil a 139 mil votos).
**Classificação:** Parcialmente demonstrado
**Em votos:** Detectado nos cenários simulados: ~123 mil votos dispersos (2,8% da margem de 2026) e ~62 mil concentrados (1,4%). Não detectado: ~25 mil (0,6%). No município inteiro de uma grande cidade, a bateria original falha até ~696 mil votos, mas o teste T44 vê a partir de 31 mil a 139 mil (2% dos válidos). Inverter 2026 exigiria trocar ~2,22 mi votos de lado.
- **2022:** Mesmo padrão; limiar ancorado no real com 23% de falso alarme.
- **2026:** Ver números.
- **Números:** 2026, 30 réplicas, limiar calibrado, falso alarme 0/30: dispersa 10% (~123 mil) 30/30; locais e municípios até ~5 mil seções a 5% (~62 mil) 30/30; região a 5% 26/30 e 23/30; 2% (~25 mil) 0 a 1/30; 5 maiores cidades a 10% (155 mil a 696 mil votos) 10 a 13/30 (E02 completo), Brasília e Fortaleza 0/12. T44: troca de 2% dos válidos no município inteiro detectável nas 5 cidades (4,0 a 5,2 desvios; falso alarme 3/200).
- **Demonstra:** O alcance dos testes nos cenários simulados.
- **Não demonstra:** Detecção fora dos cenários simulados; mecanismos que preservam medianas, mexem no comparecimento ou atuam antes do boletim; votos simulados não são votos encontrados.
- **Robustez:** Validação em 2022 com o mesmo padrão; direção conferida.
- **Causa:** não aplicável · **Alcance:** 4 mecanismos + grandes cidades; 1% das seções; 2%, 5%, 10%.
- **O que mudaria a resposta:** Novos mecanismos ou coberturas simulados.
- **Validação:** Executado (I1, A2).
- **Evidências:** `fase3/rev_i1_poder.py`, `fase3/rev_a2_poder.py`, `fase3/resultados/rev_a2_2026.json`, `fase3/resultados/rev_a2_2022.json`

## Curvas, viradas e periodicidade

### Q8. Quantas vezes a liderança mudou na ordem de recebimento dos boletins?
**Resposta:** Depois dos primeiros 10% de urnas: 2022, 1º turno 1 vez (aos 68,2%); 2022, 2º turno 1 vez (aos 67,6%, adversário → Lula); 2026, 1º turno nenhuma; 2026, 2º turno 2 vezes (aos 13,5%, Lula → adversário, e aos 47,2%, adversário → Lula).
**Classificação:** Demonstrado no escopo definido
**Em votos:** A ordem de apuração não muda nenhum voto: a mesma soma final em qualquer ordem. A virada do 2º turno de 2022 ocorreu com 67,6% das urnas; a de 2026, com 47,2%.
- **2022:** 1 e 1.
- **2026:** 0 e 2.
- **Números:** A contagem urna a urna (S1) registra 3 e 21 trocas em 2022 porque soma oscilações no ponto de cruzamento; em grade de 1% são 1 e 1.
- **Demonstra:** O número de viradas na ordem de recebimento (reconstrução).
- **Não demonstra:** Antes dos 10% das urnas; a ordem é de recebimento, não de divulgação (ver Q9).
- **Robustez:** Grade de 0,5% e 2% como sensibilidade.
- **Causa:** não aplicável · **Alcance:** Votos de Presidente, ordem por DT_BU_RECEBIDO.
- **O que mudaria a resposta:** —
- **Validação:** Executado (E2).
- **Evidências:** `fase3/f3_curvas.py`, `fase3/resultados/E2_curvas.json`

### Q9. Quantas vezes a liderança mudou na sequência pública efetivamente divulgada?
**Resposta:** Nas capturas disponíveis: 2022, 1º turno pelo menos 1; 2022, 2º turno 1 (adversário até 18:22, com 49,53% para Lula; Lula a partir de 19:43); 2026, 1º turno 0; 2026, 2º turno pelo menos 2 (Lula às 19:36 com 50,55%, adversário às 20:07 com 49,56%, Lula às 21:25). A sequência capturada é amostrada: os números são limites inferiores entre capturas.
**Classificação:** Parcialmente demonstrado
**Em votos:** Idem: a sequência divulgada é a soma parcial dos mesmos votos; 0 voto de diferença no total final.
- **2022:** 1º turno ≥ 1; 2º turno 1.
- **2026:** 1º turno 0; 2º turno ≥ 2.
- **Números:** Capturas: 2022 1º turno 2; 2º turno 27; 2026 1º turno 6; 2º turno 4.
- **Demonstra:** As viradas observadas na divulgação coincidem em sentido e momento com a reconstrução.
- **Não demonstra:** Viradas entre capturas não observadas; 2022 1º turno e 2026 têm poucas capturas.
- **Robustez:** Mesmo resultado por número de seções e por horário (defasagem de 0 minuto).
- **Causa:** não aplicável · **Alcance:** Totais nacionais divulgados.
- **O que mudaria a resposta:** Mais capturas (por UF, outras janelas).
- **Validação:** Executado (R2).
- **Evidências:** `fase3/resultados/r2_curva_publica.json`, `fase3/externos/wayback_capturas/`

### Q10. Uma quantidade pequena de viradas é incomum sob modelos realistas de chegada dos boletins?
**Resposta:** Não determinado: nenhum dos cinco nulos de permutação é calibrado, e o modelo de chegada com as horas reais de emissão e atraso de transmissão sorteado (fila F4) não foi validado em 2022 (última troca e maior vale fora da faixa; 0 de 27 capturas na faixa). O número de trocas observado cabe no modelo nos quatro casos, mas isso não é confirmatório.
**Classificação:** Não determinado com as evidências disponíveis
**Em votos:** Não se traduz em votos: trata da ordem de chegada, não do total.
- **Números:** Nulos: irrestrito, por UF, por município, UF × hora de encerramento, UF × hora × tamanho; 200 permutações cada.
- **Demonstra:** —
- **Não demonstra:** Que as viradas sejam comuns ou incomuns.
- **Robustez:** —
- **Causa:** não aplicável · **Alcance:** —
- **O que mudaria a resposta:** Um modelo de chegada que reproduza 2022 e as capturas.
- **Validação:** Tentado (E2, E2b, F4); nenhum validado. Parado pelo critério.
- **Evidências:** `fase3/resultados/E2_curvas.json`, `fase3/resultados/E2b_curvas.json`
- **Reabertura:** Construir modelo de chegada por lotes e validá-lo com as 27 capturas do 2º turno de 2022.

### Q11. Os vales aparentemente periódicos e os trechos lineares são reproduzíveis com os dados brutos?
**Resposta:** A curva divulgada é reproduzível com os dados por seção nos 39 instantes capturados (diferença ≤ 0,083 pp); periodicidade não foi testada com estatística validada.
**Classificação:** Parcialmente demonstrado
**Em votos:** Não se traduz em votos: forma da curva.
- **Números:** S3 (maior vale), S4 (oscilações), S5 (maior trecho linear) calculados; sem nulo calibrado.
- **Demonstra:** Que os pontos divulgados saem dos dados publicados por seção.
- **Não demonstra:** Que vales ou trechos lineares sejam anômalos ou normais.
- **Robustez:** —
- **Causa:** não aplicável · **Alcance:** Curvas de 2022 e 2026.
- **O que mudaria a resposta:** Modelo de chegada validado; teste espectral pré-registrado.
- **Validação:** Parcial.
- **Evidências:** `fase3/resultados/r2_curva_publica.json`, `fase3/resultados/E2_curvas.json`

### Q12. Os padrões continuam anômalos após controles por geografia, lotes, horários, arredondamento e dependência territorial?
**Resposta:** Não determinado: com controles por UF, município, hora de encerramento e tamanho, os nulos continuam rejeitando também em 2022, então não discriminam.
**Classificação:** Não determinado com as evidências disponíveis
**Em votos:** Não se traduz em votos: forma da curva.
- **Números:** η² da ordem por UF × hora × tamanho: 0,36 (2026 1º turno).
- **Demonstra:** —
- **Não demonstra:** Anomalia ou normalidade da curva.
- **Robustez:** —
- **Causa:** não aplicável · **Alcance:** —
- **O que mudaria a resposta:** Modelo de chegada validado (fila).
- **Validação:** Tentado.
- **Evidências:** `fase3/resultados/E2b_curvas.json`

### Q13. 2022 e 2026 apresentam semelhanças estatisticamente relevantes depois desses controles?
**Resposta:** Não determinado estatisticamente. Descritivamente: nos dois anos a última troca de liderança vem mais tarde do que nos modelos nulos e do que o modelo de atraso de transmissão prevê (2022 2º turno: 68% contra 39% a 42%; 2026 2º turno: 48% contra 30% a 34%); em 2026 a ordem de chegada é mais territorial (η² por UF 0,39 contra 0,24).
**Classificação:** Não determinado com as evidências disponíveis
**Em votos:** Não se traduz em votos: comparação da forma das curvas.
- **Números:** —
- **Demonstra:** Semelhanças descritivas.
- **Não demonstra:** Semelhança estatística após controles.
- **Robustez:** —
- **Causa:** não aplicável · **Alcance:** —
- **O que mudaria a resposta:** Depende de Q10.
- **Validação:** Parcial.
- **Evidências:** `fase3/resultados/E2_curvas.json`

### Q14. Há divergência objetiva entre a sequência publicada e os registros históricos disponíveis?
**Resposta:** Não: nas 39 capturas históricas, a sequência divulgada é igual à recomposta pela base final (≤ 0,083 pp, mesmo líder, votos que nunca diminuem, total final igual).
**Classificação:** Refutado no escopo definido (a hipótese de divergência)
**Em votos:** 0 voto de diferença entre a sequência divulgada e a base nas capturas finais.
- **Números:** 2022 2º turno: 27/27 consistentes; 2026 2º turno: 4/4; 2022 1º turno: 2/2; 2026 1º turno: 6/6.
- **Demonstra:** Ausência de divergência nos instantes capturados (custódia independente).
- **Não demonstra:** Instantes não capturados; divergência seção a seção que preserve o total nacional.
- **Robustez:** Duas formas de comparação (por seções e por horário).
- **Causa:** não aplicável · **Alcance:** Totais nacionais.
- **O que mudaria a resposta:** Captura histórica com valor incompatível.
- **Validação:** Executado (R2).
- **Evidências:** `fase3/resultados/r2_curva_publica.json`

## Zeros de votos

### Q15. Quantas seções tiveram zero votos para Flávio Bolsonaro em cada turno de 2026?
**Resposta:** 79 no 1º turno e 106 no 2º.
**Classificação:** Demonstrado no escopo definido
**Em votos:** Nas 79 seções do 1º turno, 9.542 votos foram para Lula; nas 106 do 2º turno, 14.860 (todos os válidos dessas seções). São 0,34% da margem de 2026.
- **Números:** Universo: seções fora do exterior com votos válidos nos dois turnos (497.897). Comparação: Bolsonaro 2022, 160 e 141; Lula 2026, 8 e 4.
- **Demonstra:** A contagem.
- **Não demonstra:** —
- **Robustez:** —
- **Causa:** não aplicável · **Alcance:** Seções do Brasil.
- **O que mudaria a resposta:** —
- **Validação:** Executado (E3).
- **Evidências:** `fase3/resultados/E3_zeros.json`

### Q16. Quantas tiveram comparecimento positivo e registros válidos?
**Resposta:** Todas: 79 e 106 com comparecimento positivo, e boletim, RDV, imagem e tabela consistentes entre si em todas.
**Classificação:** Demonstrado no escopo definido
**Em votos:** Os votos dessas seções conferem nos registros: 0 voto de diferença.
- **Números:** Mediana de 102 e 124 votos válidos nessas seções (geral: 245 e 254); 62 e 67 municípios, concentradas em AM, PA, MA.
- **Demonstra:** Que não são seções vazias nem erros de leitura.
- **Não demonstra:** Consistência interna: BU, RDV, imagem e log são gerados pela mesma urna e assinados pela mesma chave; tabela e totais vêm do mesmo TSE. A concordância não verifica de forma independente o que foi votado.
- **Robustez:** —
- **Causa:** não aplicável · **Alcance:** Seções do Brasil.
- **O que mudaria a resposta:** —
- **Validação:** Executado.
- **Evidências:** `fase3/resultados/E3_zeros.json`, `fase3/resultados/bu1.json`

### Q17. Como essas seções mudaram entre o primeiro e o segundo turno?
**Resposta:** Das seções com zero em algum turno: 50 com zero nos dois, 56 passaram de votos a zero e 29 de zero a votos.
**Classificação:** Demonstrado no escopo definido
**Em votos:** Não se traduz em votos: transições entre turnos.
- **Números:** 2022 (Bolsonaro): 84 nos dois, 57 de votos a zero, 76 de zero a votos.
- **Demonstra:** As transições.
- **Não demonstra:** Por quê.
- **Robustez:** —
- **Causa:** não demonstrada · **Alcance:** Seções do Brasil.
- **O que mudaria a resposta:** —
- **Validação:** Executado.
- **Evidências:** `fase3/resultados/E3_zeros.json`

### Q18. O fenômeno é estatisticamente incomum depois de controlar tamanho, município, local e heterogeneidade?
**Resposta:** Pelo critério pré-registrado, não determinado (o modelo não passou na calibração). Descritivamente, não há excesso agregado: um modelo ajustado em outra metade dos municípios prevê 79,1 e 101,5 zeros contra 79 e 106 observados, dentro do intervalo.
**Classificação:** Não determinado com as evidências disponíveis
**Em votos:** Se os zeros fossem anomalia, os votos em jogo seriam os que o candidato teria nessas seções: de ~44 a ~4.800 votos conforme o modelo (2026, 2º turno), no máximo 0,11% da margem de 4,43 mi.
- **Números:** Intervalos de predição: [63, 98] e [88, 115]. Falhas do critério: teste de Hosmer–Lemeshow rejeita desvios mínimos nos controles grandes (dezenas de milhares de seções), razões por decil de 1,25 a 1,27 (limite 1,25) e controles de Lula com 1 a 8 zeros. O modelo anterior (I2) também falhou.
- **Demonstra:** Que o total de zeros observado é o previsto fora da amostra por um modelo de covariáveis locais.
- **Não demonstra:** Calibração formal; ausência de excesso em seções específicas.
- **Robustez:** Sensibilidade sem a covariável do 1º turno: mesmo resultado.
- **Causa:** não demonstrada · **Alcance:** Seções do Brasil; Flávio 2026.
- **O que mudaria a resposta:** Modelo que passe em critério de calibração adequado a controles grandes e pequenos.
- **Validação:** Executado (R3); validação formal falhou.
- **Evidências:** `fase3/inv_r3_zeros.py`, `fase3/resultados/r3_zeros.json`, `fase3/resultados/rev_i2.json`
- **Reabertura:** Refazer o critério de calibração (controles com esperado ≥ 20; tolerância por decil adequada a n grande) antes de nova tentativa.

### Q19. O mesmo método identifica padrões semelhantes em 2022?
**Resposta:** Sim, o mesmo resultado: Bolsonaro 2022 com 160 e 141 zeros contra 162,9 e 136,5 previstos fora da amostra; mesma falha do critério formal.
**Classificação:** Não determinado com as evidências disponíveis
**Em votos:** 2022: de ~66 a ~4.300 votos esperados para Bolsonaro nessas seções, no máximo 0,2% da margem de 2,14 mi.
- **Números:** Intervalos [140, 187] e [118, 153].
- **Demonstra:** Que 2026 e 2022 se comportam do mesmo modo no modelo.
- **Não demonstra:** Calibração formal.
- **Robustez:** —
- **Causa:** não demonstrada · **Alcance:** Bolsonaro 2022.
- **O que mudaria a resposta:** Ver Q18.
- **Validação:** Executado (R3).
- **Evidências:** `fase3/resultados/r3_zeros.json`

### Q20. Existem divergências objetivas nos boletins ou apenas resultados numéricos extremos?
**Resposta:** Apenas resultados numéricos extremos: 0 divergências de votos entre boletim, RDV, imagem e tabela nas 486 seções-turno com zero votos para um finalista.
**Classificação:** Demonstrado no escopo definido
**Em votos:** 0 voto de diferença nos registros dessas seções.
- **Números:** 2026: 185; 2022: 301 (incluindo a seção do Sistema de Apuração verificada no BU1).
- **Demonstra:** Ausência de divergência documental nessas seções.
- **Não demonstra:** Consistência interna: BU, RDV, imagem e log são gerados pela mesma urna e assinados pela mesma chave; tabela e totais vêm do mesmo TSE. A concordância não verifica de forma independente o que foi votado.
- **Robustez:** —
- **Causa:** não aplicável · **Alcance:** Seções com zero.
- **O que mudaria a resposta:** Boletim impresso de terceiro diferente.
- **Validação:** Executado.
- **Evidências:** `fase3/resultados/E3_zeros.json`, `fase3/resultados/bu1.json`

## Mudança entre o primeiro e o segundo turno

### Q21. Quantos votos cada finalista ganhou ou perdeu entre os turnos?
**Resposta:** 2022: Lula +3.086.495, Bolsonaro +7.134.009. 2026: Lula +10.376.694, Flávio +3.721.538 (base por seção, com exterior).
**Classificação:** Demonstrado no escopo definido
**Em votos:** 2022: Lula +3,09 mi, Bolsonaro +7,13 mi. 2026: Lula +10,38 mi, Flávio +3,72 mi.
- **2022:** Lula +3,09 mi; Bolsonaro +7,13 mi.
- **2026:** Lula +10,38 mi; Flávio +3,72 mi.
- **Números:** 1º → 2º turno, 2022: Lula 57.259.504 → 60.345.999; Bolsonaro 51.072.345 → 58.206.354. 2026: Lula 53.879.538 → 64.256.232; Flávio 56.104.503 → 59.826.041.
- **Demonstra:** As variações.
- **Não demonstra:** Quem mudou de voto.
- **Robustez:** Soma das urnas = total oficial (T32).
- **Causa:** não aplicável · **Alcance:** Brasil e exterior.
- **O que mudaria a resposta:** —
- **Validação:** Executado.
- **Evidências:** `fase3/resultados/entre_turnos_contas.json`

### Q22. Quanto da mudança corresponde a comparecimento, votos dos eliminados, brancos e nulos?
**Resposta:** Toda a mudança fecha exatamente: ganho dos finalistas = votos dos eliminados no 1º turno + variação do comparecimento − variação de brancos e nulos.
**Classificação:** Demonstrado no escopo definido
**Em votos:** 2026: os finalistas somaram +14,10 mi = 9,32 mi dos eliminados + 2,96 mi de comparecimento + 1,82 mi de brancos e nulos a menos. 2022: +10,22 mi = 9,90 mi + 0,57 mi − 0,25 mi.
- **Números:** 2022: 10.220.504 = 9.897.870 + 570.424 − 247.790. 2026: 14.098.232 = 9.321.993 + 2.960.239 + 1.816.000 (brancos e nulos caíram 1,82 mi).
- **Demonstra:** A identidade contábil.
- **Não demonstra:** A divisão dos eliminados entre os finalistas (ver Q24).
- **Robustez:** —
- **Causa:** não aplicável · **Alcance:** Totais.
- **O que mudaria a resposta:** —
- **Validação:** Executado.
- **Evidências:** `fase3/resultados/entre_turnos_contas.json`

### Q23. Existem diferenças impossíveis de reconciliar com os totais oficiais?
**Resposta:** Não: as contas fecham nacionalmente e nenhuma seção tem mais votos que comparecimento ou mais comparecimento que aptos.
**Classificação:** Refutado no escopo definido (a hipótese de diferença impossível)
**Em votos:** 0 voto inconsistente: nenhuma seção com mais votos que comparecimento.
- **Números:** 0 seções inconsistentes; 638/638 itens iguais ao total oficial.
- **Demonstra:** Ausência de impossibilidade contábil.
- **Não demonstra:** Que os números reflitam os votos dados (ver integridade).
- **Robustez:** —
- **Causa:** não aplicável · **Alcance:** Todas as seções.
- **O que mudaria a resposta:** Seção com contagem impossível.
- **Validação:** Executado.
- **Evidências:** `fase3/resultados/entre_turnos_contas.json`, `testes/registro.json (T32)`

### Q24. Quais fluxos entre escolhas são matematicamente possíveis?
**Resposta:** Um intervalo amplo: os dados agregados admitem desde fluxos quase nulos até milhões de votos em cada direção; só limites, não um fluxo.
**Classificação:** Parcialmente demonstrado
**Em votos:** Trocas diretas entre finalistas em 2026: mínimo garantido de 79 e 123 votos, máximo de 43,5 mi e 39,4 mi; abstencionistas para Lula entre 4.116 e 32,3 mi. A razão do C06 erra de ±0,5 a ±1,5 mi votos.
- **Números:** 2026: trocas diretas entre finalistas com mínimo garantido de 79 (Flávio → Lula) e 123 (Lula → Flávio) votos e máximos de 43,5 mi e 39,4 mi; abstencionistas para Lula entre 4.116 e 32,3 mi (Fréchet). O estimador C06 dá razão ~4:1 entre abstencionistas, frágil (1,7 a 11,8 sob heterogeneidade).
- **Demonstra:** Os limites matemáticos.
- **Não demonstra:** Qual fluxo ocorreu.
- **Robustez:** Sensibilidade do C06 sob heterogeneidade sintética.
- **Causa:** não aplicável · **Alcance:** Seções do Brasil.
- **O que mudaria a resposta:** —
- **Validação:** Executado (F2).
- **Evidências:** `fase2/resultados/P13.json`, `fase2/resultados/P15.json`, `fase2/sessao_limitada_2026-10-28/p1_resultado_principal.json`

### Q25. O padrão territorial de crescimento apresenta desvios persistentes após controles?
**Resposta:** Sim, em parte: a assimetria de cauda do T02 é real nos dois anos; cerca de 0,1% dos locais são atípicos (lista depende do método); há dependência espacial entre municípios; em São Paulo 2022 a zona 251 mantém desvio depois de controlar o perfil do eleitorado; em 2026, Salvador tem virada de Lula ~30 mil votos acima do previsto pelo histórico, em todas as 19 zonas (T44), a única entre as 27 capitais e não explicada pelo perfil do eleitorado; Fortaleza tem desvio de tamanho parecido no sentido oposto.
**Classificação:** Parcialmente demonstrado
**Em votos:** Salvador 2026: ~30 mil votos de Lula acima do previsto (0,7% da margem de 2026). Zona 251 (SP, 2022): ~4,2 mil votos de Lula acima da virada mediana da capital (0,2% da margem de 2022); zona 259: ~6,2 mil. Cauda pró-Lula do T02: ~740 votos (2026) e ~2.600 (2022). Cada local atípico: dezenas a poucas centenas de votos.
- **Números:** Zona 251: desvio de 0,58 z cai para 0,42 (IC 95% 0,23 a 0,62; 26% explicado) com escolaridade, idade, sexo e estado civil; sensibilidade 0,37 (36%). Zona 259: explicado em parte. Moran's I 0,16 a 0,20. Locais: 61 (2026) e 84 (2022) contra o entorno.
- **Demonstra:** Que há desvios territoriais persistentes, inclusive na zona 251 depois do perfil.
- **Não demonstra:** A causa; que sejam irregularidades.
- **Robustez:** R² do perfil 0,02; sensibilidade com todas as zonas.
- **Causa:** não demonstrada · **Alcance:** Brasil; SP capital para a zona 251.
- **O que mudaria a resposta:** Covariáveis de campanha, renda, migração; dados externos da zona.
- **Validação:** Executado (R4, I3, P17, P19).
- **Evidências:** `fase2/resultados/P17.json`, `fase3/resultados/rev_i3.json`, `fase3/resultados/p19.json`, `fase3/inv_r4_zona251.py`, `fase3/resultados/r4_zona251.json`, `fase3/teste_grandes_cidades.py`, `fase3/resultados/teste_grandes_cidades.json`

### Q26. É possível demonstrar transferência individual entre candidatos com os dados existentes?
**Resposta:** Não. Com dados agregados e voto secreto, transferências individuais não são identificáveis; só os limites de Q24.
**Classificação:** Demonstrado no escopo definido (a impossibilidade)
**Em votos:** Não se traduz em votos: limite de identificabilidade (os limites estão na Q24).
- **Números:** Limites de Fréchet: razão entre abstencionistas de ~0 a 1,7 mi.
- **Demonstra:** A não identificabilidade com estes dados.
- **Não demonstra:** —
- **Robustez:** —
- **Causa:** não aplicável · **Alcance:** —
- **O que mudaria a resposta:** Só dados individuais (inexistentes por sigilo).
- **Validação:** Encerrada no escopo.
- **Evidências:** `fase2/resultados/P15.json`

## Matriz dos 33 itens do inventário

| Id | Resposta direta | Em votos | Classificação | Perguntas |
|---|---|---|---|---|
| P1 | O estimador de fluxos C06 recupera a verdade? Em parte: a ordem dos fluxos e o contraste com 2022 resistem; a magnitude '4:1' não (erro de ±0,5 a ±1,5 mi votos). | Erro de ±0,5 a ±1,5 mi votos na razão estimada. | Parcialmente demonstrado | Q24 |
| P2 | A bateria detecta trocas de votos? Só nos cenários e tamanhos da Q7. | Detectado nos cenários simulados: ~123 mil votos dispersos (2,8% da margem de 2026) e ~62 mil concentrados (1,4%). Não detectado: ~25 mil (0,6%). No município inteiro de uma grande cidade, a bateria original falha até ~696 mil votos, mas o teste T44 vê a partir de 31 mil a 139 mil (2% dos válidos). Inverter 2026 exigiria trocar ~2,22 mi votos de lado. | Parcialmente demonstrado | Q7 |
| P3 | As inconsistências dependem de canal e versão? Nos canais comparados (tabela, BU, decodificação de terceiro, divulgação ao vivo) não há inconsistência de votos; versões datadas dos arquivos não existem localmente. | 0 voto de diferença entre os canais comparados. | Parcialmente demonstrado | Q1, Q4, Q6, Q14 |
| P4 | A curva pública pode ser reconstruída pelos boletins recebidos? Sim, nos 39 instantes capturados: a recomposição pela ordem de recebimento reproduz o total divulgado (≤ 0,083 pp), sem defasagem. | Na captura final de cada eleição, 0 voto de diferença entre o total divulgado ao vivo e a base. A maior diferença em capturas parciais equivale a ~1,7 mil a ~3 mil votos naquele instante (seções com o mesmo horário de recebimento ordenadas de forma diferente), e não muda o líder. | Demonstrado no escopo definido | Q9, Q11, Q14 |
| P5 | O modelo de urna afeta a virada? Não, dentro de ±0,02 logit (2º turno, municípios com 2 ou mais modelos). | Maior efeito +0,004 logit, ~2,7 mil votos se fosse real. | Demonstrado no escopo definido |  |
| P6 | Boletins de terceiros validam os arquivos? Não foi possível determinar: não há boletins de terceiros com dados primários. | — | Não determinado com as evidências disponíveis | Q6 |
| P7 | A urna trocada vota diferente? Não, equivalente na margem de ±0,10 z fixada antes. | Diferença de −0,029 z, desprezível; não convertida em votos. | Demonstrado no escopo definido |  |
| P8 | A virada depende da ordem de chegada? Efeito desprezível (|r| ≤ 0,05); em 2022, −0,028, diferente de zero. | Efeito desprezível. | Demonstrado no escopo definido |  |
| P9 | Os locais atípicos do E02 resistem? Cerca de 0,1% dos locais, em três métodos; a lista depende do método; causa não demonstrada. | Cada local atípico: dezenas a poucas centenas de votos. | Parcialmente demonstrado | Q25 |
| P10 | A rajada sem biometria do T28 resiste? 8 urnas do 1º turno de 2026 seguem sinalizadas pelo critério beta-binomial (99 votos); em 2022 o mesmo critério sinaliza 18 e 21 urnas (23 e 25 pelo T28 original). | 99 votos nos últimos 30 min das 8 urnas (2026, 1º turno). | Demonstrado no escopo definido |  |
| P11 | Os certificados se ligam a uma âncora do TSE? Não foi possível determinar: válidos até a AC emissora; raiz não obtida. | Alcança todos os votos: nenhum voto, de 2022 ou 2026, tem a assinatura verificada até a raiz do TSE; todos estão verificados até a AC emissora. | Não determinado com as evidências disponíveis | Q5 |
| P12 | Diferença do eleitorado do exterior? Explicada: 423 de seções não instaladas + 72 + 30 de seções só nos arquivos de urna. | Eleitores aptos do exterior (−495 e −525), não votos. | Demonstrado no escopo definido |  |
| P13 | O C06b é reproduzível? Sim: 79 e 123 reproduzidos. | Trocas diretas entre finalistas em 2026: mínimo garantido de 79 e 123 votos, máximo de 43,5 mi e 39,4 mi; abstencionistas para Lula entre 4.116 e 32,3 mi. A razão do C06 erra de ±0,5 a ±1,5 mi votos. | Demonstrado no escopo definido | Q24 |
| P14 | Qual a causa da assimetria do T02 em 2022? Não demonstrada; o desvio está no nível da zona (251, 259) e persiste na 251 depois do perfil do eleitorado. | Salvador 2026: ~30 mil votos de Lula acima do previsto (0,7% da margem de 2026). Zona 251 (SP, 2022): ~4,2 mil votos de Lula acima da virada mediana da capital (0,2% da margem de 2022); zona 259: ~6,2 mil. Cauda pró-Lula do T02: ~740 votos (2026) e ~2.600 (2022). Cada local atípico: dezenas a poucas centenas de votos. | Parcialmente demonstrado | Q25 |
| P15 | Os limites de Fréchet estreitam a razão? Não: a razão não é identificada. | Abstencionistas para Lula entre 4.116 e 32,3 mi votos. | Demonstrado no escopo definido | Q24, Q26 |
| P16 | 200 seções conferem? Sim, 200/200 no 1º turno de 2026 (consistência interna); o 2º turno é coberto pelo T17b e pelo R1. | 0 voto de diferença nas 200 seções. | Demonstrado no escopo definido | Q1, Q2 |
| P17 | A assimetria de cauda do T02 é real? Sim, nos dois anos. | ~740 votos (2026) e ~2.600 (2022) na cauda pró-Lula. | Demonstrado no escopo definido | Q25 |
| P18 | O T13 bilateral vê os dois sentidos? Sim, para troca dispersa; limites na Q7. | Detectado nos cenários simulados: ~123 mil votos dispersos (2,8% da margem de 2026) e ~62 mil concentrados (1,4%). Não detectado: ~25 mil (0,6%). No município inteiro de uma grande cidade, a bateria original falha até ~696 mil votos, mas o teste T44 vê a partir de 31 mil a 139 mil (2% dos válidos). Inverter 2026 exigiria trocar ~2,22 mi votos de lado. | Parcialmente demonstrado | Q7 |
| P19 | Há dependência espacial entre municípios? Sim, Moran's I 0,16 a 0,20; causa não distinguida. | Não se traduz em votos. | Demonstrado no escopo definido | Q25 |
| P20 | O que há nos locais de SP 2022? Desvio no nível da zona, que persiste na 251 após o perfil; arquivos conferem; causa não demonstrada. | Salvador 2026: ~30 mil votos de Lula acima do previsto (0,7% da margem de 2026). Zona 251 (SP, 2022): ~4,2 mil votos de Lula acima da virada mediana da capital (0,2% da margem de 2022); zona 259: ~6,2 mil. Cauda pró-Lula do T02: ~740 votos (2026) e ~2.600 (2022). Cada local atípico: dezenas a poucas centenas de votos. | Parcialmente demonstrado | Q25 |
| P21 | Fontes externas e cadeia autenticada confirmam os arquivos? Só no agregado nacional ao vivo (Q6); boletins de terceiros e raiz não obtidos. | Na captura final de cada eleição, 0 voto de diferença entre o total divulgado ao vivo e a base. A maior diferença em capturas parciais equivale a ~1,7 mil a ~3 mil votos naquele instante (seções com o mesmo horário de recebimento ordenadas de forma diferente), e não muda o líder. | Parcialmente demonstrado | Q5, Q6 |
| R1-20 | A base coincide com decodificação independente? Sim, nas seções comuns (99,96% em 2022, 100% em 2026 1º turno); o 2º turno de 2026 não tem comparação de terceiro. | 0 voto de diferença nas seções comuns (~119 mi em 2026, 1º turno; ~118 mi por turno em 2022). | Parcialmente demonstrado | Q1 |
| C1 | As curvas são compatíveis com processos plausíveis de chegada? Não determinado (nenhum modelo de chegada validado). A curva divulgada é reproduzível com os dados por seção. | Não se traduz em votos: trata da ordem de chegada, não do total. | Não determinado com as evidências disponíveis | Q10, Q11, Q12 |
| C1a | Quando ocorreram as viradas? Ver Q8 e Q9. | A ordem de apuração não muda nenhum voto: a mesma soma final em qualquer ordem. A virada do 2º turno de 2022 ocorreu com 67,6% das urnas; a de 2026, com 47,2%. | Demonstrado no escopo definido | Q8, Q9 |
| C1b | Há periodicidade ou trechos lineares anômalos? Não determinado. | Não se traduz em votos: forma da curva. | Não determinado com as evidências disponíveis | Q11, Q12 |
| C2 | 2022 e 2026 têm as mesmas características? Diferem na descrição; semelhança estatística não determinada. | Não se traduz em votos: comparação da forma das curvas. | Não determinado com as evidências disponíveis | Q13 |
| M1 | O crescimento entre turnos é reconciliável? Sim, contabilmente (identidade exata); fluxos individuais não identificáveis. | 2026: os finalistas somaram +14,10 mi = 9,32 mi dos eliminados + 2,96 mi de comparecimento + 1,82 mi de brancos e nulos a menos. 2022: +10,22 mi = 9,90 mi + 0,57 mi − 0,25 mi. | Parcialmente demonstrado | Q21, Q22, Q23, Q24, Q26 |
| Z1 | Os zeros indicam anomalia? Sem divergência documental; excepcionalidade estatística não determinada pelo critério; sem excesso agregado descritivamente. | Se os zeros fossem anomalia, os votos em jogo seriam os que o candidato teria nessas seções: de ~44 a ~4.800 votos conforme o modelo (2026, 2º turno), no máximo 0,11% da margem de 4,43 mi. | Não determinado com as evidências disponíveis | Q15, Q16, Q17, Q18, Q19, Q20 |
| MET | Os métodos resistem à revisão? Com limites registrados: T10/T11 descritivos; T02 cego a município inteiro; E02 dependente do método; zeros sem modelo validado; concordância entre registros é consistência interna. | Detectado nos cenários simulados: ~123 mil votos dispersos (2,8% da margem de 2026) e ~62 mil concentrados (1,4%). Não detectado: ~25 mil (0,6%). No município inteiro de uma grande cidade, a bateria original falha até ~696 mil votos, mas o teste T44 vê a partir de 31 mil a 139 mil (2% dos válidos). Inverter 2026 exigiria trocar ~2,22 mi votos de lado. | Parcialmente demonstrado | Q7 |
| AUT | Os arquivos são autênticos? Íntegros e assinados até a AC emissora; consistentes entre si; a autenticidade integral do processo não é verificável com dados públicos. | 0 voto de diferença entre a tabela e os boletins em todos os ~128 milhões de votos de 2026 (2º turno) e ~124 milhões de 2022 conferidos. As 5 seções de 2022 sem arquivo somam 5 votos de comparecimento. Alcança todos os votos: nenhum voto, de 2022 ou 2026, tem a assinatura verificada até a raiz do TSE; todos estão verificados até a AC emissora. | Parcialmente demonstrado | Q1, Q2, Q3, Q5, Q6 |
| A173 | Os 173 arquivos estão ausentes da publicação? Sim, do pacote de dados abertos (duas cópias); conteúdo não verificado; outro canal do TSE inacessível. | 64 seções com 21.112 comparecimentos; votos do boletim iguais à tabela. | Parcialmente demonstrado | Q4 |
| BU1 | A seção com BU não lido concorda? Sim (boletim do Sistema de Apuração, assinatura válida; consistência interna). | 16 votos, iguais à tabela. | Demonstrado no escopo definido | Q20 |
| SA22 | As 159 seções do Sistema de Apuração de 2022 conferem? Sim, 159/159 (consistência interna). | 27.692 votos, iguais à tabela. | Demonstrado no escopo definido | Q1 |

## Achados que persistem sem causa demonstrada

- Salvador (2026): virada de Lula ~30 mil votos acima do previsto pelo histórico, em todas as zonas, única entre as 27 capitais, não explicada pelo perfil do eleitorado (T44, final_salvador.json); sem 2º turno estadual na Bahia; Fortaleza com desvio parecido no sentido oposto.
- Assimetria de cauda do T02 (pró-Lula) real nos dois anos; em SP 2022, desvio da zona 251 que persiste após o perfil do eleitorado.
- RS 88013/2/199 (2022): imagem do boletim (196 votos) diferente do boletim digital e da tabela (288); log publicado só cobre 196 votos.
- 2022: 153 seções-turno com log diferente do comparecimento (5.287 votos sem registro no log publicado; 2.503 votos a mais no log em 47 seções), recontagem confirmada (fila F1).
- 173 arquivos assinados e 485 auxiliares fora do pacote de dados abertos de 2022.
- 8 urnas com rajada sem biometria no fim do dia (2026, 1º turno; 99 votos), padrão também presente em 2022.
- Última troca de liderança mais tardia que nos modelos nulos e que o modelo de atraso de transmissão prevê, nos dois anos (fila F4).

## Limites das fontes e dos métodos

- Autenticidade só até a AC emissora (sem âncora do TSE).
- BU, RDV, imagem e log não são testemunhas independentes entre si.
- Comprometimento anterior à geração dos registros (H2) não é distinguível com dados públicos.
- Única fonte externa de custódia: capturas do Internet Archive (agregado nacional, instantes amostrados).
- Fluxos individuais entre turnos não identificáveis.
- Sem modelo de chegada validado (curvas) e sem modelo de cauda baixa validado (zeros).
