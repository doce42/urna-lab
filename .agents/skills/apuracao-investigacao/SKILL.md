---
name: apuracao-investigacao
description: Investigar perguntas e hipóteses de fraude no estudo da apuração e transformar resultados em respostas legíveis — pergunta central de 2026, catálogo de hipóteses (o que cada fraude deixaria, quantos votos exige), escala de sinal separada de "passou", regra adversarial (compatível com log ≠ verificado), pré-registro por investigação com orçamento e parada, respostas pergunta a pergunta com impacto em votos. Use ao abrir uma investigação nova, ao avaliar uma anomalia ou ao atualizar as respostas e o veredito. Desde a rodada 7: fluxo de alegação pública (pré-registro antes de contar), resposta central com pontos cegos e poder por mecanismo, frases que não podem voltar e fila aberta.
---
# Investigação, hipóteses e respostas

## Quando usar
Ao investigar uma anomalia ou hipótese, ao propor um teste novo, ao atualizar a resposta central ou as respostas do site.

## A pergunta que o estudo responde
"A apuração presidencial de 2026 tem sinais de fraude capaz de mudar o resultado?" Para inverter, é preciso trocar ~2,22 mi votos (metade da margem de 4.430.191). Toda conclusão diz o que significa em votos, comparado a isso.

## Fontes únicas (editar estas, nunca o JSON gerado)
- `fase3/f3_veredito.py` → `fase3/veredito_2026.json` e `VEREDITO_2026.md`. Contém:
  - a resposta central e a dedução;
  - as **10 hipóteses de fraude** (mecanismo, o que deixaria, escala, testes, resultado, situação, em votos);
  - as **anomalias de 2026**;
  - o **sinal de cada teste** (S0 sem sinal, S1 explicado por fator verificável, S2 compatível só com o registro do sistema, S3 anomalia sem causa, S4 divergência ou lacuna objetiva, S5 indício, PC ponto cego, M método).
- `fase3/f3_respostas.py` → `fase3/respostas_f3.json` e `RESPOSTAS_F3.md`: 26 perguntas (integridade, curvas, zeros, entre turnos) e os 33 itens do inventário, cada um com resposta, classificação, em votos, demonstra, não demonstra, validação, reabertura e fechamento.
- `fase3/f3_inventario.py` → `inventario.json` e `INVENTARIO.md`: estado e histórico de cada pergunta (blocos REV…), com `evidencia_arquivos`.
- **Ordem para regerar:** `f3_veredito.py`, `f3_inventario.py`, `f3_respostas.py`, `scripts/verificar.py` e o build do site.

## Regras (aprendidas na F3; não negociáveis)
1. **Pré-registro antes de rodar** (`fase3/PREREG_*.md`, com emenda no PROTOCOLO): pergunta, hipóteses concorrentes, o que mudaria a conclusão, nulo, critério de calibração ou validação, parada, custo.
2. **Orçamento por lote:** no máximo 4 investigações, 1 teste principal + 1 validação cada, 1 correção + 1 repetição por falha operacional. O que excede é declarado como desvio. Sem subagente, salvo pedido do responsável.
3. **Regra adversarial:** BU, RDV, imagem e log vêm da mesma urna; tabela, totais e declarações, do mesmo TSE.
   - Concordância entre eles é **consistência interna**.
   - Explicação vinda do log é **"compatível com o registro"**, nunca "explicada" (ver `fase3/RELATORIO_ADVERSARIAL.md`).
   - Para cada anomalia, separar as hipóteses H0 a H3 e dizer o que as distinguiria.
4. **Artefato antes de anomalia:** quando um comparador acusa milhares de divergências, suspeite primeiro do comparador. Exemplos: o nulo por suspensão de 2022 já somado, NaN + n, campo "urna" do log de 2022 inválido.
5. **Modelo que falha a calibração não é usado**, e não se tenta modelo atrás de modelo: registra "não determinado" com o motivo.
6. **Simulação não é evidência de fraude:** votos simulados são sintéticos. Detecção conta só o **sentido correto** (A2).
7. Nada de vídeos, influenciadores ou redes sociais como fonte.

## Pontos cegos e fila (para continuar)
- **H9 (deslocamento uniforme pequeno) e H10 (urna alterada antes dos registros):** só fecham com boletins impressos de fiscais em amostra aleatória, auditoria independente ou cadeia de certificados até a raiz.
- **P11:** `dados/brutos/doc/anexo_2179302_tse_lista_hashes_chave_publica_eleicoes_2022.zip` (lista de hashes de chaves públicas publicada pelo TSE) ainda não foi examinado.
- **Salvador (T44):** desvio de cidade inteira sem causa.
- **Curvas (Q10, Q12):** sem modelo de chegada validado.
- **Zeros:** sem modelo de cauda baixa calibrado (refazer o critério de calibração antes).

## Atualização da rodada 7 (28/10/2026, V1.5)
- **Fluxo para alegação pública (rodadas 6 e 7):** transcrever o que se afirma em números; pré-registrar medidas e leitura pré-fixada; rodar; registrar T-nn; acrescentar a pergunta (Q-nn) no capítulo certo; regerar veredito, inventário e respostas. Ex.: T45 a T51 (live de 2022, matérias, thread), T52 a T55, T65 (vídeo dos "votos extras").
- **Operação Veracidade Geral (`operacao_veracidade/`):** a resposta central agora é "não encontramos sinal nos mecanismos que os dados públicos conseguem examinar, com o poder medido para cada um"; os pontos cegos incluem UF, região, lote e uniforme abaixo de ~0,5 a 2,2 mi, além de H9 e H10. **Não escreva "deixariam sinais muito maiores" sem os limiares do T63, nem trate a soma das anomalias como teto.**
- **Frases que não podem voltar:** "dois caminhos" (H9 e H10 só), "zeros no nível previsto" (H7 é não determinado), dígitos S0 (T05 é PC), "falso alarme 0/30" como taxa, "todos até a AC emissora" sem a data da verificação completa.
- **Fila aberta:** reler os 16 casos do T14 por data, ID de urna e seção; T44 por cidade com o poder do T63; correção formal de multiplicidade; teste de integridade com votos conhecidos (resultado não obtido); raiz da cadeia; amostra probabilística de boletins impressos.
- **Rodada 8 está aberta** (hipótese do "Relatório Pericial Independente"): pré-registro e testes entram no registro vivo; **não congelar sem aprovação explícita**.
