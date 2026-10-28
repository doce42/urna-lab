"""T60a: lista de casos concretos (certificado × tabela × log × turnos) para os anos com extração pronta. Saída: resultados/casos_certificado.csv e .json"""
import glob, json, os
import numpy as np, pandas as pd
R = "."; OP = R + "/operacao_veracidade"; CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
casos, resumo = [], {}
for ano in ("2022", "2026"):
    if not all(os.path.exists(f"{OP}/resultados/certs_{ano}_{t}t.parquet") for t in (1, 2)):
        continue
    b = pd.read_parquet(f"{R}/analise/base.parquet" if ano == "2026" else f"{R}/analise/base_{ano}.parquet").astype({c: str for c in CH})
    cs = {t: pd.read_parquet(f"{OP}/resultados/certs_{ano}_{t}t.parquet").astype({c: str for c in CH}) for t in (1, 2)}
    urn = {t: pd.concat([pd.read_parquet(g, columns=CH + ["cert_igual_log", "ids_urna_log", "computado", "modelo"]) for g in glob.glob(f"{R}/analise/brutos/{('1t' if t == 1 else '2t') if ano == '2026' else f'{ano}_{t}t'}/urnas_*.parquet")]).astype({c: str for c in CH}) for t in (1, 2)}
    r = {}
    for t in (1, 2):
        c = cs[t][cs[t].cn != ""]
        j = c.merge(b[CH + [f"NR_URNA_EFETIVADA_{t}", f"QT_COMPARECIMENTO_{t}", f"validos_{t}"]], on=CH).merge(urn[t], on=CH)
        cnn = pd.to_numeric(j.cn.str.extract(r"(\d+)$")[0], errors="coerce"); tab = pd.to_numeric(j[f"NR_URNA_EFETIVADA_{t}"], errors="coerce")
        a = j[(cnn != tab) & tab.notna()]
        for x in a.itertuples(index=False):
            casos.append({"ano": ano, "turno": t, "tipo": "A_certificado_de_outra_urna_que_a_da_tabela", "SG_UF": x.SG_UF, "CD_MUNICIPIO": x.CD_MUNICIPIO, "NR_ZONA": x.NR_ZONA, "NR_SECAO": x.NR_SECAO, "cn_certificado": x.cn,
                          "urna_tabela": getattr(x, f"NR_URNA_EFETIVADA_{t}"), "ids_urna_log": x.ids_urna_log, "log_computado": x.computado, "comparecimento": getattr(x, f"QT_COMPARECIMENTO_{t}"), "votos_validos": getattr(x, f"validos_{t}")})
        d = c[c.duplicated("cn", keep=False)]
        for x in d.itertuples(index=False):
            casos.append({"ano": ano, "turno": t, "tipo": "F_mesmo_certificado_em_duas_secoes", "SG_UF": x.SG_UF, "CD_MUNICIPIO": x.CD_MUNICIPIO, "NR_ZONA": x.NR_ZONA, "NR_SECAO": x.NR_SECAO, "cn_certificado": x.cn})
        r[f"{t}t"] = {"secoes": int(len(j)), "A_cert_diferente_da_urna_da_tabela": int(len(a)), "A_votos_validos": int(a[f"validos_{t}"].sum()), "F_certificado_em_mais_de_uma_secao": int(d.cn.nunique())}
    j = cs[1].merge(cs[2], on=CH, suffixes=("_1", "_2")); j = j[(j.cert_sha256_1 != "") & (j.cert_sha256_2 != "")].merge(b[CH + ["NR_URNA_EFETIVADA_1", "NR_URNA_EFETIVADA_2"]], on=CH)
    dc = j.cert_sha256_1 != j.cert_sha256_2; dt = j.NR_URNA_EFETIVADA_1.astype(str) != j.NR_URNA_EFETIVADA_2.astype(str)
    for nome, m in (("B_certificado_mudou_entre_turnos_mas_urna_da_tabela_nao", dc & ~dt), ("C_urna_da_tabela_mudou_mas_certificado_nao", ~dc & dt)):
        for x in j[m].itertuples(index=False):
            casos.append({"ano": ano, "turno": "1e2", "tipo": nome, "SG_UF": x.SG_UF, "CD_MUNICIPIO": x.CD_MUNICIPIO, "NR_ZONA": x.NR_ZONA, "NR_SECAO": x.NR_SECAO, "cn_certificado": f"{x.cn_1} -> {x.cn_2}", "urna_tabela": f"{x.NR_URNA_EFETIVADA_1} -> {x.NR_URNA_EFETIVADA_2}"})
    r["entre_turnos"] = {"certificado_diferente": int(dc.sum()), "urna_da_tabela_diferente": int(dt.sum()), "ambos": int((dc & dt).sum()), "so_certificado": int((dc & ~dt).sum()), "so_tabela": int((~dc & dt).sum())}
    for t in (1, 2):
        c = cs[t][cs[t].emissor == "AC URNA"]; x = c[pd.to_datetime(c.nao_antes, utc=True) > pd.Timestamp("2026-07-18", tz="UTC")] if ano == "2026" else c.iloc[0:0]
        r[f"D_AC_URNA_emitidos_depois_de_18_07_2026_{t}t"] = int(len(x))
        for y in x.itertuples(index=False):
            casos.append({"ano": ano, "turno": t, "tipo": "D_certificado_emitido_depois_do_fim_da_validade_do_certificado_publico_da_AC_URNA", "SG_UF": y.SG_UF, "CD_MUNICIPIO": y.CD_MUNICIPIO, "NR_ZONA": y.NR_ZONA, "NR_SECAO": y.NR_SECAO, "cn_certificado": y.cn, "emitido_em": y.nao_antes[:10]})
    resumo[ano] = r
pd.DataFrame(casos).to_csv(f"{OP}/resultados/casos_certificado.csv", index=False)
json.dump(resumo, open(f"{OP}/resultados/casos_certificado.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(resumo, ensure_ascii=False, indent=1)); print(pd.DataFrame(casos).groupby(["ano", "tipo"]).size())
