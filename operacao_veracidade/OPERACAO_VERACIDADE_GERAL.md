# Operação Veracidade Geral: relatório executivo

Executada em 28/10/2026. A operação em si não publicou nem alterou o site, versões congeladas ou o `testes/registro.json`; a integração ao registro (T60a a T65), às Respostas (Q42 a Q50) e ao site, o congelamento (rodada 7, V1.5) e a publicação foram feitos depois, por decisão do responsável. Os documentos `00` a `09` detalham; os scripts e resultados estão em `scripts/` e `resultados/`; `REPRODUCAO.md` e `SHA256SUMS.txt` fecham a rastreabilidade.

**Pergunta da operação:** os dados oficiais usados pelo Urna Lab são fiéis ao que aconteceu? **Resposta direta: o que se pôde testar não mostra adulteração; o que não se pôde testar é exatamente a parte que responderia à pergunta.**

## Estado encontrado
As fases F4 a F7 **não existem**. O projeto tem F1, F2, F3, as alegações públicas (rodada 6, V1.4) e a rodada 7 só no registro vivo (T58 e T59, não congelada). Snapshots das rodadas 1 a 6 íntegros; no manifesto, só 331 de 51.883 arquivos têm hash oficial de download.

## O que foi feito (testes novos T60a a T64 e complementos)
1. **T60a, cadeia de certificados em 100% das urnas:** 1.942.246 pares seção × turno (2022 e 2026), **0 falhas**, todos válidos no dia, nenhum emitido depois da eleição, nenhuma chave repetida. A raiz do TSE não é pública.
2. **T60b, controles do verificador:** 0 falso positivo; 7 mutações rejeitadas em 40 de 40; 9 testes unitários do Ed521 passam; a assinatura do arquivo sozinha não detecta alteração (o hash detecta); um certificado sintético autoassinado passa pela verificação de lista e só a cadeia o rejeita.
3. **T61 e republicação, evidência de origem diferente:** 404 boletins impressos lidos por terceiros no 2º turno de 2026 (22 UFs, amostra de conveniência): assinatura, cadeia e votos iguais, 404 de 404; 404 de 404 arquivos `bu.dat` idênticos entre dois downloads independentes.
4. **T62, T63, experimento B (simulações adversariais):** 15 mecanismos, 2 sentidos, 7 magnitudes, 2 anos; registros coerentes assinados pelo próprio gerador **passam por todas as verificações internas**; um fabricante de estrutura completa passa D1 a D7 em 2026.
5. **T64, zeros:** três famílias de modelo falham; os zeros são locais de uma seção só com menos de 1% do total, nos dois anos.
6. Curvas, entre turnos, anomalias e logs, e a revisão de todas as perguntas e vereditos: `04` a `09`.
7. **T65, a hipótese do vídeo dos "98,12% dos votos extras"** (`10_HIPOTESE_DO_VIDEO.md`): a aritmética confere, mas o 98% é a premissa de 60% devolvida (o mínimo possível para a parcela dos outros que vai a Lula, e nenhum voto dos extras para Flávio); o mesmo método dá 370% para Bolsonaro em 2022; a abstenção também caiu em 2022; a regressão ecológica não apoia "todos os extras para Lula" (0,72 e 0,28). Resíduo real descrito: o candidato que mais cresceu recebeu mais que a divisão proporcional nos dois anos, em 27 de 27 UFs (+3,68 mi em 2026 e +1,99 mi em 2022).

## Principais achados novos
- **A cadeia de assinaturas fecha em 100%** (antes: 200 seções). Isso reforça a integridade dos arquivos e **não** a veracidade dos votos.
- **A bateria estatística tem pontos cegos maiores do que o veredito dizia:** UFs inteiras, os cinco grandes juntos, macrorregião, lote tardio, conversão de brancos e nulos, enchimento abaixo de 250 mil e deslocamento uniforme só são vistos a partir de 0,5 a 2,2 milhões de votos, ou nunca. O poder é **assimétrico entre os sentidos**.
- **A pausa de recebimento de 116 minutos (17:07 a 19:03) no 2º turno de 2026 é um fato medido**, só de 2026; 77 boletins de terceiros estavam registrados antes de o TSE registrar o recebimento. Não altera votos; a causa não está nos dados.
- **Um artefato do projeto:** o leitor de log conta eventos de logs de outras urnas e seções embutidos no pacote (ES 85: 612 eventos para 308 votos).

## Divergências objetivas
**Nenhuma divergência de votos entre fontes.** Lacunas documentais sem efeito em votos: 98 certificados emitidos depois da validade do certificado público da AC URNA (todos verificam com a chave publicada); certificado ≠ urna da tabela em 17 seções de 2026 e 22 de 2022, um caso com três identificações diferentes e votos iguais; a regra de emissão por modelo não é pública; a cadeia não chega à raiz.

## Hipóteses efetivamente contrariadas
Alteração depois da publicação entre versões do TSE (39 capturas, 404 arquivos iguais); troca na soma (638 de 638 itens iguais ao oficial, T32; reforçada pelos 404 boletins de terceiros); troca de dezenas de milhares de votos em seções, locais, zonas ou municípios (poder ≥ 80% a partir de 25 a 50 mil votos); certificado de urna não assinado por uma AC conhecida (nenhum em 1.942.246).

## Pontos cegos identificados ou confirmados
H9 (deslocamento uniforme em logit: nunca visto) e H10 (registros coerentes gerados antes da assinatura, T62); escala de UF, região e lote; zeros (sem modelo calibrado); curvas (sem modelo de chegada validado); raiz da cadeia de certificados; teste de integridade com votos conhecidos (resultado não obtido).

## Testes que falharam e os motivos
Os três modelos de zeros (critério fixado antes, falha por ordem de grandeza no município e por 50% a 75% de cobertura no local); o modelo de curvas (herdado, sem calibração); o fabricante de estrutura v1 (defeito de desenho meu, corrigido na v2); o estimador de fluxos C06 em 3 de 5 destinos de origem conhecida (T59, rodada 7).

## Respostas diretas

### 2022
1. **Divergências objetivas?** Nenhuma de votos. Lacunas documentais: 173 arquivos assinados ausentes do pacote (herdado), 22 seções com certificado de outra urna que a da tabela, 3 certificados em duas seções, 14 seções (1º turno) e 6 (2º turno) de urnas pré-2020 sem a ligação log-BU-RDV completa (T45, já catalogadas).
2. **Provado com evidência independente:** a versão publicada coincide com as capturas do Internet Archive; a decodificação de terceiro coincide em 99,96% das seções (independente na implementação). Não há boletins impressos de terceiros de 2022 neste estudo.
3. **Provado só por concordância interna:** hash e assinatura de todos os arquivos até a AC emissora (100% das urnas, T60a), BU = RDV = imagem = tabela, log.
4. **Mecanismos testados:** os 15 do T63 na base de 2022, T62, T60a e T60b, zeros (T64), curvas (herdado).
5. **Sem suporte, com cobertura e poder:** troca em seções, locais, zonas e municípios: sem alarme, com poder ≥ 80% a partir de 25 a 50 mil votos (pró-Lula, em seções dispersas, só a partir de 500 mil por assimetria da base).
6. **Anomalias sem causa:** zona 251 de São Paulo (~4,2 mil votos) e 259; cauda pró-Lula do T02 (90 seções, ~2.600 votos); 141 seções com zero para Bolsonaro, sem modelo calibrado; log ≠ comparecimento (5.287 votos sem registro e 2.503 a mais).
7. **Possível sem ser detectável:** H9 e H10; alterações regionais, de UF ou de lote abaixo de 0,5 a 2,2 mi; deslocamento uniforme em logit.
8. **Evidência positiva e reproduzível de manipulação?** **Não.**
9. **O que precisa mudar:** `09` (22 itens; destaques: H7, T05, "deixariam sinais muito maiores", Q5, "dois caminhos").
10. **Conclusão mais forte sustentável:** os dados oficiais de 2022 são internamente consistentes em todos os níveis testados, inclusive a cadeia de assinaturas até a AC em 100% das urnas, e não há evidência positiva de adulteração; a bateria tem poder medido contra vários mecanismos e é cega a outros; a hipótese de comprometimento antes dos registros não é testável com dados públicos.

### 2026
1. **Divergências objetivas?** Nenhuma de votos. Lacunas: 98 certificados emitidos depois da validade do certificado público da AC URNA; certificado ≠ urna da tabela em 17 seções (um caso com três identificações diferentes); pausa de recebimento de 116 minutos (fato, sem efeito no conteúdo).
2. **Provado com evidência independente:** 404 boletins impressos de terceiros iguais ao TSE, com assinatura e cadeia válidas (obtenção diferente, amostra de conveniência); 404 arquivos iguais entre downloads independentes; capturas do Internet Archive; 77 boletins registrados fora do TSE antes do recebimento do TSE.
3. **Só por concordância interna:** BU = RDV = imagem = tabela; assinaturas e cadeia até a AC emissora (100% das urnas); log.
4. **Mecanismos testados:** os 15 do T63 em 2026, T62, T60a e T60b, T61, zeros (T64), fluxos e brancos e nulos (T56 a T59).
5. **Sem suporte, com poder:** os mesmos de 2022, com limiares de 25 a 50 mil votos para seções, locais, zonas e municípios.
6. **Anomalias sem causa:** Salvador (~30 mil votos, no limiar de detecção); 33 seções do T02 (~773 votos); 106 seções com zero para Flávio sem modelo calibrado; rajadas sem biometria (99 votos); 17 seções com certificado de outra urna.
7. **Possível sem ser detectável:** H9 e H10 (registros coerentes assinados pelo gerador passam por todas as verificações internas); alterações de escala regional, de UF ou de lote abaixo de 0,5 a 2,2 mi; um fabricante de estrutura completa passou D1 a D7 em 2026.
8. **Evidência positiva e reproduzível de manipulação?** **Não.**
9. **O que precisa mudar:** `09`.
10. **Conclusão mais forte sustentável:** não encontramos sinal de fraude nos mecanismos que os dados públicos conseguem examinar, e a evidência de origem diferente (404 boletins) concorda; mas a evidência é de conveniência e pequena, vários mecanismos só seriam vistos em centenas de milhares a milhões de votos, e o comprometimento anterior ao registro não é distinguível com dados públicos.

## Resposta em linguagem comum (≤ 200 palavras)
**Os dados oficiais usados pelo Urna Lab foram adulterados?** Não encontramos adulteração, mas não provamos que não houve. **Observado:** os arquivos que o TSE publicou concordam entre si; as assinaturas de todas as urnas de 2022 e 2026 verificam até a autoridade certificadora; 404 boletins impressos lidos por cidadãos em 2026 batem com o TSE, sem diferença de votos; e os arquivos não mudaram entre downloads. **Excluído:** alterações de dezenas de milhares de votos em seções, locais, zonas ou municípios deixariam sinal, e não há. **Sem resposta:** alterações em escala de estado, região ou uniformes passariam sem alarme até centenas de milhares de votos; e qualquer manipulação na urna antes de gerar os registros produz dados coerentes que nenhuma conferência interna distingue. Ficam também 106 seções com zero voto para Flávio (141 para Bolsonaro em 2022) e algumas anomalias pequenas sem causa. **O que faltaria:** boletins impressos de uma amostra sorteada de seções, auditoria independente do software da urna e a raiz da cadeia de certificados, que não é pública.

## Evidências produzidas
Ver `SHA256SUMS.txt` (todos os arquivos desta pasta com hash). Documentos: `00`, `01`, `02`, `03`, `04`, `05`, `06`, `07`, `08`, `09`, `10`, `PROTOCOLO_PRE_EXECUCAO.md`, `REPRODUCAO.md`, `RECOMENDACOES_SITE.md`. Dados externos baixados: `externo/arvor_totalizacao/` (com SHA-256 e data).
