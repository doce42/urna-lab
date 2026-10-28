#!/usr/bin/env bash
# Segunda parte das etapas mecânicas (não edita o script em execução): sensibilidade e manifesto de proveniência.
P="$(cd "$(dirname "$0")/.." && pwd)"; cd "$P"
PY=".venv/bin/python"; B="nice -n 10 ionice -c3"
until grep -q FIM_POS_2026 dados/listas/pos_processamento.log 2>/dev/null; do sleep 60; done
for a in 2026 2022; do $B $PY analise/sensibilidade.py $a > analise/resultado_sensibilidade_$a.txt 2>&1; done
echo "[$(date +%T)] sensibilidade ok"
until grep -q "FIM_POS$" dados/listas/pos_processamento.log 2>/dev/null; do sleep 120; done
$B $PY scripts/manifesto.py > dados/listas/pos_manifesto.log 2>&1
echo "[$(date +%T)] FIM_POS2"
