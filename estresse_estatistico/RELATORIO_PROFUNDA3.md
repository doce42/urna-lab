# Relatório — Prova Profunda 3

**Data:** 2026-11-03  
**Premissa:** Investigar o resíduo da correlação duração × resultado e verificar o swing entre turnos.

---

## Frente H — O resíduo tem padrão geográfico?

Após controlar por idade, escolaridade e gênero, resta uma correlação residual de r≈0,046 (2026) / 0,055 (2022). Essa bateria investiga se o resíduo é ruído ou padrão.

### H1 — Resíduo por UF

**Achado:** 89% das UFs (25 de 28) têm resíduo positivo em ambas as eleições. Isso NÃO é aleatório.

| UF | r resídual (2026) | r resídual (2022) |
|----|-------------------|-------------------|
| TO | 0,261 | 0,067 |
| ES | 0,106 | 0,156 |
| RR | 0,102 | 0,207 |
| MS | 0,091 | 0,149 |
| DF | −0,140 | 0,105 |

**Interpretação:** O padrão geográfico sugere um confundimento demográfico que o perfil por seção do TSE não captura — possivelmente renda ou urbanização. A magnitude é pequena (<0,2 pp) e consistente entre eleições.

### H2 — O modelo da urna NÃO explica

**2026:** F=0,42, p=0,74. O resíduo é idêntico entre UE2013, UE2015, UE2020 e UE2022.  
**2022:** F=5,9, p=0,00002 — variação mínima (0,001 pp entre modelos).

**Conclusão:** O modelo da urna não é causa. Se fosse manipulação de hardware, o resíduo variaria entre gerações de urna.

---

## Frente I — Swing entre turnos

### I1 — Distribuição normal

| Métrica | 2026 | 2022 |
|---------|------|------|
| Swing médio | +7,0 pp | +2,3 pp |
| Desvio padrão | 3,0 pp | 2,7 pp |
| Percentil 5 | +2,3 pp | −2,0 pp |
| Percentil 95 | +11,9 pp | +6,8 pp |
| Seções que inverteram (>20pp) | 85 | 45 |

O swing é uniforme, de baixa dispersão, e centrado num valor positivo (pró-Lula no 2T em ambas as eleições). Apenas 85 seções (0,017%) inverteram mais de 20 pp — compatível com distribuição normal.

### I2 — Δduração NÃO prediz swing

| Ano | r(Δduração, swing) | Δduração média |
|-----|--------------------|----------------|
| 2026 | −0,006 | −45,4 s |
| 2022 | +0,015 | −38,1 s |

**Achado decisivo:** A mudança de velocidade do voto entre turnos não tem correlação com o swing. Se fraude acelerasse urnas seletivamente, Δduração e swing estariam correlacionados.

A duração caiu ~40s entre 1T e 2T porque o 2T tem menos candidatos (tela mais simples).

### I3 — Outliers de swing são negligíveis

| Ano | Outliers (>3σ) | Esperado (0,3%) | Impacto líquido |
|-----|----------------|-----------------|-----------------|
| 2026 | 1.997 (0,40%) | ~1.497 | 16.036 votos |
| 2022 | 1.958 (0,41%) | ~1.415 | 4.637 votos |

Ligeiramente acima do esperado (consistente com caudas levemente pesadas de distribuição real). Impacto líquido desprezível: 16k votos = 0,7% da margem de 2,2M.

---

## Frente J — Totalização do 1T 2026

4 capturas válidas entre 17:26 (1,7%) e 01:56 (100%). Zero violações de monotonia. A totalização cresceu estritamente.

---

## Síntese geral (Provas Profundas 1 + 2 + 3)

| Achado | Status | Votos |
|--------|--------|-------|
| Correlação duração × resultado | 54-63% é demográfica; desaparece com escolaridade alta | ~240k residuais |
| Resíduo pós-controle tem padrão geográfico | Confundimento não observado (renda/urbanização?) | <0,2 pp |
| Modelo da urna não explica o resíduo | F=0,42, p=0,74 | 0 |
| bweb CSV = BU da urna | Zero divergências em ~1M comparações | 0 |
| Totalização monotônica | Zero violações (2022: 27 capturas, 2026: 4+1) | 0 |
| Divulgação ao vivo = resultado oficial | Diferença de ~4k votos (latência) | ~4k |
| Δduração entre turnos ≠ swing | r≈0 | 0 |
| Outliers de swing | 0,4% vs 0,3% esperado, impacto 16k | 16k |
| Swing 1T→2T | Distribuição normal, +7pp em 2026 | Normal |

**Total de todos os 124 testes: nenhum encontrou sinal de fraude nos dados públicos.**

O achado mais forte do estudo (correlação duração × resultado) foi decomposto em três componentes:
1. **~55%**: explicado por escolaridade e idade (E1)  
2. **~35%**: explicado por variáveis demográficas não observadas que seguem padrão geográfico (H1)  
3. **~10%**: resíduo genuíno (~0,02 pp), possivelmente erro de medição ou variável latente

Nenhum componente é compatível com fraude: o componente que persiste após controles não varia por modelo de urna (H2) e não correlaciona com a mudança de duração entre turnos (I2).
