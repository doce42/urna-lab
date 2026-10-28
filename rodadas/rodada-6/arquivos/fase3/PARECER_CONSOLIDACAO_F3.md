# F3: parecer de consolidação científica (28/10/2026)

Auditoria sem teste estatístico novo, sem reexecução de I1 a I3 e sem mudança no leitor geral. As únicas leituras feitas foram três checagens determinísticas pequenas, todas sobre arquivos já gerados:
- **(a)** integridade das versões congeladas;
- **(b)** em que universos de análise de 2022 entraram as 159 seções do SA22;
- **(c)** direção dos alarmes do I1, a partir de `fase3/resultados/rev_i1_*.json`, que já trazia as taxas por lado.

Nada foi publicado. Este arquivo é o único criado nesta sessão, e as correções de texto propostas na seção 11 **não foram aplicadas**.

## 1. Estado atual da F3
- **Commit publicado:** `b25c88e` (`main` = `origin/main`), sem alteração local pendente além deste parecer.
- **Versões congeladas íntegras:** rodadas 1 a 4 conferem com os SHA-256 do próprio `resumo.json` (28, 30, 45 e 30 arquivos, 0 diferenças). Os arquivos acrescentados à rodada 4 depois do congelamento conferem com os hashes de `rodadas/rodada-4-desvio.md`. As pastas `rodada-2`, `rodada-3` e `rodada-4` são idênticas às das tags `v1.0`, `v1.1` e `v1.2` (git diff vazio).
- **F3:** "em revisão" na linha do tempo, no README e na CONCLUSAO. A V1.2 está preservada.
- **Inventário:** 30 itens, sendo 18 trabalhados na F3 e 12 herdados da F2.
  - **Por estado:** 13 respondidas, 12 respondidas parcialmente, 4 bloqueadas por fonte externa, 1 não decidível com os modelos disponíveis.
  - **Fonte:** `fase3/inventario.json`, campo `estado_final`.

## 2. Impacto das 159 seções-turno do SA22
Checagem (b): as 159 chaves de `sa22.csv` foram cruzadas com `analise/brutos/2022_{1,2}t/urnas_*.parquet`, a entrada de todas as análises por arquivo de 2022.

| Universo de análise de 2022 | Usa arquivos de urna? | Deveria incluir as seções do Sistema de Apuração? | Quantas entraram (de 116 no 1º turno e 43 no 2º) | Efeito |
|---|---|---|---|---|
| Testes estatísticos sobre a tabela publicada (T02, E02, T13, C06, zeros, P9, I1 a I3) | não | sim | todas, pela tabela | nenhum: os votos delas estavam no universo |
| T28/T29/T30/T31/T33 de 2022 (`resultado_logs_2022_*`) e P10 de 2022 | sim (sequência do log da urna) | não, salvo as que têm log da urna: o Sistema de Apuração registra cédulas, sem habilitação biométrica | 5 e 4 (as que têm `.logjez`) | denominador declarado (`urnas` = 472.024 e 472.027) inclui as 159 linhas sem log; o denominador efetivo (`urnas_com_sequencia`) está certo. Nenhuma das 15 urnas listadas como exemplo em cada turno é do Sistema de Apuração; as outras 8 e 10 sinalizadas não estão listadas no resultado e não foram conferidas |
| P5 (modelo de urna, 2022) | sim (`modelo`) | não, salvo as com log da urna | 7 e 4 | nenhum sobre a conclusão (equivalência em ±0,02 logit em 1.779 municípios) |
| E3, zeros 2022 (conferência por arquivo) | sim | sim | 0 BU lidos; a única seção do Sistema de Apuração entre as zero era o BU1 | coberto pelo BU1: 301/301 verificadas |
| P20, as 29 seções de SP | sim | sim | nenhuma das 29 é do Sistema de Apuração | nenhum |
| Integridade por arquivo de 2022 (hash, assinatura, RDV) | sim | sim | 0 BU e 0 assinatura lidos; as 159 linhas existem só porque o `.rdv` era reconhecido (marcado "vazio") | o projeto nunca afirmou integridade nacional de 2022 (T14 a T17 são de 2026), mas a cobertura não estava declarada. Coberta agora pelo SA22, à parte |
| T14 a T17, T17b, T34 (2026) | sim | sim | o leitor de 2026 reconhece `busa` (T34: 31 seções do Sistema de Apuração no 1º turno) | nenhum |

**Cobertura efetiva depois do complemento, 2022:**
- **Seções de urna:** arquivos presentes conferidos pelo pipeline.
- **Sistema de Apuração:** as 159 seções-turno conferidas pelo SA22 (boletim, texto impresso e assinatura, interno).
- **Fora do pacote:** 173 arquivos assinados (A173) e 485 auxiliares (SA22).

**O que não pode ser dado como validado retroativamente:**
- **Análises de log de 2022 (T28 a T33, P10):** não processaram as 148 seções do Sistema de Apuração sem log da urna (o parecer dizia 150; corrigido pelo A4). Isso é adequado ao método, mas o denominador publicado as conta.
- **Urnas sinalizadas não listadas:** 8 (1º turno) e 10 (2º) das urnas sinalizadas pelo T28 em 2022 não estão listadas no resultado, e não se pode afirmar que nenhuma é do Sistema de Apuração.
- **Pipeline geral:** o pipeline geral de 2022 continua sem ler essas seções.

## 3. Matriz definitiva por pergunta
Estados: **R** respondida · **RP** parcialmente respondida · **NE** não executada · **NI** não identificável (impossibilidade demonstrada) · **NDM** não decidível com os modelos disponíveis · **EXT** depende de evidência externa. A coluna "Grupo" remete à seção 6.

| Id | Pergunta | Evidência (script → resultado) | Estado | Conclusão mais forte permitida | Limitação | Próximo passo | Grupo |
|---|---|---|---|---|---|---|---|
| P1 | O estimador de fluxos entre turnos (C06) recupera a verdade sob heterogeneidade? | `fase2/sessao_limitada…/p1_c06_adversarial.py` → `p1_resultado_*.json`; T37 | R | Ordem dos fluxos em 2026 e contraste com 2022 resistem; razão "4:1" erra ±0,5 a ±1,5 mi votos | estimativa ecológica | — | — |
| M1 | O crescimento de Lula entre turnos (2026: +10,33 mi; 2022: +3,07 mi) é reconciliável com eliminados, brancos, nulos e abstenção? | C06, T37, T38, `f2_completa.py P13/P15` | R (contas) / NI (fluxos) | As contas fecham exatamente nos dois anos; a assinatura de enchimento prevista (T38) não aparece | quem migrou para quem não é identificável com dados agregados (limites de Fréchet, P15) | voto individual (não existe) | C |
| P15 | Os limites de Fréchet estreitam a razão entre abstencionistas? | `f2_completa.py P15` | R | Razão não identificada (0 a 1,7 mi) | — | — | C |
| P13 | O C06b é reproduzível? | `f2_completa.py P13` | R | 79 e 123 reproduzidos | — | — | — |
| P2 / P18 | Com que tamanho e mecanismo uma troca de votos seria detectada, nos dois sentidos? | `f3_pendencias.py p18`, `rev_i1_poder.py` → `rev_i1_2026/2022.json` | RP | **Sentido certo, limiar calibrado, 2026:** troca dispersa de 10% dos válidos em 1% das seções (~123 mil votos) 30/30 pelo T1 do lado certo; concentrada em locais ou municípios a 5% (~62 mil) 30/30 pelo E02 do lado certo; região a 5% 26/30 e 23/30 (incerta); 2% (~25 mil) em nenhuma forma; dispersa a 5% não | 1% de cobertura; 5 grandes municípios fora do M2; E02 "simples"; mundos binomiais em torno do real; alarmes no sentido oposto são frequentes a 10% concentrado (E02 até 83%); mecanismos que preservam medianas, que mexem no comparecimento ou anteriores ao BU não testados | E02 "completo" e grandes municípios (A2) | A, C |
| P10 | A rajada sem biometria (T28) resiste à taxa incerta? | `f2_completa.py P10` | R | 8 de 13 urnas do 1º turno de 2026 seguem sinalizadas (99 votos); 2022 também sinaliza (não é específico de 2026) | denominador de 2022 inclui 148 linhas sem log (seção 2) | — | — |
| P5 | O modelo de urna afeta o resultado? | `f2_completa.py P5` | R | Equivalente a zero em ±0,02 logit | — | — | — |
| P7 | A urna trocada vota diferente? | `f2_completa.py P7` | R | Equivalência na margem ±0,10 z | — | — | — |
| P8 | O T03 resiste à dependência municipal? | `f2_completa.py P8` | R | Efeito desprezível | — | — | — |
| P9 | Os locais de votação atípicos (E02) resistem à correlação intralocal e ao entorno? | `f2_completa.py P9`, `rev_i3_espacial.py` → `rev_i3.json` | RP | ~0,1% dos locais significativos com ρ e com referência de zona ou município (2026: 55, 61, 63; 2022: 102, 84, 80); a lista muda com o método (só 28 e 41 em comum) | a referência é administrativa (zona), não geográfica; causa não investigada | coordenadas dos locais (não estão no material) | B/C |
| P17 | A assimetria de cauda do T02 é real? | `f2_completa.py P17` | R | Sim, com bootstrap por município, nos dois anos | causa (P14) | — | — |
| P14 | Qual a causa da assimetria de cauda do T02 em 2022? | `f2_completa.py P14`, `p20.json`, `rev_i3.json` | RP | Localização: SP capital; desvio no nível da zona (251 com o 2º maior z médio de 58 zonas; 259 o 7º), não do local | causa não demonstrada; vizinhança entre zonas não medida | perfil do eleitorado por zona (A3) | A |
| P20 | O que há nos locais de SP com seções atípicas (2022)? | `p20.json`, `rev_i3.json` | RP | 15 locais não atípicos contra a própria zona (z de −1,3 a 2,9); sem as seções selecionadas, −1,7 a 1,5; arquivos 29/29 conferem | não mostra ausência de fenômeno: mostra que ele é da zona; persistência 2026 fraca | idem P14 | A |
| P19 | Há dependência espacial entre municípios? | `f3_pendencias.py p19` | R | Moran's I 0,16 a 0,20 (p = 0,001), nos dois anos | não distingue causa | — | — |
| C1 | A forma das curvas é compatível com um processo de chegada plausível? | `f3_curvas.py`, `f3_curvas2.py` → `E2*.json` | NDM | Nenhum dos 5 nulos é calibrado, nem em 2022; a forma não permite concluir compatibilidade nem incompatibilidade | curva reconstruída pela hora de recebimento, não a divulgada; sem modelo de chegada validado | snapshots datados (B1) | B, C |
| C1a | Quando e onde ocorreram as viradas de liderança? | `E2_curvas.json` | RP (descrição) | Na reconstrução: 2026 2T, Lula lidera aos 10%, perde aos 13,5% e retoma aos 47,2%; 2022 2T, adversário lidera até 67,6%. A última troca vem mais tarde que nos nulos nos dois anos | descrição da ordem de recebimento; não explica nem refuta nada | snapshots | B |
| C1b | Há periodicidade, vales ou trechos lineares anômalos? | `E2*.json` (S3 a S5) | NDM | Estatísticas calculadas; S1 mede ruído no cruzamento; nenhuma leitura possível sem nulo calibrado | método | modelo de chegada por lote | C |
| C2 | As curvas de 2022 e 2026 têm as mesmas características? | `E2_curvas.json` | RP (descrição) | Diferem: 2026 mais territorial (η² por UF 0,39 × 0,24) e com duas trocas no 2º turno | sem teste formal | — | C |
| Z1 | Seções com zero votos para um finalista excedem o esperado? | `f3_zeros.py`, `rev_i2_zeros.py`, `bu1.json` | RP | **Arquivos:** 0 divergências em 486/486 seções-turno (2026: 185; 2022: 301). **Estatística:** nenhum modelo calibrado; o modelo subestima toda a cauda baixa (0, 1, 2 e 3 a 5 votos), com o mesmo formato em 2022 e 2026; não se afirma excesso nem normalidade | método atual não calibrado (não é impossibilidade) | modelo de mistura com critério de calibração refeito (C3) | C |
| P3 | As inconsistências dependem do canal e da versão de publicação? | `f3_reconcilia.py` → `R1_20_*.json`; E3 | RP | A tabela publicada é igual ao BU decodificado por terceiro nas seções comuns | mesma origem; uma só versão de cada arquivo | versões datadas (B4) | B |
| R1-20 | A base do projeto concorda com uma decodificação independente? | `f3_reconcilia.py` | RP | 0 diferenças em 499.206 seções (2026 1T) e ~470,8 mil por turno (2022); reprodução idêntica, com commit e hashes conferidos | 2026 2T não coberto; 2022: 174 e 166 seções do Brasil sem par e sem explicação | explicar as 174 e 166 (A1); decodificação de terceiro do 2T de 2026 (B5) | A, B |
| P16 | 200 seções sorteadas: todos os arquivos concordam? | `f2_completa.py P16` | R | 200/200 no 1º turno de 2026 | o 2º turno de 2026 é coberto nacionalmente pelo T17b (BU = RDV = publicado em todas as urnas) | — | — |
| P11 | Os certificados das urnas se ligam a uma âncora do TSE? | `f2_completa.py P11` | EXT | Urna → AC emissora verificada (ACs obtidas de terceiro) | elo AC → raiz não verificado | AC URNA v2 e AC RAIZ UE do TSE (B3) | B |
| P21 | Boletins de terceiros e cadeia autenticada confirmam os arquivos? | — | EXT | — | nada obtido | B2, B3 | B |
| P4 | A curva pública pode ser reconstruída a partir dos BUs? | — | EXT | — | nenhuma captura histórica | B1 | B |
| P6 | O que boletins de terceiros permitiriam validar? | — | EXT | — | nenhum dado primário | B2 | B |
| P12 | Diferença de eleitorado do exterior | `f2_completa.py P12` | R | Explicada, resíduo zero | — | — | — |
| A173 | Os 173 arquivos de 2022 estão ausentes da publicação? | `ver_a173.py` → `a173.csv/json` | RP | Ausentes do pacote de dados abertos em duas cópias (14/10 e 27/10), assinados pela urna (SHA-512 igual); BUs das 64 seções iguais à tabela | não se sabe se há outro canal (site de 2022: 404) | consulta ao TSE (B6) | B |
| BU1 | A seção com BU não lido concorda? | `ver_bu1.py` → `bu1.json` | R | Sim: boletim do Sistema de Apuração, texto impresso e assinatura conferem | conferência interna | — | — |
| SA22 | As 159 seções-turno do Sistema de Apuração de 2022 conferem? | `ver_sa22.py` → `sa22.csv/json` | R | 159/159: boletim e texto impresso iguais à tabela; assinatura válida | interna; cadeia só até a AC; 485 auxiliares listados e ausentes | motivo dos auxiliares (B6) | B |
| AUT | Os arquivos são autênticos e íntegros? | T14 a T17, T17b, P16, SA22, P11 | RP | 2026: hash, assinatura, RDV e BU conferem (cobertura por turno em T14 a T17b); 2022: arquivos presentes conferem, com lacunas de publicação (A173, SA22) | origem autenticada só até a AC; não alcança alteração anterior à geração do boletim, porque BU, RDV e log saem do mesmo equipamento | B3; o resto é limite dos dados públicos | B, C |
| MET | Os métodos resistem à revisão? | auditoria, I1 a I3 | RP | T10/T11 descritivos; T02 só vê trocas dentro do município; E02 depende do método; zeros sem modelo | — | ver A2, C3 | A, C |

## 4. Achados que permanecem demonstrados
- **Contas e correspondência (prova determinística, interna):**
  - A tabela publicada é igual ao BU decodificado pelo projeto (T15, T17b) e por terceiro (T43) nas seções comuns.
  - Soma das urnas = total oficial.
  - Em 2026, BU = RDV = publicado em todas as urnas dos dois turnos (T17b).
  - Em 2022, os boletins das 64 seções do A173 e das 159 do SA22 conferem.
- **Integridade criptográfica até a AC emissora:** 2026 nacional, e em 2022 nos arquivos presentes e no SA22.
- **Publicação de 2022, objetivo e de causa desconhecida:** 173 arquivos assinados pelas urnas faltam no pacote de dados abertos, e 485 auxiliares também nas seções do Sistema de Apuração. Isso é **inconsistência de publicação, não de votos**.
- **Estatística com poder medido:**
  - A assimetria de cauda do T02 existe (P17), e em SP 2022 se concentra no nível da zona eleitoral.
  - Dependência espacial (Moran's I).
  - Poder no sentido certo: troca dispersa de ~123 mil votos e concentrada em locais ou municípios de ~62 mil. *(Restrito pelo A2 a municípios de até ~5 mil seções.)*

## 5. Conclusões enfraquecidas ou corrigidas
- **T10/T11:** viraram descrição.
- **T02:** não vê troca em município ou região inteiros.
- **T13:** o limiar ancorado no real dá 23% de falso alarme em 2022. No P18, o falso alarme calibrado era 0 por construção.
- **E02:** lista de locais depende do método.
- **Zeros:** "sem evidência de excesso" foi retirado.
- **SP 2022:** "zonas vizinhas" foi retirado.
- **R1-20:** "exterior e agregadas" foi retirado.
- **Novo nesta sessão (I1, direção):** o mecanismo regional a 5% passa de "detectável" para "detecção incerta" no sentido certo (26/30 e 23/30). Nos demais casos que eu tinha chamado de detectáveis, a detecção vem do lado certo.
- **E02 a 10% concentrado:** também acende no sentido oposto (até 83% das réplicas). Um sinal do E02 não diz, sozinho, para quem foi a troca.

## 6. Pendências por natureza

### Grupo A: resolvíveis com dados locais (nenhuma executada)
| Id | O que fazer | Custo | Relevância | Chance de resposta discriminante |
|---|---|---|---|---|
| A1 | Explicar as 174 (1º turno) e 166 (2º) seções de 2022 do Brasil que a base tem e o DataUrnas-BR não. Leitura determinística: tipo de urna, seção agregada, arquivos no pacote | baixo (minutos) | média: fecha o R1-20 em 2022 | alta |
| A2 | Repetir o I1 com o E02 "completo" e com uma cobertura que inclua os 5 grandes municípios | médio (~10 min por ano) | média: as conclusões de poder usam o E02 da F2 | média |
| A3 | Testar se o deslocamento da zona 251 (e 259) de SP em 2022 se explica pelo perfil do eleitorado (dados locais em `dados/2022/perfil_eleitorado`) | médio | média (P14, P20) | baixa a média: pode explicar ou não, não decide manipulação |
| A4 | Listar todas as urnas sinalizadas pelo T28 em 2022 e corrigir o denominador declarado | baixo | baixa | alta (só cobertura) |

### Grupo B: dependentes de dados externos
| Id | Fonte necessária | Como obter legitimamente | O que permitiria verificar |
|---|---|---|---|
| B1 | Snapshots datados da divulgação (2022 e 2026) | arquivos de terceiros com data e hash (Internet Archive, imprensa, pesquisadores) ou pedido ao TSE | ordem de divulgação × ordem de recebimento; viradas observadas (P4, C1) |
| B2 | Boletins impressos fotografados por terceiros, com proveniência | coletas públicas com lista de seções e imagens | publicado = impresso na seção (P6, P21) |
| B3 | Certificados AC URNA v2 e AC RAIZ UE | publicação oficial do TSE ou pedido via Lei de Acesso à Informação | cadeia até a âncora (P11, P21) |
| B4 | Versões datadas dos arquivos e tabelas | capturas periódicas futuras; pedido ao TSE | republicação (P3) |
| B5 | Decodificação independente do 2º turno de 2026 | DataUrnas-BR ou outro projeto quando publicar | R1-20 no turno decisivo |
| B6 | Situação dos 173 arquivos e dos auxiliares `.hash`, `.ver`, `.chvtp`, `.jufa` | pedido ao TSE via LAI | se estão publicados em outro canal e por quê |

### Grupo C: identificabilidade ou validade de método
| Item | Natureza |
|---|---|
| Fluxos individuais entre turnos (M1, P1, P15) | **impossibilidade demonstrada**: os limites de Fréchet (P15) mostram que a razão vai de ~0 a 1,7 mi sem violar os dados |
| Curvas (C1, C1b) | **limitação do método e falta de dados**: nenhum modelo de chegada validado, e não há snapshots. Não é impossibilidade demonstrada |
| Cauda baixa dos zeros (Z1) | **limitação do método atual**: o modelo falhou, mas um modelo de mistura com critério de calibração refeito poderia ser tentado (C3). Não é impossibilidade |
| Alteração anterior à geração de BU, RDV e log | **limite dos dados públicos**: os registros saem do mesmo equipamento, e a coerência entre eles não testa o que veio antes |
| Mecanismos sem poder medido (P2, P18) | **limitação de cobertura do método**: preservam medianas, mexem no comparecimento, ficam abaixo de ~25 mil votos ou são dispersos abaixo de ~123 mil |

## 7. Auditoria das conclusões principais
- **A. Detecção:** os documentos atuais (CONCLUSAO, METODOLOGIA, PROTOCOLO e emenda 6) já trazem a exclusão das grandes cidades, a diferença entre alarme e detecção, o E02 "simples", os mundos binomiais e os mecanismos não testados. Duas frases precisam de correção (seção 11): a região a 5% como "detectável" e a ausência da observação sobre alarmes no sentido oposto. Nenhum documento afirma detecção garantida fora dos mecanismos avaliados.
- **B. Zeros:** nenhum documento vivo afirma excesso ou normalidade. A observação da cauda baixa está preservada como falha do modelo.
- **C. SP:** o I3 está descrito como referência pela zona, não como nulo geográfico (METODOLOGIA e emenda 6). O texto separa local, zona e vizinhança, e a vizinhança entre zonas não foi medida.
- **D. Curvas:** a ordem de recebimento (`DT_BU_RECEBIDO`) aparece como reconstrução retrospectiva. A ordem de divulgação e os registros independentes estão em "bloqueado" (P4, B1). Nenhum documento declara viradas explicadas, fraudulentas ou refutadas.
- **E. Correspondência:** os documentos separam comparação de valores (T35, T36, T43, A173, SA22), integridade criptográfica (T16, SA22), origem autenticada (só até a AC, P11) e evidência externa (nenhuma).
- **Pendências de documentação:**
  - O registro do T28 de 2022 não diz que o denominador inclui as 148 seções do Sistema de Apuração sem log (corrigido pelo A4; dizia 150).
  - A matriz da seção 3 ainda não está no inventário. Hoje M1 e AUT estão espalhados.

## 8. Suficiência científica
**A pesquisa já extraiu dos dados disponíveis tudo o que pode ser demonstrado com métodos validados?** **Quase, mas não inteiramente.**

| Critério | Avaliação | Base |
|---|---|---|
| 1. Cobertura das perguntas | todas as 30 do inventário enfrentadas com critério explícito; nenhuma não executada | `inventario.json` |
| 2. Robustez dos métodos | determinísticos robustos; estatísticos com limites medidos; curvas e zeros sem método validado | seções 3 e 6C |
| 3. Reprodutibilidade | scripts e resultados versionados; R1-20 com commit e hash; I1 a I3 com sementes fixas | `fase3/*.py` |
| 4. Proveniência | boa, com duas falhas registradas: rodada 4 alterada após congelar (com hash posterior) e execução original do R1-20 sem hash | `rodada-4-desvio.md`, `DATAURNAS.md` |
| 5. Poder de detecção | medido para 4 mecanismos e 3 magnitudes, nos dois sentidos, com direção conferida nesta sessão; lacunas documentadas | `rev_i1_*.json` |
| 6. Validação externa | só de implementação (DataUrnas-BR); nenhuma de origem | P3, P6, P11, P21 |
| 7. Transparência das limitações | alta, com histórico | inventário, provas, emenda 6 |
| 8. Preservação dos achados | V1.0 a V1.2 íntegras; estados anteriores no campo `historico` | seção 1 |
| 9. Proporcionalidade | corrigida várias vezes; duas frases do I1 ainda a corrigir | seção 5 |
| 10. Pendências locais viáveis | sim: A1 a A4, todas de baixo ou médio custo | seção 6A |

O que separa a F3 de "tudo o que é demonstrável" são A1 (determinístico, fecha um resíduo de reconciliação) e A2 (consolida a medida de poder com o E02 da conclusão). A3 e C3 são investigações novas, legítimas mas não necessárias: explicam ou não, sem mudar o nível das conclusões.

## 9. Problemas metodológicos ainda relevantes
1. A afirmação de poder usa o E02 "simples" e exclui as 5 maiores cidades (A2).
2. Alarmes no sentido oposto a 10% concentrado: o E02 não atribui direção de forma confiável nessas condições.
3. O critério de calibração do I2 era inadequado para controles grandes e precisa ser refeito antes de qualquer nova tentativa.
4. As curvas não têm modelo de chegada nem dado histórico.
5. Pré-registros da F3 fora do PROTOCOLO (emenda 6 feita depois, declarada como tal).

Nenhum desses itens inverte uma conclusão central (contas, correspondência, ausência de classe E/F, limites de poder). Os itens 1 e 2 mudam a precisão da afirmação de poder.

## 10. Recomendação
**Situação B: a F3 precisa de verificações finais específicas**, poucas e delimitadas, antes da aprovação condicionada.
- **Não é A** porque restam duas pendências locais viáveis que tocam afirmações publicadas: A1 (resíduo de 174 e 166 seções do R1-20) e A2 (poder com o E02 da conclusão e sem excluir as grandes cidades). Há também duas correções de redação (seção 11).
- **Não é C** porque nenhuma falha encontrada altera uma conclusão científica importante. As correções mudam alcance e precisão, não direção. As versões congeladas e a proveniência estão íntegras.

**Proposta mínima para chegar a A:**
1. Aplicar as correções de texto da seção 11.
2. Executar A1, que é determinístico.
3. Decidir se A2 entra ou se o poder fica declarado com as ressalvas atuais.
4. Aceitar formalmente A3, A4, C3 e o Grupo B como pendências registradas fora da F3.

A decisão é do responsável.

## 11. Correções de texto propostas (não aplicadas)
1. **Inventário P18 e P2, CONCLUSAO (seção "Fase 3 em revisão"), METODOLOGIA (I1), `RELATORIO_F3.md` (tabela do I1):**
   - **Região a 5%:** acrescentar que, contando só alarmes do lado certo, a região a 5% dá 26/30 (para Lula) e 23/30 (contra), ou seja, detecção incerta. Trocar "região a 5% no sentido para Lula (29/30)" da lista de detectáveis para a de incertos.
   - **Alarmes no sentido oposto:** acrescentar que, a 10% concentrado, o E02 também sinaliza locais no sentido oposto em até 83% das réplicas, e o sinal do E02 não identifica sozinho o beneficiário.
2. **Registro do T28 (evidência de 2022) e P10:** declarar que o denominador de 2022 (472.024 e 472.027) inclui 148 seções-turno do Sistema de Apuração sem log da urna. A análise efetiva foi sobre `urnas_com_sequencia` (471.859 e 471.983).
3. **Inventário:** acrescentar os itens M1 (fluxos entre turnos, NI para fluxos individuais), AUT (autenticidade), C1a e C1b, hoje dispersos. Assim a matriz da seção 3 fica integralmente no inventário.
4. **P16:** registrar que a ressalva "2º turno não amostrado" está coberta pelo T17b nacional.
