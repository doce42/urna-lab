"""Verificação A (Adendo 2): até 20 seções do 1º turno de 2026. Seleção conforme PREREG.md. Uma execução."""
import sys, os, json, glob, hashlib, zipfile, collections
import numpy as np, pandas as pd
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AQ = RAIZ + "/analise"
sys.path.insert(0, AQ); os.chdir(AQ)
import processar_brutos as P, der
AQUI = os.path.dirname(os.path.abspath(__file__))

casos = json.load(open(AQ + "/resultado_casos_integridade_1t.json"))["casos_lista"]
chave = lambda c: (c["uf"], str(c["municipio"]), str(c["zona"]), str(c["secao"]))
casos = sorted(casos, key=lambda c: tuple(map(str, chave(c))))
obrig = [c for c in casos if c["grau"] == "sem_explicacao" or "d_fora_do_bu" in c["tipos"]]
rest = [c for c in casos if c not in obrig]
rng = np.random.default_rng(2026)
exc = obrig + [rest[i] for i in rng.choice(len(rest), 10 - len(obrig), replace=False)]
exc_keys = {chave(c) for c in exc}
# universo de urnas
univ = pd.concat([pd.read_parquet(f, columns=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]) for f in sorted(glob.glob(AQ + "/brutos/1t/urnas_*.parquet"))], ignore_index=True)
univ = univ.astype(str).drop_duplicates()
univ = univ[~univ.apply(lambda r: tuple(r) in exc_keys, axis=1)].reset_index(drop=True)
rnd = univ.iloc[np.random.default_rng(2027).choice(len(univ), 10, replace=False)]
sel = [("excecao", chave(c), c["tipos"], c["grau"]) for c in exc] + [("aleatoria", tuple(r), [], "") for r in rnd.itertuples(index=False)]


def ints_e_textos(no, acc):
    if no.get("k"):
        for f in no["f"]: ints_e_textos(f, acc)
    else:
        v = no.get("v", b"")
        if len(v) <= 8: acc["int"].add(int.from_bytes(v, "big"))
        try: acc["txt"].add(v.decode("ascii"))
        except Exception: pass

zips = {}; res = []
for grupo, (uf, mun, zona, sec), tipos, grau in sel:
    r = {"grupo": grupo, "uf": uf, "mun": mun, "zona": zona, "secao": sec, "tipos_t36": tipos, "grau_t36": grau}
    pacote, _ = P.fonte(1, uf)
    if not os.path.exists(pacote): r["erro"] = "sem pacote"; res.append(r); continue
    zf = zips.setdefault(uf, zipfile.ZipFile(pacote))
    mem = {}
    for n in zf.namelist():
        a = P.analisa_nome(n, uf)
        if a and a[0] == (uf, mun, zona, sec): mem[a[1]] = n
    r["arquivos"] = sorted(mem)
    if not mem: r["erro"] = "seção sem arquivos no pacote (esperado para sistema de apuração/exterior)"; res.append(r); continue
    dados = {t: zf.read(n) for t, n in mem.items()}
    r["nomes"] = {t: mem[t] for t in mem}
    lista, resumo, ver = P.ler_vsc(dados["vota"]) if "vota" in dados else (None, {}, None)
    r.update({k: resumo.get(k) for k in ("algoritmo", "cert_urna", "cert_emissor", "assin_lista_ok")})
    r["lista_assinada_itens"] = sorted(lista) if lista else None
    for t, d in dados.items():
        if t == "vota": continue
        it = lista.get(mem[t]) if lista else None
        r[f"sha512_{t}"] = hashlib.sha512(d).hexdigest()[:16]
        r[f"hash_ok_{t}"] = bool(it and it[:2] == (len(d), hashlib.sha512(d).digest()))
        r[f"assin_ok_{t}"] = bool(it and ver(it[2], it[1]))
    # conteúdo
    bu = P.ler_bu(dados["bu"], 1) if "bu" in dados else {}
    try: rdv = P.ler_rdv(dados["rdv"], 1) if "rdv" in dados else {}
    except (KeyError, IndexError): rdv = {}; r["rdv_vazio_ou_outro_formato"] = True
    img = P.ler_imgbu(dados["imgbu"]) if "imgbu" in dados else None
    lg = P.ler_log(dados["log"], 1)[0] if "log" in dados else {}
    cand = lambda d, p: {k[len(p) + 1:]: v for k, v in d.items() if k.startswith(p + "_v")}
    r["bu"] = {k: v for k, v in bu.items() if k.startswith(("bu_v", "bu_b", "bu_n", "bu_comp", "bu_aptos"))}
    r["rdv_igual_bu"] = (all(rdv.get("rdv_" + k[3:], 0) == v for k, v in bu.items() if k.startswith("bu_v"))
                         and rdv.get("rdv_branco", 0) == bu.get("bu_branco", 0) and rdv.get("rdv_nulo", 0) == bu.get("bu_nulo", 0)) if rdv else None
    r["img_igual_bu"] = (all(img.get("img_" + k[3:], 0) == v for k, v in bu.items() if k.startswith("bu_v"))
                         and img.get("img_branco") == bu.get("bu_branco") and img.get("img_nulo") == bu.get("bu_nulo")) if img else None
    r["log"] = {k: lg.get(k) for k in ("computado", "modelo", "ids_urna_log", "urnas_com_voto_no_log", "primeiro_voto", "ultimo_voto")}
    r["log_computado_igual_comparecimento_bu"] = lg.get("computado") == bu.get("bu_comparecimento") if lg and bu else None
    # identidade heurística: inteiros/textos do bu.dat contêm zona, seção, município?
    if "bu" in dados:
        env, _ = der.ler(dados["bu"]); inner, _ = der.ler(env["f"][4]["v"])
        acc = {"int": set(), "txt": set()}; ints_e_textos(inner, acc)
        r["identidade_no_bu"] = {"secao": int(sec) in acc["int"], "zona": int(zona) in acc["int"], "municipio": int(mun) in acc["int"],
                                 "uf_texto": uf in acc["txt"] or uf.lower() in acc["txt"]}
    res.append(r)
# confronto com BU na Web
for uf in {r["uf"] for r in res if "bu" in r}:
    f = f"{RAIZ}/dados/1turno/bweb_1t_{uf}_presidente.csv"
    ks = {(r["mun"], r["zona"], r["secao"]): r for r in res if r["uf"] == uf and "bu" in r}
    for ch in pd.read_csv(f, sep=";", encoding="latin1", dtype=str, chunksize=400000,
                          usecols=["CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_VOTAVEL", "QT_VOTOS", "QT_COMPARECIMENTO", "DS_TIPO_VOTAVEL", "QT_APTOS"]):
        ch["k"] = list(zip(ch.CD_MUNICIPIO.astype(int).astype(str), ch.NR_ZONA.astype(int).astype(str), ch.NR_SECAO.astype(int).astype(str)))
        for k, g in ch[ch.k.isin(list(ks))].groupby("k"):
            ks[k].setdefault("_web", []).append(g)
for r in res:
    if "_web" in r:
        g = pd.concat(r.pop("_web")); web = {}
        for x in g.itertuples():
            n = x.NR_VOTAVEL; t = x.DS_TIPO_VOTAVEL.lower()
            nm = "branco" if "branco" in t else "nulo" if "nulo" in t else f"v{int(n)}"
            web[nm] = web.get(nm, 0) + int(x.QT_VOTOS)
        bu = r["bu"]; bun = {k[3:]: v for k, v in bu.items() if k.startswith(("bu_v", "bu_branco", "bu_nulo"))}
        r["web"] = {"votos": web, "comparecimento": int(g.QT_COMPARECIMENTO.iloc[0]), "aptos": int(g.QT_APTOS.iloc[0])}
        r["web_igual_bu"] = all(web.get(k, 0) == v for k, v in bun.items()) and set(k for k in web if web[k]) <= set(k for k in bun if bun[k]) | set()
        r["web_comparecimento_igual_bu"] = r["web"]["comparecimento"] == bu.get("bu_comparecimento")
json.dump({"selecao": [{"grupo": s[0], "chave": s[1]} for s in sel], "resultados": res}, open(AQUI + "/va_resultado.json", "w"), indent=1, ensure_ascii=False, default=str)
print("ok", len(res))
