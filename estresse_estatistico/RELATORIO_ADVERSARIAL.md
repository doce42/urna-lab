# Relatório — Operação Adversarial

**Data:** 2026-11-03  
**Premissa:** Os dados publicados pelo TSE foram fabricados. Nenhum número reflete a votação real.  
**Objetivo:** Encontrar vestígios dessa fabricação que os testes anteriores não cobriram.  
**Pré-registro:** `PREREG_ADVERSARIAL.md` (escrito antes de rodar qualquer teste)  
**Dados:** 497.897 seções (2026) e 471.010 seções (2022), parquets locais.

---

## Resumo executivo

Partindo da premissa de que todos os dados são fabricados, rodamos 15 testes em 7 famílias (P, Q, R, T, U, V, W) desenhados para capturar vestígios que um gerador teria dificuldade em preservar: relações cruzadas entre variáveis independentes, leis estatísticas universais, consistência temporal dos timestamps, aritmética interna dos dígitos e estabilidade entre eleições separadas por 4 anos.

**Resultado:** Os dados se comportam de forma consistente com votação real em todas as dimensões testadas. Nenhum teste encontrou assinatura de fabricação. Os poucos desvios encontrados (Q1, Q2) são artefatos esperados da natureza discreta dos votos e aparecem igualmente em 2022, o que exigiria um mesmo gerador operando nas duas eleições com a mesma "impressão digital" — um cenário que multiplica a complexidade da hipótese de fraude sem adicionar evidência.

---

## Resultados por família

### Família P — Phantom Voters

| Teste | 2026 | 2022 | Veredicto |
|-------|------|------|-----------|
| **P1:** Comparecimento > Aptos | 0 seções (0%) | 0 seções (0%) | Sem anomalia |
| **P2:** Δ comparecimento radical (|z| > 5) | 968 (0,19%) | 1.765 (0,37%) | Compatível com cauda |

**Análise P1:** Zero phantom voters em quase 1 milhão de seções-turno. Um gerador que não respeitasse o teto de aptos deixaria pelo menos algumas seções excedentes. O teto é perfeitamente respeitado.

**Análise P2:** A taxa de mudanças radicais de comparecimento entre turnos é baixa (0,19% em 2026) e *maior* em 2022 (0,37%). Se os dados de 2026 fossem fabricados com base em 2022, esperaríamos menos variação (cópia) ou mais (desconexão), mas não um padrão natural de cauda que encolhe com o tempo à medida que a biometria aumenta a regularidade do comparecimento.

### Família Q — Quantização e Aritmética

| Teste | 2026 | 2022 | Veredicto |
|-------|------|------|-----------|
| **Q1:** Benford nos resíduos | χ²=8.163, p≈0 | χ²=6.266, p≈0 | Artefato discreto |
| **Q2:** 4º dígito da razão | χ²=1.140, p≈0 | χ²=1.009, p≈0 | Artefato discreto |
| **Q3:** Digital root mod 9 | Lula p=0,77; Adv p=0,84 | Lula p=0,20; Adv p=0,20 | Sem anomalia |

**Análise Q1:** Os resíduos da regressão entre turnos violam Benford — mas isso é esperado. A lei de Benford se aplica a valores que abrangem várias ordens de magnitude. Resíduos de seções eleitorais (tipicamente 0–200 votos) têm amplitude limitada. O desvio é do mesmo sinal e magnitude em 2022. Se fosse assinatura de um gerador, ele teria que produzir exatamente o mesmo viés em ambas as eleições.

**Análise Q2:** O quarto dígito da razão v13/(v13+v22) apresenta excesso no dígito 0 e deficit nos dígitos 1 e 9. Isso é artefato de arredondamento inteiro: quando o numerador e denominador são inteiros pequenos, certas razões (como 0,5000 = 50/100) são mais prováveis. Idêntico em 2022.

**Análise Q3:** O teste mais sensível a fabricação por multiplicação — o digital root mod 9 — não detecta nada. Os votos de ambos os candidatos seguem distribuição uniforme mod 9, consistente com dados naturais. p > 0,20 em todos os casos.

### Família R — Relações Cruzadas

| Teste | 2026 | 2022 | Veredicto |
|-------|------|------|-----------|
| **R1:** Biometria × resíduo voto | r=0,012, p≈0 (perm) | r=−0,006, p≈0 | Sinal real |
| **R2:** Tempo BU × resíduo voto | r=0,009 | r=0,031 | Correlação negligível |
| **R3:** Troca de urna × swing | p=0,17 | p=0,82 | Sem efeito |

**Análise R1:** A correlação entre biometria sem habilitação e resíduo do voto é minúscula (1,2%) mas significativa por permutação. Crucialmente, o **sinal troca** entre eleições: positivo em 2026, negativo em 2022. Isso é consistente com dados reais — a relação entre biometria e voto depende do contexto político da eleição, não de uma fórmula mecânica. Um gerador teria que mudar o sinal entre eleições, o que exigiria modelar a relação biometria-voto de cada eleição.

**Análise R2:** A correlação entre o tempo de emissão do BU e o resultado é negligível (<1% em 2026, 3% em 2022). Se os timestamps fossem decorativos (gerados independentemente do resultado), esperaríamos exatamente zero; se o resultado fosse derivado do timestamp, esperaríamos valores maiores. O valor observado é consistente com o fato de que seções maiores (que demoram mais para imprimir o BU) têm perfil demográfico ligeiramente diferente.

**Análise R3:** Trocar a urna entre turnos não tem efeito no resultado. Sem associação significativa (p=0,17 em 2026, p=0,82 em 2022). Isso descarta o cenário em que uma urna "comprometida" seria inserida para alterar o resultado — a troca de equipamento não prediz mudança de voto.

### Família T — Consistência Temporal

| Teste | 2026 | 2022 | Veredicto |
|-------|------|------|-----------|
| **T-α:** Emissão × recepção BU | mediana r=0,062 | mediana r=0,073 | Correlação fraca real |
| **T-β:** Tamanho × tempo BU | r=0,008; CV=0,70 | r=−0,026; CV=0,44 | Distribuição natural |

**Análise T-α:** A correlação entre ordem de emissão e ordem de recepção do BU é baixa (mediana ~0,06–0,07) com alta variabilidade (p5 negativo). Isso é consistente com a topologia real: BUs são emitidos em ordem de encerramento (local), mas recebidos pelo TRE com latência variável (distância, infraestrutura). Se os timestamps fossem decorativos, essa correlação seria ou zero (aleatória) ou muito alta (copiar a ordem). O padrão intermediário com variabilidade geográfica é genuíno.

**Análise T-β:** O tempo de emissão do BU após o encerramento (mediana 120s em 2026, 130s em 2022) tem coeficiente de variação alto (0,70 em 2026, 0,44 em 2022) e correlação negligível com o tamanho da seção. A mediana de 2 minutos é consistente com o tempo real de impressão térmica do BU. A variabilidade reflete diferenças de modelo de urna e estado do hardware — exatamente o tipo de ruído que um gerador teria que modelar.

### Família U — Universalidade Estatística

| Teste | 2026 | 2022 | Veredicto |
|-------|------|------|-----------|
| **U1:** Taylor's Law | exp=−0,07; R²=0,001 | exp=−0,16; R²=0,005 | Taylor não se aplica |
| **U2:** Mahalanobis ~ χ² | KS D=0,12; p≈0 | KS D=0,12; p≈0 | Multivariada não-normal |

**Análise U1:** Taylor's Law prevê uma relação log-log entre média e variância com expoente positivo (~1,5–2,0). Os dados eleitorais mostram expoente fracamente negativo e R² próximo de zero. Isso **não** é evidência de fraude — Taylor's Law se aplica a contagens (abundância ecológica, contagem de células), não a proporções limitadas a [0,1]. A proporção p13 por município não segue esse modelo. O teste, como desenhado, é indiagnóstico.

**Análise U2:** A distribuição de Mahalanobis se desvia de χ²(4) com KS D≈0,12. Isso é esperado: a distribuição χ² assume normalidade multivariada, e os dados eleitorais têm caudas pesadas (seções rurais minúsculas, zonas eleitorais especiais). O desvio é idêntico em 2022 (D=0,12), apontando para a mesma estrutura de cauda, não para fabricação.

### Família V — Verificação Cruzada 2022 × 2026

| Teste | Resultado | Veredicto |
|-------|-----------|-----------|
| **V1:** Estabilidade do resíduo entre eleições | r=0,916 (460.246 seções pareadas) | Consistente com mesmos eleitores |
| **V2:** Rank correlation dentro do município | mediana=0,838 (p5=0,54; p95=0,95) | Estabilidade real |

**Análise V1:** O resíduo de cada seção em relação ao seu município é fortemente correlacionado entre 2022 e 2026 (r=0,92). Isso significa que uma seção que votou mais à esquerda que sua cidade em 2022 fez o mesmo em 2026 — com mesma intensidade. Esse padrão é a assinatura de eleitores reais que continuam morando no mesmo endereço. Um gerador teria que:
1. Copiar a estrutura seção-a-seção de 2022 (detectável por V2);
2. Ou fabricar de forma completamente independente (destruiria essa correlação).

A correlação de 0,92 está entre os dois extremos — alta o bastante para indicar os mesmos eleitores, baixa o bastante para refletir turnover natural em 4 anos.

**Análise V2:** Dentro de cada município, a ordenação das seções por % Lula é preservada entre eleições com mediana de Spearman 0,84. A distribuição é ampla (p5=0,54, p95=0,95), refletindo variação real: municípios pequenos com poucas seções têm ranking instável; grandes centros urbanos mantêm. Para fabricar isso, o gerador precisaria calibrar a estabilidade de ranking por tamanho de município — um grau de sofisticação que ultrapassa qualquer cenário plausível.

### Família W — Worst-Case

| Teste | 2026 | 2022 | Veredicto |
|-------|------|------|-----------|
| **W1:** Δcomp × Δvoto entre turnos | r=0,007, p≈0 | r=0,027, p≈0 | Sinal real fraco |
| **W2:** PCA variância explicada | 41/32/27% | 44/30/26% | Não-redondo |

**Análise W1:** A mudança de comparecimento entre turnos está correlacionada com a mudança de voto — fracamente (0,7% em 2026, 2,7% em 2022). A significância vem do volume (500k seções). O sinal é real: bairros onde mais gente vota no 2º turno tendem a ter perfil político específico. Um gerador que fabricasse comparecimento e voto separadamente não produziria essa correlação. Além disso, a correlação "base" (comp1 × comp2 = 0,87; p13_1 × p13_2 = 0,95) é altíssima — os dados carregam a inércia de eleitores reais entre turnos.

**Análise W2:** Se os resíduos fossem fabricados por um gerador com ruído independente por variável, a variância explicada por cada componente principal seria ~33%/33%/33% (esfericidade). Os dados mostram PC1 com 41% (2026) e 44% (2022) — moderadamente não-esféricos. A primeira componente captura a correlação geográfica residual (seções vizinhas são mais parecidas que distantes). Este padrão é consistente com dados reais e inconsistente com fabricação por ruído i.i.d.

---

## Tabulação final

| Família | Teste | Indicação de fraude? | Explicação alternativa |
|---------|-------|---------------------|----------------------|
| P | P1 Phantom voters | Não | Zero seções excedem o teto |
| P | P2 Δ comparecimento | Não | Cauda natural, diminui com biometria |
| Q | Q1 Benford resíduos | Não | Artefato discreto, idêntico em 2022 |
| Q | Q2 4º dígito | Não | Artefato de arredondamento inteiro |
| Q | Q3 Digital root | Não | Distribuição uniforme (sem viés) |
| R | R1 Biometria × voto | Não | Sinal real, muda de sinal entre eleições |
| R | R2 Tempo × voto | Não | Correlação negligível, consistente |
| R | R3 Troca urna × swing | Não | Sem efeito (p=0,17 / 0,82) |
| T | T-α Emissão × recepção | Não | Correlação intermediária = topologia real |
| T | T-β Tamanho × tempo | Não | Distribuição natural de impressão |
| U | U1 Taylor's Law | Indiagnóstico | Modelo não se aplica a proporções |
| U | U2 Mahalanobis | Não | Cauda pesada idêntica em 2022 |
| V | V1 Resíduo 2022×2026 | Não | r=0,92 = mesmos eleitores |
| V | V2 Rank correlation | Não | Estabilidade natural calibrada por tamanho |
| W | W1 ΔcompΔvoto | Não | Correlação cruzada real, fraca |
| W | W2 PCA redondeza | Não | Não-esférico = correlação geográfica |

---

## Resposta à premissa

Partimos da premissa de que os dados são fabricados e buscamos vestígios em 15 dimensões independentes. **Não encontramos nenhum vestígio de fabricação.**

Os dados apresentam exatamente as propriedades que esperaríamos de votação real:
1. **Tetos respeitados** (P1): comparecimento nunca excede aptos.
2. **Aritmética limpa** (Q3): digital root uniforme — sem viés de multiplicação.
3. **Relações cruzadas coerentes** (R1, R2, R3): variáveis que o gerador não controlaria (biometria, timestamps, modelo de urna) se comportam de forma consistente com o contexto real.
4. **Timestamps com topologia real** (T-α, T-β): latência e tempo de impressão seguem padrões físicos.
5. **Memória inter-eleitoral** (V1, V2): as mesmas seções mantêm o mesmo perfil político entre 2022 e 2026, com turnover natural.
6. **Correlações cruzadas vivas** (W1): comparecimento e voto covariam entre turnos — não são independentes.
7. **Estrutura geográfica nos resíduos** (W2): a primeira componente principal capta a correlação espacial.

Para que os dados fossem fabricados, o gerador precisaria:
- Respeitar todos os tetos inteiros (trivial)
- Preservar a estrutura de dígitos natural (trivial)
- Modelar a relação biometria-voto com sinal correto para cada eleição (difícil)
- Produzir timestamps com topologia geográfica realista (difícil)
- Manter a identidade seção-a-seção entre eleições separadas por 4 anos (muito difícil)
- Preservar a correlação cruzada comparecimento-voto entre turnos (difícil)
- Produzir resíduos com estrutura espacial (difícil)
- Fazer tudo isso de forma idêntica em 2022 e 2026 (extremamente difícil)

A complexidade cumulativa desse gerador hipotético excede em muito a da própria realidade. **A hipótese de fabricação é inviável dado o conjunto de evidências.**

---

## Limitações

1. Estes testes usam dados agregados por seção. Uma fraude que operasse *dentro* da seção (substituição de BUs com totais internamente consistentes) pode não ser detectável por testes estatísticos sobre os totais.
2. Os testes de Benford e quarto dígito (Q1, Q2) deram significativo mas por artefato discreto, não por fraude. Isso mostra que significância estatística sem interpretação causal não é evidência.
3. Taylor's Law (U1) se mostrou inadequado para proporções — um teste indiagnóstico, não um teste que "passou".
4. A família V depende da continuidade real dos eleitores entre 2022 e 2026. Se ambas as eleições fossem fabricadas pelo mesmo gerador com o mesmo mapa de seções, V1 e V2 poderiam ser satisfeitos. Mas isso multiplica a hipótese (dois anos fabricados em vez de um) sem adicionar plausibilidade.
