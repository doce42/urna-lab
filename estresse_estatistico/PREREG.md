# Pré-registro — Operação Estresse Estatístico

**Data:** 2026-11-02T23:30-03:00 (antes de rodar qualquer teste).
**Commit base:** repositório sem commits (working tree).
**Dados:** `dados_leves/secoes_{2022,2026}.parquet`, `dados_leves/perfil_por_secao_{2022,2026}.parquet`.

## Pergunta central

Os números publicados de votos por seção apresentam impressões digitais estatísticas de um processo artificial de geração ou alteração?

## Hipóteses concorrentes

| Código | Hipótese |
|---|---|
| H0 | Processo eleitoral heterogêneo (preferências distintas entre eleitores, municípios, locais e seções) |
| H1 | Alteração artificial dispersa (pequenas alterações em muitas seções) |
| H2 | Alteração concentrada (intervenções em locais, zonas, municípios ou regiões) |
| H3 | Algoritmo excessivamente regular (variação insuficiente, proporções repetidas, relações determinísticas) |
| H4 | Alteração preservadora de estatísticas (mantém médias/medianas/distribuições agregadas) |
| H5 | Dependência artificial entre registros (regra comum criando correlações residuais) |
| H6 | Erro operacional ou de processamento (formato, agregação, arredondamento) |
| H7 | Comportamento eleitoral legítimo não representado pelo modelo |

## Famílias de testes e o que será feito

### Família A — Impressões digitais dos números
- **EA1:** Distribuição condicional dos últimos dígitos (0–9) das contagens de votos de cada candidato, condicionada ao tamanho da seção (faixas de 50 em 50 eleitores). Referência: 10.000 simulações beta-binomiais por faixa. Estatística: chi-quadrado por faixa, combinado por Fisher. Aplica a 2022 e 2026, turnos 1 e 2.
- **EA2:** Proporções repetidas — frequência de frações v/n idênticas entre seções do mesmo município e entre municípios. Referência: simulação binomial com a mesma proporção municipal e o mesmo n. Estatística: contagem de colisões observada vs esperada.

### Família B — Suavidade excessiva (PRIORITÁRIA)
- **EB1:** Dispersão residual intra-local. Para cada local de votação com ≥ 5 seções, calcular a variância da proporção de Lula entre seções, condicionada à proporção do local. Modelo nulo: beta-binomial com sobredispersão estimada por UF (MLE). Estatística: razão variância observada / variância esperada, por local. Detecta tanto excesso quanto insuficiência de dispersão. BH q=0.05.
- **EB2:** Entropia condicional das contagens. Para cada município com ≥ 10 seções, calcular a entropia de Shannon da distribuição discreta de votos em Lula por seção (normalizada pelo tamanho). Comparar com 1.000 simulações beta-binomiais calibradas ao município. Detecta regularidade artificial (entropia baixa demais).

### Família C — Dependências e correlações residuais
- **EC1:** Modelo condicional: regressão por UF de v13/(v13+v22) no 2º turno sobre: (a) proporção no 1º turno, (b) tamanho, (c) perfil demográfico (idade, escolaridade, sexo), (d) comparecimento. Resíduos: autocorrelação espacial (Moran's I com vizinhança por local e zona). Distingue H5 de H0/H7.
- **EC2:** Correlação residual entre candidato e comparecimento dentro do município, após remover o efeito da proporção no 1º turno. Se há dependência artificial (H5), a relação Lula × comparecimento difere entre turnos além do esperado. Referência: permutação de seções dentro do município.

### Família D — Varredura territorial adversarial
- **ED1:** Scan statistic: para cada município m, estatística = |média dos z das seções| × √(n_seções). Calibração por permutação do z dentro da UF (1.000 réplicas). Detecta H2.
- **ED2:** Descontinuidade de fronteira: para cada par de municípios vizinhos na mesma zona, diferença média dos resíduos entre o último decil de seções de um e o primeiro decil do outro. Referência: pares aleatórios dentro da zona. Detecta H2 em fronteiras.

### Família E — Primeiro vs segundo turno
- **EE1:** Relação entre turnos: regressão logit_2 ~ logit_1 por município. Teste de linearidade excessiva: comparar R² observado com R² de 1.000 simulações beta-binomiais que reproduzem a transferência municipal. R² perto demais de 1.0 seria compatível com H3.
- **EE2:** Resíduos modulares entre turnos: (v13_2 − v13_1) mod k para k=2,3,5,10. Se há arredondamento (H6) ou regra aritmética (H3), certas classes modulares serão mais frequentes. Referência: simulação da mudança com ruído binomial.

### Família F — Aleatoriedade, ordem e temporalidade
- **EF1:** Autocorrelação residual na ordem de recebimento dos BUs dentro do município: correlação dos resíduos do modelo (EC1) entre seções consecutivas. H5 prevê autocorrelação; H0 não. Referência: permutação da ordem dentro do município.
- **Nota:** sem snapshots datados da divulgação (limitação declarada).

### Família G — Simulação de geração artificial
- **EG1:** Gerar 6 mundos sintéticos (troca dispersa ±50k, troca concentrada ±50k em 5 municípios, suavização forçada, algoritmo proporcional) e rodar EA1, EB1, EC1, ED1, EE1 em cada. Medir poder e falsos alarmes.

### Família H — Busca sistemática de anomalias desconhecidas
- **EH1:** Isolation Forest nos resíduos multivariados (z do T02, z do EB1, resíduo do EC1, mudança de comparecimento entre turnos, fração sem biometria). Top 100 anomalias agrupadas por local/zona/município.

## Critérios fixados antes

- α = 0.01 por teste individual.
- BH q = 0.05 em famílias de testes geográficos.
- Tamanho de efeito sempre em votos (não só z ou p).
- Seções com < 20 válidos excluídas.
- Todo teste roda em 2022 e 2026.
- Exploratório: descoberta nos dados. Confirmatório: validação em holdout (metade aleatória de municípios, semente 42).
- Anomalia: divergência que (a) passa do limiar, (b) não se explica por H0/H6/H7 e (c) se repete em ≥ 2 famílias independentes.

## Limites da operação

- 8 famílias, 2 testes principais por família.
- 1 etapa exploratória + 1 confirmatória por teste.
- Até 3 modelos nulos plausíveis.
- Dados locais existentes; sem downloads novos.
- Sem subagentes em cascata.
- Sem variantes por não-significância.
