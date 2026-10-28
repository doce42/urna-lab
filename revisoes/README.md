# Revisões independentes

Cada revisão é uma tentativa de derrubar o que o estudo afirma. Ela é guardada **inteira e sem edição**, separada do material que revisou, e cada achado recebe uma resposta registrada. O objetivo é poder comparar o que o primeiro agente produziu com o que um segundo agente conseguiu verificar, questionar ou refutar.

| Revisão | Revisor | Data | Alvo | Achados | Situação |
|---|---|---|---|---|---|
| [R1](R1-codex/) | Codex (agente de IA em sessão separada; o estudo foi conduzido por Claude) | 28/10/2026 | V1.0-rc1 (tag `rodada-1`, commit `78bef1e`) | 28: 20 da revisão, 6 perguntas novas (P1 a P6) e 2 da nossa autorrevisão | respondida (20 achados respondidos, 8 viram Fase 2) |

## Como cada achado é tratado

- **Classificação** (o achado procede?):
  - `confirmado`: verificamos no código, nas saídas ou por reprodução;
  - `pendente_de_reproducao`: plausível, ainda não reproduzido por nós;
  - `questao_metodologica`: questão de método ou de alcance da afirmação.
- **Situação:**
  - `aberto`: registrado, ainda sem resposta;
  - `em_andamento`: ação começada, não concluída;
  - `respondido`: ação feita no registro vivo;
  - `aceito_como_limite`: fica como limite declarado;
  - `adiado_fase2`: aceito, vira trabalho da Fase 2;
  - `rejeitado`: não procede, com justificativa.
- **No teste afetado:** a contestação entra no campo `provas`, com o alvo (evidência, método, interpretação, redação ou rastreabilidade) e o resultado: **resistiu**, **ajustado**, **caiu** ou **em andamento**. A mudança entra em `mudancas`, com a causa.
- **O retrato revisado nunca é editado.** As correções vão para o registro vivo e entram na versão seguinte.

## Critérios para aprovar a baseline V1.0

A V1.0-rc1 só vira **V1.0 (baseline aprovada)** quando todos estes critérios forem cumpridos e registrados:

1. Todo achado da R1 deixou de estar `aberto` ou `em_andamento`. Cada um está respondido, aceito como limite ou adiado para a Fase 2 com justificativa.
2. Todo achado de prioridade alta com alvo V1.0 tem a ação concluída. Cumprido em 28/10: o R1-02 terminou com todas as listas reverificadas.
3. `make verificar` passa, comparando conjuntos de chaves e não só contagens.
4. A conclusão revisada está coerente com o registro, frase a frase.
5. A proveniência está completa: commit, manifesto de dados, ambiente, sementes e parâmetros.
6. **O responsável pelo estudo aprova explicitamente.** A aprovação significa que o levantamento está documentado e auditado conforme estes critérios, não que todos os resultados sejam infalíveis.

Aprovada, a V1.0 recebe uma tag `v1.0` e um GitHub Release, e abre oficialmente a Fase 2.
