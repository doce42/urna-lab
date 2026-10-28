"""Z2 (fase3/PREREG_FINAL.md): o que são as 'verificações de assinatura do software sem sucesso' no log das urnas de 2026, quando
ocorrem, e as urnas com essas linhas votam diferente? Saída: fase3/resultados/final_t33.json."""
import collections, glob, json, os, re, sys, zipfile
import numpy as np, pandas as pd

os.environ["ANO"] = "2026"
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); sys.path.insert(0, RAIZ + "/analise")
import processar_brutos as pb  # noqa: E402
src = open(RAIZ + "/fase3/adv_casos.py").read().split('R = {"pre_registro"')[0]; exec(src)   # base(), teste(), K

DIA = {1: "04/10/2026", 2: "25/10/2026"}
R = {"pre_registro": "fase3/PREREG_FINAL.md (Z2)"}
b26 = base("2026")
for t, pasta, pas in ((1, "1turno", "1t"), (2, "2turno_pacotes", "2t")):
    u = pd.concat([pd.read_parquet(f, columns=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "sw_verif_falha", "sw_verif_ok", "modelo"]) for f in glob.glob(f"{RAIZ}/analise/brutos/{pas}/urnas_*.parquet")], ignore_index=True)
    alvo = u[u.sw_verif_falha.fillna(0) > 0].copy(); alvo["k"] = [K(*r) for r in zip(alvo.SG_UF, alvo.CD_MUNICIPIO, alvo.NR_ZONA, alvo.NR_SECAO)]
    textos = collections.Counter(); momentos = collections.Counter(); por_modelo = alvo.modelo.value_counts().to_dict(); exemplos = []
    zips = {}
    for _, r in alvo.iterrows():
        uf = r.SG_UF
        if uf not in zips:
            pc = glob.glob(f"{RAIZ}/dados/brutos/{pasta}/*_{uf}.zip"); zips[uf] = zipfile.ZipFile(pc[0]) if pc else None
        zf = zips[uf]
        if zf is None: continue
        cod = f"{uf.lower()}{int(r.CD_MUNICIPIO):05d}{int(r.NR_ZONA):04d}{int(r.NR_SECAO):04d}-log.jez"
        nome = next((n for n in zf.namelist() if n.endswith(cod)), None)
        if not nome: continue
        linhas, _ = pb.linhas_do_log(zf.read(nome))
        for l in linhas:
            p = l.split("\t")
            if len(p) < 5 or not p[4].startswith("Verificação de assinatura") or "SUCESSO" in p[4].upper(): continue
            msg = re.sub(r"\d+", "#", p[4])[:140]; textos[msg] += 1
            hora = p[0][11:16] if len(p[0]) >= 16 else "?"; dia = p[0][:10]
            mom = "outro dia" if dia != DIA[t] else ("antes das 8h" if hora < "08:00" else ("8h às 17h" if hora < "17:00" else "depois das 17h"))
            momentos[mom] += 1
            if len(exemplos) < 8: exemplos.append({"secao": r.k, "linha": l[:220]})
    teste_votos = teste(b26, set(alvo.k), 0.3, 9910 + t)
    R[f"{t}T"] = {"urnas": int(len(alvo)), "linhas_por_texto": dict(textos.most_common(10)), "linhas_por_momento": dict(momentos), "por_modelo": por_modelo, "exemplos": exemplos,
                  "teste_de_votos": teste_votos}
    print(t, len(alvo), dict(textos.most_common(5)), dict(momentos), por_modelo, "| votos:", round(teste_votos.get("diferenca", 0), 3), teste_votos.get("p_bilateral_media"), teste_votos.get("leitura"), flush=True)
json.dump(R, open(RAIZ + "/fase3/resultados/final_t33.json", "w"), ensure_ascii=False, indent=1, default=float)
