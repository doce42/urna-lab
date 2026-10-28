#!/usr/bin/env bash
# Baixa os arquivos das urnas de São Paulo no 2º turno (o único estado sem pacote oficial em 27/10/2026), urna por urna,
# com curl em HTTP/2 multiplexado (o site recusa muitas conexões, não muitos pedidos numa conexão).
# Etapa 1: índice (aux.json) de cada seção. Etapa 2: os arquivos listados no índice. Retoma: pula o que já existe.
set -u
P="$(cd "$(dirname "$0")/.." && pwd)"
B=https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221
D=$P/dados/brutos/2turno/SP; A=$P/dados/brutos/2turno/aux_sp; T=$P/dados/listas/sp_tmp
mkdir -p $D $A $T
curl -s $B/config/sp/sp-p003221-cs.json -o $T/cs.json
$P/.venv/bin/python -I - "$T/cs.json" "$A" "$B" > $T/etapa1.cfg <<'PY'
import json, os, sys
cs, A, B = sys.argv[1:4]
d = json.load(open(cs))
for ab in d["abr"]:
    for m in ab["mu"]:
        for z in m["zon"]:
            for s in z["sec"]:
                nome = f"p003221-sp-m{m['cd']}-z{z['cd']}-s{s['ns']}-aux.json"
                if not os.path.exists(f"{A}/{nome}"):
                    print(f'url = "{B}/dados/sp/{m["cd"]}/{z["cd"]}/{s["ns"]}/{nome}"\noutput = "{A}/{nome}"')
PY
echo "etapa 1: $(grep -c '^url' $T/etapa1.cfg) índices a baixar $(date +%T)"
curl -s -Z --parallel-max 80 --http2 --max-time 60 --retry 8 --retry-delay 2 --retry-max-time 120 --retry-all-errors -f -K $T/etapa1.cfg
echo "etapa 1 fim $(date +%T): $(ls $A | wc -l) índices"
$P/.venv/bin/python -I - "$A" "$D" "$B" > $T/etapa2.cfg <<'PY'
import json, os, re, sys
A, D, B = sys.argv[1:4]
for nome in os.listdir(A):
    m = re.match(r"p003221-sp-m(\d+)-z(\d+)-s(\d+)-aux\.json$", nome)
    if not m:
        continue
    try:
        a = json.load(open(f"{A}/{nome}"))
    except Exception:
        continue
    hs = [h for h in a.get("hashes", []) if h.get("st") == "Totalizado"] or a.get("hashes", [])
    if not hs:
        continue
    h = hs[-1]
    for arq in h["arq"]:
        if not os.path.exists(f"{D}/{arq['nm']}"):
            print(f'url = "{B}/dados/sp/{m[1]}/{m[2]}/{m[3]}/{h["hash"]}/{arq["nm"]}"\noutput = "{D}/{arq["nm"]}"')
PY
echo "etapa 2: $(grep -c '^url' $T/etapa2.cfg) arquivos a baixar $(date +%T)"
curl -s -Z --parallel-max 80 --http2 --max-time 60 --retry 8 --retry-delay 2 --retry-max-time 120 --retry-all-errors -f -K $T/etapa2.cfg
echo "etapa 2 fim $(date +%T): $(ls $D | wc -l) arquivos"
echo FIM_SP
