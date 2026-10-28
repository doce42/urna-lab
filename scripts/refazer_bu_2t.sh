#!/usr/bin/env bash
# Reprocessa só as UFs do 2º turno de 2026 cujo bu.dat não foi lido (lista de eleições com governador antes de Presidente)
P="$(cd "$(dirname "$0")/.." && pwd)"; cd "$P"
PY=".venv/bin/python"; B="nice -n 10 ionice -c3"
echo "[$(date +%T)] reprocessando 2026 2º turno: MT PA PR RJ RS SP ZZ"
ANO=2026 NPROC=14 $B $PY analise/processar_brutos.py 2 MT PA PR RJ RS SP ZZ
echo "[$(date +%T)] análises"
ANO=2026 $B $PY analise/analise_logs.py 2 > dados/listas/pos_logs_2026_2t.log 2>&1
$B $PY analise/casos_integridade.py 2 > dados/listas/pos_casos_2t.log 2>&1; $B $PY analise/correspondencia.py 2 > dados/listas/pos_corresp_2t.log 2>&1
$B $PY analise/relatorio_dados.py > dados/listas/pos_relatorio_final.log 2>&1
$B $PY analise/mapas_dados.py > dados/listas/pos_mapas_final.log 2>&1
$PY scripts/verificar.py > dados/listas/pos_verificar_final.log 2>&1
echo "[$(date +%T)] FIM_BU2T"
