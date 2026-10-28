# Fase 2 completa (28/10/2026)

Decisão do responsável: finalizar todas as perguntas da Fase 2 (P1 a P17). Pré-registro em [`fase2/sessao_limitada_2026-10-28/PREREG.md`](fase2/sessao_limitada_2026-10-28/PREREG.md) (seção "Fase 2 completa"), escrito antes das execuções. Código: `fase2/f2_completa.py <Pn>`. Resultados: `fase2/resultados/`. Cada resultado está nas `provas` do teste correspondente e no campo `impacto_votos`. Complementa o [`RELATORIO_SESSAO_LIMITADA.md`](RELATORIO_SESSAO_LIMITADA.md) (P1 e T37 a T39).

## Respostas, uma por pergunta
| P | Pergunta | Situação | O que ficou demonstrado | Em votos |
|---|---|---|---|---|
| P1 | O C06 resiste a taxas heterogêneas? | respondida | A magnitude "4:1" não; ordem e contraste 2022 × 2026 sim (T37) | erro de ±0,5 a ±1,5 mi na célula Abs→Lula, estimada em 3,18 mi |
| P2 | Poder do T13 nos dois sentidos | respondida | 10% dos válidos em 1% das urnas: 100% (Flávio→Lula) e 0% (Lula→Flávio); 2% e 5%: 0% nos dois. T1 e T3 só contam um lado | ~250 mil votos movidos não vistos no sentido contrário |
| P3 | Canal e versão de publicação | em parte | 200 de 200 concordam (BU, imagem, RDV, log, BU na Web); um canal só | 0 votos de diferença |
| P4 | Curva reconstruída por BUs | inventariada | sem capturas externas locais | n/a |
| P5 | Modelo de urna, mesmo município | respondida | equivalente a zero em ±0,02 logit | até ~2,7 mil votos se fosse real |
| P6 | Coleta externa de BUs | inventariada | sem material local; nada coletado | n/a |
| P7 | Urna trocada: equivalência | respondida | dentro de ±0,10 z nos dois anos | sem contagem |
| P8 | T03 por município | respondida | r = +0,004 e −0,028, ambos desprezíveis | sem contagem |
| P9 | E02 com ρ intralocal | em parte | de 766 para 102 locais (2022); de 1.140 para 55 (2026, sem perfil); Moran's I não feito | dezenas a centenas de votos por local |
| P10 | T28 beta-binomial | respondida | 8 das 13 urnas permanecem; 2022 tem 18 e 21 | 99 votos |
| P11 | Cadeia de certificados | em parte | 200 de 200 certificados de urna assinados pela AC emissora; âncora não verificada | n/a |
| P12 | Exterior −495 e −525 | respondida | 423 (41 seções não instaladas) + 72 (+30 no 2º turno) de seções só nos arquivos das urnas; resíduo 0 | eleitores, não votos |
| P13 | C06b em script | respondida | reproduz 79 e 123 | 79 e 123 votos (mínimos) |
| P14 | Causa da assimetria do T02 | respondida | 2022: 29 de 90 na capital de São Paulo, 8 locais repetidos (esperado 0,15); 2026 espalhado | ~740 e ~2.600 votos de excesso |
| P15 | Limites de Fréchet para o C06 | respondida | não identificam a razão (de ~0 a 1,7 mi) | 4,1 mil a 32,3 mi para Lula |
| P16 | 200 seções, comparador corrigido | respondida | 200 de 200; 14 falsas divergências do 1º ensaio eram erro do comparador | 0 votos |
| P17 | Assimetria do T02 com bootstrap | respondida | real nos dois anos (IC 95% > 0 a 3, 4 e 5 desvios) | idem P14 |

## Testes que mudaram de leitura (sem reescrever a V1.0)
- **E02:** de 766 (2022) e 683 (2026) locais para 102 e 55 depois de corrigir a correlação dentro do local. O agrupamento "significativo" era sobretudo correlação local.
- **T13:** passa a valer só para o sentido a favor de Lula; a detecção a 5% do original não se repete em mundo com ruído só binomial.
- **T28:** de 13 para 8 urnas no 1º turno, com padrão semelhante em 2022.
- **T32:** diferença do exterior explicada.
- **C06b:** passa a ter script que reproduz 79 e 123.
- **T02:** a assimetria é real, sem causa; em 2022 concentrada em São Paulo capital e em locais repetidos.
- **Resistiram:** T03, T04, T20, T14 a T17 (200 seções).

## Falhas e repetições
- P16: 1º ensaio acusou 14 divergências de imagem do BU por erro do comparador (campo ausente contra zero). Corrigido e repetido uma vez: 200 de 200.
- P2: biblioteca ausente (statsmodels) no 1º disparo; troquei por intervalo de Wilson próprio e repeti.
- P12: primeira versão comparava com o cadastro de julho, que não é a fonte; refeita com o total oficial.

## O que continua sem resposta (fila)
P18 T13 com as duas caudas; P19 Moran's I com adjacência do IBGE; P20 o que há nos locais de São Paulo em 2022; P21 boletins de terceiros e a cadeia AC URNA v2 → AC RAIZ UE por canal do TSE. As três primeiras são viáveis com dados e código locais; a P21 depende de fonte externa.

## Alcance
Tudo vale para os dados e os métodos descritos. Os resultados do P11 e do P16 se restringem à amostra do 1º turno de 2026 e a certificados de AC obtidos de repositório de terceiros. Nenhuma divergência objetiva nova indica alteração de votos; a ausência de achados não demonstra que toda alteração seria detectada.
