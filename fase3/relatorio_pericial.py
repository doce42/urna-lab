"""Rodada 8 (aberta): "Relatório Pericial Independente". Pré-registro: fase3/PREREG_RELATORIO_PERICIAL.md. Saída: fase3/resultados/relatorio_pericial.json"""
import json, glob
import numpy as np, pandas as pd

R = "."; AN = R + "/analise"; OUT = R + "/fase3/resultados/relatorio_pericial.json"
rng = np.random.default_rng(88)
out = {"pre_registro": "fase3/PREREG_RELATORIO_PERICIAL.md"}


def base(ano):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
    b["mun"] = b.SG_UF + "|" + b.CD_MUNICIPIO.astype(str)
    return b


b = base("2026"); b22 = base("2022")
for d in (b, b22):
    for t in (1, 2):
        d[f"bn_{t}"] = d[f"branco_{t}"] + d[f"nulo_{t}"]
        d[f"manual_{t}"] = d[f"QT_ELEI_BIOM_SEM_HABILITACAO_{t}"]
# ---------------- R1 ----------------
out["R1"] = {"secoes": int(len(b)), "comparecimento_2t": int(b.QT_COMPARECIMENTO_2.sum()), "validos_mais_brancos_e_nulos_2t": int((b.validos_2 + b.bn_2).sum()), "secoes_com_dados_2t": int(b.QT_COMPARECIMENTO_2.notna().sum())}
# ---------------- R2, R3 ----------------
x = b[b.DT_ENCERRAMENTO_2.notna()].copy(); x["enc"] = pd.to_datetime(x.DT_ENCERRAMENTO_2)
ab = pd.to_datetime(b.DT_ABERTURA_2); ok = ab.dt.hour.between(6, 8) & (ab.dt.minute < 15)
fz = (8 - ab.dt.hour)[ok].groupby(b.mun[ok]).agg(lambda v: v.mode().iloc[0]); x["fuso"] = x.mun.map(fz)
x["enc_bsb"] = x.enc + pd.to_timedelta(x.fuso.fillna(0), unit="h")
dia = pd.Timestamp("2026-10-25")


def faixas(col, rotulo):
    h = (x[col] - dia).dt.total_seconds()
    cortes = [("ate_17h00_59", h <= 17 * 3600 + 59), ("17h01_a_17h15", (h > 17 * 3600 + 59) & (h < 17 * 3600 + 16 * 60)), ("17h16_a_18h59", (h >= 17 * 3600 + 16 * 60) & (h < 19 * 3600)), ("19h_ou_mais", h >= 19 * 3600),
              ("ate_17h00_00", h <= 17 * 3600), ("mais_de_17h30", h > 17 * 3600 + 30 * 60)]
    r = {}
    for nome, m in cortes:
        g = x[m]; L, F = g.v13_2.sum(), g.v22_2.sum()
        r[nome] = {"secoes": int(len(g)), "comparecimento": int(g.QT_COMPARECIMENTO_2.sum()), "lula": int(L), "flavio": int(F), "pct_lula": float(100 * L / (L + F)) if L + F else None, "vantagem_lula": int(L - F)}
    apos = x[h > 17 * 3600 + 59]; r["apos_17h00_59_total"] = {"secoes": int(len(apos)), "vantagem_lula": int(apos.v13_2.sum() - apos.v22_2.sum()), "pct_lula": float(100 * apos.v13_2.sum() / (apos.v13_2.sum() + apos.v22_2.sum()))}
    q = h.quantile([.01, .1, .5, .9, .99, .999]); r["horario_de_encerramento_quantis"] = {str(k): f"{int(v // 3600):02d}:{int(v % 3600 // 60):02d}" for k, v in q.items()}
    return r


out["R2_R3_hora_local"] = faixas("enc", "local"); out["R2_R3_hora_brasilia"] = faixas("enc_bsb", "brasilia")
out["R2_R3_margem_nacional"] = {"lula": int(b.v13_2.sum()), "flavio": int(b.v22_2.sum()), "margem": int(b.v13_2.sum() - b.v22_2.sum())}
# ---------------- R4 ----------------
x["h"] = (x.enc - dia).dt.total_seconds(); x["tardia"] = x.h >= 19 * 3600
x["pl2"] = x.v13_2 / x.validos_2; x["pl1"] = x.v13_1 / x.validos_1
r4 = {}
for uf in ("BA", "PE", "MA", "SP"):
    g = x[(x.SG_UF == uf) & x.tardia]; t = x[x.SG_UF == uf]
    r4[uf] = {"secoes_tardias": int(len(g)), "pct_lula_tardias": float(100 * g.v13_2.sum() / (g.v13_2.sum() + g.v22_2.sum())) if len(g) else None, "pct_lula_demais_do_estado": float(100 * t[~t.tardia].v13_2.sum() / (t[~t.tardia].v13_2.sum() + t[~t.tardia].v22_2.sum()))}
# dentro do município: tardia × demais do mesmo município (só municípios com os dois grupos)
m = x.groupby(["mun", "tardia"]).agg(L2=("v13_2", "sum"), F2=("v22_2", "sum"), L1=("v13_1", "sum"), V1=("validos_1", "sum")).reset_index()
m["pl2"] = m.L2 / (m.L2 + m.F2); m["pl1"] = m.L1 / m.V1; m["sw"] = m.pl2 - m.pl1; w = (m.L2 + m.F2)
a = m[m.tardia].set_index("mun"); c = m[~m.tardia].set_index("mun"); com = a.index.intersection(c.index)
dif_pl2 = a.loc[com, "pl2"] - c.loc[com, "pl2"]; dif_sw = a.loc[com, "sw"] - c.loc[com, "sw"]; pesos = (a.loc[com, "L2"] + a.loc[com, "F2"])
r4["dentro_do_municipio"] = {"municipios_com_secoes_tardias_e_demais": int(len(com)), "diferenca_media_ponderada_pct_lula_pontos": float(100 * np.average(dif_pl2, weights=pesos)), "diferenca_media_ponderada_da_virada_pontos": float(100 * np.average(dif_sw, weights=pesos)),
                             "municipios_onde_a_tardia_tem_mais_lula": int((dif_pl2 > 0).sum()), "secoes_tardias_totais": int(x.tardia.sum()), "secoes_tardias_em_municipio_so_com_tardias": int(x[x.tardia & ~x.mun.isin(com)].shape[0])}
out["R4"] = r4
# ---------------- R5, R6 ----------------
def manual(d, t):
    return {"manual": int(d[f"manual_{t}"].sum()), "comparecimento": int(d[f"QT_COMPARECIMENTO_{t}"].sum()), "pct": float(100 * d[f"manual_{t}"].sum() / d[f"QT_COMPARECIMENTO_{t}"].sum())}


m26, m22 = manual(b, 2), manual(b22, 2)
out["R5"] = {"2026_2t": m26, "2026_1t": manual(b, 1), "2022_2t": m22, "2022_1t": manual(b22, 1), "margem_2026": int(b.v13_2.sum() - b.v22_2.sum()), "margem_2022": int(abs(b22.v13_2.sum() - b22.v22_2.sum())),
             "razao_manual_sobre_margem": {"2026_2t": m26["manual"] / (b.v13_2.sum() - b.v22_2.sum()), "2022_2t": m22["manual"] / abs(b22.v13_2.sum() - b22.v22_2.sum())}}


def corr_bloco(d, t):
    d = d[(d[f"QT_COMPARECIMENTO_{t}"] >= 50) & (d[f"validos_{t}"] >= 20)].copy(); d["tx"] = d[f"manual_{t}"] / d[f"QT_COMPARECIMENTO_{t}"]; d["pl"] = d[f"v13_{t}"] / d[f"validos_{t}"]
    d = d[(d.tx <= 1)]
    r = {"secoes": int(len(d)), "correlacao_entre_secoes": float(np.corrcoef(d.tx, d.pl)[0, 1])}
    g = d.groupby("mun").agg(tx=("tx", "mean"), pl=("pl", "mean")); r["correlacao_entre_municipios"] = float(np.corrcoef(g.tx, g.pl)[0, 1])
    dx = d.tx - d.groupby("mun").tx.transform("mean"); dy = d.pl - d.groupby("mun").pl.transform("mean"); r["correlacao_dentro_do_municipio"] = float(np.corrcoef(dx, dy)[0, 1]); r["inclinacao_dentro_do_municipio"] = float((dx * dy).sum() / (dx ** 2).sum())
    bins = [0, .05, .10, .20, .30, .50, 1.01]; rot = ["0-5%", "5-10%", "10-20%", "20-30%", "30-50%", ">50%"]; q = pd.cut(d.tx, bins, labels=rot, right=False)
    gb = d.groupby(q, observed=True); r["curva_pct_lula_por_taxa_de_liberacao_manual"] = {str(k): {"secoes": int(len(v)), "pct_lula": float(100 * v.pl.mean())} for k, v in gb}
    return r


out["R6"] = {"2026_2t": corr_bloco(b, 2), "2026_1t": corr_bloco(b, 1), "2022_2t": corr_bloco(b22, 2), "2022_1t": corr_bloco(b22, 1)}
# ---------------- R7 ----------------
def unani(d, t, col="v13"):
    v = d[d[f"validos_{t}"] > 0]; r = {}
    for nome, c in (("lula", "v13"), ("direita", "v22")):
        p = v[f"{c}_{t}"].fillna(0) / v[f"validos_{t}"]
        r[nome] = {"100pct": int((p == 1).sum()), "mais_de_90pct": int((p > .9).sum()), "mais_de_90pct_sem_100": int(((p > .9) & (p < 1)).sum())}
    r["razao_100pct"] = r["lula"]["100pct"] / max(r["direita"]["100pct"], 1); r["razao_mais_de_90pct"] = r["lula"]["mais_de_90pct"] / max(r["direita"]["mais_de_90pct"], 1)
    return r


out["R7"] = {"2026_2t": unani(b[b.SG_UF != "ZZ"], 2), "2026_1t": unani(b[b.SG_UF != "ZZ"], 1), "2022_2t": unani(b22[b22.SG_UF != "ZZ"], 2), "2022_1t": unani(b22[b22.SG_UF != "ZZ"], 1)}
v = b[(b.SG_UF != "ZZ") & (b.validos_2 > 0) & (b.v13_2 / b.validos_2 > .9)]
out["R7"]["onde_ficam_as_seções_com_mais_de_90pct_de_Lula_2026_2t"] = {"uf_top": v.SG_UF.value_counts().head(6).to_dict(), "mediana_validos": float(v.validos_2.median()), "mediana_validos_todas": float(b.validos_2.median()), "pct_no_norte_e_nordeste": float(100 * v.SG_UF.isin(["AC", "AL", "AM", "AP", "BA", "CE", "MA", "PA", "PB", "PE", "PI", "RN", "RO", "RR", "SE", "TO"]).mean())}
# ---------------- R8 ----------------
def digito(a):
    a = np.asarray(a); a = a[a >= 1]; return np.array([(np.floor(a / 10 ** np.floor(np.log10(a))).astype(int) == k).mean() for k in range(1, 10)])


BEN = np.log10(1 + 1 / np.arange(1, 10))
mad = lambda p: float(np.mean(np.abs(p - BEN)))
chi = lambda p, n: float(n * np.sum((p - BEN) ** 2 / BEN))
r8 = {}
for nome, d in (("2026_2t", b), ("2022_2t", b22)):
    d = d[(d.validos_2 > 0)]
    for cand, c in (("lula", "v13_2"), ("direita", "v22_2")):
        vals = d[c].fillna(0).values; p = digito(vals)
        # referências sem manipulação: binomial e beta-binomial com participação municipal observada
        pm = (d.groupby("mun")[c].transform("sum") / d.groupby("mun").validos_2.transform("sum")).clip(1e-4, 1 - 1e-4).values; n = d.validos_2.values.astype(int)
        sims = {"binomial": [], "beta_binomial_rho_0_02": []}
        for _ in range(40):
            sims["binomial"].append(mad(digito(rng.binomial(n, pm))))
            k = 1 / .02 - 1; pp = rng.beta(pm * k, (1 - pm) * k); sims["beta_binomial_rho_0_02"].append(mad(digito(rng.binomial(n, pp))))
        r8[f"{nome}_{cand}"] = {"secoes": int(len(vals)), "mad_observado": mad(p), "qui2_observado": chi(p, (vals >= 1).sum()), "primeiro_digito_observado": [round(float(z), 4) for z in p], "benford": [round(float(z), 4) for z in BEN],
                                "mad_referencia_binomial": [float(np.min(sims["binomial"])), float(np.max(sims["binomial"]))], "mad_referencia_beta_binomial": [float(np.min(sims["beta_binomial_rho_0_02"])), float(np.max(sims["beta_binomial_rho_0_02"]))]}
out["R8"] = r8
# ---------------- R9 ----------------
c = pd.read_csv(f"{R}/operacao_veracidade/externo/arvor_totalizacao/conferencia_tse.csv", dtype=str)
t = pd.to_datetime(c.conferido_em, utc=True).dt.tz_convert("America/Sao_Paulo")
out["R9"] = {"primeira_conferencia_de_terceiro_contra_o_arquivo_do_tse_brasilia": str(t.min()), "conferencias_em_25_10": int((t.dt.date == pd.Timestamp("2026-10-25").date()).sum()), "conferencias_total": int(len(c)),
             "nota": "arquivos por urna estavam publicados em resultados.tse.jus.br na noite de 25/10; o CSV BWeb de dados abertos não tem registro de primeira publicação neste projeto, então a afirmação sobre ele não é testável aqui"}
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1, default=float)
print(json.dumps(out, ensure_ascii=False, indent=1, default=float)[:9000])
