---
name: apuracao-metodologia
description: Rigor metodológico do estudo da apuração — protocolo pré-registrado, emendas datadas, critérios de anomalia, autoauditoria (mapa de ameaças), catálogo de etapas/consumo, referências classificadas. Use antes de qualquer teste novo, ao revisar conclusões ou ao documentar.
---
# Metodologia, protocolo e documentação

## Quando usar
Antes de criar um teste, ao revisar se uma conclusão se sustenta, ao registrar etapas e ao acrescentar referências.

## Arquivos e papéis
- `PROTOCOLO.md`:
  - perguntas Q1–Q6, modelos nulos N1–N7, módulos A–F, critérios (α = 0,01; BH q = 0,05; efeito abaixo de 0,1 pp = desprezível; anomalia = limiar + sem explicação + repetida em 2 testes);
  - **emendas datadas** antes de rodar.
- `METODOLOGIA.md`: a matemática completa de cada teste (estatística, nulo, limiar, poder).
- `AUTOAUDITORIA.md`: mapa de ameaças (seção → software → preparação → transmissão → totalização → divulgação) × testes; ameaças à validade; lacunas. Releia antes de concluir.
- `CATALOGO.md`: linha do tempo (hora, etapa, script, resultado), testes, artefatos e incidentes, dados e consumo (`dados/listas/recursos.csv` via `scripts/monitorar.sh`).
- `REFERENCIAS.md`: cada fonte com [P] revisada por pares, [T] técnica, [I] imprensa, [G] grupo com posição, [D] dado oficial.
- `testes/registro.json`: o registro legível por máquina; mantenha em sincronia com o CATALOGO.

## Fluxo para uma conclusão
1. O teste estava pré-registrado?
2. Tem poder medido e não acusa dado limpo?
3. Os artefatos foram descartados?
4. Repete em outro teste independente?
5. Em que nível de afirmação está (prova, evidência, limite)?

Só depois disso a afirmação entra no relatório.

- **Situação e resultados num lugar só:** `testes/registro.json` e `CATALOGO.md`. Os documentos de método (METODOLOGIA, PROTOCOLO) não carregam situação ("pendente", "feito"), para não haver versões contraditórias. Ao atualizar, preserve o texto antigo como instantâneo datado no CATALOGO (lição de 27/10, revisão cega externa).

## Desde a F3
- **Pré-registro de cada lote:** em `fase3/PREREG_*.md`, com emenda no PROTOCOLO.
- **Regra adversarial e escala de sinal:** na skill apuracao-investigacao.
- **Resultado:** "Passou" não é conclusão. Todo resultado tem sinal (S0 a S5, ponto cego, método) e impacto em votos (`scripts/impacto_votos.py`, campo `impacto_votos`).

## Atualização da rodada 7 (28/10/2026, V1.5)
- **Escada de verificação:** hash correto ≠ assinatura válida ≠ cadeia autenticada ≠ voto fiel à intenção do eleitor. Diga em qual degrau cada resultado está.
- **Alegação pública vira pré-registro antes de contar** (`fase3/PREREG_*.md` + emenda no PROTOCOLO + `testes/registro.json`), com leitura pré-fixada. A origem da pergunta (matéria, post, vídeo) não é fonte; a resposta entra como pergunta no capítulo "Alegações públicas testadas".
- **Poder é condicional à base:** simulação sobre a base real mede alteração **adicional**; não diz que a base está limpa; a soma das anomalias nunca é teto.
- **Mudança de desenho depois de ver algo (teste de fumaça, resultado intermediário) vira emenda datada e declarada**, com o que foi visto e por quê; a versão anterior fica preservada (ex.: fabricante de estrutura v1 e v2 no T63).
- **Erros do comparador antes de anomalia:** ausente = 0 em BU e RDV, hora de qualquer dia, cache de zip, eventos de log de outras seções. Cada correção é declarada (máx. 2 por teste).
- **Revisão dos próprios vereditos** (`operacao_veracidade/09_*.md`): frase por frase, com situação (preservada, reforçada, enfraquecida, refutada, não avaliável) e redação sugerida.

## Atualização da rodada 8 (aberta, 28/10/2026)
- **Reproduza antes de contestar:** o teste de uma alegação começa por reproduzir os números dela; só depois se examina o agrupamento e a conclusão. Se a alegação se reproduz mas a divisão não separa o que ela diz, diga as duas coisas.
- **Classe de evidência (A a G, Fase 1) e Sinal (S0 a S5, PC, M) são escalas diferentes:** ao integrar um teste, a classe deve ser coerente com o sinal (S3 com B, S4 com D, S0 e S1 com A ou B, PC com G); mostre o Sinal ao público.
