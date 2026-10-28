---
name: apuracao-comportamento
description: Comportamento do eleitor e mudança entre turnos — transferência de votos (inferência ecológica com restrição), comparecimento e voto por perfil demográfico, região, porte do município, hora do voto, curva prevista. Use para os módulos B, C e E do PROTOCOLO.
---
# Comportamento eleitoral e divergências

## Quando usar
Explicar o que mudou entre turnos, quem votou, onde e quando; montar o "comportamento esperado" e as divergências (E01–E03).

## Comandos
- `make comportamento ANO=2026|2022` → `analise/resultado_comportamento_<ano>.json` (C01, C03, C06, C07, C08).
- Perfil do eleitorado por seção: `analise/perfil.py` → `analise/perfil.parquet`.
- Curva prevista: `grafico/prever.py` (no gráfico) e `analise/curva.py`.

## Métodos e cuidados
- **C06, transferência:**
  - Goodman com restrição (frações entre 0 e 1; cada linha soma 1), estimado por UF e combinado pelo peso de cada grupo.
  - **Pesos normalizados** (sem isso o otimizador não converge e devolve linhas uniformes, já aconteceu).
  - **Conferência obrigatória:** a matriz tem que reproduzir o total observado do 2º turno (erro abaixo de 0,1%).
  - É inferência ecológica: média de grupos, nunca comportamento individual.
- **Regressões "dentro do município":** subtraia a média do município (efeito fixo) e use erro-padrão agrupado por município. São associações, não causas.
- **Fuso:** horários do BU e do log são locais. Use `8 − hora local de abertura` (moda do município, só urnas que abriram nos primeiros 15 min).
- **Prorrogação no 2º turno de 2026:** 6.748 seções abertas até ~19h. Não confundir com anomalia.

## Divergências (E01–E03)
Comportamento esperado = modelos N2 (persistência), N3 (transferência) e N4 (perfil). Divergência = resíduo. Procure agrupamento por local, zona e município. Explique cada uma antes de chamar de anomalia (PROTOCOLO, seção 4).
