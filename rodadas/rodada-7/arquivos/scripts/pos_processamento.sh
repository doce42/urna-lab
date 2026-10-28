#!/usr/bin/env bash
# Etapas mecânicas que faltam, encadeadas e sem acompanhamento de modelo de IA (economia de limite).
# 1. espera a releitura do 1º turno de 2026 terminar; refaz ZZ e MG do 1º turno com o leitor corrigido (exterior / Sistema de Apuração)
# 2. testes de log, casos de integridade e correspondência (1º e 2º turno de 2026); bateria e dados do relatório/mapas
# 3. espera 2022 (download + processamento, encadeado em processar_2022_quando_pronto.sh); roda as mesmas análises para 2022
# Cada etapa grava sua saída em dados/listas/pos_*.log; no fim escreve FIM_POS.
P="$(cd "$(dirname "$0")/.." && pwd)"; cd "$P"
PY=".venv/bin/python"; B="nice -n 10 ionice -c3"
until grep -q FIM_1T_SEQ dados/listas/processar_1t_seq.log 2>/dev/null; do sleep 60; done
echo "[$(date +%T)] refaz ZZ e MG (1º turno)"; NPROC=8 $B $PY analise/processar_brutos.py 1 ZZ MG
for t in 1 2; do
  echo "[$(date +%T)] análises do ${t}º turno"
  $B $PY analise/analise_logs.py $t > dados/listas/pos_logs_${t}t.log 2>&1
  $B $PY analise/casos_integridade.py $t > dados/listas/pos_casos_${t}t.log 2>&1
  $B $PY analise/correspondencia.py $t > dados/listas/pos_corresp_${t}t.log 2>&1
done
echo "[$(date +%T)] bateria, relatório e mapas (2026)"
for a in 2026 2022; do $B $PY analise/bateria.py $a > analise/resultado_bateria_$a.txt 2>&1; done
$B $PY analise/relatorio_dados.py > dados/listas/pos_relatorio.log 2>&1
$B $PY analise/mapas_dados.py > dados/listas/pos_mapas.log 2>&1
$PY scripts/verificar.py > dados/listas/pos_verificar_2026.log 2>&1
echo "[$(date +%T)] FIM_POS_2026"
until grep -q FIM_2022 dados/listas/processar_2022.log 2>/dev/null; do sleep 120; done
echo "[$(date +%T)] análises de 2022 (arquivos das urnas)"
for t in 1 2; do ANO=2022 $B $PY analise/analise_logs.py $t > dados/listas/pos_logs_2022_${t}t.log 2>&1 || true; done
echo "[$(date +%T)] FIM_POS"
