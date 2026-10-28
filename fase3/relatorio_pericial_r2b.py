"""Rodada 8, R2b (exploratório): sensibilidade do corte das 17h, composição e comparação dentro do município."""
import json
import numpy as np, pandas as pd
R = "."; AN = R + "/analise"
b = pd.read_parquet(f"{AN}/base.parquet"); b["mun"] = b.SG_UF + "|" + b.CD_MUNICIPIO.astype(str)
x = b[b.DT_ENCERRAMENTO_2.notna() & (b.validos_2 > 0)].copy(); x["enc"] = pd.to_datetime(x.DT_ENCERRAMENTO_2); dia = pd.Timestamp("2026-10-25"); x["h"] = (x.enc - dia).dt.total_seconds()
ab = pd.to_datetime(b.DT_ABERTURA_2); ok = ab.dt.hour.between(6, 8) & (ab.dt.minute < 15); fz = (8 - ab.dt.hour)[ok].groupby(b.mun[ok]).agg(lambda v: v.mode().iloc[0]); x["fuso"] = x.mun.map(fz)
out = {"rotulo": "exploratorio_depois_do_R2"}
s = lambda g: {"secoes": int(len(g)), "comparecimento": int(g.QT_COMPARECIMENTO_2.sum()), "pct_lula": float(100 * g.v13_2.sum() / (g.v13_2.sum() + g.v22_2.sum())) if len(g) else None, "vantagem_lula": int(g.v13_2.sum() - g.v22_2.sum())}
cortes = {"17:00:59": 17 * 3600 + 59, "17:01:59": 17 * 3600 + 119, "17:02:59": 17 * 3600 + 179, "17:05:59": 17 * 3600 + 359, "17:10:59": 17 * 3600 + 659, "17:15:59": 17 * 3600 + 959, "17:30:00": 17 * 3600 + 1800, "19:00:00": 19 * 3600}
out["a_sensibilidade_do_corte"] = {k: {"antes": s(x[x.h <= v]), "depois": s(x[x.h > v])} for k, v in cortes.items()}
g1 = x[x.h <= 17 * 3600 + 59]; g2 = x[(x.h > 17 * 3600 + 59) & (x.h < 17 * 3600 + 960)]
out["b_composicao"] = {"fuso_ate_17h00_59": g1.fuso.value_counts(dropna=False).to_dict(), "fuso_17h01_a_17h15": g2.fuso.value_counts(dropna=False).to_dict(),
                       "pct_dos_votos_por_regiao": {nome: {"ate_17h00_59": float(100 * g1[g1.SG_UF.isin(ufs)].QT_COMPARECIMENTO_2.sum() / g1.QT_COMPARECIMENTO_2.sum()), "17h01_a_17h15": float(100 * g2[g2.SG_UF.isin(ufs)].QT_COMPARECIMENTO_2.sum() / g2.QT_COMPARECIMENTO_2.sum())}
                                                    for nome, ufs in {"Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"], "Sudeste": ["ES", "MG", "RJ", "SP"], "Sul": ["PR", "RS", "SC"], "Norte": ["AC", "AM", "AP", "PA", "RO", "RR", "TO"], "Centro-Oeste": ["DF", "GO", "MS", "MT"]}.items()},
                       "ufs_com_mais_secoes_ate_17h00_59": g1.SG_UF.value_counts().head(6).to_dict(), "ufs_com_mais_secoes_17h01_a_17h15": g2.SG_UF.value_counts().head(6).to_dict()}
def dentro(g, chave):
    t = x[x.h <= 17 * 3600 + 959]; t = t.assign(cedo=t.h <= 17 * 3600 + 59)
    a = t.groupby([chave, "cedo"]).agg(L=("v13_2", "sum"), F=("v22_2", "sum")).reset_index(); a["p"] = a.L / (a.L + a.F); a["n"] = a.L + a.F
    e = a[a.cedo].set_index(chave); l = a[~a.cedo].set_index(chave); c = e.index.intersection(l.index); w = np.minimum(e.loc[c, "n"], l.loc[c, "n"])
    return {"blocos_com_os_dois_grupos": int(len(c)), "diferenca_media_ponderada_pct_lula_tarde_menos_cedo_pontos": float(100 * np.average(l.loc[c, "p"] - e.loc[c, "p"], weights=w))}
out["c_dentro_do_bloco"] = {"municipio": dentro(x, "mun"), "uf": dentro(x, "SG_UF")}
cedo = x[x.h < 17 * 3600]; out["d_antes_das_17h00_00"] = {**s(cedo), "taxa_de_comparecimento_media_pct": float(100 * (cedo.QT_COMPARECIMENTO_2.sum() / cedo.QT_APTOS_2.sum())), "taxa_de_comparecimento_demais_pct": float(100 * (x[x.h >= 17 * 3600].QT_COMPARECIMENTO_2.sum() / x[x.h >= 17 * 3600].QT_APTOS_2.sum())), "mediana_de_aptos": float(cedo.QT_APTOS_2.median()), "mediana_de_aptos_demais": float(x[x.h >= 17 * 3600].QT_APTOS_2.median())}
json.dump(out, open(f"{R}/fase3/resultados/relatorio_pericial_r2b.json", "w"), ensure_ascii=False, indent=1, default=float)
for k, v in out["a_sensibilidade_do_corte"].items(): print(k, "antes", v["antes"]["secoes"], round(v["antes"]["pct_lula"], 2), v["antes"]["vantagem_lula"], "| depois", v["depois"]["secoes"], round(v["depois"]["pct_lula"], 2), v["depois"]["vantagem_lula"])
print(json.dumps({k: v for k, v in out.items() if k not in ("a_sensibilidade_do_corte",)}, ensure_ascii=False, indent=1, default=float))

# (e) fuso e hora de Brasília (acrescentado no mesmo adendo: a hora local mistura fusos)
x["enc_bsb"] = x.enc + pd.to_timedelta(x.fuso.fillna(0), unit="h"); x["hb"] = (x.enc_bsb - dia).dt.total_seconds()
cedo = x[x.h < 17 * 3600]
out["e_fuso_e_hora_de_brasilia"] = {"secoes_antes_das_17h00_local_por_fuso": cedo.fuso.value_counts(dropna=False).to_dict(), "secoes_antes_das_17h00_local_em_fuso_diferente_de_brasilia": int((cedo.fuso.fillna(0) != 0).sum()), "secoes_antes_das_17h00_local": int(len(cedo)),
                                    "ufs_antes_das_17h00_local": cedo.SG_UF.value_counts().head(8).to_dict(), "sensibilidade_em_hora_de_brasilia": {k: {"antes": s(x[x.hb <= v]), "depois": s(x[x.hb > v])} for k, v in cortes.items()}}
json.dump(out, open(f"{R}/fase3/resultados/relatorio_pericial_r2b.json", "w"), ensure_ascii=False, indent=1, default=float)
e = out["e_fuso_e_hora_de_brasilia"]; print("antes das 17h local por fuso:", e["secoes_antes_das_17h00_local_por_fuso"], "| UFs:", e["ufs_antes_das_17h00_local"])
for k, v in e["sensibilidade_em_hora_de_brasilia"].items(): print("BSB", k, "antes", v["antes"]["secoes"], round(v["antes"]["pct_lula"], 2), v["antes"]["vantagem_lula"], "| depois", v["depois"]["secoes"], round(v["depois"]["pct_lula"], 2), v["depois"]["vantagem_lula"])
