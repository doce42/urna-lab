# 10. A hipótese do vídeo dos "98,12% dos votos extras" (T65)

Origem: transcrição de um vídeo de 90 s, usada **só como origem da pergunta**. Pré-registro em `PROTOCOLO_PRE_EXECUCAO.md` (T65 e M6). Script: `scripts/hipotese_video.py` e `hipotese_video_m6.py`. Saídas: `resultados/hipotese_video.json` e `hipotese_video_m6.json`.

## 1. O que o vídeo afirma
(a) 1º turno: Flávio 56,1 mi, Lula 53,8 mi, outros 9,3 mi. (b) A abstenção caiu ~3 mi e os brancos e nulos 1,8 mi; a soma, 4,8 mi, são os "votos extras". (c) Lula ganhou 10,3 mi. (d) Simulação: os finalistas repetem o voto e 60% dos outros vão a Lula (~5,5 mi); faltariam 4,7 mi, que são **98,12% dos extras**. (e) "Nunca aconteceu" a abstenção cair entre turnos. (f) Sugestão: a conta não fecha.

## 2. O que a base confere (M1)
Os números do vídeo estão **certos**: outros 9.321.993; queda de abstenção (aumento de comparecimento) 2.960.239; queda de brancos e nulos 1.816.000; extras 4.776.239; ganho de Lula 10.376.694. Com 60% dos outros (5.593.196), faltam 4.783.498, que são **100,15%** dos extras com os números exatos (os 98,12% vêm do arredondamento do vídeo). **A aritmética está correta; o que ela significa é o ponto.**

## 3. Por que o "98%" não é um achado: ele é a premissa devolvida (M1 e M2)
- Os 60% dos outros para Lula significam 40% para Flávio: **3.728.797 votos, praticamente o ganho real de Flávio (3.721.538)**. A simulação do vídeo atribui **todo** o ganho de Flávio aos "outros" e, portanto, **nada** dos extras a Flávio. Então, por construção, tudo o que sobra para Lula é 100% dos extras.
- Como Lula e Flávio ganharam 14.098.232 votos no total, que é exatamente os outros mais os extras (identidade exata, diferença 0), existe uma família de resultados, não um resultado. A fração dos extras que iria a Lula é função da parcela *s* dos outros que vai a Lula:

| Parcela dos outros que vai a Lula | Fração dos extras que vai a Lula | Ganho de Flávio (confere) |
|---|---|---|
| 60% (o vídeo) | **100%** | 3.721.538 |
| 70% | 81% | 3.721.538 |
| 75% | 71% | 3.721.538 |
| 80% | 61% | 3.721.538 |
| **85%** | **51%** (≈ o resultado final do 2º turno, 51,8%) | 3.721.538 |
| 90% | 42% | 3.721.538 |
| 100% | 22% | 3.721.538 |

- **60,08% é o mínimo possível** para a parcela dos outros que vai a Lula (abaixo disso a fração dos extras passa de 100%). O vídeo escolheu o piso e concluiu que os extras tiveram que ir todos a Lula. Qualquer parcela maior dos outros reparte os extras. Os dados agregados não dizem qual é (Q24, Q26).

## 4. O mesmo método em 2022 não discrimina (M3)
Para o candidato que mais cresceu em 2022 (Bolsonaro, +7.134.009), com os mesmos 60% dos outros (9.897.870 → 5.938.722), faltam 1.195.287; os extras de 2022 são só 322.634 (comparecimento +570.424 menos o aumento de 247.790 em brancos e nulos). **A fração é 370%: impossível sob as premissas do vídeo.** Isto é, o método "acusaria" 2022 de modo ainda mais forte, e em 2022 nenhuma suspeita foi formulada com esse número. A parcela mínima dos outros que teria de ir a Bolsonaro em 2022 era **68,8%**, maior que os 60,1% de Lula em 2026.

## 5. "Nunca aconteceu" (M4)
Na base do projeto, a abstenção também caiu entre turnos em 2022 (20,95% → 20,58%; 570.424 votantes a mais) e em 2026 (21,08% → 19,22%; 2.960.239 a mais). **A queda de 2026 é maior (1,86 ponto contra 0,36), mas não é inédita dentro do projeto.** Eleições anteriores a 2022 **não estão no projeto**, então a afirmação de que "nunca antes aconteceu" não é testável aqui além de 2022; não foi verificada por fonte externa.

## 6. O que os dados dizem sobre a divisão dos extras (M5, associação ecológica)
Regressão por município (5.571; pesos por aptos; efeito fixo de UF; IC por bootstrap de municípios). **Associação, não comportamento individual** (T37 e T59 mostram que o estimador ecológico acerta alguns grupos e erra outros):

| | Eliminados → | Extras → |
|---|---|---|
| 2026, Lula | 0,61 (IC 0,58 a 0,65) | **0,72** (0,69 a 0,80) |
| 2026, Flávio | 0,39 (0,35 a 0,42) | **0,28 (0,20 a 0,31)** |
| 2022, Bolsonaro | 0,51 (0,47 a 0,56) | 0,53 (0,49 a 0,55) |
| 2022, Lula | 0,49 (0,44 a 0,53) | 0,47 (0,45 a 0,51) |

Pela leitura fixada antes: **o coeficiente dos extras para Flávio em 2026 é claramente maior que zero (IC 0,20 a 0,31), então a hipótese "todos os extras foram para Lula" não tem apoio nem no nível ecológico.** A associação é de ~72% a favor de Lula em 2026, contra um quase empate (47% e 53%) em 2022.

## 7. O que sobra depois de descontar a geografia (M6, exploratório)
Dividindo, em cada município, os votos dos eliminados e os extras entre os finalistas **na proporção do 1º turno entre eles** (hipótese nula proporcional), os extras iriam 50,2% a Lula (os eliminados, 46,1%). O ganho previsto de Lula seria 6,66 mi; o observado foi 10,33 mi.

| | Ganho observado do candidato que mais subiu | Previsto na hipótese proporcional | Resíduo | % do disponível | UFs com resíduo no mesmo sentido |
|---|---|---|---|---|---|
| 2026, Lula | 10,33 mi | 6,66 mi | **+3,68 mi** | **26,2%** de 14,03 mi | 27 de 27 |
| 2022, Bolsonaro | 7,11 mi | 5,12 mi | **+1,99 mi** | **19,6%** de 10,18 mi | 27 de 27 |

**Este é o resíduo real: nos dois anos, o candidato que mais cresceu entre os turnos recebeu mais do que a divisão proporcional daria, em todas as UFs, e em 2026 a diferença é maior (26,2% contra 19,6% do disponível).** A forma do fenômeno é a mesma de 2022; a escala é maior.

## 8. Composição dos "extras" (resultados já registrados)
Os 1,82 mi de queda de brancos e nulos não são "novos votantes": são pessoas que já votaram e cujo voto passou a valer. Parte tem causa estrutural medida: ~0,47 mi com marca no 1º turno e ~0,69 mi por haver menos 2º turno de governador (8% dos votos em 2026 contra 53% em 2022; erro de campo com número de governador, 698 mil nulos no 1º turno de 2026) (T56 a T58). Isso muda o que "extras" significa, mas o vídeo trata brancos e nulos como eleitores que "foram votar".

## 9. Conclusão
1. **A aritmética do vídeo está certa e a conclusão não segue dela.** O "98,12%" é a premissa de 60% devolvida: o mínimo possível para a parcela dos outros e nenhum ganho de Flávio vindo dos extras.
2. **Sob outras premissas, igualmente compatíveis com os totais,** os extras se repartem (51% para Lula se 85% dos outros foram a Lula).
3. **O mesmo método dá 370% para Bolsonaro em 2022.** Não discrimina.
4. **"Nunca aconteceu" não vale dentro do projeto:** a abstenção caiu em 2022 também (menos). Anos anteriores não foram testados.
5. **Nenhuma conclusão sobre fraude se tira disso.** Agregados e voto secreto não identificam transferência individual (Q26).
6. **O que é real e fica registrado:** o candidato que mais cresceu recebeu mais que a divisão proporcional nos dois anos, em todas as UFs, e em 2026 mais do que em 2022 (+3,68 mi, 26,2% do disponível, contra +1,99 mi, 19,6%). É um fenômeno de sinal conhecido, de escala maior, sem causa demonstrada e que os dados públicos não resolvem.
