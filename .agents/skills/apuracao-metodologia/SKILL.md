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
