# F3, missão de resolução: pré-registro das investigações R1 a R4 (28/10/2026)

Escrito antes de qualquer execução. Limites:
- 4 investigações, cada uma com um teste principal e uma validação ou sensibilidade;
- uma correção e uma repetição por falha operacional;
- sem subagente, sem reprocessamento nacional, sem baixar bases grandes.

As respostas às 33 perguntas do inventário ficam em `fase3/RESPOSTAS_F3.md`. Elas usam primeiro os resultados existentes. As investigações abaixo atacam o que os resultados existentes não respondiam e que dados locais, ou uma fonte externa pequena e definida, permitem responder.

## R1. Integridade de 2022 pelos arquivos já decodificados (Q1 a Q5 para 2022)
- **Pergunta:** em 2022, nos dois turnos, os votos de Presidente da tabela publicada (BU na Web) são iguais aos do boletim (`bu.dat`), aos da recontagem pelo RDV e aos do boletim impresso, seção a seção? E hash e assinatura conferem?
- **Hipóteses:** igualdade em todas as seções com arquivo × divergência em alguma seção.
- **O que mudaria a conclusão:** qualquer seção com valor diferente, com o arquivo lido.
- **Universo:** `analise/brutos/2022_{1,2}t/urnas_*.parquet` (colunas `bu_*`, `rdv_*`, `img_*`, `hash_ok_*`, `assin_*`, já decodificadas pelo leitor do projeto) × `analise/base_2022.parquet`, mais as 159 seções do Sistema de Apuração já verificadas no SA22.
- **Regra:** uma divergência só conta se o arquivo foi lido (valor presente). Ausente é "não lido", não "diferente". Para o RDV, os nulos por suspensão (tipo 6) entram em "nulo", como no T17b.
- **Validação:** 100 seções sorteadas (semente 9100) são decodificadas de novo, direto dos zips, com as funções do leitor. Comparadas com o parquet, as duas leituras devem ser idênticas.
- **Parada:** uma execução.
- **Custo:** minutos.

## R2. Curva divulgada × curva reconstruída (Q8, Q9, Q11 parcial, Q14)
- **Pergunta:** a sequência pública divulgada durante a apuração coincide com a reconstrução do projeto pela hora de recebimento dos boletins? Quantas mudanças de liderança aparecem em cada uma?
- **Fonte externa, de escopo definido:**
  - **O que:** capturas do Internet Archive (Wayback Machine) do JSON nacional oficial de resultados de Presidente.
  - **Endpoints:** `resultados.tse.jus.br/oficial/ele2022/544|545/dados-simplificados/br/br-c0001-e000544|545-r.json` e `.../ele2026/6257|6258/dados/br/br-c0001-e00625[78]-u.json`.
  - **Janela:** da abertura da apuração até as 06h UTC do dia seguinte.
  - **Variantes:** com e sem parâmetro de cache, só respostas HTTP 200.
  - **Formato:** os `.jws`, que são versões assinadas, são lidos se tiverem o mesmo conteúdo em JSON.
  - **Busca:** uma consulta ao índice (CDX) e o download de cada captura (alguns KB cada), sem nenhuma outra busca.
- **Comparação, por captura:**
  - **(a) Por seções:** a reconstrução com o mesmo número de seções totalizadas (`st`), na ordem de `DT_BU_RECEBIDO`, comparada com os votos publicados de cada finalista.
  - **(b) Por horário:** a reconstrução com as seções recebidas até a hora de geração (`hg`), na mesma comparação.
- **Critérios fixados antes:**
  - **Consistente:** em (a), a diferença de proporção de cada finalista no total publicado fica abaixo de 0,1 ponto percentual e o líder é o mesmo.
  - **Divergência objetiva:**
    - votos de um candidato que diminuem de uma captura para outra posterior; ou
    - última captura diferente do total oficial final; ou
    - proporção da captura impossível de obter com qualquer conjunto de `st` seções da base (fora do intervalo entre a soma das `st` seções com menor e maior proporção do candidato).
  - **Lideranças na sequência pública:** contadas entre capturas consecutivas, com a ressalva de que a sequência é amostrada (cobertura informada).
- **Validação:** sensibilidade (b), que compara por horário e não por número de seções, e a defasagem entre recebimento e divulgação que melhor ajusta.
- **Parada:** uma execução. Se uma eleição não tiver nenhuma captura durante a apuração, ela é dada como "sem sequência pública disponível no escopo".

## R3. Zeros de votos com modelo de cauda baixa validado fora da amostra (Q18, Q19)
- **Pergunta:** depois de controlar o tamanho da seção, a proporção do candidato no mesmo local, na zona, no município e (no 2º turno) na própria seção no 1º turno, o número de seções com zero votos para o finalista é incomum?
- **Modelo:** regressão logística de I(y = 0), com as covariáveis:
  - log dos válidos;
  - logit da proporção do candidato nas outras seções do local, da zona e do município (sem a própria seção);
  - (2º turno) logit da proporção do candidato na própria seção no 1º turno.
  - Um modelo separado para I(y ≤ 2), usado como verificação preditiva.
- **Separação treino e teste:** sorteio de municípios em duas metades (semente 9300), com ajuste na metade A e avaliação na B, e o inverso. Assim cada seção tem predição feita sem a sua metade.
- **Calibração, critério fixado antes:** o modelo é **validado** se, fora da amostra:
  1. o total previsto de zeros fica dentro de ±15% do observado em todos os conjuntos de controle (Lula 2022 e 2026, dois turnos; candidatos 2 e 3 do 1º turno de cada ano; e, como verificação preditiva, I(y ≤ 2) do próprio alvo);
  2. em decis de probabilidade prevista, o teste de Hosmer–Lemeshow não rejeita a 1%, ou a razão observado/previsto fica entre 0,8 e 1,25 nos 3 decis superiores.
- **Leitura confirmatória (só se validado):**
  - **"Incomum":** zeros observados do alvo acima do percentil 97,5 do intervalo de predição (soma de Bernoulli com bootstrap de municípios).
  - **"Não incomum":** dentro do intervalo.
  - **Sem validação:** "não determinado", sem outro modelo nesta sessão.
- **Mesmo método nos dois anos:** Flávio 2026 e Bolsonaro 2022.
- **Sensibilidade:** sem a covariável do 1º turno.
- **Parada:** uma execução.

## R4. Zona 251 de São Paulo (2022): o perfil do eleitorado explica o desvio? (P14, P20, Q25)
- **Pergunta:** o desvio médio da virada na zona 251 (2º maior z médio entre 58 zonas da capital) persiste depois de controlar o perfil do eleitorado da seção?
- **Hipóteses:** composição do eleitorado (escolaridade, idade, sexo) explica × persiste após controle.
- **Dados:** `dados/2022/perfil_eleitorado/perfil_eleitor_secao_2022_SP.zip` (perfil por seção, oficial) × resíduo zz do I3 (modelo completo do P9) nas seções da capital.
- **Modelo:** regressão linear de zz em proporções por faixa de escolaridade, faixa etária e sexo, mais o log dos aptos, ajustada nas seções da capital **fora** das zonas 251 e 259, para não absorver o efeito testado. O resíduo médio das zonas 251 e 259 é avaliado com erro padrão por bootstrap de locais.
- **Critério fixado antes:**
  - **"Explicado":** o resíduo médio da 251 cai abaixo de 1/3 do desvio original e o IC de 95% inclui 0.
  - **"Persiste":** o IC exclui 0 e o desvio residual é pelo menos 2/3 do original.
  - **Fora disso:** "explicado em parte".
- **Sensibilidade:** ajuste incluindo todas as zonas.
- **Parada:** uma execução.
- **Causa:** mesmo que persista, o teste não demonstra causa. Só exclui a explicação pela composição medida.

## Fila (não executada nesta sessão)
- **Q10 e Q12:** modelo de chegada validado. Com a sequência pública do R2 como validação, um modelo de chegada por lotes poderia ser testado.
- **Q13:** comparação formal entre 2022 e 2026 após controles. Depende de Q10.
- **2º turno de 2026:** comparação com decodificação de terceiro.

## Execução e desvios (registrados depois de rodar)
- **R1:** duas correções do comparador, uma acima do orçamento.
  1. `NaN` mais nulo por suspensão virava `NaN`, contado como diferença.
  2. Em 2022, a regra pré-registrada somava o nulo por suspensão de novo, mas o leitor de 2022 já o inclui no nulo (`processar_brutos.py`, linha 200). Isso gerou 42.764 e 7.410 diferenças falsas. Lido como o leitor grava: 0 diferenças.
  - A validação (releitura de 100 seções) também tinha o erro `NaN or 0`, corrigido. Ficou 100/100.
- **R2:** três execuções.
  1. O `urllib` teve a conexão recusada (trocado por `curl`, correção).
  2. Uma captura falhou e interrompeu tudo.
  3. Passou a tolerar falha por captura e a usar as capturas guardadas quando o índice do Internet Archive recusou conexão. A 3ª execução ficou acima do orçamento, declarada.
- **R3:** o critério de calibração pré-registrado se mostrou inadequado:
  - o teste de Hosmer–Lemeshow com centenas de milhares de seções rejeita qualquer desvio;
  - controles com 1 a 8 zeros não cabem na tolerância de ±15%.
  - A leitura formal seguiu o critério ("não determinado"). A descrição fora da amostra foi relatada à parte, sem valor confirmatório.
- **R4:** executado como pré-registrado.
- **Fora das 4 investigações:** contagens determinísticas da identidade contábil entre turnos (`resultados/entre_turnos_contas.json`). A primeira soma de "eliminados" incluiu colunas que não eram candidatos e foi corrigida.
