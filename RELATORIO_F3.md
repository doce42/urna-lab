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

## Sessão 2 (28/10/2026): R1-20 e nulo de ordem condicionado
Autorizada pelo responsável. Dois scripts novos, nenhum subagente, nenhuma correção de modelo, nenhum arquivo do TSE baixado. Pré-registro: adendo no fim de `fase3/PREREG.md`.

**R1-20, reconciliação com a decodificação independente (T43).** O repositório de terceiro DataUrnas-BR (clone raso) contém os votos por seção já decodificados dos BUs. Comparados com a base do projeto, seção a seção:

| Conjunto | Seções comuns | Seções com diferença de votos | Votos comparados |
|---|---|---|---|
| 2026, 1º turno, candidatos | 499.206 | 0 | 119,3 mi |
| 2026, 1º turno, brancos e nulos | 499.206 | 0 | 6,0 mi |
| 2022, 1º turno, candidatos | 470.819 | 0 | 117,9 mi |
| 2022, 2º turno, candidatos | 470.834 | 0 | 118,2 mi |
| 2022, brancos e nulos (1º e 2º) | 470.736 e 470.750 | 0 | 5,4 mi e 5,7 mi |

Em 2022 a base tem 1.194 a 1.292 seções que o DataUrnas não traz (334 mil votos; 1.018 são do exterior e várias são seções agregadas); essas não foram comparadas. O repositório não inclui o 2º turno de 2026. A conclusão é limitada: dois decodificadores independentes concordam, mas a origem (TSE) é a mesma e há uma só versão de publicação. Isto fecha o P3 apenas em parte e resolve o R1-20.

**Nulos de ordem com hora de fechamento e tamanho (C1, MET).** Condicionando em UF × faixa de 30 min do encerramento (D) e também no tercil de eleitores aptos (F), o η² da ordem de chegada sobe pouco (2026, 1º turno: 0,34 → 0,36; 2022, 2º turno: 0,24 → 0,25). Ainda rejeitam a fração da última inversão (S2) em todos os anos e turnos, inclusive o 2º turno de 2022, e o maior vale (S3) em 2026 (p ≈ 0,01). Como o ano de referência também é rejeitado, os nulos não discriminam. C1 passa a **não identificável com estes dados**; T10 e T11 ficam como descrições, não como testes.

**Estado final da fila.** Respondidas: P1, P2, P5, P7, P8, P10, P12 a P19, R1-20. Respondidas parcialmente: P3 (falta a dimensão de versão), P9, P20, C2, M1, Z1, MET. Não identificável com estes dados: C1. Bloqueadas por evidência externa: P4, P6, P11, P21 (certificados AC URNA v2 e AC RAIZ UE, snapshots históricos e boletins de terceiros com dados primários). Nada disso muda a conclusão do estudo: nenhum teste chegou às classes E ou F.

## Revisão da F3 (28/10/2026): auditoria e investigações I1 a I3
A F3 foi encerrada e congelada como V1.2 antes de uma auditoria científica. A auditoria ([`fase3/AUDITORIA_F3.md`](fase3/AUDITORIA_F3.md)) encontrou estados acima da evidência e falhas de registro. Com aprovação do responsável, a fase voltou a **em revisão**. A V1.2 e a tag `v1.2` ficam preservadas, e os desvios do congelamento estão em [`rodadas/rodada-4-desvio.md`](rodadas/rodada-4-desvio.md). As seções anteriores deste relatório ficam como estavam; o que a revisão mudou está aqui e no inventário (campo `historico` de cada item).

**Orçamento:**
- 3 investigações, cada uma com um script principal (`fase3/rev_i1_poder.py`, `rev_i2_zeros.py`, `rev_i3_espacial.py`) e uma etapa de validação ou sensibilidade.
- Nenhuma correção nem repetição por falha técnica, nenhum subagente, nenhum download.
- Pré-registro escrito antes de rodar: [`fase3/PREREG_REVISAO.md`](fase3/PREREG_REVISAO.md).
- Desvio menor: o I1 grava um arquivo por ano (`rev_i1_2026.json`, `rev_i1_2022.json`), e não um só.
- Detalhe de implementação não previsto no pré-registro: no M2, municípios maiores que o alvo de 1% são pulados, o que exclui São Paulo capital.

### Correções de registro
- **R1-20:** o script agora confere o commit 12f0433 do DataUrnas-BR e os SHA-256 das entradas, lendo de uma pasta permanente. A reexecução deu resultado idêntico. A falta de registro na execução original está documentada em `fase3/externos/DATAURNAS.md`, sem reconstruir nada que não pudesse ser verificado.
- **Estados revistos com histórico:** P9, P14, P18, P2, R1-20, C1 (agora "não decidível com os modelos disponíveis"), Z1, P19, P20 e MET.
- **Itens novos:** A173 (173 arquivos de 2022 apontados como ausentes) e BU1 (seção de 2022 com BU não lido), ambos não executados.
- **`fase2/respostas.json`:** atualizado, com histórico.
- **Registro de testes:** provas em T13, T02, E02, T40, T41, T42 e T43, e textos vivos de T41 e T42 corrigidos.

### I1. Poder contra trocas concentradas
Mundos legítimos: binomial em torno dos dados reais, com 20 mundos de calibração e 30 de avaliação separados. Cada mecanismo afeta cerca de 1% das seções (4.9 mil em 2026). Taxa de detecção do conjunto (T13 + E02) com limiar calibrado, em 2026, 2º turno:

| Mecanismo | 2% dos válidos (~25 mil votos) | 5% (~62 mil) | 10% (~123 mil) |
|---|---|---|---|
| Disperso (seções sorteadas) | 1/30 nos dois sentidos | 2/30 e 0/30 | 30/30 nos dois sentidos (pelo T02/T1) |
| Locais de votação inteiros | 2/30 e 1/30 | 30/30 (pelo E02) | 30/30 |
| Municípios inteiros | 2/30 e 1/30 | 30/30 (pelo E02) | 30/30 |
| Região contígua | 4/30 e 2/30 | 29/30 e 27/30 | 30/30 |

- **Falso alarme:** em 2026, o conjunto dá 0/30 com o limiar ancorado no real e 1/30 com o calibrado (IC 95% de 0,6% a 17%).
- **Validação em 2022:** o mesmo padrão aparece com o limiar calibrado (falso alarme 3/30). O limiar ancorado no real dá 7/30 falsos alarmes, e com ele a troca dispersa de 10% a favor de Lula é vista só em 7/30, ou seja, no nível do falso alarme. Esse limiar é inadequado para 2022.
- **T02 e T13 contra troca concentrada:** com a mediana municipal como referência, o T02 não vê troca de 10% aplicada a município ou região inteiros (0/30 no lado afetado), porque a mediana absorve o deslocamento. A regra do T13 sozinha vê essa troca em só 1/30 a 19/30. Quem detecta as trocas concentradas é o E02 (referência estadual), com ρ reestimado em cada mundo.
- **Correção do P18:** os falsos alarmes do limiar calibrado tinham sido medidos nos mesmos mundos da calibração, logo eram 0 por construção.

**Leitura pelo critério pré-registrado, em 2026:**
- **Detectáveis:** troca dispersa de 10%; locais e municípios inteiros a 5% e 10%; região a 10%; região a 5% no sentido para Lula (29/30).
- **Detecção incerta:** região a 5% no sentido contrário (27/30, limite inferior do IC de 74%).
- **Não detectáveis:** toda troca de 2%, exceto região contígua no sentido para Lula (4/30, incerta); troca dispersa de 5%.

**Conclusão permitida:** as conclusões anteriores sobre ausência de sinal valem só acima desses tamanhos e para esses mecanismos. Não excluem trocas de até ~25 mil votos em 1% das seções, trocas dispersas de ~62 mil votos, nem mecanismos que preservem as medianas municipal e estadual. Também não alcançam alterações anteriores à geração do boletim.

### I2. Zeros de votos com modelo calibrado
O modelo é uma beta-binomial com média pelo local de votação sem a própria seção, encolhida para o município, e ρ ajustado sem a célula zero. **Não passou na calibração pré-registrada**:
- **Controles:** Lula 2026 tem 8 zeros contra 0,4 esperados no 1º turno e 4 contra 0,2 no 2º. Os candidatos menores, com dezenas de milhares de zeros, ficam 10% a 22% abaixo do esperado, fora do intervalo.
- **Sensibilidade (prior pela zona):** também falha.

Pelo critério fixado antes, o resultado confirmatório é **não interpretável**: não se conclui excesso nem ausência de excesso. Descritivo, sem valor confirmatório:
- **Cauda baixa:** o modelo subestima toda a cauda baixa dos finalistas, não só o zero, o que indica falha do modelo e não excesso demonstrado. Em Flávio 2026, 1º turno, as seções com 0, 1, 2 e 3 a 5 votos ficam cerca de 20, 12, 7 e 4 vezes acima do modelo; em Bolsonaro 2022, 14, 8, 5 e 3 vezes. O zero faz parte de uma cauda baixa mais pesada que o modelo, com o mesmo formato nos dois anos.
- **Comparação 2026 × 2022:** a razão das razões vai de 1,35 a 1,46, com IC que inclui 1, pelo prior de local, e de 2,4 a 3,4 pelo prior de zona. Depende do modelo, então também não é interpretável.
- **Votos:** os esperados nessas seções vão de ~44 a ~4.800 votos, conforme o modelo.

### I3. Locais de votação com nulo espacial
Cada local foi comparado com a própria zona, sem o local, com escala robusta por faixa de tamanho e BH.

| Ano | Locais significativos (nulo espacial) | Pró-Lula / pró-adversário | Correção só por ρ (P9) | Coincidentes |
|---|---|---|---|---|
| 2026 | 61 de 59.885 | 36 / 25 | 55 (28 / 27) | 28 |
| 2022 | 84 de 56.164 | 46 / 38 | 102 (30 / 72) | 41 |

- **Sensibilidade (município como referência):** 63 locais em 2026 e 80 em 2022.
- **O que resiste:** a ordem de grandeza, cerca de 0,1% dos locais, e o equilíbrio de sentidos em 2026.
- **O que não resiste:** a lista específica de locais e o sentido de 2022, que passa de 72 para 38 pró-adversário.
- **São Paulo capital, 2022:** nenhum dos 15 locais com seções atípicas resiste.
  - Contra a própria zona, os z vão de −1,3 a 2,9, e nenhum é significativo.
  - Sem as seções que os selecionaram, ficam entre −1,7 e 1,5.
  - O local 251/1074, com 10 das 29 seções, fica no nível da sua zona (z −0,3).
  - O deslocamento acompanha a zona: a zona 251 inteira tem o 2º maior z médio das 58 zonas da capital e a 259 o 7º (vizinhança entre zonas não foi medida). A causa continua desconhecida.
  - Em 2026, 1 dos 15 tem z acima de 2 contra a zona (2,03), e nenhum contra o município.

### Pendências mantidas
- **Fonte externa:** P3 (versões de publicação; 2º turno de 2026), P4 (curva histórica), P6 e P21 (boletins de terceiros), P11 (âncora AC URNA v2 e AC RAIZ UE).
- **Investigação incompleta:**
  - P9: nulo geográfico no nível do local e causa dos locais.
  - P14 e P20: causa do deslocamento regional em São Paulo.
  - P18 e P2: mecanismos não testados e coberturas diferentes de 1%.
  - Z1: modelo de cauda baixa validado.
  - C1 e C2: viradas, periodicidade, mudanças de regime e diferenças entre 2022 e 2026, que exigem snapshots ou um modelo de chegada adequado.
  - M1: nada novo.
- **Não executados:** A173 e BU1.

Nenhuma dessas pendências foi declarada refutada ou comprovada pela falha de um modelo. A F3 não está concluída.

## Verificação documental e auditoria de aceitação (28/10/2026)
Em [`fase3/RELATORIO_ACEITACAO_F3.md`](fase3/RELATORIO_ACEITACAO_F3.md).
- **A173:** os 173 arquivos também faltam no pacote baixado pelo projeto; os boletins das 64 seções conferem.
- **BU1:** era um boletim do Sistema de Apuração e confere com a tabela publicada.
- **Lacuna nova (SA22):** 159 seções-turno de 2022 não foram verificadas pelos arquivos.
- **Revisão de I1 a I3 e matriz completa:** no mesmo relatório.
- **Parecer:** a F3 continua em revisão.
- **SA22:** 159 de 159 seções-turno do Sistema de Apuração de 2022 lidas, com boletim, texto impresso e assinatura conferindo com a tabela (conferência interna). Detalhe no adendo do relatório de aceitação.
