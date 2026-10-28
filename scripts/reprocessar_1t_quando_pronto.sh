#!/usr/bin/env bash
# Relê os arquivos das urnas do 1º turno com a leitura da sequência do log (T28–T31, T33) depois que o 2º turno terminar.
P="$(cd "$(dirname "$0")/.." && pwd)"; cd "$P"
until grep -q FIM_2T dados/listas/processar_2t.log 2>/dev/null; do sleep 30; done
echo "início releitura 1º turno $(date +%T)"
NPROC=14 nice -n 10 ionice -c3 .venv/bin/python analise/processar_brutos.py 1
echo "FIM_1T_SEQ $(date +%T)"
