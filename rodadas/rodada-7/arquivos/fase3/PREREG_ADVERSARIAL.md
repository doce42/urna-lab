# F3: auditoria adversarial das explicações baseadas em registros oficiais (28/10/2026)

Escrito antes das execuções. Responde à instrução do responsável: **compatibilidade com o log não é comprovação independente da causa.** Limites: 3 casos, 1 teste principal e 1 validação por caso, sem subagente, sem reprocessamento nacional, sem alterar dados brutos, sem deploy.

## Hipóteses de trabalho (não são afirmações)
- **H0, funcionamento legítimo:** os registros descrevem corretamente o ocorrido.
- **H1, registro ou explicação incorretos:** o evento ocorreu, mas o log é incompleto, errado ou não documenta a causa real.
- **H2, comprometimento anterior à geração:** registros coerentes entre si, produzidos por software ou processo comprometido.
- **H3, alteração posterior à geração:** os arquivos publicados divergem de registros genuínos ou de cópias preservadas de forma independente.

## Levantamento
Conclusões do registro que se apoiam em concordância entre registros da mesma origem ou em explicação operacional registrada pelo próprio sistema:
- **Concordância entre registros:** T01, T14, T15, T16, T17, T17b, T32, T39, T41 (arquivos), T43, P16, SA22, BU1, A173 (votos) e R1.
- **Explicação operacional:** T30, T31, T33, T34, T36.

Os três casos abaixo são os de maior impacto sobre a integridade dos votos.

## Caso A: concordância dos votos entre BU, RDV, imagem, tabela e totalização
- **Explicação atual:** "os votos conferem" (T01, T14 a T17b, T32, R1).
- **Dependência das fontes:**
  - BU, RDV, imagem e log são gerados pela mesma urna, com o mesmo software, e assinados pela mesma chave.
  - A tabela e a totalização são publicadas pelo mesmo TSE.
  - O DataUrnas-BR só reimplementa a leitura dos mesmos arquivos.
- **Observações esperadas:**
  - **H0:** tudo concorda, e cópias independentes da divulgação feita durante a apuração também concordam.
  - **H1:** nada específico para votos.
  - **H2:** tudo concorda, e cópias da divulgação ao vivo também (o comprometimento é anterior a tudo). Indistinguível de H0 com dados públicos.
  - **H3 (alteração posterior da base por seção):** os totais parciais publicados ao vivo divergiriam dos totais recompostos a partir da base publicada depois.
- **Teste:** o R2, já executado com fonte de custódia externa e escopo pré-registrado em `PREREG_RESPOSTAS.md`. As capturas do Internet Archive dos totais nacionais divulgados durante a apuração são comparadas com a recomposição pela base final, no mesmo número de seções.
- **Critério:** diferença de proporção abaixo de 0,1 ponto percentual e mesmo líder em todas as capturas; votos que nunca diminuem; captura final igual ao total.
- **Validação:** a comparação por horário (defasagem entre recebimento e divulgação).
- **Limite já conhecido:** é agregado nacional. Uma alteração posterior que preserve os totais nacionais em cada momento capturado, trocando votos entre seções sem mudar a soma, não é detectada.

## Caso B: contas de integridade que não fecham (T36), "explicadas" por declaração, log ou inferência
- **Explicação atual:**
  - 1º turno de 2026: 186 casos, sendo 38 declarados pelo TSE (CEFT), 5 com evento compatível no log, 142 inferidos (uma confirmação sem voto computado) e 1 sem explicação.
  - 2º turno de 2026: 75 casos.
- **Dependência:** as explicações vêm do próprio log da urna ou de declaração do próprio TSE. A inferência é do projeto, a partir do mesmo log.
- **Observações esperadas:**
  - **H0:** os votos dessas seções se comportam como os do resto do município.
  - **H1 ou H2 com efeito em votos concentrado nessas seções:** deslocamento direcional da virada nessas seções.
  - **H1 sem efeito em votos:** indistinguível de H0.
- **Teste principal:** z robusto da virada do T02 (resíduo contra a mediana do município) nas seções do 1º turno de 2026 com caso T36, contra as demais. Média, fração com |z| > 3 e sentido. Permutação dentro da UF, 10.000 sorteios.
- **Critério fixado antes:** "deslocamento" se p bilateral < 0,01 e |diferença da média de z| ≥ 0,3. "Sem deslocamento detectável" se p ≥ 0,01. Poder: com n ≈ 186, a média de z tem erro padrão de ~0,08, então desloca ≥ 0,3 seria visto.
- **Validação:** os 75 casos do 2º turno de 2026, separadamente.

## Caso C: contingências de urna justificadas pelos registros (T34, T16, T30)
- **Explicação atual:** urna substituída, voto por recuperação de dados (RED) ou Sistema de Apuração, conforme o log, o certificado e a tabela de correspondência do TSE.
- **Dependência:** a "substituição" é inferida do próprio log (mais de uma urna com votos no log), do certificado do arquivo diferente da urna do log ou do campo de origem do boletim. Todos são registros do mesmo sistema.
- **Observações esperadas:**
  - **H0:** a votação nessas seções é como a do município.
  - **H1 ou H2 que usem a contingência como cobertura para alterar votos:** deslocamento direcional da virada.
  - **H3:** divergência entre arquivos da seção. Já há um exemplo: RS 88013/2/199, 2022, imagem do BU × bu.dat.
- **Conjunto:** seções com `urnas_com_voto_no_log` ≥ 2, ou `cert_igual_log` falso com certificado lido, ou origem RED ou Sistema de Apuração. Lido dos parquets por urna; turno 2.
- **Teste principal:** o mesmo do caso B, no 2º turno de 2026.
- **Critério:** "deslocamento" se p < 0,01 e |diferença da média de z| ≥ 0,1.
- **Validação:** 2022, 2º turno, mesmo critério.
- **Documental:** o caso RS 88013/2/199 entra como divergência objetiva preservada, com as hipóteses H0 (troca de urna: imagem parcial da primeira urna) e H3, e o que as distinguiria: o BU impresso afixado na seção, ou o log com o evento de troca e a contagem.

## O que nenhum dos casos distingue
H2 global, isto é, comprometimento do software ou da geração que produza registros coerentes e totais coerentes em toda parte, não é distinguível de H0 com dados públicos. Distinguir exigiria evidência independente da urna: boletins impressos fotografados por terceiros, auditoria de código e de integridade da urna, ou a cadeia de certificados até uma âncora verificada. Isso fica registrado como não identificável, não como refutado.
