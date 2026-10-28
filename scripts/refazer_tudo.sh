#!/usr/bin/env bash
# Reprocessa os arquivos das urnas das 4 combinações (2026 e 2022, 1º e 2º turno) depois da correção do log em várias partes
# (linhas duplicadas entre partes), e refaz todas as análises que dependem do log. Sem acompanhamento de modelo de IA.
P="$(cd "$(dirname "$0")/.." && pwd)"; cd "$P"
PY=".venv/bin/python"; B="nice -n 10 ionice -c3"
for a in 2026 2022; do for t in 1 2; do
  echo "[$(date +%T)] processando $a ${t}º turno"
  ANO=$a NPROC=14 $B $PY analise/processar_brutos.py $t
done; done
echo "[$(date +%T)] análises"
for a in 2026 2022; do for t in 1 2; do ANO=$a $B $PY analise/analise_logs.py $t > dados/listas/pos_logs_${a}_${t}t.log 2>&1; done; done
for t in 1 2; do $B $PY analise/casos_integridade.py $t > dados/listas/pos_casos_${t}t.log 2>&1; $B $PY analise/correspondencia.py $t > dados/listas/pos_corresp_${t}t.log 2>&1; done
$B $PY analise/relatorio_dados.py > dados/listas/pos_relatorio_final.log 2>&1
$B $PY analise/mapas_dados.py > dados/listas/pos_mapas_final.log 2>&1
$PY scripts/verificar.py > dados/listas/pos_verificar_final.log 2>&1
echo "[$(date +%T)] FIM_REFAZER"
