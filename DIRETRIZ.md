# Diretriz científica permanente

**Origem:** recebida do responsável pelo estudo em 27/10/2026, 20h30, e incorporada sem interromper os trabalhos em andamento. É a referência metodológica de nível mais alto do projeto. O `PROTOCOLO.md` operacionaliza esta diretriz; o `AGENTS.md` a resume para os agentes.

## 1. Pergunta do estudo
A pergunta inicial ("houve fraude?") evoluiu para:

> **Quais padrões, regularidades, anomalias e divergências podem ser identificados nos dados eleitorais brasileiros (2022 e 2026), quais explicações científicas existem para eles e quais hipóteses resistem a uma investigação rigorosa?**

O projeto não tem como objetivo provar fraude, nem provar a ausência de fraude, nem defender ou contestar o sistema eleitoral. O compromisso é com evidência, método, transparência e reprodutibilidade. Qualquer conclusão é admissível se for proporcional às evidências, inclusive "os dados não bastam para responder".

**A pergunta "houve fraude?" continua sendo respondida no final,** nos termos da classificação da seção 4: o que foi demonstrado, o que é evidência, o que é inconclusivo e o que está fora do alcance dos dados.

## 2. Princípios para quem conduz (pessoa ou agente)
1. Não presumir que houve fraude.
2. Não presumir que fraude seria impossível.
3. Anomalia estatística não é fraude.
4. Não descartar anomalia por contrariar expectativas.
5. Buscar explicações alternativas para todo resultado incomum.
6. Não selecionar resultados para favorecer candidato, partido ou conclusão.
7. Separar observação, hipótese, evidência, interpretação e conclusão.
8. Declarar limitações, vieses e pressupostos de cada método.
9. Registrar resultados negativos, positivos e inconclusivos.
10. Ausência de evidência não é demonstração de inexistência.
11. Significância estatística não é relevância prática nem evidência de manipulação.
12. Não afirmar fraude demonstrada sem evidência específica suficiente.

Imparcialidade não exige dar a mesma plausibilidade a todas as hipóteses; exige avaliá-las com critérios consistentes e evidências verificáveis.

## 3. Os cinco níveis da investigação (e onde estão no projeto)
| Nível | Conteúdo | No projeto |
|---|---|---|
| 1. Integridade e reconstrução dos dados | Originais e hashes; proveniência; formatos, chaves, completude; duplicidades; reconciliação de totais; **distinguir consistência entre arquivos oficiais de verificação independente** | Módulo A; T01, T14–T17b, T24, T30–T35; `dados/MANIFESTO.csv` (proveniência) |
| 2. Descoberta de padrões | Distribuições, correlações, território, tempo; comparecimento, brancos/nulos; 2022 × 2026 respeitando diferenças | Módulos B e C; C01–C08; T09; logs (C02) |
| 3. Investigação de anomalias | Para cada uma: descrever; erro de ingestão?; método apropriado?; geografia/demografia/confusão; alternativas; sensibilidade; persiste após controles?; que evidência distinguiria as hipóteses | Módulo E; CATALOGO, seção 4 (artefatos); E01–E03 |
| 4. Validação e refutação | Caminhos independentes; métodos complementares; simulações; falsos positivos/negativos; poder; FDR; dependência entre testes; falácia ecológica, Simpson; exploratório × confirmatório; validação em dados não usados na descoberta | T13/T13b (poder); 2022 (especificidade); BH; holdout (seção 6) |
| 5. Conclusão e documentação | Para cada resultado: observação, hipótese, método e referência, unidade e dados, controles, resultado, efeito e incerteza, alternativas, limitações, reprodução | Ficha de resultado (seção 5); relatório |

## 4. Classificação das evidências (substitui o binário "fraude / sem fraude")
| Classe | Significado |
|---|---|
| **A. Regularidade observada** | Padrão descritivo presente nos dados |
| **B. Anomalia estatística** | Incomum segundo um modelo específico, sem causa demonstrada |
| **C. Anomalia robusta** | Persiste após verificações, controles e sensibilidade |
| **D. Inconsistência verificável** | Divergência objetiva entre dados ou registros, de origem a investigar |
| **E. Evidência de possível irregularidade** | Achado com elementos específicos que justificam investigação adicional |
| **F. Evidência de manipulação** | Documentação ou resultados independentes, específicos o bastante para sustentar uma hipótese de intervenção, com alcance e limites explícitos |
| **G. Resultado inconclusivo** | Dados ou métodos insuficientes para distinguir hipóteses |

**Não é uma escada.** Uma anomalia robusta não vira evidência de manipulação só por ser muito significativa.

**Como se combina com a força das afirmações** (AUTOAUDITORIA): cada resultado recebe uma classe (A–G) e um tipo de afirmação:
1. verificação determinística (conta exata ou criptografia);
2. evidência estatística (com poder medido);
3. fora do alcance dos dados públicos.

E também a **independência da verificação:**
- **interna:** coerência entre arquivos oficiais da mesma origem, por exemplo BU × votação por seção × total divulgado;
- **criptográfica:** conferível por qualquer pessoa com matemática pública e a chave da urna, mas que ainda depende do software da urna;
- **externa:** fonte fora do TSE, como observação, teste de integridade com cédulas ou dados de terceiros.

## 5. Ficha de resultado (obrigatória para resultados relevantes)
Cada resultado relevante no relatório e no `testes/registro.json` traz:
- **observação:** o que foi visto;
- **hipótese testada;**
- **método e referência;**
- **unidade de análise e dados** (população, ano, turno, filtros);
- **controles;**
- **resultado, tamanho do efeito e incerteza;**
- **classe A–G, tipo de afirmação e independência;**
- **natureza:** exploratório ou confirmatório;
- **explicações alternativas** que permanecem;
- **limitações;**
- **como reproduzir** (comando, semente, parâmetros).

## 6. Exploratório × confirmatório
- **Exploratório:** padrão encontrado olhando os dados. Exemplos: as maiores divergências do módulo E; o resíduo positivo de quem não votou no 1º turno.
- **Confirmatório:** hipótese fixada antes e testada em dados **não usados para descobri-la**.

Neste estudo, as fontes de confirmação são:
- os arquivos das urnas (logs, assinaturas, RDV), independentes das tabelas de votação onde os padrões foram descobertos;
- 2022, para padrões descobertos em 2026, e vice-versa;
- metades aleatórias de municípios, com semente fixa, para padrões territoriais.

Um achado exploratório só sobe de classe (B → C) depois de confirmado assim.

## 7. Proteção contra viés de confirmação (perguntas obrigatórias antes de interpretar)
1. Que explicações naturais produziriam o resultado?
2. Pode ser acaso ou excesso de comparações?
3. O método detectaria manipulação se ela existisse (poder)?
4. O teste falha com dado legítimo (especificidade)?
5. Depende de decisão arbitrária de pré-processamento (sensibilidade)?
6. Reproduz em outros recortes?
7. Distingue de fato as hipóteses concorrentes?
8. Que evidência faria abandonar a interpretação atual?

## 8. Arquitetura (três camadas)
- **Dados:** obtenção, preservação, proveniência e integridade (`scripts/`, `dados/`, `dados/MANIFESTO.csv`).
- **Científica:** cálculos determinísticos e testes por código (`analise/`, `grafico/`, `testes/registro.json`, `Makefile`). **A fonte de verdade dos números é o código, nunca o texto de um agente.**
- **Agêntica:** hipóteses, investigação, explicações alternativas, documentação e relatórios (`AGENTS.md`, `.agents/skills/`).

A reprodução não depende de modelo de IA específico. Dependências, versões, sementes, parâmetros e comandos ficam documentados. Mudanças de método ficam em emendas datadas (PROTOCOLO, seção 8), nunca silenciosas.

## 9. Produtos possíveis
Não precisa haver uma resposta única. Os produtos podem ser:
- uma base eleitoral validada e reproduzível;
- métodos de auditoria estatística;
- um catálogo de padrões e anomalias;
- um estudo dos limites das técnicas de detecção;
- um sistema aberto de investigação assistida por agentes;
- evidências que confirmem, enfraqueçam ou deixem inconclusivas hipóteses específicas.

## Princípio central
Não procure uma conclusão: procure explicações testáveis. Não force os dados a responder o que não conseguem. Não ignore o inesperado: investigue. Não confunda suspeita, correlação, anomalia, inconsistência e prova. Permita que qualquer pessoa reproduza e tente refutar.
