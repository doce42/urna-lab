#!/usr/bin/env bash
# Revisão R1: reexecuções baratas que respondem a achados confirmados (sem reprocessar os 405 GB). Sem IA acompanhando.
P="$(cd "$(dirname "$0")/.." && pwd)"; cd "$P"
PY=".venv/bin/python"; B="nice -n 10 ionice -c3"
echo "[$(date +%T)] R1-02 varredura das chaves (1º turno)"; NPROC=12 $B $PY analise/varrer_chaves.py 1
echo "[$(date +%T)] R1-02 varredura das chaves (2º turno)"; NPROC=12 $B $PY analise/varrer_chaves.py 2
echo "[$(date +%T)] FIM_R1"
