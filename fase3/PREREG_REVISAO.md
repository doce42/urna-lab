# F3 em revisão: pré-registro das investigações I1, I2 e I3 (28/10/2026)

Escrito antes de qualquer execução, depois da auditoria em `fase3/AUDITORIA_F3.md` e com autorização do responsável. Limites: 3 investigações, um script principal por investigação (`fase3/rev_i1_poder.py`, `fase3/rev_i2_zeros.py`, `fase3/rev_i3_espacial.py`), uma etapa de validação ou sensibilidade em cada uma, uma correção e uma repetição por falha técnica, nenhum subagente, nenhum download, nenhuma investigação nova por resultado inesperado. Dados: só as bases já preparadas (`analise/base*.parquet`) e a malha municipal já usada no P19.

Achado da auditoria que motiva o I1: no P18, os falsos alarmes do limiar "calibrado no mundo" foram medidos nos mesmos mundos usados para fixar o limiar, portanto são 0 por construção. O I1 separa mundos de calibração e de avaliação.

## I1. Poder contra intervenções concentradas (`rev_i1_poder.py`)

**Pergunta:** que magnitude de troca de votos, concentrada em locais, municípios ou regiões, a bateria (T02, regra do T13 e E02 corrigido) detecta, nos dois sentidos?

**Universo:** seções com pelo menos 20 válidos nos dois turnos, sem exterior. Principal: 2026, 2º turno. Validação: 2022, 2º turno, com o mesmo desenho.

**Mundos legítimos:** os votos de Lula no 2º turno são sorteados por binomial a partir da proporção real de cada seção, como no P18. Há 20 mundos de calibração, que só fixam limiares, e 30 mundos de avaliação, que medem falsos alarmes e servem de base para as injeções.

**Mecanismos**, cada um cobrindo cerca de 1% das seções, sorteados de novo em cada mundo:
- **M0 disperso:** seções sorteadas ao acaso. É a âncora, igual ao P18.
- **M1 locais:** locais de votação inteiros, sorteados até completar 1%.
- **M2 municípios:** municípios inteiros, sorteados com igual probabilidade até completar 1%.
- **M3 região:** um município semente sorteado mais os municípios de centróide mais próximo, até completar 1%.

**Intervenção:** em cada seção afetada, mover m dos votos válidos do perdedor para o beneficiário, com m de 2%, 5% e 10% e limite no que o perdedor tem. Há dois sentidos: A (adversário → Lula) e B (Lula → adversário). Cada resultado informa os votos movidos.

**Estatísticas** (as mesmas do registro):
- **T02:** contagem de seções com z robusto acima de 5 e abaixo de −5, com mediana municipal.
- **T13:** regra de duas caudas do P18 (T1 a T4).
- **E02 corrigido:** modelo "simples" do P9, isto é, resíduo da virada por UF, média por local, correção por ρ intralocal e BH com q = 0,05. A contagem de locais significativos é feita por sentido em duas versões: ρ reestimado em cada mundo, que é como o método é aplicado, e ρ fixo no valor dos dados reais.

**Regras de alarme:**
- **Ancorada no real:** a mesma do P18 (contagem real + máx(5, 5√contagem); T2 × 3; T4 3,5), usada nas conclusões anteriores.
- **Calibrada:** o máximo dos 20 mundos de calibração mais as margens do P18 (contagens +5, T2 +0,05, T4 +0,5). Para o E02 a margem é +5 locais.

**Saídas:** taxa de detecção com IC de Wilson de 95% por teste e pelo conjunto, para cada mecanismo × magnitude × sentido. Também a taxa de falso alarme nos 30 mundos de avaliação sem injeção, com IC.

**Critério de leitura**, fixado antes: um mecanismo é "detectável" numa magnitude se o conjunto alcança pelo menos 90% (limite inferior do IC acima de 75%) e o falso alarme do conjunto fica em até 10%. É "não detectável" se o limite superior do IC fica abaixo de 25%. Fora disso, é "detecção incerta".

**Validação:** o mesmo desenho em 2022, 2º turno, com 30 mundos de avaliação.

## I2. Zeros de votos com modelo calibrado (`rev_i2_zeros.py`)

**Pergunta:** o número de seções com zero votos para um finalista (Flávio em 2026, Bolsonaro em 2022, nos dois turnos) excede o previsto por um modelo calibrado?

**Universo:** o mesmo do E3, isto é, sem exterior e com válidos acima de 0 nos dois turnos.

**Modelo:** os votos do candidato na seção seguem uma beta-binomial com média μ e sobredispersão ρ.
- μ vem do mesmo local de votação, sem a própria seção: (votos do candidato no local − y) / (válidos no local − n), encolhida para a média do município com peso de 50 válidos.
- Se o local tem uma seção só, usa-se a zona (sem a seção). Se a zona também tem uma só, o município.
- ρ é estimado por máxima verossimilhança da beta-binomial truncada em zero, ou seja, só com seções em que o candidato teve votos. A célula zero não entra no ajuste.

**Calibração preditiva**, avaliada antes de olhar o resultado confirmatório:
- **Controles:** zeros de Lula nos quatro conjuntos ano × turno.
- **Candidatos menores:** os dois maiores fora os finalistas no 1º turno de cada ano (2026: números 70 e 14; 2022: 15 e 12), em que zeros são comuns.
- **Critério:** o modelo é "calibrado" se, em todos os controles com esperado de pelo menos 5, o observado cai dentro do intervalo de predição de 95%. Nos controles com esperado abaixo de 5, a calibração é só descrita.
- **Se não calibrar:** o resultado confirmatório é relatado como "não interpretável" e não se conclui excesso nem ausência de excesso.

**Intervalos:**
- **Predição:** soma de Bernoulli(P0 da seção), 4.000 simulações.
- **Razão observado/esperado:** IC de 95% por bootstrap de municípios, 1.000 réplicas.

**Critério confirmatório**, só se calibrado:
- **"Excesso":** observado acima do percentil 97,5 da predição e limite inferior do IC da razão acima de 1.
- **"Excesso, se existir, menor que 50%":** limite superior do IC da razão abaixo de 1,5.
- **Fora disso:** "inconclusivo".
- **Comparação 2026 × 2022:** razão das razões com IC de bootstrap.

**Alcance em votos:** soma de μ × n nas seções com zero, que são os votos esperados para o candidato nessas seções.

**Sensibilidade:** prior pela zona (sem a seção) em vez do local.

## I3. Concentrações territoriais com nulo espacial (`rev_i3_espacial.py`)

**Pergunta:** quantos locais de votação seguem atípicos quando o termo de comparação é o entorno (zona ou município) e não só a UF? Os locais de São Paulo capital de 2022 resistem a isso e à remoção das seções que os selecionaram?

**Universo:** o do P9, isto é, seções com pelo menos 20 válidos nos dois turnos, sem exterior, e locais com pelo menos 3 seções; modelo "completo" do P9. Rodado para 2026 e 2022.

**Estatística por local:** d = (média do z das seções do local) − (média do z das demais seções da mesma zona), com fallback para o município sem o local. Locais sem nenhuma outra seção de referência ficam fora e são contados.

**Nulo empírico:** a escala de d é estimada pela dispersão robusta (MAD × 1,4826) de d entre todos os locais, por faixa de tamanho (3 a 5, 6 a 9, 10 a 14, 15 ou mais seções), centrada na mediana da faixa. z_esp = (d − mediana) / escala. P bilateral normal e BH com q = 0,05, contados por sentido.

**São Paulo 2022:** para cada um dos 15 locais com seções atípicas do P20:
- **z_esp:** com todas as seções.
- **z_esp sem as seções selecionadas:** só com as demais seções do local, excluindo as que tinham z acima de 5. É o teste da dependência da seleção.
- **z_esp em 2026:** do mesmo local, fora da amostra.

**Critério de leitura:**
- **Resiste ao nulo espacial:** BH significativo com todas as seções e z_esp acima de 3 sem as selecionadas.
- **Persiste:** z_esp de 2026 acima de 2.

**Sensibilidade:** referência pelo município em vez da zona.

## Registro

Resultados em `fase3/resultados/rev_i1.json`, `rev_i2.json` e `rev_i3.json`. Relatório da revisão no fim de `RELATORIO_F3.md`, com o estado de cada pergunta revisado em `fase3/inventario.json`, preservando os estados anteriores. Nada é publicado nem congelado sem aprovação.
