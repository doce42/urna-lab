#!/usr/bin/env bash
# Depois do processamento dos arquivos das urnas de 2022: análises de log de 2022, dados do relatório e dos mapas, conferências.
P="$(cd "$(dirname "$0")/.." && pwd)"; cd "$P"
PY=".venv/bin/python"; B="nice -n 10 ionice -c3"
until grep -q FIM_2022 dados/listas/processar_2022.log 2>/dev/null; do sleep 60; done
for t in 1 2; do ANO=2022 $B $PY analise/analise_logs.py $t > dados/listas/pos_logs_2022_${t}t.log 2>&1; done
echo "[$(date +%T)] análises de log de 2022 ok"
$B $PY analise/relatorio_dados.py > dados/listas/pos_relatorio_final.log 2>&1
$B $PY analise/mapas_dados.py > dados/listas/pos_mapas_final.log 2>&1
$PY scripts/verificar.py > dados/listas/pos_verificar_final.log 2>&1
echo "[$(date +%T)] FIM_POS3"
