# Auditoria da F3 (28/10/2026)

Auditoria documental e técnica, sem experimento novo. Fontes lidas: `fase3/*.py`, `fase3/resultados/*.json`, `fase3/PREREG.md`, `fase3/inventario.json`, `RELATORIO_F3.md`, `fase2/respostas.json`, `FASE2.md`, `testes/registro.json`, `rodadas/` (rodada-4 e linha do tempo), `analise/montar_base.py`, o repositório público `urna-lab-publico` e o site no ar.

## 1. Estado real

| Pergunta | Resposta | Evidência |
|---|---|---|
| A F3 foi executada? | Sim, em duas sessões | 6 scripts em `fase3/`, 7 JSON em `fase3/resultados/` com números consistentes com o relatório |
| Foi documentada? | Sim | `PREREG.md` (com adendo), `INVENTARIO.md` (27 itens), `RELATORIO_F3.md`, `CONCLUSAO.md`, registro (T40 a T43) |
| Foi publicada? | Sim | GitHub `main` = 86c3aef (local = publicado; as únicas diferenças são caminhos sanitizados); tag `v1.2` → f74b91f; site no ar mostra F3 "concluida" |
| Foi validada? | **Não** | Nenhuma revisão independente da F3; `verificar.py` confere documentação e totais, não as conclusões da F3. Esta auditoria encontrou problemas listados na seção 4 |

Diretório de trabalho não é repositório git (branch `master` sem commits); o versionamento real está em `urna-lab-publico` (branch `main`, limpo, igual a `origin/main`). Não há suíte de testes unitários; `make teste` roda testes do registro; `scripts/verificar.py` termina com "tudo ok".

## 2. Problemas de registro e reprodutibilidade

1. **F3 marcada como concluída e V1.2 congelada** com base na mensagem "terminar a f3 inteira agora autorizo", antes desta auditoria. Pelos critérios da seção 9 do prompt atual, a F3 não é satisfatória (ver seção 4).
2. **Rodada 4 alterada depois de congelar:** `CONCLUSAO.md`, `INVENTARIO.md` e `fase3_resultados/` foram copiados para `rodadas/rodada-4/` 17 s depois do `fechar`; não estão entre os 30 arquivos com SHA-256 do `resumo.json`. A rodada 4 também não tem `proveniencia.json` (a rodada 3 tem).
3. **R1-20 não reproduzível:** `f3_reconcilia.py` lê o DataUrnas-BR de um diretório temporário da sessão (caminho absoluto em `/tmp/...`, também publicado). O commit usado (12f0433, 15/10/2026) e os hashes dos parquet não foram registrados no resultado.
4. **Fonte desatualizada:** em `fase2/respostas.json`, P18 a P21 continuam "aberta"; o estado final só existe no inventário (o site faz a fusão).
5. **Tag `v1.2`** aponta para o commit anterior à correção do site (86c3aef); só afeta exibição.

## 3. Matriz de perguntas

Estados: R respondida, RP respondida parcialmente, NI não identificável com estes dados, B bloqueada por evidência externa, NE não executada. "Inventário" = estado declarado no inventário da F3; "Auditoria" = estado que esta auditoria sustenta.

| Pergunta | Estado F2 | Executada na F3? | Evidência (arquivo) | Conclusão permitida | Lacuna | Inventário → Auditoria | Prioridade |
|---|---|---|---|---|---|---|---|
| P1 C06 sob heterogeneidade | R | Não (não reaberta) | `fase2/resultados` | Ordem e contraste 2022 resistem; magnitude "4:1" não (±0,5 a ±1,5 mi) | — | R → R | — |
| P2 sensibilidade da regra | R (assimétrica) | Revisada pelo P18 | `p18.json` | Ver P18 | Mecanismos concentrados | R → RP | Alta (ver P18) |
| P3 canais e versões | RP | Sim (E3, R1-20) | `E3_zeros.json`, `R1_20_dataurnas.json` | Tabela `bweb` publicada = decodificação do BU por terceiro, em todas as seções comuns (2026 1T; 2022 1T e 2T) | Versão (uma captura só); 2026 2T fora do DataUrnas; origem comum | RP → RP | Média |
| P4 curva pública histórica | Inventariada | Tentativa externa (E7) | `RELATORIO_F3.md` | Nenhuma curva histórica observada disponível | Snapshots datados da divulgação | B → B | Baixa (sem dado) |
| P5 modelo de urna | R | Não | — | Equivalente a zero em ±0,02 logit | — | R → R | — |
| P6 boletins de terceiros | Inventariada | Busca (E7) | `RELATORIO_F3.md` | Só citações de imprensa; nenhum dado primário | Listas de seções e valores dos terceiros | B → B | Baixa (sem dado) |
| P7 urna trocada (TOST) | R | Não | — | Equivalência na margem ±0,10 z | — | R → R | — |
| P8 T03 com bootstrap | R | Não | — | Efeito desprezível | — | R → R | — |
| P9 locais do E02 calibrados e espaciais | RP | **Só o pré-requisito** (Moran no P19) | `p19.json` | Dependência espacial existe; **não se sabe** quantos locais sobrevivem a um nulo espacial | Recalcular significância dos locais com dependência espacial | RP → **NE (no essencial)** | **Alta** |
| P10 T28 beta-binomial | R | Não | — | 8 de 13 urnas seguem sinalizadas (99 votos) | — | R → R | — |
| P11 âncora criptográfica | RP | Tentativa (E7: HTTP 403) | `RELATORIO_F3.md` | Urna → AC verificada com AC de terceiro; elo AC → raiz não | AC URNA v2 e AC RAIZ UE por canal do TSE | B → B | Média (pedido ao TSE) |
| P12 eleitorado exterior | R | Não | — | Explicada, resíduo zero | — | R → R | — |
| P13 C06b reproduzível | R | Não | — | 79 e 123 reproduzidos | — | R → R | — |
| P14 **causa** da assimetria do T02 | "R" | Parcial (via P20) | `p20.json` | Localização: locais inteiros em SP capital (2022). **Causa não demonstrada** | Covariáveis de local; dado externo do local | R → **RP** (classificação da F2 excedia a evidência) | Alta |
| P15 Fréchet | R | Não | — | Razão não identificada | — | R → R | — |
| P16 200 seções | R | Não | — | 200/200 concordam (1º turno) | 2º turno de 2026 não amostrado nesta verificação | R → R | Baixa |
| P17 assimetria significativa | R | Não | — | Real com bootstrap por município; sem causa | Causa (P14) | R → R | — |
| P18 T13 bilateral | Aberta | Sim | `p18.json` | 2026: 10% dos válidos em 1% das urnas sorteadas (~125 mil votos) detectado 30/30 nos dois sentidos, **só pelo T1**; 5% (~62 mil) 0/30 (IC 95% 0 a 11%); 2022 depende do limiar | Só urnas sorteadas ao acaso; manipulação concentrada (local, município) não testada e tende a ser absorvida pela mediana municipal | R → **RP** | **Alta** |
| P19 Moran's I | Aberta | Sim | `p19.json` | I = 0,16 a 0,20 (p = 0,001) no z médio municipal do modelo com virada do estado | A frase "estrutura regional, não manipulação" excede o teste: Moran não distingue causa | R → R (com redação corrigida) | Baixa |
| P20 SP 2022 | Aberta | Sim | `p20.json` | 29 seções em 15 locais (10 num local); outras seções dos mesmos locais têm z médio +3,6; 4 de 29 seguem acima de 5 após controle (R² 0,29); persistência parcial em 2026 (r = 0,45); 29/29 arquivos conferem | Causa; o controle foi ajustado nas próprias seções selecionadas pelo extremo (regressão à média esperada) | RP → RP | Média |
| P21 terceiros + cadeia | Aberta | Tentativa | — | Nada obtido | Mesmo que P6 e P11 | B → B | Média |
| R1-20 DataUrnas | Pendente | Sim | `R1_20_dataurnas.json` | 0 diferenças em 499.206 seções (2026 1T) e ~470,8 mil por turno (2022) | Reprodutibilidade (seção 2); 2026 2T; 1.194 a 1.292 seções de 2022 só na base (334 mil votos) | R → **RP** até registrar commit e hashes | Alta (barata) |
| C1 curvas × nulos | Nova | Sim (5 nulos) | `E2_curvas.json`, `E2b_curvas.json` | Nenhum nulo testado é calibrado, nem em 2022; a curva é **reconstrução retrospectiva** por `DT_BU_RECEBIDO`, não a curva divulgada | Snapshots históricos; S1 conta trocas de sinal urna a urna (2022 2T: 21 "inversões" todas a 67,6%, ruído no cruzamento) | NI → **RP** ("não decidível com os nulos disponíveis"; não é não identificabilidade matemática) | Baixa |
| C2 2022 × 2026 | Nova | Sim | `E2_curvas.json` | Descrição: 2026 2T troca a liderança aos 13,5% e 47,2%; 2022 2T o adversário lidera até 67,6%; ordem mais territorial em 2026 (η² UF 0,39 × 0,24) | Sem teste formal de diferença | RP → RP | Baixa |
| M1 mudança entre turnos | Nova | **Não** (usa a F2) | C06, T37, T38, C06b, P15 | Contas fecham; fluxos não identificáveis; razão 4:1 frágil | Nenhuma análise nova na F3 | RP → RP (herdado) | Média |
| Z1 zeros | Nova | Sim | `E3_zeros.json` | Ver seção 4.3 | Calibração do modelo | RP → RP (redação a corrigir) | **Alta** |
| MET revisão de métodos | Nova | Sim (parcial) | relatório | T10/T11 viram descrição; T13 simetrizado | P9 e mecanismos concentrados | RP → RP | — |

## 4. Tentativas de refutação

### 4.1 Curvas (C1, C2)
- **Ordem usada:** `DT_BU_RECEBIDO` da tabela `bweb` do TSE. É a hora de recebimento do boletim, não a hora em que o resultado foi divulgado; a diferença entre recebimento e divulgação **não foi examinada** (não há dado). O relatório diz isso (P4), mas a conclusão C2 descreve "momentos de virada" como se fossem da curva pública.
- **S1 mal definido:** conta trocas de sinal urna a urna depois de 10% das urnas. Em 2022 2T são 21 trocas no mesmo ponto (67,6%): ruído no cruzamento. Sob os nulos B e C, S1 simulado é 53 a 64 em 2026 2T contra 2 observados: a curva real é **mais suave** que os nulos, não mais irregular.
- **S2 rejeitado em todos os anos:** a última troca de liderança vem mais tarde do que nos nulos (2026 2T: 0,47 contra 0,26 a 0,41; 2022 2T: 0,68 contra 0,38 a 0,48). Isso é uma característica real das duas eleições, não exclusiva de 2026.
- **Múltiplas comparações:** 5 estatísticas × 5 nulos × 4 curvas, com piso de p = 0,01 (200 permutações), sem correção.
- **Ajuste pós-observação:** os nulos D e F foram desenhados depois de ver B e C falharem (o adendo foi escrito antes de rodar, mas a escolha não é cega).
- **Conclusão sustentável:** com os dados públicos, a forma da curva não permite inferência sobre manipulação em nenhum sentido. "Não identificável" deve ser reescrito como "não decidível com os modelos de chegada disponíveis".

### 4.2 Mudança entre turnos (M1)
Separada corretamente da virada durante a apuração (C1 e C2 são itens distintos). A F3 não fez experimento novo: crescimento absoluto, eliminados, brancos e nulos, comparecimento e limites vêm da F2 (C06, T37, T38, C06b, P15) e do T02. A conclusão vigente (contas fecham, fluxos não identificáveis, magnitude frágil) continua válida e não foi reforçada nem enfraquecida.

### 4.3 Zeros (Z1)
- Universo: seções fora do exterior com válidos nos dois turnos (497.897 em 2026; 471.010 em 2022). Contagem, transições e conferência de arquivos feitas para 2022 e 2026, por turno.
- Números do JSON (observado / esperado com prior de local de votação): Flávio 2026: 79 / 64,5 (1,23×) e 106 / 82,8 (1,28×); Bolsonaro 2022: 160 / 95,2 (1,68×) e 141 / 84,9 (1,66×). Controle Lula: 2026 8 / 3,8 (2,1×) e 4 / 2,4 (1,7×); 2022 1 / 0,36 e 2 / 0,40.
- O prior de local foi escolhido **depois** de o prior municipal falhar (esperado 1,2 contra 79): seleção de modelo pós-observação, declarada.
- Com o preditor do próprio 1º turno, o esperado de 2022 2T é 362 contra 141 observados: o modelo erra para os dois lados. Os esperados dependem fortemente do modelo (62 a 83 para 2026 2T; 85 a 362 para 2022 2T).
- Não há intervalo de predição nem calibração formal. A redação "sem evidência de excesso" é mais forte do que o teste permite. **Redação sustentável:** "o excesso relativo de 2026 (1,2 a 1,3×) é menor que o de 2022 (1,7×) com o mesmo modelo; o modelo não é calibrado na cauda, então nem excesso nem ausência de excesso foram demonstrados".
- Arquivos: 0 divergências de votos entre BU, RDV, imagem e tabela nas 185 seções-turno de 2026 e nas 301 de 2022, **exceto 1 seção de 2022 (1º turno) com BU não lido pelo leitor**, que não foi verificada. Não é divergência demonstrada, mas também não é concordância.

### 4.4 Confiabilidade dos dados (D)
- Integridade e assinatura dos arquivos: verificadas nacionalmente na baseline; certificados verificados até a AC emissora com AC de terceiro (P11).
- Correspondência entre canais: `bweb` × BU (baseline) e `bweb` × decodificação do DataUrnas (R1-20). Mesma origem.
- Independência BU/RDV/log: são gerados pela mesma urna; concordância entre eles não testa alteração anterior à geração. Documentado na conclusão da baseline; a F3 não acrescentou nada aqui.
- Fontes externas independentes: nenhuma com dado primário.
- Achado externo não incorporado: o README do DataUrnas-BR registra 173 arquivos assinados ausentes do pacote de dados abertos de 2022 (64 seções, maioria do exterior). Não foi confrontado com a base do projeto.

### 4.5 Poder (P18)
Injeção em 1% das urnas **sorteadas ao acaso**, 30 réplicas, 5% e 10% dos válidos. A detecção vem inteira do T1 (contagem de |z| > 5); T2, T3 e T4 quase não contribuem. Manipulação concentrada (locais ou municípios inteiros) não foi testada e tende a ser absorvida pela mediana municipal usada no T02. Pela regra "um teste incapaz de detectar um mecanismo não permite excluí-lo", a bateria não exclui manipulação concentrada nem difusa abaixo de ~10% dos válidos em 1% das urnas.

## 5. Síntese

- **A. Demonstrado pela F3:** concordância seção a seção entre a tabela publicada e a decodificação independente do BU (2026 1T, 2022); simetria do T13 bilateral para injeção aleatória de 10%; dependência espacial do z municipal; efeito de local de votação nas seções atípicas de SP 2022; 0 divergências de arquivo nas seções com zero votos (com 1 exceção não verificada); inadequação dos nulos de permutação para a curva.
- **B. Refutado ou enfraquecido:** T10 e T11 como testes (viram descrição); P14 "respondida" (a causa não foi demonstrada); "~250 mil votos" (corrigido para ~125 mil); prior municipal dos zeros.
- **C. Robusto e sem causa:** assimetria de cauda do T02 (P17), concentrada em locais inteiros de SP capital em 2022 e com persistência parcial em 2026; última troca de liderança mais tardia que os nulos nos dois anos; dependência espacial municipal.
- **D. Respostas parciais:** P3, P14, P18, P20, R1-20 (reprodutibilidade), C1, C2, M1, Z1, MET.
- **E. Não executadas:** P9 no essencial; M1 sem análise nova; manipulação concentrada (P2/P18); seção de 2022 com BU não lido; 173 arquivos ausentes de 2022 apontados pelo DataUrnas.
- **F. Dependem de fonte externa:** P4 (snapshots datados), P6 e P21 (boletins de terceiros com dados primários), P11 e P21 (AC URNA v2 e AC RAIZ UE do TSE).
- **G. Problemas metodológicos capazes de mudar conclusões:** S1 das curvas; seleção pós-observação dos nulos D/F e do prior de zeros; ausência de calibração no modelo de zeros; poder testado só para injeção aleatória; controle do P20 ajustado nas seções selecionadas pelo extremo.
- **H. Snapshots e publicação:** rodada 4 (V1.2) congelada e publicada com F3 "concluída"; arquivos acrescentados depois do congelamento sem hash; sem `proveniencia.json`; tag `v1.2` antes da correção do site; R1-20 depende de diretório temporário.
