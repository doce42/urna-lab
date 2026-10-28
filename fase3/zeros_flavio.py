"""T49: seções com zero voto para Flávio no 2º turno de 2026 (pré-registro em fase3/PREREG_ZEROS_FLAVIO.md)."""
import glob, json
import numpy as np, pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; OUT = RAIZ + "/fase3/resultados/zeros_flavio.json"
CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
REGIAO = {**dict.fromkeys(["AC", "AM", "AP", "PA", "RO", "RR", "TO"], "Norte"),
          **dict.fromkeys(["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"], "Nordeste"),
          **dict.fromkeys(["DF", "GO", "MS", "MT"], "Centro-Oeste"), **dict.fromkeys(["ES", "MG", "RJ", "SP"], "Sudeste"),
          **dict.fromkeys(["PR", "RS", "SC"], "Sul"), "ZZ": "Exterior"}
R = {"pre_registro": "fase3/PREREG_ZEROS_FLAVIO.md"}


def base(ano):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet").astype({c: str for c in CH})
    b["regiao"] = b.SG_UF.map(REGIAO)
    return b


def zerados(b):
    z = b[(b.v22_2.fillna(0) == 0) & (b.validos_2 > 0)]
    br = z[z.SG_UF != "ZZ"]
    return z, {"secoes_brasil": int(len(br)), "votos_lula_brasil": int(br.v13_2.sum()), "secoes_exterior": int((z.SG_UF == "ZZ").sum()),
               "votos_lula_exterior": int(z[z.SG_UF == "ZZ"].v13_2.sum()), "por_regiao": br.regiao.value_counts().to_dict(),
               "por_uf": br.SG_UF.value_counts().to_dict(), "validos_ge_20": int((br.validos_2 >= 20).sum())}


def viradas(b):
    m = b[b.SG_UF != "ZZ"].groupby(["SG_UF", "CD_MUNICIPIO"])[["v13_1", "v22_1", "v13_2", "v22_2", "QT_APTOS_2"]].sum()
    v = m[(m.v22_1 > m.v13_1) & (m.v13_2 > m.v22_2)]
    return v, {"municipios_22_lider_1t_13_vence_2t": int(len(v)), "por_uf": v.reset_index().SG_UF.value_counts().to_dict(),
               "inverso_13_lider_1t_22_vence_2t": int(((m.v13_1 > m.v22_1) & (m.v22_2 > m.v13_2)).sum())}


b26, b22 = base("2026"), base("2022")
z26, R["a_2026"] = zerados(b26)
nomes = b26.drop_duplicates(["SG_UF", "CD_MUNICIPIO"]).set_index(["SG_UF", "CD_MUNICIPIO"]).NM_MUNICIPIO_2
am = z26[z26.SG_UF == "AM"]
R["a_2026"]["amazonas_municipios"] = sorted(set(nomes.loc[list(zip(am.SG_UF, am.CD_MUNICIPIO))]))
R["a_2026"]["maiores_secoes"] = z26.nlargest(10, "v13_2")[CH + ["NM_MUNICIPIO_2", "v13_2", "validos_2"]].to_dict("records")
v26, R["e_2026"] = viradas(b26)
rj = b26[(b26.SG_UF == "RJ") & (b26.NM_MUNICIPIO_2.str.upper() == "RIO DE JANEIRO")]
R["e_2026"]["rio_de_janeiro"] = {"aptos": int(rj.QT_APTOS_2.sum()), "vantagem_13_2t": int(rj.v13_2.sum() - rj.v22_2.sum()),
                                 "vantagem_22_1t": int(rj.v22_1.sum() - rj.v13_1.sum())}
z22, R["b_2022"] = zerados(b22)
_, R["e_2022"] = viradas(b22)

# (c) continuidade seção a seção
c = z26[z26.SG_UF != "ZZ"][CH + ["v13_1", "v22_1", "validos_1", "v13_2", "validos_2"]].merge(
    b22[CH + ["v13_2", "v22_2", "validos_2"]].rename(columns={"v13_2": "l22", "v22_2": "b22", "validos_2": "val22"}), on=CH, how="left")
c["prop_b22"] = c.b22 / (c.l22 + c.b22)
R["c_continuidade"] = {"com_par_em_2022": int(c.b22.notna().sum()), "sem_par_em_2022": int(c.b22.isna().sum()),
                       "tambem_zero_em_2022": int((c.b22 == 0).sum()), "prop_bolsonaro_2022_mediana": float(c.prop_b22.median()),
                       "prop_bolsonaro_2022_max": float(c.prop_b22.max()), "com_bolsonaro_2022_ge_20pct": int((c.prop_b22 >= .2).sum()),
                       "flavio_zero_tambem_no_1t_2026": int((c.v22_1.fillna(0) == 0).sum()),
                       "flavio_1t_2026_mediana_pct": float((c.v22_1 / c.validos_1).median()),
                       "lista_ge_20pct": c[c.prop_b22 >= .2][CH + ["v13_2", "validos_2", "l22", "b22", "v22_1"]].to_dict("records")}

# (d) integridade nos arquivos da urna
u = pd.concat([pd.read_parquet(f, columns=CH + ["modelo", "assin_lista_ok", "hash_ok_bu", "assin_ok_bu", "hash_ok_rdv", "assin_ok_rdv",
                                                "hash_ok_log", "assin_ok_log", "bu_v13", "bu_v22", "rdv_v13", "rdv_v22"])
               for f in glob.glob(f"{AN}/brutos/2t/urnas_*.parquet")]).astype({c: str for c in CH})
d = z26.merge(u, on=CH, how="left")
assin = d[["assin_lista_ok", "hash_ok_bu", "assin_ok_bu", "hash_ok_rdv", "assin_ok_rdv", "hash_ok_log", "assin_ok_log"]].fillna(False).astype(bool).all(axis=1)
lido = d.bu_v13.notna()
votos = lido & (d.bu_v13.fillna(0) == d.rdv_v13.fillna(0)) & (d.bu_v13.fillna(0) == d.v13_2) & (d.bu_v22.fillna(0) == 0) & (d.rdv_v22.fillna(0) == 0)
R["d_integridade"] = {"secoes": int(len(d)), "assinaturas_ok": int(assin.sum()), "bu_lido": int(lido.sum()), "bu_rdv_tabela_iguais": int(votos.sum()),
                      "por_modelo": d.modelo.value_counts(dropna=False).astype(int).to_dict(),
                      "falhas": d[~(assin & votos)][CH + ["modelo"]].astype(str).to_dict("records")}
json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str)[:6000])
