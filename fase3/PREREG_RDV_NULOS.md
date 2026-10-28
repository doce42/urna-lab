# Pré-registro da rodada 7: o que foi digitado nos nulos (T58) e calibração do C06 com origem conhecida (T59), 28/10/2026

Escrito antes de ler os dígitos no país inteiro (só uma urna do AC e uma de AL foram abertas para conferir a estrutura). Motivação: a fila do T57 (o número digitado em cada nulo está no RDV e não tinha sido lido) e a ideia de calibrar a inferência ecológica com dado real, vinda de um estudo independente (welwelaraujo.github.io/transferencia_votos, que não é fonte).

**Dado:** RDV de todas as seções, 2022 e 2026, 1º e 2º turno (pacotes já no disco). No RDV cada voto tem tipo (2 nominal, 3 branco, 4 nulo com número digitado, 6 nulo sem número em 2022/2026) e o número digitado. Extração: `fase3/rdv_nulos.py` → `fase3/resultados/rdv_nulos_<ano>_<turno>t.parquet` (por seção: cargo, tipo, número, quantidade, só votos nulos e brancos; e os números com voto nominal para governador por UF). Conferência obrigatória: total de nulos e brancos de presidente por seção = o já gravado (rdv_nulo, rdv_branco); diferença ≠ 0 é artefato do leitor e para tudo.

## T58: o que os eleitores digitaram nos nulos de presidente?
- **Classes do número digitado:** (a) número com voto nominal para governador na mesma UF e turno (candidato a governador); (b) número de candidato a presidente eliminado no 1º turno (só no 2º turno); (c) zeros ("0", "00"); (d) outros; (e) sem número.
- **Medidas:** classes por ano e turno, nacional e por grupo de UF (com/sem 2º turno de governador); no 2º turno de 2026, os nulos que digitam número de governador explicam quanto dos +0,78 ponto das UFs com governador (T57)? e no 1º turno de 2026, o excesso de nulos onde Lula é forte (T56) é de qual classe?
- **Leitura pré-fixada:** se a classe (a) concentrar o excesso de nulos nas UFs com 2º turno de governador, o mecanismo do T57 fica medido diretamente (erro de campo). Descritivo e determinístico.

## T59: o C06 acerta uma origem conhecida?
- **Destino de origem quase conhecida:** no 2º turno, nulo digitando o número de um candidato a presidente eliminado no 1º turno (2026: 14, 70, 55; 2022: 12, 15). Quem digita 14 no 2º turno quase certamente votou 14 no 1º.
- **Teste:** o mesmo Goodman do C06 (efeito fixo de município, ponderado), com esse destino separado; mede-se a fração do destino que o modelo atribui à origem certa.
- **Critério fixado antes:** passa se ≥ 50% do destino for atribuído à origem certa, nacional e na maioria das UFs; falha se < 25%. Entre 25% e 50%: parcial. Se falhar, as magnitudes do C06 (e da Q39) passam a ser lidas só como direção.

Orçamento: 2 investigações; extração 1 vez (+1 repetição por falha operacional); cada teste 1 execução + 1 correção. Pesado: ~2 mi de arquivos RDV, CPU por horas, com nice e no máximo 12 processos; RAM baixa.
