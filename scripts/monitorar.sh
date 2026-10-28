#!/usr/bin/env bash
# Registra o consumo da máquina a cada 30 s em dados/listas/recursos.csv (para o catálogo).
P="$(cd "$(dirname "$0")/.." && pwd)"
f=$P/dados/listas/recursos.csv
[ -f "$f" ] || echo "hora;carga_1min;nucleos;ram_usada_gb;ram_livre_gb;internet_recebido_gb_total;disco_projeto_gb;disco_livre_ssd_gb" > "$f"
while true; do
  read l1 _ < /proc/loadavg
  ram=$(free -m | awk '/Mem:/{printf "%.1f;%.1f", $3/1024, $7/1024}')
  rx=$(awk '/:/ && $1!~/lo/{s+=$2} END{printf "%.2f", s/1e9}' /proc/net/dev)
  dp=$(du -sm $P 2>/dev/null | awk '{printf "%.1f", $1/1024}')
  dl=$(df -BG . | awk 'NR==2{gsub("G","",$4); print $4}')
  echo "$(date '+%F %T');$l1;$(nproc);$ram;$rx;$dp;$dl" >> "$f"
  sleep 30
done
