"""F3 em revisão / A173: os 173 arquivos de 2022 que o DataUrnas-BR (commit 12f0433) aponta como assinados pela urna e
ausentes do pacote de dados abertos do TSE. Verificação documental com os pacotes oficiais guardados localmente
(dados/2022/brutos), lendo só as entradas das 64 seções; nada é baixado. Saída: fase3/resultados/a173.json e a173.csv."""
import collections, hashlib, json, os, re, sys, zipfile
import pandas as pd

os.environ["ANO"] = "2022"
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); sys.path.insert(0, RAIZ + "/analise")
import processar_brutos as pb  # noqa: E402  (ler_vsc, ler_bu com ANO=2022)

DU = os.environ.get("DATAURNAS_DIR", "./externos/DataUrnas-BR")
LISTA = DU + "/data/parquet/2022/integridade/divergencias.jsonl"
SHA_LISTA = "registrado abaixo"
recs = [json.loads(l) for l in open(LISTA)]
assert len(recs) == 173, len(recs)
sha_lista = hashlib.sha256(open(LISTA, "rb").read()).hexdigest()
base = pd.read_parquet(RAIZ + "/analise/base_2022.parquet")
base["k"] = base.SG_UF + "/" + base.CD_MUNICIPIO.astype(int).astype(str) + "/" + base.NR_ZONA.astype(int).astype(str) + "/" + base.NR_SECAO.astype(int).astype(str)
base = base.set_index("k")
NOME = re.compile(r"o(\d{5})-(\d{13})\.(\w+)$")

por_pac = collections.defaultdict(list)
for r in recs: por_pac[(r["turno"], r["uf"].upper())].append(r)
linhas, secoes = [], {}
for (t, uf), rs in sorted(por_pac.items()):
    pac = f"{RAIZ}/dados/2022/brutos/{t}turno/bu_imgbu_logjez_rdv_vscmr_2022_{t}t_{uf}.zip"
    if not os.path.exists(pac):
        for r in rs: linhas.append({**{k: r[k] for k in ("turno", "uf", "cd_mun", "zona", "secao", "arquivo")}, "classe": "pacote local ausente"})
        continue
    zf = zipfile.ZipFile(pac); idx = collections.defaultdict(list)
    for n in zf.namelist():
        m = NOME.search(n)
        if m: idx[m.group(2)].append(n)
    info_pac = {"arquivo": os.path.basename(pac), "bytes": os.path.getsize(pac), "entradas": len(zf.namelist())}
    for r in rs:
        cod = f"{int(r['cd_mun']):05d}{int(r['zona']):04d}{int(r['secao']):04d}"; sk = (t, uf, cod)
        if sk not in secoes:
            nomes = sorted(idx.get(cod, []))
            exts = sorted({NOME.search(n).group(3) for n in nomes})
            vsc = next((n for n in nomes if n.endswith(".vscmr")), None); lista = None; resumo = None
            if vsc:
                try: lista, resumo, _ = pb.ler_vsc(zf.read(vsc))
                except Exception as e: resumo = {"erro": str(e)}
            sha_presentes = {hashlib.sha512(zf.read(n)).hexdigest(): n for n in nomes}
            bu = next((n for n in nomes if n.endswith(".bu")), None); votos = None
            if bu:
                try: votos = pb.ler_bu(zf.read(bu), t)
                except Exception as e: votos = {"erro": str(e)}
            k = f"{uf}/{int(r['cd_mun'])}/{int(r['zona'])}/{int(r['secao'])}"
            pub = None
            if k in base.index:
                row = base.loc[k]
                if isinstance(row, pd.DataFrame): row = row.iloc[0]
                pub = {"aptos": None if pd.isna(row.get(f"QT_APTOS_{t}")) else int(row[f"QT_APTOS_{t}"]),
                       "comparecimento": None if pd.isna(row.get(f"QT_COMPARECIMENTO_{t}")) else int(row[f"QT_COMPARECIMENTO_{t}"]),
                       "votos": {c: int(row[c]) for c in row.index if re.fullmatch(rf"v\d+_{t}|branco_{t}|nulo_{t}", c) and not pd.isna(row[c])},
                       "tipo_urna": row.get(f"DS_TIPO_URNA_{t}")}
            comp = None
            if votos and "erro" not in votos and pub:
                difs = {}
                for c, v in pub["votos"].items():
                    nome = c.rsplit("_", 1)[0]; bk = "bu_" + nome
                    if votos.get(bk, 0) != v: difs[c] = (votos.get(bk, 0), v)
                comp = {"diferencas_bu_x_publicado": difs, "bu_comparecimento": votos.get("bu_comparecimento"), "publicado_comparecimento": pub["comparecimento"]}
            secoes[sk] = {"turno": t, "uf": uf, "cd_mun": r["cd_mun"], "zona": r["zona"], "secao": r["secao"], "arquivos_no_pacote_local": nomes, "extensoes": exts,
                          "vscmr": vsc, "vsc_resumo": resumo, "lista": lista, "sha_presentes": sha_presentes, "tem_bu": bool(bu), "publicado": pub, "comparacao_votos": comp, "pacote": info_pac}
        s = secoes[sk]; nome = r["arquivo"]
        listado = s["lista"] is not None and nome in s["lista"]
        sha_local = s["lista"][nome][1].hex() if listado else None
        presente = nome in s["arquivos_no_pacote_local"]
        renome = s["sha_presentes"].get(r["sha512_assinado"]) if not presente else None
        if s["vscmr"] is None: classe = "não verificável (sem .vscmr no pacote local)"
        elif presente: classe = "presente no pacote local (diferença de coleta ou de versão do pacote)"
        elif renome: classe = f"conteúdo presente com outro nome ({renome})"
        elif listado: classe = "ausente também no pacote local; assinado pela urna"
        else: classe = "ausente também no pacote local; não listado no .vscmr local"
        linhas.append({"turno": t, "uf": uf, "cd_mun": r["cd_mun"], "zona": r["zona"], "secao": r["secao"], "arquivo": nome, "tipo": nome.rsplit(".", 1)[1],
                       "listado_no_vscmr_local": listado, "sha512_local_igual_ao_dataurnas": (sha_local == r["sha512_assinado"]) if listado else None,
                       "assin_lista_ok_local": (s["vsc_resumo"] or {}).get("assin_lista_ok"), "presente_no_pacote_local": presente, "classe": classe,
                       "bu_da_secao_presente": s["tem_bu"], "extensoes_da_secao_no_pacote": ",".join(s["extensoes"])})
df = pd.DataFrame(linhas)
df.to_csv(RAIZ + "/fase3/resultados/a173.csv", index=False)
sec = []
for s in secoes.values():
    sec.append({k: v for k, v in s.items() if k not in ("lista", "sha_presentes", "pacote")} | {"pacote": s["pacote"]["arquivo"]})
R = {"pergunta": "A173", "lista_dataurnas": {"arquivo": "data/parquet/2022/integridade/divergencias.jsonl", "commit": "12f0433bd20882d305dd7b9e4987d6dcf3b321a9", "sha256": sha_lista, "linhas": len(recs)},
     "pacotes_locais": sorted({(s["pacote"]["arquivo"], s["pacote"]["bytes"]) for s in secoes.values()}),
     "por_classe": df.classe.value_counts().to_dict(), "por_tipo": df.tipo.value_counts().to_dict(), "secoes": len(secoes),
     "secoes_por_uf": collections.Counter(s["uf"] for s in secoes.values()), "secoes_com_bu_presente": sum(s["tem_bu"] for s in secoes.values()),
     "secoes_com_divergencia_de_votos": [f"{s['turno']}T {s['uf']}/{s['cd_mun']}/{s['zona']}/{s['secao']}" for s in secoes.values() if s["comparacao_votos"] and s["comparacao_votos"]["diferencas_bu_x_publicado"]],
     "secoes_sem_comparacao": [f"{s['turno']}T {s['uf']}/{s['cd_mun']}/{s['zona']}/{s['secao']}" for s in secoes.values() if not s["comparacao_votos"]],
     "aptos_nas_secoes": sum((s["publicado"] or {}).get("aptos") or 0 for s in secoes.values()),
     "comparecimento_nas_secoes": sum((s["publicado"] or {}).get("comparecimento") or 0 for s in secoes.values()),
     "secoes_detalhe": sec}
json.dump(R, open(RAIZ + "/fase3/resultados/a173.json", "w"), ensure_ascii=False, indent=1, default=str)
print({k: v for k, v in R.items() if k != "secoes_detalhe"})
