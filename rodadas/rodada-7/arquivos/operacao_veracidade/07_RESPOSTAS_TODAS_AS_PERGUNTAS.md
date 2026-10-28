# 07. Resposta científica a cada pergunta de todas as fases

Fonte: `fase3/respostas_f3.json` (gerado por `fase3/f3_respostas.py`; as respostas anteriores não foram alteradas aqui), com os campos extras abaixo e as perguntas novas desta operação (N1 a N9). Cada item diz o que foi tentado e por que a resposta não é mais forte.

Mapa fase → pergunta: Q1 a Q26 e os 33 itens do inventário são da F2 e F3 (V1.1 a V1.3); Q27 a Q39 são da rodada 6 (V1.4); Q40 e Q41 são da rodada 7 (registro vivo); N1 a N9 são desta operação (no site, N9 é a Q42 e N1 a N9 são Q43 a Q50).

## Parte A. Perguntas do capítulo de respostas (Q1 a Q41)

### Capítulo: Integridade dos resultados oficiais

### Q1. Os votos oficiais por seção são iguais aos boletins de urna?
- **Resposta direta:** Sim, em todas as seções cujo boletim foi lido, nos dois anos e nos dois turnos: 0 diferenças entre a tabela publicada e o bu.dat.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/inv_r1_integridade.py`, `fase3/resultados/r1_integridade.json`, `fase3/resultados/sa22.json`, `fase3/resultados/R1_20_dataurnas.json`
- **Cobertura:** Todas as seções com boletim publicado; votos de Presidente.
- **Validação:** Executado e reproduzido (R1, releitura).
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Os votos da tabela publicada são os mesmos dos boletins digitais assinados pelas urnas.
- **O que não demonstra:** Consistência interna: BU, RDV, imagem e log são gerados pela mesma urna e assinados pela mesma chave; tabela e totais vêm do mesmo TSE. A concordância não verifica de forma independente o que foi votado. Não exclui comprometimento anterior à geração do boletim (H2).
- **Impacto em votos:** 0 voto de diferença entre a tabela e os boletins em todos os ~128 milhões de votos de 2026 (2º turno) e ~124 milhões de 2022 conferidos. As 5 seções de 2022 sem arquivo somam 5 votos de comparecimento.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q2. Os votos publicados podem ser reconstruídos a partir dos RDVs disponíveis?
- **Resposta direta:** Sim, em todas as seções com RDV lido: a recontagem voto a voto dá os mesmos totais de candidatos, brancos e nulos da tabela.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/resultados/r1_integridade.json`, `testes/registro.json (T17, T17b)`
- **Cobertura:** Seções com RDV publicado.
- **Validação:** Executado (R1).
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** A tabela pode ser recomposta voto a voto pelo RDV publicado.
- **O que não demonstra:** O RDV é gravado pela mesma urna e pelo mesmo software que geram o boletim: a recontagem não é contagem independente do que o eleitor digitou.
- **Impacto em votos:** 0 voto de diferença entre a recontagem pelo RDV e a tabela, nos dois anos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q3. Existem divergências verificáveis entre boletins, RDV, logs, tabelas e totalização?
- **Resposta direta:** Nos votos, não. Entre arquivos e entre log e comparecimento, sim: há divergências objetivas pontuais, preservadas como achados, sem efeito demonstrado sobre votos.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/resultados/r1_integridade.json`, `fase3/resultados/adv_log_x_comparecimento.json`, `fase3/RELATORIO_ADVERSARIAL.md`, `analise/resultado_casos_integridade_1t.json`, `testes/registro.json (T32, T36)`
- **Cobertura:** Seções com arquivos; Presidente.
- **Validação:** Executado (R1, auditoria adversarial).
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Há divergências documentais objetivas, todas pequenas e sem deslocamento de votos detectável nas seções envolvidas.
- **O que não demonstra:** A causa de cada divergência. As explicações operacionais vêm do próprio sistema (compatíveis, não verificadas).
- **Impacto em votos:** Nenhuma divergência muda um voto da tabela. Divergências de registro: 2022, 5.287 votos sem registro no log publicado e 2.503 a mais no log (0,25% e 0,12% da margem de 2022); RS 88013/2/199, 92 votos entre a imagem do boletim (196) e o boletim digital (288); 2026, 113 votos em 16 seções-turno do T36 (0,003% da margem).
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

### Q4. Existem arquivos ausentes, seções não cobertas ou versões conflitantes? Qual o alcance?
- **Resposta direta:** Sim, arquivos ausentes e algumas seções não cobertas; versões conflitantes não foram encontradas no que foi possível comparar.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/resultados/a173.json`, `fase3/resultados/sa22.json`, `fase3/resultados/a1.json`, `fase3/resultados/r1_integridade.json`, `fase3/resultados/r2_curva_publica.json`
- **Cobertura:** Pacotes de dados abertos do TSE.
- **Validação:** Executado (A173, SA22, R1, R2).
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Ausências de publicação objetivas e de alcance pequeno; os boletins dessas seções coincidem com a tabela.
- **O que não demonstra:** O conteúdo dos arquivos ausentes; republicação de arquivos entre datas (só há uma versão local).
- **Impacto em votos:** Seções com arquivos ausentes: 64 seções com 21.112 comparecimentos em 2022 (boletim presente e igual à tabela); o Sistema de Apuração soma 27.692 votos em 2022 e as seções de 2026 também conferem; as 5 seções sem arquivo somam 5 votos.
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

### Q5. Os registros foram autenticados criptograficamente até uma fonte de confiança apropriada?
- **Resposta direta:** Não até a raiz: as assinaturas das urnas são válidas até a autoridade certificadora emissora em 100% das urnas de 2022 e 2026 (cadeia verificada por completo em 28/10/2026, T60a; antes, só em 200 seções e em 5% por terceiro), mas a ligação dessa autoridade a uma âncora do TSE não foi verificada: a raiz não é pública.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `testes/registro.json (T16, T60a, T60b)`, `fase2/resultados/P11.json`, `fase3/resultados/sa22.json`, `fase3/resultados/r1_integridade.json`, `operacao_veracidade/resultados/cert_analise.json`
- **Cobertura:** Arquivos presentes.
- **Validação:** Bloqueado no elo final (fonte externa).
- **Independência:** Interna (lista assinada) + cadeia até a AC emissora (T60a, N1); raiz não pública
- **O que demonstra:** Os arquivos presentes não foram alterados depois de assinados pela chave da urna, e todo certificado de urna é assinado pela AC emissora que temos.
- **O que não demonstra:** Que a chave pertence a uma urna autêntica do TSE (sem âncora); que a AC usada é a oficial (cópia de terceiro); qualquer coisa anterior à assinatura.
- **Impacto em votos:** Alcança todos os votos: nenhum voto, de 2022 ou 2026, tem a assinatura verificada até a raiz do TSE; todos estão verificados até a AC emissora (100% das urnas, verificação completa em 28/10/2026, T60a).
- **Próxima evidência decisiva:** AC RAIZ UE e AC URNA v2 obtidas por canal oficial verificável (página do TSE responde HTTP 403 a este ambiente)

### Q6. Existem evidências externas independentes que confirmem ou contradigam os registros publicados?
- **Resposta direta:** Sim, duas, e as duas confirmam: capturas do Internet Archive dos totais nacionais divulgados durante a apuração confirmam a base publicada nos instantes capturados; e 404 boletins impressos lidos por terceiros no 2º turno de 2026 (22 UFs) são iguais à tabela e ao BU do TSE, com assinatura e cadeia válidas (T61). Os boletins são amostra de conveniência (0,08% das seções), não sorteada; de 2022 não há boletins de terceiros.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/inv_r2_curva_publica.py`, `fase3/resultados/r2_curva_publica.json`, `fase3/externos/wayback_capturas/`, `testes/registro.json (T61)`, `operacao_veracidade/resultados/terceiros_qr.json`
- **Cobertura:** Totais nacionais de Presidente em 39 instantes; 404 seções do 2º turno de 2026.
- **Validação:** Executado (R2, T61), com bloqueio parcial do Internet Archive registrado.
- **Independência:** Externa parcial (terceiro preservou ou leu conteúdo do TSE; não é a urna)
- **O que demonstra:** Que a base publicada depois corresponde ao que foi divulgado ao vivo, no agregado nacional e nos instantes capturados (contraria alteração posterior que mudasse esses totais).
- **O que não demonstra:** Correspondência seção a seção com fonte externa fora das 404 seções; o que aconteceu antes da geração do boletim; instantes não capturados.
- **Impacto em votos:** Nas 404 seções com boletim de terceiro, 0 voto de diferença. Na captura final de cada eleição, 0 voto de diferença entre o total divulgado ao vivo e a base. A maior diferença em capturas parciais equivale a ~1,7 mil a ~3 mil votos naquele instante (seções com o mesmo horário de recebimento ordenadas de forma diferente), e não muda o líder.
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística, coletados por fiscais de partidos ou observadores, com lista de seções sorteada antes

### Q7. Os testes conseguem detectar mecanismos plausíveis de alteração, e em quais condições falham?
- **Resposta direta:** Detectam alguns, em condições limitadas: nos cenários simulados, trocas dispersas de ~123 mil votos e concentradas de ~62 mil em locais ou municípios de até ~5 mil seções foram detectadas no sentido certo; trocas de ~25 mil não foram detectadas; no município inteiro das 5 maiores cidades, a bateria original não detecta, mas o teste T44 (histórico de 2022 e perfil do 1º turno) detecta a partir de 2% dos válidos (31 mil a 139 mil votos). A grade adversarial do T63 (15 mecanismos, dois sentidos) mostra o resto do mapa: seções, locais, zonas e municípios são vistos a partir de 25 a 50 mil votos; UFs inteiras, os cinco grandes juntos, macrorregião, lote tardio, conversão de brancos e nulos, enchimento abaixo de 250 mil e deslocamento uniforme só a partir de 0,5 a 2,2 milhões, ou nunca; e o poder é assimétrico entre os sentidos.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/rev_i1_poder.py`, `fase3/rev_a2_poder.py`, `fase3/resultados/rev_a2_2026.json`, `fase3/resultados/rev_a2_2022.json`, `testes/registro.json (T63)`, `operacao_veracidade/03_SIMULACOES_ADVERSARIAIS.md`
- **Cobertura:** 4 mecanismos + grandes cidades (I1, A2); 15 mecanismos, 7 magnitudes e 2 sentidos (T63).
- **Validação:** Executado (I1, A2).
- **Independência:** Sintética (simulação; nenhum voto real alterado)
- **O que demonstra:** O alcance dos testes nos cenários simulados.
- **O que não demonstra:** Detecção fora dos cenários simulados; mecanismos que preservam medianas, mexem no comparecimento ou atuam antes do boletim; que a base real esteja limpa (o poder é medido sobre ela); votos simulados não são votos encontrados.
- **Impacto em votos:** Detectado nos cenários simulados: ~123 mil votos dispersos (2,8% da margem de 2026) e ~62 mil concentrados (1,4%). Não detectado: ~25 mil (0,6%). No município inteiro de uma grande cidade, a bateria original falha até ~696 mil votos, mas o teste T44 vê a partir de 31 mil a 139 mil (2% dos válidos). No T63, UFs, região, lote e deslocamento uniforme passam sem alarme até ~0,5 a 2,2 mi votos, ou sempre (uniforme em logit). Inverter 2026 exigiria trocar ~2,22 mi votos de lado.
- **Próxima evidência decisiva:** Mais mecanismos (UF inteira, região, lote) com poder medido por detector; ver 03_SIMULACOES_ADVERSARIAIS.md

### Capítulo: Curvas, viradas e periodicidade

### Q8. Quantas vezes a liderança mudou na ordem de recebimento dos boletins?
- **Resposta direta:** Depois dos primeiros 10% de urnas: 2022, 1º turno 1 vez (aos 68,2%); 2022, 2º turno 1 vez (aos 67,6%, adversário → Lula); 2026, 1º turno nenhuma; 2026, 2º turno 2 vezes (aos 13,5%, Lula → adversário, e aos 47,2%, adversário → Lula).
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/f3_curvas.py`, `fase3/resultados/E2_curvas.json`
- **Cobertura:** Votos de Presidente, ordem por DT_BU_RECEBIDO.
- **Validação:** Executado (E2).
- **Independência:** Interna (hora de recebimento registrada pelo próprio TSE) + capturas de terceiro (externa parcial)
- **O que demonstra:** O número de viradas na ordem de recebimento (reconstrução).
- **O que não demonstra:** Antes dos 10% das urnas; a ordem é de recebimento, não de divulgação (ver Q9).
- **Impacto em votos:** A ordem de apuração não muda nenhum voto: a mesma soma final em qualquer ordem. A virada do 2º turno de 2022 ocorreu com 67,6% das urnas; a de 2026, com 47,2%.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q9. Quantas vezes a liderança mudou na sequência pública efetivamente divulgada?
- **Resposta direta:** Nas capturas disponíveis: 2022, 1º turno pelo menos 1; 2022, 2º turno 1 (adversário até 18:22, com 49,53% para Lula; Lula a partir de 19:43); 2026, 1º turno 0; 2026, 2º turno pelo menos 2 (Lula às 19:36 com 50,55%, adversário às 20:07 com 49,56%, Lula às 21:25). A sequência capturada é amostrada: os números são limites inferiores entre capturas.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/resultados/r2_curva_publica.json`, `fase3/externos/wayback_capturas/`
- **Cobertura:** Totais nacionais divulgados.
- **Validação:** Executado (R2).
- **Independência:** Externa parcial (terceiro preservou ou leu conteúdo do TSE; não é a urna)
- **O que demonstra:** As viradas observadas na divulgação coincidem em sentido e momento com a reconstrução.
- **O que não demonstra:** Viradas entre capturas não observadas; 2022 1º turno e 2026 têm poucas capturas.
- **Impacto em votos:** Idem: a sequência divulgada é a soma parcial dos mesmos votos; 0 voto de diferença no total final.
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

### Q10. Uma quantidade pequena de viradas é incomum sob modelos realistas de chegada dos boletins?
- **Resposta direta:** Não determinado: nenhum dos cinco nulos de permutação é calibrado, e o modelo de chegada com as horas reais de emissão e atraso de transmissão sorteado (fila F4) não foi validado em 2022 (última troca e maior vale fora da faixa; 0 de 27 capturas na faixa). O número de trocas observado cabe no modelo nos quatro casos, mas isso não é confirmatório.
- **Estado:** Não determinado com as evidências disponíveis
- **Evidência:** `fase3/resultados/E2_curvas.json`, `fase3/resultados/E2b_curvas.json`
- **Cobertura:** —
- **Validação:** Tentado (E2, E2b, F4); nenhum validado. Parado pelo critério.
- **Independência:** Interna (hora de recebimento registrada pelo próprio TSE) + capturas de terceiro (externa parcial)
- **O que demonstra:** —
- **O que não demonstra:** Que as viradas sejam comuns ou incomuns.
- **Impacto em votos:** Não se traduz em votos: trata da ordem de chegada, não do total.
- **Próxima evidência decisiva:** Registro de recebimento do sistema de totalização do TSE e capturas da divulgação com resolução de minutos

### Q11. Os vales aparentemente periódicos e os trechos lineares são reproduzíveis com os dados brutos?
- **Resposta direta:** A curva divulgada é reproduzível com os dados por seção nos 39 instantes capturados (diferença ≤ 0,083 pp); periodicidade não foi testada com estatística validada.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/resultados/r2_curva_publica.json`, `fase3/resultados/E2_curvas.json`
- **Cobertura:** Curvas de 2022 e 2026.
- **Validação:** Parcial.
- **Independência:** Interna (hora de recebimento registrada pelo próprio TSE) + capturas de terceiro (externa parcial)
- **O que demonstra:** Que os pontos divulgados saem dos dados publicados por seção.
- **O que não demonstra:** Que vales ou trechos lineares sejam anômalos ou normais.
- **Impacto em votos:** Não se traduz em votos: forma da curva.
- **Próxima evidência decisiva:** idem Q10

### Q12. Os padrões continuam anômalos após controles por geografia, lotes, horários, arredondamento e dependência territorial?
- **Resposta direta:** Não determinado: com controles por UF, município, hora de encerramento e tamanho, os nulos continuam rejeitando também em 2022, então não discriminam.
- **Estado:** Não determinado com as evidências disponíveis
- **Evidência:** `fase3/resultados/E2b_curvas.json`
- **Cobertura:** —
- **Validação:** Tentado.
- **Independência:** Interna (hora de recebimento registrada pelo próprio TSE) + capturas de terceiro (externa parcial)
- **O que demonstra:** —
- **O que não demonstra:** Anomalia ou normalidade da curva.
- **Impacto em votos:** Não se traduz em votos: forma da curva.
- **Próxima evidência decisiva:** idem Q10

### Q13. 2022 e 2026 apresentam semelhanças estatisticamente relevantes depois desses controles?
- **Resposta direta:** Não determinado estatisticamente. Descritivamente: nos dois anos a última troca de liderança vem mais tarde do que nos modelos nulos e do que o modelo de atraso de transmissão prevê (2022 2º turno: 68% contra 39% a 42%; 2026 2º turno: 48% contra 30% a 34%); em 2026 a ordem de chegada é mais territorial (η² por UF 0,39 contra 0,24).
- **Estado:** Não determinado com as evidências disponíveis
- **Evidência:** `fase3/resultados/E2_curvas.json`
- **Cobertura:** —
- **Validação:** Parcial.
- **Independência:** Interna (hora de recebimento registrada pelo próprio TSE) + capturas de terceiro (externa parcial)
- **O que demonstra:** Semelhanças descritivas.
- **O que não demonstra:** Semelhança estatística após controles.
- **Impacto em votos:** Não se traduz em votos: comparação da forma das curvas.
- **Próxima evidência decisiva:** idem Q10

### Q14. Há divergência objetiva entre a sequência publicada e os registros históricos disponíveis?
- **Resposta direta:** Não: nas 39 capturas históricas, a sequência divulgada é igual à recomposta pela base final (≤ 0,083 pp, mesmo líder, votos que nunca diminuem, total final igual).
- **Estado:** Refutado no escopo definido (a hipótese de divergência)
- **Evidência:** `fase3/resultados/r2_curva_publica.json`
- **Cobertura:** Totais nacionais.
- **Validação:** Executado (R2).
- **Independência:** Externa parcial (terceiro preservou ou leu conteúdo do TSE; não é a urna)
- **O que demonstra:** Ausência de divergência nos instantes capturados (custódia independente).
- **O que não demonstra:** Instantes não capturados; divergência seção a seção que preserve o total nacional.
- **Impacto em votos:** 0 voto de diferença entre a sequência divulgada e a base nas capturas finais.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Capítulo: Zeros de votos

### Q15. Quantas seções tiveram zero votos para Flávio Bolsonaro em cada turno de 2026?
- **Resposta direta:** 79 no 1º turno e 106 no 2º.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/resultados/E3_zeros.json`
- **Cobertura:** Seções do Brasil.
- **Validação:** Executado (E3).
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** A contagem.
- **O que não demonstra:** —
- **Impacto em votos:** Nas 79 seções do 1º turno, 9.542 votos foram para Lula; nas 106 do 2º turno, 14.860 (todos os válidos dessas seções). São 0,34% da margem de 2026.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q16. Quantas tiveram comparecimento positivo e registros válidos?
- **Resposta direta:** Todas: 79 e 106 com comparecimento positivo, e boletim, RDV, imagem e tabela consistentes entre si em todas.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/resultados/E3_zeros.json`, `fase3/resultados/bu1.json`
- **Cobertura:** Seções do Brasil.
- **Validação:** Executado.
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Que não são seções vazias nem erros de leitura.
- **O que não demonstra:** Consistência interna: BU, RDV, imagem e log são gerados pela mesma urna e assinados pela mesma chave; tabela e totais vêm do mesmo TSE. A concordância não verifica de forma independente o que foi votado.
- **Impacto em votos:** Os votos dessas seções conferem nos registros: 0 voto de diferença.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q17. Como essas seções mudaram entre o primeiro e o segundo turno?
- **Resposta direta:** Das seções com zero em algum turno: 50 com zero nos dois, 56 passaram de votos a zero e 29 de zero a votos.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/resultados/E3_zeros.json`
- **Cobertura:** Seções do Brasil.
- **Validação:** Executado.
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** As transições.
- **O que não demonstra:** Por quê.
- **Impacto em votos:** Não se traduz em votos: transições entre turnos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q18. O fenômeno é estatisticamente incomum depois de controlar tamanho, município, local e heterogeneidade?
- **Resposta direta:** Não determinado: nenhum modelo de cauda baixa passou na calibração. O modelo do R3 (que previa 79,1 e 101,5 zeros contra 79 e 106) falhou o critério pré-registrado, então não sustenta nem excesso nem ausência de excesso; as três famílias novas do T64 também falham (por município, 1,3 zeros previstos contra 106; por local de votação, 66,7 contra 106). Descritivamente, os zeros são locais de uma só seção, com menos de 1% do total.
- **Estado:** Não determinado com as evidências disponíveis
- **Evidência:** `fase3/inv_r3_zeros.py`, `fase3/resultados/r3_zeros.json`, `fase3/resultados/rev_i2.json`, `testes/registro.json (T41, T64)`, `operacao_veracidade/05_ZEROS_E_ENTRE_TURNOS.md`
- **Cobertura:** Seções do Brasil; Flávio 2026.
- **Validação:** Executado (R3); validação formal falhou.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** Só a descrição: onde estão e que os registros conferem.
- **O que não demonstra:** Excesso ou ausência de excesso (nenhum modelo calibrou); ausência de excesso em seções específicas.
- **Impacto em votos:** Se os zeros fossem anomalia, os votos em jogo seriam os que o candidato teria nessas seções: de ~44 a ~4.800 votos conforme o modelo (2026, 2º turno), no máximo 0,11% da margem de 4,43 mi.
- **Próxima evidência decisiva:** Modelo de cauda baixa que passe no critério fixado (nenhum das 3 famílias testadas em T64 passou)

### Q19. O mesmo método identifica padrões semelhantes em 2022?
- **Resposta direta:** Sim, com o mesmo resultado: não determinado. Bolsonaro 2022 teve 160 e 141 zeros; o modelo do R3 previa 162,9 e 136,5, mas falhou o mesmo critério formal, e no T64 o modelo por município prevê 4,3 contra 141 e o por local, 63,3 contra 141, ambos reprovados. Descritivamente, os zeros de 2022 também são locais de uma só seção, com menos de 1% do total.
- **Estado:** Não determinado com as evidências disponíveis
- **Evidência:** `fase3/resultados/r3_zeros.json`, `testes/registro.json (T64)`
- **Cobertura:** Bolsonaro 2022.
- **Validação:** Executado (R3).
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** Que 2026 e 2022 têm a mesma descrição e a mesma falha dos modelos.
- **O que não demonstra:** Excesso ou normalidade (nenhum modelo calibrou).
- **Impacto em votos:** 2022: de ~66 a ~4.300 votos esperados para Bolsonaro nessas seções, no máximo 0,2% da margem de 2,14 mi.
- **Próxima evidência decisiva:** idem Q18

### Q20. Existem divergências objetivas nos boletins ou apenas resultados numéricos extremos?
- **Resposta direta:** Apenas resultados numéricos extremos: 0 divergências de votos entre boletim, RDV, imagem e tabela nas 486 seções-turno com zero votos para um finalista.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/resultados/E3_zeros.json`, `fase3/resultados/bu1.json`
- **Cobertura:** Seções com zero.
- **Validação:** Executado.
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Ausência de divergência documental nessas seções.
- **O que não demonstra:** Consistência interna: BU, RDV, imagem e log são gerados pela mesma urna e assinados pela mesma chave; tabela e totais vêm do mesmo TSE. A concordância não verifica de forma independente o que foi votado.
- **Impacto em votos:** 0 voto de diferença nos registros dessas seções.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Capítulo: Mudança entre o primeiro e o segundo turno

### Q21. Quantos votos cada finalista ganhou ou perdeu entre os turnos?
- **Resposta direta:** 2022: Lula +3.086.495, Bolsonaro +7.134.009. 2026: Lula +10.376.694, Flávio +3.721.538 (base por seção, com exterior).
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/resultados/entre_turnos_contas.json`
- **Cobertura:** Brasil e exterior.
- **Validação:** Executado.
- **Independência:** Aritmética exata sobre totais do TSE
- **O que demonstra:** As variações.
- **O que não demonstra:** Quem mudou de voto.
- **Impacto em votos:** 2022: Lula +3,09 mi, Bolsonaro +7,13 mi. 2026: Lula +10,38 mi, Flávio +3,72 mi.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q22. Quanto da mudança corresponde a comparecimento, votos dos eliminados, brancos e nulos?
- **Resposta direta:** Toda a mudança fecha exatamente: ganho dos finalistas = votos dos eliminados no 1º turno + variação do comparecimento − variação de brancos e nulos.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/resultados/entre_turnos_contas.json`
- **Cobertura:** Totais.
- **Validação:** Executado.
- **Independência:** Aritmética exata sobre totais do TSE
- **O que demonstra:** A identidade contábil.
- **O que não demonstra:** A divisão dos eliminados entre os finalistas (ver Q24).
- **Impacto em votos:** 2026: os finalistas somaram +14,10 mi = 9,32 mi dos eliminados + 2,96 mi de comparecimento + 1,82 mi de brancos e nulos a menos. 2022: +10,22 mi = 9,90 mi + 0,57 mi − 0,25 mi.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q23. Existem diferenças impossíveis de reconciliar com os totais oficiais?
- **Resposta direta:** Não: as contas fecham nacionalmente e nenhuma seção tem mais votos que comparecimento ou mais comparecimento que aptos.
- **Estado:** Refutado no escopo definido (a hipótese de diferença impossível)
- **Evidência:** `fase3/resultados/entre_turnos_contas.json`, `testes/registro.json (T32)`
- **Cobertura:** Todas as seções.
- **Validação:** Executado.
- **Independência:** Aritmética exata sobre totais do TSE
- **O que demonstra:** Ausência de impossibilidade contábil.
- **O que não demonstra:** Que os números reflitam os votos dados (ver integridade).
- **Impacto em votos:** 0 voto inconsistente: nenhuma seção com mais votos que comparecimento.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q24. Quais fluxos entre escolhas são matematicamente possíveis?
- **Resposta direta:** Um intervalo amplo: os dados agregados admitem desde fluxos quase nulos até milhões de votos em cada direção; só limites, não um fluxo.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase2/resultados/P13.json`, `fase2/resultados/P15.json`, `fase2/sessao_limitada_2026-10-28/p1_resultado_principal.json`
- **Cobertura:** Seções do Brasil.
- **Validação:** Executado (F2).
- **Independência:** Aritmética exata sobre totais do TSE
- **O que demonstra:** Os limites matemáticos.
- **O que não demonstra:** Qual fluxo ocorreu.
- **Impacto em votos:** Trocas diretas entre finalistas em 2026: mínimo garantido de 79 e 123 votos, máximo de 43,5 mi e 39,4 mi; abstencionistas para Lula entre 4.116 e 32,3 mi. A razão do C06 erra de ±0,5 a ±1,5 mi votos.
- **Próxima evidência decisiva:** Dado individual (inexistente por sigilo) ou pesquisa de painel

### Q25. O padrão territorial de crescimento apresenta desvios persistentes após controles?
- **Resposta direta:** Sim, em parte: a assimetria de cauda do T02 é real nos dois anos; cerca de 0,1% dos locais são atípicos (lista depende do método); há dependência espacial entre municípios; em São Paulo 2022 a zona 251 mantém desvio depois de controlar o perfil do eleitorado; em 2026, Salvador tem virada de Lula ~30 mil votos acima do previsto pelo histórico, em todas as 19 zonas (T44), a única entre as 27 capitais e não explicada pelo perfil do eleitorado; Fortaleza tem desvio de tamanho parecido no sentido oposto.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase2/resultados/P17.json`, `fase3/resultados/rev_i3.json`, `fase3/resultados/p19.json`, `fase3/inv_r4_zona251.py`, `fase3/resultados/r4_zona251.json`, `fase3/teste_grandes_cidades.py`, `fase3/resultados/teste_grandes_cidades.json`
- **Cobertura:** Brasil; SP capital para a zona 251.
- **Validação:** Executado (R4, I3, P17, P19).
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** Que há desvios territoriais persistentes, inclusive na zona 251 depois do perfil.
- **O que não demonstra:** A causa; que sejam irregularidades.
- **Impacto em votos:** Salvador 2026: ~30 mil votos de Lula acima do previsto (0,7% da margem de 2026). Zona 251 (SP, 2022): ~4,2 mil votos de Lula acima da virada mediana da capital (0,2% da margem de 2022); zona 259: ~6,2 mil. Cauda pró-Lula do T02: ~740 votos (2026) e ~2.600 (2022). Cada local atípico: dezenas a poucas centenas de votos.
- **Próxima evidência decisiva:** Covariáveis externas por zona (renda, migração, campanha); fiscalização presencial das zonas citadas

### Q26. É possível demonstrar transferência individual entre candidatos com os dados existentes?
- **Resposta direta:** Não. Com dados agregados e voto secreto, transferências individuais não são identificáveis; só os limites de Q24.
- **Estado:** Demonstrado no escopo definido (a impossibilidade)
- **Evidência:** `fase2/resultados/P15.json`
- **Cobertura:** —
- **Validação:** Encerrada no escopo.
- **Independência:** Aritmética exata sobre totais do TSE
- **O que demonstra:** A não identificabilidade com estes dados.
- **O que não demonstra:** —
- **Impacto em votos:** Não se traduz em votos: limite de identificabilidade (os limites estão na Q24).
- **Próxima evidência decisiva:** idem Q24

### Capítulo: Alegações públicas testadas

### Q27. A live de 4/11/2022 dizia que urnas anteriores a 2020 deram mais votos a Lula. Isso é verdade?
- **Resposta direta:** A diferença existe, mas é de lugar, não de urna: no 1º turno de 2022 Lula teve 50,3% nas antigas e 46,0% nas UE2020, e a diferença persiste dentro do município; comparando urnas do mesmo local de votação, ela some (equivalente a zero em ±0,02 logit nos dois turnos).
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/PREREG_LIVE_2022.md`, `fase3/live_2022.py`, `fase3/resultados/live_2022.json`, `docs/pesquisas/2026-10-28_live_cerimedo_2022.md`
- **Cobertura:** 2022, Brasil.
- **Validação:** T47 (pré-registrado, emenda 7); P5/T20.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados; alegação pública (a origem da pergunta não é fonte)
- **O que demonstra:** Que o modelo de urna não muda o voto quando se compara o mesmo lugar.
- **O que não demonstra:** A causa da distribuição desigual dos modelos.
- **Impacto em votos:** Dentro do local: ~600 votos (1º turno) e ~440 (2º), contra margem de 2,14 mi (2022).
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q28. O log das urnas antigas não identifica a urna, como alegou o PL em 2022?
- **Resposta direta:** O bug existe: nas 279.291 seções com urnas UE2009 a UE2015 o campo de identificação do log traz o valor fixo 67305985. Mas o log se liga ao boletim e ao RDV pela assinatura da urna e pelo número do certificado em 279.285 delas; as 6 restantes são trocas de urna e arquivos faltantes já catalogados. Em 2026 o bug não aparece.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/PREREG_LIVE_2022.md`, `fase3/live_2022.py`, `fase3/resultados/live_2022.json`, `docs/pesquisas/2026-10-28_live_cerimedo_2022.md`
- **Cobertura:** 2022 e 2026, dois turnos.
- **Validação:** T45 (emenda 7).
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados; alegação pública (a origem da pergunta não é fonte)
- **O que demonstra:** Que o log se liga ao BU apesar do bug.
- **O que não demonstra:** Consistência interna: BU, RDV, imagem e log são gerados pela mesma urna e assinados pela mesma chave; tabela e totais vêm do mesmo TSE. A concordância não verifica de forma independente o que foi votado.
- **Impacto em votos:** As 6 seções sem ligação completa somam menos de 2 mil votos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q29. Contando só as urnas UE2020, Bolsonaro teria vencido 2022 com 51,05%?
- **Resposta direta:** A conta está certa (51,0508%), mas mede o voto das cidades que tinham UE2020, não o efeito do modelo: 220 mil seções com urnas antigas estavam em municípios sem nenhuma UE2020. Comparando dentro do mesmo município, Lula continua vencendo (Bolsonaro 49,25%).
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/PREREG_LIVE_2022.md`, `fase3/live_2022.py`, `fase3/resultados/live_2022.json`, `docs/pesquisas/2026-10-28_live_cerimedo_2022.md`
- **Cobertura:** 2º turno de 2022.
- **Validação:** T46 (emenda 7).
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados; alegação pública (a origem da pergunta não é fonte)
- **O que demonstra:** Que o 51,05% é efeito de seleção geográfica.
- **O que não demonstra:** O voto de quem não votou em UE2020.
- **Impacto em votos:** Contrafactual dentro do município: −179 mil votos de Lula, menos que metade da margem de 2022 (1,07 mi).
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q30. Em 2022 havia dois softwares diferentes ou unanimidades ligadas ao modelo de urna?
- **Resposta direta:** Não: a mesma versão 8.26.0.0 em todas as seções de todos os modelos; as seções 100% de um candidato aparecem em cada modelo na proporção da sua presença nos mesmos municípios.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/PREREG_LIVE_2022.md`, `fase3/live_2022.py`, `fase3/resultados/live_2022.json`, `docs/pesquisas/2026-10-28_live_cerimedo_2022.md`
- **Cobertura:** 2022.
- **Validação:** T48 (emenda 7).
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados; alegação pública (a origem da pergunta não é fonte)
- **O que demonstra:** Software único segundo o log; unanimidade sem relação com modelo.
- **O que não demonstra:** Versão lida do próprio log (compatível com o registro).
- **Impacto em votos:** Unânimes de Lula: 16.418 votos (0,8% da margem de 2022).
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q31. Flávio teve zero voto em 106 urnas no 2º turno de 2026. Isso é anormal?
- **Resposta direta:** O número está certo (106 seções, 14.860 votos de Lula), e não há sinal de ruptura nem de erro de registro: em 2022 foram 141 seções com Bolsonaro zerado; são aldeias e comunidades do Norte e do Nordeste que já votavam quase só em Lula em 2022 (nenhuma com Bolsonaro acima de 11%) e no 1º turno; os 106 boletins conferem com o RDV e têm assinaturas válidas. Se o número é estatisticamente excepcional não foi determinado: nenhum modelo de cauda baixa calibrou (Q18, T64).
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/PREREG_ZEROS_FLAVIO.md`, `fase3/zeros_flavio.py`, `fase3/resultados/zeros_flavio.json`
- **Cobertura:** 2º turno de 2026 e 2022.
- **Validação:** T49 (emenda 8); Q15, Q20.
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Continuidade e integridade das seções.
- **O que não demonstra:** Consistência interna: BU, RDV, imagem e log são gerados pela mesma urna e assinados pela mesma chave; tabela e totais vêm do mesmo TSE. A concordância não verifica de forma independente o que foi votado.
- **Impacto em votos:** 14.860 votos (0,34% da margem de 2026).
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q32. O voto de Lula ficou mais concentrado em seções de mais de 80%?
- **Resposta direta:** Não, ficou menos: 35.591 seções com Lula acima de 80% em 2026, contra 40.046 em 2022; o saldo vindo dessas seções caiu de 6,19 mi para 5,56 mi. Os números da thread que levantou a pergunta se reproduzem.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/PREREG_THREAD_CONCENTRACAO.md`, `fase3/thread_concentracao.py`, `fase3/resultados/thread_concentracao.json`
- **Cobertura:** 2º turno, 2022 e 2026.
- **Validação:** T50 (emenda 9).
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados; alegação pública (a origem da pergunta não é fonte)
- **O que demonstra:** As contagens.
- **O que não demonstra:** Fraude ou ausência dela (descritivo).
- **Impacto em votos:** Descritivo; não se traduz em votos suspeitos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q33. Lula cresceu mais que Flávio em 93% dos municípios e em todos os estados. Isso é estatisticamente impossível?
- **Resposta direta:** Não: em 2022 Bolsonaro cresceu mais que Lula em 87,1% dos municípios e no agregado das 27 UFs; em proporção, 2022 foi até mais uniforme (98,0% dos municípios contra 97,1%). Crescimento quase universal do candidato que avança é o padrão do 2º turno. Em 2026 o candidato de trás precisava de 1,02 ponto e cresceu 2,80; em 2022 precisava de 2,85 e cresceu 1,95.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/PREREG_CRESCIMENTO_ENTRE_TURNOS.md`, `fase3/crescimento_turnos.py`, `fase3/resultados/crescimento_turnos.json`
- **Cobertura:** 2022 e 2026.
- **Validação:** T51 (emenda 10); Q21, Q22.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados; alegação pública (a origem da pergunta não é fonte)
- **O que demonstra:** Que a uniformidade se repete em 2022.
- **O que não demonstra:** Anos anteriores a 2022 (sem dados no projeto).
- **Impacto em votos:** Descritivo; não se traduz em votos suspeitos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q34. Os boletins ficaram parados duas horas antes de chegar ao TSE no 2º turno de 2026?
- **Resposta direta:** Sim: o recebimento parou às 17:07 e voltou às 19:03 (116 minutos), só em 2026; voltou junto com o fechamento das urnas prorrogadas (99% fecharam até 19:10). Isso não muda votos: o boletim é assinado pela urna na emissão (mediana 17:03) e confere com a tabela e o RDV. A causa administrativa da pausa não está nos dados.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/PREREG_POSTS_ARVOR.md`, `fase3/posts_arvor.py`, `fase3/resultados/posts_arvor.json`
- **Cobertura:** 2º turno, Brasil.
- **Validação:** T52 (emenda 11); T09, T16, Q1.
- **Independência:** Mista: relógio do TSE (interno) e boletins de terceiros (externa parcial, relógio do app não auditado)
- **O que demonstra:** O vazio e a coincidência com o fim da prorrogação.
- **O que não demonstra:** Quem decidiu a pausa e por quê.
- **Impacto em votos:** 34.327 votos depois das 17h (0,8% da margem); a pausa não altera votos.
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

### Q35. Há fortes evidências de votos sem biometria em 2026?
- **Resposta direta:** Não no agregado: a liberação pelo código do mesário caiu de 8,1% (2022) para 6,8% (2026), e dentro do município, onde ela foi maior, Lula virou um pouco menos (correlação −0,058; em 2022, +0,056). Com o perfil do eleitorado o efeito é nulo (T12). Há 8 urnas com rajada sem biometria no fim do dia (99 votos), padrão também presente em 2022 (T28/P10).
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/PREREG_POSTS_ARVOR.md`, `fase3/posts_arvor.py`, `fase3/resultados/posts_arvor.json`, `fase2/resultados/P10.json`
- **Cobertura:** 2º turno, 2022 e 2026.
- **Validação:** T53 (emenda 11); T12, T28, P10.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados; alegação pública (a origem da pergunta não é fonte)
- **O que demonstra:** Que a liberação sem biometria não favorece Lula no agregado.
- **O que não demonstra:** Quem foi cada eleitor liberado (só ata e caderno).
- **Impacto em votos:** Sem votos suspeitos no agregado; rajadas do T28: 99 votos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q36. Flávio teve menos votos no 2º turno do que no 1º em 938 municípios. Isso é anormal?
- **Resposta direta:** Não: em 2022 aconteceu o espelho, de tamanho parecido; Lula perdeu votos em 981 municípios (114.916 votos) enquanto Bolsonaro ganhava 236.690 neles. O candidato que perde fôlego no 2º turno perde votos em cerca de mil municípios.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/PREREG_POSTS_ARVOR.md`, `fase3/posts_arvor.py`, `fase3/resultados/posts_arvor.json`
- **Cobertura:** 2022 e 2026.
- **Validação:** T54 (emenda 11); Q22, Q24.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados; alegação pública (a origem da pergunta não é fonte)
- **O que demonstra:** Que o padrão se repete em 2022.
- **O que não demonstra:** Quem trocou de voto (Q26).
- **Impacto em votos:** 133.852 votos perdidos por Flávio (3% da margem), contra 114.916 de Lula em 2022.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q37. E o grupo atípico do algoritmo de mistura gaussiana, a totalização paralela e as pesquisas?
- **Resposta direta:** O grupo atípico (10.850 seções) não foi reproduzido aqui, mas o próprio dossiê que o criou mede que a fatia de Flávio nele não mudou (−0,05 ponto, IC −0,19 a +0,07) e que ele não se liga a região nem a modelo; nossos testes de locais atípicos (E02/I3) acham ~0,1% de locais sem causa demonstrada. A totalização paralela tem 286 boletins iguais ao TSE, como os nossos 0 de diferença; a amostra é de voluntários e o placar dela não estima nada. Pesquisas ficam fora do escopo (não são dado oficial).
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/PREREG_POSTS_ARVOR.md`, `fase2/resultados/P17.json`, `fase3/resultados/rev_i3.json`
- **Cobertura:** 2º turno de 2026.
- **Validação:** Respondida com testes existentes (E02, I3, Q1, T39).
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados; alegação pública (a origem da pergunta não é fonte)
- **O que demonstra:** Que nenhuma das três alegações aponta divergência nos dados.
- **O que não demonstra:** O modelo de mistura do autor (não rodado aqui).
- **Impacto em votos:** Não se traduz em votos.
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

### Q38. Cabo Frio, onde Lula ganhou 50 votos para cada 1 de Flávio no 2º turno, é estatisticamente impossível?
- **Resposta direta:** Não. Os números estão certos (Lula +9.169, Flávio +342), mas cabem exatamente nos votos que estavam disponíveis: 8.822 dos candidatos eliminados no 1º turno mais 1.229 de brancos e nulos a menos, menos 540 de comparecimento (9.511). Lula ficou com 96% disso; 11% dos municípios do país tiveram fração igual ou maior. Em 2022 houve 28 municípios fortemente de Lula em que Bolsonaro levou mais de 90% do ganho.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/PREREG_CABO_FRIO.md`, `fase3/cabo_frio.py`, `fase3/resultados/cabo_frio.json`
- **Cobertura:** Municípios, 2022 e 2026.
- **Validação:** T55 (emenda 12); Q22, Q26.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados; alegação pública (a origem da pergunta não é fonte)
- **O que demonstra:** Que o resultado é aritmeticamente possível e não é único.
- **O que não demonstra:** Quem eram os eleitores dos eliminados (Q26).
- **Impacto em votos:** Cabo Frio: 9.169 votos ganhos por Lula (0,2% da margem), todos cobertos pelos 9.511 disponíveis.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q39. Os brancos e nulos do 1º turno foram quase todos para Lula em 2026? Isso é uma anomalia?
- **Resposta direta:** Não é anomalia, e a maior parte tem causa medida. O estimador de fluxos aponta essa direção (cerca de 62% para Lula), mas a leitura do número digitado em cada nulo (Q40) mostra o mecanismo: no 1º turno de 2026, onde Lula é forte, sobrou nulo de presidente porque muita gente digitou o número do governador no campo de presidente (erro de campo); no 2º turno, sem governador na maioria dos estados, essas pessoas votaram normalmente. E em 2022 metade do eleitorado tinha 2º turno de governador, que gera esse mesmo erro, contra 8% em 2026. Sobra uma queda pequena e uniforme (~0,6 ponto). A magnitude dos fluxos estimados deve ser lida só como direção (Q41).
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/resultados/brancos_nulos.json`, `fase3/resultados/nulos_governador.json`, `fase3/resultados/rdv_nulos_analise.json`
- **Cobertura:** Brasil, 2022 e 2026.
- **Validação:** T56, T57, T58 (emendas 13 a 15); C06, Q22, Q26.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados; alegação pública (a origem da pergunta não é fonte)
- **O que demonstra:** O mecanismo (erro de campo) e a composição de UFs com governador.
- **O que não demonstra:** Em quem a pessoa queria votar.
- **Impacto em votos:** Queda de brancos e nulos de 1,82 mi entre os turnos de 2026, explicada em grande parte por erro de campo (número de governador no campo de presidente) e por haver menos 2º turno de governador; resto uniforme.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q40. O que os eleitores digitaram nos votos nulos para presidente?
- **Resposta direta:** Mais da metade digitou '00'. Uma parte grande digitou o número de um candidato a governador do próprio estado: 698 mil no 1º turno de 2026 (422 mil em 2022). No 2º turno, onde havia governador, cerca de 1 em cada 100 eleitores fez isso, o que explica todo o excesso de nulos desses estados. No 2º turno de 2026, 246 mil digitaram o número de um candidato a presidente já eliminado, 143 mil deles o 14 do Renan.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/PREREG_RDV_NULOS.md`, `fase3/rdv_nulos.py`, `fase3/rdv_nulos_analise.py`, `fase3/resultados/rdv_nulos_analise.json`
- **Cobertura:** Todas as seções, 2022 e 2026.
- **Validação:** T58 (emenda 15).
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados; alegação pública (a origem da pergunta não é fonte)
- **O que demonstra:** Os números digitados, voto a voto, conferidos com a contagem dos boletins.
- **O que não demonstra:** A intenção do eleitor.
- **Impacto em votos:** 698 mil nulos com número de governador no 1º turno de 2026; 143 mil digitando 14 no 2º turno.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q41. O estimador de fluxos de votos (para onde foi cada eleitor) acerta quando a origem é conhecida?
- **Resposta direta:** Em parte. Quem digitou 14 no 2º turno de 2026 quase certamente votou no Renan no 1º; o estimador atribui 90% desses votos ao Renan, e 69% dos que digitaram 70 ao Cury. Mas erra outros casos (55 em 2026; 12 e 15 em 2022). Pela regra fixada antes, os números de fluxo (por exemplo, '62% dos brancos e nulos para Lula') valem só como direção, não como tamanho.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/PREREG_RDV_NULOS.md`, `fase3/resultados/rdv_nulos_analise.json`, `analise/resultado_comportamento_2026.json`
- **Cobertura:** 2º turno, 2022 e 2026.
- **Validação:** T59 (emenda 15); C06, T37, Q24.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados; alegação pública (a origem da pergunta não é fonte)
- **O que demonstra:** O desempenho do estimador com dado real.
- **O que não demonstra:** Qual fluxo ocorreu (Q26).
- **Impacto em votos:** Não se traduz em votos; muda a leitura das magnitudes de fluxo.
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

### Capítulo: Operação Veracidade: os dados são fiéis ao que aconteceu?

### Q42. A conta dos "votos extras" (98,12%) mostra que o crescimento de Lula entre os turnos não fecha?
- **Resposta direta:** Não. A aritmética do vídeo está certa, mas o 98% é a premissa de 60% devolvida: é o mínimo possível para a parcela dos outros que vai a Lula e deixa Flávio sem nenhum voto dos extras. Com 85% dos outros indo a Lula, os extras se dividem 51/49. O mesmo método dá 370% para Bolsonaro em 2022. O que é real: o candidato que mais cresceu recebeu mais que a divisão proporcional nos dois anos, em todas as UFs, e em 2026 mais (26,2% do disponível contra 19,6%). (no relatório da operação: N9)
- **Estado:** Refutado no escopo definido
- **Evidência:** `operacao_veracidade/scripts/hipotese_video.py`, `operacao_veracidade/scripts/hipotese_video_m6.py`, `operacao_veracidade/resultados/hipotese_video.json`, `operacao_veracidade/resultados/hipotese_video_m6.json`, `operacao_veracidade/10_HIPOTESE_DO_VIDEO.md`
- **Cobertura:** totais nacionais com exterior (identidade exata) e 5.570 municípios sem exterior, 2022 e 2026
- **Validação:** Aritmética exata sobre totais do TSE; ecológica (associação, frágil: T37 e T59)
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Que o 98,12% decorre da premissa; que os extras não precisam ter ido todos a Lula; que o método não discrimina (2022: 370%); que a abstenção também caiu em 2022.
- **O que não demonstra:** Para onde foi cada eleitor (Q26); causa do resíduo de 3,68 mi acima do proporcional; a afirmação 'nunca aconteceu' para anos anteriores a 2022 (sem dados no projeto).
- **Impacto em votos:** Resíduo acima do proporcional: +3,68 mi para Lula em 2026 (26,2% do disponível) e +1,99 mi para Bolsonaro em 2022 (19,6%); não é limite de fraude nem evidência dela.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q43. Os certificados de todas as urnas de 2022 e 2026 verificam até a AC emissora, estavam válidos no dia da eleição e são únicos?
- **Resposta direta:** Sim: nos 1.942.246 pares seção × turno (2022 e 2026, dois turnos) a assinatura da AC emissora verifica, 0 falhas, todos válidos no dia, nenhum emitido depois da eleição, nenhuma chave pública repetida. A raiz não é pública. (no relatório da operação: N1)
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `operacao_veracidade/scripts/cert_extrai.py`, `operacao_veracidade/resultados/cert_analise.json`, `operacao_veracidade/resultados/certs_2026_1t.parquet`, `operacao_veracidade/resultados/certs_2022_2t.parquet`
- **Cobertura:** 499.176 + 499.178 seções (2026) e 471.908 + 471.984 (2022), 0 erros de leitura; exterior e Sistema de Apuração sem vota.vsc ficam fora
- **Validação:** Interna (certificados e lista vêm da mesma urna) com ACs obtidas de terceiro; **externa quanto à AC só por cópia de terceiro**
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Que toda chave de urna pertence à cadeia das ACs que temos e que nenhuma chave se repete entre urnas. Fecha a lacuna dos 200 casos do P11.
- **O que não demonstra:** Que a raiz é do TSE (AC RAIZ UE e AC URNA v2 não são públicas); que a cópia das ACs é a oficial (página do TSE bloqueada a este ambiente); fidelidade do voto.
- **Impacto em votos:** Não se traduz em votos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q44. O verificador de assinaturas rejeita arquivos adulterados, e o que cada degrau (hash, assinatura do arquivo, assinatura da lista, cadeia) prova?
- **Resposta direta:** Sim: 0 de 40 genuínos rejeitados; 40 de 40 rejeitados em cada uma de 7 mutações, em 2026 e em 2022. A assinatura do arquivo sozinha não detecta alteração do arquivo; o hash detecta. Um certificado sintético autoassinado passa pela verificação de lista e só a cadeia o rejeita. (no relatório da operação: N2)
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `operacao_veracidade/scripts/controles_mutacao.py`, `operacao_veracidade/resultados/controles_mutacao_2026_AC.json`, `operacao_veracidade/resultados/controles_mutacao_2022_AL.json`, `operacao_veracidade/resultados/ed521_unitarios.json`
- **Cobertura:** 40 seções reais de AC (2026) e 40 de AL (2022); 9 testes unitários do Ed521
- **Validação:** Sintética (mutações em cópias em memória)
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Que o verificador do projeto não aceita as adulterações testadas e que nenhum resultado herdado depende de `assin_ok` isolado.
- **O que não demonstra:** Que o verificador seja correto contra todo ataque; que a chave seja de uma urna autêntica.
- **Impacto em votos:** Não se traduz em votos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q45. Os boletins impressos lidos por terceiros (QR Code) concordam com a base do TSE e têm assinatura válida?
- **Resposta direta:** Sim, nos 404 boletins do 2º turno de 2026 obtidos: assinatura da urna válida, cadeia até a AC, votos iguais à tabela e ao BU do TSE, identidade da urna igual. É amostra de conveniência (0,08% das seções). (no relatório da operação: N3)
- **Estado:** Parcialmente demonstrado
- **Evidência:** `operacao_veracidade/scripts/terceiros_qr.py`, `operacao_veracidade/resultados/terceiros_qr.json`, `operacao_veracidade/externo/arvor_totalizacao/SHA256SUMS.txt`
- **Cobertura:** 404 de 499.207 seções (0,08%), 22 UFs, 167 de SP, só 2º turno de 2026
- **Validação:** **Externa parcial**: cadeia de obtenção diferente (QR do boletim impresso), mas a assinatura é da mesma urna; coletor e publicador são o mesmo projeto
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Que o boletim impresso na seção coincide com o que o TSE publicou nas 404 seções; 77 deles já estavam no servidor de terceiros entre 18:10 e 18:47, 45 minutos ou mais antes do TSE registrar o recebimento.
- **O que não demonstra:** Veracidade do voto; representatividade; qualquer coisa fora da amostra; o relógio do servidor de terceiros não é auditado.
- **Impacto em votos:** Não se traduz em votos: 404 seções sem diferença.
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

### Q46. Que alterações cada verificação de consistência consegue ver, e um registro coerente gerado por fonte comprometida seria distinguível de um genuíno?
- **Resposta direta:** Alterar só a tabela é visto pela comparação com o BU; BU e tabela, pelo RDV, pela imagem e pelo hash; tudo sem reassinar, só pelo hash da lista assinada; registros coerentes assinados pelo próprio gerador **não são vistos por nenhuma verificação interna**. (no relatório da operação: N4)
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `operacao_veracidade/scripts/identificabilidade.py`, `operacao_veracidade/resultados/identificabilidade.json`
- **Cobertura:** 52.062 seções reais de MG, 2º turno de 2026, 2.497 alteradas (59.499 votos); 6 cenários e 6 verificações
- **Validação:** Sintética
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** O que cada consistência interna pode e não pode ver.
- **O que não demonstra:** Que alguém consiga produzir registros coerentes assinados na prática; só mede o limite.
- **Impacto em votos:** Não se traduz em votos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q47. Que mecanismos de alteração a bateria estatística consegue ver, com que poder, e quais passam sem alarme?
- **Resposta direta:** Vê com 80% de poder a partir de 25 a 50 mil votos: seções dispersas, poucas seções, locais, zonas e municípios inteiros, redutos. Só vê a partir de 0,5 a 2,2 milhões, ou nunca: UFs, os cinco grandes juntos, macrorregião, lote tardio, conversão de brancos e nulos, deslocamento uniforme. O poder é assimétrico entre sentidos. Um atacante de estrutura completa passa D1 a D7 em 2026. (no relatório da operação: N5)
- **Estado:** Parcialmente demonstrado
- **Evidência:** `operacao_veracidade/scripts/sim_adversarial.py`, `operacao_veracidade/scripts/sim_fabricacao_v2.py`, `operacao_veracidade/resultados/sim_2026_resumo.json`, `operacao_veracidade/resultados/sim_2022_resumo.json`, `operacao_veracidade/03_SIMULACOES_ADVERSARIAIS.md`
- **Cobertura:** 2026 e 2022; 15 mecanismos, 2 sentidos, 7 magnitudes, 20 réplicas; limiares do bootstrap por município
- **Validação:** Sintética (base real é referência, não verdade conhecida)
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Quais mecanismos a bateria vê e em que escala; que a ausência de alarme em mecanismos de UF, região, lote e uniforme não exclui alterações de centenas de milhares de votos.
- **O que não demonstra:** Que a base real foi ou não alterada (alteração já presente é absorvida pelo limiar); que a soma das anomalias seja teto de fraude.
- **Impacto em votos:** Poder ≥ 80% só a partir de 25 mil (locais, zonas) a 2,22 mi votos movidos (UFs, uniforme); ver tabela em 03.
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

### Q48. Os zeros de votos de um finalista são excepcionais depois de modelos calibrados (2022 e 2026)?
- **Resposta direta:** Não determinável: três famílias de modelo (município, zona, local de votação) falharam o critério fixado antes; os zeros são, na descrição, locais de uma seção só com menos de 1% do total, nos dois anos (141 em 2022 e 106 em 2026 para o candidato da direita; 2 e 4 para Lula). (no relatório da operação: N6)
- **Estado:** Não determinado com as evidências disponíveis
- **Evidência:** `operacao_veracidade/scripts/zeros_contagens.py`, `operacao_veracidade/scripts/zeros_locais.py`, `operacao_veracidade/resultados/zeros_contagens.json`, `operacao_veracidade/05_ZEROS_E_ENTRE_TURNOS.md`
- **Cobertura:** todas as seções com comparecimento positivo, 2022 e 2026, dois turnos, dois finalistas
- **Validação:** Interna (tabela do TSE)
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** As contagens (0, 1, 2, 3 a 5 votos) e o perfil descritivo dos zeros.
- **O que não demonstra:** Excesso ou ausência de excesso de zeros; o modelo por local reproduz 45% a 63% e falha.
- **Impacto em votos:** 14.860 votos de Lula nas 106 seções de 2026 (0,34% da margem); 16.418 em 2022.
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

### Q49. Os arquivos que o TSE publicou mudaram entre downloads independentes?
- **Resposta direta:** Não, nos 404 boletins: o SHA-256 do `bu.dat` baixado por terceiros do TSE (a partir de 25/10) é igual ao do nosso download (27 e 28/10) em 404 de 404. (no relatório da operação: N7)
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `operacao_veracidade/scripts/republicacao_bu.py`, `operacao_veracidade/resultados/republicacao_bu.json`
- **Cobertura:** 404 BU de 22 UFs
- **Validação:** Externa parcial: hash declarado por terceiro, confirmado por igualdade com o nosso
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Nenhuma republicação nesses arquivos entre os dois downloads.
- **O que não demonstra:** Que o arquivo seja o que a urna gerou; arquivos fora dos 404; mudanças antes do primeiro download.
- **Impacto em votos:** Não se traduz em votos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### Q50. Há divergência objetiva nova nos dados publicados pelo TSE?
- **Resposta direta:** Nenhuma divergência de votos. Há lacunas documentais: 98 certificados emitidos depois da validade do certificado público da AC URNA; certificado ≠ urna da tabela em 17 seções de 2026 e 22 de 2022 (1 com três identificações diferentes); regra de emissão por modelo não pública; raiz ausente. (no relatório da operação: N8)
- **Estado:** Parcialmente demonstrado
- **Evidência:** `operacao_veracidade/resultados/casos_certificado.csv`, `operacao_veracidade/resultados/casos_A_relidos_por_id_e_data.csv`, `operacao_veracidade/evidencia/caso_ES_57932_9_85_112.json`, `operacao_veracidade/06_ANOMALIAS_E_LOGS.md`
- **Cobertura:** 2026 e 2022, dois turnos, todas as seções com certificado
- **Validação:** Interna (certificado da AC, tabela e log têm origens parcialmente distintas)
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** As lacunas e o artefato do leitor (log de pacote traz logs arquivados de outras urnas e seções).
- **O que não demonstra:** Causa de cada caso; os explicados vêm do próprio log (compatível, não verificado).
- **Impacto em votos:** Menos de 30 mil votos válidos nas seções dos tipos A e D (cerca de 0,6% da margem de 2026).
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

## Parte B. Itens do inventário (33)

### P1. P1 (respondida na F2)
- **Resposta direta:** O estimador de fluxos C06 recupera a verdade? Em parte: a ordem dos fluxos e o contraste com 2022 resistem; a magnitude '4:1' não (erro de ±0,5 a ±1,5 mi votos).
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase2/sessao_limitada_2026-10-28/p1_c06_adversarial.py`, `fase2/sessao_limitada_2026-10-28/p1_resultado_principal.json`, `fase2/sessao_limitada_2026-10-28/p1_resultado_sensibilidade.json`
- **Cobertura:** ver as perguntas relacionadas: Q24
- **Validação:** Com taxas homogêneas por UF o C06 recupera a verdade (razão Abs→Lula:Abs→Adv de 2026: 4,12 contra 4,01). Com heterogeneidade contextual a razão estimada vai de 1,7 a 11,8 contra 3 a 4 verdadeiro. A ordem de 2026 e o contraste com 2022 (razão 0,56) resistem; a magnitude '4:1' não. Em votos: ±0,5 mi (estresse moderado) a ±1,5 mi (forte) na célula Abs→Lula, contra 3,18 mi estimados.
- **Independência:** Sintética (simulação; nenhum voto real alterado)
- **O que demonstra:** Em parte: a ordem dos fluxos e o contraste com 2022 resistem; a magnitude '4:1' não (erro de ±0,5 a ±1,5 mi votos).
- **O que não demonstra:** —
- **Impacto em votos:** Erro de ±0,5 a ±1,5 mi votos na razão estimada.
- **Próxima evidência decisiva:** idem Q24

### P2. P2 (respondida na F2)
- **Resposta direta:** A bateria detecta trocas de votos? Só nos cenários e tamanhos da Q7.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase2/f2_completa.py`, `fase2/resultados/P2_principal.json`, `fase2/resultados/P2_sensibilidade.json`, `fase3/resultados/p18.json`, `fase3/resultados/rev_i1_2026.json`, `fase3/resultados/rev_a2_2026.json`
- **Cobertura:** ver as perguntas relacionadas: Q7
- **Validação:** Revisado pelo P18, pelo I1 e pelo A2: no sentido correto, a bateria não detecta troca de até ~25 mil votos (2% em 1% das seções) em nenhuma forma testada, nem troca dispersa de ~62 mil votos, nem troca no município inteiro das 5 maiores cidades com confiabilidade (até ~700 mil votos em São Paulo a 10%); detecta ~123 mil dispersos e ~62 mil concentrados em locais ou municípios de até ~5 mil seções.
- **Independência:** Sintética (simulação; nenhum voto real alterado)
- **O que demonstra:** Só nos cenários e tamanhos da Q7.
- **O que não demonstra:** Ver P18.
- **Impacto em votos:** Detectado nos cenários simulados: ~123 mil votos dispersos (2,8% da margem de 2026) e ~62 mil concentrados (1,4%). Não detectado: ~25 mil (0,6%). No município inteiro de uma grande cidade, a bateria original falha até ~696 mil votos, mas o teste T44 vê a partir de 31 mil a 139 mil (2% dos válidos). No T63, UFs, região, lote e deslocamento uniforme passam sem alarme até ~0,5 a 2,2 mi votos, ou sempre (uniforme em logit). Inverter 2026 exigiria trocar ~2,22 mi votos de lado.
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

### P3. As inconsistências aparentes dependem do canal e da versão de publicação?
- **Resposta direta:** As inconsistências dependem de canal e versão? Nos canais comparados (tabela, BU, decodificação de terceiro, divulgação ao vivo) não há inconsistência de votos; versões datadas dos arquivos não existem localmente.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/f3_reconcilia.py`, `fase3/resultados/R1_20_dataurnas.json`, `fase3/resultados/E3_zeros.json`, `fase2/resultados/P16.json`
- **Cobertura:** ver as perguntas relacionadas: Q1, Q4, Q6, Q14
- **Validação:** Canais comparados: tabela × bu.dat × RDV × imagem (R1: 0 diferenças de votos nos dois anos), decodificação de terceiro (T43), divulgação ao vivo × base final (R2: consistente em 39 instantes). Versões datadas dos arquivos: só uma cópia local. Concordância entre arquivos da mesma urna é consistência interna.
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Nos canais comparados (tabela, BU, decodificação de terceiro, divulgação ao vivo) não há inconsistência de votos; versões datadas dos arquivos não existem localmente.
- **O que não demonstra:** Versões datadas dos arquivos.
- **Impacto em votos:** 0 voto de diferença entre os canais comparados.
- **Próxima evidência decisiva:** Versões datadas dos arquivos (não existem localmente)

### P4. A curva pública pode ser reconstruída pelos BUs recebidos, dentro da latência esperada?
- **Resposta direta:** A curva pública pode ser reconstruída pelos boletins recebidos? Sim, nos 39 instantes capturados: a recomposição pela ordem de recebimento reproduz o total divulgado (≤ 0,083 pp), sem defasagem.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/inv_r2_curva_publica.py`, `fase3/resultados/r2_curva_publica.json`, `fase3/externos/wayback_capturas/`
- **Cobertura:** ver as perguntas relacionadas: Q9, Q11, Q14
- **Validação:** R2: 39 capturas do Internet Archive dos totais nacionais divulgados durante a apuração (2022: 2 e 27; 2026: 6 e 4). A recomposição pela base final, na ordem de recebimento, reproduz cada captura com diferença máxima de 0,083 ponto percentual, mesmo líder, sem defasagem; votos nunca diminuem; a última captura é igual ao total oficial. A curva pública pode ser reconstruída a partir dos boletins recebidos nos instantes capturados.
- **Independência:** Externa parcial (terceiro preservou ou leu conteúdo do TSE; não é a urna)
- **O que demonstra:** Sim, nos 39 instantes capturados: a recomposição pela ordem de recebimento reproduz o total divulgado (≤ 0,083 pp), sem defasagem.
- **O que não demonstra:** Capturas por UF e mais instantes (o Internet Archive limitou o acesso durante a coleta).
- **Impacto em votos:** Nas 404 seções com boletim de terceiro, 0 voto de diferença. Na captura final de cada eleição, 0 voto de diferença entre o total divulgado ao vivo e a base. A maior diferença em capturas parciais equivale a ~1,7 mil a ~3 mil votos naquele instante (seções com o mesmo horário de recebimento ordenadas de forma diferente), e não muda o líder.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### P5. P5 (respondida na F2)
- **Resposta direta:** O modelo de urna afeta a virada? Não, dentro de ±0,02 logit (2º turno, municípios com 2 ou mais modelos).
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase2/resultados/P5.json`
- **Cobertura:** ver as perguntas relacionadas: —
- **Validação:** Dentro dos 1.436 municípios (2026) e 1.779 (2022) com mais de um modelo de urna, a diferença entre modelos é equivalente a zero em ±0,02 logit; o maior efeito é +0,004 logit (UE2013, 2026), cerca de 2,7 mil votos se fosse real. A associação do T20 é efeito do território, não do modelo.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** Não, dentro de ±0,02 logit (2º turno, municípios com 2 ou mais modelos).
- **O que não demonstra:** —
- **Impacto em votos:** Maior efeito +0,004 logit, ~2,7 mil votos se fosse real.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### P6. O que boletins coletados por terceiros permitiriam validar?
- **Resposta direta:** Boletins de terceiros validam os arquivos? Em parte: 404 boletins impressos lidos por terceiros no 2º turno de 2026 (22 UFs) são iguais à tabela e ao BU do TSE, com assinatura e cadeia válidas (T61); é amostra de conveniência, não sorteada; de 2022 não há.
- **Estado:** Parcialmente demonstrado (404 boletins, amostra de conveniência)
- **Evidência:** `operacao_veracidade/resultados/terceiros_qr.json`, `operacao_veracidade/resultados/republicacao_bu.json`, `RELATORIO_F3.md (E7: busca de boletins de terceiros, só imprensa)`
- **Cobertura:** ver as perguntas relacionadas: Q6, Q45
- **Validação:** T61: 404 boletins impressos lidos por terceiros (QR Code) no 2º turno de 2026, em 22 UFs: assinatura da urna válida, cadeia até a AC, votos iguais à tabela e ao BU do TSE e mesma urna em 404 de 404. Amostra de conveniência (0,08% das seções), não sorteada; de 2022 não há boletins de terceiros neste estudo.
- **Independência:** Externa (boletins de terceiros): obtida só em T61, N3
- **O que demonstra:** Em parte: 404 boletins impressos lidos por terceiros no 2º turno de 2026 (22 UFs) são iguais à tabela e ao BU do TSE, com assinatura e cadeia válidas (T61); é amostra de conveniência, não sorteada; de 2022 não há.
- **O que não demonstra:** Boletins impressos de uma amostra sorteada de seções.
- **Impacto em votos:** 0 voto de diferença nas 404 seções com boletim impresso de terceiro (amostra de conveniência, 0,08%).
- **Próxima evidência decisiva:** idem Q6

### P7. P7 (respondida na F2)
- **Resposta direta:** A urna trocada vota diferente? Não, equivalente na margem de ±0,10 z fixada antes.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase2/resultados/P7.json`
- **Cobertura:** ver as perguntas relacionadas: —
- **Validação:** Equivalência declarada na margem de ±0,10 z fixada antes: 2026 −0,029 (IC 90% −0,054 a −0,003, 4.432 urnas); 2022 −0,008 (−0,023 a +0,008, 12.653 urnas).
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** Não, equivalente na margem de ±0,10 z fixada antes.
- **O que não demonstra:** —
- **Impacto em votos:** Diferença de −0,029 z, desprezível; não convertida em votos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### P8. P8 (respondida na F2)
- **Resposta direta:** A virada depende da ordem de chegada? Efeito desprezível (|r| ≤ 0,05); em 2022, −0,028, diferente de zero.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase2/resultados/P8.json`
- **Cobertura:** ver as perguntas relacionadas: —
- **Validação:** Com bootstrap por município, 2026 tem r = +0,004 (IC 95% −0,004 a +0,012) e 2022 r = −0,028 (−0,040 a −0,019): efeitos desprezíveis (|r| ≤ 0,05), de sinais opostos.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** Efeito desprezível (|r| ≤ 0,05); em 2022, −0,028, diferente de zero.
- **O que não demonstra:** —
- **Impacto em votos:** Efeito desprezível.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### P9. Os locais de votação do E02 permanecem significativos com p-valores calibrados e com dependência espacial?
- **Resposta direta:** Os locais atípicos do E02 resistem? Cerca de 0,1% dos locais, em três métodos; a lista depende do método; causa não demonstrada.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase2/resultados/P9.json`, `fase3/resultados/p19.json`, `fase3/rev_i3_espacial.py`, `fase3/resultados/rev_i3.json`
- **Cobertura:** ver as perguntas relacionadas: Q25
- **Validação:** I3 (rev_i3_espacial.py): com o entorno como referência (zona sem o local, nulo empírico por faixa de tamanho, BH), 61 locais de 59.885 seguem significativos em 2026 (36 pró-Lula, 25 pró-adversário) e 84 de 56.164 em 2022 (46 e 38); com o município como referência, 63 e 80. A correção só por ρ do P9 dava 55 (28 e 27) e 102 (30 e 72). Só 28 (2026) e 41 (2022) locais são significativos nos dois métodos: a lista depende do método; a ordem de grandeza (cerca de 0,1% dos locais) e o equilíbrio de sentidos em 2026 não. O sentido de 2022 muda (72 pró-adversário com ρ; 38 com o entorno).
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** Cerca de 0,1% dos locais, em três métodos; a lista depende do método; causa não demonstrada.
- **O que não demonstra:** Nulo geográfico no nível do local (sem coordenadas de locais no material); causa dos locais significativos.
- **Impacto em votos:** Cada local atípico: dezenas a poucas centenas de votos.
- **Próxima evidência decisiva:** idem Q25

### P10. P10 (respondida na F2)
- **Resposta direta:** A rajada sem biometria do T28 resiste? 8 urnas do 1º turno de 2026 seguem sinalizadas pelo critério beta-binomial (99 votos); em 2022 o mesmo critério sinaliza 18 e 21 urnas (23 e 25 pelo T28 original).
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase2/resultados/P10.json`, `analise/resultado_logs_2022_1t.json`, `analise/resultado_logs_2022_2t.json`, `fase3/resultados/a4_t28.json`
- **Cobertura:** ver as perguntas relacionadas: —
- **Validação:** 8 de 13 urnas do 1º turno de 2026 seguem sinalizadas (99 votos); 2022 sinaliza 18 e 21. A4: a regra do T28 de 2022 reproduz exatamente 23 e 25 urnas sinalizadas; nenhuma é do Sistema de Apuração. Denominador efetivo do T28 em 2022: 471.851 e 471.979 urnas com votos nos últimos 30 min; o total declarado 'urnas' (472.024 e 472.027) inclui 109 e 39 seções do Sistema de Apuração sem sequência de log (148).
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** 8 urnas do 1º turno de 2026 seguem sinalizadas pelo critério beta-binomial (99 votos); em 2022 o mesmo critério sinaliza 18 e 21 urnas (23 e 25 pelo T28 original).
- **O que não demonstra:** —
- **Impacto em votos:** 99 votos nos últimos 30 min das 8 urnas (2026, 1º turno).
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### P11. Os certificados das urnas se ligam a uma âncora do TSE?
- **Resposta direta:** Os certificados se ligam a uma âncora do TSE? Não foi possível determinar: válidos até a AC emissora em 100% das urnas (T60a); raiz não obtida.
- **Estado:** Não determinado com as evidências disponíveis
- **Evidência:** `operacao_veracidade/resultados/cert_analise.json`, `fase2/resultados/P11.json`, `fase2/externos/certificados/`
- **Cobertura:** ver as perguntas relacionadas: Q5, Q43
- **Validação:** T60a: a cadeia urna → AC emissora verifica em 1.942.246 de 1.942.246 pares seção × turno (2022 e 2026), 0 falhas, todos válidos no dia, nenhuma chave repetida. O elo AC → raiz do TSE continua sem verificação: AC URNA v2 e AC RAIZ UE não são públicas (página oficial com HTTP 403).
- **Independência:** Interna + cadeia até a AC emissora (T60a, N1); raiz não pública
- **O que demonstra:** Não foi possível determinar: válidos até a AC emissora em 100% das urnas (T60a); raiz não obtida.
- **O que não demonstra:** Certificados da AC URNA v2 e da AC RAIZ UE por canal do TSE.
- **Impacto em votos:** Alcança todos os votos: nenhum voto, de 2022 ou 2026, tem a assinatura verificada até a raiz do TSE; todos estão verificados até a AC emissora (100% das urnas, verificação completa em 28/10/2026, T60a).
- **Próxima evidência decisiva:** idem Q5

### P12. P12 (respondida na F2)
- **Resposta direta:** Diferença do eleitorado do exterior? Explicada: 423 de seções não instaladas + 72 + 30 de seções só nos arquivos de urna.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase2/resultados/P12.json`
- **Cobertura:** ver as perguntas relacionadas: —
- **Validação:** Explicada: −495 = 423 (41 seções não instaladas) + 72 (uma seção com boletim só nos arquivos das urnas); −525 = 423 + 72 + 30 (outra seção, no 2º turno). Resíduo zero. São eleitores aptos, não votos.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** Explicada: 423 de seções não instaladas + 72 + 30 de seções só nos arquivos de urna.
- **O que não demonstra:** —
- **Impacto em votos:** Eleitores aptos do exterior (−495 e −525), não votos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### P13. P13 (respondida na F2)
- **Resposta direta:** O C06b é reproduzível? Sim: 79 e 123 reproduzidos.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase2/resultados/P13.json`
- **Cobertura:** ver as perguntas relacionadas: Q24
- **Validação:** Script reproduzível reproduz exatamente 79 (Flávio→Lula) e 123 (Lula→Flávio) como mínimos garantidos, com os aptos do 2º turno, sem exterior; máximos 43,5 mi e 39,4 mi.
- **Independência:** Aritmética exata sobre totais do TSE
- **O que demonstra:** Sim: 79 e 123 reproduzidos.
- **O que não demonstra:** —
- **Impacto em votos:** Trocas diretas entre finalistas em 2026: mínimo garantido de 79 e 123 votos, máximo de 43,5 mi e 39,4 mi; abstencionistas para Lula entre 4.116 e 32,3 mi. A razão do C06 erra de ±0,5 a ±1,5 mi votos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### P14. P14 (respondida na F2)
- **Resposta direta:** Qual a causa da assimetria do T02 em 2022? Não demonstrada; o desvio está no nível da zona (251, 259) e persiste na 251 depois do perfil do eleitorado.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase2/resultados/P14.json`, `fase3/resultados/p20.json`, `fase3/resultados/rev_i3.json`, `fase3/inv_r4_zona251.py`, `fase3/resultados/r4_zona251.json`
- **Cobertura:** ver as perguntas relacionadas: Q25
- **Validação:** Causa não demonstrada. R4: o desvio da zona 251 (0,58 z) persiste depois de controlar escolaridade, idade, sexo e estado civil da seção (0,42 z, IC 95% 0,23 a 0,62; 26% explicado); zona 259 explicada em parte.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** Não demonstrada; o desvio está no nível da zona (251, 259) e persiste na 251 depois do perfil do eleitorado.
- **O que não demonstra:** Covariáveis de campanha, renda, migração; dados externos.
- **Impacto em votos:** Salvador 2026: ~30 mil votos de Lula acima do previsto (0,7% da margem de 2026). Zona 251 (SP, 2022): ~4,2 mil votos de Lula acima da virada mediana da capital (0,2% da margem de 2022); zona 259: ~6,2 mil. Cauda pró-Lula do T02: ~740 votos (2026) e ~2.600 (2022). Cada local atípico: dezenas a poucas centenas de votos.
- **Próxima evidência decisiva:** idem Q25

### P15. P15 (respondida na F2)
- **Resposta direta:** Os limites de Fréchet estreitam a razão? Não: a razão não é identificada.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase2/resultados/P15.json`
- **Cobertura:** ver as perguntas relacionadas: Q24, Q26
- **Validação:** Limites de Fréchet por seção para quem se absteve em 2026: para Lula entre 4.116 e 32,3 mi; para o adversário entre 19 e 31,3 mi; a razão não é identificada (de ~0 a 1,7 mi). A estimativa do C06 cai dentro dos limites, mas só o modelo a escolhe.
- **Independência:** Aritmética exata sobre totais do TSE
- **O que demonstra:** Não: a razão não é identificada.
- **O que não demonstra:** —
- **Impacto em votos:** Abstencionistas para Lula entre 4.116 e 32,3 mi votos.
- **Próxima evidência decisiva:** idem Q24

### P16. P16 (respondida na F2)
- **Resposta direta:** 200 seções conferem? Sim, 200/200 no 1º turno de 2026 (consistência interna); o 2º turno é coberto pelo T17b e pelo R1.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase2/resultados/P16.json`
- **Cobertura:** ver as perguntas relacionadas: Q1, Q2
- **Validação:** 200 de 200 seções sorteadas do 1º turno de 2026 concordam em todos os arquivos. A amostra é só do 1º turno; o 2º turno é coberto nacionalmente pelo T17b (BU = RDV = publicado em todas as urnas eletrônicas), não por amostra com todos os arquivos.
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Sim, 200/200 no 1º turno de 2026 (consistência interna); o 2º turno é coberto pelo T17b e pelo R1.
- **O que não demonstra:** —
- **Impacto em votos:** 0 voto de diferença nas 200 seções.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### P17. P17 (respondida na F2)
- **Resposta direta:** A assimetria de cauda do T02 é real? Sim, nos dois anos.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase2/resultados/P17.json`
- **Cobertura:** ver as perguntas relacionadas: Q25
- **Validação:** A assimetria de cauda do T02 é estatisticamente real com bootstrap por município (IC 95% da razão acima de 1 em 3, 4 e 5 desvios, nos dois anos). Isto confirma que a característica existe; não explica a causa.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** Sim, nos dois anos.
- **O que não demonstra:** —
- **Impacto em votos:** ~740 votos (2026) e ~2.600 (2022) na cauda pró-Lula.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### P18. Com o T1 e o T3 de duas caudas, a regra do T13 enxerga os dois sentidos?
- **Resposta direta:** O T13 bilateral vê os dois sentidos? Sim, para troca dispersa; limites na Q7.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/f3_pendencias.py`, `fase3/resultados/p18.json`, `fase3/rev_i1_poder.py`, `fase3/resultados/rev_i1_2026.json`, `fase3/resultados/rev_i1_2022.json`, `fase3/rev_a2_poder.py`, `fase3/resultados/rev_a2_2026.json`, `fase3/resultados/rev_a2_2022.json`
- **Cobertura:** ver as perguntas relacionadas: Q7
- **Validação:** A2 (rev_a2_poder.py; mesmos mundos e cenários do I1), detecção só no sentido correto, limiar calibrado, 2026: troca dispersa de 10% dos válidos em 1% das seções (~123 mil votos) 30/30; locais ou municípios de até ~5 mil seções a 5% (~62 mil) 30/30, com E02 simples e completo; região a 5% 26/30 e 23/30 (simples) ou 27/30 e 25/30 (completo): detecção incerta; 2% (~25 mil) 0/30 em todas as formas; dispersa a 5% 0/30. Falso alarme no sentido correto 0/30 (IC até 11%). Município inteiro das 5 maiores cidades (antes excluídas): a 5% (77 mil a 348 mil votos) o E02 completo detecta 0 a 1 de 30 e o simples 13 a 21 de 30; a 10% (155 mil a 696 mil votos) 10 a 13 de 30 (completo) e 24 de 30 (simples), pelo completo, 0 de 12 em Brasília e Fortaleza e 1 de 12 em São Paulo (6 réplicas por cidade e sentido; Brasília é o único município da UF, e o modelo por UF absorve a troca). A 10% concentrado, o E02 também acusa locais no sentido oposto em 10% a 80% das réplicas. 2022 (validação): padrão semelhante; região a 5% detectável no sentido para Lula (30/30) e 27/30 (simples) ou 28/30 (completo) no outro.
- **Independência:** Sintética (simulação; nenhum voto real alterado)
- **O que demonstra:** Sim, para troca dispersa; limites na Q7.
- **O que não demonstra:** Mecanismos não simulados (preservar medianas, mexer no comparecimento, anteriores ao BU) e outras coberturas não testados.
- **Impacto em votos:** Detectado nos cenários simulados: ~123 mil votos dispersos (2,8% da margem de 2026) e ~62 mil concentrados (1,4%). Não detectado: ~25 mil (0,6%). No município inteiro de uma grande cidade, a bateria original falha até ~696 mil votos, mas o teste T44 vê a partir de 31 mil a 139 mil (2% dos válidos). No T63, UFs, região, lote e deslocamento uniforme passam sem alarme até ~0,5 a 2,2 mi votos, ou sempre (uniforme em logit). Inverter 2026 exigiria trocar ~2,22 mi votos de lado.
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

### P19. Há dependência espacial entre municípios nos resíduos do E02?
- **Resposta direta:** Há dependência espacial entre municípios? Sim, Moran's I 0,16 a 0,20; causa não distinguida.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/resultados/p19.json`
- **Cobertura:** ver as perguntas relacionadas: Q25
- **Validação:** Moran's I = 0,161 (2026) e 0,179 (2022) pela vizinhança por arco; 0,172 e 0,198 por 5 vizinhos; p = 0,001 (piso de 999 permutações); sem os 5% mais extremos, 0,157 e 0,170. Variável: z médio municipal do modelo de virada por UF (divergencias_municipios_*_completo.csv). Há dependência espacial nos dois anos. O teste não distingue a causa (estrutura regional legítima ou não).
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** Sim, Moran's I 0,16 a 0,20; causa não distinguida.
- **O que não demonstra:** —
- **Impacto em votos:** Não se traduz em votos.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### P20. O que explica a concentração de seções atípicas em São Paulo capital em 2022?
- **Resposta direta:** O que há nos locais de SP 2022? Desvio no nível da zona, que persiste na 251 após o perfil; arquivos conferem; causa não demonstrada.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/resultados/p20.json`, `fase3/resultados/rev_i3.json`
- **Cobertura:** ver as perguntas relacionadas: Q25
- **Validação:** 29 seções em 15 locais; os locais não se destacam da própria zona; a zona 251 mantém desvio após o perfil do eleitorado (R4); arquivos conferem (consistência interna); causa não demonstrada.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** Desvio no nível da zona, que persiste na 251 após o perfil; arquivos conferem; causa não demonstrada.
- **O que não demonstra:** Ver P14.
- **Impacto em votos:** Salvador 2026: ~30 mil votos de Lula acima do previsto (0,7% da margem de 2026). Zona 251 (SP, 2022): ~4,2 mil votos de Lula acima da virada mediana da capital (0,2% da margem de 2022); zona 259: ~6,2 mil. Cauda pró-Lula do T02: ~740 votos (2026) e ~2.600 (2022). Cada local atípico: dezenas a poucas centenas de votos.
- **Próxima evidência decisiva:** idem Q25

### P21. Evidências externas e certificados por canal oficial confirmam os arquivos?
- **Resposta direta:** Fontes externas e cadeia autenticada confirmam os arquivos? Em parte: no agregado nacional ao vivo e em 404 boletins impressos de terceiros iguais ao TSE (Q6, T61; amostra de conveniência); a cadeia fecha até a AC emissora em 100% das urnas (T60a), mas a raiz não foi obtida.
- **Estado:** Parcialmente demonstrado (404 boletins, amostra de conveniência)
- **Evidência:** `operacao_veracidade/resultados/terceiros_qr.json`, `operacao_veracidade/resultados/cert_analise.json`, `RELATORIO_F3.md (E7)`, `fase3/RELATORIO_ACEITACAO_F3.md (consultas ao site de resultados de 2022: HTTP 404)`
- **Cobertura:** ver as perguntas relacionadas: Q5, Q6, Q45
- **Validação:** Fontes externas obtidas: capturas do Internet Archive dos totais divulgados (R2) e 404 boletins impressos de terceiros iguais ao TSE (T61, amostra de conveniência); 404 arquivos iguais entre downloads independentes. Cadeia até a AC emissora em 100% das urnas (T60a); a raiz não foi obtida.
- **Independência:** Externa parcial (terceiro preservou ou leu conteúdo do TSE; não é a urna)
- **O que demonstra:** Em parte: no agregado nacional ao vivo e em 404 boletins impressos de terceiros iguais ao TSE (Q6, T61; amostra de conveniência); a cadeia fecha até a AC emissora em 100% das urnas (T60a), mas a raiz não foi obtida.
- **O que não demonstra:** Amostra sorteada de boletins impressos; AC URNA v2 e AC RAIZ UE.
- **Impacto em votos:** Nas 404 seções com boletim de terceiro, 0 voto de diferença. Na captura final de cada eleição, 0 voto de diferença entre o total divulgado ao vivo e a base. A maior diferença em capturas parciais equivale a ~1,7 mil a ~3 mil votos naquele instante (seções com o mesmo horário de recebimento ordenadas de forma diferente), e não muda o líder.
- **Próxima evidência decisiva:** idem Q6

### R1-20. Reconciliação com o DataUrnas e outros projetos externos.
- **Resposta direta:** A base coincide com decodificação independente? Sim, nas seções comuns (99,96% em 2022, 100% em 2026 1º turno); o 2º turno de 2026 não tem comparação de terceiro.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/f3_reconcilia.py`, `fase3/resultados/R1_20_dataurnas.json`, `fase3/resultados/R1_20_dataurnas_reproducao.json`, `fase3/externos/DATAURNAS.md`, `fase3/ver_a1.py`, `fase3/resultados/a1.csv`, `fase3/resultados/a1.json`
- **Cobertura:** ver as perguntas relacionadas: Q1
- **Validação:** 0 diferenças em 499.206 seções (2026, 1º turno) e nas seções comuns de 2022, com reprodução idêntica e commit e hashes conferidos. A1 (fase3/ver_a1.py, a1.csv): as 191 (1º turno) e 176 (2º) seções do Brasil sem par em 2022 são: 17 e 10 do Sistema de Apuração (SA22); 167 e 166 em 5 zonas da Bahia (as mesmas nos dois turnos) que estão na tabela de seções do DataUrnas-BR sem nenhum voto (167 das 769 seções dessas zonas; lacuna do acervo do terceiro, motivo não identificado); 7 (1º turno) que o DataUrnas-BR registra como 'seção fora do banco'. Os 367 boletins locais foram lidos e conferem com a tabela (0 divergências). Cobertura da comparação com implementação independente em 2022: 470.819 de 471.010 seções do Brasil (1º turno) e 470.834 de 471.010 (2º), 99,96%; as demais só com o leitor do projeto. Sem cobertura independente: o 2º turno de 2026.
- **Independência:** Independente na implementação, não na origem (decodificação de terceiro sobre o dado do TSE)
- **O que demonstra:** Sim, nas seções comuns (99,96% em 2022, 100% em 2026 1º turno); o 2º turno de 2026 não tem comparação de terceiro.
- **O que não demonstra:** Decodificação independente do 2º turno de 2026.
- **Impacto em votos:** 0 voto de diferença nas seções comuns (~119 mi em 2026, 1º turno; ~118 mi por turno em 2022).
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

### C1. As curvas públicas da apuração (2022 e 2026) são compatíveis com processos plausíveis de recepção e publicação?
- **Resposta direta:** As curvas são compatíveis com processos plausíveis de chegada? Não determinado (nenhum modelo de chegada validado). A curva divulgada é reproduzível com os dados por seção.
- **Estado:** Não determinado com as evidências disponíveis
- **Evidência:** `fase3/f3_curvas.py`, `fase3/f3_curvas2.py`, `fase3/resultados/E2_curvas.json`, `fase3/resultados/E2b_curvas.json`
- **Cobertura:** ver as perguntas relacionadas: Q10, Q11, Q12
- **Validação:** Nenhum modelo de chegada validado (cinco nulos rejeitam também 2022). R2: a curva divulgada é reproduzida pelos dados por seção nos 39 instantes capturados; viradas observadas na divulgação coincidem com a reconstrução.
- **Independência:** Interna (hora de recebimento registrada pelo próprio TSE) + capturas de terceiro (externa parcial)
- **O que demonstra:** Não determinado (nenhum modelo de chegada validado). A curva divulgada é reproduzível com os dados por seção.
- **O que não demonstra:** Modelo de chegada validado contra as capturas do R2.
- **Impacto em votos:** Não se traduz em votos: trata da ordem de chegada, não do total.
- **Próxima evidência decisiva:** idem Q10

### C1a. Quando e em que contexto ocorreram as viradas de liderança durante a apuração, em 2022 e 2026?
- **Resposta direta:** Quando ocorreram as viradas? Ver Q8 e Q9.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/resultados/E2_curvas.json`
- **Cobertura:** ver as perguntas relacionadas: Q8, Q9
- **Validação:** Na reconstrução pela hora de recebimento do boletim: 2º turno de 2026, Lula lidera aos 10% apurados, perde aos 13,5% e retoma aos 47,2%; 2º turno de 2022, o adversário lidera até 67,6%. A última troca vem mais tarde do que nos nulos nos dois anos. É descrição da ordem de recebimento; não explica nem refuta nada.
- **Independência:** Interna (hora de recebimento registrada pelo próprio TSE) + capturas de terceiro (externa parcial)
- **O que demonstra:** Ver Q8 e Q9.
- **O que não demonstra:** Snapshots datados da divulgação.
- **Impacto em votos:** A ordem de apuração não muda nenhum voto: a mesma soma final em qualquer ordem. A virada do 2º turno de 2022 ocorreu com 67,6% das urnas; a de 2026, com 47,2%.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### C1b. As curvas têm periodicidade, vales ou trechos lineares anômalos?
- **Resposta direta:** Há periodicidade ou trechos lineares anômalos? Não determinado.
- **Estado:** Não determinado com as evidências disponíveis
- **Evidência:** `fase3/resultados/E2_curvas.json`, `fase3/resultados/E2b_curvas.json`
- **Cobertura:** ver as perguntas relacionadas: Q11, Q12
- **Validação:** Estatísticas calculadas, sem leitura possível: nenhum dos 5 nulos é calibrado, nem em 2022; S1 mede ruído no cruzamento.
- **Independência:** Interna (hora de recebimento registrada pelo próprio TSE) + capturas de terceiro (externa parcial)
- **O que demonstra:** Não determinado.
- **O que não demonstra:** Modelo de chegada por lote de recepção ou snapshots.
- **Impacto em votos:** Não se traduz em votos: forma da curva.
- **Próxima evidência decisiva:** idem Q10

### C2. As curvas de 2022 e 2026 têm as mesmas características?
- **Resposta direta:** 2022 e 2026 têm as mesmas características? Diferem na descrição; semelhança estatística não determinada.
- **Estado:** Não determinado com as evidências disponíveis
- **Evidência:** `fase3/resultados/E2_curvas.json`
- **Cobertura:** ver as perguntas relacionadas: Q13
- **Validação:** Diferem: no 2º turno de 2026 a liderança muda duas vezes (Lula 10%, perde aos 13,5%, retoma aos 47,2%); em 2022 o adversário lidera até 67,6% apurado e Lula assume. A ordem de chegada é mais territorial em 2026 (η² por UF 0,39 contra 0,24; por município 0,71 contra 0,59). 1º turno parecido. Semelhança visual não é estatística.
- **Independência:** Interna (hora de recebimento registrada pelo próprio TSE) + capturas de terceiro (externa parcial)
- **O que demonstra:** Diferem na descrição; semelhança estatística não determinada.
- **O que não demonstra:** Mais anos ou snapshots externos.
- **Impacto em votos:** Não se traduz em votos: comparação da forma das curvas.
- **Próxima evidência decisiva:** idem Q10

### M1. O crescimento de votos entre turnos é reconciliável?
- **Resposta direta:** O crescimento entre turnos é reconciliável? Sim, contabilmente (identidade exata); fluxos individuais não identificáveis.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase2/sessao_limitada_2026-10-28/p1_resultado_principal.json`, `fase2/resultados/P13.json`, `fase2/resultados/P15.json`, `fase2/sessao_limitada_2026-10-28/h1_resultado.json`
- **Cobertura:** ver as perguntas relacionadas: Q21, Q22, Q23, Q24, Q26
- **Validação:** A identidade contábil fecha em 2022 e 2026 e nenhuma combinação observada é matematicamente impossível; quais transferências ocorreram não é identificável.
- **Independência:** Aritmética exata sobre totais do TSE
- **O que demonstra:** Sim, contabilmente (identidade exata); fluxos individuais não identificáveis.
- **O que não demonstra:** Dados individuais (não existem).
- **Impacto em votos:** 2026: os finalistas somaram +14,10 mi = 9,32 mi dos eliminados + 2,96 mi de comparecimento + 1,82 mi de brancos e nulos a menos. 2022: +10,22 mi = 9,90 mi + 0,57 mi − 0,25 mi.
- **Próxima evidência decisiva:** idem Q24

### Z1. Seções com zero votos para um finalista (Flávio em 2026; Bolsonaro em 2022) indicam anomalia?
- **Resposta direta:** Os zeros indicam anomalia? Sem divergência documental; não determinado: nenhum modelo de cauda baixa calibrou (R3 e T64); descritivamente, são locais de uma só seção, com menos de 1% do total.
- **Estado:** Não determinado com as evidências disponíveis
- **Evidência:** `operacao_veracidade/05_ZEROS_E_ENTRE_TURNOS.md`, `fase3/f3_zeros.py`, `fase3/resultados/E3_zeros.json`, `fase3/rev_i2_zeros.py`, `fase3/resultados/rev_i2.json`, `fase3/resultados/bu1.json`, `fase3/inv_r3_zeros.py`, `fase3/resultados/r3_zeros.json`
- **Cobertura:** ver as perguntas relacionadas: Q15, Q16, Q17, Q18, Q19, Q20
- **Validação:** Arquivos: 0 divergências nas 486 seções-turno com zero. Estatística: nenhum modelo de cauda baixa passou na calibração. O modelo do R3 (79,1 e 101,5 previstos para Flávio; 162,9 e 136,5 para Bolsonaro 2022) falhou o critério; as três famílias do T64 também (por município, 1,3 contra 106 e 4,3 contra 141; por local, 66,7 contra 106 e 63,3 contra 141). Descritivamente, os zeros são locais de uma só seção, com menos de 1% do total, nos dois anos.
- **Independência:** Estatística sobre dado do TSE (origem única); poder só nos mecanismos simulados
- **O que demonstra:** Sem divergência documental; não determinado: nenhum modelo de cauda baixa calibrou (R3 e T64); descritivamente, são locais de uma só seção, com menos de 1% do total.
- **O que não demonstra:** Modelo de cauda baixa que passe em critério fixado antes.
- **Impacto em votos:** Se os zeros fossem anomalia, os votos em jogo seriam os que o candidato teria nessas seções: de ~44 a ~4.800 votos conforme o modelo (2026, 2º turno), no máximo 0,11% da margem de 4,43 mi.
- **Próxima evidência decisiva:** idem Q18

### MET. Os métodos usados nas perguntas ativas resistem à revisão?
- **Resposta direta:** Os métodos resistem à revisão? Com limites registrados: T10/T11 descritivos; T02 cego a município inteiro; E02 dependente do método; zeros sem modelo validado; concordância entre registros é consistência interna.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/AUDITORIA_F3.md`, `fase3/RELATORIO_ACEITACAO_F3.md`, `fase3/PARECER_CONSOLIDACAO_F3.md`, `fase3/RELATORIO_VERIFICACOES_FINAIS_F3.md`
- **Cobertura:** ver as perguntas relacionadas: Q7
- **Validação:** T10/T11 descritivos; T02 cego a município inteiro; E02 dependente do método; zeros sem modelo validado; regra de detecção válida é a do sentido correto; 'explicado pelo log' passa a 'compatível com os registros'; concordância BU/RDV/imagem/log é consistência interna; 'certificado ≠ log' não indica troca de urna em 2022.
- **Independência:** Sintética (simulação; nenhum voto real alterado)
- **O que demonstra:** Com limites registrados: T10/T11 descritivos; T02 cego a município inteiro; E02 dependente do método; zeros sem modelo validado; concordância entre registros é consistência interna.
- **O que não demonstra:** Modelos de chegada e de cauda baixa.
- **Impacto em votos:** Detectado nos cenários simulados: ~123 mil votos dispersos (2,8% da margem de 2026) e ~62 mil concentrados (1,4%). Não detectado: ~25 mil (0,6%). No município inteiro de uma grande cidade, a bateria original falha até ~696 mil votos, mas o teste T44 vê a partir de 31 mil a 139 mil (2% dos válidos). No T63, UFs, região, lote e deslocamento uniforme passam sem alarme até ~0,5 a 2,2 mi votos, ou sempre (uniforme em logit). Inverter 2026 exigiria trocar ~2,22 mi votos de lado.
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística ou auditoria independente; para a parte estatística, modelo validado

### AUT. Os arquivos publicados (BU, RDV, log, imagem) são íntegros e autênticos, e até onde vai essa verificação?
- **Resposta direta:** Os arquivos são autênticos? Íntegros e assinados até a AC emissora; consistentes entre si; a autenticidade integral do processo não é verificável com dados públicos.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `testes/registro.json (T14 a T17b)`, `fase3/inv_r1_integridade.py`, `fase3/resultados/r1_integridade.json`, `fase3/RELATORIO_ADVERSARIAL.md`, `fase3/resultados/adv_casos.json`, `fase3/resultados/adv_log_x_comparecimento.json`, `fase2/resultados/P16.json`, `fase2/resultados/P11.json`, `fase3/resultados/a173.json`, `fase3/resultados/sa22.json`
- **Cobertura:** ver as perguntas relacionadas: Q1, Q2, Q3, Q5, Q6
- **Validação:** R1: tabela = bu.dat = RDV = imagem em todas as seções lidas de 2022 e 2026, com hash e assinatura válidos até a AC emissora. Auditoria adversarial: isso é consistência interna (mesma urna, mesma chave); a única custódia independente é o R2 (agregado nacional). Divergências documentais preservadas: RS 88013/2/199 (imagem 196 × boletim 288; log só com 196 votos) e 153 seções-turno de 2022 com log diferente do comparecimento (5.287 votos sem registro no log publicado).
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Íntegros e assinados até a AC emissora; consistentes entre si; a autenticidade integral do processo não é verificável com dados públicos.
- **O que não demonstra:** Âncora do TSE; boletins de terceiros; logs das urnas substitutas.
- **Impacto em votos:** 0 voto de diferença entre a tabela e os boletins em todos os ~128 milhões de votos de 2026 (2º turno) e ~124 milhões de 2022 conferidos. As 5 seções de 2022 sem arquivo somam 5 votos de comparecimento. Alcança todos os votos: nenhum voto, de 2022 ou 2026, tem a assinatura verificada até a raiz do TSE; todos estão verificados até a AC emissora (100% das urnas, verificação completa em 28/10/2026, T60a).
- **Próxima evidência decisiva:** Cadeia até a raiz e auditoria do software

### A173. Os 173 arquivos assinados pela urna que o DataUrnas-BR aponta como ausentes do pacote de dados abertos de 2022 (64 seções, a maioria do exterior) afetam a base do projeto?
- **Resposta direta:** Os 173 arquivos estão ausentes da publicação? Sim, do pacote de dados abertos (duas cópias); conteúdo não verificado; outro canal do TSE inacessível.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `fase3/ver_a173.py`, `fase3/resultados/a173.csv`, `fase3/resultados/a173.json`
- **Cobertura:** ver as perguntas relacionadas: Q4
- **Validação:** Os 173 arquivos (61 .logjez, 56 .rdv, 56 .imgbu) em 64 seções (54 do exterior, 1º turno, cada uma sem .imgbu, .logjez e .rdv; 10 no Brasil, sem 1 ou 2 arquivos) estão listados no .vscmr do pacote local com o mesmo SHA-512 informado pelo DataUrnas-BR, com assinatura da lista válida, e também faltam no pacote oficial baixado pelo projeto em 27/10/2026 (o DataUrnas-BR baixou em 14/10). Não é diferença de nome, de coleta nem de processamento: nenhum outro arquivo da seção tem o mesmo SHA-512. São registros únicos (RDV voto a voto, log, imagem) sem substituto no pacote. O BU está presente nas 64 seções, e os votos do BU são iguais aos da tabela publicada em todas (0 diferenças; 44.983 aptos, 21.112 comparecimentos). O outro canal do TSE (arquivos por urna no site de resultados de 2022) devolveu 404 em duas consultas; não se sabe se esses arquivos estão publicados em outro lugar.
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Sim, do pacote de dados abertos (duas cópias); conteúdo não verificado; outro canal do TSE inacessível.
- **O que não demonstra:** Consulta ao TSE sobre os 173 arquivos; site de resultados de 2022 acessível.
- **Impacto em votos:** 64 seções com 21.112 comparecimentos; votos do boletim iguais à tabela.
- **Próxima evidência decisiva:** Segunda via dos 173 arquivos ausentes por canal do TSE

### BU1. A seção MG 49050/196/173 (2022, 1º turno), cujo BU não foi lido pelo leitor do projeto, concorda com a tabela publicada?
- **Resposta direta:** A seção com BU não lido concorda? Sim (boletim do Sistema de Apuração, assinatura válida; consistência interna).
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/ver_bu1.py`, `fase3/resultados/bu1.json`
- **Cobertura:** ver as perguntas relacionadas: Q20
- **Validação:** Arquivos da seção no pacote local: .busa, .imgbusa, .logsajez, .rdv e .vscsa (seção apurada pelo Sistema de Apuração, BU emitido às 23:47). A falha era do leitor de 2022, que não reconhece essas extensões; o arquivo não está danificado. Lista .vscsa assinada (ECDSA P-521, certificado ueao01293146 emitido pela AC URNA) com hash e assinatura válidos para os 4 arquivos. Boletim decodificado: 109 aptos, 16 comparecimentos, 16 votos para Lula, 0 para os demais; leitura independente do texto impresso (.imgbusa): 16 para Lula, 0 brancos, 0 nulos. Igual à tabela publicada (0 diferenças). Com isso as 301 seções-turno de 2022 com zero votos para Bolsonaro estão verificadas.
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia)
- **O que demonstra:** Sim (boletim do Sistema de Apuração, assinatura válida; consistência interna).
- **O que não demonstra:** —
- **Impacto em votos:** 16 votos, iguais à tabela.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

### SA22. As 159 seções-turno de 2022 apuradas pelo Sistema de Apuração (arquivos .busa, .imgbusa, .logsajez, .vscsa) foram verificadas pelos arquivos de urna do projeto?
- **Resposta direta:** As 159 seções do Sistema de Apuração de 2022 conferem? Sim, 159/159 (consistência interna).
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `fase3/ver_sa22.py`, `fase3/resultados/sa22.csv`, `fase3/resultados/sa22.json`
- **Cobertura:** ver as perguntas relacionadas: Q1
- **Validação:** fase3/ver_sa22.py leu as 159 seções-turno de 2022 apuradas pelo Sistema de Apuração (116 no 1º turno, 99 do exterior; 43 no 2º, 33 do exterior; 27 no Brasil), uma por uma (lista em fase3/resultados/sa22.csv). Em todas há .busa, .imgbusa, .logsajez, .rdv e .vscsa (11 também com log da urna, .logjez). Motivo da falha: o leitor de 2022 não reconhecia essas extensões. Resultado: 159 de 159 com boletim decodificado igual à tabela publicada (votos e comparecimento; 27.692 votos no total), texto impresso (.imgbusa, segunda leitura) igual e lista .vscsa com assinatura válida (156 ECDSA P-521 pela AC URNA, 3 Ed521 pela AC UE2020), conferindo tamanho, SHA-512 e assinatura de todos os arquivos presentes. 0 divergências objetivas; 0 seções sem leitura. Limites: comparação interna (mesma origem, TSE; o texto impresso é outra leitura, não outra fonte); cadeia de certificados só até a AC emissora (ver P11); as listas assinadas citam arquivos ausentes do pacote: .hash, .ver e .chvtp nas 159 e .jufa em 8 (485 arquivos), sem efeito sobre votos, sem explicação verificada.
- **Independência:** Interna (mesma origem TSE: tabela, BU, RDV, imagem, log e lista assinada vêm do mesmo equipamento ou da mesma cadeia); decodificação por leitor próprio
- **O que demonstra:** Sim, 159/159 (consistência interna).
- **O que não demonstra:** Saber se os auxiliares .hash, .ver, .chvtp e .jufa ficam fora do pacote por regra de publicação.
- **Impacto em votos:** 27.692 votos, iguais à tabela.
- **Próxima evidência decisiva:** Não é necessária para a pergunta no escopo; para veracidade, ver H9 e H10 (amostra probabilística de boletins impressos)

## Parte C. As perguntas desta operação com o rótulo N (mesmo conteúdo das Q42 a Q50 da Parte A; N9 = Q42 e N1 a N8 = Q43 a Q50)

### N1. Os certificados de todas as urnas de 2022 e 2026 verificam até a AC emissora, estavam válidos no dia da eleição e são únicos?
- **Resposta direta:** Sim: nos 1.942.246 pares seção × turno (2022 e 2026, dois turnos) a assinatura da AC emissora verifica, 0 falhas, todos válidos no dia, nenhum emitido depois da eleição, nenhuma chave pública repetida. A raiz não é pública.
- **Estado:** Demonstrado no escopo definido (até a AC emissora)
- **Evidência:** `operacao_veracidade/scripts/cert_extrai.py`, `operacao_veracidade/resultados/cert_analise.json`, `operacao_veracidade/resultados/certs_2026_1t.parquet`, `operacao_veracidade/resultados/certs_2022_2t.parquet`
- **Cobertura:** 499.176 + 499.178 seções (2026) e 471.908 + 471.984 (2022), 0 erros de leitura; exterior e Sistema de Apuração sem vota.vsc ficam fora
- **Validação:** Ed521 só com M = TBS (sem busca de variantes); ECDSA por biblioteca padrão; controles positivos e negativos em T60b; testes unitários do Ed521 (9 de 9)
- **Independência:** Interna (certificados e lista vêm da mesma urna) com ACs obtidas de terceiro; **externa quanto à AC só por cópia de terceiro**
- **O que demonstra:** Que toda chave de urna pertence à cadeia das ACs que temos e que nenhuma chave se repete entre urnas. Fecha a lacuna dos 200 casos do P11.
- **O que não demonstra:** Que a raiz é do TSE (AC RAIZ UE e AC URNA v2 não são públicas); que a cópia das ACs é a oficial (página do TSE bloqueada a este ambiente); fidelidade do voto.
- **Impacto em votos:** Não se traduz em votos.
- **Próxima evidência decisiva:** AC RAIZ UE e AC URNA v2 obtidas por canal oficial verificável

### N2. O verificador de assinaturas rejeita arquivos adulterados, e o que cada degrau (hash, assinatura do arquivo, assinatura da lista, cadeia) prova?
- **Resposta direta:** Sim: 0 de 40 genuínos rejeitados; 40 de 40 rejeitados em cada uma de 7 mutações, em 2026 e em 2022. A assinatura do arquivo sozinha não detecta alteração do arquivo; o hash detecta. Um certificado sintético autoassinado passa pela verificação de lista e só a cadeia o rejeita.
- **Estado:** Demonstrado no escopo definido
- **Evidência:** `operacao_veracidade/scripts/controles_mutacao.py`, `operacao_veracidade/resultados/controles_mutacao_2026_AC.json`, `operacao_veracidade/resultados/controles_mutacao_2022_AL.json`, `operacao_veracidade/resultados/ed521_unitarios.json`
- **Cobertura:** 40 seções reais de AC (2026) e 40 de AL (2022); 9 testes unitários do Ed521
- **Validação:** controle positivo (genuíno) e 8 negativos; chave descartável em memória
- **Independência:** Sintética (mutações em cópias em memória)
- **O que demonstra:** Que o verificador do projeto não aceita as adulterações testadas e que nenhum resultado herdado depende de `assin_ok` isolado.
- **O que não demonstra:** Que o verificador seja correto contra todo ataque; que a chave seja de uma urna autêntica.
- **Impacto em votos:** Não se traduz em votos.
- **Próxima evidência decisiva:** Revisão externa do código de verificação por criptógrafo independente

### N3. Os boletins impressos lidos por terceiros (QR Code) concordam com a base do TSE e têm assinatura válida?
- **Resposta direta:** Sim, nos 404 boletins do 2º turno de 2026 obtidos: assinatura da urna válida, cadeia até a AC, votos iguais à tabela e ao BU do TSE, identidade da urna igual. É amostra de conveniência (0,08% das seções).
- **Estado:** Parcialmente demonstrado (amostra de conveniência)
- **Evidência:** `operacao_veracidade/scripts/terceiros_qr.py`, `operacao_veracidade/resultados/terceiros_qr.json`, `operacao_veracidade/externo/arvor_totalizacao/SHA256SUMS.txt`
- **Cobertura:** 404 de 499.207 seções (0,08%), 22 UFs, 167 de SP, só 2º turno de 2026
- **Validação:** verificador próprio da assinatura; `hash_final` = SHA-512 do conteúdo em 404; comparação com tabela, BU do pacote e certificado do vota.vsc
- **Independência:** **Externa parcial**: cadeia de obtenção diferente (QR do boletim impresso), mas a assinatura é da mesma urna; coletor e publicador são o mesmo projeto
- **O que demonstra:** Que o boletim impresso na seção coincide com o que o TSE publicou nas 404 seções; 77 deles já estavam no servidor de terceiros entre 18:10 e 18:47, 45 minutos ou mais antes do TSE registrar o recebimento.
- **O que não demonstra:** Veracidade do voto; representatividade; qualquer coisa fora da amostra; o relógio do servidor de terceiros não é auditado.
- **Impacto em votos:** Não se traduz em votos: 404 seções sem diferença.
- **Próxima evidência decisiva:** Boletins impressos de amostra probabilística, com lista de seções sorteada antes da eleição

### N4. Que alterações cada verificação de consistência consegue ver, e um registro coerente gerado por fonte comprometida seria distinguível de um genuíno?
- **Resposta direta:** Alterar só a tabela é visto pela comparação com o BU; BU e tabela, pelo RDV, pela imagem e pelo hash; tudo sem reassinar, só pelo hash da lista assinada; registros coerentes assinados pelo próprio gerador **não são vistos por nenhuma verificação interna**.
- **Estado:** Demonstrado no escopo definido (limite de identificabilidade)
- **Evidência:** `operacao_veracidade/scripts/identificabilidade.py`, `operacao_veracidade/resultados/identificabilidade.json`
- **Cobertura:** 52.062 seções reais de MG, 2º turno de 2026, 2.497 alteradas (59.499 votos); 6 cenários e 6 verificações
- **Validação:** controle sem alteração: 0 em todas as verificações
- **Independência:** Sintética
- **O que demonstra:** O que cada consistência interna pode e não pode ver.
- **O que não demonstra:** Que alguém consiga produzir registros coerentes assinados na prática; só mede o limite.
- **Impacto em votos:** Não se traduz em votos.
- **Próxima evidência decisiva:** Amostra probabilística de boletins impressos ou auditoria do software da urna (as únicas que separam os dois mundos)

### N5. Que mecanismos de alteração a bateria estatística consegue ver, com que poder, e quais passam sem alarme?
- **Resposta direta:** Vê com 80% de poder a partir de 25 a 50 mil votos: seções dispersas, poucas seções, locais, zonas e municípios inteiros, redutos. Só vê a partir de 0,5 a 2,2 milhões, ou nunca: UFs, os cinco grandes juntos, macrorregião, lote tardio, conversão de brancos e nulos, deslocamento uniforme. O poder é assimétrico entre sentidos. Um atacante de estrutura completa passa D1 a D7 em 2026.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `operacao_veracidade/scripts/sim_adversarial.py`, `operacao_veracidade/scripts/sim_fabricacao_v2.py`, `operacao_veracidade/resultados/sim_2026_resumo.json`, `operacao_veracidade/resultados/sim_2022_resumo.json`, `operacao_veracidade/03_SIMULACOES_ADVERSARIAIS.md`
- **Cobertura:** 2026 e 2022; 15 mecanismos, 2 sentidos, 7 magnitudes, 20 réplicas; limiares do bootstrap por município
- **Validação:** falso alarme em bootstrap independente (4% a 14,5% a união); sensibilidade do D1 (z de 3 e 5); fabricação em três níveis
- **Independência:** Sintética (base real é referência, não verdade conhecida)
- **O que demonstra:** Quais mecanismos a bateria vê e em que escala; que a ausência de alarme em mecanismos de UF, região, lote e uniforme não exclui alterações de centenas de milhares de votos.
- **O que não demonstra:** Que a base real foi ou não alterada (alteração já presente é absorvida pelo limiar); que a soma das anomalias seja teto de fraude.
- **Impacto em votos:** Poder ≥ 80% só a partir de 25 mil (locais, zonas) a 2,22 mi votos movidos (UFs, uniforme); ver tabela em 03.
- **Próxima evidência decisiva:** Detectores com referência externa (histórico, boletins impressos)

### N6. Os zeros de votos de um finalista são excepcionais depois de modelos calibrados (2022 e 2026)?
- **Resposta direta:** Não determinável: três famílias de modelo (município, zona, local de votação) falharam o critério fixado antes; os zeros são, na descrição, locais de uma seção só com menos de 1% do total, nos dois anos (141 em 2022 e 106 em 2026 para o candidato da direita; 2 e 4 para Lula).
- **Estado:** Não determinável com as evidências disponíveis
- **Evidência:** `operacao_veracidade/scripts/zeros_contagens.py`, `operacao_veracidade/scripts/zeros_locais.py`, `operacao_veracidade/resultados/zeros_contagens.json`, `operacao_veracidade/05_ZEROS_E_ENTRE_TURNOS.md`
- **Cobertura:** todas as seções com comparecimento positivo, 2022 e 2026, dois turnos, dois finalistas
- **Validação:** beta-binomial com UF retida, 500 sorteios Monte Carlo; critério: 80% das UFs com esperado ≥ 1 dentro do intervalo de 95%
- **Independência:** Interna (tabela do TSE)
- **O que demonstra:** As contagens (0, 1, 2, 3 a 5 votos) e o perfil descritivo dos zeros.
- **O que não demonstra:** Excesso ou ausência de excesso de zeros; o modelo por local reproduz 45% a 63% e falha.
- **Impacto em votos:** 14.860 votos de Lula nas 106 seções de 2026 (0,34% da margem); 16.418 em 2022.
- **Próxima evidência decisiva:** Modelo de cauda baixa que passe no critério (nenhum das 3 famílias passou)

### N7. Os arquivos que o TSE publicou mudaram entre downloads independentes?
- **Resposta direta:** Não, nos 404 boletins: o SHA-256 do `bu.dat` baixado por terceiros do TSE (a partir de 25/10) é igual ao do nosso download (27 e 28/10) em 404 de 404.
- **Estado:** Demonstrado no escopo definido (404 arquivos)
- **Evidência:** `operacao_veracidade/scripts/republicacao_bu.py`, `operacao_veracidade/resultados/republicacao_bu.json`
- **Cobertura:** 404 BU de 22 UFs
- **Validação:** comparação byte a byte (SHA-256) entre duas origens de download
- **Independência:** Externa parcial: hash declarado por terceiro, confirmado por igualdade com o nosso
- **O que demonstra:** Nenhuma republicação nesses arquivos entre os dois downloads.
- **O que não demonstra:** Que o arquivo seja o que a urna gerou; arquivos fora dos 404; mudanças antes do primeiro download.
- **Impacto em votos:** Não se traduz em votos.
- **Próxima evidência decisiva:** Capturas de arquivos do TSE em horários de resolução fina por terceiros

### N8. Há divergência objetiva nova nos dados publicados pelo TSE?
- **Resposta direta:** Nenhuma divergência de votos. Há lacunas documentais: 98 certificados emitidos depois da validade do certificado público da AC URNA; certificado ≠ urna da tabela em 17 seções de 2026 e 22 de 2022 (1 com três identificações diferentes); regra de emissão por modelo não pública; raiz ausente.
- **Estado:** Parcialmente demonstrado
- **Evidência:** `operacao_veracidade/resultados/casos_certificado.csv`, `operacao_veracidade/resultados/casos_A_relidos_por_id_e_data.csv`, `operacao_veracidade/evidencia/caso_ES_57932_9_85_112.json`, `operacao_veracidade/06_ANOMALIAS_E_LOGS.md`
- **Cobertura:** 2026 e 2022, dois turnos, todas as seções com certificado
- **Validação:** releitura por ID de urna, data e seção, com segundo método de leitura do log (caso ES)
- **Independência:** Interna (certificado da AC, tabela e log têm origens parcialmente distintas)
- **O que demonstra:** As lacunas e o artefato do leitor (log de pacote traz logs arquivados de outras urnas e seções).
- **O que não demonstra:** Causa de cada caso; os explicados vêm do próprio log (compatível, não verificado).
- **Impacto em votos:** Menos de 30 mil votos válidos nas seções dos tipos A e D (cerca de 0,6% da margem de 2026).
- **Próxima evidência decisiva:** Ata e caderno de votação das seções citadas; documentação de contingência do TSE; certificado renovado da AC URNA

### N9. A conta dos "votos extras" (98,12%) mostra que o crescimento de Lula entre os turnos não fecha?
- **Resposta direta:** Não. A aritmética do vídeo está certa, mas o 98% é a premissa de 60% devolvida: é o mínimo possível para a parcela dos outros que vai a Lula e deixa Flávio sem nenhum voto dos extras. Com 85% dos outros indo a Lula, os extras se dividem 51/49. O mesmo método dá 370% para Bolsonaro em 2022. O que é real: o candidato que mais cresceu recebeu mais que a divisão proporcional nos dois anos, em todas as UFs, e em 2026 mais (26,2% do disponível contra 19,6%).
- **Estado:** Refutado no escopo definido (a conclusão do vídeo); resíduo descrito sem causa
- **Evidência:** `operacao_veracidade/scripts/hipotese_video.py`, `operacao_veracidade/scripts/hipotese_video_m6.py`, `operacao_veracidade/resultados/hipotese_video.json`, `operacao_veracidade/resultados/hipotese_video_m6.json`, `operacao_veracidade/10_HIPOTESE_DO_VIDEO.md`
- **Cobertura:** totais nacionais com exterior (identidade exata) e 5.570 municípios sem exterior, 2022 e 2026
- **Validação:** identidade exata (diferença 0); regressão ecológica com bootstrap de municípios; controle proporcional (M6) declarado como exploratório
- **Independência:** Aritmética exata sobre totais do TSE; ecológica (associação, frágil: T37 e T59)
- **O que demonstra:** Que o 98,12% decorre da premissa; que os extras não precisam ter ido todos a Lula; que o método não discrimina (2022: 370%); que a abstenção também caiu em 2022.
- **O que não demonstra:** Para onde foi cada eleitor (Q26); causa do resíduo de 3,68 mi acima do proporcional; a afirmação 'nunca aconteceu' para anos anteriores a 2022 (sem dados no projeto).
- **Impacto em votos:** Resíduo acima do proporcional: +3,68 mi para Lula em 2026 (26,2% do disponível) e +1,99 mi para Bolsonaro em 2022 (19,6%); não é limite de fraude nem evidência dela.
- **Próxima evidência decisiva:** Pesquisa de painel 1º→2º turno ou dado individual (inexistente por sigilo)

