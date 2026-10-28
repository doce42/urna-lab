# Conclusão do estudo

**Data:** 28/10/2026. **Escopo:** eleição presidencial brasileira de 2026, 1º turno (04/10) e 2º turno (25/10), com 2022 como referência. **Fonte:** só dados oficiais do TSE: tabelas de dados abertos e os arquivos gravados por cada urna (boletim `bu.dat`, registro digital do voto `RDV`, log, imagem do boletim e assinaturas), cerca de 405 GB e 51.846 arquivos com SHA-256 no manifesto.

Esta conclusão responde à pergunta "houve fraude?" só nos termos que a [DIRETRIZ](DIRETRIZ.md) permite: **o que foi demonstrado**, **o que a estatística mostra e com que poder**, e **o que os dados públicos não alcançam**. Ela foi escrita depois de todos os testes registrados terem rodado e de dois erros de leitura do próprio estudo terem sido achados e corrigidos (ver [CATALOGO](CATALOGO.md)). Cada afirmação aponta para o teste do [registro](testes/registro.json) que a sustenta.

## Resposta curta

Dentro do que os dados públicos permitem verificar, **não foi encontrada evidência de manipulação** nos resultados presidenciais de 2026. Nenhum teste chegou às classes E (evidência de possível irregularidade) ou F (evidência de manipulação).

- **Demonstrado:** o resultado publicado é exatamente o que as urnas gravaram e assinaram. A recontagem de cada urna pelo registro dos votos dá o mesmo boletim.
- **Estatística:** as fraudes que os testes conseguiriam ver não aparecem. O tamanho do que eles veem foi medido.
- **Fora do alcance:** uma alteração no software, igual em todas as urnas, que produzisse arquivos coerentes e assinados não deixaria rastro nestes dados. Este estudo **não** consegue excluir esse tipo de fraude, e nenhum estudo feito só com dados públicos consegue.

## 1. Prova determinística (conta exata e criptografia, sem amostra)

| O que foi conferido | 1º turno | 2º turno | Teste |
|---|---|---|---|
| Boletim de Urna = votação por seção, voto a voto | igual | igual | T01 |
| Soma das urnas = total oficial divulgado | 638 de 638 itens iguais (os dois turnos juntos) | | T32 |
| Assinatura digital e hash válidos (BU, log e lista de arquivos) | todas as 499.176 urnas eletrônicas | todas as 499.178 | T14, T16 |
| Recontagem pelo RDV = boletim | 499.176 | 499.180 (inclui recuperação de dados) | T17 |
| `bu.dat` (o que é somado) = RDV = publicado | todas as urnas eletrônicas | todas | T17b |
| Urna usada = urna do boletim no cadastro de correspondências | 499.206 de 499.206 | 499.205 de 499.205 | T34 |
| Contas de integridade que não fecham exatamente | 186 casos: 185 com explicação operacional e 1 sem (log corrompido pela urna, votos íntegros) | 75 casos: 74 explicados e 1 inconsistência de publicação | T36 |

A verificação de assinatura foi testada contra controles negativos: 300 de 300 assinaturas legítimas aceitas e 0 aceitas nos 5 controles adulterados (T16c). Os casos sem explicação operacional completa são três, e nenhum altera votos:

- **RJ 60011/8/61 (1º turno):** a própria urna gravou linhas corrompidas no log. O hash do arquivo, a assinatura e os totais conferem, e as 2 "confirmações sem habilitação" do T31 vêm daí.
- **SP, 2º turno (D1):** o log de 1 urna está na lista assinada pela urna mas não foi publicado no pacote do TSE. É uma inconsistência de publicação, não de contagem.
- **MA 7846/74/228 (1º turno):** o RDV faltava no pacote. Foi baixado do site de resultados e verificado (hash, assinatura, Lula 158 votos = publicado).

**O que isso prova:** do momento em que cada urna fechou e assinou seus arquivos até o total divulgado, não houve alteração. O resultado publicado é a soma fiel do que as urnas registraram.
**O que isso não prova:** que a urna registrou corretamente o que cada eleitor digitou. Isso depende do software, que não se audita com arquivos de saída (nível 3).

## 2. Evidência estatística, com poder medido

**Nada do que se esperaria de uma fraude localizada apareceu:**
- A virada entre turnos não depende da hora em que o boletim chegou ao TSE (T03, efeito desprezível, 2022 igual).
- Urnas trocadas entre turnos votaram igual às demais (T04).
- Não há padrões de dígitos manipulados (T05, T21, T27).
- Não há assinatura de enchimento de urna (T07, T25) nem de fraude incremental (T22).
- A curva da apuração seguiu a prevista pelo histórico de cada município, com desvio máximo de 0,08 ponto percentual depois das 19h (T10, T11).
- Nenhum voto depois do encerramento da própria urna; os 2 votos antes da abertura (1 urna por turno) são de urnas substituídas antes do primeiro voto (T30).
- O software de votação foi o mesmo em todas as urnas (T33).
- O agrupamento das divergências é local, com lados equilibrados, como em 2022 (E01, E02).

**Anomalias estatísticas registradas (classe B, exploratórias, sem prova de causa):**
- **T02:** 46 seções de 499 mil se afastaram mais de 5 desvios das vizinhas (33 pró-Lula, 13 pró-Flávio), contra cerca de 17 esperadas. O excesso na cauda pró-Lula também existe em 2022 (90 contra 36 esperadas), em outra eleição e com outro vencedor. Nos logs, essas seções não diferem das demais em biometria, tempo de voto ou troca de urna.
- **T28, 1º turno:** 13 urnas com mais habilitações sem biometria nos últimos 30 minutos do que a própria urna teve no resto do dia. São de 6 a 14 casos cada, cerca de 140 votos no total, em 7 estados e sem direção de voto. Em 2022 foram 23 e 25 urnas. No 2º turno de 2026, nenhuma.
- **T26 (2º dígito de Benford):** rejeita nos dois anos e para os dois candidatos. Por acusar tudo, inclusive 2022 e os dois lados, foi tratado como método inadequado para este dado e excluído da conclusão.

**Poder (o que os testes teriam visto, medido com fraude simulada sobre os dados reais, T13, T23, T13b):**
- **Margem:** 4.429.831 votos. Inverter o resultado exigiria trocar cerca de 2,2 milhões de votos.
- **Fraudes não uniformes:** de 37 cenários simulados, 25 foram detectados. Entre os cenários não uniformes (urnas sorteadas, estados inteiros, enchimento), todos os que moviam mais de 500 mil votos foram detectados. O maior que passou despercebido moveu 496.895 votos (2% dos válidos em 20% das urnas), cerca de 22% do necessário para inverter.
- **Troca uniforme nacional:** nenhum dos 3 cenários foi detectado, nem o de 2% dos válidos em todas as urnas, que basta para inverter. É o limite estrutural da estatística entre seções.
- **Teste de rajada no fim do dia (T28):** só detecta conversões grandes e concentradas. Com 10% dos votos dos últimos 30 minutos alterados, detecta quase nada.

**O que isso permite dizer:** uma fraude localizada (em urnas escolhidas, em estados, por enchimento) grande o bastante para mudar o vencedor teria muito provavelmente aparecido, e não apareceu. Uma fraude espalhada por igual no país inteiro não seria vista por estes testes.

## 3. Limites dos dados públicos

Estes pontos ficam fora do alcance do estudo e estão detalhados em [AUTOAUDITORIA §6](AUTOAUDITORIA.md):

- **Software da urna:** só se vê o que a urna gravou, não o que ela executou. Uma alteração no software igual em todas as urnas, que gere arquivos coerentes e assinados, passaria por todos os testes deste estudo. A versão do software é a mesma em todas as urnas (T33), mas o conteúdo dela não é auditável aqui.
- **Cadeia de certificados até a raiz do TSE:** não está publicada. A assinatura foi conferida contra o certificado declarado por cada urna.
- **Especificação de 2026:** a especificação oficial obtida é a de 2022. A estrutura confere com os leitores; o formato de 2026 traz campos novos e foi validado pelos totais, não por especificação.
- **3 máquinas de carga sem log do GEDAI publicado (T35):** registrado como ausência de dado, sem inferência.
- **Voto individual:** secreto por desenho; nenhum arquivo liga eleitor a voto.
- **Comportamento do eleitor:** as estimativas de transferência de votos entre turnos (C06, C06b) são inferência ecológica. Elas descrevem padrões ("abstencionistas do 1º turno foram 4:1 para Lula") mas não identificam quem trocou de candidato.
- **Reprodução a partir de clone limpo:** não foi executada ponta a ponta. Os comandos estão no `Makefile` e no [AGENTS.md](AGENTS.md).

## Erros do próprio estudo (transparência)

Dois erros de leitura foram cometidos e corrigidos antes desta conclusão. Ambos estão documentados com data no [CATALOGO](CATALOGO.md):
1. O leitor de log contava duas vezes linhas repetidas entre partes de um log.
2. O leitor do `bu.dat` só achava a eleição de Presidente quando ela vinha primeiro na lista. Isso criou 757 "casos sem explicação" falsos, que sumiram com a correção.

Nenhum dos dois afetava assinaturas, RDV ou totais. Os resultados antigos estão preservados para comparação. Todos os achados anteriores que dependiam dessas leituras foram refeitos.

## Como discordar

Tudo é reproduzível: código MIT, documentos CC BY 4.0, comandos no `Makefile`. Uma discordância metodológica, um teste novo ou um erro encontrado entram por fork e pull request (ver [CONTRIBUTING](CONTRIBUTING.md)). Um teste que contradiga esta conclusão será registrado com o mesmo peso dos demais.
