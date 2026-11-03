# Pré-registro — Operação Adversarial: Assumindo Fraude

**Data:** 2026-11-03T02:00-03:00 (antes de rodar qualquer teste).  
**Premissa:** Os dados publicados pelo TSE NÃO refletem a votação real. Algum mecanismo alterou os números entre a urna e a publicação.  
**Objetivo:** Encontrar vestígios dessa alteração que os testes anteriores (Estresse Estatístico, bateria T01-T71) não conseguiram detectar.

## Filosofia

Os testes anteriores usaram modelos nulos baseados em comportamento eleitoral natural (H0/H7). Se os dados foram fabricados por um gerador sofisticado, eles passam nesses testes por construção — o gerador imita o comportamento natural. 

Esta operação inverte a lógica: parte da premissa de fraude e busca inconsistências que um gerador teria dificuldade em preservar, especialmente:

1. **Relações entre variáveis que o fraudador não controlou** (ex: biometria vs voto, timestamp vs voto, modelo de urna vs voto)
2. **Leis estatísticas difíceis de imitar** (ex: lei de Newcomb-Benford em combinações não óbvias, momentos de ordem alta, distribuição conjunta multivariada)
3. **Anomalias entre-eleições que exigiriam coordenação temporal** (ex: mesma seção em 2022 e 2026 com padrões que não poderiam coexistir naturalmente)
4. **Assinaturas do próprio mecanismo de fabricação** (ex: correlações entre timestamps e resultado, dependência entre "ruído" de diferentes seções)

## Famílias de testes

### Família P — Phantom voters (comparecimento impossível)
- **P1:** Seções onde o comparecimento do 2t > aptos do 2t (phantom voters). Em dados fabricados, o gerador pode não respeitar o teto.
- **P2:** Seções onde |comparecimento_2t − comparecimento_1t| > X% dos aptos, com X calibrado por município. Mudanças radicais de comparecimento entre turnos na mesma seção são difíceis de fabricar com consistência.

### Família Q — Quantização e aritmética interna
- **Q1:** Benford generalizado nos RESÍDUOS (v13_2 − E[v13_2|v13_1, tamanho]), não nos valores brutos. Se um gerador usa uma fórmula linear, os resíduos têm distribuição de dígitos diferente da natural.
- **Q2:** Teste de Kuiper nos dígitos da razão v13/(v13+v22) discretizada a 4 casas. Se o gerador arredonda, a distribuição do quarto dígito é não-uniforme.
- **Q3:** Soma de dígitos (digital root) de v13 e v22: se o gerador usa multiplicação por proporção, o digital root tem viés mod 9.

### Família R — Relações cruzadas não-triviais
- **R1:** Correlação entre QT_ELEI_BIOM_SEM_HABILITACAO (eleitores sem biometria) e o resíduo do voto. Um gerador que não considere a biometria deixa essa variável independente do resultado; no mundo real, regiões com menos biometria têm perfil socioeconômico específico.
- **R2:** Diferença entre DT_ENCERRAMENTO e DT_EMISSAO_BU × resultado. Se os dados são fabricados, o timestamp é decorativo — a correlação com a "rapidez" do encerramento será mais fraca que a natural.
- **R3:** Variação do resultado por modelo de urna (DS_TIPO_URNA) dentro do mesmo local/zona, controlando por tamanho. Se a urna foi substituída entre turnos (NR_URNA_EFETIVADA diferente), há correlação com mudança de resultado?

### Família T — Testes de consistência temporal
- **T-alpha:** Ordem de emissão do BU (DT_EMISSAO_BU) vs ordem de recebimento (DT_BU_RECEBIDO) dentro do município. Se os dados são gerados, a latência (recebido − emitido) é decorativa e pode não respeitar a topologia real (seções mais distantes devem demorar mais).
- **T-beta:** Intervalo entre DT_ENCERRAMENTO e DT_EMISSAO_BU. No real, é o tempo de impressão do BU. Se fabricado, pode ter distribuição irreal (muito uniforme, muito concentrada, ou não correlacionada com o tamanho da seção).

### Família U — Universalidade estatística
- **U1:** Teste de Taylor's Law (lei de potência entre média e variância por grupo). Dados eleitorais reais seguem Taylor's Law com expoente ~1.5-2.0. Dados fabricados por proporção fixa violam essa lei.
- **U2:** Distribuição de distâncias de Mahalanobis no espaço multivariado (v13, comparecimento, biometria, tamanho). Dados reais seguem chi-quadrado; dados fabricados com variáveis independentes não.

### Família V — Verificação cruzada temporal (2022 × 2026)
- **V1:** Estabilidade do resíduo por seção entre 2022 e 2026. No real, o resíduo (desvio da seção em relação ao município) é correlacionado entre eleições porque os eleitores são os mesmos. Se os dados de um ano foram fabricados, essa correlação é mais fraca ou mais forte que o esperado.
- **V2:** Ranktest: dentro de cada município, a ordenação das seções por % Lula em 2022 deve se correlacionar com a de 2026. Se fabricado, o ranking é preservado demais (copiado) ou destruído demais (aleatório).

### Família W — Worst-case: o que o melhor gerador não consegue fazer
- **W1:** Teste de independência condicional: dado o município, o par (comparecimento_1t, v13_1t) deve prever (comparecimento_2t, v13_2t) com erro correlacionado entre as duas dimensões. Um gerador que fabrica comparecimento e voto separadamente quebra essa correlação.
- **W2:** Análise de componentes principais dos resíduos por UF. Se os dados são reais, as primeiras componentes capturam geografia e demografia. Se fabricados, os resíduos são mais "redondos" (variância explicada mais distribuída).

## Critérios

- α = 0.01 por teste individual
- Cada teste roda em 2022 e 2026
- Referência: permutação ou simulação (não distribuição teórica)
- Resultado em magnitude (votos), não só p-valor
- Semente: 42

## Limites

- Máximo 2 testes por família
- Dados locais existentes
- Sem subagentes em cascata
- Sem variantes por não-significância
