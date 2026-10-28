#!/usr/bin/env bash
# Processa os arquivos das urnas do 2º turno quando: (1) o processamento do 1º turno acabou e (2) os pacotes chegaram.
# São Paulo (sem pacote oficial) entra quando o download urna por urna terminar.
P="$(cd "$(dirname "$0")/.." && pwd)"
cd $P
until grep -q FIM_1T dados/listas/processar_1t.log; do sleep 30; done
until grep -q "FIM.*2turno_pacotes" dados/listas/download_2t_pacotes.log; do sleep 30; done
echo "início 2º turno (pacotes) $(date +%T)"
NPROC=14 nice -n 10 ionice -c3 .venv/bin/python analise/processar_brutos.py 2 AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE TO ZZ
until grep -qE "FIM_SP|PACOTE_SP_PUBLICADO" dados/listas/brutos_2t_sp.log; do sleep 60; done
echo "início SP $(date +%T)"
NPROC=14 nice -n 10 ionice -c3 .venv/bin/python analise/processar_brutos.py 2 SP
echo FIM_2T
