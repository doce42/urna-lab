# Relatório da sessão limitada (28/10/2026)

Escopo vigente: duas investigações, conforme os adendos 1 e 2 que substituíram o escopo original (P2 foi para a fila). Pré-registro: [`fase2/sessao_limitada_2026-10-28/PREREG.md`](fase2/sessao_limitada_2026-10-28/PREREG.md), escrito antes das execuções. Início 03:52, fim das execuções 04:28 (relógio da máquina), CPU limitada a 4 threads por `nice`.

## 1. Estado encontrado
Projeto na V1.0-rc1 (tag `rodada-1`, commit `78bef1e`), R1 respondida (20 respondidos, 8 adiados para a Fase 2, nenhum aberto), `make verificar` passando, baseline V1.0 pendente. Diretório de trabalho sem repositório git próprio (a publicação é por cópia higienizada, `scripts/publicar.py`).

## 2. Versão e commit
Dados e código do estado vivo após a R1. Durante a sessão o responsável **aprovou a baseline V1.0** (mensagem de 28/10, condicionada a "fazer sentido logicamente"): conferi os seis critérios de `revisoes/README.md` (todos cumpridos), congelei a **rodada 2** (`rodadas/rodada-2/`, 48 testes, 30 arquivos com SHA-256) e publiquei com a tag `v1.0`. Os resultados desta sessão entram como provas da **rodada 3** e não alteram a rodada 2.

## 3. Investigações selecionadas
1. **P1 + hipótese de manipulação sobre o crescimento de Lula** (Adendo 1).
2. **Confiabilidade dos dados públicos** (Adendo 2): verificação A (20 seções) e verificação B (confronto independente).

## INVESTIGAÇÃO 1

### 4. Métodos e hipótese
- **A. Contabilidade** (sem modelo): identidades, limites determinísticos, reprodução do C06 gravado. `p1_c06_adversarial.py`.
- **B. Adversarial:** o estimador C06 (cópia literal) aplicado a dados sintéticos com X real e taxas de transição conhecidas que variam por município (S0 homogêneo; S1 heterogeneidade independente de X; S2± heterogeneidade correlacionada ao voto de Lula do município dentro da UF; γ=0,5 principal, γ=1,0 sensibilidade; 10 réplicas por cenário; 2026 e 2022 separados).
- **Hipótese de manipulação (única):** *enchimento/transferência localizada de votos para Lula usando eleitores ausentes.* Motivo: é a que o dado permite refutar de forma direta (deixa assinatura de comparecimento), é relevante ao tamanho do crescimento, e os testes T02 e T07 já mostram um excesso pró-Lula na cauda. Não foi escolhida por parecer suspeita; a assimetria do T02 foi o ponto de partida, não a conclusão. `h1_outliers_lula.py` (dados já preparados).

### 5. Resultados — contabilidade (seções com ≥50 aptos nos dois turnos, as mesmas do C06)
| | 2026 | 2022 |
|---|---|---|
| Δ votos de Lula (2º−1º) | +10.333.758 | +3.072.672 |
| Δ votos do adversário | +3.693.982 | +7.111.212 |
| Δ comparecimento | +2.920.949 | +564.627 |
| Eliminados + queda de brancos/nulos + queda de abstenção ("reservatório") | 14.027.740 | 10.183.884 |
| Identidade Δlula + Δadv = reservatório | exata | exata |
| Ganho de Lula como fração do reservatório | 74% | 30% |
| Abstenção do 1º turno | 32.893.286 | 32.378.875 |

- **Identidade contábil:** fecha exatamente nos dois anos. O crescimento de Lula é aritmeticamente possível sem nenhuma troca direta entre finalistas: cabe no reservatório com sobra.
- **Limites matemáticos:** votos de quem se absteve no 1º turno que foram a Lula: mínimo 0, máximo 32,9 mi (2026). Os limites não identificam a transferência. O C06b (Duncan-Davis, troca direta) segue como registrado (79 a 43,6 mi); sua rastreabilidade em script continua na fila (P13).
- **Reprodução do C06 gravado:** diferença máxima da matriz 4,8e-5 (2026) e 5,0e-5 (2022), 27 UFs, todas convergiram.
- **Estimativa C06 de quem se absteve no 1º turno (rótulo: estimativa ecológica):** 2026, 3,18 mi a Lula e 0,79 mi ao adversário (razão 4,0:1). **2022: 0,74 mi a Lula e 1,32 mi ao adversário (razão 0,56:1), sentido oposto.** O comparecimento subiu 5 vezes mais em 2026.
- **Transferências diretamente observadas:** nenhuma fonte independente existe (voto secreto; não há cruzamento individual). Não avaliável.

### 6. Resultados — adversarial (médias de 10 réplicas; razão = Abs→Lula : Abs→Adv)
| Cenário | 2026 verdade | 2026 estimado | 2022 verdade | 2022 estimado |
|---|---|---|---|---|
| S0 homogêneo (γ=0) | 4,01 | 4,12 (3,94–4,23) | 0,56 | 0,56 |
| S1 aleatório, γ=0,5 | 3,68 | 3,78 (2,75–5,48) | 0,57 | 0,50 (0,25–0,77) |
| S2+ contextual, γ=0,5 | 3,60 | **10,55** | 0,42 | 0,36 |
| S2− contextual, γ=0,5 | 4,05 | **2,29** | 0,77 | 0,50 |
| S1, γ=1,0 | 3,67 | 4,64 (2,45–8,06) | 0,61 | 0,42 |
| S2+ γ=1,0 | 2,95 | **11,81** | 0,33 | 0,22 |
| S2− γ=1,0 | 3,63 | **1,70** | 1,08 | **0,58** |

- Erro absoluto nas células Abs→Lula e Abs→Adv: ≤0,02 em γ=0,5 (critério pré-registrado de ≤0,03: **cumprido**) e até 0,046 em γ=1,0 (**não cumprido**).
- Critério de recuperação em S0/S1 (erro relativo da razão ≤25%): cumprido na média, **não** na pior réplica de S1 (2,75–5,48 contra 3,68).
- Reproduzir o total do 2º turno não discrimina: o erro médio do total de Lula no 2º turno fica abaixo de 0,4% (γ=0,5) e 1,3% (γ=1,0) mesmo quando a razão está errada em fator 3.
- A ordem Abs→Lula > Abs→Adv de 2026 foi preservada em todos os cenários; em 2022 a ordem inversa estimada também, exceto S2− γ=1,0, em que a verdade (1,08) tem Lula ligeiramente acima e o estimador dá 0,58.
- γ **não é calibrado à realidade**: isto mede sensibilidade do estimador, não a heterogeneidade real.

### 7. Hipótese de manipulação: A a H
**A. Mecanismo.** Votos extras para Lula em seções sorteadas ou escolhidas, lançados em nome de eleitores ausentes (ou trocas em urna).
**B. Previsões.** Excesso unilateral de seções com virada acima do município; comparecimento subindo junto nessas seções; assinatura de comparecimento ≥95% com ≥90% Lula (T07); desvio da curva (T10).
**C. Favoráveis.** T02: 32 seções pró-Lula contra 13 pró-outro além de 5 desvios em 2026; em 2022, 90 contra 13. A assimetria aparece também a 3 e 4 desvios (1.997×692 e 190×53 em 2026), isto é, a distribuição tem a cauda pró-Lula mais pesada.
**D. Contrárias.** (i) Nas seções pró-Lula a mudança de comparecimento relativa ao município é negativa (−1,8 pp em 2026, −0,6 pp em 2022), 44% e 48% positivas contra 50% no conjunto. (ii) T07: 0 seções acima de 100%, canto igual a 2022. (iii) T10: desvio máximo 0,08 pp (município). (iv) O excesso total de votos nessas seções é ~740 (2026) e ~2.600 (2022), ordem de 0,007% e 0,08% do ganho de Lula. (v) Em 2026, nas seções acima da mediana de tamanho, 6 pró-Lula e 8 pró-outro: sem assimetria; em 2022, 46 contra 2, concentrada (SP 32 das 90).
**E. Alternativas legítimas.** Cauda assimétrica da própria distribuição de virada (o corpo é só levemente assimétrico, razão q99/q01 1,12 em 2026); mobilização desigual; heterogeneidade territorial; efeito de modelo (resíduo relativo à mediana do município).
**F. Testes existentes.** T02, T03, T07, T10, T11, E01/E02, C06, C06b.
**G. Refutação.** (1) Foi demonstrada uma **correção metodológica no C06**: a razão "4:1" não sobrevive a heterogeneidade contextual de estresse; só ordem e contraste 2022×2026 sobrevivem. A conclusão já dizia "estimativa"; agora há medida do quanto a magnitude depende do pressuposto. (2) A assinatura de comparecimento prevista pelo mecanismo **não apareceu**.
**H. Seguro afirmar.** O crescimento de Lula nos dois anos é contabilmente reconciliável com os registros. A hipótese de enchimento localizado via ausentes **não encontrou sustentação** no sinal que lhe cabe (comparecimento), em 2026 nem em 2022. Isso **não exclui** troca em urna sem alteração de comparecimento nem alteração uniforme; a causa da assimetria de cauda do T02, mais forte em 2022 nas seções maiores, permanece desconhecida. Não há evidência de intenção, autoria ou impacto agregado.

### 8. Classificação de evidência
Anomalia estatística: assimetria de cauda do T02 (persiste). Inconsistência contábil: nenhuma. Divergência documental: nenhuma nova. Divergência criptográfica: nenhuma. Alteração de registros, intervenção deliberada e impacto agregado: **sem evidência**.

## INVESTIGAÇÃO 2 — Confiabilidade dos dados públicos: verificações realizadas, evidências independentes e limites científicos

### Verificação A (`v_a_secoes.py`, resultado em `va_resultado.json`)
**Seleção fixada antes de inspecionar:** 10 exceções do T36 (obrigatórias a sem-explicação e a `d_fora_do_bu`; as outras por `default_rng(2026)`), mais 10 aleatórias de `default_rng(2027)` no universo de urnas do 1º turno 2026. **Amostra estratificada de conveniência: não generaliza.**

| Propriedade verificada | Resultado |
|---|---|
| Tamanho e SHA-512 de BU, log, RDV e imagem do BU contra a lista assinada da própria urna | 19 de 19 seções com arquivos conferem |
| Assinatura da lista e de cada arquivo com a chave do certificado da urna | 19 de 19 válidas (Ed521 e ECDSA P-521) |
| Chave da seção (seção, zona, município) dentro do `bu.dat` | 19 de 19 (UF só confere pelo nome do arquivo) |
| RDV recontado = BU | 18 de 19; AL 28339/13/118 difere em 1 nulo = voto nulo por suspensão (`rdv_tipo6`) que meu comparador não somou: falha do verificador desta sessão, não do dado (BU 17 = RDV 16+1) |
| Imagem do BU = BU | 19 de 19 |
| BU = BU na Web (candidatos, branco, nulo, comparecimento) | 19 de 19 |
| Votos computados no log = comparecimento do BU | 18 de 19; RJ 58971/87/184 (256 contra 258) já é caso documentado do T36 (tipo a e b, classificado "compatível") |
| Seção do Sistema de Apuração (ZZ 29564/1/91) | sem lista assinada de urna, `busa`+`rdv` apenas; já documentada no T36 (D1) e na cobertura do `make verificar` |
| Emissor do certificado até âncora | **não verificado**: emissores observados (AC UE2020, AC UE2022, AC URNA) sem cadeia até raiz TSE no material obtido (R1-01, P11) |

### Verificação B (confronto independente)
**Não realizada, por indisponibilidade:** o repositório local não contém boletins impressos de terceiros, QR Codes preservados externamente nem capturas históricas independentes. O que existe é do mesmo canal do TSE (tabelas, BU na Web, totais, CEFT, pacotes) ou é código de terceiros (DataUrnas, em `revisoes/R1-codex/original/fontes`), não dado. A lista `20220829-LEGAL-qrcode-hashes.txt` é de hashes de chaves públicas do QR de 2022, não das chaves das urnas, e não fecha a cadeia delas. Sem coleta massiva (proibida), a verificação terminou aqui. A pergunta fica em P3, P6 e P11.

### Respostas obrigatórias
1. **Efetivamente verificado:** consistência interna entre BU, RDV, imagem do BU, log e BU na Web; hashes e assinaturas contra a lista assinada pela própria urna; completude por seção (`make verificar`: 499.206 e 499.205 de 499.206 e 499.205); soma das urnas = total oficial (638 de 638).
2. **Correspondência:** as 19 seções verificadas, e o universo conforme T01/T14/T16/T17/T32 (já registrados, não repetidos).
3. **Divergências objetivas:** eleitorado do exterior (−495/−525, T32), 186 casos do T36 no 1º turno (1 sem explicação: RJ 60011/8/61; verificada aqui nos arquivos: lista, hash, assinatura, RDV, imagem e BU na Web conferem, e o log 311 bate com comparecimento 311; a pendência é a conta de confirmações), 1 log não publicado no 2º turno (D1), RJ 58971/87/184 (log 256 contra comparecimento 258).
4. **Anomalias estatísticas persistentes:** T02 (assimetria de cauda pró-Lula, 2022 e 2026), E02, T28 (13 urnas no 1º turno). Todas exploratórias, sem causa determinada.
5. **Possíveis problemas de coleta/publicação/processamento:** falha do meu comparador (tipo 6) é processamento; o log faltante é publicação; os 41 e 423 itens do exterior são cadastro.
6. **Alterações detectáveis pelos testes existentes:** troca ou enchimento localizado em urnas isoladas que deixe diferença com o BU, o RDV ou o log assinados; troca local grande em seções (T02/T13). Alteração antes da assinatura, ou uma troca coerente de BU+RDV+imagem com nova assinatura válida, só seria vista pela cadeia de certificados.
7. **Não identificáveis:** alteração anterior à geração do BU/RDV assinado; software da urna; troca de pacote inteiro validamente assinado; intervenção uniforme (T13: troca uniforme não vista); canal comum de origem de BU, RDV e log.
8. **Evidência externa necessária:** cadeia de certificados até âncora TSE obtida por canal confiável (P11); boletins impressos fotografados por terceiros em amostra; QR de BUs; capturas históricas da totalização; logs públicos de teste de integridade com votos conhecidos (P3, P4, P6).
9. **Só vale para a amostra:** toda a Verificação A.
10. **Alcance da confiança:** os dados são **internamente coerentes e conferem com as assinaturas apresentadas pelas próprias urnas**. Isso não demonstra autenticidade das chaves, nem que os eventos registrados correspondem aos que ocorreram, nem exclui alteração anterior à assinatura. Concordância de BU, RDV e log pode refletir a mesma origem. Nenhuma divergência objetiva encontrada nesta sessão indica alteração.

## 9. Testes que resistiram ou foram enfraquecidos
- **C06 (método):** ajustado (magnitude do "4:1" depende do pressuposto; ordem e contraste 2022×2026 resistem).
- **T02 (interpretação exploratória):** resistiu. **T16/T14/T17 (amostra):** resistiram. Nenhuma classificação foi alterada.

## 10. Limitações e problemas
Estresse do P1 não calibrado; só uma família de heterogeneidade (logit linear em um contexto); 10 réplicas (a variação entre réplicas em S1 é grande); contabilidade sobre as seções com ≥50 aptos (64,05 mi de Lula no 2º turno contra 64,26 mi no total); h1 usa a definição do T02 (um lado para os votos), sem teste formal de assimetria; ZZ fora do C06; o identificador de UF no BU não foi checado; falha do comparador (tipo 6) corrigida na leitura, não no script.

## 11. Fila de perguntas futuras (não executadas)
P2 (poder da regra T13 nos dois sentidos: observação prévia, o T1 e o T3 só contam um lado). Novas: **P14** causa da assimetria de cauda do T02 em 2022 (SP 32 de 90, seções maiores); **P15** C06 com covariáveis municipais e limites de Fréchet por UF para a razão Abs→Lula:Abs→Adv; **P16** corrigir o comparador do RDV (tipo 6) em `v_a_secoes.py` e repetir sobre amostra maior; **P17** teste formal de assimetria (bootstrap por município) da cauda do T02.

## 12. Arquivos e execuções
Novos: `fase2/sessao_limitada_2026-10-28/{PREREG.md, p1_c06_adversarial.py, p1_resumo.py, p1_resultado_principal.json, p1_resultado_sensibilidade.json, p1_resultado_principal_fumaca.json, h1_outliers_lula.py, h1_resultado.json, v_a_secoes.py, va_resultado.json}`. Alterados: `testes/registro.json` (5 provas, rodada 3; V1.0 na história de cada um dos 48 testes), `CONCLUSAO.md` (estado), `RODADAS.md`, `FASE2.md`, `revisoes/README.md`, `rodadas/linha_do_tempo.json`, `rodadas/rodada-2/`, página inicial e linha do tempo do site. Nenhum snapshot congelado foi alterado.
Execuções: P1 principal (1), P1 sensibilidade (1), mais 1 fumaça de desenvolvimento (3 UFs, 1 réplica, não conta como resultado); hipótese (1 execução, 2 anos como replicação); Verificação A (1 execução, depois de uma falha operacional de leitura do RDV de seção do Sistema de Apuração corrigida com `try/except` igual ao do pipeline, uma repetição); Verificação B não executada. Tempo: ~40 min de execução, ~17 min por rodada do P1.
