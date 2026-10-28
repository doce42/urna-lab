"""Preenche testes[].impacto_votos no registro: quanto cada resultado representa em número de votos (ou por que não se traduz em votos).
Valores calculados em 28/10/2026 a partir dos resultados já existentes (referência: margem do 2º turno 2026 = 4.430.191 votos; 124.082.273 válidos)."""
import json, os
REG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "testes", "registro.json")
ZERO = "Zero votos de diferença nas comparações feitas; não há valor a converter."
I = {
"T01": "0 votos de diferença em 3.800.511 pares seção × votável (1º turno) e 1.931.103 (2º). Nenhum voto divergente entre as duas tabelas.",
"T02": "Excesso pró-Lula nas 33 seções acima de 5 desvios (2026): cerca de 740 votos; nas 13 pró-Flávio, cerca de 415 votos a menos para Lula. Em 2022: cerca de 2.600 e 350. Contra margem de 4,43 mi (2026): 0,017%. Se fosse tudo irregular (não demonstrado), não mudaria o resultado.",
"T03": "Efeito desprezível: r = +0,004. Nenhuma seção ou lote identificado; o teste não produz contagem de votos.",
"T04": "Efeito de −0,03 desvio-padrão por seção, limítrofe; não se traduz em um número de votos identificável. Nenhuma urna isolada sinalizada.",
"T05": "Não se traduz em votos: teste de padrão de dígitos; nenhum conjunto de seções sinalizado (p de 0,05 a 0,84).",
"T07": "0 seções acima de 100% de comparecimento; 0 votos de enchimento por esta assinatura.",
"T08": "0 boletins emitidos antes do fim da votação depois da correção do fuso; 0 votos envolvidos.",
"T09": "Prorrogação em 6.748 seções (1,4% das 499 mil); virada de +7,45 e +7,56 pp nos dois grupos: diferença de 0,1 pp, sem efeito identificável em votos.",
"T10": "Desvio máximo da curva de 0,08 pp (município) e 0,25 a 0,32 pp (estado). Sobre 124 mi de votos válidos, 0,32 pp equivale a ~400 mil votos num instante da curva; é distância entre a curva e a reconstrução, não votos alterados.",
"T11": "Não se traduz em votos: conta oscilações da curva (23 contra 22 ± 1).",
"T12": "Efeito de −14,7 para +0,3 (t) depois de controlar a idade: sem efeito residual; nenhum voto atribuível à liberação sem biometria (12,7% das habilitações).",
"T13": "Menor alteração detectada na grade: 11.677 votos movidos (0,1% das urnas, 10% dos válidos). Maior alteração localizada não detectada: 496.895 votos. Troca uniforme de até 2,48 mi de votos (2% dos válidos) não foi vista. Descreve a grade, não a probabilidade geral.",
"T13b": "Rajada convertendo 100% dos votos dos últimos 30 min em 'sem biometria' é vista em 76% a 98% das urnas alteradas; a 10% não é vista (recall ≈ 0%). As 13 urnas do 1º turno têm ≈140 votos no total.",
"T14": "0 votos de diferença entre log e comparecimento nas urnas sem exceção; nas exceções documentadas (T36) a soma das diferenças é 59 votos no 1º turno e 358 no 2º.",
"T15": ZERO,
"T16": "Não mede votos: mede se os bytes batem com a assinatura. 0 arquivos com hash ou assinatura divergente em 499.176 e 499.178 urnas.",
"T16c": "Não se traduz em votos: valida o verificador (300/300 legítimas aceitas; 0 aceitas nos 5 controles negativos).",
"T17": "0 votos de diferença entre a recontagem do RDV e o boletim em 499.176 urnas (1º turno).",
"T17b": ZERO,
"T19": "Mesmos números do T02 a T11 em 2022; ver cada teste.",
"T20": "Maior diferença entre modelos: +0,003 logit na UE2013 (2,59 mi de votos válidos no 2º turno), cerca de 1,9 mil votos; nos demais modelos, menos.",
"T21": "Não se traduz em votos: |z| ≤ 1,6 nos dois anos, nenhum excesso de percentuais inteiros.",
"T22": "Não se traduz em votos: assinatura de fraude incremental simétrica (±0,08) e igual à de 2022 (±0,10).",
"T23": "Sensibilidade em fração de seções, não em votos: troca de 20% dos votos da seção é vista em 97% das seções alteradas; troca de 5%, em 7%. Seções reais marcadas: 0,35% das avaliadas, abaixo do 1% esperado.",
"T24": "Urnas substituídas registradas (ex.: MS 22); sem diferença de totais registrada (T32).",
"T25": "Não se traduz em votos: canto vazio e curtose 3,7 contra 4,1 (2022).",
"T26": "Não se traduz em votos: método inadequado, excluído da conclusão.",
"T27": "Não se traduz em votos: p = 0,57 e 0,34 no comparecimento.",
"T28": "2º turno: 0 urnas, 0 votos. 1º turno: 13 urnas acusadas, ≈140 votos no total (6 a 14 habilitações sem biometria cada); 0,0001% dos votos.",
"T29": "1.120.676 votos (0,9% do 2º turno) abaixo de 5 s entre habilitação e voto, em 273.451 urnas; padrão estrutural que se repete em 2022 (306.528), sem direção para candidato.",
"T30": "1 urna por turno com primeiro voto 2 a 4 min antes da abertura registrada (urna substituída); votos envolvidos: os da urna, sem diferença de totais.",
"T31": "2º turno: 0 votos. 1º turno: 2 votos em 1 urna (RJ 60011/8/61, log corrompido pela própria urna; totais e assinatura conferem).",
"T32": "0 votos de diferença em 638 itens de voto e comparecimento. A diferença do eleitorado do exterior (−495 e −525) é de eleitores aptos, não de votos.",
"T33": "Sem votos atribuíveis: mesma versão do software em todas as urnas; falhas de verificação de assinatura do software em 128 urnas (1º turno) e 162 (2º), sem diferença de totais.",
"T34": "3.060 seções com troca de urna declarada (0,6%); a urna efetivada coincide com a do boletim em todas as seções, e o total oficial confere (T32, 0 votos de diferença).",
"T35": "Sem votos atribuíveis: 3 máquinas de geração de mídia (1º turno) e 2 (2º) sem log GEDAI publicado.",
"C01": "Descritivo: comparecimento 78,9% (1º turno) e 80,8% (2º); a diferença de 2,92 mi de votantes é o que o C06 tenta repartir.",
"C02": "Descritivo: distribuição dos votos por minuto; não altera totais.",
"C03": "Descritivo: associação entre perfil e voto; não se converte em votos trocados.",
"C06": "Estimativa de 3,18 mi de abstencionistas do 1º turno para Lula e 0,79 mi para o adversário (2026). Sob heterogeneidade contextual, o erro da célula chega a ±0,5 mi (estresse moderado) e ±1,5 mi (estresse forte). O ganho total de Lula entre turnos foi de 10,33 mi.",
"C06b": "Troca direta entre finalistas: mínimo garantido de 79 votos (Flávio → Lula) e 123 (Lula → Flávio); máximo matemático de ~40 milhões. Estimativa pontual: ~106 mil votos líquidos, dependente do C06.",
"C07": "Descritivo: idosos +3,2 pp e mulheres +3,3 pp de comparecimento por 100% do grupo; associação, não votos.",
"C08": "Mudança da diferença Lula − Flávio entre turnos: Sudeste +2,86 mi, Nordeste +2,56 mi, Sul +0,47 mi, Norte +0,46 mi, Centro-Oeste +0,30 mi (total 6,64 mi no país, sem exterior).",
"E01": "Não se traduz em votos: 33 a 36% da variância dos resíduos está entre locais de votação, como em 2022.",
"E02": "683 locais de votação significativos em 2026 (766 em 2022), lados equilibrados (390 × 293); sem soma de votos, por serem agrupamentos exploratórios.",
"E03": "Lista dos casos extremos; as divergências individuais são de dezenas a centenas de votos por seção; nenhuma confirmada em dado independente.",
"INC": "Define o menor efeito detectável (MDE) de cada teste; não é voto.",
"T36": "1º turno: 186 urnas com contas que não fecham, das quais só 9 têm log ≠ comparecimento, somando 59 votos (maior diferença 36). 2º turno: 75 urnas, 7 com diferença, somando 358 votos (maior 304). Os demais casos diferem em 1 confirmação sem voto computado. Total no máximo 417 votos em 128 mi.",
}
r = json.load(open(REG, encoding="utf-8"))
ids = {t["id"] for t in r["testes"]}
assert set(I) <= ids, (set(I) - ids)
for t in r["testes"]:
    if t["id"] in I: t["impacto_votos"] = I[t["id"]]
json.dump(r, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(I))
