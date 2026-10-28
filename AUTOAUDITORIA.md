# Autoauditoria do plano de testes

**Data:** 27/10/2026, 20h20.

**Pergunta:** o plano, com os testes e a metodologia escolhidos, chega a um resultado irrefutável e completo?

**Resposta curta:** em parte, e é preciso dizer exatamente qual parte. O estudo produz três tipos de afirmação, com força diferente:

| Tipo | Natureza | Força | Exemplos |
|---|---|---|---|
| **1. Prova determinística** | Conta exata ou verificação criptográfica sobre os dados públicos | **Irrefutável**, dentro do que os arquivos contêm: qualquer pessoa repete e chega ao mesmo número | Assinatura de cada urna válida; hash dos arquivos = lista assinada; RDV recontado = boletim; soma dos boletins = total oficial; log = comparecimento |
| **2. Evidência estatística** | Comparação com um modelo do comportamento esperado | **Probabilística:** diz que não há padrão acima de um tamanho detectável, com o tamanho medido pelo teste de poder | Seções fora do padrão, curva × prevista, impressão digital, dígitos, percentuais inteiros |
| **3. Fora do alcance dos dados públicos** | Não aparece em nenhum arquivo publicado | **Nenhuma:** o estudo só pode declarar o limite | Software da urna contando errado e assinando o erro; troca uniforme no país inteiro |

**Conclusão da autoauditoria:** o estudo pode chegar a um resultado irrefutável sobre **a integridade da cadeia de dados, da urna ao resultado divulgado** (tipo 1), e a um resultado **quantificado** sobre manipulações localizadas (tipo 2). Ele não pode, sozinho, provar a ausência de manipulação no software das urnas (tipo 3). A conclusão final vai separar esses três níveis explicitamente.

## 1. Mapa de ameaças: onde uma fraude poderia acontecer e qual teste cobre

| Ponto da cadeia | Fraude possível | Deixa rastro nos dados públicos? | Testes | Tipo |
|---|---|---|---|---|
| **A. Seção eleitoral** (mesário, eleitor) | Mesário habilitar e votar por eleitores ausentes ("eleitor fantasma") | Sim: habilitação sem biometria, rajadas no fim do dia, intervalos curtos e comparecimento alto com voto concentrado | T28, T29, T31, T07, T22, T02, T12 (biometria com perfil) | 2 |
| **A'. Seção** | Coação ou compra de voto | Fraca: voto concentrado em seções atípicas | T02, E01/E02 (agrupamento por local) | 2 (fraco) |
| **B. Software da urna** | Programa alterado contando ou atribuindo votos errado | Só se for desigual entre urnas (modelo, versão, região); o RDV, o BU e o log saem do mesmo software | T33 (versão e verificação de software no log), T20 (modelo × voto), T02/T10 (padrões), T13 (poder) | 2; o caso uniforme é tipo 3 |
| **B'. Preparação da urna** (carga) | Urna carregada com programa ou dados indevidos; urna não oficial | Sim: correspondência esperada × efetivada; log do GEDAI; código de carga no BU e no log | **T34 e T35 (novos)**, T33 | 1 |
| **C. Depois da urna** (mídia, transmissão) | Boletim alterado no caminho | Sim: a assinatura da urna deixa de validar | T16 (assinatura), T17b (`bu.dat`), T15 (impresso × publicado) | 1 |
| **D. Totalização** | Soma diferente dos boletins | Sim | T01, **T32** (soma das urnas × total oficial) | 1 |
| **E. Divulgação** | Total divulgado ≠ totalizado | Sim | T32 | 1 |

**Leitura do mapa:**
- Os pontos C, D e E ficam cobertos por prova determinística.
- O ponto A fica coberto estatisticamente, com os testes de sequência do log, que são a parte mais forte do tipo 2.
- O ponto B só fica coberto quando a manipulação seria desigual.

**Uma consequência importante, que reforça o estudo:** toda alteração **depois** da urna quebra a assinatura (T16). Então qualquer fraude que não apareça no T16 teria de acontecer **dentro** da urna: na seção (ponto A, visível no log) ou no software (ponto B). Isso reduz o espaço de hipóteses a duas, e é por isso que os testes do log e do software são prioritários.

## 2. Ameaças à validade e o que foi feito

| Ameaça | Risco | Mitigação |
|---|---|---|
| Teste escolhido depois de ver o dado | Achar padrão em qualquer lugar | Protocolo escrito antes; emendas datadas |
| Artefato lido como anomalia | Falso alarme | Investigação obrigatória; 9 artefatos já encontrados e documentados (CATALOGO, seção 4) |
| Confusão geográfica e demográfica | Falso alarme | Comparação dentro do município; controles de perfil; voto órfão |
| Muitos testes | Falso alarme por acaso | α = 0,01; Benjamini-Hochberg nas famílias |
| Teste sem poder | "Não achei" sem valor | Teste de poder com fraude sintética (T13); estender aos testes de log |
| Teste que acusa dado limpo | Conclusão falsa | Calibração em 2022 e nos dados reais (o T4 com Goiás foi corrigido) |
| Formato dos arquivos inferido (sem a especificação oficial) | Leitura errada | Validação cruzada: RDV = boletim = impresso = publicado em 100%; assinatura que valida não acontece por acaso; teste de adulteração. Pendente: conferir com a especificação oficial |
| Cadeia de certificados não verificada até a raiz | Certificado de urna falso | Todas as urnas por emissor e chave de AC; T34/T35 ligam a urna à seção. Pendente: certificados das ACs do TSE |
| Dado incompleto | Conclusão parcial | Conferência de cobertura: urnas processadas × urnas no boletim, por UF |
| Um único analista | Viés e erro não detectado | Código e dados reprodutíveis (PIPELINE.md); convite à replicação independente; nenhum resultado sem script |

## 3. Lacunas e como fechar

| Lacuna | Como fechar | Situação |
|---|---|---|
| Especificação oficial dos arquivos | Baixar do site do TSE (pelo navegador) e conferir o leitor | Pendente (depende do usuário) |
| Certificados das ACs do TSE (raiz) | Obter os certificados públicos das ACs e verificar a cadeia | A buscar |
| Correspondência urna × seção | **T34:** "correspondências esperadas e efetivadas" (dados abertos) × urna do certificado e do log | Novo, a fazer |
| Preparação das urnas | **T35:** logs do GEDAI (dados abertos): toda urna usada tem carga registrada, no período oficial | Novo, a fazer |
| Hashes oficiais do software | Os hashes do software lacrado estão publicados pelo TSE; o log só registra que a verificação deu "SUCESSO" e não traz os hashes. Fica como limite, junto com a menção à cerimônia pública | Limite |
| Teste de integridade (votação paralela com cédulas) | Resultado só divulgado em notícia (1º turno, sem ocorrências); sem dados abertos | Limite, a citar |
| Poder dos testes de log | Simular rajadas de "eleitor fantasma" com a distribuição real de tempos e medir o T28 | A fazer |
| Classificador com fraude sintética (T23) | Zhang, Alvarez e Levin (2019) | A fazer |
| Mais anos de referência | 2022 feito; 2018 tem formato diferente | Opcional |

## 4. O que a conclusão final vai poder dizer (modelo fixado antes)

1. **Integridade (tipo 1):** "X de Y urnas têm assinatura válida, arquivos íntegros, RDV = boletim, log = comparecimento; a soma dá o total oficial." Se Y = X, isso é uma prova, não uma opinião.
2. **Manipulação localizada (tipo 2):**
   - "Nenhum padrão acima de [tamanho], com poder de [p] para detectar [cenário]", ou "encontrado [padrão] em [onde], explicado / não explicado por [...]".
   - Inclui o comportamento do eleitor que explica cada divergência.
3. **Limites (tipo 3):** o que os dados públicos não alcançam, e quem pode verificar (TSE, TCU, entidades fiscalizadoras, teste de integridade).
4. **Resposta direta à pergunta "teve fraude?",** nos termos acima, sem ir além do que os dados sustentam e sem ficar aquém.

## 5. Avaliação frente à DIRETRIZ.md (27/10/2026, 20h35)

Feita sem interromper os processos em andamento e sem alterar resultados já obtidos.

### Já implementado
| Princípio da diretriz | Onde |
|---|---|
| Não presumir fraude nem impossibilidade | PROTOCOLO (postura); AGENTS.md, princípio 1 |
| Anomalia ≠ fraude; buscar alternativas | Critério de anomalia (PROTOCOLO, seção 4); 9 artefatos documentados (CATALOGO, seção 4) |
| Registrar resultados negativos e inconclusivos | CATALOGO, seção 3; T26 mantido e marcado "excluído da conclusão" |
| Poder e falsos positivos | T13 (fraude sintética); calibração em 2022; T4 corrigido (Goiás) |
| FDR | Benjamini-Hochberg no módulo E |
| Mudanças documentadas | Emendas datadas 1 e 2; CATALOGO com horários |
| Reprodutibilidade | Makefile, registro, requirements, sementes fixas nos scripts (rng 1, 3, 7, 11, 42) |
| Comparação 2022 × 2026 | `bateria.py`, `comportamento.py` e `divergencias.py` com o mesmo código |

### Lacunas identificadas (melhorias, não erros)
| Lacuna | Risco | Melhoria | Situação |
|---|---|---|---|
| Testes apresentados sem dizer se a verificação é **interna** (mesma origem) ou independente | Superestimar a força de T01/T32 (coerência do TSE consigo mesmo) | Campo `independencia` no registro e no relatório | Feito (emenda 3) |
| Sem classe de evidência A–G por resultado | Conclusão binária | Campo `classe` no registro; relatório por classe | Feito (emenda 3) |
| Achados do módulo E são **exploratórios** (descobertos nos dados) | Viés de seleção | Confirmar nos logs das urnas (dados não usados na descoberta) e em metades aleatórias de municípios | A fazer |
| Proveniência sem manifesto de hashes de todos os arquivos | Reprodução não verificável byte a byte | `dados/MANIFESTO.csv` (url, data, tamanho, SHA-256, conferência .sha512 do TSE) | A fazer no fim (disco ocupado pelo processamento) |
| Dependência entre testes (vários testes usam o mesmo resíduo) | Contar duas vezes a mesma evidência no critério "repete em 2 testes" | "Independente" passa a exigir dado de origem diferente (tabelas × logs × assinatura) | Feito (emenda 3) |
| Análises de sensibilidade não sistemáticas | Resultado dependente de escolhas (limiar 5, mínimo de 20 válidos, janela de 30 min) | Repetir os principais com limiares alternativos | A fazer |
| Falácia ecológica na transferência de votos (C06) | Ler média de grupo como comportamento individual | Já rotulado; reforçar no relatório | Parcial |
| Fonte externa ao TSE | Toda verificação depende do sistema avaliado | Citar teste de integridade, TCU e observadores como externos (sem dados abertos); declarar como limite | Limite |
| Resultados intermediários sobrescritos ao reprocessar | Perder versões anteriores | Resultados com data/hora no CATALOGO; o git versiona os resultados pequenos | Parcial |
