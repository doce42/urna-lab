"""F3 / fila F3: as 10 seções-turno de 2022 cujo boletim não foi lido pelo leitor do projeto. Ver fase3/PREREG_FILA.md.
Saída: fase3/resultados/fila_f3_semboletim.json."""
import hashlib, json, os, re, sys, zipfile
import pandas as pd

os.environ["ANO"] = "2022"
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); sys.path.insert(0, RAIZ + "/analise")
import processar_brutos as pb  # noqa: E402

SECOES = [(1, "ZZ", 29505, 1, 78), (1, "ZZ", 29564, 1, 91), (1, "ZZ", 29505, 1, 79), (1, "ZZ", 29416, 1, 38), (1, "PA", 4383, 91, 73),
          (2, "RS", 86568, 100, 15), (2, "PA", 4499, 17, 41), (2, "ZZ", 29505, 1, 78), (2, "ZZ", 29564, 1, 91), (2, "ZZ", 29505, 1, 79)]
base = pd.read_parquet(RAIZ + "/analise/base_2022.parquet")
out = []
for t, uf, m, z, s in SECOES:
    cod = f"{m:05d}{z:04d}{s:04d}"; zf = zipfile.ZipFile(f"{RAIZ}/dados/2022/brutos/{t}turno/bu_imgbu_logjez_rdv_vscmr_2022_{t}t_{uf}.zip")
    arqs = {n.rsplit(".", 1)[1]: n for n in zf.namelist() if cod in n}
    row = base[(base.SG_UF == uf) & (base.CD_MUNICIPIO.astype(int) == m) & (base.NR_ZONA.astype(int) == z) & (base.NR_SECAO.astype(int) == s)]
    pub = None
    if len(row) and not pd.isna(row.iloc[0][f"total_{t}"]):
        r0 = row.iloc[0]; pub = {c.rsplit("_", 1)[0]: int(r0[c]) for c in r0.index if re.fullmatch(rf"v\d+_{t}|branco_{t}|nulo_{t}", c) and not pd.isna(r0[c])}
        pub["comparecimento"] = int(r0[f"QT_COMPARECIMENTO_{t}"]); pub["tipo_urna"] = r0[f"DS_TIPO_URNA_{t}"]; pub["agregadas"] = r0[f"DS_SECOES_AGREGADAS_{t}"]
    L = {"turno": t, "secao": f"{uf}/{m}/{z}/{s}", "arquivos": sorted(arqs.values()), "publicado": pub}
    bol = arqs.get("bu") or arqs.get("busa")
    if bol:
        try:
            bu = pb.ler_bu(zf.read(bol), t); L["boletim"] = {k: v for k, v in bu.items()}
            if pub: L["boletim_x_tabela"] = {c: (bu.get("bu_" + c, 0), v) for c, v in pub.items() if c not in ("comparecimento", "tipo_urna", "agregadas") and bu.get("bu_" + c, 0) != v}
        except Exception as e: L["erro_boletim"] = repr(e)[:200]
    vsc = arqs.get("vscmr") or arqs.get("vscsa")
    if vsc:
        try:
            lista, resumo, verifica = pb.ler_vsc(zf.read(vsc)); L["assinatura"] = resumo
            L["arquivos_conferidos"] = {n: bool(lista.get(n) is not None and lista[n][:2] == (len(zf.read(n)), hashlib.sha512(zf.read(n)).digest()) and verifica(lista[n][2], lista[n][1])) for n in arqs.values() if n != vsc}
            L["listados_e_ausentes"] = sorted(x for x in lista if x not in arqs.values())
        except Exception as e: L["erro_assinatura"] = repr(e)[:200]
    img = arqs.get("imgbu") or arqs.get("imgbusa")
    if img:
        try: L["imagem"] = pb.ler_imgbu(zf.read(img))
        except Exception as e: L["erro_imagem"] = repr(e)[:200]
    if not arqs: L["classe"] = "não verificável: nenhum arquivo da seção no pacote"
    elif not bol: L["classe"] = "não verificável: sem boletim no pacote"
    elif "erro_boletim" in L: L["classe"] = "não verificável: boletim presente e não decodificado"
    elif L.get("boletim_x_tabela"): L["classe"] = "divergência objetiva boletim × tabela"
    elif pub is None: L["classe"] = "boletim lido; seção ausente da tabela"
    else: L["classe"] = "boletim lido e igual à tabela (consistência interna)"
    out.append(L); print(L["turno"], L["secao"], L["classe"], [a.rsplit(".", 1)[1] for a in L["arquivos"]], L.get("boletim_x_tabela"), (L.get("assinatura") or {}).get("assin_lista_ok"), flush=True)
json.dump({"pergunta": "fila F3", "secoes": out}, open(RAIZ + "/fase3/resultados/fila_f3_semboletim.json", "w"), ensure_ascii=False, indent=1, default=str)
