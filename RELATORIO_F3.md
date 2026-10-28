# Relatório da F3, primeira sessão (28/10/2026)

**A F3 não está concluída e não foi congelada.** Esta sessão cumpriu o orçamento definido e termina aqui. O fechamento depende do responsável. Pré-registro: [`fase3/PREREG.md`](fase3/PREREG.md). Inventário mestre: [`fase3/INVENTARIO.md`](fase3/INVENTARIO.md) e `fase3/inventario.json` (27 itens, nenhum omitido). Resultados brutos: `fase3/resultados/`.

## Prestação de contas da sessão
| Limite | Usado |
|---|---|
| 90 min | cerca de 20 min de execução (relógio da máquina, início 05:58) |
| 4 scripts novos | 4: `f3_inventario.py`, `f3_curvas.py`, `f3_zeros.py`, `f3_pendencias.py` |
| 8 experimentos | 8: E1 inventário, E2 curvas, E3 zeros, E4 P18, E5 P20, E6 P19, E7 evidências externas (2 buscas e 1 leitura de página), E8 síntese |
| Sem subagentes, sem deploy, sem download massivo | cumprido; **nada publicado no GitHub nem no site** |
| 1 sensibilidade por experimento | cumprido, exceto no E3 (ver abaixo) |
| 1 correção e 1 repetição por falha | **excedido no E3 e no P19**, declarado abaixo |

**Desvios declarados.** (1) E3: o modelo com prior municipal falhou na validação (esperava 1 zero, havia 79), então acrescentei dois modelos (prior por local de votação e a própria seção no 1º turno) além da sensibilidade por UF: uma correção científica a mais que o orçamento previa. Depois corrigi uma leitura (campo ausente do BU contado como diferente de zero) e repeti uma vez. (2) P19: o primeiro disparo falhou ao ler o código IBGE vazio de um município; corrigi e repeti uma vez. (3) Correção da própria F2: a conta de votos do P2 estava errada (ver "Revisões").

## E2. Curvas de apuração, 2022 e 2026 (pergunta C1 e C2)
**Dados:** ordem real de recebimento dos BUs (`DT_BU_RECEBIDO`), Lula e adversário acumulados (válidos). **Estatísticas fixadas antes:** S1 inversões da liderança parcial após 10% das urnas; S2 fração apurada na última inversão; S3 maior vale da margem relativa; S4 oscilações por faixa de 1%; S5 maior trecho linear. **Nulos:** A permutação irrestrita; B dentro de UF mantendo a sequência de UFs; C dentro de município mantendo a sequência de municípios; 200 permutações cada; sensibilidade de grade (0,5% e 2%) contra o nulo B. Modelo D (snapshots externos): **bloqueado**, não existem.

| | 2026, 1º turno | 2026, 2º turno | 2022, 1º turno | 2022, 2º turno |
|---|---|---|---|---|
| Quem lidera aos 10% apurado | adversário (−10,1 pp) | Lula (+0,96 pp) | adversário (−5,5 pp) | adversário (−4,0 pp) |
| Líder final | adversário | Lula | Lula | Lula |
| Inversões (nível da urna) | 0 | 2 (13,5% e 47,2% apurado) | 3 (68,2%) | 21 (todas em 67,6%) |
| Margem final | −1,87 pp | +3,57 pp | +5,23 pp | +1,81 pp |
| Oscilações S4 (observado / média de A) | 5 / 44 | 11 / 44 | 4 / 44 | 4 / 44 |
| η² da ordem de chegada por UF / município | 0,22 / 0,56 | 0,39 / 0,71 | 0,22 / 0,56 | 0,24 / 0,59 |

**Observações.** (a) A permutação irrestrita (A) é um nulo **inadequado**: simula curvas planas (zero inversões, 44 oscilações), contra 4 a 11 oscilações reais; rejeita tudo em qualquer ano. (b) Os nulos B e C, que preservam a estrutura territorial, ainda rejeitam ao menos uma estatística (p ≤ 0,01 a 0,03) em **todos** os anos e turnos, inclusive 2022 e o 1º turno de 2026 sem nenhuma inversão. A ordem real tem estrutura além do território (tamanho da seção, hora de fechamento, lotes) que nenhum nulo disponível reproduz. (c) As 21 "inversões" do 2º turno de 2022 são oscilações em torno de zero no momento em que Lula assume a liderança (67,6% apurado); contar cruzamentos no nível da urna superestima inversões reais, e o valor de S1 é sensível a isso (limitação do desenho fixado antes).
**Conclusão autorizada:** a pergunta "as curvas são incompatíveis com processos plausíveis?" **não é decidível** com os nulos disponíveis: não se demonstra incompatibilidade e não se demonstra compatibilidade. **Estado: respondida parcialmente** (a observação e a inadequação dos nulos estão demonstradas; o modelo D está bloqueado).

## Comparação 2022 × 2026 (C2)
- **Curvas:** 2022 tem o adversário na frente até 67,6% do 2º turno e Lula assume; em 2026 Lula está à frente aos 10%, perde a liderança aos 13,5% e a retoma aos 47,2%. Não são curvas iguais.
- **Estrutura de chegada:** no 1º turno os dois anos são semelhantes (η² por UF 0,22); no 2º turno a ordem de chegada é mais territorial em 2026 (0,39 contra 0,24).
- **Mudanças entre turnos:** Lula +10,33 mi e adversário +3,69 mi em 2026 (comparecimento +2,92 mi); +3,07 mi e +7,11 mi em 2022 (+0,56 mi).
- **Zeros:** Flávio 79 e 106 seções (2026), Bolsonaro 160 e 141 (2022).
- **Dependência espacial:** Moran's I 0,16 a 0,17 (2026) e 0,18 a 0,20 (2022).
- **Anomalias persistentes:** assimetria de cauda do T02 nos dois anos (concentrada em São Paulo capital em 2022).
- **Limites:** a semelhança visual de gráficos não é semelhança estatística; os dois anos têm candidatos, infraestrutura e formatos diferentes; não há snapshots externos de nenhum.

## E3. Zeros de votos por finalista (Z1)
**Definição:** seção com comparecimento positivo e zero voto para o finalista, por turno e ano (excluído o exterior), dentre as seções com votos válidos nos dois turnos. **Modelo:** beta-binomial com prior leave-one-out (município; sensibilidade por UF; correção por local de votação; correção pela própria seção no 1º turno) e sobredispersão estimada por momentos; controle com os zeros de Lula.
| | observados | esperado, prior municipal | esperado, prior de local | razão (local) |
|---|---|---|---|---|
| Flávio 2026, 1º turno | 79 | 1,2 | 64,5 | 1,2 |
| Flávio 2026, 2º turno | 106 | 1,6 | 82,8 | 1,3 |
| Bolsonaro 2022, 1º turno | 160 | 8,3 | 95,2 | 1,7 |
| Bolsonaro 2022, 2º turno | 141 | 5,2 | 84,9 | 1,7 |
| Controle: Lula 2026, 1º/2º turno | 8 / 4 | 0,6 / 0,2 | 3,8 / 2,4 | 2,1 / 1,7 |
| Controle: Lula 2022, 1º/2º turno | 1 / 2 | 0,4 / 0,5 | 0,4 / 0,4 | 2,5 / 5 |
- **Transições 2026 (Flávio):** 29 de zero para positivo, 56 de positivo para zero, 50 zero nos dois turnos. 2022 (Bolsonaro): 76, 57 e 84.
- **Tamanho e lugar:** mediana de 102 e 124 votos válidos nas seções zero (2026) contra 254 no país; concentração em AM, PA, MA e BA; 62 e 67 municípios distintos (2026).
- **Arquivos das urnas nas seções zero:** em 486 seções-turno, BU, RDV e imagem do BU dão 0 votos para o finalista e o BU bate com a tabela publicada em todas (1 seção de 2022 sem BU lido pelo leitor). Nenhuma seção "zero" é ausência de arquivo ou de informação.
- **Alcance em votos:** 2026, 2º turno: 106 seções com 14.860 votos válidos; pela taxa do local o esperado seria ~44 votos de Flávio (0,001% da margem de 4,43 mi). 2022, 2º turno: 141 seções, 16.418 válidos, ~66 votos.
**Conclusão autorizada:** a contagem binomial homogênea e o prior municipal **não** são modelos válidos para zeros (refutados pela validação). Com o prior de local de votação os zeros observados excedem o esperado em 1,2 a 1,7 vez, mas o controle (zeros de Lula) mostra que o modelo subestima também zeros do outro finalista por cerca de 2 vezes. **Não há evidência de excesso de zeros, nem prova de que o excesso seja nulo**: um excesso modesto não é excluível. Zero isolado não é irregularidade. **Estado: respondida parcialmente.**

## E4. P18, regra do T13 de duas caudas
Regra completa com T1 e T3 contando os dois lados (T1: z robusto > 5 e < −5; T3: ≥ 90% para qualquer finalista), mundo de referência legítimo por bootstrap paramétrico, 1% das urnas, 30 réplicas, dois sentidos, limiar ancorado nos dados reais e limiar calibrado no mundo simulado.
- **2026:** 10% dos válidos movidos (~125 mil votos): detecção 30 de 30 (IC 95% 89% a 100%) em **ambos** os sentidos, pelo T1 de cada lado; 5% (~62 mil votos): 0 de 30 nos dois; falsos alarmes 0 de 30 nas duas calibrações. O T3 e o T4 nunca dispararam.
- **2022 (sensibilidade):** limiar ancorado nos dados reais: Flávio→Lula (aqui Bolsonaro→Lula) 0 de 30 a 10%, Lula→adversário 30 de 30, porque a cauda pró-Lula real de 2022 (90 seções) eleva o limiar; com limiar calibrado no mundo simulado, 30 de 30 nos dois.
**Conclusão autorizada:** a regra de duas caudas é simétrica para troca localizada de ~125 mil votos ou mais, e cega abaixo de ~62 mil nesse desenho; a calibração do limiar decide quem é visto em 2022. Não vale para outros mecanismos (enchimento, troca uniforme) nem para outras frações de urnas. **Estado: respondida** para o desenho delimitado.

## E5. P20, São Paulo capital 2022
29 seções pró-Lula acima de 5 desvios, em 15 locais de votação, 10 delas em um único local (zona 251, local 1074); 10 na zona 251, 10 na 259. As outras seções dos mesmos locais têm z médio +3,6 contra +0,09 nas demais de SP: é o **local inteiro** que se deslocou. Com controle de tamanho e histórico (R² 0,29), só 4 das 29 continuam acima de 5. As mesmas seções em 2026 têm z médio +0,62 (r = 0,45 com 2022; 1 acima de 3). Mediana de eleitores de Lula no 1º turno 34% (47% em SP). Arquivos: lista, hash, assinatura, RDV e log conferem nas 29 (modelos UE2009 a UE2020 variados, nenhuma urna substituída). **Conclusão autorizada:** a assimetria é um efeito de locais de votação inteiros, parcialmente explicável por tamanho e histórico, sem divergência documental; a causa do deslocamento dos locais **não é identificável** com estes dados. **Estado: respondida parcialmente.**

## E6. P19 (e P9), dependência espacial
Moran's I do z médio municipal (5.570 municípios; adjacência por arco compartilhado da malha IBGE, média de 5,7 vizinhos; e 5 vizinhos mais próximos pelo centróide; 999 permutações): 2026: 0,161 e 0,172; 2022: 0,179 e 0,198; p = 0,001 (piso) nos quatro; sem os 5% mais extremos, 0,157 e 0,170. **Conclusão:** há autocorrelação espacial real nos dois anos, um pouco maior em 2022; é estrutura regional que o modelo por UF não captura, não prova de manipulação. **P19: respondida. P9: respondida parcialmente** (agrupamentos específicos não mapeados).

## E7. Evidências externas (P4, P6, P11, P21)
- **Certificados:** busca web e leitura de uma página do TSE (HTTP 403) não entregaram AC URNA v2 nem AC RAIZ UE por canal do TSE. **P11 e P21: bloqueadas.** O elo urna → AC (200 certificados, F2) continua verificado com ACs de terceiros.
- **Snapshots da divulgação:** nenhum arquivo público encontrado. **P4: bloqueada.** A curva do E2 é reconstrução, não observação histórica.
- **Boletins de terceiros:** a imprensa relata comparações da Defesa (442 e 501 urnas em 2022, 0% de inconsistência), do TCU (4.577 seções) e o aplicativo QRTot do TRE-SC; **não** temos dados primários nem proveniência verificável, e não os usei como evidência. **P6: bloqueada.**

## Revisão das conclusões anteriores (E8 e MET)
| Conclusão anterior | Estado agora |
|---|---|
| T13 só vê um sentido (F2) | Corrigido pelo P18 (duas caudas, simétrico); a regra antiga fica registrada |
| Conta de votos do P2 (F2): "~250 mil votos" | **Erro de cálculo meu na F2.** O correto é ~125 mil (1% de 499 mil urnas × ~250 votos × 10%). Corrigido no registro vivo, em `impacto_votos` e em `respostas.json`; as cópias congeladas da rodada 3 conservam o texto original |
| E02: significância dos locais | Enfraquecida na F2 (ρ intralocal); agora com dependência espacial real (P19) |
| T02: assimetria de cauda | Resistiu e se explica em parte por efeito de local (P20); causa dos locais desconhecida |
| T10/T11: curva × permutação | **Exigem evidência adicional**: o nulo de ordem não está calibrado (E2) |
| Zeros: probabilidade binomial homogênea | **Refutada** como modelo; modelo de local resiste com ressalva |
| Contabilidade e C06 (M1) | Mantidos; nenhuma combinação observada é matematicamente impossível; quais transferências ocorreram não é identificável |

## Confiabilidade dos dados (resumo)
Validado: coerência contábil, integridade e assinatura de arquivos (200 + 486 seções-turno de zeros + 29 de SP), correspondência de BU, RDV, imagem, log e tabela publicada (mesma origem), elo urna → AC. **Não validado:** âncora institucional dos certificados, canais de origem independente, qualquer evidência externa. **Independência real:** baixa; BU, RDV, log e tabelas derivam do mesmo equipamento e da mesma cadeia de publicação. Mecanismos que permanecem fora do alcance: alteração anterior à assinatura, troca coerente de pacotes assinados, intervenção uniforme.

## Estado final da fila
Ver `fase3/INVENTARIO.md`. Resumo: respondidas P18, P19; respondidas parcialmente P3, P9, P20, C1, C2, M1, Z1, MET; bloqueadas por evidência externa P4, P6, P11, P21; não executada R1-20; P1, P2, P5, P7, P8, P10, P12 a P17 permanecem como na F2.

## Arquivos
Novos: `fase3/{PREREG.md, f3_inventario.py, f3_curvas.py, f3_zeros.py, f3_pendencias.py, INVENTARIO.md, inventario.json, resultados/*}`. Alterados: `testes/registro.json` (T40 a T42; provas da rodada 4 em T02, T10, T11, T13, E02), `scripts/impacto_votos.py`, `fase2/respostas.json` e `RELATORIO_FASE2_COMPLETA.md` (correção da conta), `rodadas/linha_do_tempo.json` (F3 em andamento), código do site (módulo H). Nada publicado, nenhum deploy, nenhuma versão congelada.
