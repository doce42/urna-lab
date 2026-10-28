#!/usr/bin/env bash
# Processa os arquivos brutos das urnas de 2022 (1º e 2º turno) depois que: (1) a releitura do 1º turno de 2026 terminou
# (para não somar carga) e (2) o download dos brutos de 2022 terminou.
P="$(cd "$(dirname "$0")/.." && pwd)"; cd "$P"
until grep -q FIM_1T_SEQ dados/listas/processar_1t_seq.log 2>/dev/null; do sleep 60; done
until grep -q "FIM.*2022/brutos/2turno" dados/listas/download_2022_brutos.log 2>/dev/null; do sleep 60; done
for t in 1 2; do
  echo "início 2022 ${t}º turno $(date +%T)"
  ANO=2022 NPROC=14 nice -n 10 ionice -c3 .venv/bin/python analise/processar_brutos.py $t
done
echo "FIM_2022 $(date +%T)"
