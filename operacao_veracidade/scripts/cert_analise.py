"""T60a: análise dos certificados de todas as urnas (usa o que existir de resultados/certs_<ano>_<turno>t.parquet)."""
import base64, glob, json, os
import numpy as np, pandas as pd
from cryptography import x509
R = "."; OP = R + "/operacao_veracidade"; AN = R + "/analise"
CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
acs = {}
for nome in ("acurna", "acue2020", "acue2022"):
    c = x509.load_pem_x509_certificate(open(f"{R}/fase2/externos/certificados/{nome}_certificado_publico.txt", "rb").read())
    acs[c.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value] = {"nao_antes": c.not_valid_before_utc.isoformat(), "nao_depois": c.not_valid_after_utc.isoformat()}
out = {"acs_usadas": acs, "conjuntos": {}}
dias = {("2026", 1): "2026-10-04", ("2026", 2): "2026-10-25", ("2022", 1): "2022-10-02", ("2022", 2): "2022-10-30"}
por_ano = {}
for ano in ("2022", "2026"):
    dfs = {}
    for t in (1, 2):
        f = f"{OP}/resultados/certs_{ano}_{t}t.parquet"
        if os.path.exists(f):
            d = pd.read_parquet(f); d = d.astype({c: str for c in CH}); dfs[t] = d
            u = d.drop_duplicates("cert_sha256"); u = u[u.cert_sha256 != ""]
            pasta = ("1t" if ano == "2026" and t == 1 else "2t" if ano == "2026" else f"2022_{t}t")
            modelo = pd.concat([pd.read_parquet(g, columns=CH + ["modelo", "cert_igual_log"]) for g in glob.glob(f"{AN}/brutos/{pasta}/urnas_*.parquet")]).astype({c: str for c in CH})
            m = d.merge(modelo, on=CH, how="left")
            nb = pd.to_datetime(d.nao_antes, utc=True, errors="coerce"); dia = pd.Timestamp(dias[(ano, t)], tz="UTC")
            r = {"secoes_com_certificado": int((d.cert_sha256 != "").sum()), "erros_de_leitura": int((d.erro != "").sum()), "certificados_unicos": int(len(u)),
                 "cadeia": {"verifica": int((d.cadeia_ok == True).sum()), "falha": int((d.cadeia_ok == False).sum()), "sem_AC_disponivel": int(d.cadeia_ok.isna().sum() - (d.erro != "").sum())},
                 "cadeia_por_emissor": d[d.cert_sha256 != ""].groupby("emissor").cadeia_ok.agg(lambda s: {"ok": int((s == True).sum()), "falha": int((s == False).sum())}).to_dict(),
                 "validade": {"validos_no_dia": int((d.valido_no_dia == True).sum()), "nao_validos_no_dia": int((d.valido_no_dia == False).sum()), "emitidos_depois_da_eleicao": int((d.emitido_depois_da_eleicao == True).sum()),
                              "emitidos_nos_30_dias_antes": int(((dia - nb).dt.days.between(0, 30)).sum()), "emitidos_nos_90_dias_antes": int(((dia - nb).dt.days.between(0, 90)).sum())},
                 "emissor_por_modelo": m.groupby(["modelo", "emissor"]).size().unstack(fill_value=0).to_dict("index"),
                 "cn_em_mais_de_uma_secao": int(d[d.cn != ""].groupby("cn").size().gt(1).sum()), "cn_com_mais_de_um_certificado": int((u.groupby("cn").cert_sha256.nunique() > 1).sum()),
                 "mesma_chave_publica_em_cn_diferentes": int((u.groupby("pub_sha256").cn.nunique() > 1).sum()), "mesmo_certificado_em_cn_diferentes": int((u.groupby("cert_sha256").cn.nunique() > 1).sum()),
                 "emitidos_depois_do_fim_de_validade_da_AC_publicada": {k: int(((u.emissor == k) & (pd.to_datetime(u.nao_antes, utc=True) > pd.Timestamp(v["nao_depois"]))).sum()) for k, v in acs.items()}}
            if "cert_igual_log" in m:
                r["cert_igual_urna_no_log"] = {"sim": int((m.cert_igual_log == True).sum()), "nao": int((m.cert_igual_log == False).sum())}
            out["conjuntos"][f"{ano}_{t}t"] = r
    if 1 in dfs and 2 in dfs:
        j = dfs[1].merge(dfs[2], on=CH, suffixes=("_1", "_2"))
        j = j[(j.cert_sha256_1 != "") & (j.cert_sha256_2 != "")]
        out["conjuntos"][f"{ano}_entre_turnos"] = {"secoes_nos_dois_turnos": int(len(j)), "mesmo_certificado": int((j.cert_sha256_1 == j.cert_sha256_2).sum()), "certificado_diferente_na_mesma_secao": int((j.cert_sha256_1 != j.cert_sha256_2).sum()),
                                                  "mesmo_CN": int((j.cn_1 == j.cn_2).sum()), "CN_diferente": int((j.cn_1 != j.cn_2).sum())}
json.dump(out, open(f"{OP}/resultados/cert_analise.json", "w"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(out, ensure_ascii=False, indent=1, default=str)[:7000])
