"""F3: respostas científicas explícitas (fonte única). Gera fase3/respostas_f3.json (lido pelo site, página "Perguntas e respostas
científicas") e fase3/RESPOSTAS_F3.md. Cada resposta aponta para os arquivos de resultado que a sustentam; o histórico de cada item
do inventário vem de fase3/inventario.json."""
import json

R = "."
DEM, REF, PAR, ND, NE = "Demonstrado no escopo definido", "Refutado no escopo definido", "Parcialmente demonstrado", "Não determinado com as evidências disponíveis", "Não executado"
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
   "Não até a raiz: as assinaturas das urnas são válidas até a autoridade certificadora emissora, mas a ligação dessa autoridade a uma âncora do TSE não foi verificada.",
   PAR, ["testes/registro.json (T16)", "fase2/resultados/P11.json", "fase3/resultados/sa22.json", "fase3/resultados/r1_integridade.json"],
   "2026: hash e assinatura válidos em 499.176 (1º) e 499.178 (2º) boletins. 2022: 471.908 e 471.984 boletins e as 159 seções do Sistema de Apuração. Certificados de AC obtidos de terceiro (DataUrnas-BR); AC URNA v2 e AC RAIZ UE não obtidas por canal do TSE.",
   "Os arquivos presentes não foram alterados depois de assinados pela chave da urna.", "Que a chave pertence a uma urna autêntica do TSE (sem âncora); qualquer coisa anterior à assinatura.",
   "Verificação Ed521 e ECDSA P-521 própria; chaves degeneradas rejeitadas.", "não aplicável", "Arquivos presentes.", "Certificados raiz obtidos do TSE por canal verificável.", "Bloqueado no elo final (fonte externa).",
   {"2022": "Assinatura válida até a AC emissora nos arquivos presentes.", "2026": "Idem."}),
 q("Q6", "Existem evidências externas independentes que confirmem ou contradigam os registros publicados?",
   "Sim, uma: capturas do Internet Archive dos totais nacionais divulgados durante a apuração confirmam a base publicada nos instantes capturados. Não há boletins de terceiros nem outra fonte de origem independente.",
   PAR, ["fase3/inv_r2_curva_publica.py", "fase3/resultados/r2_curva_publica.json", "fase3/externos/wayback_capturas/"],
   "39 capturas (2022: 2 e 27; 2026: 6 e 4): diferença máxima de 0,083 ponto percentual entre a proporção divulgada e a recomposta pela base final no mesmo número de seções; mesmo líder em todas; votos nunca diminuem; a última captura é igual ao total oficial onde existe.",
   "Que a base publicada depois corresponde ao que foi divulgado ao vivo, no agregado nacional e nos instantes capturados (contraria alteração posterior que mudasse esses totais).", "Correspondência seção a seção com fonte externa; o que aconteceu antes da divulgação; instantes não capturados.",
   "Custódia de terceiro (Internet Archive); escopo de busca fixado antes; capturas brutas guardadas com SHA-256.", "não aplicável", "Totais nacionais de Presidente em 39 instantes.", "Boletins impressos fotografados por terceiros; capturas por UF.", "Executado (R2), com bloqueio parcial do Internet Archive registrado.",
   {"2022": "29 capturas consistentes.", "2026": "10 capturas consistentes."}),
 q("Q7", "Os testes conseguem detectar mecanismos plausíveis de alteração, e em quais condições falham?",
   "Detectam alguns, em condições limitadas: nos cenários simulados, trocas dispersas de ~123 mil votos e concentradas de ~62 mil em locais ou municípios de até ~5 mil seções foram detectadas no sentido certo; trocas de ~25 mil e trocas no município inteiro das 5 maiores cidades não foram detectadas com confiabilidade.",
   PAR, ["fase3/rev_i1_poder.py", "fase3/rev_a2_poder.py", "fase3/resultados/rev_a2_2026.json", "fase3/resultados/rev_a2_2022.json"],
   "2026, 30 réplicas, limiar calibrado, falso alarme 0/30: dispersa 10% (~123 mil) 30/30; locais e municípios até ~5 mil seções a 5% (~62 mil) 30/30; região a 5% 26/30 e 23/30; 2% (~25 mil) 0 a 1/30; 5 maiores cidades a 10% (155 mil a 696 mil votos) 10 a 13/30 (E02 completo), Brasília e Fortaleza 0/12.",
   "O alcance dos testes nos cenários simulados.", "Detecção fora dos cenários simulados; mecanismos que preservam medianas, mexem no comparecimento ou atuam antes do boletim; votos simulados não são votos encontrados.",
   "Validação em 2022 com o mesmo padrão; direção conferida.", "não aplicável", "4 mecanismos + grandes cidades; 1% das seções; 2%, 5%, 10%.", "Novos mecanismos ou coberturas simulados.", "Executado (I1, A2).",
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
   "Pelo critério pré-registrado, não determinado (o modelo não passou na calibração). Descritivamente, não há excesso agregado: um modelo ajustado em outra metade dos municípios prevê 79,1 e 101,5 zeros contra 79 e 106 observados, dentro do intervalo.",
   ND, ["fase3/inv_r3_zeros.py", "fase3/resultados/r3_zeros.json", "fase3/resultados/rev_i2.json"],
   "Intervalos de predição: [63, 98] e [88, 115]. Falhas do critério: teste de Hosmer–Lemeshow rejeita desvios mínimos nos controles grandes (dezenas de milhares de seções), razões por decil de 1,25 a 1,27 (limite 1,25) e controles de Lula com 1 a 8 zeros. O modelo anterior (I2) também falhou.",
   "Que o total de zeros observado é o previsto fora da amostra por um modelo de covariáveis locais.", "Calibração formal; ausência de excesso em seções específicas.", "Sensibilidade sem a covariável do 1º turno: mesmo resultado.", "não demonstrada",
   "Seções do Brasil; Flávio 2026.", "Modelo que passe em critério de calibração adequado a controles grandes e pequenos.", "Executado (R3); validação formal falhou.",
   reabre="Refazer o critério de calibração (controles com esperado ≥ 20; tolerância por decil adequada a n grande) antes de nova tentativa."),
 q("Q19", "O mesmo método identifica padrões semelhantes em 2022?", "Sim, o mesmo resultado: Bolsonaro 2022 com 160 e 141 zeros contra 162,9 e 136,5 previstos fora da amostra; mesma falha do critério formal.", ND,
   ["fase3/resultados/r3_zeros.json"], "Intervalos [140, 187] e [118, 153].", "Que 2026 e 2022 se comportam do mesmo modo no modelo.", "Calibração formal.", "—", "não demonstrada", "Bolsonaro 2022.", "Ver Q18.", "Executado (R3)."),
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
   "Sim, em parte: a assimetria de cauda do T02 é real nos dois anos; cerca de 0,1% dos locais são atípicos (lista depende do método); há dependência espacial entre municípios; em São Paulo 2022 a zona 251 mantém desvio depois de controlar o perfil do eleitorado.",
   PAR, ["fase2/resultados/P17.json", "fase3/resultados/rev_i3.json", "fase3/resultados/p19.json", "fase3/inv_r4_zona251.py", "fase3/resultados/r4_zona251.json"],
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
 "Q5": "Alcança todos os votos: nenhum voto, de 2022 ou 2026, tem a assinatura verificada até a raiz do TSE; todos estão verificados até a AC emissora.",
 "Q6": "Na captura final de cada eleição, 0 voto de diferença entre o total divulgado ao vivo e a base. A maior diferença em capturas parciais equivale a ~1,7 mil a ~3 mil votos naquele instante (seções com o mesmo horário de recebimento ordenadas de forma diferente), e não muda o líder.",
 "Q7": "Detectado nos cenários simulados: ~123 mil votos dispersos (2,8% da margem de 2026) e ~62 mil concentrados (1,4%). Não detectado: ~25 mil (0,6%); trocas no município inteiro das 5 maiores cidades até ~696 mil votos (15,7% da margem; ~31% do que seria preciso para inverter o resultado). Inverter 2026 exigiria trocar ~2,22 mi votos de lado.",
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
 "Q25": "Zona 251 (SP, 2022): ~4,2 mil votos de Lula acima da virada mediana da capital (0,2% da margem de 2022); zona 259: ~6,2 mil. Cauda pró-Lula do T02: ~740 votos (2026) e ~2.600 (2022). Cada local atípico: dezenas a poucas centenas de votos.",
 "Q26": "Não se traduz em votos: limite de identificabilidade (os limites estão na Q24).",
}
EMV_INV = {"P1": "Erro de ±0,5 a ±1,5 mi votos na razão estimada.", "P2": EMV["Q7"], "P3": "0 voto de diferença entre os canais comparados.", "P4": EMV["Q6"],
 "P5": "Maior efeito +0,004 logit, ~2,7 mil votos se fosse real.", "P6": "—", "P7": "Diferença de −0,029 z, desprezível; não convertida em votos.", "P8": "Efeito desprezível.",
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
 "P6": ("Boletins de terceiros validam os arquivos? Não foi possível determinar: não há boletins de terceiros com dados primários.", ND, ["Q6"]),
 "P7": ("A urna trocada vota diferente? Não, equivalente na margem de ±0,10 z fixada antes.", DEM, []),
 "P8": ("A virada depende da ordem de chegada? Efeito desprezível (|r| ≤ 0,05); em 2022, −0,028, diferente de zero.", DEM, []),
 "P9": ("Os locais atípicos do E02 resistem? Cerca de 0,1% dos locais, em três métodos; a lista depende do método; causa não demonstrada.", PAR, ["Q25"]),
 "P10": ("A rajada sem biometria do T28 resiste? 8 urnas do 1º turno de 2026 seguem sinalizadas pelo critério beta-binomial (99 votos); em 2022 o mesmo critério sinaliza 18 e 21 urnas (23 e 25 pelo T28 original).", DEM, []),
 "P11": ("Os certificados se ligam a uma âncora do TSE? Não foi possível determinar: válidos até a AC emissora; raiz não obtida.", ND, ["Q5"]),
 "P12": ("Diferença do eleitorado do exterior? Explicada: 423 de seções não instaladas + 72 + 30 de seções só nos arquivos de urna.", DEM, []),
 "P13": ("O C06b é reproduzível? Sim: 79 e 123 reproduzidos.", DEM, ["Q24"]),
 "P14": ("Qual a causa da assimetria do T02 em 2022? Não demonstrada; o desvio está no nível da zona (251, 259) e persiste na 251 depois do perfil do eleitorado.", PAR, ["Q25"]),
 "P15": ("Os limites de Fréchet estreitam a razão? Não: a razão não é identificada.", DEM, ["Q24", "Q26"]),
 "P16": ("200 seções conferem? Sim, 200/200 no 1º turno de 2026 (consistência interna); o 2º turno é coberto pelo T17b e pelo R1.", DEM, ["Q1", "Q2"]),
 "P17": ("A assimetria de cauda do T02 é real? Sim, nos dois anos.", DEM, ["Q25"]),
 "P18": ("O T13 bilateral vê os dois sentidos? Sim, para troca dispersa; limites na Q7.", PAR, ["Q7"]),
 "P19": ("Há dependência espacial entre municípios? Sim, Moran's I 0,16 a 0,20; causa não distinguida.", DEM, ["Q25"]),
 "P20": ("O que há nos locais de SP 2022? Desvio no nível da zona, que persiste na 251 após o perfil; arquivos conferem; causa não demonstrada.", PAR, ["Q25"]),
 "P21": ("Fontes externas e cadeia autenticada confirmam os arquivos? Só no agregado nacional ao vivo (Q6); boletins de terceiros e raiz não obtidos.", PAR, ["Q5", "Q6"]),
 "R1-20": ("A base coincide com decodificação independente? Sim, nas seções comuns (99,96% em 2022, 100% em 2026 1º turno); o 2º turno de 2026 não tem comparação de terceiro.", PAR, ["Q1"]),
 "C1": ("As curvas são compatíveis com processos plausíveis de chegada? Não determinado (nenhum modelo de chegada validado). A curva divulgada é reproduzível com os dados por seção.", ND, ["Q10", "Q11", "Q12"]),
 "C1a": ("Quando ocorreram as viradas? Ver Q8 e Q9.", DEM, ["Q8", "Q9"]),
 "C1b": ("Há periodicidade ou trechos lineares anômalos? Não determinado.", ND, ["Q11", "Q12"]),
 "C2": ("2022 e 2026 têm as mesmas características? Diferem na descrição; semelhança estatística não determinada.", ND, ["Q13"]),
 "M1": ("O crescimento entre turnos é reconciliável? Sim, contabilmente (identidade exata); fluxos individuais não identificáveis.", PAR, ["Q21", "Q22", "Q23", "Q24", "Q26"]),
 "Z1": ("Os zeros indicam anomalia? Sem divergência documental; excepcionalidade estatística não determinada pelo critério; sem excesso agregado descritivamente.", ND, ["Q15", "Q16", "Q17", "Q18", "Q19", "Q20"]),
 "MET": ("Os métodos resistem à revisão? Com limites registrados: T10/T11 descritivos; T02 cego a município inteiro; E02 dependente do método; zeros sem modelo validado; concordância entre registros é consistência interna.", PAR, ["Q7"]),
 "AUT": ("Os arquivos são autênticos? Íntegros e assinados até a AC emissora; consistentes entre si; a autenticidade integral do processo não é verificável com dados públicos.", PAR, ["Q1", "Q2", "Q3", "Q5", "Q6"]),
 "A173": ("Os 173 arquivos estão ausentes da publicação? Sim, do pacote de dados abertos (duas cópias); conteúdo não verificado; outro canal do TSE inacessível.", PAR, ["Q4"]),
 "BU1": ("A seção com BU não lido concorda? Sim (boletim do Sistema de Apuração, assinatura válida; consistência interna).", DEM, ["Q20"]),
 "SA22": ("As 159 seções do Sistema de Apuração de 2022 conferem? Sim, 159/159 (consistência interna).", DEM, ["Q1"]),
}

inv = {i["id"]: i for i in json.load(open(R + "/fase3/inventario.json"))["itens"]}
itens = []
for k, (resp, classe, qs) in INV.items():
    i = inv.get(k, {})
    itens.append({"id": k, "pergunta": i.get("pergunta", ""), "resposta": resp, "classificacao": classe, "perguntas_relacionadas": qs, "estado_inventario": i.get("estado_final"),
                  "evidencias": i.get("evidencia_arquivos", []), "limitacao": i.get("proxima_evidencia", ""), "em_votos": EMV_INV[k], "historico": i.get("historico", []), "detalhe": i.get("resposta_ou_motivo", "")})
assert len(itens) == 33, len(itens)
OUT = {"gerado": "2026-10-28", "situacao": "F3 em revisão; respostas não congeladas",
       "margem": MARGEM,
       "aviso": "Votos de simulações são sintéticos. Concordância entre registros da mesma origem é consistência interna, não verificação independente. Nenhuma resposta é veredito global sobre fraude.",
       "capitulos": [{"id": "integridade", "titulo": "Integridade dos resultados oficiais", "perguntas": INT},
                     {"id": "curvas", "titulo": "Curvas, viradas e periodicidade", "perguntas": CUR},
                     {"id": "zeros", "titulo": "Zeros de votos", "perguntas": ZER},
                     {"id": "turnos", "titulo": "Mudança entre o primeiro e o segundo turno", "perguntas": TUR}],
       "inventario": itens,
       "achados_sem_causa": ["Assimetria de cauda do T02 (pró-Lula) real nos dois anos; em SP 2022, desvio da zona 251 que persiste após o perfil do eleitorado.",
                             "RS 88013/2/199 (2022): imagem do boletim (196 votos) diferente do boletim digital e da tabela (288); log publicado só cobre 196 votos.",
                             "2022: 153 seções-turno com log diferente do comparecimento (5.287 votos sem registro no log publicado; 2.503 votos a mais no log em 47 seções), recontagem confirmada (fila F1).",
                             "173 arquivos assinados e 485 auxiliares fora do pacote de dados abertos de 2022.",
                             "8 urnas com rajada sem biometria no fim do dia (2026, 1º turno; 99 votos), padrão também presente em 2022.",
                             "Última troca de liderança mais tardia que nos modelos nulos e que o modelo de atraso de transmissão prevê, nos dois anos (fila F4)."],
       "limites": ["Autenticidade só até a AC emissora (sem âncora do TSE).", "BU, RDV, imagem e log não são testemunhas independentes entre si.",
                   "Comprometimento anterior à geração dos registros (H2) não é distinguível com dados públicos.",
                   "Única fonte externa de custódia: capturas do Internet Archive (agregado nacional, instantes amostrados).",
                   "Fluxos individuais entre turnos não identificáveis.", "Sem modelo de chegada validado (curvas) e sem modelo de cauda baixa validado (zeros)."]}
json.dump(OUT, open(R + "/fase3/respostas_f3.json", "w"), ensure_ascii=False, indent=1)
L = ["# Respostas científicas da F3 (28/10/2026)", "", "> " + OUT["aviso"], "> " + MARGEM, "> A F3 está em revisão; estas respostas não são versão congelada.", ""]
for c in OUT["capitulos"]:
    L += [f"## {c['titulo']}", ""]
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
