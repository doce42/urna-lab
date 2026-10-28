# 01. Mapa de confiança dos dados

Para cada fonte: quem produz, quem publica, quem captura, quando, que hash existe, que sistema compartilha, o que prova e o que não prova. "Mesma origem" quer dizer: gerado pela mesma urna ou pelo mesmo sistema do TSE.

| Fonte | Produzida por | Publicada por | Capturada por, quando | Hash disponível | Origem compartilhada com | Prova | Não prova |
|---|---|---|---|---|---|---|---|
| Tabelas de dados abertos (resultado por seção, bweb) | totalização do TSE a partir dos BU recebidos | TSE (dados abertos) | este projeto, 27–28/10/2026 | SHA-256 local (manifesto); hash oficial em 331 de 51.883 arquivos | BU (mesma cadeia TSE) | a soma publicada é a dos boletins publicados | que o boletim reflita o voto |
| BU eletrônico (`bu.dat`) | urna, ao fechar a seção | TSE (pacote por UF; arquivos individuais de SP no 2º turno) | este projeto, 27–28/10 | SHA-512 dentro da lista assinada pela urna | RDV, imagem, log, tabela | o arquivo não foi alterado depois de assinado pela chave embutida | quem controla a chave, nem a fidelidade do conteúdo |
| BU impresso (imagem de texto, `imgbu`) | urna (impressora) | TSE (pacote) | idem | idem | BU, RDV | texto do boletim = BU digital | o que o eleitor digitou |
| **BU impresso, QR Code lido por terceiros** | urna (impressão na seção); leitura por cidadãos | projeto de totalização paralela (arquivos estáticos abertos) | este projeto, baixado em 28/10/2026 (SHA-256 em `externo/.../SHA256SUMS.txt`) | `hash_final` = SHA-512 do conteúdo (conferido); assinatura da urna no próprio QR | mesma urna (assinatura), **cadeia de obtenção diferente** (não passa pelos arquivos do TSE) | 404 boletins: assinatura válida, cadeia até a AC, votos iguais à tabela e ao BU do TSE | veracidade do que a urna registrou; vale só para 404 seções de conveniência |
| RDV (registro digital do voto) | urna | TSE | idem | SHA-512 na lista assinada | BU, log, tabela | recontagem de votos individuais embaralhados = BU | ligação voto-eleitor (não existe, por sigilo) |
| Log da urna | urna | TSE | idem | idem | BU, RDV | eventos e horários de operação, compatíveis com BU | veracidade (é a urna que escreve) |
| Lista assinada (`vota.vsc` / `.vscmr`) | urna | TSE | idem | assinatura Ed521 ou ECDSA P-521 | todos os arquivos da urna | os arquivos listados são os que a urna assinou | quem era o assinante |
| Certificado da urna | AC UE2020, AC UE2022 ou AC URNA | embutido na lista | extraído em T60a | SHA-256 do certificado | lista assinada | pertence à cadeia da AC emissora (T60a) | autenticidade da raiz |
| Certificados das ACs | TSE | TSE publica (página bloqueada a este ambiente: HTTP 403) | cópia de terceiro (DataUrnas-BR); SHA-256 em `fase2/externos/` | SHA-512 oficial só citado por terceiro | — | assinatura dos certificados de urna | origem da raiz: **AC RAIZ UE, AC RAIZ UE v2 e AC URNA v2 não são públicas** (segundo o projeto de terceiro) |
| Capturas do Internet Archive | terceiro (Internet Archive) | idem | 2022 e 2026, 39 instantes | hash do arquivo capturado | conteúdo do TSE | versão publicada pelo TSE naquele instante | voto fiel |
| Totalização do Sistema de Apuração (`busa`, `logsa`) | sistema de apuração do TSE (seções apuradas fora da urna) | TSE | idem | lista assinada (ECDSA/Ed521 de AC UE2020) | tabela | 159 seções-turno de 2022 conferem | independência |
| DataUrnas-BR | terceiro (MIT) | GitHub | consulta em 28/10/2026 | — | mesma origem TSE; **implementação independente** | decodificação independente (R1-20) e coerência em 941.987 seções de 2022 | veracidade; a cadeia lá foi validada só em 5% das seções |
| Auditoria do TCU sobre a totalização de 2022 | TCU (instituição externa) | TCU, via imprensa | lida só pela notícia (dez/2023) | — | dados do TSE | 1.163 boletins conciliados por instituição externa; resultados confirmados | não foi lido o relatório; não é reproduzível aqui |
| Teste de integridade (votação paralela) | TSE, com acompanhamento | TSE | **página bloqueada (HTTP 403)**; só notícia em 2026 | — | TSE | procedimento com votos conhecidos em 26 capitais e DF | resultado não obtido: não usado |
| Lista de hashes de chaves de QR Code por UF (2022) | TSE | TSE (29/08/2022) | arquivo local (`dados/brutos/doc/`) | próprio arquivo | — | âncora publicada antes da eleição para a chave do QR | não usada: o QR de 2026 é assinado pela chave da urna, não por chave por UF |

## Regras de independência aplicadas
- BU + RDV + log + imagem + lista da mesma urna são **uma** origem. A concordância entre eles é consistência interna (T01, T17b, Q1 a Q3).
- Uma decodificação feita por terceiro (DataUrnas-BR) é independente na **implementação**, não na **origem**.
- Um snapshot do TSE guardado por terceiro prova a **versão publicada** naquele instante, não o voto.
- Um boletim impresso lido por cidadãos tem **cadeia de obtenção diferente**: não depende de o TSE ter publicado o arquivo. Mas a assinatura é da mesma urna, e a amostra é de conveniência.
- Hash correto ≠ assinatura válida ≠ cadeia autenticada ≠ voto fiel à intenção do eleitor (T60b mede cada degrau).

## Busca por evidência externa independente (feita em 28/10/2026)
Critérios: fonte que não dependa de o TSE ter publicado o arquivo; dado primário (não notícia, não declaração); disponível por canal público sem contornar bloqueio.

| Busca | Onde | Resultado | Uso |
|---|---|---|---|
| Cadeia de certificados do TSE (AC RAIZ UE, AC URNA v2) | busca na web; página oficial `dpc.acue2020.tse.jus.br`; repositório DataUrnas-BR | a página oficial lista a cadeia, mas **responde HTTP 403 ("Access Denied") a este ambiente, inclusive via `curl`; o bloqueio não foi contornado**. Segundo o projeto de terceiro, as raízes (AC RAIZ UE, AC RAIZ UE v2) e a AC URNA v2 **não são públicas**; só AC URNA, AC UE2020 e AC UE2022 | as 3 ACs disponíveis (cópia de terceiro, `fase2/externos/certificados/`) entram no T60a; a raiz continua sem verificação |
| Resultado do teste de integridade (votação paralela com votos conhecidos) de 2022 e 2026 | busca na web; página do TSE | só a notícia do teste de 2026 em 26 capitais e DF; **a página do TSE responde HTTP 403**; resultado de 2022 não encontrado | **não usado**: sem número de urnas testadas nem divergências obtidos |
| Boletins impressos lidos por terceiros (QR Code) | busca na web; app de totalização paralela de terceiros, que publica arquivos estáticos abertos | **404 boletins do 2º turno de 2026, 22 UFs** (`externo/arvor_totalizacao/`) | **T61** |
| Outro conjunto de boletins de terceiros (um projeto independente cita 38 do 1º turno) | citado em DataUrnas-BR | os dados não foram encontrados | não usado |
| Apuração independente do TRE-SC (QRTot) e aplicativo oficial "Boletim na Mão" | busca na web | são ferramentas, não conjuntos de dados públicos | não usadas |
| Auditoria do TCU da totalização de 2022 | notícia (Gazeta do Povo, 26/12/2023) | 1.163 boletins (559 do 1º turno e 604 do 2º) conciliados por instituição externa; resultados confirmados; falhas pontuais de comunicação e leitura de QR Code. **O relatório em si não foi lido** | não usada como número; citada como existência de uma auditoria externa, sem reprodução |
| Capturas históricas da divulgação | Internet Archive (já em uso) | 39 instantes | Q6, P4, Q14 |
| Estudo acadêmico sobre o ecossistema da urna (SBSeg) | encontrado na busca | não lido nesta operação | — |

**O que a ausência de fonte deixa sem teste:** a hipótese de comprometimento **anterior** à geração dos registros (H-D, H10) só pode ser separada de registros genuínos com boletins impressos de **amostra probabilística** (lista de seções sorteada antes) ou auditoria independente do software da urna. Não foi encontrada nenhuma. Os 404 boletins de terceiros cobrem 0,08% das seções, de conveniência, e não substituem isso. Nenhuma simulação adicional sobre os dados oficiais foi usada como substituta.
