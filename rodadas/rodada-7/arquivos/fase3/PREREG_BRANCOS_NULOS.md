# Pré-registro: "a anomalia dos brancos e nulos" (T56), 28/10/2026

Escrito antes de rodar o que é novo. Origem (só pergunta): post de @calvete_pedro no X com tabela por UF (inferência ecológica: em 2026 os brancos e nulos do 1º turno vão quase todos para Lula, em 2022 boa parte ia para Bolsonaro) e as três explicações que o próprio post lista: (1) eleitores de Lula anularam ou votaram em branco no 1º turno e voltaram; (2) campanha entre quem rejeitava os dois; (3) viés ecológico. Comentários: totais de brancos e nulos por turno; "6 cargos no 1º turno fazem idosos errar".

**Já existente:** C06 (Goodman por UF, com efeito fixo de município) dá a mesma direção; T37 mostra que a magnitude do C06 é frágil sob heterogeneidade; Q22/Q24/Q26: identidade exata, fluxos individuais não identificáveis.

**Medidas novas:**
- (a) Reprodução: linha "Branco/nulo (1º)" do C06 nacional e por UF, 2022 e 2026; número de UFs com fração para o candidato da direita < 5%.
- (b) Totais de brancos e nulos por turno, 2022 e 2026 (conferir os números dos comentários).
- (c) Teste que distingue (1)/(2) de (3): nas seções com o mesmo número em 2022 e 2026, excesso de brancos+nulos no 1º turno de 2026 sobre o 1º turno de 2022 (em pontos do comparecimento) e sua relação com a proporção de Lula em 2022 (inclinação dentro do município); o mesmo no 2º turno. Se o excesso do 1º turno de 2026 for maior onde Lula é forte e sumir no 2º turno, o padrão está no próprio 1º turno (compatível com 1 ou 2), e não só no estimador. Se não houver excesso, o resultado do C06 é atribuível à estrutura (3) ou a mudança entre turnos sem marca no 1º.
- (d) Cargos no 1º turno: 2022 e 2026 tiveram as mesmas eleições gerais no 1º turno; comparar o nível de brancos+nulos de presidente no 1º turno dos dois anos.

**Leitura pré-fixada:** descritiva para (a), (b), (d); (c) é a evidência que separa as hipóteses, sem identificar eleitores. Nada aqui distingue (1) de (2).

Orçamento: 1 execução + 1 correção. Script `fase3/brancos_nulos.py`.
