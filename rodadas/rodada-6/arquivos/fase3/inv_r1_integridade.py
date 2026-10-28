"""F3 / R1: tabela publicada × boletim (bu.dat) × recontagem pelo RDV × boletim impresso, seção a seção, e hash/assinatura,
pelos arquivos já decodificados (analise/brutos/*/urnas_*.parquet). 2022 e 2026, dois turnos. Validação: 100 seções de 2022
decodificadas de novo direto dos zips. Ver fase3/PREREG_RESPOSTAS.md (R1). Saída: fase3/resultados/r1_integridade.json."""
import glob, json, os, re, sys, zipfile
import numpy as np, pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"
K = lambda d: d.SG_UF.astype(str) + "/" + d.CD_MUNICIPIO.astype(int).astype(str) + "/" + d.NR_ZONA.astype(int).astype(str) + "/" + d.NR_SECAO.astype(int).astype(str)
R = {"pergunta": "R1", "correcao": "1ª execução: comparador somava NaN + nulos por suspensão (resultado NaN, contado como diferença) e a validação usava NaN or 0; corrigido e repetido uma vez", "regra": "divergência só com arquivo lido (valor presente); RDV: nulo inclui nulo por suspensão (tipo 6)"}


def compara(ano, t):
    base = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
    base = base[base[f"total_{t}"].notna()].copy(); base["k"] = K(base); base = base.drop_duplicates("k").set_index("k")
    pas = f"{t}t" if ano == "2026" else f"{ano}_{t}t"
    u = pd.concat([pd.read_parquet(f) for f in glob.glob(f"{AN}/brutos/{pas}/urnas_*.parquet")], ignore_index=True)
    u["k"] = K(u); u = u.drop_duplicates("k").set_index("k")
    m = u.join(base, how="inner", rsuffix="_b") if False else u.join(base.drop(columns=[c for c in base.columns if c in u.columns]), how="inner")
    out = {"secoes_tabela": int(len(base)), "secoes_com_linha_de_arquivo": int(len(u)), "pareadas": int(len(m))}
    for fonte in ("bu", "rdv", "img"):
        campos = ["v13", "v22", "branco", "nulo"]
        lidas = m[f"{fonte}_v13"].notna() if f"{fonte}_v13" in m else pd.Series(False, index=m.index)
        dif = pd.Series(False, index=m.index)
        for c in campos:
            col = f"{fonte}_{c}"
            if col not in m: continue
            val = m[col].astype(float)
            if fonte == "rdv" and c == "nulo" and "rdv_tipo6" in m: val = val.fillna(0) + m["rdv_tipo6"].fillna(0)   # correção: NaN + tipo6 virava NaN
            pub = m[f"{c}_{t}"].astype(float)
            dif |= lidas & (val.fillna(0) != pub.fillna(0))
        out[fonte] = {"lidas": int(lidas.sum()), "iguais_nos_4_campos": int((lidas & ~dif).sum()), "diferentes": int(dif.sum()),
                      "exemplos_diferentes": m.index[dif].tolist()[:10]}
    if "bu_comparecimento" in m:
        lid = m["bu_comparecimento"].notna()
        out["bu_comparecimento_diferente"] = int((lid & (m["bu_comparecimento"] != m[f"QT_COMPARECIMENTO_{t}"])).sum())
    for tipo in ("bu", "rdv", "log", "imgbu"):
        h, a = f"hash_ok_{tipo}", f"assin_ok_{tipo}"
        if h in u:
            pres = u[h].notna()
            out[f"arquivo_{tipo}"] = {"com_conferencia": int(pres.sum()), "hash_ok": int((u[h] == True).sum()), "assinatura_ok": int((u.get(a) == True).sum()) if a in u else None}
    if "assin_lista_ok" in u: out["lista_assinada_ok"] = int((u["assin_lista_ok"] == True).sum()); out["lista_lida"] = int(u["assin_lista_ok"].notna().sum())
    so_tab = base.index.difference(u.index)
    out["secoes_da_tabela_sem_linha_de_arquivo"] = int(len(so_tab)); out["sem_linha_por_uf"] = pd.Series([k.split("/")[0] for k in so_tab]).value_counts().head(5).to_dict()
    return out, m


for ano in ("2022", "2026"):
    for t in (1, 2):
        r, m = compara(ano, t); R[f"{ano}_{t}T"] = r
        print(ano, t, {k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "exemplos_diferentes"}) for k, v in r.items()}, flush=True)

# validação: 100 seções de 2022 decodificadas de novo direto dos zips
os.environ["ANO"] = "2022"; sys.path.insert(0, AN)
import processar_brutos as pb  # noqa: E402
rng = np.random.default_rng(9100); val = []
for t in (1, 2):
    r, m = compara("2022", t); cand = m[m["bu_v13"].notna() & (m.SG_UF != "ZZ")]
    for k in rng.choice(cand.index, 50, replace=False):
        uf, mu, z, s = k.split("/"); cod = f"{int(mu):05d}{int(z):04d}{int(s):04d}"
        zf = zipfile.ZipFile(f"{RAIZ}/dados/2022/brutos/{t}turno/bu_imgbu_logjez_rdv_vscmr_2022_{t}t_{uf}.zip")
        nome = next(n for n in zf.namelist() if n.endswith(cod + ".bu"))
        bu = pb.ler_bu(zf.read(nome), t)
        rdvn = next((n for n in zf.namelist() if n.endswith(cod + ".rdv")), None)
        rdv = pb.ler_rdv(zf.read(rdvn), t) if rdvn else {}
        z0 = lambda x: 0 if pd.isna(x) else x   # correção: NaN or 0 continuava NaN
        ok = all(bu.get(f"bu_{c}", 0) == z0(m.loc[k, f"bu_{c}"]) for c in ("v13", "v22", "branco", "nulo")) and \
             all(rdv.get(f"rdv_{c}", 0) == z0(m.loc[k, f"rdv_{c}"]) for c in ("v13", "v22", "branco", "nulo", "tipo6"))
        val.append({"turno": t, "secao": k, "igual_ao_parquet": bool(ok)})
R["validacao_releitura_100_secoes_2022"] = {"secoes": len(val), "identicas": sum(v["igual_ao_parquet"] for v in val), "diferentes": [v for v in val if not v["igual_ao_parquet"]]}
print("validação", R["validacao_releitura_100_secoes_2022"]["identicas"], "de", len(val))
json.dump(R, open(f"{RAIZ}/fase3/resultados/r1_integridade.json", "w"), ensure_ascii=False, indent=1, default=str)
