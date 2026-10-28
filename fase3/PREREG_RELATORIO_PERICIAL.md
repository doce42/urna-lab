# Pré-registro: "Relatório Pericial Independente" (rodada 8, ABERTA), 28/10/2026

Escrito antes de qualquer conta. **Origem (só pergunta, não fonte):** transcrição de 7 páginas de um relatório de 8 imagens divulgado por uma conta no X (a transcrição foi feita por terceiro; trechos ilegíveis ficaram marcados; as alegações **não foram verificadas** por quem transcreveu). A rodada 8 **permanece aberta**: nada é congelado sem aprovação explícita do responsável.

## Alegações testáveis com dados oficiais do TSE e como serão medidas
| # | Alegação do relatório | Medida (dados do TSE) |
|---|---|---|
| R1 | 499.205 seções e 128.236.074 votos apurados no 2º turno | contagem de seções e soma de comparecimento (válidos + brancos + nulos), com exterior |
| R2 | "Até as 17h00 (prazo legal)" Flávio venceu com 52,39% e quase 1,8 mi de frente; "após as 17h00 (prorrogação)" Lula teve mais de 6,1 mi de vantagem e virou o resultado | seções por `DT_ENCERRAMENTO_2` (hora **local**), cortes: ≤ 17:00:59, 17:01 a 17:15, 17:16 a 18:59, ≥ 19:00; também em hora de Brasília (fuso do município pela abertura às 8h); % do vencedor e vantagem por grupo; distribuição do horário de encerramento |
| R3 | Faixas: 17h01 a 17h15 com 339.593 seções, 88.071.750 eleitores, 53,46% Lula; 17h16 a 18h59 com 2.472 seções, 674.799 eleitores, 57,16%; após 19h com 6.333 seções, 1.856.306 eleitores | reproduzir (seções, comparecimento, % de Lula nos válidos) |
| R4 | Seções após 19h: BA 936 seções com 72,31%; PE 657 com 65,70%; MA 83,31%; SP 1.571 com 57,46%, "contrariando o restante do estado" | reproduzir; comparar cada seção tardia com as demais **do mesmo município** (diferença da proporção de Lula e da virada entre turnos), que é o que "contrariar o restante" exige |
| R5 | 8.632.488 eleitores liberados sem biometria (6,73% do comparecimento), "quase o dobro" da margem de 4.430.191 | reproduzir a soma de `QT_ELEI_BIOM_SEM_HABILITACAO_2`, a fração e a razão com a margem; **o mesmo em 2022 e no 1º turno de 2026** |
| R6 | Correlação positiva: quanto maior a liberação manual, mais Lula ("disparou em linha reta, picos de mais de 61%") | curva do % de Lula por faixa da taxa de liberação manual; correlação entre seções, entre municípios e **dentro do município**; mesma relação no 1º turno de 2026 e em 2022 (uma causa específica do 2º turno de 2026 não apareceria nos outros) |
| R7 | Seções com 100% dos válidos: 106 para Lula contra 4 para Flávio (26,5 : 1); mais de 90%: 6.899 contra 384 (18 : 1) | reproduzir; mesmo em 2022 (1º e 2º turnos) e no 1º turno de 2026; geografia (UF) e tamanho |
| R8 | Teste de Benford do primeiro dígito sobre 499.205 seções "detecta manipulação" | primeiro dígito dos votos por candidato e seção: desvio de Benford (MAD e qui-quadrado) em 2026 e 2022, **contra duas referências sem manipulação simuladas**: binomial e beta-binomial (ρ = 0,02) com os mesmos tamanhos e as participações municipais |
| R9 | Microdados "trancados em sigilo por quase três dias", liberados só na manhã de 28/10 | evidência de disponibilidade pública dos arquivos por urna na noite de 25/10 (primeira conferência de terceiros contra o TSE) e o que o projeto consegue ou não afirmar sobre o CSV BWeb |
| R10 | Decisão judicial de passaportes, prisão preventiva, Banco Master, reação internacional, mídia estatal chinesa, "fiscais partidários independentes", "baixíssima fiscalização", "zonas rurais" | **fora do escopo dos dados do TSE: não testadas e não afirmadas**, listadas como tal |

## Leitura pré-fixada
1. R2 e R3: se o grupo "após 17h00" incluir o horário de rotina de encerramento (17:01 a 17:15, que cobre a maior parte das seções), o corte não separa uma "prorrogação"; a prorrogação real é a que fecha depois de ~17:30 (T09, T52). Será dito qual é o tamanho de cada coisa em votos.
2. R4: "contrariar o restante" só vale se a diferença persistir **dentro do município**.
3. R5: a liberação sem biometria é medida contra o mesmo número em 2022 e no 1º turno; "maior que a margem" é uma comparação que só informa se a razão for incomum.
4. R6: uma correlação entre seções mistura geografia e idade (T12, T53); a leitura causal só vale se a relação for específica do 2º turno de 2026 e persistir dentro do município. Uma correlação que existe igual no 1º turno de 2026 e em 2022 não é efeito de um evento do 2º turno.
5. R7: razões de unanimidade são lidas contra 2022 e contra a geografia (T49: locais de uma seção só com participação quase nula).
6. R8: o primeiro dígito de contagens limitadas (≤ ~400 eleitores por seção) não segue Benford; o que importa é se o desvio observado cabe nas referências simuladas.
7. R9: o CSV de dados abertos não tem registro de primeira publicação neste projeto; o que se pode afirmar é a disponibilidade dos arquivos por urna, com a evidência de terceiros.
8. Nada aqui afirma nem nega fraude além do que os números sustentam.

**Orçamento:** 1 execução + 1 correção. Script `fase3/relatorio_pericial.py`; saída `fase3/resultados/relatorio_pericial.json`.

## Adendo (28/10/2026, escrito depois de ver o resultado do R2 e antes de rodar o R2b): R2b, exploratório
O R2 reproduziu os números do relatório (ver `resultados/relatorio_pericial.json`). A pergunta que sobra é se a divisão em dois grupos, no minuto 17:00, separa algo real. Medidas: **(a)** sensibilidade do corte: vantagem de Lula e % de Lula nos grupos antes e depois de cada corte (17:00:59, 17:01:59, 17:02:59, 17:05:59, 17:10:59, 17:15:59, 17:30:00, 19:00:00); **(b)** composição dos grupos "até 17:00:59" e "17:01 a 17:15": UFs e fuso; **(c)** a diferença do % de Lula entre os dois grupos **dentro do mesmo município** e dentro da mesma UF; **(d)** as seções com encerramento **antes** das 17:00:00 (quantas e com que taxa de comparecimento). Leitura: se a diferença some dentro do município, a divisão é composição geográfica e não uma "segunda eleição".
