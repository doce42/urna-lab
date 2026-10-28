# Protocolo pré-execução (escrito em 28/10/2026, antes dos testes novos)

Escopo: Operação Veracidade Geral. Regra: nada abaixo foi calculado antes de ser escrito aqui, exceto o que consta em "Já observado antes deste protocolo".

## Já observado antes deste protocolo (para não parecer pré-registro do que não é)
- Estado do projeto (`resultados/estado_inicial.txt`): as fases F4, F5, F6 e F7 **não existem**; existem F1, F2, F3, a rodada 6 (V1.4, alegações públicas) e a rodada 7 no registro vivo (T58, T59), não congelada.
- Integridade dos snapshots (`resultados/integridade_snapshots.json`): rodadas 1 a 6, todos os hashes batem; amostra de 25 arquivos brutos bate com o manifesto. No manifesto, só 331 de 51.883 arquivos foram conferidos contra um hash publicado pelo TSE.
- Do repositório DataUrnas-BR (terceiro): a cadeia de certificados foi validada em 5% das seções; a raiz não é pública; o certificado publicado da AC URNA venceu em 18/07/2026 e há certificado de urna emitido depois.
- A página oficial de certificados do TSE respondeu "Access Denied" (HTTP 403) a este ambiente; não foi contornada.
- O app de totalização paralela de terceiros publica arquivos estáticos (404 boletins do 2º turno de 2026, lidos do QR Code do boletim impresso); foram baixados (`externo/arvor_totalizacao/`, com SHA-256 e data), sem uso da API deles.

## Modelo de ameaças e onde cada teste entra
| Hipótese | Mecanismo | Testes existentes | Testes novos |
|---|---|---|---|
| H-A alteração posterior | arquivo genuíno trocado antes da publicação | T01, T16, T17b, Q1 a Q6 | T60b (controles de mutação), T61 |
| H-B totalização incorreta | boletins certos, soma errada | T32, T43, Q1 | — (T61 confere por seção) |
| H-C republicação seletiva | versões substituídas depois | P4, Q6 (Internet Archive) | T61 (relógio independente) |
| H-D comprometimento anterior | urna gera registros coerentes e incorretos | nenhum (ponto cego H10) | T62 (identificabilidade), T60a |
| H-E fabricação coordenada | vários documentos da mesma origem | CONS (consistência interna) | T62 (experimento B) |
| H-F concentrada | locais, zonas, municípios | T44, I1, I3, E02 | T63 |
| H-G distribuída | pequenas alterações em muitas seções | T13 (poder), ponto cego H9 | T63 |
| H-H temporal | horários e lotes | T09, T40, T52 | T61 (relógio independente), T63 (lote) |
| H-I comportamento legítimo | heterogeneidade | P5, T47, T49 a T57 | — |
| H-J erros não fraudulentos | leitura, software, formato | catálogo de artefatos | T60b (falhas do verificador) |

Frentes (8): (1) estado e mapa de confiança; (2) criptografia hostil; (3) evidência externa; (4) versões e documentos; (5) simulações adversariais; (6) curvas; (7) zeros e entre turnos; (8) anomalias, logs e revisão geral. Testes novos: T60a, T60b, T61, T62, T63, T64 (no máximo 2 por frente; frentes 1, 4, 6 e 8 sem teste novo, por reaproveitarem resultados existentes ou por falta de dado novo viável).

## T60a: cadeia de certificados de todas as urnas
- **Pergunta:** o certificado de cada urna (2022 e 2026, 1º e 2º turno) é assinado pela AC emissora declarada, estava válido na data da eleição e é único?
- **Hipótese nula:** todos os certificados verificam e são únicos. **Concorrente:** há certificados de urna não assinados por AC conhecida, emitidos depois da eleição, com chave repetida ou diferentes entre turnos.
- **Estatística/universo:** todos os certificados únicos (por SHA-256) extraídos dos `vota.vsc/.vscmr` das 4 combinações ano × turno. Ed521: verificação só com a variante de mensagem fixada em P11 (M = TBS), **sem tentar outras**; ECDSA: `verify_directly_issued_by`. Chaves públicas das ACs: as de `fase2/externos/certificados/` (origem de terceiro, ver limite).
- **Critério de aceitação:** 100% verificam; nenhum emitido depois do dia da eleição; nenhum CN com dois certificados na mesma eleição; nenhuma chave pública em dois CN. Qualquer exceção é listada (seção, hash) e investigada como possível artefato (extração, formato) antes de ser chamada de anomalia.
- **Parada:** 1 extração + 1 repetição por falha operacional. **Custo:** ~4 extrações de ~8 min com 12 processos; RAM baixa.
- **Limite declarado de antemão:** as ACs vêm de terceiro e a raiz não é pública; o teste prova consistência da cadeia até a AC emissora, não autenticidade da raiz.

## T60b: controles positivos e negativos do verificador
- **Pergunta:** o verificador rejeita arquivos adulterados e aceita os genuínos? O que a verificação de lista prova, e o que só a cadeia prova?
- **Controles (cópias em memória de arquivos reais de AC 2026 2º turno e AL 2022 2º turno, 40 seções cada):** (1) um byte alterado no BU; (2) BU truncado; (3) um byte alterado na lista assinada; (4) um byte alterado na assinatura da lista; (5) certificado trocado por o de outra urna; (6) arquivo removido da lista; (7) arquivo extra; (8) controle genuíno sem alteração.
- **Controle hostil sintético:** par de chaves ECDSA P-521 descartável, certificado autoassinado rotulado `TESTE-SINTETICO`, lista assinada com ele. Esperado: aceito pela verificação de lista (autoconsistência), rejeitado pela verificação de cadeia. Nada disso é gravado em arquivo de dados nem reproduz nome ou assinatura oficial.
- **Critério:** 8/8 comportam-se como esperado; qualquer desvio é falha do verificador e vira achado. **Custo:** segundos.

## T61: boletins impressos de terceiros (QR Code)
- **Pergunta:** os 404 boletins do 2º turno de 2026 obtidos do QR Code do boletim impresso concordam com a base do TSE, e suas assinaturas verificam de forma independente?
- **Hipótese nula:** concordam em tudo. **Concorrente:** há divergência de votos, de identidade da urna ou de assinatura.
- **Medidas, por boletim:** (a) assinatura do QR contra o certificado do próprio QR (verificador nosso); (b) certificado: cadeia até a AC (função do T60a), validade na data; (c) votos (13, 22, brancos, nulos, comparecimento, aptos) contra a tabela do TSE e contra o BU decodificado do pacote; (d) urna do QR (IDUE) contra a urna efetivada e o certificado do `vota.vsc`; (e) horários: impressão (DTFC/HRFC do QR), emissão e recebimento no TSE (base), recebimento no app de terceiros.
- **Critério:** qualquer diferença em (a) a (d) é S4 e é preservada com hash; (e) é descritivo.
- **Limites declarados de antemão:** amostra de conveniência (404 de 499.207 seções, 22 UFs, sem desenho probabilístico, viés de seleção desconhecido); quem coleta e quem publica são o mesmo projeto; a evidência cobre o 2º turno de 2026 apenas; não extrapola.

## T62: identificabilidade (experimentos A e B, determinísticos, sobre cópias sintéticas)
- **A (alteração só na publicação):** em 5% das seções de uma UF real, alterar apenas a tabela; depois apenas a tabela e o BU; depois BU e RDV; depois todos menos o log. Medir, por verificação de consistência (tabela = BU, BU = RDV, BU = imagem, BU = log, hash e assinatura), quais alterações cada uma detecta.
- **B (registros coerentes sintéticos):** alterar tabela, BU, RDV, imagem e contagem do log da mesma forma. Verificar se alguma consistência interna detecta. Esperado: nenhuma, por construção; o experimento mede e documenta o limite de identificabilidade, **não** a possibilidade operacional de comprometer urnas.
- **Critério:** determinístico; a matriz alteração × verificação é o resultado.

## T63: poder da bateria estatística contra mecanismos adversariais
- **Dados:** base por seção do 2º turno, 2026 (grade completa) e 2022 (grade reduzida); cópias sintéticas; a base real é a referência, não verdade conhecida sem fraude.
- **Detectores (fixados agora):** D1 cauda de resíduos por seção (resíduo da virada contra a média do município, z robusto, limiar 4, contagem direcional); D2 efeito de local de votação (média de z do local × √n, limiar 5, contagem direcional) e de zona; D3 desvio de município (virada municipal contra UF, 1º turno e tamanho; z robusto, limiar 4); D4 comparecimento (z do aumento de comparecimento por seção contra o município); D5 dígito final (qui-quadrado, p < 0,001, sem direção). Limiares de alarme: percentil 97,5 do bootstrap por município (B = 200, semente 11) da estatística na base real.
- **Mecanismos:** troca de votos, enchimento (abstenção → finalista) e conversão de brancos e nulos; seleção: seções aleatórias dispersas, poucas seções com alteração grande, locais inteiros, zonas inteiras, municípios inteiros (sem os cinco grandes), os cinco grandes (SP, RJ, DF, CE, BA) juntos, UFs inteiras, macrorregião, seções de reduto do alvo, seções de reduto do oponente, deslocamento proporcional uniforme (H9), lote tardio de recebimento. Ambos os sentidos (Lula → Flávio e Flávio → Lula).
- **Magnitudes (votos movidos ao total):** 25 mil, 50 mil, 100 mil, 250 mil, 500 mil, 1 milhão e 2,22 milhões (o que inverte 2026); limitadas pela aritmética.
- **Réplicas:** 20 por célula nos mecanismos aleatórios, 1 nos determinísticos; sementes registradas.
- **Medidas:** poder (alarme na direção correta por qualquer detector D1 a D4), alarme na direção oposta, alarme sem direção (D5), menor magnitude com poder ≥ 80% por mecanismo, falsos alarmes (bootstrap e base de 2022 sem alteração, tratados como achado e não falso positivo).
- **Critério de adequação:** um mecanismo é "visível" se alcança poder ≥ 80% em magnitude ≤ 2,22 milhões; senão é "ponto cego" para esse mecanismo. Falsos alarmes: 0 em 30 simulações não é taxa zero; intervalo de Clopper-Pearson é informado.
- **Parada:** 1 execução da grade + 1 sensibilidade (limiares 3 e 5 no D1). **Custo:** minutos com 12 processos.

## T64: zeros e poucos votos, 2022 e 2026
- **Descritivo (determinístico):** por ano, turno e finalista, número de seções com 0, 1, 2, 3 a 5 votos entre as de comparecimento positivo, e a distribuição por UF.
- **Modelo novo (3ª família):** beta-binomial por seção com média municipal do próprio turno e sobredispersão intramunicipal global estimada fora da UF avaliada (validação por UF retida). Critério fixado agora: o modelo é adequado se o número observado de zeros estiver dentro do intervalo de predição de 95% (Monte Carlo, 500 sorteios) em pelo menos 80% das UFs com esperado ≥ 1. Senão: "modelo falhou", sem uso confirmatório.
- **Parada:** 1 execução + 1 correção.

## Regras gerais
- Dados brutos, versões congeladas e `testes/registro.json` não são alterados. Os testes novos têm registro próprio em `resultados/registro_operacao.json`; a integração ao registro e ao site depende de aprovação.
- Sem push, deploy, tag ou release. Sem subagentes.
- Erros de comparador e de extração: corrigir no máximo duas vezes por teste, declarando a correção.
- Cada afirmação final precisa de arquivo e script rastreáveis.

## Emenda 1 (escrita antes de rodar o T63; 28/10/2026)
- **Experimento B2 (fabricação coerente de um 2º turno inteiro):** dois fabricantes sintéticos que mantêm o resultado nacional: *ingênuo* (virada municipal observada + sorteio binomial) e *calibrado* (acrescenta a sobredispersão por seção que a base real tem, como faria um atacante que aprendeu com a eleição real). Mede se D1 a D5 distinguem a fabricação da base real.
- **Detector D6 (sub-dispersão):** razão entre a escala robusta (MAD) do z por seção da cena e a da base real; alarme se < 0,85 ou > 1,15. Fixado agora, antes de rodar.
- Réplicas B2: 20 por fabricante, mesmas sementes derivadas do ano e do índice.

## Emenda 2 (escrita antes de rodar a grade do T63, depois de um teste de fumaça de 2 réplicas; 28/10/2026)
O teste de fumaça (sem a grade completa) mostrou: (a) a base real tem escala robusta do z por seção de 0,50 (sub-dispersa em relação ao binomial independente, porque os mesmos eleitores votam nos dois turnos); (b) o "deslocamento uniforme proporcional" é uniforme em voto, não em logit, e por isso deixa rastro nos detectores. Mudanças, todas fixadas antes de ver os resultados da grade:
- **Mecanismo novo `uniforme_logit`:** soma uma constante c ao logit da participação de Lula em todas as seções (c por bisseção para mover X votos). É o caso de deslocamento distribuído que preserva a estrutura relativa entre seções (H9).
- **Fabricante calibrado (B2) corrigido:** sem sorteio binomial; participação do 2º turno = logit(1º turno) + virada municipal observada + ruído N(0, τᵢ) com τᵢ = S0 · seᵢ (S0 = escala robusta da base real), de modo que a escala do z da fabricação coincida com a da base real. O fabricante ingênuo continua como definido (binomial independente).
- **Detector D7 (estrutura local):** razão entre o desvio padrão do z agregado por local de votação (locais com ≥ 3 seções) e por zona (≥ 10) da cena e o da base real; alarme se fora de [0,8; 1,25].
- Nenhum limiar ou critério dos detectores D1 a D5 muda.

## Emenda 3 (escrita antes de rodar a grade do T63; depois do segundo teste de fumaça; 28/10/2026)
O segundo teste de fumaça mostrou que o fabricante calibrado em dispersão passa D1 a D6 e só é flagrado por D7 (estrutura de local e zona). Para medir o limite de identificabilidade com o atacante mais bem informado possível com dados públicos, entra um terceiro fabricante:
- **`calibrada_estrutura`:** participação do 2º turno = logit(1º turno) + virada municipal observada + efeito de zona N(0, b²) + efeito de local N(0, a²) + ruído por seção N(0, eᵢ²), com eᵢ² = max(S0²·seᵢ² − a² − b², 0,05·S0²·seᵢ²). (a, b) escolhidos por grade 7×7 em [0; 0,3] logit, minimizando |ln(razão de escala z)| + |ln(razão de local)| + |ln(razão de zona)| contra a base real, com uma única realização por ponto e semente fixa. Isso supõe um atacante que conhece a estrutura de variância da eleição real (cenário de teto, não de plausibilidade operacional).
- Os três fabricantes são avaliados com D1 a D7 e mantêm o resultado nacional por construção da virada municipal observada.

## Emenda 4 (escrita depois da 1ª execução da grade e antes da 2ª execução apenas do fabricante de estrutura; 28/10/2026)
**O que a 1ª execução mostrou (preservada em `resultados/sim_<ano>_fabricada.csv`, versão v1):** o fabricante `calibrada_estrutura` foi flagrado por D2z e D3 nos dois anos. Causa inspecionada: os efeitos de zona e de local entravam com média diferente de zero dentro do município, o que desloca o total municipal (escala 0,047 logit no D3), coisa que um atacante que preserva os totais municipais não faria; além disso a grade de (a, b) era grossa demais perto de zero.
**Mudança (só nesse fabricante; a grade principal não é refeita):** `calibrada_estrutura_v2`: (1) efeitos de zona centrados na média ponderada do município e efeitos de local centrados na média da zona; (2) correção do total municipal por uma iteração (a diferença de logit entre o total municipal real e o fabricado é somada a todas as seções do município); (3) grade de (a, b) com 11 valores {0; 0,005; 0,01; 0,02; 0,03; 0,05; 0,075; 0,1; 0,15; 0,2; 0,3}, mesmo critério de custo.
**Uso:** é o teto de sofisticação de um atacante que conhece os totais municipais e a estrutura de variância da eleição real. Não é prova de que alguém possa fazer isso na prática.
**Contagem do orçamento:** 2ª execução do experimento B2 (uma tentativa de correção de desenho); a grade principal teve 1 execução.

## T65: a hipótese do vídeo dos "98,12% dos votos extras" (escrito antes de qualquer conta; 28/10/2026)
**Origem (só pergunta, não fonte):** transcrição de um vídeo de 90 s. **Afirmações:** (a) 1º turno: Flávio 56,1 mi, Lula 53,8 mi, outros 9,3 mi; (b) a abstenção caiu ~3 mi e os brancos e nulos 1,8 mi: "votos extras" = 4,8 mi; (c) Lula ganhou 10,3 mi; (d) simulação: finalistas repetem o voto e 60% dos outros vão a Lula (~5,5 mi), faltariam 4,7 mi, que são **98,12% dos extras**; (e) "nunca aconteceu" a abstenção cair entre turnos; (f) conclusão sugerida: a conta não fecha.
**Medidas fixadas:** M1 reproduzir a aritmética e o 98,12% com a base; M2 a fração dos extras que iria a Lula em função da parcela s dos outros que vai a Lula (identidade exata), e o intervalo de s compatível; M3 a mesma conta em 2022 para o candidato que mais cresceu (Bolsonaro) com os mesmos 60%; M4 a queda de abstenção entre turnos em 2022 e 2026 na base do projeto; M5 regressão ecológica em municípios (pesos por aptos, efeito fixo de UF, IC por bootstrap de municípios, 200 sorteios, semente 65): ganho do finalista por apto contra votos dos eliminados e contra extras, 2026 (Lula) e 2022 (Bolsonaro).
**Leitura pré-fixada:** (i) o 98,12% é uma consequência da premissa de 60% se, para s = 60%, a fração dos extras for ≥ ~100%; (ii) se a mesma conta em 2022 passar de 100%, o método não discrimina; (iii) fluxos individuais não são identificáveis (Q26); (iv) a regressão (M5) é associação ecológica, frágil (T37, T59), lida só como direção; se o coeficiente dos extras para Lula em 2026 for ≈ 1 e o de Flávio ≈ 0, a hipótese de que os extras foram todos para Lula tem apoio ecológico; se o de Flávio for claramente > 0, não tem.
**Orçamento:** 1 execução + 1 correção.
**M6 (exploratório, acrescentado depois de ver o M5; 28/10/2026):** o M5 mistura "os votos novos preferiram um candidato" com "os votos novos estão onde ele é forte". Controle: em cada município, os votos dos eliminados e os extras são divididos entre os finalistas **na proporção do 1º turno entre eles** (hipótese nula proporcional); soma-se o ganho previsto e compara-se com o ganho observado, nacionalmente e por UF, 2026 e 2022. O resíduo é o que passou do proporcional.
