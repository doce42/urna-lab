# Pré-registro da sessão limitada (28/10/2026, escrito antes de qualquer execução nova)

Escopo: P1 e P2 de `FASE2.md`. Tetos: 2 investigações, 2 execuções por investigação (principal + validação/sensibilidade), 90 min, sem subagentes, sem reprocessamento nacional, sem novo download. Um teste de fumaça (poucos UFs, 1 réplica) é desenvolvimento e será declarado no relatório.

## P1 — C06 sob heterogeneidade (script `p1_c06_adversarial.py`)
Pergunta: o estimador C06 (Goodman restrito por UF, cópia literal de `analise/comportamento.py`) recupera a matriz nacional verdadeira quando as taxas de transferência variam entre municípios?

**Parte A (contabilidade, sem modelo).** Para 2026 e 2022 separadamente: (i) identidade ΔLula = ΔAdv + fontes; (ii) reprodução do C06 gravado (matriz e conferência de totais) a partir de `base*.parquet`; (iii) limites determinísticos nacionais (sem identificação de trocas diretas); (iv) decomposição estimada do ganho de Lula por origem, rotulada como estimativa.

**Parte B (adversarial).** X = frações reais por seção (mesmas linhas e UFs do C06). Verdade central B0 = matriz C06 gravada do ano. Taxa da seção i (município m, z_m): B_i[j,:] = softmax(log B0[j,:] + γ·s·z_m·d), d = (+1 Lula, −1 Adversário, 0 branco/nulo, 0 abstenção), aplicado a todas as origens j.
- S0: γ=0 (homogêneo na UF; controle).
- S1: z_m ~ N(0,1) independente de X (heterogeneidade não correlacionada).
- S2+: z_m = z-score do % de Lula (válidos, 1º turno) do município **dentro da UF**, s=+1.
- S2−: idem, s=−1.
Y = multinomial(aptos_2, X_i·B_i)/aptos_2. Verdade nacional T[j,k] = Σ X_ij w_i B_i[j,k] / Σ X_ij w_i (w = aptos_1).
- Execução principal: semente 1001, γ=0,5, 10 réplicas por cenário, 2026 e 2022.
- Execução de sensibilidade: semente 2002, γ=1,0 (S1, S2±) e S0 de novo, 10 réplicas.
Unidade: γ é o deslocamento em log-odds por 1 DP de contexto; **não é calibrado à realidade**, é um estresse.

Métricas: erro (estimado − verdadeiro) nas células Abs→Lula, Abs→Adv, BN→Lula, e razão Abs→Lula : Abs→Adv; erro absoluto médio das 36 células; erro de reprodução do total nacional do 2º turno (para mostrar se o ajuste das margens discrimina cenários).

Critérios (fixados agora): *recuperação* em S0/S1 = erro absoluto ≤ 0,01 nas células Abs→Lula e Abs→Adv e erro relativo da razão ≤ 25%. *Robustez* em S2± = erro absoluto ≤ 0,03 nessas células e ordem Abs→Lula > Abs→Adv preservada quando verdadeira. Falhou o critério → interpretação "enfraquecida" para a magnitude, e a sensibilidade diz se a ordem sobrevive.

## P2 — poder da regra T13 nos dois sentidos (script `p2_poder_sentidos.py`)
Mecanismo: troca de votos em 1% das urnas sorteadas (o mesmo mecanismo do T13), 5% dos válidos da urna movidos (célula do T13 em que só o T1 detectou, 111 contra limiar 62).
Sentidos: A = Flávio→Lula (como no T13); B = Lula→Flávio (simétrico, mesma magnitude, limitado ao saldo da origem).
Regra: a do T13, copiada literalmente: limiares fixos do real não modificado (T1>62, T2>1,09 pp, T3>170, T4>3,5); detecta se **algum** dos quatro excede.
Mundo de referência legítimo: bootstrap paramétrico do 2º turno real (L2 ~ Binomial(V2, L2/V2) por seção), 30 réplicas; intervenção aplicada sobre **o mesmo** mundo (pareado). A referência "dados reais não modificados" não pode alarmar por construção (os limiares partem dela).
- Execução principal: semente 1001, 30 réplicas, 5% dos válidos.
- Sensibilidade: semente 2002, 30 réplicas, 2% e 10% dos válidos.
Resultado: taxa de detecção por sentido, por teste e conjunta, com IC de Wilson 95%; taxa de alarme na referência.
Critério: "resistiu" se a detecção conjunta de A e B difere por ≤ 15 pp e a referência alarma em ≤ 5% das réplicas. A detecção quantitativa só vale para esta combinação (mecanismo × magnitude × mundo).
Observação previa de leitura do código (antes de rodar): o T1 conta só z robusto > +5 (um lado) e o T3 só ≥90% para Lula; espera-se assimetria. Isso é hipótese a testar, não resultado.

---
## ADENDOS 1 e 2 (recebidos durante a sessão, antes das execuções que os afetam). Escopo vigente
- Investigação 1 = P1 (acima) + hipótese de manipulação sobre o crescimento de Lula entre turnos, 2022 e 2026 separados. Usa só resultados já existentes (T02, T03, T10, C06, C06b, E02) e a parte A do P1; nenhum teste novo além do P1 adversarial. Hipótese escolhida (fixada antes de olhar além do que o CONCLUSAO já mostra): **enchimento/transferência localizada de votos para Lula em seções, via eleitores ausentes** (mecanismo: voto extra usando abstenção). Previsões: seções com salto de comparecimento junto com virada acima da vizinhança; excesso unilateral de outliers T02; T3 (comparecimento ≥95% e ≥90% Lula); curva T10 desviando. Contrárias/alternativas: tamanho da seção, composição do eleitorado, efeito de mobilização (comparecimento sobe 2,96 mi em 2026).
- P2 (poder dos testes) **fica na fila futura**: o Adendo 2 substitui a segunda investigação. `p2_poder_sentidos.py` não será escrito/rodado.
- Investigação 2 = Adendo 2. Verificação A (até 20 seções do 1º turno 2026, pacotes brutos já baixados): 10 exceções + 10 aleatórias. **Seleção fixada agora:** das exceções do T36 (`resultado_casos_integridade_1t.json` → `casos_lista`), entram obrigatoriamente o caso "sem explicação" e o caso do tipo `d_fora_do_bu` se existir; as demais até 10 saem por `numpy.random.default_rng(2026).choice` sobre a lista ordenada por (UF, município, zona, seção) em texto; as 10 aleatórias saem de `default_rng(2027)` sobre o universo de urnas em `analise/brutos/1t` (excluídas as exceções). Verificações por seção: tamanho+SHA-512 de cada arquivo contra a lista assinada; assinatura da lista e dos arquivos; chave da seção dentro do BU e do log (UF/município/zona/seção, turno, pleito); RDV recontado = BU = imagem do BU; BU = BU na Web (`bweb_1t_*.csv`); emissor do certificado e se há cadeia até âncora (não há âncora local). Uma execução; sem validação extra a menos que haja falha técnica.
- Verificação B (confronto independente): inventário do que existe localmente (boletins impressos de terceiros, QR, capturas externas). Se nada existir, documentar e encerrar.

---
## FASE 2 COMPLETA (decisão do responsável em 28/10/2026: finalizar todas as perguntas). Pré-registro escrito antes das execuções
Script único `fase2/f2_completa.py <Pn>`, saída `fase2/resultados/<Pn>.json`. Critérios fixados agora:
- **P2** (T13 nos dois sentidos): como acima (1% das urnas, 5% dos válidos; 30 réplicas; semente 1001; sensibilidade 2% e 10% com semente 2002). Resistiu se detecção A e B diferem ≤ 15 pp e o mundo de referência alarma em ≤ 5% das réplicas.
- **P5** (T20 dentro de municípios com mais de um modelo): diferença média do resíduo da virada entre modelos, dentro do município, IC 95% por bootstrap de municípios (200). Equivalência declarada se o IC fica em ±0,02 logit.
- **P7** (T04 equivalência): diferença de z entre urnas trocadas e demais, IC 90% por bootstrap de municípios (200); equivalência se contida em ±0,10 z.
- **P8** (T03 por município): Spearman e IC 95% por bootstrap de municípios (200), postos fixos globais; desprezível se |r| ≤ 0,05.
- **P9** (E02): correlação intralocal ρ pelo ANOVA, razão de variância 1+(k−1)ρ aplicada ao z do grupo, BH 5% antes e depois, 2022 e 2026 com o mesmo modelo (simples e completo sem perfil). Moran's I só se houver adjacência municipal local; senão fica registrado como não feito.
- **P10** (T28 beta-binomial): prior beta por UF × modelo de urna (momentos, descontado o ruído binomial); preditiva beta-binomial para os últimos 30 min; BH 5%; comparar com as 13 urnas originais. Controle de horário: razão últimos 30 min / resto por grupo, apenas relatada.
- **P12** (exterior): cadastro de eleitores por seção (perfil, ZZ) × aptos do BU, seção a seção; soma das diferenças × −495/−525.
- **P13** (C06b): limites de Duncan-Davis por seção somados, variantes de população (aptos 1º turno, aptos 2º turno, com e sem exterior); registrar qual variante reproduz 79 e 123.
- **P14** (assimetria do T02): concentração por município e por local de votação das seções acima de 5 desvios contra sorteio aleatório dentro da UF (1.000 sorteios), 2022 e 2026.
- **P15** (limites Fréchet por seção para Abs→Lula e Abs→Adversário): soma, razão mínima e máxima, comparação com a estimativa do C06.
- **P16** (verificação de 200 seções sorteadas, semente 2028, comparador do RDV corrigido).
- **P17** (assimetria de cauda do T02, bootstrap por município, limiares 3, 4 e 5).
- **P11** (cadeia de certificados): validar a assinatura do certificado de cada urna da amostra do P16 pela chave da AC UE2020/UE2022 do repositório DataUrnas (terceiros); relatar como verificação de elo, não de raiz.
- **P3, P4, P6**: P3 = P16 (um canal) mais a limitação do canal único; P4 e P6 = inventário local (sem coleta).

**Registro de desvios (Fase 2 completa):** P16 repetido uma vez depois de corrigir o comparador (campo ausente contra zero); P12 refeito com o total oficial do site em vez do cadastro de julho; P2 usou intervalo de Wilson próprio. Nenhum critério de decisão foi alterado depois de ver os resultados.
