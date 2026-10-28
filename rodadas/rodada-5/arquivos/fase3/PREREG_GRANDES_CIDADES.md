# Teste H-GC: troca de votos no município inteiro de uma grande cidade (2026), pré-registro (28/10/2026)

Escrito antes de rodar.

**Motivo:** o A2 mostrou que a bateria não detecta com confiabilidade uma troca aplicada ao município inteiro de uma das 5 maiores cidades. É o maior ponto cego conhecido para uma fraude capaz de mudar votos em escala de centenas de milhares.

**Pergunta:** a virada entre turnos (Lula, logit 2º turno − logit 1º turno) de alguma grande cidade em 2026 está fora do que o próprio histórico (2022) e o perfil de votação do 1º turno preveem, quando comparada às outras cidades grandes?

**Hipóteses:**
- **H0:** a virada da cidade segue o padrão das cidades comparáveis, dado o histórico.
- **H1:** a virada da cidade foi deslocada por uma troca no município inteiro.

**Unidade:** município. Saídas da regressão: 1º e 2º turnos de 2026, com 2022 como histórico.

**Modelo:** virada de 2026 regredida em:
- virada do mesmo município em 2022;
- proporções do 1º turno de 2026 (Lula, adversário, demais);
- log do eleitorado;
- efeitos de UF.

O ajuste é por mínimos quadrados ponderados pelo eleitorado, com todos os municípios exceto os 5 alvos (São Paulo, Rio de Janeiro, Brasília, Fortaleza, Salvador).

**Escala de comparação:** resíduos dos 200 maiores municípios não alvo, em desvio robusto (MAD × 1,4826).

**Critério fixado antes:**
- **Desviante:** |resíduo| > 3 desvios robustos.
- **Correção para os 5 alvos:** Bonferroni, isto é, limiar equivalente a p < 0,01 por cidade.
- **Votos:** o resíduo é convertido em votos de Lula a mais ou a menos que o previsto no 2º turno.

**Poder, determinístico:** para cada cidade, calcular o deslocamento do logit que uma troca de 2%, 5% e 10% dos válidos produziria. Uma cidade é "testável" naquela magnitude se esse deslocamento for maior que o limiar (3 desvios robustos).

**Validação (falso alarme):** aplicar a mesma regra, deixando um de fora, a cada um dos outros 200 maiores municípios, um por vez fora do ajuste. A fração marcada como desviante estima o falso alarme. A regra só vale se essa fração for de até 5%.

**Universo:** municípios presentes nos dois anos, com o mesmo código TSE, sem o exterior.

**Parada:** uma execução, uma correção por falha operacional.

**Limite:** um deslocamento que acompanhe o padrão das outras cidades (troca em todas as grandes cidades ao mesmo tempo) não é detectado por este teste.
