# Operação Veracidade Geral

**Versão:** V1.5 · **Situação:** concluída · **Início:** 2026-10-28

## Resumo

Rodada 7 (V1.5), 28/10/2026: auditoria adversarial dos dados e do próprio veredito. Pergunta: os dados oficiais usados pelo estudo são fiéis ao que aconteceu? O que se pôde testar não mostra adulteração; o que não se pôde testar é exatamente a parte que responderia à pergunta. A cadeia de certificados verifica em 100% das urnas de 2022 e 2026 (1.942.246 pares seção × turno, 0 falhas); 404 boletins impressos lidos por terceiros no 2º turno de 2026 são iguais ao TSE (amostra de conveniência, 0,08%). As simulações adversariais mostram pontos cegos maiores do que o veredito dizia: UFs, região, lote e deslocamento uniforme só são vistos a partir de ~0,5 a 2,2 milhões de votos, ou nunca, e registros coerentes gerados pela própria fonte passam em todas as verificações internas. Testes T60a a T65, perguntas Q42 a Q50 (com T58, T59, Q40 e Q41 da mesma rodada). A resposta central fica mais estreita: não encontramos sinal nos mecanismos que os dados públicos conseguem examinar, com o poder medido.

## O que foi feito

1. **Pré-registro da operação.** Protocolo e emendas 1 a 4 escritos antes de ver os resultados da grade (operacao_veracidade/PROTOCOLO_PRE_EXECUCAO.md).
2. **Cadeia de certificados (T60a, T60b).** 1.942.246 de 1.942.246 certificados verificam até a AC emissora; o verificador rejeita 7 mutações em 40 de 40 e não rejeita nenhum arquivo genuíno.
3. **Boletins de terceiros (T61).** 404 de 404 iguais à tabela e ao BU do TSE, com assinatura e cadeia válidas; 404 arquivos iguais entre downloads independentes.
4. **Simulações adversariais (T62, T63).** 15 mecanismos, 2 sentidos, 7 magnitudes e 2 anos: o que a bateria vê, a partir de quantos votos, e o que passa sem alarme.
5. **Zeros (T64) e a conta do vídeo (T65).** Três famílias de modelo de zeros falham a calibração; o '98,12% dos votos extras' é a premissa devolvida e o mesmo método dá 370% em 2022.
6. **Impacto nos vereditos.** 22 afirmações confrontadas: 10 preservadas ou reforçadas, 6 enfraquecidas, 2 refutadas como redigidas (H7 e T05), 1 superada, 1 não avaliável (operacao_veracidade/09).

## Onde está o detalhe

- [`operacao_veracidade/OPERACAO_VERACIDADE_GERAL.md`](../operacao_veracidade/OPERACAO_VERACIDADE_GERAL.md)
- [`operacao_veracidade/REPRODUCAO.md`](../operacao_veracidade/REPRODUCAO.md)

Nada aqui afirma nem nega fraude além do que os números sustentam.
