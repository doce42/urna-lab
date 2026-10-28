#!/usr/bin/env bash
# Baixa um arquivo grande em N faixas paralelas (curl --range) e junta; retoma faixas incompletas; confere o tamanho.
# Uso: baixar_paralelo.sh <url> <arquivo_destino> [faixas]
set -eu
url=$1; dest=$2; n=${3:-8}
tam=$(curl -sI -m 30 "$url" | awk 'tolower($1)=="content-length:"{print $2+0}' | tail -1)
[ -n "$tam" ] || { echo "sem tamanho"; exit 1; }
pedaco=$(( (tam + n - 1) / n ))
for i in $(seq 0 $((n-1))); do
  ini=$(( i * pedaco )); fim=$(( ini + pedaco - 1 )); [ $fim -ge $tam ] && fim=$(( tam - 1 ))
  ( f="$dest.parte$i"; esperado=$(( fim - ini + 1 ))
    for t in 1 2 3 4 5 6 7 8; do
      atual=$( [ -f "$f" ] && stat -c %s "$f" || echo 0 )
      [ "$atual" -ge "$esperado" ] && break
      curl -s -f --retry 5 -m 7200 -r $(( ini + atual ))-$fim "$url" >> "$f" || sleep 10
    done ) &
done
wait
cat $(for i in $(seq 0 $((n-1))); do echo "$dest.parte$i"; done) > "$dest.tmp"
[ "$(stat -c %s "$dest.tmp")" -eq "$tam" ] || { echo "TAMANHO ERRADO"; exit 1; }
mv "$dest.tmp" "$dest"; rm -f "$dest".parte*; touch "$dest.ok"
echo "FIM paralelo $(basename "$dest") $tam bytes"
