# Proposta de termo de encerramento condicionado da F3

> **Situação:** proposta revisada pelo responsável. Depois dela, a pedido do responsável, a F3 executou as investigações de resolução, a auditoria adversarial, o veredito de 2026 e as investigações finais (ver `RESPOSTAS_F3.md` e `VEREDITO_2026.md`, que prevalecem sobre este termo onde forem mais recentes). **Aprovada e congelada como V1.3 (rodada 5) em 28/10/2026.**
> **Base:** commit publicado `96f48a9` (28/10/2026). Inventário de 33 itens com evidência por item em [`fase3/INVENTARIO.md`](INVENTARIO.md) e `fase3/inventario.json` (campo `evidencia_arquivos`). Relatórios: [`AUDITORIA_F3.md`](AUDITORIA_F3.md), [`RELATORIO_ACEITACAO_F3.md`](RELATORIO_ACEITACAO_F3.md), [`PARECER_CONSOLIDACAO_F3.md`](PARECER_CONSOLIDACAO_F3.md), [`RELATORIO_VERIFICACOES_FINAIS_F3.md`](RELATORIO_VERIFICACOES_FINAIS_F3.md).
> **Leitura:**
> - **Simulações:** os números de simulação (poder de detecção) são de votos **sintéticos**, inseridos para medir o que a bateria veria. Não são votos encontrados nos dados.
> - **Alcance das taxas de detecção:** valem só para os cenários, réplicas e critérios avaliados (30 réplicas por cenário; 6 por cidade nas grandes cidades; limiar calibrado; detecção contada no sentido certo).
> - **Concordância entre registros:** BU, RDV, imagem, log e tabelas é **consistência documental entre registros publicados**. Não autentica o processo de votação como um todo.
> - **Fraude:** nada neste termo é veredito global sobre fraude.

## 1. Achados demonstrados

### Consistência documental e verificação criptográfica (determinísticas)
O que estas verificações mostram é que os registros publicados são coerentes entre si e que os arquivos presentes têm assinatura válida até a autoridade emissora. Elas não mostram que o processo de votação seja autêntico em todas as suas etapas (seção 5).
1. **2026:** a tabela publicada pelo TSE, o boletim de cada urna (BU, `bu.dat`) e a recontagem voto a voto do RDV coincidem nos votos de Presidente em todas as urnas eletrônicas com arquivos (1º turno: 499.176; 2º: 499.178). As duas tabelas públicas coincidem seção a seção. A soma das urnas coincide com o total oficial em 638 de 638 itens de voto e comparecimento. (T01, T15, T17b, T32)
   - **O que é:** consistência entre registros gerados ou publicados pela mesma cadeia (urna e TSE).
   - **O que não é:** verificação independente do que foi votado.
   - **Eleitorado do exterior:** diferença de −495 e −525, explicada no P12.
2. **2026, 1º turno:** a tabela publicada coincide com a decodificação dos boletins feita por terceiro (DataUrnas-BR, commit 12f0433) em 499.206 de 499.206 seções. A independência é de implementação, não de origem: os dois leem os arquivos publicados pelo TSE. (T43)
3. **2022:** a mesma comparação, independente quanto à implementação, cobre 99,96% das seções do Brasil, sem nenhuma diferença nos votos de Presidente. As seções sem par foram lidas pelo projeto e conferem: 27 do Sistema de Apuração, 333 numa lacuna do acervo do terceiro na Bahia e 7 que ele registra fora do banco. (A1)
4. **Assinatura e hash válidos até a autoridade emissora:** em 2026, nos arquivos presentes de todas as urnas. Em 2022, nos arquivos presentes e nas 159 seções-turno do Sistema de Apuração, conferidas à parte. Isso mostra que os arquivos presentes não foram alterados depois de assinados pela chave da urna. **Não verifica:** a ligação dessa chave a uma âncora do TSE (P11), nem o que aconteceu antes da assinatura. (T14 a T16, SA22)
5. **Publicação de 2022:** 173 arquivos (RDV, log e imagem do BU de 64 seções, 54 delas do exterior) constam com nome, tamanho e SHA-512 das listas de arquivos assinadas pelas urnas (`.vscmr`), cuja assinatura foi verificada. Esses arquivos não estão no pacote de dados abertos, nas duas cópias baixadas com 13 dias de diferença.
   - **Não verificados:** o conteúdo dos 173 arquivos não foi verificado, porque eles não estão disponíveis. O que está demonstrado é que foram listados e assinados e que estão ausentes do pacote, não o que contêm.
   - **Auxiliares:** também constam das listas assinadas, e faltam no pacote, 485 arquivos auxiliares (`.hash`, `.ver`, `.chvtp`, `.jufa`) das seções do Sistema de Apuração.
   - **Boletins:** os BUs presentes dessas seções coincidem com a tabela publicada.
   - **Conclusão:** **é uma inconsistência objetiva de publicação, de causa desconhecida, sem divergência de votos entre os registros disponíveis.** (A173, SA22)
6. **Seção MG 49050/196/173 (2022):** boletim do Sistema de Apuração, lido e coincidente com a tabela, com assinatura válida. Com ela, nas 486 seções-turno com zero votos para um finalista, os registros disponíveis (BU, RDV, imagem, tabela) são consistentes entre si. (BU1, Z1)
7. **Contas entre turnos:** o crescimento de votos entre turnos fecha exatamente com eliminados, brancos, nulos e comparecimento, em 2022 e 2026. (C06, T37)

### Evidência estatística (com poder ou limite medido)
8. **Assimetria de cauda do T02:** é real nos dois anos (bootstrap por município). Em São Paulo capital, em 2022, ela se concentra no nível da zona eleitoral: a 251 tem o 2º maior desvio médio entre 58 zonas, e a 259 o 7º. Não está concentrada nos locais. **Causa desconhecida.** (P17, P14, P20, I3)
9. **Dependência espacial entre municípios:** Moran's I de 0,16 a 0,20, com p = 0,001, nos dois anos. (T42)
10. **Locais de votação atípicos:** cerca de 0,1% dos locais, por três métodos. A lista específica depende do método. (E02, P9, I3)
11. **Alcance de detecção no sentido certo, nos cenários simulados:** 4 mecanismos (disperso, locais, municípios, região) mais o município inteiro das 5 maiores cidades; cerca de 1% das seções; 2%, 5% e 10% dos válidos; dois sentidos; 30 réplicas; limiar calibrado em 20 mundos à parte; critério fixado antes.
    - **Detectada em 30 de 30 réplicas:**
      - troca dispersa de 10% dos válidos (~123 mil votos);
      - troca concentrada de 5% (~62 mil) em locais ou em municípios de até ~5 mil seções.
    - **Detectada em 0 (ou 1) de 30 réplicas, ou seja, não detectada nesses cenários:**
      - 2% (~25 mil votos), nos quatro mecanismos (no máximo 1 de 30, num caso, com o E02 completo);
      - 5% dispersos.
      - Isso não estabelece um limite geral: outros arranjos do mesmo tamanho não foram testados.
    - **Município inteiro das 5 maiores cidades (6 réplicas por cidade e sentido):**
      - a 10% (155 mil a 696 mil votos), 10 a 13 de 30 pelo E02 completo;
      - 0 de 12 em Brasília e Fortaleza.
      - Detecção não confiável nesses cenários.
    - **Falso alarme no sentido certo:** 0 de 30 mundos sem troca (IC 95% até 11%). (P18, I1, A2)
12. **Rajada sem biometria (T28):** pelo critério beta-binomial da F2, 8 de 13 urnas do 1º turno de 2026 seguem sinalizadas, somando 99 votos. O mesmo método também sinaliza 23 e 25 urnas em 2022, então o padrão não é específico de 2026. (P10, A4)
13. **Equivalências e efeitos desprezíveis,** cada um restrito ao desfecho, à margem e ao universo testados (fora disso, nada se afirma):
    - **Modelo de urna (P5):**
      - Desfecho: resíduo da virada entre turnos, em logit, comparado dentro do município.
      - Universo: 2º turno, seções com pelo menos 20 válidos, municípios com 2 ou mais modelos (1.436 em 2026, com 233.433 seções; 1.779 em 2022).
      - Resultado: intervalos de 95% (bootstrap por município) dentro de ±0,02 logit para todos os modelos. Maior efeito: +0,004 logit (UE2013, 2026; IC 0,001 a 0,007, diferente de zero mas dentro da margem).
      - Ressalva: a margem ±0,02 foi a usada na F2. Não consta registro de que tenha sido fixada antes de olhar.
    - **Urna trocada entre turnos (P7):**
      - Desfecho: z robusto da virada do T02.
      - Margem: ±0,10 z, fixada antes.
      - Resultado: diferença de −0,029 z (IC 90% de −0,054 a −0,003; 4.432 urnas) em 2026 e de −0,008 (−0,023 a +0,008; 12.653 urnas) em 2022.
      - Conclusão: equivalente dentro da margem.
    - **Ordem de chegada × virada (P8):**
      - Desfecho: correlação de Spearman entre a ordem de recebimento no município e o resíduo da virada.
      - Universo: municípios com pelo menos 20 seções (477.108 seções em 2026; 448.270 em 2022).
      - Resultado: r = +0,004 (IC 95% −0,004 a +0,012) em 2026 e −0,028 (−0,040 a −0,019) em 2022.
      - Conclusão: abaixo do critério de efeito desprezível |r| ≤ 0,05 usado na F2. Em 2022 o efeito é diferente de zero.

## 2. Hipóteses e afirmações que perderam sustentação
Cada uma com o que a derrubou. Nenhuma delas, sozinha, demonstra ou exclui manipulação.

| Afirmação ou hipótese anterior | O que mostrou | Evidência |
|---|---|---|
| Razão "4:1" entre abstencionistas como magnitude | Frágil: sob heterogeneidade varia de 1,7 a 11,8; limites de Fréchet admitem de ~0 a 1,7 mi | P1, P15 |
| Enchimento a favor de Lula via comparecimento nas seções atípicas | A assinatura prevista não aparece; isso não exclui troca sem mudança de comparecimento | T38 |
| 766 e 683 locais atípicos (E02 original) | Inflados por correlação dentro do local: 102 e 55 com correção | P9 |
| "O T13 só enxerga o sentido pró-Lula" | Era limitação da regra de uma cauda; com duas caudas é simétrico | P18 |
| "~250 mil votos" no P2 | Erro de conta: ~125 mil | registro T13 |
| T10 e T11 como testes da curva | Nenhum nulo é calibrado, nem em 2022; ficam como descrição | C1, T40 |
| "Curvas de 2026 iguais às de 2022" | Diferem na descrição (mais territorial em 2026; duas trocas no 2º turno) | C2 |
| Zeros: "sem evidência de excesso" | Afirmação sem modelo calibrado, retirada | Z1, I2 |
| Zeros: prior municipal | Refutado (esperado 1 a 8 contra 79 a 160) | E3 |
| Locais de SP como focos isolados | Não são atípicos contra a própria zona; o desvio é da zona | I3 |
| T02 detecta trocas em qualquer escala | Nos cenários de troca no município ou na região inteira (até 10% dos válidos), 0 de 30 detecções do T02 no lado afetado: a mediana municipal absorve o deslocamento | I1, A2 |
| Troca concentrada em municípios detectável a ~62 mil votos | Detectada (30/30) nos cenários com municípios de até ~5 mil seções; nos cenários de município inteiro das 5 maiores cidades, detecção não confiável (a 5%: 0 a 1 de 30 pelo E02 completo) | A2 |
| Troca regional a 5% detectável | Incerta no sentido certo (26/30 e 23/30) | A2 |
| Lacuna das 333 seções de 2022 como "exterior e agregadas" | Lacuna do acervo do terceiro na Bahia | A1 |
| Moran's I "não indica manipulação" | O teste não distingue causa | T42 |

## 3. Perguntas parcialmente respondidas
| Id | Respondido | Em aberto |
|---|---|---|
| P2, P18 | Poder para 4 mecanismos e 3 magnitudes, nos dois sentidos | Mecanismos não simulados; grandes cidades; outras coberturas |
| P3, R1-20 | Tabela = BU de terceiro nas seções comuns | Versões datadas; 2º turno de 2026 sem comparação independente |
| P9 | Ordem de grandeza dos locais atípicos | Causa; vizinhança geográfica (sem coordenadas de locais) |
| P14, P20 | Localização no nível da zona (SP 2022) | Causa do deslocamento da zona 251 |
| M1 | Contas fecham | Fluxos individuais (não identificáveis) |
| C1a, C2 | Descrição das viradas na ordem de recebimento | Viradas na curva divulgada; explicação |
| Z1 | Arquivos conferem em 486/486 | Frequência de zeros: sem modelo calibrado |
| A173 | Listados e assinados, ausentes do pacote de dados abertos; BUs das 64 seções coincidem com a tabela | Conteúdo dos 173 arquivos (não disponível); outro canal do TSE; motivo |
| AUT | Consistência documental e assinatura válida até a AC emissora nos arquivos presentes; lacunas de publicação | Âncora do TSE; fonte externa; etapas anteriores à assinatura |
| MET | Limites de T02, E02, T10/T11, zeros e regra de detecção registrados | Modelos de chegada e de cauda baixa |

## 4. Questões dependentes de evidência externa
| Questão | Fonte necessária | Como obter | O que permitiria verificar |
|---|---|---|---|
| P4, C1, C1a | Snapshots datados da divulgação (2022 e 2026) | arquivos de terceiros com data e hash; pedido ao TSE | Curva divulgada × ordem de recebimento; viradas observadas |
| P6, P21 | Boletins impressos fotografados por terceiros, com proveniência | coletas públicas com lista de seções | Impresso = publicado |
| P11, P21, AUT | Certificados AC URNA v2 e AC RAIZ UE | publicação oficial ou pedido via Lei de Acesso à Informação (LAI) | Cadeia até a âncora do TSE |
| P3 | Versões datadas dos arquivos e tabelas | capturas periódicas; pedido ao TSE | Republicação |
| R1-20 (2º turno de 2026) | Decodificação independente do 2º turno | projetos de terceiros quando publicarem | Comparação independente no turno decisivo |
| A173, SA22 | Situação dos 173 arquivos e dos auxiliares `.hash`, `.ver`, `.chvtp`, `.jufa` | pedido ao TSE via LAI | Se estão publicados em outro canal e por quê |

## 5. Limites dos métodos
- **Fluxos individuais entre turnos:** **não identificáveis a partir dos dados agregados publicados.** Está demonstrado para estes dados pelos limites de Fréchet, que admitem de ~0 a 1,7 mi para a razão entre abstencionistas. Só dados individuais, que não existem por causa do sigilo do voto, mudariam isso.
- **Curvas:** **limitação de método e de dados.** Não há modelo de chegada validado nem snapshots. A curva analisada é reconstrução pela hora de recebimento, não a divulgada.
- **Zeros:** **limitação do método atual.** O modelo falhou na calibração. Não é impossibilidade, mas o critério de calibração precisa ser refeito antes de nova tentativa.
- **Poder de detecção:**
  - Medido só para os mecanismos e tamanhos simulados.
  - Nos cenários avaliados, trocas de ~25 mil votos não foram detectadas.
  - Trocas que preservam medianas ou mexem no comparecimento não foram simuladas, e nada se afirma sobre elas.
  - Nos cenários de município inteiro das 5 maiores cidades, a detecção não foi confiável. Em Brasília isso decorre da construção do modelo por UF.
  - Nos cenários de troca concentrada a 10%, o E02 também acusou locais no sentido oposto em 10% a 80% das réplicas. Nesses cenários, o sinal do E02 sozinho não identificou o beneficiário.
- **Autenticidade:** o projeto verifica a consistência documental entre os registros publicados e a assinatura dos arquivos presentes até a autoridade emissora.
  - **Não verifica:** a autenticidade integral do processo de votação.
  - **Não alcança:** alterações anteriores à geração do boletim (BU, RDV e log saem do mesmo equipamento, então a concordância entre eles não é evidência independente); a origem autenticada até a raiz do TSE; o conteúdo dos arquivos ausentes da publicação.
- **Comparações "independentes":** são independentes de implementação, não de origem (tudo vem do TSE).
- **Processo:** os pré-registros da F3 ficaram fora do PROTOCOLO, e a emenda 6 foi escrita depois e declarada como tal. A V1.2 foi congelada antes da auditoria e preservada, com desvios registrados.

## 6. Condições para reabrir investigações
Uma pergunta encerrada com limitação volta a ser investigada se surgir algum destes itens:
1. **Fonte externa da seção 4:** permite reabrir a pergunta correspondente, com pré-registro antes de olhar os dados.
2. **Divergência objetiva de votos:** entre boletim, RDV, imagem ou tabela, em qualquer seção, inclusive as que hoje estão fora do alcance (arquivos ausentes de 2022).
3. **Erro de leitura ou de processamento:** algo como o leitor de 2022 ou o comparador do E3, que mude um universo de análise. Reabre os testes que usam aquele universo.
4. **Modelo validado:** um modelo de chegada (curvas) ou de cauda baixa (zeros), publicado ou desenvolvido, que passe em controles definidos antes. Reabre C1, C1b e Z1.
5. **Mecanismo concreto e plausível:** uma hipótese de manipulação específica fora dos simulados, com assinatura testável nos dados públicos. Abre uma simulação de poder dirigida.
6. **Pedido do responsável:** para as investigações locais registradas e não executadas.
   - **A3:** perfil do eleitorado da zona 251.
   - **C3:** modelo de cauda baixa para zeros.
   - **Réplicas nas grandes cidades:** mais réplicas do mecanismo de município inteiro.
   - **Leitor de 2022:** estender o leitor geral ao Sistema de Apuração.

## 7. Se o responsável aprovar
Proposta de procedimento, a executar só com autorização expressa:
1. Registrar a aprovação, com data, na linha do tempo e no README, junto com esta lista de limitações aceitas.
2. Congelar a F3 numa nova rodada (proposta: rodada 5, versão V1.3), com `proveniencia.json` e todos os arquivos copiados **antes** de calcular os hashes. A V1.2 permanece como registro do encerramento prematuro.
3. Criar a tag correspondente, publicar e fazer o deploy.
4. Manter as pendências das seções 3, 4 e 6 no inventário, abertas, para a fase seguinte.
