# Protocolo do estudo

**Diretriz de referência:** `DIRETRIZ.md` (nível mais alto; este protocolo a operacionaliza).

**Título:** Integridade, comportamento eleitoral e testes forenses na eleição presidencial brasileira de 2026 (1º e 2º turno), com 2022 como referência.

**Escrito em:** 27/10/2026, 19h55, **antes** de rodar os módulos B a F.

**Por que antes:** um teste escolhido depois de ver o resultado encontra padrão em qualquer eleição. Mudanças posteriores a este protocolo ficam registradas na seção 8, com data e motivo.

**Postura:** o estudo não parte de hipótese sobre quem ganhou, nem de suspeita sobre o sistema. Ele descreve o comportamento observado, define o comportamento esperado a partir de modelos explícitos e mede as divergências. Cada divergência só é chamada de anomalia depois de esgotadas as explicações por artefato, geografia, demografia e comportamento conhecido.

## 1. Perguntas

- **Q1 (integridade):** os dados publicados são íntegros e consistentes entre si, urna por urna, e com o que cada urna gravou e assinou?
- **Q2 (comportamento):** como o eleitor se comportou em cada turno?
  - Quem votou e quem se absteve.
  - A que horas votou.
  - Como o voto se distribui por região, tamanho de município e perfil demográfico.
- **Q3 (mudança):** o que mudou do 1º para o 2º turno?
  - Para onde foram os votos dos candidatos eliminados.
  - Quem deixou de votar ou passou a votar.
  - Onde a virada foi maior ou menor, e por quê.
- **Q4 (forense):** os testes da literatura (da clássica à atual) encontram assinatura de manipulação? Com que poder e com que taxa de falso alarme?
- **Q5 (divergências):** onde o observado se afasta do esperado, em qualquer nível (seção, local de votação, zona, município, estado)? As divergências se agrupam no espaço, no tempo ou por tipo de urna? Qual é a explicação mais simples de cada uma?
- **Q6 (referência):** os mesmos números, em 2022, mostram o mesmo padrão?

## 2. Comportamento esperado (modelos nulos)

O "comportamento esperado" não é um palpite. É o que cada modelo abaixo prevê sem manipulação, e cada teste diz qual modelo usa.

| Código | Modelo | O que prevê |
|---|---|---|
| N1 | Contagem como sorteio (binomial/multinomial por seção) | Variação puramente aleatória dado o tamanho e a proporção da seção |
| N2 | Persistência do eleitor | O voto de cada seção no 2º turno é o do 1º turno mais uma virada comum ao município (ou ao estado) |
| N3 | Transferência de votos | O 2º turno é o 1º turno redistribuído: cada grupo de eleitores (de cada candidato, branco/nulo, abstenção) se divide entre os finalistas com proporções estimadas dos dados (inferência ecológica) |
| N4 | Perfil demográfico | Idade, escolaridade e sexo da seção explicam parte do voto e do comparecimento |
| N5 | Ordem de chegada aleatória dentro do município | A hora em que a urna chega não tem relação com o voto |
| N6 | Referência histórica | 2022 com o mesmo código |
| N7 | Integridade criptográfica | Toda urna tem lista assinada válida; hash, RDV, log e boletim batem |

## 3. Módulos e testes

| Módulo | Testes (numeração do CATALOGO) | Modelo nulo | Situação em 27/10 19h55 |
|---|---|---|---|
| A. Integridade | T01, T14–T17, T24 | N7 | Em andamento (Brasil inteiro) |
| B. Comportamento | C01 comparecimento por perfil e região; C02 hora do voto (logs); C03 voto × perfil demográfico; C04 voto × tamanho do município e região; C05 modelo de urna × voto (T20) | N4, N5 | A fazer |
| C. Mudança entre turnos | C06 matriz de transferência de votos (inferência ecológica, dentro do município); C07 mudança de comparecimento × perfil; C08 geografia da virada | N2, N3 | A fazer |
| D. Forense | T02–T13, T21, T22; T25 impressão digital 2D de Klimek com curtose; T26 2º dígito de Benford (Mebane), com ressalvas; T27 dígitos de branco, nulo e comparecimento; T23 classificador com fraude sintética (Zhang, Alvarez e Levin) | N1, N2, N5 | Parcial |
| E. Divergências | E01 resíduos em vários níveis (seção, local, zona, município, UF); E02 agrupamento espacial dos resíduos (local de votação e município); E03 lista das maiores divergências com explicação | N2–N4 | A fazer |
| F. Referência | Toda a bateria em 2022 | N6 | Parcial |

## 4. Critérios fixados antes

- **Significância:** α = 0,01 por teste. Com muitos testes, controle de taxa de falsas descobertas (Benjamini-Hochberg, q = 0,05) quando houver famílias de testes (por UF, por município).
- **Tamanho de efeito:** sempre reportado (pontos percentuais e votos). Um efeito "significativo" com menos de 0,1 ponto é descrito como desprezível.
- **Anomalia:** divergência que (a) passa do limiar, (b) não se explica pelos modelos N1–N4 nem por artefato conhecido e (c) se repete em pelo menos dois testes independentes.
- **Calibração:** todo teste forense novo é rodado (a) nos dados reais, (b) em 2022 e (c) com fraude sintética injetada (poder). Teste que acusa dado limpo não entra na conclusão.

## 5. O que o estudo não pode responder
- **Em quem cada eleitor votou e a que horas:** o voto é secreto e o RDV é embaralhado.
- **Manipulação uniforme do software antes da eleição:** o mesmo percentual em todas as urnas não deixa diferença entre urnas. A integridade criptográfica (módulo A) mostra que os arquivos são os que as urnas assinaram, mas não audita o software que as urnas rodaram. Isso cabe ao teste de integridade e à verificação de software do TSE, fora dos dados públicos.
- **Causalidade de comportamentos:** as relações com perfil e geografia são associações, não causas.

## 6. Dados
Só dados oficiais do TSE (lista e conferências em CATALOGO, seção 2). Nada estimado onde existe dado medido.

## 7. Produtos
- `relatorio.html` + PDF: para leigos, visual, com o rigor preservado.
- `METODOLOGIA.md`: completo, com a matemática de cada teste.
- `CATALOGO.md`: trilha de auditoria.
- `PIPELINE.md`: reprodução.
- `REFERENCIAS.md`: bibliografia.

## 8. Mudanças no protocolo
- **27/10/2026, 20h10, emenda 1, antes de rodar.** Revisão de cobertura: os logs estavam sendo usados só para contar votos, e a assinatura mais citada de fraude local no Brasil (mesário habilitando eleitor ausente) aparece na **sequência** de eventos do log. Acrescentados:
  - **T17b:** decodificação do `bu.dat` (o arquivo somado na totalização) × RDV × publicado.
  - **T28:** rajadas de habilitação sem biometria perto do encerramento.
  - **T29:** intervalos entre habilitação e voto, e entre eleitores (mínimos fisicamente plausíveis).
  - **T30:** votos fora do horário legal (abertura, encerramento, prorrogação).
  - **T31:** voto computado sem habilitação anterior.
  - **T32:** soma das urnas × totais oficiais divulgados (BR, UF e município).
  - **T33:** versão do software, verificações de assinatura de aplicação e carga, urna por urna.
  - **E02:** agrupamento espacial das divergências (Moran's I e excesso de variância por local de votação e zona).
  - **Benjamini-Hochberg** em todas as famílias de testes.

  Critério de anomalia e limiares: os mesmos da seção 4.
- **27/10/2026, 20h20, emenda 2, autoauditoria (AUTOAUDITORIA.md).** Acrescentados:
  - **T34:** correspondência esperada × efetivada (dados abertos do TSE) × urna do certificado e do log.
  - **T35:** logs do GEDAI: carga registrada de toda urna usada.
  - **T13b:** poder dos testes de log com "eleitor fantasma" sintético.
  - **Cobertura:** urnas processadas × urnas do boletim, por UF.

  A conclusão final passa a separar três tipos de afirmação: prova determinística, evidência estatística com poder medido e limite dos dados públicos.
- **27/10/2026, 20h35, emenda 3, incorporação da DIRETRIZ.md.** Sem interromper processos e sem mudar resultados já obtidos.
  - Todo resultado recebe:
    - classe de evidência A–G;
    - tipo de afirmação (determinística, estatística, fora do alcance);
    - independência da verificação (interna, criptográfica, externa);
    - natureza (exploratório ou confirmatório).
  - O critério de anomalia (seção 4c), "repete em pelo menos dois testes independentes", passa a exigir **dados de origem diferente** (tabelas de votação × arquivos das urnas × assinatura), e não dois testes sobre o mesmo resíduo.
  - Achados exploratórios do módulo E só sobem de classe após confirmação em dados não usados na descoberta (logs das urnas, 2022 ou metade aleatória de municípios com semente fixa).
  - Lacunas e melhorias em AUTOAUDITORIA, seção 5.
- **28/10/2026, emenda 4, resposta à revisão independente R1 (Codex).** Não muda nenhum resultado congelado da V1.0-rc1.
  - **Pré-registro, de forma honesta:** os testes rodados antes deste protocolo (19h55 de 27/10) são marcados `anterior_ao_protocolo` no registro e não são tratados como pré-registrados, mesmo que tenham o rótulo "confirmatório".
  - **Moran's I:** citado acima, nunca foi implementado. O E02 mede agrupamento por local de votação, não autocorrelação espacial. A implementação com vizinhança é a pergunta P9 da Fase 2.
  - **Independência:** "dados de origem diferente" não garante erros independentes. Tabelas, BU, RDV e log vêm do mesmo equipamento ou da mesma cadeia de publicação. No 2º turno, testes sobre os dois candidatos são matematicamente dependentes (T21, T22). A conclusão não soma testes favoráveis, e a regra conjunta passa a ser avaliada por simulação (P2).
  - **Calibração:** o critério que torna um teste inadequado para o dado é fixado antes de olhar o resultado. Detecções em dados reais são achados, não falsos positivos.
  - **Não detecção:** não demonstra equivalência. Afirmações de "igual" exigem margem de equivalência definida antes (P7).
  - **Perguntas novas:** a partir daqui, só entram pelo [`FASE2.md`](FASE2.md), registradas antes de rodar.
- **28/10/2026, emenda 5, primeira sessão da Fase 2.** Pré-registro em `fase2/sessao_limitada_2026-10-28/PREREG.md`, escrito antes das execuções. Entram:
  - **T37:** o C06 sob heterogeneidade sintética (P1);
  - **T38:** assinatura de comparecimento nas seções pró-Lula atípicas (hipótese de enchimento, derivada do T02, exploratória);
  - **T39:** verificação de 20 seções do 1º turno (seleção fixada antes).
- **28/10/2026, emenda 6, Fase 3 e sua revisão (registrada depois das execuções).** O AGENTS.md exige emenda aqui **antes** de um teste novo. Na F3 os pré-registros foram escritos fora deste arquivo, antes de rodar: `fase3/PREREG.md` (T40 a T43) e `fase3/PREREG_REVISAO.md` (I1 a I3). Esta emenda só registra o que já foi feito, com data, e não deve ser lida como pré-registro. Testes e verificações:
  - **T40 (curvas de apuração):** nulos de permutação da ordem de chegada (irrestrito, por UF, por município, UF × hora de encerramento, UF × hora × tamanho). Nenhum é calibrado, nem em 2022, e o T40 é descritivo. A ordem usada é a hora de recebimento do boletim (reconstrução retrospectiva), não a curva divulgada.
  - **T41 (zeros de votos):** exploratório. Nenhum modelo de frequência de zeros passou na calibração, e não se afirma excesso nem ausência de excesso.
  - **T42 (Moran's I):** mede dependência espacial entre municípios; não distingue causa.
  - **T43 (reconciliação com decodificação de terceiro):** interna quanto à origem (TSE), independente quanto à implementação.
  - **I1 (poder contra trocas concentradas):** mundos de calibração e de avaliação separados. Alarme estatístico ≠ detecção correta: a regra conta alarme em qualquer sentido. Municípios maiores que 1% das seções (São Paulo, Rio, Brasília, Fortaleza, Salvador) não entram no mecanismo por município.
  - **I2 (zeros com modelo calibrado):** o critério de calibração fixado antes não foi cumprido. O critério para controles com dezenas de milhares de zeros era quase impossível de cumprir e precisa ser refeito antes de nova tentativa.
  - **I3 (locais contra o entorno):** a referência é a zona eleitoral (divisão administrativa), não uma vizinhança geográfica.
  - **A173, BU1, SA22:** verificações documentais dos arquivos de 2022 (sem estatística).
- **28/10/2026, emenda 7, alegações da live de 4/11/2022 e do pedido do PL (antes de rodar).** Pré-registro em `fase3/PREREG_LIVE_2022.md`; contexto em `docs/pesquisas/2026-10-28_live_cerimedo_2022.md`. Entram:
  - **T45:** ligação log → BU → RDV nas urnas com o ID fixo 67305985 (2022 e 2026).
  - **T46:** reprodução dos 51,05% "só UE2020" e contrafactual dentro do município.
  - **T47:** voto em Lula por modelo de urna no nível (1º e 2º turno), dentro do município e do local de votação, margem ±0,02 logit, calibração por permutação e poder com fraude sintética.
  - **T48:** versão do software e seções unânimes por modelo.
- **28/10/2026, emenda 8, seções com zero voto para Flávio no 2º turno (antes de rodar).** Pré-registro em `fase3/PREREG_ZEROS_FLAVIO.md`. Entra o **T49:** reprodução da alegação de 106 seções e 211 municípios virados, comparação com 2022, continuidade seção a seção e integridade dos arquivos.
- **28/10/2026, emenda 9, thread "concentração do voto no PT" (antes de rodar).** Pré-registro em `fase3/PREREG_THREAD_CONCENTRACAO.md`. Entra o **T50:** reprodução descritiva de seções acima de 80% por candidato (2022 e 2026), região, continuidade e saldo por seções vencidas.
- **28/10/2026, emenda 10, crescimento entre turnos por município (antes de rodar).** Pré-registro em `fase3/PREREG_CRESCIMENTO_ENTRE_TURNOS.md`. Entra o **T51:** fração de municípios e UFs em que cada candidato cresceu mais que o rival entre os turnos, 2022 e 2026.
- **28/10/2026, emenda 11, postagens de Leonardo Dias/arvor.co (antes de rodar).** Pré-registro em `fase3/PREREG_POSTS_ARVOR.md`. As alegações já cobertas respondem com T09, T12, T28, E02, T39 e Q1. Entram: **T52** (intervalo emissão → recebimento do BU e votos após 17h), **T53** (liberações sem biometria no 2º turno, 2026 × 2022), **T54** (municípios em que cada finalista perdeu votos entre turnos, 2026 × 2022).
- **28/10/2026, emenda 12, Cabo Frio e cidades citadas (antes de rodar).** Pré-registro em `fase3/PREREG_CABO_FRIO.md`. Entra o **T55:** reprodução, decomposição pelos votos disponíveis, posição na distribuição nacional (2026 × 2022) e integridade dos arquivos.
- **28/10/2026, emenda 13, brancos e nulos entre turnos (antes de rodar).** Pré-registro em `fase3/PREREG_BRANCOS_NULOS.md`. Entra o **T56:** reprodução pela linha de brancos e nulos do C06, totais por turno, excesso de brancos e nulos no 1º turno de 2026 sobre 2022 nas mesmas seções e sua relação com o voto em Lula.
- **28/10/2026, emenda 14, nulos de presidente e 2º turno de governador (antes de rodar).** Pré-registro em `fase3/PREREG_NULOS_GOVERNADOR.md`. Entra o **T57:** brancos e nulos do 2º turno por grupo de UF (com e sem 2º turno de governador), 2022 × 2026, contrafactual de composição e resíduo nas UFs sem governador.
- **28/10/2026, emenda 15, rodada 7: dígitos dos nulos no RDV e calibração do C06 (antes de rodar).** Pré-registro em `fase3/PREREG_RDV_NULOS.md`. Entram o **T58** (classes do número digitado nos nulos de presidente, 2022 e 2026, dois turnos) e o **T59** (Goodman do C06 contra destino de origem quase conhecida: nulo com número de candidato eliminado).
- **28/10/2026, emenda 16, Operação Veracidade Geral e a hipótese do vídeo (escritas antes de rodar, no protocolo próprio da operação).** Pré-registro, emendas internas 1 a 4 e T65 em `operacao_veracidade/PROTOCOLO_PRE_EXECUCAO.md`. Entram: **T60a** (cadeia de certificados em 100% das urnas), **T60b** (controles positivos e negativos do verificador), **T61** (boletins impressos de terceiros e republicação), **T62** (identificabilidade: experimentos A e B), **T63** (poder da bateria contra 15 mecanismos adversariais e fabricação coerente), **T64** (zeros: três famílias de modelo) e **T65** (hipótese dos "votos extras"). Mudanças de desenho durante a execução do T63 estão declaradas como emendas 1 a 4 naquele arquivo.
- **28/10/2026, emenda 17, rodada 8 (ABERTA): "Relatório Pericial Independente" (antes de rodar).** Pré-registro em `fase3/PREREG_RELATORIO_PERICIAL.md`. Entram as medidas R1 a R9 (totais, divisão por hora de encerramento, faixas, estados após 19h, liberação sem biometria, correlação com Lula, unanimidade, Benford do primeiro dígito, disponibilidade dos arquivos); R10 fica fora do escopo dos dados do TSE. A rodada 8 não será congelada sem aprovação explícita do responsável.
  - **Resultados da rodada 8 (registrados depois de rodar, no registro vivo; rodada em aberto):** T66 (divisão por hora de encerramento, R2, R3, R4 e R2b), T67 (liberação sem biometria, R5 e R6), T68 (unanimidade, R7), T69 (Benford do primeiro dígito, R8) e T70 (disponibilidade dos arquivos, R9) e, pela emenda 18, T71 (curvas dos dois turnos sobrepostas, C1 a C5). O R2b e a conferência de fuso (e) são **exploratórios**, feitos depois de ver o R2 e declarados no adendo do pré-registro.
- **30/10/2026, emenda 18, rodada 8 (ABERTA): "curvas do 1º e do 2º turno sobrepostas" (antes de rodar).** Pré-registro em `fase3/PREREG_CURVAS_SOBREPOSTAS.md`. Entra o **T71** (Q57): reprodução das curvas acumuladas por ordem de recebimento e dos números do vídeo (C1), conta da "projeção" deslocada (C2), premissa de ordem aleatória (C3), semelhança das curvas em 2026 e 2022 (C4) contra ordens independentes e contrafactual estrutural 1º turno + virada (C5). A rodada 8 continua aberta.
