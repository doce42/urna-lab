#!/usr/bin/env bash
# Baixa uma lista de URLs para uma pasta, retomando downloads interrompidos e conferindo o .sha512 quando o TSE publica.
# Uso: baixar_lista.sh <arquivo_de_urls> <pasta> [paralelos]
set -u
lista=$1; dest=$2; par=${3:-4}
mkdir -p "$dest"
baixa() {
  u=$1; dest=$2; f="$dest/$(basename "$u")"
  [ -f "$f.ok" ] && return 0
  for t in 1 2 3 4 5; do
    curl -s -f -L -C - --retry 5 --retry-delay 10 -m 7200 -o "$f" "$u" && break
    sleep 20
  done
  if h=$(curl -s -f -m 60 "$u.sha512" | awk '{print $1}') && [ -n "$h" ]; then
    if [ "$(sha512sum "$f" | awk '{print $1}')" = "$h" ]; then echo "ok hash $(basename "$f")"; touch "$f.ok"
    else echo "HASH ERRADO $(basename "$f")"; mv "$f" "$f.ruim"; fi
  else
    echo "ok sem-hash $(basename "$f")"; touch "$f.ok"
  fi
}
export -f baixa
xargs -P "$par" -I{} bash -c 'baixa "$@"' _ {} "$dest" < "$lista"
echo "FIM $(date +%T) $dest"
