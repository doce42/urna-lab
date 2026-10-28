#!/usr/bin/env bash
# Repete o download de SP (2º turno) até não faltar nenhum índice nem arquivo (cada rodada retoma do ponto onde parou).
P="$(cd "$(dirname "$0")/.." && pwd)"
for rodada in 1 2 3 4 5 6 7 8; do
  echo "== rodada $rodada $(date +%T)"
  $P/scripts/baixar_sp_2t.sh
  f1=$(grep -c '^url' $P/dados/listas/sp_tmp/etapa1.cfg); f2=$(grep -c '^url' $P/dados/listas/sp_tmp/etapa2.cfg)
  echo "faltavam no início da rodada: $f1 índices, $f2 arquivos"
  # só índices de seções agregadas (404 permanente) podem sobrar; arquivos não podem
  [ "$f2" -eq 0 ] && [ "$rodada" -gt 1 ] && break
done
echo FIM_SP_COMPLETO
