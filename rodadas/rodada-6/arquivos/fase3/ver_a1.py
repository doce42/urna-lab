"""F3 em revisão / A1: seções de 2022 do Brasil que a base do projeto tem e que não têm votos de Presidente no DataUrnas-BR
(commit 12f0433). Classificação por regra fixa (fase3/PREREG_REVISAO.md, adendo A1/A2/A4) e comparação de votos do boletim
local com a tabela publicada. Validação: segunda contagem pelo cruzamento das listas de seções do pacote e do DataUrnas-BR.
Só arquivos locais. Saída: fase3/resultados/a1.csv e a1.json."""
import collections, glob, json, os, re, sys, zipfile
import pandas as pd

os.environ["ANO"] = "2022"
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); sys.path.insert(0, RAIZ + "/analise")
import processar_brutos as pb  # noqa: E402

DU = os.environ.get("DATAURNAS_DIR", "./externos/DataUrnas-BR") + "/data/parquet/"
K = lambda uf, m, z, s: f"{uf.upper()}/{int(m)}/{int(z)}/{int(s)}"
base = pd.read_parquet(RAIZ + "/analise/base_2022.parquet")
base["k"] = [K(*x) for x in zip(base.SG_UF, base.CD_MUNICIPIO, base.NR_ZONA, base.NR_SECAO)]
base = base.drop_duplicates("k").set_index("k")
# votos de Presidente no DataUrnas-BR (mesma leitura do f3_reconcilia.py)
v = pd.concat([pd.read_parquet(DU + f, columns=["secao_id", "cargo"]) for f in ("votos_t1_a.parquet", "votos_t1_b.parquet", "votos_t2.parquet")])
v = v[v.cargo == "Presidente"].secao_id.drop_duplicates().str.split("/", expand=True)
com_votos = {(int(a[0]), K(b, c, d, e)) for a, b, c, d, e in zip(v[0], v[1], v[2], v[3], v[4])}
sec = pd.read_parquet(DU + "secoes.parquet", columns=["id", "turno", "tipo_urna", "is_reserva", "n_issues", "comparecimento"])
sp = sec.id.str.split("/", expand=True); sec["k"] = [K(b, c, d, e) for b, c, d, e in zip(sp[1], sp[2], sp[3], sp[4])]
sec_deles = {(int(t), k): r for t, k, r in zip(sec.turno, sec.k, sec.to_dict("records"))}
iss = pd.read_parquet(DU + "issues.parquet", columns=["secao_id", "codigo"])
iss_por = iss.groupby("secao_id").codigo.apply(lambda s: ",".join(sorted(set(s)))).to_dict()
ocor = [json.loads(l) for l in open(DU + "2022/integridade/ocorrencias_publicacao.jsonl")]
ocor_k = {(o["turno"], K(o["uf"], o["cd_mun"], o["zona"], o["secao"])): o["categoria"] for o in ocor}
sa22 = pd.read_csv(RAIZ + "/fase3/resultados/sa22.csv"); sa_k = {(int(t), k) for t, k in zip(sa22.turno, sa22.chave)}
# seções agregadas: a base lista, na seção principal, as seções agregadas a ela
agreg = set()
for t in (1, 2):
    for k, s in base[f"DS_SECOES_AGREGADAS_{t}"].dropna().items():
        if s in ("#NULO#", "", "#NE#"): continue
        uf, m, z, _ = k.split("/")
        for x in re.findall(r"\d+", str(s)): agreg.add((t, f"{uf}/{m}/{z}/{int(x)}"))
NOME = re.compile(r"o(\d{5})-(\d{13})\.(\w+)$")
linhas = []
for t in (1, 2):
    nossas = base[base[f"total_{t}"].notna() & (base.SG_UF != "ZZ")].index
    alvo = [k for k in nossas if (t, k) not in com_votos]
    por_uf = collections.defaultdict(list)
    for k in alvo: por_uf[k.split("/")[0]].append(k)
    for uf, ks in sorted(por_uf.items()):
        pac = f"{RAIZ}/dados/2022/brutos/{t}turno/bu_imgbu_logjez_rdv_vscmr_2022_{t}t_{uf}.zip"
        zf = zipfile.ZipFile(pac); idx = collections.defaultdict(dict)
        for n in zf.namelist():
            mm = NOME.search(n)
            if mm: idx[mm.group(2)][mm.group(3)] = n
        for k in ks:
            _, m, z, s = k.split("/"); cod = f"{int(m):05d}{int(z):04d}{int(s):04d}"; arqs = idx.get(cod, {})
            row = base.loc[k]; deles = sec_deles.get((t, k)); sid = f"{t}T/{uf.lower()}/{int(m):05d}/{int(z):04d}/{int(s):04d}"
            L = {"turno": t, "uf": uf, "chave": k, "tipo_urna_tabela": row.get(f"DS_TIPO_URNA_{t}"), "secoes_agregadas_nesta": row.get(f"DS_SECOES_AGREGADAS_{t}"),
                 "aptos": row.get(f"QT_APTOS_{t}"), "comparecimento": row.get(f"QT_COMPARECIMENTO_{t}"), "arquivos_no_pacote": ",".join(sorted(arqs)),
                 "no_dataurnas_secoes": deles is not None, "dataurnas_tipo_urna": (deles or {}).get("tipo_urna"), "dataurnas_reserva": (deles or {}).get("is_reserva"),
                 "dataurnas_issues": iss_por.get(sid, ""), "dataurnas_ocorrencia": ocor_k.get((t, k), ""), "sa22": (t, k) in sa_k, "agregada_a_outra": (t, k) in agreg}
            boletim = "bu" if "bu" in arqs else ("busa" if "busa" in arqs else None); L["boletim_local"] = boletim or ""
            if boletim:
                try:
                    bu = pb.ler_bu(zf.read(arqs[boletim]), t)
                    pub = {c.rsplit("_", 1)[0]: int(row[c]) for c in row.index if re.fullmatch(rf"v\d+_{t}|branco_{t}|nulo_{t}", c) and not pd.isna(row[c])}
                    dif = {c: (bu.get("bu_" + c, 0), x) for c, x in pub.items() if bu.get("bu_" + c, 0) != x}
                    if bu.get("bu_comparecimento") != L["comparecimento"]: dif["comparecimento"] = (bu.get("bu_comparecimento"), L["comparecimento"])
                    L["boletim_lido"] = True; L["diferencas_boletim_x_tabela"] = json.dumps(dif, ensure_ascii=False) if dif else ""
                except Exception as e:
                    L["boletim_lido"] = False; L["erro"] = repr(e)[:150]
            else:
                L["boletim_lido"] = False
            # regra fixa, na ordem do pré-registro
            if L["sa22"]: c = "1 Sistema de Apuração (SA22)"
            elif L["agregada_a_outra"] and not arqs: c = "2 seção agregada a outra (sem arquivos próprios)"
            elif L["no_dataurnas_secoes"]: c = "3 no DataUrnas-BR sem votos de Presidente"
            elif arqs: c = "4 fora do DataUrnas-BR, com arquivos no pacote local"
            elif not arqs: c = "5 sem arquivos no pacote local"
            else: c = "6 outra"
            L["classe"] = c; linhas.append(L)
df = pd.DataFrame(linhas); df.to_csv(RAIZ + "/fase3/resultados/a1.csv", index=False)
# validação: segunda contagem independente da regra, pelas listas de seções (pacote local × DataUrnas-BR)
val = {}
for t in (1, 2):
    d = df[df.turno == t]
    val[f"{t}T"] = {"sem_par": len(d), "com_arquivos_no_pacote": int((d.arquivos_no_pacote != "").sum()), "sem_arquivos_no_pacote": int((d.arquivos_no_pacote == "").sum()),
                    "na_tabela_de_secoes_do_dataurnas": int(d.no_dataurnas_secoes.sum()), "agregadas_segundo_a_base": int(d.agregada_a_outra.sum())}
R = {"pergunta": "A1", "sem_par_por_turno": df.turno.value_counts().to_dict(), "por_classe": {f"{t}T": df[df.turno == t].classe.value_counts().to_dict() for t in (1, 2)},
     "boletins_lidos": int(df.boletim_lido.sum()), "divergencias_de_votos": df[df.get("diferencas_boletim_x_tabela", pd.Series(dtype=str)).fillna("") != ""].chave.tolist(),
     "validacao_segunda_contagem": val,
     "issues_mais_comuns_entre_as_do_dataurnas": collections.Counter(c for x in df.dataurnas_issues for c in x.split(",") if c).most_common(8),
     "votos_nas_secoes_sem_par": {f"{t}T": int(df[df.turno == t].comparecimento.fillna(0).sum()) for t in (1, 2)}}
json.dump(R, open(RAIZ + "/fase3/resultados/a1.json", "w"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, default=str))
