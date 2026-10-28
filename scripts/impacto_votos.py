"""Preenche testes[].impacto_votos no registro: quanto cada resultado representa em número de votos (ou por que não se traduz em votos).
Valores calculados em 28/10/2026 a partir dos resultados já existentes (referência: margem do 2º turno 2026 = 4.430.191 votos; 124.082.273 válidos)."""
import json, os
REG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "testes", "registro.json")
ZERO = "Zero votos de diferença nas comparações feitas; não há valor a converter."
I = {
"T01": "0 votos de diferença em 3.800.511 pares seção × votável (1º turno) e 1.931.103 (2º). Nenhum voto divergente entre as duas tabelas.",
"T02": "Excesso pró-Lula nas 33 seções acima de 5 desvios (2026): cerca de 740 votos; nas 13 pró-Flávio, cerca de 415 votos a menos para Lula. Em 2022: cerca de 2.600 e 350. Contra margem de 4,43 mi (2026): 0,017%. A assimetria é estatisticamente real (P17), mas somando tudo o que está nessas seções não muda o resultado.",
"T03": "Efeito desprezível: r = +0,004 (2026) e −0,028 (2022), com IC por município dentro de |r| ≤ 0,05. Nenhuma seção ou lote identificado; o teste não produz contagem de votos.",
"T04": "Diferença de −0,03 desvio-padrão por seção, equivalente a zero em ±0,10; nenhuma urna isolada sinalizada, sem contagem de votos.",
"T05": "Não se traduz em votos: teste de padrão de dígitos; nenhum conjunto de seções sinalizado (p de 0,05 a 0,84).",
"T07": "0 seções acima de 100% de comparecimento; 0 votos de enchimento por esta assinatura.",
"T08": "0 boletins emitidos antes do fim da votação depois da correção do fuso; 0 votos envolvidos.",
"T09": "Prorrogação em 6.748 seções (1,4% das 499 mil); virada de +7,45 e +7,56 pp nos dois grupos: diferença de 0,1 pp, sem efeito identificável em votos.",
"T10": "Desvio máximo da curva de 0,08 pp (município) e 0,25 a 0,32 pp (estado). Sobre 124 mi de votos válidos, 0,32 pp equivale a ~400 mil votos num instante da curva; é distância entre a curva e a reconstrução, não votos alterados.",
"T11": "Não se traduz em votos: conta oscilações da curva (23 contra 22 ± 1).",
"T12": "Efeito de −14,7 para +0,3 (t) depois de controlar a idade: sem efeito residual; nenhum voto atribuível à liberação sem biometria (12,7% das habilitações).",
"T13": "Menor alteração detectada na grade original: 11.677 votos movidos. Sentido correto (A2, 2026): troca dispersa de ~123 mil votos vista em 30 de 30; ~62 mil concentrados em locais ou municípios de até ~5 mil seções, 30 de 30 pelo E02; ~25 mil em nenhuma forma; troca no município inteiro das 5 maiores cidades não é vista com confiabilidade nem a 10% (155 mil a 696 mil votos). Votos simulados, não encontrados nos dados. Troca uniforme de 2,48 mi de votos não foi vista.",
"T13b": "Rajada convertendo 100% dos votos dos últimos 30 min em 'sem biometria' é vista em 76% a 98% das urnas alteradas; a 10% não é vista (recall ≈ 0%). As 13 urnas do 1º turno têm ≈140 votos no total.",
"T14": "0 votos de diferença entre log e comparecimento nas 200 seções sorteadas e nas urnas sem exceção; nas exceções documentadas (T36) a soma é 59 votos no 1º turno e 358 no 2º.",
"T15": ZERO,
"T16": "Não mede votos: mede se os bytes batem com a assinatura. 0 arquivos com hash ou assinatura divergente em 499.176 e 499.178 urnas.",
"T16c": "Não se traduz em votos: valida o verificador (300/300 legítimas aceitas; 0 aceitas nos 5 controles negativos).",
"T17": "0 votos de diferença entre a recontagem do RDV e o boletim em 499.176 urnas (1º turno).",
"T17b": ZERO,
"T19": "Mesmos números do T02 a T11 em 2022; ver cada teste.",
"T20": "Dentro de municípios com mais de um modelo, a maior diferença é +0,004 logit (UE2013, 2026), cerca de 2,7 mil votos nas 2,59 mi de votos válidas dessas urnas, se fosse real; equivalente a zero em ±0,02 logit.",
"T21": "Não se traduz em votos: |z| ≤ 1,6 nos dois anos, nenhum excesso de percentuais inteiros.",
"T22": "Não se traduz em votos: assinatura de fraude incremental simétrica (±0,08) e igual à de 2022 (±0,10).",
"T23": "Sensibilidade em fração de seções, não em votos: troca de 20% dos votos da seção é vista em 97% das seções alteradas; troca de 5%, em 7%. Seções reais marcadas: 0,35% das avaliadas, abaixo do 1% esperado.",
"T24": "Urnas substituídas registradas (ex.: MS 22); sem diferença de totais registrada (T32).",
"T25": "Não se traduz em votos: canto vazio e curtose 3,7 contra 4,1 (2022).",
"T26": "Não se traduz em votos: método inadequado, excluído da conclusão.",
"T27": "Não se traduz em votos: p = 0,57 e 0,34 no comparecimento.",
"T28": "2º turno: 0 urnas, 0 votos. 1º turno: 13 urnas pelo método original (≈140 votos) e 8 pelo beta-binomial (99 votos nos últimos 30 min, 93 sem biometria); 2022 tem 23 e 18. Perto de 0,0001% dos votos.",
"T29": "1.120.676 votos (0,9% do 2º turno) abaixo de 5 s entre habilitação e voto, em 273.451 urnas; padrão estrutural que se repete em 2022 (306.528), sem direção para candidato.",
"T30": "1 urna por turno com primeiro voto 2 a 4 min antes da abertura registrada (urna substituída); votos envolvidos: os da urna, sem diferença de totais.",
"T31": "2º turno: 0 votos. 1º turno: 2 votos em 1 urna (RJ 60011/8/61, log corrompido pela própria urna; totais e assinatura conferem).",
"T32": "0 votos de diferença em 638 itens de voto e comparecimento. A diferença do eleitorado do exterior (−495 e −525) está explicada: 423 eleitores de 41 seções não instaladas mais 72 (1º turno) e 102 (2º) de seções com boletim só nos arquivos das urnas; resíduo 0. São eleitores aptos, não votos.",
"T33": "Sem votos atribuíveis: mesma versão do software em todas as urnas; falhas de verificação de assinatura do software em 128 urnas (1º turno) e 162 (2º), sem diferença de totais.",
"T34": "3.060 seções com troca de urna declarada (0,6%); a urna efetivada coincide com a do boletim em todas as seções, e o total oficial confere (T32, 0 votos de diferença).",
"T35": "Sem votos atribuíveis: 3 máquinas de geração de mídia (1º turno) e 2 (2º) sem log GEDAI publicado.",
"C01": "Descritivo: comparecimento 78,9% (1º turno) e 80,8% (2º); a diferença de 2,92 mi de votantes é o que o C06 tenta repartir.",
"C02": "Descritivo: distribuição dos votos por minuto; não altera totais.",
"C03": "Descritivo: associação entre perfil e voto; não se converte em votos trocados.",
"C06": "Estimativa de 3,18 mi de abstencionistas do 1º turno para Lula e 0,79 mi para o adversário (2026). Sob heterogeneidade contextual, o erro da célula chega a ±0,5 mi (estresse moderado) e ±1,5 mi (estresse forte). O ganho total de Lula entre turnos foi de 10,33 mi.",
"C06b": "Troca direta entre finalistas: mínimo garantido de 79 votos (Flávio → Lula) e 123 (Lula → Flávio) e máximo matemático de ~43,5 e ~39,4 milhões. Para quem se absteve no 1º turno os limites por seção são de 4,1 mil a 32,3 mi para Lula: não identificam o fluxo.",
"C07": "Descritivo: idosos +3,2 pp e mulheres +3,3 pp de comparecimento por 100% do grupo; associação, não votos.",
"C08": "Mudança da diferença Lula − Flávio entre turnos: Sudeste +2,86 mi, Nordeste +2,56 mi, Sul +0,47 mi, Norte +0,46 mi, Centro-Oeste +0,30 mi (total 6,64 mi no país, sem exterior).",
"E01": "Não se traduz em votos: 33 a 36% da variância dos resíduos está entre locais de votação, como em 2022.",
"E02": "Depois de corrigir a correlação dentro do local: 55 locais significativos em 2026 (28 pró-Lula, 27 pró-adversário) e 102 em 2022 (30 e 72); cada local tem de dezenas a poucas centenas de votos de diferença, sem soma que se aproxime da margem de 4,43 mi.",
"E03": "Lista dos casos extremos; as divergências individuais são de dezenas a centenas de votos por seção; nenhuma confirmada em dado independente.",
"INC": "Define o menor efeito detectável (MDE) de cada teste; não é voto.",
"T40": "Margem final de 4,43 mi (2026, 2º turno) e 2,14 mi (2022). As inversões acontecem com menos de 10% dos votos apurados; a curva não altera o total.",
"T41": "2026, 2º turno: 106 seções com 14.860 válidos; o esperado para Flávio nelas vai de ~44 votos (modelo de local do E3) a ~3.100 (modelo da revisão I2), conforme o modelo: no máximo 0,07% da margem de 4,43 mi. 2022, 2º turno: 141 seções, 16.418 válidos, ~66 a ~3.000 votos esperados.",
"T44": "Salvador: ~30 mil votos de Lula acima do previsto (0,7% da margem de 4,43 mi). As outras 4 grandes cidades: Lula abaixo do previsto (−3 mil a −27 mil).",
"T43": "0 votos de diferença em 119,3 mi (2026) e em cerca de 118 mi por turno (2022) nas seções comuns; os 334 mil votos de seções só da base em 2022 não foram comparados.",
"T42": "Não se traduz em votos: mede dependência espacial dos resíduos de virada.",
"T36": "1º turno: 186 urnas com contas que não fecham, das quais só 9 têm log ≠ comparecimento, somando 59 votos (maior diferença 36). 2º turno: 75 urnas, 7 com diferença, somando 358 votos (maior 304). Os demais casos diferem em 1 confirmação sem voto computado. Total no máximo 417 votos em 128 mi.",
}
r = json.load(open(REG, encoding="utf-8"))
ids = {t["id"] for t in r["testes"]}
assert set(I) <= ids, (set(I) - ids)
for t in r["testes"]:
    if t["id"] in I: t["impacto_votos"] = I[t["id"]]
json.dump(r, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(I))
