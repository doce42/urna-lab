"""F3: respostas científicas explícitas (fonte única). Gera fase3/respostas_f3.json (lido pelo site, página "Perguntas e respostas
científicas") e fase3/RESPOSTAS_F3.md. Cada resposta aponta para os arquivos de resultado que a sustentam; o histórico de cada item
do inventário vem de fase3/inventario.json."""
import json

R = "."
DEM, REF, PAR, ND, NE = "Demonstrado no escopo definido", "Refutado no escopo definido", "Parcialmente demonstrado", "Não determinado com as evidências disponíveis", "Não executado"
PARC404 = "Parcialmente demonstrado (404 boletins, amostra de conveniência)"
CONS = "Consistência interna: BU, RDV, imagem e log são gerados pela mesma urna e assinados pela mesma chave; tabela e totais vêm do mesmo TSE. A concordância não verifica de forma independente o que foi votado."


def q(id, pergunta, resposta, classe, evid, numeros, demonstra, nao_demonstra, robustez, causa, alcance, mudaria, validacao, por_ano=None, reabre=""):
    return {"id": id, "pergunta": pergunta, "resposta": resposta, "classificacao": classe, "evidencias": evid, "numeros": numeros, "demonstra": demonstra,
            "nao_demonstra": nao_demonstra, "robustez": robustez, "causa": causa, "alcance": alcance, "mudaria": mudaria, "validacao": validacao, "por_ano": por_ano or {}, "reabertura": reabre}


INT = [
 q("Q1", "Os votos oficiais por seção são iguais aos boletins de urna?",
   "Sim, em todas as seções cujo boletim foi lido, nos dois anos e nos dois turnos: 0 diferenças entre a tabela publicada e o bu.dat.",
   DEM, ["fase3/inv_r1_integridade.py", "fase3/resultados/r1_integridade.json", "fase3/resultados/sa22.json", "fase3/resultados/R1_20_dataurnas.json"],
   "2026: 499.198 de 499.206 (1º turno) e 499.201 de 499.205 (2º) boletins lidos, 0 diferenças. 2022: 471.907 (1º) e 471.980 (2º) lidos, 0 diferenças, mais 159 seções-turno do Sistema de Apuração lidas à parte (0 diferenças); 10 seções-turno de 2022 sem boletim lido pelo projeto (7 do exterior, 2 do Pará, 1 do Rio Grande do Sul), na fila.",
   "Os votos da tabela publicada são os mesmos dos boletins digitais assinados pelas urnas.", CONS + " Não exclui comprometimento anterior à geração do boletim (H2).",
   "Releitura direta de 100 seções sorteadas dos zips: 100/100 idênticas. Decodificação independente de terceiro (DataUrnas-BR): 0 diferenças em 2026 1º turno e em 99,96% das seções do Brasil em 2022.",
   "não aplicável", "Todas as seções com boletim publicado; votos de Presidente.", "Uma seção com boletim lido e votos diferentes da tabela; boletim impresso coletado por terceiro com valores diferentes.",
   "Executado e reproduzido (R1, releitura).",
   {"2022": "0 diferenças em 471.907 + 471.980 seções + 159 do Sistema de Apuração; 10 sem boletim lido.", "2026": "0 diferenças em 499.198 + 499.201 seções."}),
 q("Q2", "Os votos publicados podem ser reconstruídos a partir dos RDVs disponíveis?",
   "Sim, em todas as seções com RDV lido: a recontagem voto a voto dá os mesmos totais de candidatos, brancos e nulos da tabela.",
   DEM, ["fase3/resultados/r1_integridade.json", "testes/registro.json (T17, T17b)"],
   "2026: 499.167 (1º) e 499.174 (2º) RDVs lidos, 0 diferenças. 2022: 471.851 e 471.980, 0 diferenças (o leitor de 2022 já soma o nulo por suspensão no nulo; a primeira comparação somava de novo e acusou 42.764 e 7.410 diferenças falsas; corrigido e declarado).",
   "A tabela pode ser recomposta voto a voto pelo RDV publicado.", "O RDV é gravado pela mesma urna e pelo mesmo software que geram o boletim: a recontagem não é contagem independente do que o eleitor digitou.",
   "Duas correções do comparador declaradas (R1); releitura direta 100/100.", "não aplicável", "Seções com RDV publicado.", "Divergência RDV × tabela com o arquivo lido; RDV ausente em seções relevantes.", "Executado (R1).",
   {"2022": "0 diferenças em 471.851 + 471.980 seções.", "2026": "0 diferenças em 499.167 + 499.174 seções."}),
 q("Q3", "Existem divergências verificáveis entre boletins, RDV, logs, tabelas e totalização?",
   "Nos votos, não. Entre arquivos e entre log e comparecimento, sim: há divergências objetivas pontuais, preservadas como achados, sem efeito demonstrado sobre votos.",
   PAR, ["fase3/resultados/r1_integridade.json", "fase3/resultados/adv_log_x_comparecimento.json", "fase3/RELATORIO_ADVERSARIAL.md", "analise/resultado_casos_integridade_1t.json", "testes/registro.json (T32, T36)"],
   "Totalização: 638 de 638 itens iguais ao total oficial (T32). Log × comparecimento: 2022, log com menos votos em 70 (1º) e 36 (2º) seções (3.618 e 1.669 votos sem registro no log publicado) e com mais em 34 e 13 (fila F1: recontagem confirmada em 153/153; em 29 das 47 com log maior, um subconjunto exato das partes arquivadas do log soma o comparecimento, compatível com partes de outra sessão no log publicado); 2026, 9 e 7 seções (59 e 54 votos), no T36. Imagem × boletim: RS 88013/2/199 (2022): imagem assinada com 196 votos, boletim e tabela com 288; log da urna 2215062 com 196 votos (último às 13:53). T36 (2026): 186 e 75 casos de contas que não fecham, compatíveis com registros (troca de urna, RED, reinício), 1 sem explicação (RJ 60011/8/61).",
   "Há divergências documentais objetivas, todas pequenas e sem deslocamento de votos detectável nas seções envolvidas.", "A causa de cada divergência. As explicações operacionais vêm do próprio sistema (compatíveis, não verificadas).",
   "Teste de votação nas seções com explicação registrada (T36, contingências): sem deslocamento (adv_casos.json). Exploratório em 2022 (log ≠ comparecimento): sem deslocamento, poder baixo.",
   "não demonstrada", "Seções com arquivos; Presidente.", "Logs das urnas substitutas; boletins impressos da seção; esclarecimento do TSE por seção.", "Executado (R1, auditoria adversarial).",
   {"2022": "Votos: 0. Log × comparecimento: 153 seções-turno; imagem × boletim: 1 seção.", "2026": "Votos: 0. Log × comparecimento: 16 seções-turno (T36); imagem da urna × tabela: 1 seção explicada como contingência registrada (Sistema de Apuração), compatível, não verificada."}),
 q("Q4", "Existem arquivos ausentes, seções não cobertas ou versões conflitantes? Qual o alcance?",
   "Sim, arquivos ausentes e algumas seções não cobertas; versões conflitantes não foram encontradas no que foi possível comparar.",
   PAR, ["fase3/resultados/a173.json", "fase3/resultados/sa22.json", "fase3/resultados/a1.json", "fase3/resultados/r1_integridade.json", "fase3/resultados/r2_curva_publica.json"],
   "2022: 173 arquivos assinados (RDV, log, imagem; 64 seções, 54 do exterior) e 485 auxiliares fora do pacote de dados abertos; das 10 seções sem boletim lido, 5 foram lidas na fila F3 (conferem) e 5 do exterior não têm arquivo nenhum no pacote. 2026: 1 log assinado e não publicado (SP, 2º turno); seções do Sistema de Apuração (31 e 29) conferidas na fila F2: lista assinada válida em 60/60, boletim = tabela; 3 seções do exterior fora da tabela com comparecimento 0 (P12); a imagem parcial da urna em MG 50075/47/41 não consta de lista assinada publicada. Versões: uma só captura de cada arquivo; os totais divulgados ao vivo (39 capturas) batem com a base final.",
   "Ausências de publicação objetivas e de alcance pequeno; os boletins dessas seções coincidem com a tabela.", "O conteúdo dos arquivos ausentes; republicação de arquivos entre datas (só há uma versão local).",
   "Duas cópias do pacote de 2022 (14/10 e 27/10/2026) com as mesmas ausências.", "não demonstrada", "Pacotes de dados abertos do TSE.", "Os 173 arquivos por outro canal; versões datadas dos pacotes.", "Executado (A173, SA22, R1, R2).",
   {"2022": "173 + 485 arquivos ausentes; 10 seções sem boletim lido.", "2026": "1 log ausente; assinatura do Sistema de Apuração não conferida pelo leitor."}),
 q("Q5", "Os registros foram autenticados criptograficamente até uma fonte de confiança apropriada?",
   "Não até a raiz: as assinaturas das urnas são válidas até a autoridade certificadora emissora em 100% das urnas de 2022 e 2026 (cadeia verificada por completo em 28/10/2026, T60a; antes, só em 200 seções e em 5% por terceiro), mas a ligação dessa autoridade a uma âncora do TSE não foi verificada: a raiz não é pública.",
   PAR, ["testes/registro.json (T16, T60a, T60b)", "fase2/resultados/P11.json", "fase3/resultados/sa22.json", "fase3/resultados/r1_integridade.json", "operacao_veracidade/resultados/cert_analise.json"],
   "2026: hash e assinatura válidos em 499.176 (1º) e 499.178 (2º) boletins. 2022: 471.908 e 471.984 boletins e as 159 seções do Sistema de Apuração. Cadeia até a AC emissora (T60a, 28/10/2026): 1.942.246 de 1.942.246 pares seção × turno, 0 falhas, todos válidos no dia, nenhuma chave repetida. Certificados de AC obtidos de terceiro (DataUrnas-BR); AC URNA v2 e AC RAIZ UE não obtidas por canal do TSE.",
   "Os arquivos presentes não foram alterados depois de assinados pela chave da urna, e todo certificado de urna é assinado pela AC emissora que temos.", "Que a chave pertence a uma urna autêntica do TSE (sem âncora); que a AC usada é a oficial (cópia de terceiro); qualquer coisa anterior à assinatura.",
   "Verificação Ed521 e ECDSA P-521 própria; chaves degeneradas rejeitadas.", "não aplicável", "Arquivos presentes.", "Certificados raiz obtidos do TSE por canal verificável.", "Bloqueado no elo final (fonte externa).",
   {"2022": "Assinatura válida até a AC emissora nos arquivos presentes; cadeia em 943.892 de 943.892 pares seção × turno (T60a).", "2026": "Idem; cadeia em 998.354 de 998.354 (T60a)."}),
 q("Q6", "Existem evidências externas independentes que confirmem ou contradigam os registros publicados?",
   "Sim, duas, e as duas confirmam: capturas do Internet Archive dos totais nacionais divulgados durante a apuração confirmam a base publicada nos instantes capturados; e 404 boletins impressos lidos por terceiros no 2º turno de 2026 (22 UFs) são iguais à tabela e ao BU do TSE, com assinatura e cadeia válidas (T61). Os boletins são amostra de conveniência (0,08% das seções), não sorteada; de 2022 não há boletins de terceiros.",
   PAR, ["fase3/inv_r2_curva_publica.py", "fase3/resultados/r2_curva_publica.json", "fase3/externos/wayback_capturas/", "testes/registro.json (T61)", "operacao_veracidade/resultados/terceiros_qr.json"],
   "39 capturas (2022: 2 e 27; 2026: 6 e 4): diferença máxima de 0,083 ponto percentual entre a proporção divulgada e a recomposta pela base final no mesmo número de seções; mesmo líder em todas; votos nunca diminuem; a última captura é igual ao total oficial onde existe.",
   "Que a base publicada depois corresponde ao que foi divulgado ao vivo, no agregado nacional e nos instantes capturados (contraria alteração posterior que mudasse esses totais).", "Correspondência seção a seção com fonte externa fora das 404 seções; o que aconteceu antes da geração do boletim; instantes não capturados.",
   "Custódia de terceiro (Internet Archive); escopo de busca fixado antes; capturas brutas guardadas com SHA-256.", "não aplicável", "Totais nacionais de Presidente em 39 instantes; 404 seções do 2º turno de 2026.", "Boletins impressos de uma amostra sorteada de seções; capturas por UF.", "Executado (R2, T61), com bloqueio parcial do Internet Archive registrado.",
   {"2022": "29 capturas consistentes; sem boletins de terceiros.", "2026": "10 capturas consistentes; 404 de 404 boletins de terceiros iguais."}),
 q("Q7", "Os testes conseguem detectar mecanismos plausíveis de alteração, e em quais condições falham?",
   "Detectam alguns, em condições limitadas: nos cenários simulados, trocas dispersas de ~123 mil votos e concentradas de ~62 mil em locais ou municípios de até ~5 mil seções foram detectadas no sentido certo; trocas de ~25 mil não foram detectadas; no município inteiro das 5 maiores cidades, a bateria original não detecta, mas o teste T44 (histórico de 2022 e perfil do 1º turno) detecta a partir de 2% dos válidos (31 mil a 139 mil votos). A grade adversarial do T63 (15 mecanismos, dois sentidos) mostra o resto do mapa: seções, locais, zonas e municípios são vistos a partir de 25 a 50 mil votos; UFs inteiras, os cinco grandes juntos, macrorregião, lote tardio, conversão de brancos e nulos, enchimento abaixo de 250 mil e deslocamento uniforme só a partir de 0,5 a 2,2 milhões, ou nunca; e o poder é assimétrico entre os sentidos.",
   PAR, ["fase3/rev_i1_poder.py", "fase3/rev_a2_poder.py", "fase3/resultados/rev_a2_2026.json", "fase3/resultados/rev_a2_2022.json", "testes/registro.json (T63)", "operacao_veracidade/03_SIMULACOES_ADVERSARIAIS.md"],
   "2026, 30 réplicas, limiar calibrado, falso alarme 0 em 30 (não é taxa zero: limite superior de 95% ≈ 11,6%); na grade do T63, a união dos detectores tem falso alarme medido de 4% a 14,5% conforme o ano e o sentido: dispersa 10% (~123 mil) 30/30; locais e municípios até ~5 mil seções a 5% (~62 mil) 30/30; região a 5% 26/30 e 23/30; 2% (~25 mil) 0 a 1/30; 5 maiores cidades a 10% (155 mil a 696 mil votos) 10 a 13/30 (E02 completo), Brasília e Fortaleza 0/12. T44: troca de 2% dos válidos no município inteiro detectável nas 5 cidades (4,0 a 5,2 desvios; falso alarme 3/200).",
   "O alcance dos testes nos cenários simulados.", "Detecção fora dos cenários simulados; mecanismos que preservam medianas, mexem no comparecimento ou atuam antes do boletim; que a base real esteja limpa (o poder é medido sobre ela); votos simulados não são votos encontrados.",
   "Validação em 2022 com o mesmo padrão; direção conferida.", "não aplicável", "4 mecanismos + grandes cidades (I1, A2); 15 mecanismos, 7 magnitudes e 2 sentidos (T63).", "Novos mecanismos ou coberturas simulados.", "Executado (I1, A2).",
   {"2022": "Mesmo padrão; limiar ancorado no real com 23% de falso alarme.", "2026": "Ver números."}),
]

CUR = [
 q("Q8", "Quantas vezes a liderança mudou na ordem de recebimento dos boletins?",
   "Depois dos primeiros 10% de urnas: 2022, 1º turno 1 vez (aos 68,2%); 2022, 2º turno 1 vez (aos 67,6%, adversário → Lula); 2026, 1º turno nenhuma; 2026, 2º turno 2 vezes (aos 13,5%, Lula → adversário, e aos 47,2%, adversário → Lula).",
   DEM, ["fase3/f3_curvas.py", "fase3/resultados/E2_curvas.json"],
   "A contagem urna a urna (S1) registra 3 e 21 trocas em 2022 porque soma oscilações no ponto de cruzamento; em grade de 1% são 1 e 1.",
   "O número de viradas na ordem de recebimento (reconstrução).", "Antes dos 10% das urnas; a ordem é de recebimento, não de divulgação (ver Q9).",
   "Grade de 0,5% e 2% como sensibilidade.", "não aplicável", "Votos de Presidente, ordem por DT_BU_RECEBIDO.", "—", "Executado (E2).",
   {"2022": "1 e 1.", "2026": "0 e 2."}),
 q("Q9", "Quantas vezes a liderança mudou na sequência pública efetivamente divulgada?",
   "Nas capturas disponíveis: 2022, 1º turno pelo menos 1; 2022, 2º turno 1 (adversário até 18:22, com 49,53% para Lula; Lula a partir de 19:43); 2026, 1º turno 0; 2026, 2º turno pelo menos 2 (Lula às 19:36 com 50,55%, adversário às 20:07 com 49,56%, Lula às 21:25). A sequência capturada é amostrada: os números são limites inferiores entre capturas.",
   PAR, ["fase3/resultados/r2_curva_publica.json", "fase3/externos/wayback_capturas/"],
   "Capturas: 2022 1º turno 2; 2º turno 27; 2026 1º turno 6; 2º turno 4.",
   "As viradas observadas na divulgação coincidem em sentido e momento com a reconstrução.", "Viradas entre capturas não observadas; 2022 1º turno e 2026 têm poucas capturas.",
   "Mesmo resultado por número de seções e por horário (defasagem de 0 minuto).", "não aplicável", "Totais nacionais divulgados.", "Mais capturas (por UF, outras janelas).", "Executado (R2).",
   {"2022": "1º turno ≥ 1; 2º turno 1.", "2026": "1º turno 0; 2º turno ≥ 2."}),
 q("Q10", "Uma quantidade pequena de viradas é incomum sob modelos realistas de chegada dos boletins?",
   "Não determinado: nenhum dos cinco nulos de permutação é calibrado, e o modelo de chegada com as horas reais de emissão e atraso de transmissão sorteado (fila F4) não foi validado em 2022 (última troca e maior vale fora da faixa; 0 de 27 capturas na faixa). O número de trocas observado cabe no modelo nos quatro casos, mas isso não é confirmatório.",
   ND, ["fase3/resultados/E2_curvas.json", "fase3/resultados/E2b_curvas.json"],
   "Nulos: irrestrito, por UF, por município, UF × hora de encerramento, UF × hora × tamanho; 200 permutações cada.",
   "—", "Que as viradas sejam comuns ou incomuns.", "—", "não aplicável", "—",
   "Um modelo de chegada que reproduza 2022 e as capturas.", "Tentado (E2, E2b, F4); nenhum validado. Parado pelo critério.", reabre="Construir modelo de chegada por lotes e validá-lo com as 27 capturas do 2º turno de 2022."),
 q("Q11", "Os vales aparentemente periódicos e os trechos lineares são reproduzíveis com os dados brutos?",
   "A curva divulgada é reproduzível com os dados por seção nos 39 instantes capturados (diferença ≤ 0,083 pp); periodicidade não foi testada com estatística validada.",
   PAR, ["fase3/resultados/r2_curva_publica.json", "fase3/resultados/E2_curvas.json"],
   "S3 (maior vale), S4 (oscilações), S5 (maior trecho linear) calculados; sem nulo calibrado.",
   "Que os pontos divulgados saem dos dados publicados por seção.", "Que vales ou trechos lineares sejam anômalos ou normais.", "—", "não aplicável", "Curvas de 2022 e 2026.", "Modelo de chegada validado; teste espectral pré-registrado.", "Parcial."),
 q("Q12", "Os padrões continuam anômalos após controles por geografia, lotes, horários, arredondamento e dependência territorial?",
   "Não determinado: com controles por UF, município, hora de encerramento e tamanho, os nulos continuam rejeitando também em 2022, então não discriminam.",
   ND, ["fase3/resultados/E2b_curvas.json"], "η² da ordem por UF × hora × tamanho: 0,36 (2026 1º turno).", "—", "Anomalia ou normalidade da curva.", "—", "não aplicável", "—", "Modelo de chegada validado (fila).", "Tentado."),
 q("Q13", "2022 e 2026 apresentam semelhanças estatisticamente relevantes depois desses controles?",
   "Não determinado estatisticamente. Descritivamente: nos dois anos a última troca de liderança vem mais tarde do que nos modelos nulos e do que o modelo de atraso de transmissão prevê (2022 2º turno: 68% contra 39% a 42%; 2026 2º turno: 48% contra 30% a 34%); em 2026 a ordem de chegada é mais territorial (η² por UF 0,39 contra 0,24).",
   ND, ["fase3/resultados/E2_curvas.json"], "—", "Semelhanças descritivas.", "Semelhança estatística após controles.", "—", "não aplicável", "—", "Depende de Q10.", "Parcial."),
 q("Q14", "Há divergência objetiva entre a sequência publicada e os registros históricos disponíveis?",
   "Não: nas 39 capturas históricas, a sequência divulgada é igual à recomposta pela base final (≤ 0,083 pp, mesmo líder, votos que nunca diminuem, total final igual).",
   REF + " (a hipótese de divergência)", ["fase3/resultados/r2_curva_publica.json"],
   "2022 2º turno: 27/27 consistentes; 2026 2º turno: 4/4; 2022 1º turno: 2/2; 2026 1º turno: 6/6.",
   "Ausência de divergência nos instantes capturados (custódia independente).", "Instantes não capturados; divergência seção a seção que preserve o total nacional.",
   "Duas formas de comparação (por seções e por horário).", "não aplicável", "Totais nacionais.", "Captura histórica com valor incompatível.", "Executado (R2)."),
]

ZER = [
 q("Q15", "Quantas seções tiveram zero votos para Flávio Bolsonaro em cada turno de 2026?", "79 no 1º turno e 106 no 2º.", DEM, ["fase3/resultados/E3_zeros.json"],
   "Universo: seções fora do exterior com votos válidos nos dois turnos (497.897). Comparação: Bolsonaro 2022, 160 e 141; Lula 2026, 8 e 4.", "A contagem.", "—", "—", "não aplicável", "Seções do Brasil.", "—", "Executado (E3)."),
 q("Q16", "Quantas tiveram comparecimento positivo e registros válidos?", "Todas: 79 e 106 com comparecimento positivo, e boletim, RDV, imagem e tabela consistentes entre si em todas.", DEM,
   ["fase3/resultados/E3_zeros.json", "fase3/resultados/bu1.json"], "Mediana de 102 e 124 votos válidos nessas seções (geral: 245 e 254); 62 e 67 municípios, concentradas em AM, PA, MA.", "Que não são seções vazias nem erros de leitura.", CONS, "—", "não aplicável", "Seções do Brasil.", "—", "Executado."),
 q("Q17", "Como essas seções mudaram entre o primeiro e o segundo turno?", "Das seções com zero em algum turno: 50 com zero nos dois, 56 passaram de votos a zero e 29 de zero a votos.", DEM,
   ["fase3/resultados/E3_zeros.json"], "2022 (Bolsonaro): 84 nos dois, 57 de votos a zero, 76 de zero a votos.", "As transições.", "Por quê.", "—", "não demonstrada", "Seções do Brasil.", "—", "Executado."),
 q("Q18", "O fenômeno é estatisticamente incomum depois de controlar tamanho, município, local e heterogeneidade?",
   "Não determinado: nenhum modelo de cauda baixa passou na calibração. O modelo do R3 (que previa 79,1 e 101,5 zeros contra 79 e 106) falhou o critério pré-registrado, então não sustenta nem excesso nem ausência de excesso; as três famílias novas do T64 também falham (por município, 1,3 zeros previstos contra 106; por local de votação, 66,7 contra 106). Descritivamente, os zeros são locais de uma só seção, com menos de 1% do total.",
   ND, ["fase3/inv_r3_zeros.py", "fase3/resultados/r3_zeros.json", "fase3/resultados/rev_i2.json", "testes/registro.json (T41, T64)", "operacao_veracidade/05_ZEROS_E_ENTRE_TURNOS.md"],
   "Intervalos de predição: [63, 98] e [88, 115]. Falhas do critério: teste de Hosmer–Lemeshow rejeita desvios mínimos nos controles grandes (dezenas de milhares de seções), razões por decil de 1,25 a 1,27 (limite 1,25) e controles de Lula com 1 a 8 zeros. O modelo anterior (I2) também falhou.",
   "Só a descrição: onde estão e que os registros conferem.", "Excesso ou ausência de excesso (nenhum modelo calibrou); ausência de excesso em seções específicas.", "Sensibilidade sem a covariável do 1º turno: mesmo resultado.", "não demonstrada",
   "Seções do Brasil; Flávio 2026.", "Modelo que passe em critério de calibração adequado a controles grandes e pequenos.", "Executado (R3); validação formal falhou.",
   reabre="Refazer o critério de calibração (controles com esperado ≥ 20; tolerância por decil adequada a n grande) antes de nova tentativa."),
 q("Q19", "O mesmo método identifica padrões semelhantes em 2022?", "Sim, com o mesmo resultado: não determinado. Bolsonaro 2022 teve 160 e 141 zeros; o modelo do R3 previa 162,9 e 136,5, mas falhou o mesmo critério formal, e no T64 o modelo por município prevê 4,3 contra 141 e o por local, 63,3 contra 141, ambos reprovados. Descritivamente, os zeros de 2022 também são locais de uma só seção, com menos de 1% do total.", ND,
   ["fase3/resultados/r3_zeros.json", "testes/registro.json (T64)"], "Intervalos do R3: [140, 187] e [118, 153] (modelo reprovado).", "Que 2026 e 2022 têm a mesma descrição e a mesma falha dos modelos.", "Excesso ou normalidade (nenhum modelo calibrou).", "—", "não demonstrada", "Bolsonaro 2022.", "Ver Q18.", "Executado (R3)."),
 q("Q20", "Existem divergências objetivas nos boletins ou apenas resultados numéricos extremos?", "Apenas resultados numéricos extremos: 0 divergências de votos entre boletim, RDV, imagem e tabela nas 486 seções-turno com zero votos para um finalista.", DEM,
   ["fase3/resultados/E3_zeros.json", "fase3/resultados/bu1.json"], "2026: 185; 2022: 301 (incluindo a seção do Sistema de Apuração verificada no BU1).", "Ausência de divergência documental nessas seções.", CONS, "—", "não aplicável", "Seções com zero.", "Boletim impresso de terceiro diferente.", "Executado."),
]

TUR = [
 q("Q21", "Quantos votos cada finalista ganhou ou perdeu entre os turnos?", "2022: Lula +3.086.495, Bolsonaro +7.134.009. 2026: Lula +10.376.694, Flávio +3.721.538 (base por seção, com exterior).", DEM,
   ["fase3/resultados/entre_turnos_contas.json"], "1º → 2º turno, 2022: Lula 57.259.504 → 60.345.999; Bolsonaro 51.072.345 → 58.206.354. 2026: Lula 53.879.538 → 64.256.232; Flávio 56.104.503 → 59.826.041.",
   "As variações.", "Quem mudou de voto.", "Soma das urnas = total oficial (T32).", "não aplicável", "Brasil e exterior.", "—", "Executado.", {"2022": "Lula +3,09 mi; Bolsonaro +7,13 mi.", "2026": "Lula +10,38 mi; Flávio +3,72 mi."}),
 q("Q22", "Quanto da mudança corresponde a comparecimento, votos dos eliminados, brancos e nulos?",
   "Toda a mudança fecha exatamente: ganho dos finalistas = votos dos eliminados no 1º turno + variação do comparecimento − variação de brancos e nulos.", DEM, ["fase3/resultados/entre_turnos_contas.json"],
   "2022: 10.220.504 = 9.897.870 + 570.424 − 247.790. 2026: 14.098.232 = 9.321.993 + 2.960.239 + 1.816.000 (brancos e nulos caíram 1,82 mi).",
   "A identidade contábil.", "A divisão dos eliminados entre os finalistas (ver Q24).", "—", "não aplicável", "Totais.", "—", "Executado."),
 q("Q23", "Existem diferenças impossíveis de reconciliar com os totais oficiais?", "Não: as contas fecham nacionalmente e nenhuma seção tem mais votos que comparecimento ou mais comparecimento que aptos.", REF + " (a hipótese de diferença impossível)",
   ["fase3/resultados/entre_turnos_contas.json", "testes/registro.json (T32)"], "0 seções inconsistentes; 638/638 itens iguais ao total oficial.", "Ausência de impossibilidade contábil.", "Que os números reflitam os votos dados (ver integridade).", "—", "não aplicável", "Todas as seções.", "Seção com contagem impossível.", "Executado."),
 q("Q24", "Quais fluxos entre escolhas são matematicamente possíveis?", "Um intervalo amplo: os dados agregados admitem desde fluxos quase nulos até milhões de votos em cada direção; só limites, não um fluxo.", PAR,
   ["fase2/resultados/P13.json", "fase2/resultados/P15.json", "fase2/sessao_limitada_2026-10-28/p1_resultado_principal.json"],
   "2026: trocas diretas entre finalistas com mínimo garantido de 79 (Flávio → Lula) e 123 (Lula → Flávio) votos e máximos de 43,5 mi e 39,4 mi; abstencionistas para Lula entre 4.116 e 32,3 mi (Fréchet). O estimador C06 dá razão ~4:1 entre abstencionistas, frágil (1,7 a 11,8 sob heterogeneidade).",
   "Os limites matemáticos.", "Qual fluxo ocorreu.", "Sensibilidade do C06 sob heterogeneidade sintética.", "não aplicável", "Seções do Brasil.", "—", "Executado (F2)."),
 q("Q25", "O padrão territorial de crescimento apresenta desvios persistentes após controles?",
   "Sim, em parte: a assimetria de cauda do T02 é real nos dois anos; cerca de 0,1% dos locais são atípicos (lista depende do método); há dependência espacial entre municípios; em São Paulo 2022 a zona 251 mantém desvio depois de controlar o perfil do eleitorado; em 2026, Salvador tem virada de Lula ~30 mil votos acima do previsto pelo histórico, em todas as 19 zonas (T44), a única entre as 27 capitais e não explicada pelo perfil do eleitorado; Fortaleza tem desvio de tamanho parecido no sentido oposto.",
   PAR, ["fase2/resultados/P17.json", "fase3/resultados/rev_i3.json", "fase3/resultados/p19.json", "fase3/inv_r4_zona251.py", "fase3/resultados/r4_zona251.json", "fase3/teste_grandes_cidades.py", "fase3/resultados/teste_grandes_cidades.json"],
   "Zona 251: desvio de 0,58 z cai para 0,42 (IC 95% 0,23 a 0,62; 26% explicado) com escolaridade, idade, sexo e estado civil; sensibilidade 0,37 (36%). Zona 259: explicado em parte. Moran's I 0,16 a 0,20. Locais: 61 (2026) e 84 (2022) contra o entorno.",
   "Que há desvios territoriais persistentes, inclusive na zona 251 depois do perfil.", "A causa; que sejam irregularidades.", "R² do perfil 0,02; sensibilidade com todas as zonas.", "não demonstrada",
   "Brasil; SP capital para a zona 251.", "Covariáveis de campanha, renda, migração; dados externos da zona.", "Executado (R4, I3, P17, P19)."),
 q("Q26", "É possível demonstrar transferência individual entre candidatos com os dados existentes?", "Não. Com dados agregados e voto secreto, transferências individuais não são identificáveis; só os limites de Q24.", DEM + " (a impossibilidade)",
   ["fase2/resultados/P15.json"], "Limites de Fréchet: razão entre abstencionistas de ~0 a 1,7 mi.", "A não identificabilidade com estes dados.", "—", "—", "não aplicável", "—", "Só dados individuais (inexistentes por sigilo).", "Encerrada no escopo."),
]

# O que cada resposta significa em número de votos. Referências: margem do 2º turno de 2026 = 4.430.191 votos (Lula 64.256.232 ×
# Flávio 59.826.041); de 2022 = 2.139.645 (Lula 60.345.999 × Bolsonaro 58.206.354). Inverter 2026 exigiria trocar ~2,22 mi votos de lado.
MARGEM = "Margem do 2º turno: 4.430.191 votos em 2026 e 2.139.645 em 2022."
EMV = {
 "Q1": "0 voto de diferença entre a tabela e os boletins em todos os ~128 milhões de votos de 2026 (2º turno) e ~124 milhões de 2022 conferidos. As 5 seções de 2022 sem arquivo somam 5 votos de comparecimento.",
 "Q2": "0 voto de diferença entre a recontagem pelo RDV e a tabela, nos dois anos.",
 "Q3": "Nenhuma divergência muda um voto da tabela. Divergências de registro: 2022, 5.287 votos sem registro no log publicado e 2.503 a mais no log (0,25% e 0,12% da margem de 2022); RS 88013/2/199, 92 votos entre a imagem do boletim (196) e o boletim digital (288); 2026, 113 votos em 16 seções-turno do T36 (0,003% da margem).",
 "Q4": "Seções com arquivos ausentes: 64 seções com 21.112 comparecimentos em 2022 (boletim presente e igual à tabela); o Sistema de Apuração soma 27.692 votos em 2022 e as seções de 2026 também conferem; as 5 seções sem arquivo somam 5 votos.",
 "Q5": "Alcança todos os votos: nenhum voto, de 2022 ou 2026, tem a assinatura verificada até a raiz do TSE; todos estão verificados até a AC emissora (100% das urnas, verificação completa em 28/10/2026, T60a).",
 "Q6": "Nas 404 seções com boletim de terceiro, 0 voto de diferença. Na captura final de cada eleição, 0 voto de diferença entre o total divulgado ao vivo e a base. A maior diferença em capturas parciais equivale a ~1,7 mil a ~3 mil votos naquele instante (seções com o mesmo horário de recebimento ordenadas de forma diferente), e não muda o líder.",
 "Q7": "Detectado nos cenários simulados: ~123 mil votos dispersos (2,8% da margem de 2026) e ~62 mil concentrados (1,4%). Não detectado: ~25 mil (0,6%). No município inteiro de uma grande cidade, a bateria original falha até ~696 mil votos, mas o teste T44 vê a partir de 31 mil a 139 mil (2% dos válidos). No T63, UFs, região, lote e deslocamento uniforme passam sem alarme até ~0,5 a 2,2 mi votos, ou sempre (uniforme em logit). Inverter 2026 exigiria trocar ~2,22 mi votos de lado.",
 "Q8": "A ordem de apuração não muda nenhum voto: a mesma soma final em qualquer ordem. A virada do 2º turno de 2022 ocorreu com 67,6% das urnas; a de 2026, com 47,2%.",
 "Q9": "Idem: a sequência divulgada é a soma parcial dos mesmos votos; 0 voto de diferença no total final.",
 "Q10": "Não se traduz em votos: trata da ordem de chegada, não do total.",
 "Q11": "Não se traduz em votos: forma da curva.",
 "Q12": "Não se traduz em votos: forma da curva.",
 "Q13": "Não se traduz em votos: comparação da forma das curvas.",
 "Q14": "0 voto de diferença entre a sequência divulgada e a base nas capturas finais.",
 "Q15": "Nas 79 seções do 1º turno, 9.542 votos foram para Lula; nas 106 do 2º turno, 14.860 (todos os válidos dessas seções). São 0,34% da margem de 2026.",
 "Q16": "Os votos dessas seções conferem nos registros: 0 voto de diferença.",
 "Q17": "Não se traduz em votos: transições entre turnos.",
 "Q18": "Se os zeros fossem anomalia, os votos em jogo seriam os que o candidato teria nessas seções: de ~44 a ~4.800 votos conforme o modelo (2026, 2º turno), no máximo 0,11% da margem de 4,43 mi.",
 "Q19": "2022: de ~66 a ~4.300 votos esperados para Bolsonaro nessas seções, no máximo 0,2% da margem de 2,14 mi.",
 "Q20": "0 voto de diferença nos registros dessas seções.",
 "Q21": "2022: Lula +3,09 mi, Bolsonaro +7,13 mi. 2026: Lula +10,38 mi, Flávio +3,72 mi.",
 "Q22": "2026: os finalistas somaram +14,10 mi = 9,32 mi dos eliminados + 2,96 mi de comparecimento + 1,82 mi de brancos e nulos a menos. 2022: +10,22 mi = 9,90 mi + 0,57 mi − 0,25 mi.",
 "Q23": "0 voto inconsistente: nenhuma seção com mais votos que comparecimento.",
 "Q24": "Trocas diretas entre finalistas em 2026: mínimo garantido de 79 e 123 votos, máximo de 43,5 mi e 39,4 mi; abstencionistas para Lula entre 4.116 e 32,3 mi. A razão do C06 erra de ±0,5 a ±1,5 mi votos.",
 "Q25": "Salvador 2026: ~30 mil votos de Lula acima do previsto (0,7% da margem de 2026). Zona 251 (SP, 2022): ~4,2 mil votos de Lula acima da virada mediana da capital (0,2% da margem de 2022); zona 259: ~6,2 mil. Cauda pró-Lula do T02: ~740 votos (2026) e ~2.600 (2022). Cada local atípico: dezenas a poucas centenas de votos.",
 "Q26": "Não se traduz em votos: limite de identificabilidade (os limites estão na Q24).",
}
EMV_INV = {"P1": "Erro de ±0,5 a ±1,5 mi votos na razão estimada.", "P2": EMV["Q7"], "P3": "0 voto de diferença entre os canais comparados.", "P4": EMV["Q6"],
 "P5": "Maior efeito +0,004 logit, ~2,7 mil votos se fosse real.", "P6": "0 voto de diferença nas 404 seções com boletim impresso de terceiro (amostra de conveniência, 0,08%).", "P7": "Diferença de −0,029 z, desprezível; não convertida em votos.", "P8": "Efeito desprezível.",
 "P9": "Cada local atípico: dezenas a poucas centenas de votos.", "P10": "99 votos nos últimos 30 min das 8 urnas (2026, 1º turno).", "P11": EMV["Q5"],
 "P12": "Eleitores aptos do exterior (−495 e −525), não votos.", "P13": EMV["Q24"], "P14": EMV["Q25"], "P15": "Abstencionistas para Lula entre 4.116 e 32,3 mi votos.",
 "P16": "0 voto de diferença nas 200 seções.", "P17": "~740 votos (2026) e ~2.600 (2022) na cauda pró-Lula.", "P18": EMV["Q7"], "P19": "Não se traduz em votos.",
 "P20": EMV["Q25"], "P21": EMV["Q6"], "R1-20": "0 voto de diferença nas seções comuns (~119 mi em 2026, 1º turno; ~118 mi por turno em 2022).",
 "C1": EMV["Q10"], "C1a": EMV["Q8"], "C1b": EMV["Q11"], "C2": EMV["Q13"], "M1": EMV["Q22"], "Z1": EMV["Q18"], "MET": EMV["Q7"],
 "AUT": EMV["Q1"] + " " + EMV["Q5"], "A173": "64 seções com 21.112 comparecimentos; votos do boletim iguais à tabela.", "BU1": "16 votos, iguais à tabela.", "SA22": "27.692 votos, iguais à tabela."}
for lista in (INT, CUR, ZER, TUR):
    for p in lista: p["em_votos"] = EMV[p["id"]]
# 33 itens do inventário: resposta direta + classificação + ligação com as perguntas acima
INV = {
 "P1": ("O estimador de fluxos C06 recupera a verdade? Em parte: a ordem dos fluxos e o contraste com 2022 resistem; a magnitude '4:1' não (erro de ±0,5 a ±1,5 mi votos).", PAR, ["Q24"]),
 "P2": ("A bateria detecta trocas de votos? Só nos cenários e tamanhos da Q7.", PAR, ["Q7"]),
 "P3": ("As inconsistências dependem de canal e versão? Nos canais comparados (tabela, BU, decodificação de terceiro, divulgação ao vivo) não há inconsistência de votos; versões datadas dos arquivos não existem localmente.", PAR, ["Q1", "Q4", "Q6", "Q14"]),
 "P4": ("A curva pública pode ser reconstruída pelos boletins recebidos? Sim, nos 39 instantes capturados: a recomposição pela ordem de recebimento reproduz o total divulgado (≤ 0,083 pp), sem defasagem.", DEM, ["Q9", "Q11", "Q14"]),
 "P5": ("O modelo de urna afeta a virada? Não, dentro de ±0,02 logit (2º turno, municípios com 2 ou mais modelos).", DEM, []),
 "P6": ("Boletins de terceiros validam os arquivos? Em parte: 404 boletins impressos lidos por terceiros no 2º turno de 2026 (22 UFs) são iguais à tabela e ao BU do TSE, com assinatura e cadeia válidas (T61); é amostra de conveniência, não sorteada; de 2022 não há.", PARC404, ["Q6", "Q45"]),
 "P7": ("A urna trocada vota diferente? Não, equivalente na margem de ±0,10 z fixada antes.", DEM, []),
 "P8": ("A virada depende da ordem de chegada? Efeito desprezível (|r| ≤ 0,05); em 2022, −0,028, diferente de zero.", DEM, []),
 "P9": ("Os locais atípicos do E02 resistem? Cerca de 0,1% dos locais, em três métodos; a lista depende do método; causa não demonstrada.", PAR, ["Q25"]),
 "P10": ("A rajada sem biometria do T28 resiste? 8 urnas do 1º turno de 2026 seguem sinalizadas pelo critério beta-binomial (99 votos); em 2022 o mesmo critério sinaliza 18 e 21 urnas (23 e 25 pelo T28 original).", DEM, []),
 "P11": ("Os certificados se ligam a uma âncora do TSE? Não foi possível determinar: válidos até a AC emissora em 100% das urnas (T60a); raiz não obtida.", ND, ["Q5", "Q43"]),
 "P12": ("Diferença do eleitorado do exterior? Explicada: 423 de seções não instaladas + 72 + 30 de seções só nos arquivos de urna.", DEM, []),
 "P13": ("O C06b é reproduzível? Sim: 79 e 123 reproduzidos.", DEM, ["Q24"]),
 "P14": ("Qual a causa da assimetria do T02 em 2022? Não demonstrada; o desvio está no nível da zona (251, 259) e persiste na 251 depois do perfil do eleitorado.", PAR, ["Q25"]),
 "P15": ("Os limites de Fréchet estreitam a razão? Não: a razão não é identificada.", DEM, ["Q24", "Q26"]),
 "P16": ("200 seções conferem? Sim, 200/200 no 1º turno de 2026 (consistência interna); o 2º turno é coberto pelo T17b e pelo R1.", DEM, ["Q1", "Q2"]),
 "P17": ("A assimetria de cauda do T02 é real? Sim, nos dois anos.", DEM, ["Q25"]),
 "P18": ("O T13 bilateral vê os dois sentidos? Sim, para troca dispersa; limites na Q7.", PAR, ["Q7"]),
 "P19": ("Há dependência espacial entre municípios? Sim, Moran's I 0,16 a 0,20; causa não distinguida.", DEM, ["Q25"]),
 "P20": ("O que há nos locais de SP 2022? Desvio no nível da zona, que persiste na 251 após o perfil; arquivos conferem; causa não demonstrada.", PAR, ["Q25"]),
 "P21": ("Fontes externas e cadeia autenticada confirmam os arquivos? Em parte: no agregado nacional ao vivo e em 404 boletins impressos de terceiros iguais ao TSE (Q6, T61; amostra de conveniência); a cadeia fecha até a AC emissora em 100% das urnas (T60a), mas a raiz não foi obtida.", PARC404, ["Q5", "Q6", "Q45"]),
 "R1-20": ("A base coincide com decodificação independente? Sim, nas seções comuns (99,96% em 2022, 100% em 2026 1º turno); o 2º turno de 2026 não tem comparação de terceiro.", PAR, ["Q1"]),
 "C1": ("As curvas são compatíveis com processos plausíveis de chegada? Não determinado (nenhum modelo de chegada validado). A curva divulgada é reproduzível com os dados por seção.", ND, ["Q10", "Q11", "Q12"]),
 "C1a": ("Quando ocorreram as viradas? Ver Q8 e Q9.", DEM, ["Q8", "Q9"]),
 "C1b": ("Há periodicidade ou trechos lineares anômalos? Não determinado.", ND, ["Q11", "Q12"]),
 "C2": ("2022 e 2026 têm as mesmas características? Diferem na descrição; semelhança estatística não determinada.", ND, ["Q13"]),
 "M1": ("O crescimento entre turnos é reconciliável? Sim, contabilmente (identidade exata); fluxos individuais não identificáveis.", PAR, ["Q21", "Q22", "Q23", "Q24", "Q26"]),
 "Z1": ("Os zeros indicam anomalia? Sem divergência documental; não determinado: nenhum modelo de cauda baixa calibrou (R3 e T64); descritivamente, são locais de uma só seção, com menos de 1% do total.", ND, ["Q15", "Q16", "Q17", "Q18", "Q19", "Q20"]),
 "MET": ("Os métodos resistem à revisão? Com limites registrados: T10/T11 descritivos; T02 cego a município inteiro; E02 dependente do método; zeros sem modelo validado; concordância entre registros é consistência interna.", PAR, ["Q7"]),
 "AUT": ("Os arquivos são autênticos? Íntegros e assinados até a AC emissora; consistentes entre si; a autenticidade integral do processo não é verificável com dados públicos.", PAR, ["Q1", "Q2", "Q3", "Q5", "Q6"]),
 "A173": ("Os 173 arquivos estão ausentes da publicação? Sim, do pacote de dados abertos (duas cópias); conteúdo não verificado; outro canal do TSE inacessível.", PAR, ["Q4"]),
 "BU1": ("A seção com BU não lido concorda? Sim (boletim do Sistema de Apuração, assinatura válida; consistência interna).", DEM, ["Q20"]),
 "SA22": ("As 159 seções do Sistema de Apuração de 2022 conferem? Sim, 159/159 (consistência interna).", DEM, ["Q1"]),
}

# Alegações públicas (live, imprensa, X) testadas com pré-registro; origem não é fonte. em_votos vai direto no item.
LIVE = ["fase3/PREREG_LIVE_2022.md", "fase3/live_2022.py", "fase3/resultados/live_2022.json", "docs/pesquisas/2026-10-28_live_cerimedo_2022.md"]
ARV = ["fase3/PREREG_POSTS_ARVOR.md", "fase3/posts_arvor.py", "fase3/resultados/posts_arvor.json"]
ALE = [
 q("Q27", "A live de 4/11/2022 dizia que urnas anteriores a 2020 deram mais votos a Lula. Isso é verdade?",
   "A diferença existe, mas é de lugar, não de urna: no 1º turno de 2022 Lula teve 50,3% nas antigas e 46,0% nas UE2020, e a diferença persiste dentro do município; comparando urnas do mesmo local de votação, ela some (equivalente a zero em ±0,02 logit nos dois turnos).",
   DEM, LIVE, "Conta da live (eleitorado < 77 mil): 54,5% × 52,3%, antigas maiores em 18 de 23 UFs. Dentro do município: +0,031 × −0,035 logit (fora da margem). Dentro do local: +0,008 [−0,002; 0,017] × −0,008. Calibração por permutação 0% fora; fraude sintética de 1% detectada.",
   "Que o modelo de urna não muda o voto quando se compara o mesmo lugar.", "A causa da distribuição desigual dos modelos.", "Calibração e poder medidos; placebo de 2018 não rodado.", "verificável: localização", "2022, Brasil.", "Diferença persistente dentro do local de votação.", "T47 (pré-registrado, emenda 7); P5/T20."),
 q("Q28", "O log das urnas antigas não identifica a urna, como alegou o PL em 2022?",
   "O bug existe: nas 279.291 seções com urnas UE2009 a UE2015 o campo de identificação do log traz o valor fixo 67305985. Mas o log se liga ao boletim e ao RDV pela assinatura da urna e pelo número do certificado em 279.285 delas; as 6 restantes são trocas de urna e arquivos faltantes já catalogados. Em 2026 o bug não aparece.",
   DEM, LIVE, "2º turno de 2022: 279.291 com ID fixo; 279.285 com assinaturas válidas, certificado = urna efetivada e BU = RDV = tabela. 2026: 0 com ID fixo.",
   "Que o log se liga ao BU apesar do bug.", CONS, "Correção única de artefato do comparador (ausente = 0).", "não aplicável", "2022 e 2026, dois turnos.", "Seção com ID fixo sem ligação e sem explicação.", "T45 (emenda 7)."),
 q("Q29", "Contando só as urnas UE2020, Bolsonaro teria vencido 2022 com 51,05%?",
   "A conta está certa (51,0508%), mas mede o voto das cidades que tinham UE2020, não o efeito do modelo: 220 mil seções com urnas antigas estavam em municípios sem nenhuma UE2020. Comparando dentro do mesmo município, Lula continua vencendo (Bolsonaro 49,25%).",
   DEM, LIVE, "Só UE2020: Bolsonaro 26.189.721 × Lula 25.111.550. Contrafactual em 311 municípios com os dois grupos.",
   "Que o 51,05% é efeito de seleção geográfica.", "O voto de quem não votou em UE2020.", "—", "verificável: localização", "2º turno de 2022.", "Contrafactual dentro do município invertendo o resultado.", "T46 (emenda 7)."),
 q("Q30", "Em 2022 havia dois softwares diferentes ou unanimidades ligadas ao modelo de urna?",
   "Não: a mesma versão 8.26.0.0 em todas as seções de todos os modelos; as seções 100% de um candidato aparecem em cada modelo na proporção da sua presença nos mesmos municípios.",
   DEM, LIVE, "141 seções 100% Lula no 2º turno (16.418 votos), 4 de Bolsonaro; UE2015 49 × 40,7 esperadas, UE2010 37 × 39,0, UE2020 11 × 13,0. 1 seção (SC) com versão antiga a mais no log.",
   "Software único segundo o log; unanimidade sem relação com modelo.", "Versão lida do próprio log (compatível com o registro).", "—", "não aplicável", "2022.", "Versão diferente por modelo.", "T48 (emenda 7)."),
 q("Q31", "Flávio teve zero voto em 106 urnas no 2º turno de 2026. Isso é anormal?",
   "O número está certo (106 seções, 14.860 votos de Lula), e não há sinal de ruptura nem de erro de registro: em 2022 foram 141 seções com Bolsonaro zerado; são aldeias e comunidades do Norte e do Nordeste que já votavam quase só em Lula em 2022 (nenhuma com Bolsonaro acima de 11%) e no 1º turno; os 106 boletins conferem com o RDV e têm assinaturas válidas. Se o número é estatisticamente excepcional não foi determinado: nenhum modelo de cauda baixa calibrou (Q18, T64).",
   DEM, ["fase3/PREREG_ZEROS_FLAVIO.md", "fase3/zeros_flavio.py", "fase3/resultados/zeros_flavio.json"],
   "Norte 65, Nordeste 29, Centro-Oeste 6, Sudeste 3, Sul 3; 23 também zeradas em 2022; 50 com Flávio zerado no 1º turno. 211 municípios viraram para Lula; em 2022, 251 viraram para Bolsonaro. O '644 mil' no Rio não se reproduz (cidade: Lula +113 mil).",
   "Continuidade e integridade das seções.", CONS, "—", "não aplicável", "2º turno de 2026 e 2022.", "Seção zerada sem histórico ou com divergência de arquivo.", "T49 (emenda 8); Q15, Q20."),
 q("Q32", "O voto de Lula ficou mais concentrado em seções de mais de 80%?",
   "Não, ficou menos: 35.591 seções com Lula acima de 80% em 2026, contra 40.046 em 2022; o saldo vindo dessas seções caiu de 6,19 mi para 5,56 mi. Os números da thread que levantou a pergunta se reproduzem.",
   DEM, ["fase3/PREREG_THREAD_CONCENTRACAO.md", "fase3/thread_concentracao.py", "fase3/resultados/thread_concentracao.json"],
   "95,6% delas no Norte e Nordeste; 82% já acima de 80% em 2022; Lula venceu 250.108 seções, +19,28 mi; Flávio +14,88 mi; saldo 4,40 mi (4,43 mi com exterior).",
   "As contagens.", "Fraude ou ausência dela (descritivo).", "—", "não aplicável", "2º turno, 2022 e 2026.", "—", "T50 (emenda 9)."),
 q("Q33", "Lula cresceu mais que Flávio em 93% dos municípios e em todos os estados. Isso é estatisticamente impossível?",
   "Não: em 2022 Bolsonaro cresceu mais que Lula em 87,1% dos municípios e no agregado das 27 UFs; em proporção, 2022 foi até mais uniforme (98,0% dos municípios contra 97,1%). Crescimento quase universal do candidato que avança é o padrão do 2º turno. Em 2026 o candidato de trás precisava de 1,02 ponto e cresceu 2,80; em 2022 precisava de 2,85 e cresceu 1,95.",
   DEM, ["fase3/PREREG_CRESCIMENTO_ENTRE_TURNOS.md", "fase3/crescimento_turnos.py", "fase3/resultados/crescimento_turnos.json"],
   "2026: 5.228 de 5.571 municípios. 2022: 4.849 de 5.570 (Ceará é a única UF em que a maioria dos municípios foi para Lula).",
   "Que a uniformidade se repete em 2022.", "Anos anteriores a 2022 (sem dados no projeto).", "—", "não aplicável", "2022 e 2026.", "Uniformidade só em 2026.", "T51 (emenda 10); Q21, Q22."),
 q("Q34", "Os boletins ficaram parados duas horas antes de chegar ao TSE no 2º turno de 2026?",
   "Sim: o recebimento parou às 17:07 e voltou às 19:03 (116 minutos), só em 2026; voltou junto com o fechamento das urnas prorrogadas (99% fecharam até 19:10). Isso não muda votos: o boletim é assinado pela urna na emissão (mediana 17:03) e confere com a tabela e o RDV. A causa administrativa da pausa não está nos dados.",
   PAR, ARV, "2026: recebimento mediano 20:26 (2022: 18:26); 1.092 BUs antes das 19h (0,22%); 7.604 urnas prorrogadas; 34.327 votos depois das 17h (2022: 41.025).",
   "O vazio e a coincidência com o fim da prorrogação.", "Quem decidiu a pausa e por quê.", "Fuso de cada campo decidido pelos dados.", "compatível com suspensão durante a prorrogação", "2º turno, Brasil.", "Documento do TSE sobre a recepção; BU recebido diferente do emitido.", "T52 (emenda 11); T09, T16, Q1."),
 q("Q35", "Há fortes evidências de votos sem biometria em 2026?",
   "Não no agregado: a liberação pelo código do mesário caiu de 8,1% (2022) para 6,8% (2026), e dentro do município, onde ela foi maior, Lula virou um pouco menos (correlação −0,058; em 2022, +0,056). Com o perfil do eleitorado o efeito é nulo (T12). Há 8 urnas com rajada sem biometria no fim do dia (99 votos), padrão também presente em 2022 (T28/P10).",
   DEM, ARV + ["fase2/resultados/P10.json"], "Biometria 87,6% em 2026 contra 75,9% em 2022; 8,63 mi liberações pelo mesário contra 10,01 mi.",
   "Que a liberação sem biometria não favorece Lula no agregado.", "Quem foi cada eleitor liberado (só ata e caderno).", "T12 com perfil; T28 com 2022.", "não aplicável", "2º turno, 2022 e 2026.", "Relação positiva e forte com a virada depois do perfil.", "T53 (emenda 11); T12, T28, P10."),
 q("Q36", "Flávio teve menos votos no 2º turno do que no 1º em 938 municípios. Isso é anormal?",
   "Não: em 2022 aconteceu o espelho, de tamanho parecido; Lula perdeu votos em 981 municípios (114.916 votos) enquanto Bolsonaro ganhava 236.690 neles. O candidato que perde fôlego no 2º turno perde votos em cerca de mil municípios.",
   DEM, ARV, "2026: 937 municípios, 133.852 votos, 13,40 mi de aptos; Lula +486.832 neles; comparecimento caiu em 727. Lula perdeu em 79 (16.115).",
   "Que o padrão se repete em 2022.", "Quem trocou de voto (Q26).", "—", "não aplicável", "2022 e 2026.", "Padrão só em 2026.", "T54 (emenda 11); Q22, Q24."),
 q("Q37", "E o grupo atípico do algoritmo de mistura gaussiana, a totalização paralela e as pesquisas?",
   "O grupo atípico (10.850 seções) não foi reproduzido aqui, mas o próprio dossiê que o criou mede que a fatia de Flávio nele não mudou (−0,05 ponto, IC −0,19 a +0,07) e que ele não se liga a região nem a modelo; nossos testes de locais atípicos (E02/I3) acham ~0,1% de locais sem causa demonstrada. A totalização paralela tem 286 boletins iguais ao TSE, como os nossos 0 de diferença; a amostra é de voluntários e o placar dela não estima nada. Pesquisas ficam fora do escopo (não são dado oficial).",
   PAR, ["fase3/PREREG_POSTS_ARVOR.md", "fase2/resultados/P17.json", "fase3/resultados/rev_i3.json"], "Grupo atípico: 2,18% das seções, V de Cramér 0,044 (região) e 0,012 (modelo), segundo o autor.",
   "Que nenhuma das três alegações aponta divergência nos dados.", "O modelo de mistura do autor (não rodado aqui).", "—", "não aplicável", "2º turno de 2026.", "Grupo com deslocamento de voto fora do intervalo; boletim de terceiro diferente.", "Respondida com testes existentes (E02, I3, Q1, T39)."),
 q("Q38", "Cabo Frio, onde Lula ganhou 50 votos para cada 1 de Flávio no 2º turno, é estatisticamente impossível?",
   "Não. Os números estão certos (Lula +9.169, Flávio +342), mas cabem exatamente nos votos que estavam disponíveis: 8.822 dos candidatos eliminados no 1º turno mais 1.229 de brancos e nulos a menos, menos 540 de comparecimento (9.511). Lula ficou com 96% disso; 11% dos municípios do país tiveram fração igual ou maior. Em 2022 houve 28 municípios fortemente de Lula em que Bolsonaro levou mais de 90% do ganho.",
   DEM, ["fase3/PREREG_CABO_FRIO.md", "fase3/cabo_frio.py", "fase3/resultados/cabo_frio.json"],
   "Nenhum dos 5.571 municípios ganhou mais que o disponível. Campos: Lula +24.822, Flávio −1.389 (percentil 95). São Gonçalo: +45.217 × +8.156. Santana de Parnaíba: +9.244 × +4.825. 4.044 de 4.044 seções dessas cidades com arquivos íntegros.",
   "Que o resultado é aritmeticamente possível e não é único.", "Quem eram os eleitores dos eliminados (Q26).", "—", "não aplicável", "Municípios, 2022 e 2026.", "Ganho acima do disponível ou divergência de arquivo.", "T55 (emenda 12); Q22, Q26."),
 q("Q39", "Os brancos e nulos do 1º turno foram quase todos para Lula em 2026? Isso é uma anomalia?",
   "Não é anomalia, e a maior parte tem causa medida. O estimador de fluxos aponta essa direção (cerca de 62% para Lula), mas a leitura do número digitado em cada nulo (Q40) mostra o mecanismo: no 1º turno de 2026, onde Lula é forte, sobrou nulo de presidente porque muita gente digitou o número do governador no campo de presidente (erro de campo); no 2º turno, sem governador na maioria dos estados, essas pessoas votaram normalmente. E em 2022 metade do eleitorado tinha 2º turno de governador, que gera esse mesmo erro, contra 8% em 2026. Sobra uma queda pequena e uniforme (~0,6 ponto). A magnitude dos fluxos estimados deve ser lida só como direção (Q41).",
   DEM, ["fase3/resultados/brancos_nulos.json", "fase3/resultados/nulos_governador.json", "fase3/resultados/rdv_nulos_analise.json"],
   "Totais: 2022, 5.452.653 → 5.700.443; 2026, 5.969.801 → 4.153.801. Nulos com número de governador no 1º turno: 697.773 (2026) × 422.104 (2022); excesso por quintil de Lula só nessa classe (+0,08 a +0,45 ponto). 2º turno com governador: 1,18 ponto (2026) e 0,97 (2022) dos votos.",
   "O mecanismo (erro de campo) e a composição de UFs com governador.", "Em quem a pessoa queria votar.", "Leitura de todos os RDVs, conferida voto a voto com o leitor original.", "verificável: erro de campo e 2º turno de governador", "Brasil, 2022 e 2026.", "Resíduo concentrado onde Lula é forte depois do erro de campo.", "T56, T57, T58 (emendas 13 a 15); C06, Q22, Q26."),
 q("Q40", "O que os eleitores digitaram nos votos nulos para presidente?",
   "Mais da metade digitou '00'. Uma parte grande digitou o número de um candidato a governador do próprio estado: 698 mil no 1º turno de 2026 (422 mil em 2022). No 2º turno, onde havia governador, cerca de 1 em cada 100 eleitores fez isso, o que explica todo o excesso de nulos desses estados. No 2º turno de 2026, 246 mil digitaram o número de um candidato a presidente já eliminado, 143 mil deles o 14 do Renan.",
   DEM, ["fase3/PREREG_RDV_NULOS.md", "fase3/rdv_nulos.py", "fase3/rdv_nulos_analise.py", "fase3/resultados/rdv_nulos_analise.json"],
   "Nulos de presidente: 2022, 3,49 mi e 3,93 mi; 2026, 3,67 mi e 2,72 mi. Mais digitados no 1º turno de 2026: 00, 10, 15, 11, 12; no 2º: 00, 11, 14, 12, 99.",
   "Os números digitados, voto a voto, conferidos com a contagem dos boletins.", "A intenção do eleitor.", "0 diferenças contra o leitor original nos 4 conjuntos.", "não aplicável", "Todas as seções, 2022 e 2026.", "—", "T58 (emenda 15)."),
 q("Q41", "O estimador de fluxos de votos (para onde foi cada eleitor) acerta quando a origem é conhecida?",
   "Em parte. Quem digitou 14 no 2º turno de 2026 quase certamente votou no Renan no 1º; o estimador atribui 90% desses votos ao Renan, e 69% dos que digitaram 70 ao Cury. Mas erra outros casos (55 em 2026; 12 e 15 em 2022). Pela regra fixada antes, os números de fluxo (por exemplo, '62% dos brancos e nulos para Lula') valem só como direção, não como tamanho.",
   PAR, ["fase3/PREREG_RDV_NULOS.md", "fase3/resultados/rdv_nulos_analise.json", "analise/resultado_comportamento_2026.json"],
   "Fração atribuída à origem certa: 14 → 90% (22 de 27 UFs), 70 → 69% (15), 55 → 20%, 12 → 9%, 15 → 13%.",
   "O desempenho do estimador com dado real.", "Qual fluxo ocorreu (Q26).", "Mesma implementação do C06; destinos com número também de governador são menos limpos.", "não aplicável", "2º turno, 2022 e 2026.", "Calibração com destinos mais limpos.", "T59 (emenda 15); C06, T37, Q24."),
 q('Q51', 'A eleição de 2026 teve duas eleições no mesmo dia, uma vencida por Flávio até as 17h00 e outra por Lula depois, na prorrogação?', "Os números do relatório se reproduzem, mas a divisão não separa o que ele diz. Em hora local, até 17:00:59 Flávio teve 52,39% e 1,75 mi de frente (150.771 seções), e depois Lula teve +6,18 mi. Só que 98% das seções fecham até 17:15 (mediana 17:01), e o grupo 'depois das 17h00' inclui 339.593 seções de encerramento de rotina (88 mi de votantes). Com o corte em 17:02:59, Lula já lidera o grupo de antes (+0,82 mi). As 32.025 seções encerradas antes das 17h00 locais estão em MT, AM, MS, RO, AC e RR, onde o horário legal local é 16h ou 15h, as 17h de Brasília; em hora de Brasília, até 17:00:59 Flávio tem 50,99% e 0,61 mi de frente. A prorrogação de fato (depois das 17:30: 7.604 seções, 2,21 mi de votantes) deu a Lula +228 mil, 5% da margem; sem elas, Lula lidera por 4,20 mi. Dentro do mesmo município, seções que fecharam depois e antes diferem em 0,2 ponto.", REF, ['fase3/PREREG_RELATORIO_PERICIAL.md', 'fase3/relatorio_pericial.py', 'fase3/relatorio_pericial_r2b.py', 'fase3/resultados/relatorio_pericial.json', 'fase3/resultados/relatorio_pericial_r2b.json'], 'Reproduzido: 150.771 seções (até 17:00:59), 339.593 (17:01 a 17:15), 2.472 (17:16 a 18:59); sensibilidade do corte de 17:00:59 a 19:00:00; em hora de Brasília, até 17:00:59: 125.652 seções, Flávio 50,99%.', 'Que os números do relatório se reproduzem, que o resultado depende do minuto do corte e do relógio usado, e o tamanho real da prorrogação em votos.', 'Decisões judiciais, reações internacionais e fiscalização partidária citadas no relatório não são dado do TSE e não foram testadas (nem afirmadas).', 'Reprodução exata; conferência de fuso; comparação dentro do município (exploratória).', '—', '2º turno de 2026, todas as seções com encerramento registrado.', 'Corte que separe grupos comparáveis dentro do município com diferença persistente.', 'T66 (rodada 8, aberta; R2b exploratório)'),
 q('Q52', 'As seções que passaram das 19h, com 57% a 83% para Lula, mostram favorecimento a Lula?', 'Os números se reproduzem (BA 936 seções, 72,31%; PE 657, 65,70%; SP 1.571, 57,46%; MA tem só 3 seções, 83,31%; no total, 6.342 seções e 1,86 mi de votantes depois das 19h), mas a comparação certa é com as demais seções do mesmo município. Nos 144 municípios com seções tardias e demais, as tardias têm 2,09 pontos de Lula a menos, e a virada entre turnos é igual (−0,2 ponto). Em PE as tardias (65,70%) têm menos Lula que o resto do estado (69,32%). A diferença de SP (57,46% contra 45,98% no resto do estado) vem de onde estão as seções, não de serem tardias. As tardias somam +187 mil de vantagem para Lula.', REF, ['fase3/PREREG_RELATORIO_PERICIAL.md', 'fase3/relatorio_pericial.py', 'fase3/relatorio_pericial_r2b.py', 'fase3/resultados/relatorio_pericial.json', 'fase3/resultados/relatorio_pericial_r2b.json'], '144 municípios com os dois grupos; diferença média ponderada de −2,09 pontos no % de Lula e −0,2 na virada.', "Que 'contrariar o restante do estado' é diferença de composição, não de horário.", 'Causa da demora no encerramento de cada seção.', 'Comparação dentro do município.', '—', '2º turno de 2026, seções com encerramento a partir de 19h.', 'Diferença de Lula dentro do município que persista.', 'T66 (rodada 8, aberta)'),
 q('Q53', "A liberação sem biometria (8,6 milhões, quase o dobro da margem) mostra fraude, e o voto em Lula 'dispara' onde ela é maior?", 'Os números se reproduzem (8.632.488 liberações, 6,73% do comparecimento; Lula chega a 61,5% nas 96 seções com mais de 50% de liberação). Mas em 2022 foram 10.011.346 (8,06%), com razão de 4,7 vezes a margem (em 2026, 1,9); no 1º turno de 2026, 8.342.249 (6,66%). A relação com Lula tem a mesma forma no 1º turno de 2026 (de 45,1% a 52,4%) e em 2022. A correlação é de +0,07 entre seções, −0,03 entre municípios e +0,01 dentro do município: onde há mais liberação são lugares diferentes, e no mesmo município não há relação.', REF, ['fase3/PREREG_RELATORIO_PERICIAL.md', 'fase3/relatorio_pericial.py', 'fase3/relatorio_pericial_r2b.py', 'fase3/resultados/relatorio_pericial.json', 'fase3/resultados/relatorio_pericial_r2b.json'], 'Seções, municípios e, dentro do município, 2026 (1º e 2º turnos) e 2022 (1º e 2º turnos).', 'Que o volume de liberação é menor que em 2022 e que a relação com Lula é estrutural.', 'Quem foi liberado e em quem votou (voto secreto); o controle de idade está no T12.', 'Mesma conta em outras rodadas e anos; dentro do município.', '—', 'Todas as seções com 50 ou mais votantes e 20 ou mais votos válidos.', 'Relação específica do 2º turno de 2026 que persista dentro do município.', 'T67 (rodada 8, aberta); T12, T53'),
 q('Q54', 'Existem aberrações de unanimidade pró-Lula (106 contra 4 seções com 100%; 18 para 1 com mais de 90%)?', 'Os números se reproduzem (106 e 4 seções com 100%; com mais de 90%, 6.802 e 368 sem o exterior, 18,5 para 1). Em 2022 as razões eram maiores: 141 contra 2 (70,5 : 1) e 9.424 contra 199 (47 : 1); no 1º turno de 2022, 120 : 1. Em 2026, 94% das seções com mais de 90% de Lula estão no Norte e Nordeste (MA 1.549, BA 1.345, PI 870, PE 667, CE 662), com mediana de 198 votos válidos contra 255. Os zeros de votos seguem sem modelo calibrado (Q48).', REF, ['fase3/PREREG_RELATORIO_PERICIAL.md', 'fase3/relatorio_pericial.py', 'fase3/relatorio_pericial_r2b.py', 'fase3/resultados/relatorio_pericial.json', 'fase3/resultados/relatorio_pericial_r2b.json'], '2026 e 2022, 1º e 2º turnos, sem o exterior.', 'Que a razão é menor que em 2022 e concentrada onde Lula é forte e as seções são menores.', "Fiscalização partidária e 'zona rural' citadas no relatório não são dado do TSE.", 'Reprodução exata e comparação com 2022.', '—', 'Todas as seções com votos válidos.', 'Razão maior que a de 2022 depois de controlar a geografia.', 'T68 (rodada 8, aberta); T49, T64'),
 q('Q55', 'O teste de Benford do primeiro dígito acusa manipulação?', 'Não. O primeiro dígito dos votos por seção não segue Benford nos dois anos (o dígito 1 aparece em ~61% das seções de cada candidato, contra 30% do esperado), mas isso ocorre porque as contagens são limitadas, de poucas centenas por seção. O desvio observado (MAD de 0,071 a 0,081) fica entre duas referências simuladas sem manipulação (beta-binomial e binomial) nas quatro combinações de ano e candidato. O teste não discrimina neste dado.', REF, ['fase3/PREREG_RELATORIO_PERICIAL.md', 'fase3/relatorio_pericial.py', 'fase3/relatorio_pericial_r2b.py', 'fase3/resultados/relatorio_pericial.json', 'fase3/resultados/relatorio_pericial_r2b.json'], '2026 e 2022, Lula e direita, 2º turno; 40 sorteios por referência.', 'Que o desvio de Benford é esperado em contagens limitadas e cabe nas referências sem manipulação.', 'Que o teste detectaria uma alteração real: neste dado ele não tem poder.', 'Duas referências simuladas.', '—', 'Todas as seções com votos do candidato.', 'Desvio fora das duas referências.', 'T69 (rodada 8, aberta)'),
 q('Q56', 'Os microdados das urnas ficaram trancados por 72 horas, até a manhã de 28/10?', 'Para os arquivos por urna, não: a primeira conferência de um terceiro contra o arquivo publicado pelo TSE foi às 19:10 de 25/10, e 177 dos 404 boletins foram conferidos ainda em 25/10. Para o CSV BWeb de dados abertos, este projeto não tem registro da primeira publicação (baixou em 27 e 28/10), então essa parte não é testável aqui.', PAR, ['fase3/PREREG_RELATORIO_PERICIAL.md', 'fase3/relatorio_pericial.py', 'fase3/relatorio_pericial_r2b.py', 'fase3/resultados/relatorio_pericial.json', 'fase3/resultados/relatorio_pericial_r2b.json'], '404 conferências de terceiro entre 25/10 e 28/10.', 'Disponibilidade dos arquivos por urna na noite da eleição.', 'Quando o CSV BWeb foi publicado.', 'Hora da primeira conferência de terceiro.', '—', '404 boletins de terceiros.', 'Registro de primeira publicação do CSV.', 'T70 (rodada 8, aberta)'),
 q('Q57', "As curvas acumuladas do 1º e do 2º turno, 'torcidas' em 5,25 pontos, ficam semelhantes demais e projetam 53% para Flávio e 46% para Lula?", "Não. A 'projeção' é o resultado oficial (Lula 51,79%, Flávio 48,21%) com o deslocamento de 5,25 pontos escolhido no botão do gráfico, que o próprio gráfico diz não alterar os dados; ele equivale a mover 6,5 mi de votos de Lula para Flávio. A semelhança das curvas é esperada: as urnas não chegam em ordem aleatória (a mesma seção chega em posição parecida nos dois turnos, Spearman 0,56, e o Sudeste é 67% das últimas urnas), e cada seção vota no 2º turno como no 1º (correlação 0,99). Um modelo em que cada seção repete o 1º turno mais uma virada nacional reproduz a curva real do 2º turno a no máximo 0,30 ponto. Em 2022 as curvas eram ainda mais parecidas (0,94 contra 0,90).", REF, ['fase3/PREREG_CURVAS_SOBREPOSTAS.md', 'fase3/curvas_sobrepostas.py', 'fase3/resultados/curvas_sobrepostas.json'], 'Spearman da ordem 0,56 (2022: 0,64); Pearson das curvas 0,905 (2022: 0,941); contrafactual a 0,30 ponto (2022: 0,29); deslocamento = 6.514.319 votos de cada lado.', 'Que a projeção é o deslocamento visual e que a semelhança vem da ordem geográfica de chegada e do voto estável por seção, igual a 2022.', 'Opinião pública e confiança nas instituições, citadas no vídeo, não são dado do TSE.', 'Reprodução; 200 ordens aleatórias independentes; contrafactual estrutural; 2022 como referência.', '—', '2026 e 2022, 1º e 2º turnos, todas as seções com boletim recebido.', 'Semelhança maior que a de 2022 com a curva real afastada do contrafactual além de 2022.', 'T71 (rodada 8, aberta); T03, T10, T40'),
]
ALE_VOTOS = {"Q57": "Não se traduz em votos; o deslocamento do vídeo equivale a mover 6,51 mi de votos de Lula para Flávio (2,9 vezes a margem).", "Q51": "A prorrogação de fato (depois das 17:30) deu +228.095 votos de vantagem a Lula, 5,1% da margem; sem essas seções, Lula lidera por 4.202.096.", "Q52": "As seções a partir das 19h somam 1,86 mi de votantes e +187 mil de vantagem de Lula; dentro do município, menos Lula (−2,09 pontos).", "Q53": "Não se traduz em votos: a liberação não indica o voto; dentro do município a relação com Lula é nula.", "Q54": "Escala descrita (106 seções com 100% para Lula; 141 em 2022); não é limite de fraude.", "Q55": "Não se traduz em votos.", "Q56": "Não se traduz em votos.","Q27": "Dentro do local: ~600 votos (1º turno) e ~440 (2º), contra margem de 2,14 mi (2022).", "Q28": "As 6 seções sem ligação completa somam menos de 2 mil votos.",
 "Q29": "Contrafactual dentro do município: −179 mil votos de Lula, menos que metade da margem de 2022 (1,07 mi).", "Q30": "Unânimes de Lula: 16.418 votos (0,8% da margem de 2022).",
 "Q31": "14.860 votos (0,34% da margem de 2026).", "Q32": "Descritivo; não se traduz em votos suspeitos.", "Q33": "Descritivo; não se traduz em votos suspeitos.",
 "Q34": "34.327 votos depois das 17h (0,8% da margem); a pausa não altera votos.", "Q35": "Sem votos suspeitos no agregado; rajadas do T28: 99 votos.",
 "Q36": "133.852 votos perdidos por Flávio (3% da margem), contra 114.916 de Lula em 2022.", "Q37": "Não se traduz em votos.", "Q39": "Queda de brancos e nulos de 1,82 mi entre os turnos de 2026, explicada em grande parte por erro de campo (número de governador no campo de presidente) e por haver menos 2º turno de governador; resto uniforme.", "Q40": "698 mil nulos com número de governador no 1º turno de 2026; 143 mil digitando 14 no 2º turno.", "Q41": "Não se traduz em votos; muda a leitura das magnitudes de fluxo.", "Q38": "Cabo Frio: 9.169 votos ganhos por Lula (0,2% da margem), todos cobertos pelos 9.511 disponíveis."}
for p in ALE: p["em_votos"] = ALE_VOTOS[p["id"]]
# Q51 a Q56 (rodada 8, relatório pericial, em aberto) ficam em capítulo próprio, depois da Operação Veracidade: os ids não mudam (há links), só a ordem de leitura
PER = [p for p in ALE if p["id"] in {"Q51", "Q52", "Q53", "Q54", "Q55", "Q56", "Q57"}]
ALE = [p for p in ALE if p not in PER]

# Operação Veracidade Geral (28/10/2026): perguntas Q42 a Q50 vêm de operacao_veracidade/resultados/respostas_novas.json (N9 vira Q42; N1 a N8 viram Q43 a Q50)
_limpa = lambda o: {k: (_limpa(v) if isinstance(v, dict) else [x.replace("**", "") if isinstance(x, str) else x for x in v] if isinstance(v, list) else v.replace("**", "") if isinstance(v, str) else v) for k, v in o.items()}  # a fonte congelada traz **negrito** em texto simples
_NOV = {n["id"]: _limpa(n) for n in json.load(open(R + "/operacao_veracidade/resultados/respostas_novas.json"))}
_MAPA = [("N9", "Q42", REF), ("N1", "Q43", DEM), ("N2", "Q44", DEM), ("N3", "Q45", PAR), ("N4", "Q46", DEM), ("N5", "Q47", PAR), ("N6", "Q48", ND), ("N7", "Q49", DEM), ("N8", "Q50", PAR)]
OPV = []
for _n, _q, _cl in _MAPA:
    _x = _NOV[_n]
    OPV.append(q(_q, _x["pergunta"], _x["resposta"] + f" (no relatório da operação: {_n})", _cl, _x["evidencia"], _x["cobertura"], _x["demonstra"], _x["nao_demonstra"], _x["validacao"], "—", _x["cobertura"], _x["proxima"], _x["independencia"], {}, ""))
    OPV[-1]["em_votos"] = _x["votos"]

inv = {i["id"]: i for i in json.load(open(R + "/fase3/inventario.json"))["itens"]}
itens = []
for k, (resp, classe, qs) in INV.items():
    i = inv.get(k, {})
    BLOQ = {"P11", "P21", "A173"}  # P6 saiu em 28/10/2026: 404 boletins de terceiros obtidos (T61)
    fech = ("Bloqueada por fonte externa (tentativas registradas)" if k in BLOQ and not classe.startswith(("Demonstrado", "Refutado")) else
            "Encerrada: respondida no escopo" if classe.startswith(("Demonstrado", "Refutado")) else
            "Encerrada: demonstrada em parte, limite registrado" if classe.startswith("Parcialmente") else "Encerrada: não determinável com estes dados ou métodos")
    itens.append({"id": k, "pergunta": i.get("pergunta", ""), "resposta": resp, "classificacao": classe, "fechamento": fech, "perguntas_relacionadas": qs, "estado_inventario": i.get("estado_final"),
                  "evidencias": i.get("evidencia_arquivos", []), "limitacao": i.get("proxima_evidencia", ""), "em_votos": EMV_INV[k], "historico": i.get("historico", []), "detalhe": i.get("resposta_ou_motivo", "")})
assert len(itens) == 33, len(itens)
OUT = {"gerado": "2026-10-28", "situacao": "Rodada 8 em aberto (registro vivo), sobre a V1.5 congelada em 28/10/2026",
       "margem": MARGEM,
       "aviso": "Votos de simulações são sintéticos. Concordância entre registros da mesma origem é consistência interna, não verificação independente. Nenhuma resposta é veredito global sobre fraude.",
       "capitulos": [{"id": "integridade", "titulo": "Integridade dos resultados oficiais", "perguntas": INT, "descricao": "Q1 a Q7 (Fase 3): os votos publicados batem com os arquivos das urnas, a assinatura e a soma oficial?"},
                     {"id": "curvas", "titulo": "Curvas, viradas e periodicidade", "perguntas": CUR, "descricao": "Q8 a Q14 (Fase 3): a ordem em que os boletins chegaram e a curva divulgada na noite da apuração."},
                     {"id": "zeros", "titulo": "Zeros de votos", "perguntas": ZER, "descricao": "Q15 a Q20 (Fase 3): seções com zero voto para um finalista."},
                     {"id": "turnos", "titulo": "Mudança entre o primeiro e o segundo turno", "perguntas": TUR, "descricao": "Q21 a Q26 (Fase 3): de onde vieram os votos que cada finalista ganhou ou perdeu."},
                     {"id": "alegacoes", "titulo": "Alegações públicas testadas", "perguntas": ALE, "descricao": "Q27 a Q39 (rodada 6, V1.4): a live de 2022, o pedido do PL, matérias e posts; Q40 e Q41 (rodada 7, V1.5): o que foi digitado nos nulos e se o estimador de fluxos acerta."},
                     {"id": "operacao", "titulo": "Operação Veracidade: os dados são fiéis ao que aconteceu?", "perguntas": OPV, "descricao": "Q42 a Q50 (rodada 7, V1.5): auditoria adversarial dos dados e do próprio veredito, inclusive o vídeo dos \"votos extras\" (Q42)."},
                     {"id": "pericial", "titulo": "Relatório pericial e curvas sobrepostas: hora de encerramento, biometria, unanimidade, Benford, forma da curva", "perguntas": PER, "descricao": "Q51 a Q57 (rodada 8, em aberto, ainda não congelada): as alegações de um relatório divulgado em imagens e de um vídeo com as curvas dos dois turnos sobrepostas, testadas com pré-registro."}],
       "inventario": itens,
       "achados_sem_causa": ["Salvador (2026): virada de Lula ~30 mil votos acima do previsto pelo histórico, em todas as zonas, única entre as 27 capitais, não explicada pelo perfil do eleitorado (T44, final_salvador.json); sem 2º turno estadual na Bahia; Fortaleza com desvio parecido no sentido oposto.", "Assimetria de cauda do T02 (pró-Lula) real nos dois anos; em SP 2022, desvio da zona 251 que persiste após o perfil do eleitorado.",
                             "RS 88013/2/199 (2022): imagem do boletim (196 votos) diferente do boletim digital e da tabela (288); log publicado só cobre 196 votos.",
                             "2022: 153 seções-turno com log diferente do comparecimento (5.287 votos sem registro no log publicado; 2.503 votos a mais no log em 47 seções), recontagem confirmada (fila F1).",
                             "173 arquivos assinados e 485 auxiliares fora do pacote de dados abertos de 2022.",
                             "8 urnas com rajada sem biometria no fim do dia (2026, 1º turno; 99 votos), padrão também presente em 2022.",
                             "Queda uniforme de ~0,6 ponto de brancos e nulos no 2º turno de 2026 nas UFs sem 2º turno de governador nos dois anos, sem relação com a força de Lula (T57); o erro de campo (T58) explica a parte ligada a Lula.",
                             "Recebimento de boletins parado das 17:07 às 19:03 no 2º turno de 2026 (T52): coincide com a prorrogação; a regra que o acionou não está nos dados.",
                             "Certificados (T60a): 98 emitidos depois da validade do certificado público da AC URNA (todos verificam com a chave publicada); certificado de outra urna que a da tabela em 17 seções de 2026 e 22 de 2022, um caso com três identificações diferentes e votos iguais; a regra de emissão por modelo não é pública.",
                             "Última troca de liderança mais tardia que nos modelos nulos e que o modelo de atraso de transmissão prevê, nos dois anos (fila F4)."],
       "limites": ["Autenticidade só até a AC emissora, agora em 100% das urnas (T60a), sem âncora do TSE.", "BU, RDV, imagem e log não são testemunhas independentes entre si.",
                   "Comprometimento anterior à geração dos registros (H2) não é distinguível com dados públicos.",
                   "Fontes externas: capturas do Internet Archive (agregado nacional, instantes amostrados) e 404 boletins impressos de terceiros (amostra de conveniência, 0,08%, só 2º turno de 2026).",
                   "O poder de detecção é medido sobre a base real, que pode já conter alteração; e é assimétrico entre os sentidos (T63).",
                   "Registros coerentes gerados por fonte comprometida passam por todas as verificações internas (T62).",
                   "Fluxos individuais entre turnos não identificáveis.", "Sem modelo de chegada validado (curvas) e sem modelo de cauda baixa validado (zeros)."]}
json.dump(OUT, open(R + "/fase3/respostas_f3.json", "w"), ensure_ascii=False, indent=1)
L = ["# Respostas científicas da F3 (28/10/2026)", "", "> " + OUT["aviso"], "> " + MARGEM, "> Rodada 8 em aberto (relatório pericial e curvas sobrepostas, Q51 a Q57), sobre a V1.5 (rodada 7, Operação Veracidade Geral) congelada em 28/10/2026. A rodada 8 está em aberto (registro vivo, não congelado).", ""]
for c in OUT["capitulos"]:
    L += [f"## {c['titulo']}", "", f"_{c['descricao']}_", ""]
    for p in c["perguntas"]:
        L += [f"### {p['id']}. {p['pergunta']}", f"**Resposta:** {p['resposta']}", f"**Classificação:** {p['classificacao']}"]
        L.append(f"**Em votos:** {p['em_votos']}")
        for a, txt in p["por_ano"].items(): L.append(f"- **{a}:** {txt}")
        L += [f"- **Números:** {p['numeros']}", f"- **Demonstra:** {p['demonstra']}", f"- **Não demonstra:** {p['nao_demonstra']}", f"- **Robustez:** {p['robustez']}",
              f"- **Causa:** {p['causa']} · **Alcance:** {p['alcance']}", f"- **O que mudaria a resposta:** {p['mudaria']}", f"- **Validação:** {p['validacao']}",
              f"- **Evidências:** " + ", ".join(f"`{e}`" for e in p["evidencias"])] + ([f"- **Reabertura:** {p['reabertura']}"] if p["reabertura"] else []) + [""]
L += ["## Matriz dos 33 itens do inventário", "", "| Id | Resposta direta | Em votos | Classificação | Perguntas |", "|---|---|---|---|---|"]
for i in itens: L.append(f"| {i['id']} | {i['resposta']} | {i['em_votos']} | {i['classificacao']} | {', '.join(i['perguntas_relacionadas'])} |")
L += ["", "## Achados que persistem sem causa demonstrada", ""] + [f"- {x}" for x in OUT["achados_sem_causa"]] + ["", "## Limites das fontes e dos métodos", ""] + [f"- {x}" for x in OUT["limites"]]
open(R + "/fase3/RESPOSTAS_F3.md", "w").write("\n".join(L) + "\n")
print("ok", len(itens), sum(len(c["perguntas"]) for c in OUT["capitulos"]))
