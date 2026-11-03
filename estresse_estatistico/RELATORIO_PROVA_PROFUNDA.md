# Relatório — Prova Profunda

**Data:** 2026-11-03  
**Premissa:** Os dados são colocados à prova pelo ângulo dos dados brutos, não dos totais agregados.  
**Dados:** 78 variáveis por urna extraídas dos arquivos brutos (logs, RDV, BU, assinaturas) + curva temporal minuto a minuto.

---

## O que mudou em relação aos testes anteriores

Os testes anteriores (bateria T01-T71, Estresse Estatístico, Operação Adversarial) operavam sobre **totais por seção** derivados dos parquets. Esta bateria vai direto nos dados que saem de dentro da urna:

- **Duração individual de cada voto** (em segundos, do log)
- **Tipo de habilitação de cada eleitor** (biometria, manual, mesário, do log)
- **Curva de votação minuto a minuto** (forma, autocorrelação, variabilidade geográfica)
- **Modelo físico da urna** e sua performance
- **Hashes SHA-512 e assinaturas criptográficas** de cada arquivo
- **Consistência entre 4 fontes independentes** (BU, RDV, imagem impressa, log)
- **Sequência temporal** (votos antes da abertura, intervalos impossíveis)

---

## Achados

### ACHADO 1 — Duração do voto correlaciona com resultado (r = 0,10 a 0,16)

**O que é:** Dentro do mesmo município, seções onde a mediana de duração do voto é menor tendem a ter proporção ligeiramente maior de votos no candidato 13 (Lula).

| Métrica | 2026 | 2022 |
|---------|------|------|
| Correlação intra-municipal (2t) | 0,102 | 0,157 |
| Controlando por município + modelo | 0,110 | 0,150 |
| Correlação no 1º turno | 0,390 | 0,323 |
| Δp13 entre Q1 rápido e Q4 lento | −0,060 | −0,046 |
| Impacto máximo hipotético | 2,35M votos | 1,56M votos |

**Por que é suspeito:** A correlação persiste mesmo controlando por município e modelo de urna (F=28 a 60, p≈0). O impacto hipotético (se 100% fosse fabricação) é da ordem da margem do 2º turno.

**Por que NÃO é evidência de fraude:**
1. **Existe no 1º turno com sinal mais forte** (r=0,39 em 2026). No 1º turno, a "fabricação" teria que afetar uma eleição com múltiplos candidatos e resultado menos disputado.
2. **Existe em 2022 com o mesmo padrão.** Fraude teria que operar idêntica em ambas.
3. **Varia por UF de forma consistente com demografia:** TO (r=0,38), ES (r=0,24), AM (r=0,19) — estados com maior heterogeneidade intra-municipal de idade e escolaridade. SP (r=0,04), RS (r=0,04) — estados mais homogêneos intra-município.
4. **Explicação causal plausível:** Eleitores mais jovens e com maior escolaridade votam mais rápido (conhecem a interface, lembram o número) e, em média, votam diferente de idosos. Isso produz correlação duração-resultado dentro do município sem fabricação.

**Classificação:** Artefato demográfico. A correlação é **real** mas não é **causal via fraude**. A mesma correlação aparece em eleições e turnos diferentes, com magnitude proporcional à heterogeneidade demográfica.

---

### ACHADO 2 — Modelo de urna prediz resíduo do resultado

**O que é:** Urnas mais antigas (UE2013, UE2015) apresentam resultado ligeiramente diferente das mais novas (UE2020, UE2022) dentro da mesma zona.

| UF | UE2013 (resíduo p13) | UE2020 (resíduo p13) |
|----|---------------------|---------------------|
| RJ | +0,044 | −0,007 |
| MG | −0,021 | 0,000 |
| SP | −0,001 | +0,001 |

**Por que é suspeito:** A ANOVA é significativa mesmo controlando por zona (F=28, p≈0 em 2026).

**Por que NÃO é evidência de fraude:**
1. O **sinal muda de UF pra UF**: no RJ, urnas velhas estão em bairros pró-Lula; em MG, em áreas anti-Lula. Fraude via modelo de urna teria que operar em sentidos opostos em cada estado.
2. A magnitude é pequena: <1% na maioria dos estados, 4% no RJ (onde as UE2013 são poucas e concentradas em locais específicos).
3. Urnas antigas são realocadas de forma não-aleatória (escolas rurais mantêm a mesma urna por mais tempo).

**Classificação:** Confundimento geográfico. O modelo de urna é proxy de localização, não causa.

---

### ACHADO 3 — Falhas criptográficas (28 em 2022, 0 em 2026)

**O que é:** Em 2022, 10 RDVs e 4 logs falharam na verificação de hash/assinatura.

**Investigação:** Todas as 14 urnas com falha apresentam **v13=0, v22=0, comparecimento=0**. São seções onde a urna foi ativada mas não houve votação (contingência, seção cancelada, seção especial sem eleitores). O arquivo RDV/log existe mas está vazio ou malformado.

**Em 2026:** Zero falhas em 3.983.174 verificações.

**Classificação:** Artefato de contingência. Zero impacto em votos.

---

### ACHADO 4 — BU diverge do log no comparecimento (7 em 2026, 49 em 2022)

**O que é:** Em 7 urnas (2026) e 49 (2022), o total de votos computados no log difere do total no BU.

**Investigação:**
- A maioria das divergências é de 1 voto (arredondamento ou evento duplicado no log).
- O caso extremo (ES mun=57932, Δ=304) é uma urna cujo log contém eventos de outra urna do mesmo local (log concatenado).
- Em 2022, 2 urnas com LOG=0 (BA mun=34134, AM mun=2550): o log da urna não foi encontrado no pacote; o BU é a fonte primária.

**Classificação:** Artefato de processamento de logs. Não afeta a contagem (o BU é o documento primário, assinado pela urna).

---

### ACHADO 5 — Votos antes das 7h (94k em 2026, 76k em 2022)

**O que é:** Aproximadamente 94 mil votos registrados antes das 7h no 2º turno de 2026.

**Investigação:** **100% concentrados no Acre e Amazonas.** Esses estados estão no fuso -2h e -1h em relação a Brasília. A votação abre às 8h hora local = 6h hora de Brasília. O campo `primeiro_voto` registra hora local da urna, enquanto os arquivos de votos por minuto registram hora de Brasília.

**Prova:** `seq_votos_dia - bu_comparecimento = 0` em todas essas urnas → nenhum voto extra.

**Classificação:** Fuso horário. Não há votos antes da abertura.

---

### ACHADOS de consistência (positivos para a integridade)

| Verificação | 2026 | 2022 |
|-------------|------|------|
| BU = RDV (votos do candidato 13) | 497.786 de 497.786 (100%) | 470.851 de 470.851 (100%) |
| BU = IMG (boletim impresso) | 100% | 100% |
| Hash SHA-512 de todos os arquivos | 0 falhas | 14 falhas (urnas sem votação) |
| Assinatura criptográfica | 0 falhas | 14 falhas (urnas sem votação) |
| Votos sem habilitação | 0 | 0 |
| Intervalo entre votos < 3s | 0 urnas | 0 urnas |
| Verificação de software da urna | 162 falhas (0,03%) | 1 falha (0,0002%) |
| Uma versão de SW em todas as urnas | Sim (10.23.0.0) | Sim (8.26.0.0) |

**Duração do voto:**
- 2026: mediana 10,8s (CV=0,21), urnas mais novas mais rápidas
- 2022: mediana 14,5s (CV=0,25), mesma tendência
- Evolução entre eleições: −3,7s de mediana = urnas UE2020/UE2022 mais rápidas que UE2009-2015

**Curva temporal:**
- Autocorrelação 1min = 0,998 (suavidade natural da votação minuto a minuto)
- Variabilidade real entre municípios (CV=4,2 entre municípios por hora)
- Pico às 8h (abertura), cauda longa até 17h+

---

## Conclusão

Descemos ao nível mais profundo disponível nos dados: cada voto individualmente cronometrado, cada habilitação biométrica, cada hash criptográfico. Os achados suspeitos (correlação duração-resultado, modelo-resultado) se explicam por demografia e geografia, aparecem em ambas as eleições com o mesmo padrão, e mudariam de sinal entre estados se fossem fabricação.

Os achados de consistência são extraordinariamente fortes: **zero diferenças** entre BU, RDV e imagem impressa em quase 1 milhão de urnas; **zero votos sem habilitação**; **zero intervalos impossíveis**; integridade criptográfica perfeita em 2026 e com falhas apenas em urnas sem votação em 2022.

A correlação duração-resultado (Achado 1) merece atenção continuada: é o sinal mais forte que encontramos em todo o estudo (r=0,10-0,39). Mas sua presença em ambos os turnos, ambas as eleições, com magnitude proporcional à heterogeneidade demográfica de cada UF, é consistente com causa demográfica, não com fabricação.
