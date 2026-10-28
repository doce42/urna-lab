# Pré-registro: "Lula melhorou em ~93% dos municípios e 100% dos estados" e a resposta com 2022 (T51)

Escrito em 28/10/2026, antes de qualquer contagem. Origem (só pergunta): post no X citando "LULA MELHOROU EM RELAÇÃO À FLÁVIO EM ~93% DOS MUNICÍPIOS ... NOS ESTADOS ... 100%" e a resposta (@guilherme_) com duas imagens: tabela "Eleição de 2022: Bolsonaro cresceu mais em 4.849 de 5.570 municípios (87,1%)", por UF, critério "Δ votos do candidato entre os turnos, comparado ao rival, em cada município", exterior excluído; e gráfico "quanto o candidato de trás cresceu e quanto precisava" (2022 Bolsonaro +1,95; 2026 Lula +2,8; só em 2026 passou do traço). O texto do post diz 2018, a imagem diz 2022: testamos 2022 (2018 não está no projeto).

**Medidas:**
1. Critério da tabela: por município, Δ = (votos 2º − 1º turno) do candidato menos o mesmo do rival; conta onde Δ > 0, < 0, = 0. 2026 (Lula × Flávio) e 2022 (Bolsonaro × Lula). Por UF: municípios e agregado estadual.
2. Variante em proporção: Δ da proporção de Lula em Lula + rival.
3. Gráfico: proporção do candidato de trás em (Lula + rival) no 1º turno, no 2º, o crescimento e quanto faltava para 50%, em 2022 e 2026.

**Leitura pré-fixada:** reprodução se bater exatamente ou a menos de 1 p.p.; o ponto testado é se "crescer em quase todos os municípios" é raro. Se 2022 tiver fração parecida para o candidato que cresceu, a uniformidade é padrão de 2º turno, não sinal. Descritivo.

Orçamento: 1 execução. Script `fase3/crescimento_turnos.py`.
