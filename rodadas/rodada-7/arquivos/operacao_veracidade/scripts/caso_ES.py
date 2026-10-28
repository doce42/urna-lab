"""Protocolo de divergência grave: ES, município 57932, zona 9, seções 85 e 112, 2º turno de 2026. Preserva hashes e relê o log por um segundo método."""
import collections, hashlib, io, json, os, re, sys, zipfile
os.environ["ANO"] = "2026"
R = "."; sys.path.insert(0, R + "/analise")
import processar_brutos as PB  # só para nomear os arquivos; a leitura do log é feita aqui, à parte
z = zipfile.ZipFile(PB.fonte(2, "ES")[0]); por = collections.defaultdict(dict)
for n in z.namelist():
    a = PB.analisa_nome(n, "ES")
    if a and a[0][1:] == ("57932", "9", "85") or a and a[0][1:] == ("57932", "9", "112"): por[a[0][3]][a[1]] = n
out = {"secoes": {}}
for sec in ("85", "112"):
    arqs = {t: z.read(n) for t, n in por[sec].items()}
    info = {"arquivos": {t: {"nome": por[sec][t], "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()} for t, b in arqs.items()}}
    # segundo método do log: zip aninhado lido à mão, contagem de eventos de voto e de cabeçalhos de seção por ID de urna
    def le(b, prof=0):
        zz = zipfile.ZipFile(io.BytesIO(b)); res = []
        for nm in zz.namelist():
            c = zz.read(nm)
            if nm.endswith((".jez", ".logjez")): res += le(c, prof + 1)
            else: res.append((nm, c.decode("latin1")))
        return res
    partes = le(arqs["log"]); info["partes_do_log"] = [(nm, len(t.splitlines())) for nm, t in partes]
    votos, secoes, ids = collections.Counter(), collections.Counter(), collections.Counter(); por_parte = []
    vistas = set()
    for nm, txt in partes:
        pv = collections.Counter()
        for l in txt.splitlines():
            if l in vistas: continue
            vistas.add(l); c = l.split("\t")
            if len(c) < 5: continue
            data, idu, msg = c[0][:10], c[2], c[4]; ids[idu] += 1
            if "O voto do eleitor foi computado" in msg: votos[f"{idu}|{data}"] += 1; pv[f"{idu}|{data}"] += 1
            s_ = re.search(r"Seção Eleitoral: (\d+)", msg)
            if s_: secoes[f"{idu}|{data}|secao {int(s_.group(1))}"] += 1
        por_parte.append({"parte": nm, "votos_computados_por_id_e_data": dict(pv)})
    info["segundo_metodo"] = {"votos_computados_por_id_e_data": dict(votos), "votos_em_25_10_2026": int(sum(v for k, v in votos.items() if k.endswith("|25/10/2026"))),
                              "votos_em_04_10_2026": int(sum(v for k, v in votos.items() if k.endswith("|04/10/2026"))), "linhas_com_secao_eleitoral": dict(secoes), "por_parte": por_parte}
    out["secoes"][sec] = info
a, b = out["secoes"]["85"]["arquivos"], out["secoes"]["112"]["arquivos"]
out["comparacao"] = {t: ("mesmo arquivo" if a[t]["sha256"] == b[t]["sha256"] else "arquivos diferentes") for t in a if t in b}
os.makedirs(R + "/operacao_veracidade/evidencia", exist_ok=True)
json.dump(out, open(R + "/operacao_veracidade/evidencia/caso_ES_57932_9_85_112.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
