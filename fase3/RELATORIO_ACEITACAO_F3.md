# F3: verificação documental (A173, BU1) e auditoria de aceitação (28/10/2026)

**Escopo:** duas verificações documentais e uma auditoria, sem teste estatístico novo e sem refazer I1 a I3.

**Repositório:**
- Commit publicado no início da sessão: e4fd8a7 (só a mudança visual da Home).
- Nada desta sessão foi publicado.
- A V1.2 (`rodadas/rodada-4/`, tag `v1.2`) não foi tocada.

**Scripts novos:** `fase3/ver_a173.py` e `fase3/ver_bu1.py`, uma reprodução dirigida cada um.

**Validações independentes:**
- **A173:** comparação com o SHA-512 assinado no `.vscmr` local.
- **BU1:** leitura do texto impresso `.imgbusa`.

**Consultas externas:** duas, ao site de resultados de 2022, ambas com HTTP 404. O bloqueio está registrado.

**Correções de texto feitas nesta sessão, com histórico:**
- **Zonas de São Paulo:** "zonas 251, 259 e vizinhas" virou o que foi medido. A zona 251 tem o 2º maior z médio das 58 zonas da capital, e a 259 o 7º. A vizinhança entre zonas não foi medida.
- **Cauda baixa dos zeros:** passou a ser descrita como falha do modelo, não como excesso.
- **R1-20:** a frase "exterior e agregadas" não tinha sido verificada. A correção está no item R1-20 do inventário.
- **Prova do T43:** escrevi uma frase não verificada e a corrigi minutos depois, antes de qualquer publicação. A versão corrigida está no registro.

## A. Relatório A173

**Pergunta:** os 173 arquivos de 2022 que o DataUrnas-BR aponta como assinados e ausentes do pacote do TSE estão de fato ausentes, ou a diferença vem de inventário, coleta ou processamento?

**Fonte da lista:**
- **Arquivo:** `data/parquet/2022/integridade/divergencias.jsonl` do DataUrnas-BR, commit 12f0433, SHA-256 `264b5876…7969`, com 173 linhas.
- **Lista rastreável item a item:** `fase3/resultados/a173.csv`, uma linha por arquivo, com seção, tipo, presença local, listagem no `.vscmr`, igualdade de SHA-512 e classe.
- **Detalhe por seção:** `fase3/resultados/a173.json`.

| Verificação | Resultado |
|---|---|
| Arquivos e seções | 173 arquivos em 64 seções: 61 `.logjez`, 56 `.rdv`, 56 `.imgbu` |
| Distribuição | 1º turno: 54 seções do exterior (162 arquivos: cada uma sem `.imgbu`, `.logjez` e `.rdv`), BA 1, MA 1 (2 arquivos), MG 1, RN 1. 2º turno: PA 5, RN 1 |
| Listados no `.vscmr` do pacote local | 173 de 173, com o mesmo SHA-512 informado pelo DataUrnas-BR; assinatura da lista válida nas 64 seções |
| Presentes no pacote oficial baixado pelo projeto (27/10/2026) | 0 de 173 (o DataUrnas-BR baixou em 14/10/2026) |
| Mesmo conteúdo com outro nome na seção | 0 (nenhum arquivo presente tem o SHA-512 de um ausente) |
| BU da seção presente | 64 de 64 |
| Votos do BU × tabela publicada | iguais nas 64 seções, inclusive o comparecimento (0 diferenças) |
| Eleitores nas 64 seções | 44.983 aptos, 21.112 comparecimentos |

**Classificação individual:** os 173 caem na mesma classe, "ausente também no pacote local; assinado pela urna".

**Conclusão permitida:**
- **Comprovado:** os 173 arquivos foram listados e assinados pela urna e não estão no pacote de dados abertos do TSE em duas cópias baixadas com 13 dias de diferença. Não é erro de coleta nem de processamento de um projeto, nem diferença de nome.
- **Registros únicos:** são registros sem substituto no pacote (RDV voto a voto, log e imagem do BU). Nessas seções não é possível recontar pelo RDV (56 seções) nem analisar o log (61).
- **Votos:** não há divergência de votos demonstrável. O boletim de cada seção está presente e confere com a tabela publicada.
- **Fora do alcance:**
  - Se o TSE publica esses arquivos por outro canal: o site de resultados de 2022 devolveu 404 e a pergunta fica bloqueada.
  - Por que faltam.
  - Se o conteúdo deles concorda com o BU.

**Estado do item A173:** respondida parcialmente. Falta uma consulta ao TSE ou acesso a outro canal.

## B. Relatório BU1

**Identificação:** seção MG, município 49050 (Novo Cruzeiro), zona 196, seção 173, 2022, 1º turno. Pacote local `bu_imgbu_logjez_rdv_vscmr_2022_1t_MG.zip` (7.639.923.232 bytes).

**Arquivos da seção** (SHA-512 e SHA-256 completos em `fase3/resultados/bu1.json`):
- `.busa` (1.246 bytes)
- `.imgbusa` (6.270 bytes)
- `.logsajez` (92.063 bytes)
- `.rdv` (1.115 bytes)
- `.vscsa` (41.702 bytes)

São os arquivos do **Sistema de Apuração**, usado quando a seção é apurada fora da urna. O BU foi emitido às 23:47.

**Reprodução da falha:** o leitor de 2022 do projeto (`analise/processar_brutos.py`, `TIPO_2022`) só reconhece `bu`, `imgbu`, `logjez`, `rdv` e `vscmr`. Por isso só o `.rdv` foi lido, e como "vazio ou outro formato". O arquivo não está danificado; é uma lacuna de implementação. O leitor de 2026 já reconhece `busa`.

**Decodificação:**

| Fonte | Aptos | Comparecimento | Lula | Demais | Brancos | Nulos |
|---|---|---|---|---|---|---|
| `.busa`, mesmo decodificador DER do BU | 109 | 16 | 16 | 0 | 0 | 0 |
| `.imgbusa`, texto impresso (leitura independente) | — | — | 16 | 0 | 0 | 0 |
| Tabela publicada (BU na Web) | 109 | 16 | 16 | 0 | 0 | 0 |

**Assinatura:** a lista `.vscsa` é assinada em ECDSA P-521 pelo certificado `ueao01293146`, emitido pela AC URNA. Tamanho, SHA-512 e assinatura conferem nos 4 arquivos.

**Conclusão permitida:**
- O BU1 está verificado e confere.
- A afirmação "0 divergências nas seções com zero votos" passa a valer para as 301 seções-turno de 2022, sem exceção não verificada.
- A frase anterior "1 seção sem BU lido" estava correta como ressalva. Ela foi atualizada com histórico em T41, inventário, CONCLUSAO e linha do tempo.

**Consequência maior:** a mesma lacuna deixou fora de **todas** as verificações por arquivo de urna de 2022 as **159 seções-turno** apuradas pelo Sistema de Apuração.
- **1º turno:** 116, sendo 99 do exterior.
- **2º turno:** 43, sendo 33 do exterior.

Os votos delas estão na tabela publicada usada pelos testes estatísticos. O que não foi feito é hash, assinatura e comparação com o arquivo, exceto no BU1. Ficou registrado como item novo **SA22**, para análise futura, sem execução.

**Correção do R1-20:** essas seções explicam só 17 de 191 (1º turno) e 10 de 176 (2º) das seções do Brasil que a base tem e o DataUrnas-BR não. As demais não estão explicadas, e "exterior e agregadas" não tinha sido verificado.

## C. Revisão de I1 a I3 (sem reexecução)

### I1. Poder de detecção
- **Os votos inseridos nas simulações são sintéticos.** Não são votos fraudulentos encontrados nos dados reais. O I1 mede o que a bateria veria se uma troca daquele tamanho existisse.
- **Mundos:** binomial em torno das proporções reais de cada seção. Preservam a heterogeneidade real entre seções e somam ruído amostral. Servem para medir quanto uma troca acrescenta ao que já existe. Não são mundos "sabidamente limpos": qualquer anomalia real faz parte da referência.
- **Calibração e avaliação separadas:** sim. São 20 mundos só para os limiares e 30 independentes para falso alarme e poder. Os mesmos 30 mundos servem de base a todos os mecanismos, então as células são correlacionadas entre si.
- **Exclusão no M2:** pulei 5 municípios maiores que o alvo de 1%: São Paulo, Rio de Janeiro, Brasília, Fortaleza e Salvador, que somam 11,4% das seções de 2026. O resultado do M2 vale para municípios de até cerca de 4.900 seções. Uma troca no município inteiro de uma grande capital não foi testada. M1 e M3 podem incluir seções dessas cidades.
- **Dois sentidos:** sim.
- **Magnitude em votos:** cada número é a média dos votos de fato movidos (m × válidos, limitado ao que o perdedor tinha). A conta está certa: 10% em ~1% das seções dá ~123 mil votos em 2026.
- **Regra conjunta:** há alarme se qualquer estatística do conjunto passa do limiar, e o código faz isso.
  - **Direção não verificada:** a regra conta alarme do lado oposto como detecção. No M2 a 10% para Lula, a cauda contrária (T1_contra) passou do limiar em 12 de 30 réplicas, porque a mediana municipal se desloca. "Detectado" não quer dizer "atribuído ao sentido certo", e a direção não foi conferida.
- **Incerteza:** IC de Wilson com 30 réplicas. Um resultado de 0/30 tem limite superior de 11%, e um de 30/30 tem limite inferior de 89%. Isso está descrito.
- **Desvios do pré-registro:**
  - O limiar ancorado do E02 (real + máx(5, 5√)) foi uma extensão minha, não escrita no pré-registro.
  - O E02 do I1 usa o modelo "simples". As contagens da F2 e do I3 usam o "completo". O poder do E02 "completo" não foi medido, embora a troca simulada não mexa nas covariáveis extras.
- **Alcance:** um só nível de cobertura (1% das seções). Ficaram de fora: mecanismos que preservam as medianas municipal e estadual, troca que mexe no comparecimento e qualquer alteração anterior à geração do boletim. Nada disso pode ser excluído.

### I2. Zeros
- **O modelo falhou na calibração?** Sim, pelo critério fixado antes, e a falha é robusta. O controle Lula erra cerca de 18 vezes em 2026 (8 contra 0,4), independentemente da escolha dos controles grandes.
- **Os controles eram adequados?** O critério foi mal desenhado para os candidatos menores. Com dezenas de milhares de zeros, o intervalo de predição só tem ruído de Bernoulli e fica estreito demais, então quase qualquer modelo falharia ali. Isso não muda o resultado, por causa da falha do controle Lula, mas o critério precisa ser refeito antes de qualquer nova tentativa.
- **Escolhas:** o peso 50 e a comparação local × zona foram fixados antes, como parte confirmatória. Nada foi ajustado depois. Não criei outro modelo.
- **2022 × 2026:** mesmo modelo e mesmo universo. A razão das razões depende do modelo (1,35 a 3,4) e não é interpretável.
- **Relatório:** preserva a ausência de conclusão. A distribuição de 0, 1, 2 e 3 a 5 votos foi corrigida para "o modelo subestima toda a cauda baixa", que é falha do modelo e não comprovação de nada.
- **Limitação técnica:** ρ é ajustado pela verossimilhança truncada, dominada pelas seções com muitos votos. Era esperado que o ajuste fosse pior justamente na cauda baixa.

### I3. Dependência espacial
- **Referência:** a própria zona eleitoral sem o local. Se a zona tem menos de 3 outras seções, usa-se o município. A sensibilidade usa o município.
- **Nome impreciso:** é uma referência administrativa, não uma vizinhança geográfica. Não há coordenadas de locais no material, então "nulo espacial" deve ser lido como "relativo ao entorno administrativo".
- **Nulo empírico:** mediana e MAD de d por faixa de tamanho. Isso supõe que a maioria dos locais é nula, o que é razoável com cerca de 0,1% de significativos. A variância da média de referência foi ignorada; as zonas são grandes.
- **Múltiplos testes:** BH com q = 0,05 sobre todos os locais de cada ano. Sim.
- **Viés de seleção (São Paulo):** testado ao refazer d sem as seções que selecionaram os locais. As seções vieram do z do T02 (mediana municipal) e o I3 usa o resíduo do modelo por UF (zz): são variáveis diferentes, e os locais não se destacam nem com todas as seções.
- **O que se pode afirmar sobre São Paulo:**
  - Nenhum dos 15 locais é atípico contra a própria zona.
  - O desvio acompanha a zona: a 251 inteira tem o 2º maior z médio das 58 zonas da capital, e a 259 o 7º.
  - Em 2026, a persistência é fraca: 1 de 15 com zona como referência, 0 de 15 com município.
- **O que não se pode afirmar:** que "não há fenômeno". A perda de significância contra a zona mostra que o desvio não é de locais isolados. Não mostra que o desvio da zona não existe ou é legítimo. A causa do deslocamento da zona 251 não foi investigada.

### Lacunas de processo encontradas
- **PROTOCOLO.md:** nenhuma emenda para a F3 (T40 a T43, I1 a I3). O AGENTS.md exige emenda antes do teste. Os pré-registros existem (`fase3/PREREG.md`, `fase3/PREREG_REVISAO.md`), mas fora do lugar previsto.
- **METODOLOGIA.md:** sem a matemática de T40 a T43 e de I1 a I3.
- **CATALOGO.md:** sem as sessões da F3.

## D. Matriz completa da F3

R = respondida · RP = respondida parcialmente · NDM = não decidível com os modelos disponíveis · B = bloqueada por fonte externa · NE = não executada. A coluna de provas indica os arquivos em `fase3/resultados/` e `fase2/resultados/`.

| Pergunta | O que está demonstrado | Testes e provas | Força | Alternativas abertas | Falta | Estado |
|---|---|---|---|---|---|---|
| P1 Fluxos entre turnos (C06) | Ordem 2026 e contraste com 2022 resistem; magnitude "4:1" frágil | T37, C06 | média | heterogeneidade contextual | voto individual (impossível) | R |
| P2 Sensibilidade da regra | Ver P18 e I1 | T13, p18, rev_i1 | média | mecanismos não testados | outras coberturas e mecanismos | RP |
| P3 Canais e versões | Tabela = BU decodificado por terceiro, nas seções comuns | T43, R1_20, E3 | alta (concordância), mesma origem | republicação; origem comum | versões datadas; 2º turno 2026 | RP |
| P4 Curva pública histórica | Nada observado | — | — | — | snapshots datados | B |
| P5 Modelo de urna | Equivalente a zero (±0,02 logit) | T20, P5 | alta | — | — | R |
| P6 Boletins de terceiros | Nenhum dado primário | — | — | — | listas de terceiros | B |
| P7 Urna trocada (TOST) | Equivalência na margem fixada | T04 | alta | — | — | R |
| P8 T03 com bootstrap | Efeito desprezível | T03 | alta | — | — | R |
| P9 Locais do E02 | ~0,1% dos locais significativos em 3 métodos; lista depende do método | E02, P9, rev_i3 | média | causas locais legítimas ou não | nulo geográfico; causa | RP |
| P10 T28 beta-binomial | 8 de 13 urnas seguem sinalizadas (99 votos) | T28 | média | variação legítima | — | R |
| P11 Âncora criptográfica | Urna → AC verificada com AC de terceiro | T16, P11 | parcial | AC de terceiro | AC URNA v2 e AC RAIZ UE do TSE | B |
| P12 Eleitorado exterior | Explicada, resíduo zero | T32 | alta | — | — | R |
| P13 C06b reproduzível | 79 e 123 reproduzidos | C06b | alta | — | — | R |
| P14 Causa da assimetria do T02 | Localização (SP 2022, desvio no nível da zona); causa não | P14, p20, rev_i3 | — | perfil, campanha, erro, manipulação | covariáveis de zona e eleitorado 2022 | RP |
| P15 Fréchet | Razão não identificada | P15 | alta (limites) | — | — | R |
| P16 200 seções | 200/200 concordam (2026, 1º turno) | P16 | alta na amostra | — | 2º turno não amostrado | R |
| P17 Assimetria significativa | Real com bootstrap por município | P17 | alta | ver P14 | causa | R |
| P18 Poder bilateral | Disperso 10% (~123 mil) visto nos dois sentidos; concentrado 5% (~62 mil) pelo E02; 2% (~25 mil) não | T13, p18, rev_i1 | média (30 réplicas) | direção dos alarmes não conferida | mecanismos e coberturas não testados | RP |
| P19 Moran's I | I = 0,16 a 0,20, p = 0,001 | T42, p19 | alta (existência) | causa | — | R |
| P20 SP 2022 | 29 seções em 15 locais; não atípicos contra a zona; zona 251 deslocada; arquivos conferem | p20, rev_i3 | média | causa | dados da zona | RP |
| P21 Terceiros e cadeia | Nada obtido | — | — | — | TSE e terceiros | B |
| R1-20 Reconciliação independente | 0 diferenças nas seções comuns; reprodução idêntica | T43, R1_20 | alta, mesma origem | — | 2º turno 2026; 174 e 166 seções sem par | RP |
| C1 Curvas × modelos de chegada | Nenhum de 5 nulos calibrado, nem em 2022 | T40, E2, E2b | — | estrutura de lotes de recepção | snapshots; modelo de chegada | NDM |
| C1a Viradas de liderança | Descritas na curva reconstruída (2026 2T: 13,5% e 47,2%; 2022 2T: 67,6%) | E2 | descritiva | curva reconstruída ≠ divulgada | snapshots | RP |
| C1b Periodicidade, vales, trechos lineares | Estatísticas S3 a S5 calculadas; S1 mede ruído | E2, E2b | fraca | — | modelo adequado | NDM |
| C2 2022 × 2026 | Diferem na descrição; sem teste formal | E2 | descritiva | — | teste formal | RP |
| M1 Mudança entre turnos | Contas fecham; fluxos não identificáveis | C06, T37, T38, C06b, P15 | alta (contas) | — | nada novo na F3 | RP |
| Z1 Zeros | Arquivos conferem em 486/486; nenhum modelo calibrado | T41, E3, rev_i2, bu1 | alta (arquivos); nula (estatística) | heterogeneidade local × excesso | modelo de cauda baixa validado | RP |
| Autenticidade 2026 | Hash, assinatura, RDV e BU conferem (cobertura por turno em T14 a T17; cadeia até a AC) | T14 a T17, P16 | alta, interna | alteração anterior à geração | âncora do TSE; fontes externas | RP (ver P11) |
| Autenticidade 2022 | Parcial: 173 arquivos ausentes do pacote; 159 seções-turno do Sistema de Apuração não verificadas pelo projeto | a173, bu1 | parcial | — | SA22; consulta ao TSE | RP |
| A173 | Ausência confirmada no pacote de dados abertos em duas cópias; votos conferem | a173 | alta (no canal consultado) | outro canal do TSE | TSE | RP |
| BU1 | Verificado, confere | bu1 | alta | — | — | R |
| SA22 | Não verificadas pelos arquivos | bu1 (contagem) | — | — | leitura dirigida | NE |
| MET Métodos | T10/T11 descritivos; T02 cego a município inteiro; E02 dependente do método; zeros sem modelo | auditoria, I1 a I3 | — | — | modelos de chegada e de cauda | RP |

Nenhuma pergunta saiu do inventário. As perguntas abertas por falta de dado ou de modelo não foram declaradas refutadas nem comprovadas.

## E. Parecer de aceitação

**Resistem:**
- 0 diferenças entre a tabela publicada e o BU decodificado por terceiro, nas seções comuns.
- BU1 verificado.
- Votos das 64 seções do A173 iguais aos publicados.
- Dependência espacial (Moran's I).
- Simetria do T13 para troca dispersa.
- O E02 detecta troca concentrada a partir de ~62 mil votos. *(Restrito pelo A2: só em locais ou municípios de até ~5 mil seções; não no município inteiro das 5 maiores cidades.)*
- A assimetria de cauda do T02 existe (P17).
- O desvio de SP 2022 é no nível da zona, não do local.

**Enfraquecidos:**
- T10 e T11 viram descrição.
- O alcance do T02 vale só para trocas dentro do município.
- A lista de locais do E02 depende do método.
- "Sem evidência de excesso" nos zeros foi retirado.
- A leitura "regional, zonas vizinhas" de SP foi reduzida ao que foi medido.
- A cobertura das verificações por arquivo de 2022 é menor do que estava implícito: 173 arquivos ausentes e 159 seções-turno não lidas.

**Precisam ser corrigidos antes de encerrar** (documentação, sem teste novo):
- Emenda do PROTOCOLO para a F3.
- METODOLOGIA de T40 a T43 e de I1 a I3.
- Sessões da F3 no CATALOGO.
- Declarar no I1 a exclusão das 5 grandes cidades e a direção não verificada dos alarmes.
- Registrar o desvio do limiar ancorado do E02 e o uso do modelo "simples".
- Publicar estas correções e as verificações A173 e BU1 com a sua aprovação.

**Permanecem abertas:** P2, P3, P9, P14, P18, P20, R1-20, C1 (com C1a, C1b e C2), M1, Z1, MET, A173 e SA22.

**Dependem de fonte externa:**
- P4: snapshots datados.
- P6 e P21: boletins de terceiros.
- P11 e P21: AC URNA v2 e AC RAIZ UE.
- A173: outro canal do TSE.

**Para considerar a F3 satisfatoriamente encerrada:**
1. Fazer as correções documentais acima.
2. Escolher, para cada pergunta aberta, entre investigar mais (o SA22 é barato e só de leitura) ou aceitar o estado atual como limite registrado, com o motivo.
3. Registrar o estado das fontes externas e o que foi tentado (já está no inventário).
4. Ter a aprovação do responsável.

Pelos critérios do prompt anterior, a F3 pode ser aceita com perguntas abertas, desde que todas tenham critério explícito e limite documentado. Isso hoje vale para todas, exceto SA22, que é lacuna de implementação recém-descoberta, e as três correções de documentação. **A F3 não está concluída, e esta sessão não a concluiu.**

## Adendo: SA22 (verificação autorizada depois deste parecer)
Script `fase3/ver_sa22.py`, com resultado por seção em `fase3/resultados/sa22.csv` e resumo em `sa22.json`. A validação é a segunda leitura pelo texto impresso (`.imgbusa`).

| Medida | Resultado |
|---|---|
| Seções-turno | 159 (1º turno 116, sendo 99 do exterior; 2º turno 43, sendo 33 do exterior; 27 no Brasil) |
| Arquivos presentes | `.busa`, `.imgbusa`, `.logsajez`, `.rdv` e `.vscsa` em todas; `.logjez` da urna em 11 |
| Motivo da falha | extensões do Sistema de Apuração fora do leitor de 2022 (`TIPO_2022`); nenhum arquivo danificado |
| Verificadas | 159 |
| Sem leitura | 0 |
| Concordância boletim × tabela (votos e comparecimento) | 159 (27.692 votos) |
| Concordância texto impresso × tabela | 159 |
| Divergências objetivas | 0 |
| Assinatura da lista e dos arquivos presentes | 159 válidas: 156 ECDSA P-521 (AC URNA), 3 Ed521 (AC UE2020) |
| Listados na assinatura e ausentes do pacote | `.hash`, `.ver` e `.chvtp` nas 159; `.jufa` em 8 (485 arquivos); sem efeito sobre votos; motivo não verificado |

**Limites:**
- A conferência é **interna**. Boletim, texto impresso, tabela e assinatura vêm da mesma origem (TSE), então não é validação por fonte independente.
- A cadeia de certificados vai só até a AC emissora (P11).
- O leitor geral de 2022 não foi alterado. As 159 seções seguem fora das contagens agregadas antigas por arquivo (por exemplo, P10 em 2022) e foram verificadas à parte.

**Efeito sobre a cobertura:** a frase "todas as seções de 2022 com arquivo foram conferidas" nunca foi feita pelo projeto, e continua não podendo ser feita sem ressalva. Hoje, em 2022:
- Os arquivos presentes das seções com urna foram conferidos pelo pipeline.
- As 159 seções do Sistema de Apuração foram conferidas à parte.
- Faltam no pacote 173 arquivos assinados (A173) e 485 auxiliares (SA22).
