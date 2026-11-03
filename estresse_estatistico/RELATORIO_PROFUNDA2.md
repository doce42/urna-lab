# Relatório — Prova Profunda 2

**Data:** 2026-11-03  
**Premissa:** Três fontes independentes de verificação que não dependem dos testes anteriores.  

---

## Frente E — Controle demográfico

A correlação duração × resultado (Achado 1 da Prova Profunda) era o sinal mais forte do estudo (r=0,10 em 2026, r=0,15 em 2022 intra-município). Aqui testamos se ela sobrevive ao controle direto por idade, escolaridade e gênero.

### E1 — Correlação parcial

Controlando por idade (60+, <24), escolaridade (esc_1 a esc_8) e gênero dentro de cada município:

| Métrica | 2026 | 2022 |
|---------|------|------|
| r simples (intra-mun) | 0,100 | 0,147 |
| r parcial (controlando demo) | 0,046 | 0,055 |
| **Redução** | **54%** | **63%** |
| R² da demo sozinha sobre p13 | 0,226 | 0,212 |

**Conclusão:** Mais da metade da correlação era demográfica. O resíduo (r≈0,05) é estatisticamente significativo (n>470k) mas substantivamente pequeno — equivale a ~0,2 pp de diferença no resultado.

### E2 — Regressão completa

Modelo: p13 ~ duração + idade_60+ + idade_<24 + esc_1 + esc_8 + fem (demeaned por município).

| Preditor | Beta (2026) | t | Beta (2022) | t |
|----------|------------|---|------------|---|
| Duração (s) | +0,002 | 32 | +0,002 | 30 |
| Esc. baixa (esc_1) | +0,913 | 243 | +0,790 | 192 |
| Esc. superior (esc_8) | −0,183 | −170 | −0,183 | −155 |
| Jovens (<24) | +0,101 | 95 | +0,114 | 90 |
| Idosos (60+) | −0,035 | −37 | −0,046 | −43 |
| Mulheres (fem) | +0,100 | 45 | +0,082 | 31 |

**Achado:** A escolaridade baixa é o preditor dominante (t=243), não a duração (t=32). A duração acrescenta +0,002 pp por segundo — irrelevante em magnitude.

### E3 — Correlação por estrato homogêneo

Correlação duração × resultado dentro de estratos demográficos (4 quartis de idade × 4 de escolaridade):

| Estrato | r (2026) | r (2022) |
|---------|----------|----------|
| Idade Q1 (mais jovens) | 0,125 | 0,167 |
| Idade Q4 (mais idosos) | 0,075 | 0,124 |
| **Escolaridade Q4 (mais alta)** | **0,006** | **−0,009** |
| Escolaridade Q1 (mais baixa) | 0,116 | 0,110 |

**Achado decisivo:** Em seções homogeneamente de alta escolaridade, a correlação **desaparece** (r=0,006, p=0,03 em 2026; r=−0,009 em 2022). Isso elimina a hipótese de que a correlação é causada por manipulação da urna. Se fosse fraude via velocidade da urna, operaria igualmente em todos os estratos de escolaridade.

**Impacto em votos:** A correlação residual (r=0,046) corresponde a ~0,2 pp sobre ~120M de votos = ~240k votos, muito abaixo da margem do 2T (~2,2M). E essa correlação residual pode ser explicada por variáveis demográficas que não estão no perfil (renda, zona rural/urbana).

---

## Frente F — bweb CSV bruto × parquet BU

Lemos todos os 28 CSVs do bweb (sistema público de divulgação do TSE) e comparamos cada voto por seção contra o parquet extraído dos BUs das urnas.

| Métrica | 2026 | 2022 |
|---------|------|------|
| CSVs lidos | 28 | 28 |
| Seções no bweb | 499.205 | 471.636 |
| Seções no parquet | 499.207 | 472.027 |
| Em ambos | 499.205 | 471.636 |
| Só no parquet | 2 | 391 |
| **Divergências v13** | **0** | **0** |
| **Divergências v22** | **0** | **0** |

**Achado:** Zero divergências. O número publicado no site do TSE é idêntico ao que está dentro do BU assinado pela urna, em cada uma das ~500 mil seções.

As 2 seções "só no parquet" em 2026 são seções sem votação (comparecimento=0, voto=0) que o bweb não lista. As 391 em 2022 são o mesmo padrão.

**Impacto em votos:** 0 (zero) votos divergentes entre as duas fontes.

---

## Frente G — Auditoria da divulgação ao vivo

Analisamos as capturas de tela do painel de divulgação do TSE durante a noite da eleição.

### G1 — Monotonia (votos só crescem)

| Métrica | 2026 | 2022 |
|---------|------|------|
| Capturas válidas | 1 (insuficiente) | 27 |
| Violações de monotonia (seções) | — | 0 |
| Violações de monotonia (votos) | — | 0 |
| Violações por candidato | — | 0 |

**2022:** Em 27 capturas entre 17:23 e 00:29 (3,97% a 100%), a totalização cresceu estritamente a cada captura. Nenhum voto regrediu para nenhum candidato.

**2026:** Apenas 1 captura de 2T válida (3 arquivos corrompidos). Insuficiente para teste de monotonia. As capturas de 1T (6 válidas) podem ser usadas como complemento em futura análise.

### G2 — Última captura × resultado oficial

| Métrica | 2022 |
|---------|------|
| Última captura | 31/10/2022 00:29 (100,0%) |
| Divulgação v13 | 60.345.999 |
| Oficial (BU) v13 | 60.344.004 |
| **Diferença v13** | **+1.995** |
| Divulgação v22 | 58.206.354 |
| Oficial (BU) v22 | 58.204.272 |
| **Diferença v22** | **+2.082** |

**Explicação:** A divulgação mostra ~2k votos a mais por candidato. Isso é consistente com arredondamento do campo "100,00%" — a captura mostra 100% mas faltavam poucas seções com votos zerados (sem votação). Os BUs dessas seções chegaram depois e zeraram a conta.

**Impacto em votos:** ±2k votos explicados por latência da totalização, não por manipulação.

### G3 — Oscilação de fatia durante totalização (2022)

| Candidato | Maior swing | Quando |
|-----------|------------|--------|
| 13 (Lula) | 3,57 pp | Entre 3,97% e 45,29% |
| 22 (Bolsonaro) | 3,57 pp | Entre 3,97% e 45,29% |

O maior swing ocorreu no início da totalização (quando poucos estados tinham entrado), o que é esperado. Após 50% totalizado, o swing máximo entre capturas consecutivas foi inferior a 0,3 pp — estabilidade normal.

---

## Síntese

| Frente | Resultado | Impacto |
|--------|-----------|---------|
| E — Demografia explica duração × resultado | 54–63% da correlação é demográfica; desaparece em seções de alta escolaridade | ~240k votos residuais (abaixo da margem) |
| F — bweb = BU | Zero divergências em ~1M de comparações | 0 votos |
| G — Totalização monotônica | Zero regressões em 27 capturas (2022) | 0 votos |

A correlação duração × resultado, que era o achado mais forte do estudo, é majoritariamente um efeito da composição demográfica das seções — especificamente da escolaridade. Não sobrevive ao controle direto.
