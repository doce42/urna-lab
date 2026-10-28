#!/usr/bin/env bash
# Prepara do zero os dados do estudo (só Presidente), a partir das listas geradas por listas_tse.py.
# Tudo vai para dados/ (precisa de ~250 GB). Roda com prioridade baixa.
set -eu
P="$(cd "$(dirname "$0")/.." && pwd)"; cd "$P"
PY=".venv/bin/python -I"
B="nice -n 10 ionice -c3"
$PY scripts/listas_tse.py
$B scripts/baixar_lista.sh dados/listas/votacao_secao.txt dados/originais 2
$B scripts/baixar_lista.sh dados/listas/bweb_2026.txt dados/originais/bweb_2026 4
$B scripts/baixar_lista.sh dados/listas/bweb_2022.txt dados/2022/originais 4
$B scripts/baixar_lista.sh dados/listas/perfil_2026.txt dados/perfil_eleitorado 4
# votação por seção -> só Presidente, por turno
for ano in 2026 2022; do
  dest=dados; [ "$ano" = 2022 ] && dest=dados/2022
  z=$(ls dados/originais/votacao_secao_${ano}_BR.zip dados/2022/originais/votacao_secao_${ano}_BR.zip 2>/dev/null | head -1)
  unzip -p "$z" "votacao_secao_${ano}_BR.csv" | $PY scripts/secao_presidente.py /dev/stdin "$dest"
done
# Boletim de Urna -> só Presidente (UTF-8)
for ano in 2026 2022; do
  orig=dados/originais/bweb_2026; dest=dados; [ "$ano" = 2022 ] && { orig=dados/2022/originais; dest=dados/2022; }
  mkdir -p $dest/1turno $dest/2turno
  for z in $orig/bweb_*.zip; do
    t=$(basename $z | cut -c6); uf=$(basename $z | cut -c9-10)
    unzip -p "$z" '*.csv' | $PY scripts/filtrar_presidente.py /dev/stdin $dest/${t}turno/bweb_${t}t_${uf}_presidente.csv
  done
done
# arquivos das urnas (~200 GB)
$B scripts/baixar_lista.sh dados/listas/brutos_1t.txt dados/brutos/1turno 4
$B scripts/baixar_lista.sh dados/listas/brutos_2t_pacotes.txt dados/brutos/2turno_pacotes 4 || true
[ -f dados/brutos/2turno_pacotes/bu_imgbu_logjez_rdv_vscmr_2026_2t_SP.zip.ok ] || $B .venv/bin/python scripts/baixar_sp_2t_educado.py
$B scripts/baixar_lista.sh dados/listas/corresp_gedai_2026.txt dados/correspondencias_gedai 6
# 2022: perfil e arquivos brutos das urnas (~170 GB)
$B scripts/baixar_lista.sh dados/listas/perfil_2022.txt dados/2022/perfil_eleitorado 4
$B scripts/baixar_lista.sh dados/listas/brutos_2022_1t.txt dados/2022/brutos/1turno 4
$B scripts/baixar_lista.sh dados/listas/brutos_2022_2t.txt dados/2022/brutos/2turno 4
echo "dados prontos"
