"""H-C (republicação seletiva): o SHA-256 do bu.dat que o projeto de terceiros baixou do TSE (25 a 28/10/2026) é igual ao do arquivo que este projeto baixou depois?"""
import hashlib, json, os, zipfile
import pandas as pd
R = "."; OP = R + "/operacao_veracidade"
c = pd.read_csv(f"{OP}/externo/arvor_totalizacao/conferencia_tse.csv", dtype=str)
r = {"boletins": int(len(c)), "iguais": 0, "diferentes": 0, "ausentes": 0, "exemplos_diferentes": []}
zips = {}
for x in c.itertuples(index=False):
    uf = x.uf.upper(); nome = x.tse_arquivo; h = None
    ind = f"{R}/dados/brutos/2turno/{uf}/{nome}"
    if os.path.exists(ind):
        h = hashlib.sha256(open(ind, "rb").read()).hexdigest()
    else:
        zp = f"{R}/dados/brutos/2turno_pacotes/bu_imgbu_logjez_rdv_vscmr_2026_2t_{uf}.zip"
        if os.path.exists(zp):
            if uf not in zips: zips[uf] = (zipfile.ZipFile(zp), None)
            z = zips[uf][0]
            if zips[uf][1] is None: zips[uf] = (z, set(z.namelist()))   # correção 1: o cache reabria o zip a cada linha
            if nome in zips[uf][1]: h = hashlib.sha256(z.read(nome)).hexdigest()
    if h is None: r["ausentes"] += 1
    elif h == x.tse_sha256: r["iguais"] += 1
    else: r["diferentes"] += 1; r["exemplos_diferentes"].append({"uf": uf, "arquivo": nome, "terceiro": x.tse_sha256, "local": h})
r["janela_downloads_terceiro"] = [c.conferido_em.min(), c.conferido_em.max()]
r["nota"] = "download de terceiro entre 25/10 e 28/10/2026; download local em 27 e 28/10/2026 (manifesto); mesmo conteúdo = nenhuma republicação nesses boletins entre os dois downloads"
json.dump(r, open(f"{OP}/resultados/republicacao_bu.json", "w"), ensure_ascii=False, indent=1); print(json.dumps(r, ensure_ascii=False, indent=1))
