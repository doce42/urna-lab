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

## F2 e F3
- **E02 com nulo espacial:** `fase3/rev_i3_espacial.py`. A referência é a zona eleitoral, que não é vizinhança geográfica. A lista de locais depende do método.
- **Moran's I (T42):** `fase3/f3_pendencias.py p19`.
- **Zona 251 de SP (2022) e perfil do eleitorado:** `fase3/inv_r4_zona251.py`. O desvio persiste.
- **Salvador (2026) entre as capitais e com perfil:** `fase3/final_salvador.py`. Única capital desviante, não explicada pelo perfil.
- **Perfil por seção:** `dados/perfil_eleitorado` (2026, coluna `QT_ELEITORES`) e `dados/2022/perfil_eleitorado` (coluna `QT_ELEITORES_PERFIL`).
- **Contas entre turnos:** `fase3/resultados/entre_turnos_contas.json`. A identidade fecha exatamente; os fluxos individuais não são identificáveis.
