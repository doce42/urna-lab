# 05. Zeros de votos e primeiro × segundo turno, 2022 e 2026

## A. Zeros e poucos votos (T64; scripts `zeros_contagens.py`, `zeros_locais.py`)
Seções com comparecimento positivo: 471.010 (2022) e 497.897 (2026), sem o exterior. "Direita" = Bolsonaro em 2022 e Flávio em 2026 (candidato do 2º colocado no 2º turno).

| Ano, turno, finalista | 0 votos | 1 | 2 | 3 a 5 |
|---|---|---|---|---|
| 2022, 1º turno, Lula | 1 | 3 | 5 | 33 |
| 2022, 1º turno, Bolsonaro | 160 | 255 | 326 | 1.323 |
| 2022, 2º turno, Lula | 2 | 3 | 3 | 28 |
| 2022, 2º turno, Bolsonaro | 141 | 207 | 264 | 967 |
| 2026, 1º turno, Lula | 8 | 3 | 16 | 62 |
| 2026, 1º turno, Flávio | 79 | 129 | 150 | 705 |
| 2026, 2º turno, Lula | 4 | 6 | 3 | 50 |
| 2026, 2º turno, Flávio | 106 | 123 | 162 | 759 |

As dez perguntas:
1. **Seções com zero para cada finalista:** tabela acima. O candidato da direita tem de 79 a 160 seções zeradas por turno; Lula, de 1 a 8.
2. **Com comparecimento positivo:** todas as contadas têm; o universo está na primeira linha desta seção.
3. **Um, dois e de três a cinco votos:** tabela acima.
4. **Mudança entre turnos:** das 106 seções com zero para Flávio no 2º turno, **50** também tinham zero no 1º; das 141 com zero para Bolsonaro em 2022, **84**. Os votos de Lula nessas seções somam 14.860 (2026) e 16.418 (2022). Das 4 seções de Lula com zero em 2026, as 4 já tinham zero no 1º turno.
5. **Verificadas por BU e RDV:** as 106 de 2026 (T49: 106 de 106 com assinaturas válidas e BU = RDV = tabela) e, nas 486 seções-turno de 2022 e 2026 com zero para um finalista, **0 divergência** de votos entre boletim, RDV, imagem e tabela (E3, Q20).
6. **Distribuição por município, zona e local:** os zeros são seções isoladas. Em 2026, 106 seções em 98 locais de votação; em 2022, 141 em 136. **84 de 106 (2026) e 121 de 141 (2022) estão em locais onde todas as seções são zero (locais de uma seção só), e 104 de 106 e 131 de 141 estão em locais onde o candidato tem menos de 1% do total.** Mediana de votos válidos da seção zerada: 124,5 (2026) e 92 (2022), contra 254 e 257 nas demais; 42 (2026) e 78 (2022) têm menos de 100 votos válidos. Descritivo exploratório, feito depois de ver os modelos.
7. **O padrão continua atípico depois de controles?** **Não determinado.** Ver o item 10.
8. **Há fenômeno equivalente em 2022?** Sim, maior: 141 seções zeradas contra 106, com o mesmo perfil (comunidades pequenas e isoladas, sobretudo no Norte e no Nordeste; MA tem 47 e AM 23 em 2022).
9. **Diferenças entre candidatos:** 106 contra 4 em 2026 e 141 contra 2 em 2022. É assimetria forte entre os dois, e igual nos dois anos. Os dados não distinguem se vem de geografia (comunidades onde o candidato da direita não tem voto) ou de outra causa; a descrição das seções (item 6) é compatível com a primeira.
10. **O modelo de cauda baixa foi calibrado?** **Não.** Três famílias, critério fixado antes (observado dentro do intervalo de predição de 95% em pelo menos 80% das UFs com esperado ≥ 1, validação por UF retida):

| Família (onde se estima a participação esperada) | Esperado × observado, 2022 Bolsonaro | Esperado × observado, 2026 Flávio | Critério |
|---|---|---|---|
| Município (beta-binomial, sobredispersão ρ ≈ 0,02) | 4,3 × 141 | 1,3 × 106 | falha (2022: 0 de 2 UFs; 2026: nenhuma UF com esperado ≥ 1) |
| Zona | 2,9 × 141 | 0,9 × 106 | não aplicável (nenhuma UF com esperado ≥ 1) |
| Local de votação (ρ ≈ 0,005) | 63,3 × 141 (7 de 14 UFs dentro) | 66,7 × 106 (9 de 12 dentro) | falha (50% e 75% contra 80%) |

Conclusão: nenhum modelo chega perto dos zeros observados no nível de município ou de zona, e o modelo por local explica cerca de 45% a 63% e também falha. **Não se declara nem excesso nem ausência de excesso de zeros.** A descrição é que são locais de uma só seção com participação quase nula, nos dois anos.

**Impacto em votos:** os votos do candidato de quem seria o zero somam, no máximo, os 14.860 votos de Lula nas 106 seções (0,34% da margem de 4.430.191); em 2022, 16.418 (0,77% da margem de 2.139.645). Não é limite superior para alteração indetectável, é a escala do fenômeno observado.

## B. Primeiro × segundo turno
**Mudança de totais observada** (contas exatas; Q21 a Q23):

| | 1º turno | 2º turno | Variação |
|---|---|---|---|
| 2022, Lula | 57.259.504 | 60.345.999 | +3.086.495 |
| 2022, Bolsonaro | 51.072.345 | 58.206.354 | +7.134.009 |
| 2026, Lula | 53.879.538 | 64.256.232 | +10.376.694 |
| 2026, Flávio | 56.104.503 | 59.826.041 | +3.721.538 |

Brancos e nulos: 5.452.653 → 5.700.443 (2022) e 5.969.801 → 4.153.801 (2026, queda de 1,82 mi). Identidade contábil exata (Q22): 2022, 10.220.504 = 9.897.870 (eliminados) + 570.424 (comparecimento) − 247.790 (brancos e nulos); 2026, 14.098.232 = 9.321.993 + 2.960.239 + 1.816.000. **Nenhuma diferença irreconciliável** com os totais oficiais (Q23: 0 seção com mais votos que comparecimento; 638 de 638 itens iguais).

**Crescimento excepcional (T51, T55, T44):** o candidato que avança no 2º turno cresce mais que o rival em quase todos os municípios nos dois anos (Lula em 93,8% em 2026; Bolsonaro em 87,1% em 2022); em proporção, 98,0% (2022) e 97,1% (2026). Municípios onde o rival fortemente derrotado leva ≥ 90% do ganho: 36 (Lula, 2026) e 28 (Bolsonaro, 2022). Cabo Frio (Lula +9.169, Flávio +342) cabe nos 9.511 votos disponíveis; nenhum município do país ganha mais que o disponível. Salvador: ~30 mil votos de Lula acima do previsto (T44), em todas as zonas, sem causa demonstrada.

**Transferência individual inferida (não observada):**
- Limites formais (Q24): trocas diretas entre finalistas com mínimo garantido de 79 (Flávio → Lula) e 123 (Lula → Flávio) votos e máximos de 43,5 mi e 39,4 mi; abstencionistas para Lula entre 4.116 e 32,3 mi (Fréchet). **A identificação individual não é possível com dado agregado e voto secreto (Q26).**
- O estimador C06 (Goodman restrito) dá direção mas não magnitude confiável: com origem conhecida (nulos que digitaram o número de um candidato eliminado), atribui 90% ao Renan (número 14) e 69% ao Cury (70), mas acerta só 20% no Caiado (55) e 9% e 13% em 2022 (Ciro e Tebet) (T59). **Os números de fluxo valem como direção, não como tamanho.**
- Brancos e nulos: a queda de 1,82 mi tem causa estrutural medida (T56 a T58): erro de campo com número de governador no campo de presidente (698 mil no 1º turno de 2026 contra 422 mil em 2022) e haver menos 2º turno de governador em 2026 (8% dos votos contra 53% em 2022); o resíduo é uniforme (~0,6 ponto).

**Conclusão:** a variação entre turnos fecha como identidade contábil; fluxos individuais não são identificáveis; as proporções observadas de crescimento têm precedente em 2022 no sentido oposto; o que fica sem causa são Salvador (T44) e a zona 251 de SP em 2022 (Q25).
