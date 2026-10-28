"""F3 / fila F2: seções do Sistema de Apuração de 2026 (arquivos -busa.dat, -imgbusa.dat, -sa.vsc): lista assinada, tamanho,
SHA-512 e assinatura de cada arquivo, boletim × tabela, texto impresso × tabela. Ver fase3/PREREG_FILA.md (F2).
Saída: fase3/resultados/fila_f2_sa2026.json e .csv."""
import glob, hashlib, json, os, re, sys, zipfile
import pandas as pd

os.environ["ANO"] = "2026"
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); sys.path.insert(0, RAIZ + "/analise")
import processar_brutos as pb  # noqa: E402

NOME = re.compile(r"o\d{5}([a-z]{2})(\d{5})(\d{4})(\d{4})-(\w+)\.(\w+)$")
base = pd.read_parquet(RAIZ + "/analise/base.parquet")
base["k"] = base.SG_UF + "/" + base.CD_MUNICIPIO.astype(int).astype(str) + "/" + base.NR_ZONA.astype(int).astype(str) + "/" + base.NR_SECAO.astype(int).astype(str)
base = base.drop_duplicates("k").set_index("k")
linhas = []
for t, pasta in ((1, "1turno"), (2, "2turno_pacotes")):
    for pac in sorted(glob.glob(f"{RAIZ}/dados/brutos/{pasta}/*.zip")):
        zf = zipfile.ZipFile(pac); por = {}
        for n in zf.namelist():
            m = NOME.search(n)
            if m: por.setdefault((m.group(1).upper(), m.group(2), m.group(3), m.group(4)), {})[f"{m.group(5)}.{m.group(6)}"] = n
        for (uf, mu, z, s), arqs in por.items():
            if "busa.dat" not in arqs: continue
            k = f"{uf}/{int(mu)}/{int(z)}/{int(s)}"; d = {e: zf.read(n) for e, n in arqs.items()}
            L = {"turno": t, "secao": k, "arquivos": ",".join(sorted(arqs))}
            try: bu = pb.ler_bu(d["busa.dat"], t); L["boletim_lido"] = True
            except Exception as e: bu = {}; L["boletim_lido"] = False; L["erro_boletim"] = repr(e)[:150]
            img = {}
            if "imgbusa.dat" in d:
                try: img = pb.ler_imgbu(d["imgbusa.dat"]) or {}
                except Exception as e: L["erro_imagem"] = repr(e)[:150]
            L["imagem_lida"] = bool(img)
            vsc = d.get("sa.vsc")
            if vsc:
                try:
                    lista, resumo, verifica = pb.ler_vsc(vsc)
                    L.update({"algoritmo": resumo["algoritmo"], "certificado": resumo["cert_urna"], "emissor": resumo["cert_emissor"], "lista_assinada_ok": resumo["assin_lista_ok"]})
                    conf = {e: bool(lista.get(arqs[e]) is not None and lista[arqs[e]][:2] == (len(d[e]), hashlib.sha512(d[e]).digest()) and verifica(lista[arqs[e]][2], lista[arqs[e]][1])) for e in arqs if e != "sa.vsc"}
                    L["arquivos_conferidos"] = sum(conf.values()); L["arquivos_a_conferir"] = len(conf); L["nao_conferidos"] = ",".join(e for e, ok in conf.items() if not ok)
                    L["listados_e_ausentes"] = ",".join(sorted(x for x in lista if x not in arqs.values()))
                except Exception as e: L["erro_assinatura"] = repr(e)[:150]
            if k in base.index and not pd.isna(base.loc[k, f"total_{t}"]):
                row = base.loc[k]; pub = {c.rsplit("_", 1)[0]: int(row[c]) for c in row.index if re.fullmatch(rf"v\d+_{t}|branco_{t}|nulo_{t}", c) and not pd.isna(row[c])}
                L["comparecimento_tabela"] = int(row[f"QT_COMPARECIMENTO_{t}"])
                if bu: L["boletim_x_tabela"] = json.dumps({c: (bu.get("bu_" + c, 0), v) for c, v in pub.items() if bu.get("bu_" + c, 0) != v}) if any(bu.get("bu_" + c, 0) != v for c, v in pub.items()) else ""
                if img: L["imagem_x_tabela"] = json.dumps({c: (img.get("img_" + c), v) for c, v in pub.items() if c in ("v13", "v22", "branco", "nulo") and img.get("img_" + c) is not None and img.get("img_" + c) != v}) if any(c in ("v13", "v22", "branco", "nulo") and img.get("img_" + c) is not None and img.get("img_" + c) != v for c, v in pub.items()) else ""
            else: L["tabela"] = "seção ausente da tabela"
            ok_ass = L.get("lista_assinada_ok") is True and L.get("arquivos_conferidos") == L.get("arquivos_a_conferir")
            if not L["boletim_lido"]: L["classe"] = "não verificável: boletim não decodificado"
            elif L.get("tabela"): L["classe"] = "não comparável: fora da tabela"
            elif L.get("boletim_x_tabela"): L["classe"] = "divergência objetiva boletim × tabela"
            elif ok_ass and L["imagem_lida"] and not L.get("imagem_x_tabela"): L["classe"] = "concorda (boletim, texto impresso e assinatura; consistência interna)"
            elif ok_ass: L["classe"] = "concorda (boletim e assinatura; texto impresso não lido ou diferente)"
            else: L["classe"] = "concorda nos votos; assinatura não conferida integralmente"
            linhas.append(L)
df = pd.DataFrame(linhas); df.to_csv(RAIZ + "/fase3/resultados/fila_f2_sa2026.csv", index=False)
R = {"pergunta": "fila F2", "secoes_turno": len(df), "por_turno": df.turno.value_counts().to_dict(), "por_classe": df.classe.value_counts().to_dict(),
     "assinatura_ok": int((df.get("lista_assinada_ok") == True).sum()), "algoritmos": df.get("algoritmo", pd.Series(dtype=str)).value_counts().to_dict(),
     "com_listados_e_ausentes": int((df.get("listados_e_ausentes", pd.Series(dtype=str)).fillna("") != "").sum()), "nao_conferidos": df.get("nao_conferidos", pd.Series(dtype=str)).fillna("").value_counts().to_dict()}
json.dump(R, open(RAIZ + "/fase3/resultados/fila_f2_sa2026.json", "w"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, default=str))
