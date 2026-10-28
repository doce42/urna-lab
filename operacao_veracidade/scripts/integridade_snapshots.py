"""Etapa zero: confere o SHA-256 de todos os arquivos das rodadas congeladas e uma amostra dos dados brutos contra o MANIFESTO."""
import csv, hashlib, json, os, random, glob
R = "."
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
out = {"rodadas": {}, "manifesto": {}}
for n in range(1, 7):
    d = f"{R}/rodadas/rodada-{n}"; rs = json.load(open(d + "/resumo.json")); ok = bad = ausente = 0; ruins = []
    for rel, h in rs["arquivos_sha256"].items():
        p = f"{d}/{rel}"
        if not os.path.exists(p): ausente += 1; ruins.append(rel); continue
        if sha(p) == h: ok += 1
        else: bad += 1; ruins.append(rel)
    out["rodadas"][n] = {"versao": rs.get("versao"), "arquivos": len(rs["arquivos_sha256"]), "ok": ok, "diferentes": bad, "ausentes": ausente, "exemplos_problema": ruins[:5],
                         "nota_do_resumo": rs.get("nota")}
# manifesto: amostra de 25 arquivos de até 300 MB
m = list(csv.reader(open(f"{R}/dados/listas/MANIFESTO.csv"))); cab, linhas = m[0], m[1:]
out["manifesto"]["colunas"] = cab; out["manifesto"]["linhas"] = len(linhas)
i_p = next(i for i, c in enumerate(cab) if "caminho" in c.lower() or "arquivo" in c.lower() or "path" in c.lower()); i_h = next(i for i, c in enumerate(cab) if "sha" in c.lower())
i_t = next((i for i, c in enumerate(cab) if "tam" in c.lower() or "bytes" in c.lower()), None)
random.seed(20261028); cand = [l for l in linhas if i_t is None or int(l[i_t]) <= 300_000_000]
amostra = random.sample(cand, 25); ok = bad = ausente = 0; ruins = []
for l in amostra:
    p = f"{R}/dados/{l[i_p]}"
    if not os.path.exists(p): ausente += 1; ruins.append(l[i_p]); continue
    h = hashlib.sha256(); h.update(open(p, "rb").read())
    (ok := ok + 1) if h.hexdigest() == l[i_h] else (bad := bad + 1, ruins.append(l[i_p]))
out["manifesto"].update({"amostra": len(amostra), "ok": ok, "diferentes": bad, "ausentes": ausente, "problemas": ruins[:5], "semente": 20261028})
json.dump(out, open(f"{R}/operacao_veracidade/resultados/integridade_snapshots.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1)[:3000])
