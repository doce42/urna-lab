"""F3 em revisão / SA22: as seções-turno de 2022 apuradas pelo Sistema de Apuração (boletim .busa sem .bu), que o leitor
de 2022 do projeto não reconhecia. Para cada uma: arquivos presentes, decodificação do .busa (mesmo decodificador DER do BU),
leitura independente do texto impresso (.imgbusa), conferência de tamanho, SHA-512 e assinatura pela lista .vscsa e
comparação com a tabela publicada (base do projeto). Só pacotes oficiais locais.
Saída: fase3/resultados/sa22.csv (uma linha por seção-turno) e sa22.json."""
import collections, glob, hashlib, json, os, re, sys, zipfile
import pandas as pd

os.environ["ANO"] = "2022"
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); sys.path.insert(0, RAIZ + "/analise")
import processar_brutos as pb  # noqa: E402

NOME = re.compile(r"o(\d{5})-(\d{13})\.(\w+)$")
base = pd.read_parquet(RAIZ + "/analise/base_2022.parquet")
base["k"] = base.SG_UF + "/" + base.CD_MUNICIPIO.astype(int).astype(str) + "/" + base.NR_ZONA.astype(int).astype(str) + "/" + base.NR_SECAO.astype(int).astype(str)
base = base.drop_duplicates("k").set_index("k")
linhas = []
for t in (1, 2):
    for pac in sorted(glob.glob(f"{RAIZ}/dados/2022/brutos/{t}turno/bu_imgbu_logjez_rdv_vscmr_2022_{t}t_*.zip")):
        uf = pac.rsplit("_", 1)[1][:2]; zf = zipfile.ZipFile(pac); por = collections.defaultdict(dict)
        for n in zf.namelist():
            m = NOME.search(n)
            if m: por[m.group(2)][m.group(3)] = n
        for cod, arqs in sorted(por.items()):
            if "busa" not in arqs or "bu" in arqs: continue
            k = f"{uf}/{int(cod[:5])}/{int(cod[5:9])}/{int(cod[9:])}"
            L = {"turno": t, "uf": uf, "cd_mun": cod[:5], "zona": cod[5:9], "secao": cod[9:], "chave": k, "extensoes": ",".join(sorted(arqs)),
                 "tem_rdv": "rdv" in arqs, "tem_log_sa": "logsajez" in arqs, "tem_log_urna": "logjez" in arqs, "tem_imgbusa": "imgbusa" in arqs, "tem_vscsa": "vscsa" in arqs,
                 "motivo_falha_leitor": "extensões do Sistema de Apuração (.busa/.imgbusa/.logsajez/.vscsa) fora de TIPO_2022"}
            dados = {e: zf.read(n) for e, n in arqs.items()}
            try:
                bu = pb.ler_bu(dados["busa"], t); L["busa_lido"] = True
            except Exception as e:
                bu = {}; L["busa_lido"] = False; L["busa_erro"] = repr(e)[:200]
            img = {}
            if "imgbusa" in dados:
                try: img = pb.ler_imgbu(dados["imgbusa"]) or {}
                except Exception as e: L["imgbusa_erro"] = repr(e)[:200]
            L["imgbusa_lido"] = bool(img)
            # assinatura: lista .vscsa (mesmo leiaute do bloco da urna) contra cada arquivo presente
            if "vscsa" in dados:
                try:
                    lista, resumo, verifica = pb.ler_vsc(dados["vscsa"])
                    L["vsc_algoritmo"], L["vsc_cert"], L["vsc_emissor"], L["vsc_lista_ok"] = resumo["algoritmo"], resumo["cert_urna"], resumo["cert_emissor"], resumo["assin_lista_ok"]
                    conf = []
                    for e, n in arqs.items():
                        if e == "vscsa": continue
                        it = lista.get(n)
                        conf.append(it is not None and it[:2] == (len(dados[e]), hashlib.sha512(dados[e]).digest()) and bool(verifica(it[2], it[1])))
                    L["arquivos_conferidos"] = sum(conf); L["arquivos_a_conferir"] = len(conf)
                    L["listados_ausentes"] = ",".join(sorted(x for x in lista if x not in arqs.values() and not re.search(r"\.(hash|ver|chvtp)$", x)))
                except Exception as e:
                    L["vsc_erro"] = repr(e)[:200]
            # comparação com a tabela publicada
            if k in base.index and not pd.isna(base.loc[k, f"total_{t}"]):
                row = base.loc[k]
                pub = {c.rsplit("_", 1)[0]: int(row[c]) for c in row.index if re.fullmatch(rf"v\d+_{t}|branco_{t}|nulo_{t}", c) and not pd.isna(row[c])}
                L["publicado_comparecimento"] = int(row[f"QT_COMPARECIMENTO_{t}"]); L["publicado_aptos"] = int(row[f"QT_APTOS_{t}"])
                L["publicado_votos_presidente"] = sum(pub.values())
                if L["busa_lido"]:
                    dif = {c: (bu.get("bu_" + c, 0), v) for c, v in pub.items() if bu.get("bu_" + c, 0) != v}
                    extra = {c: v for c, v in bu.items() if re.fullmatch(r"bu_(v\d+|branco|nulo)", c) and c[3:] not in pub and v}
                    if bu.get("bu_comparecimento") != L["publicado_comparecimento"]: dif["comparecimento"] = (bu.get("bu_comparecimento"), L["publicado_comparecimento"])
                    L["busa_x_publicado_diferencas"] = json.dumps({**dif, **{f"so_no_busa_{c}": v for c, v in extra.items()}}, ensure_ascii=False) if (dif or extra) else ""
                if img:
                    dimg = {c: (img.get("img_" + c), v) for c, v in pub.items() if c in ("v13", "v22", "branco", "nulo") and img.get("img_" + c) is not None and img.get("img_" + c) != v}
                    L["imgbusa_x_publicado_diferencas"] = json.dumps(dimg, ensure_ascii=False) if dimg else ""
            else:
                L["publicado"] = "ausente da tabela"
            linhas.append(L)
        print(t, uf, sum(1 for x in linhas if x["turno"] == t and x["uf"] == uf), flush=True)
df = pd.DataFrame(linhas)


def classe(r):
    if not r.get("busa_lido"): return "não verificada: boletim não decodificado"
    if r.get("publicado") == "ausente da tabela": return "não comparável: seção ausente da tabela publicada"
    if r.get("busa_x_publicado_diferencas"): return "divergência objetiva entre boletim e tabela"
    ok_img = r.get("imgbusa_lido") and not r.get("imgbusa_x_publicado_diferencas")
    ok_ass = r.get("vsc_lista_ok") is True and r.get("arquivos_conferidos") == r.get("arquivos_a_conferir")
    if ok_img and ok_ass: return "concorda (boletim, texto impresso e assinatura)"
    if ok_ass: return "concorda (boletim e assinatura; texto impresso não lido ou diferente)"
    return "concorda nos votos; assinatura não conferida integralmente"


df["classe"] = df.apply(classe, axis=1)
df.to_csv(RAIZ + "/fase3/resultados/sa22.csv", index=False)
R = {"pergunta": "SA22", "secoes_turno": len(df), "por_turno": df.turno.value_counts().to_dict(), "exterior": int((df.uf == "ZZ").sum()),
     "por_classe": df.classe.value_counts().to_dict(), "busa_lidos": int(df.busa_lido.sum()), "imgbusa_lidos": int(df.imgbusa_lido.sum()),
     "com_rdv": int(df.tem_rdv.sum()), "com_log_sa": int(df.tem_log_sa.sum()), "com_log_urna": int(df.tem_log_urna.sum()),
     "assinatura_lista_ok": int((df.get("vsc_lista_ok") == True).sum()), "algoritmos": df.get("vsc_algoritmo").value_counts().to_dict() if "vsc_algoritmo" in df else {},
     "emissores": df.get("vsc_emissor").value_counts().to_dict() if "vsc_emissor" in df else {},
     "com_arquivos_listados_e_ausentes": int((df.get("listados_ausentes", pd.Series(dtype=str)).fillna("") != "").sum()),
     "comparecimento_publicado_total": int(df.get("publicado_comparecimento", pd.Series(dtype=float)).fillna(0).sum()),
     "votos_presidente_publicados_total": int(df.get("publicado_votos_presidente", pd.Series(dtype=float)).fillna(0).sum())}
json.dump(R, open(RAIZ + "/fase3/resultados/sa22.json", "w"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, default=str))
