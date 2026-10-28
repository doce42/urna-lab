"""T52 a T54: postagens de Leonardo Dias/arvor.co (pré-registro em fase3/PREREG_POSTS_ARVOR.md)."""
import glob, json
import numpy as np, pandas as pd

AN = "analise"; OUT = "fase3/resultados/posts_arvor.json"
CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
DIA = {"2026": "2026-10-25", "2022": "2022-10-30"}
R = {"pre_registro": "fase3/PREREG_POSTS_ARVOR.md"}


def base(ano):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
    b = b[b.SG_UF != "ZZ"].copy(); b["mun"] = b.SG_UF + b.CD_MUNICIPIO.astype(str)
    for c in ("DT_ABERTURA_2", "DT_ENCERRAMENTO_2", "DT_EMISSAO_BU_2", "DT_BU_RECEBIDO_2"):
        b[c] = pd.to_datetime(b[c], errors="coerce")
    ab = b.DT_ABERTURA_2; ok = ab.dt.hour.between(6, 8) & (ab.dt.minute < 15)
    fz = (8 - ab.dt.hour)[ok].groupby(b.mun[ok]).agg(lambda v: v.mode().iloc[0])
    b["fuso"] = b.mun.map(fz)
    return b.dropna(subset=["fuso"])


hm = lambda s: None if pd.isna(s) else s.strftime("%H:%M")

# ---------------- T52 ----------------
t52 = {}
for ano in ("2026", "2022"):
    b = base(ano); dia = pd.Timestamp(DIA[ano]); fh = pd.to_timedelta(b.fuso, unit="h")
    # fuso de cada campo, decidido pelos dados: menor (recebido − emissão) por grupo de fuso, com e sem conversão do recebido
    d_local = (b.DT_BU_RECEBIDO_2 - b.DT_EMISSAO_BU_2).dt.total_seconds() / 60
    teste = {f"fuso_{int(k)}": {"p01_min_recebido_local": float(g.quantile(.01)), "p01_min_recebido_brasilia": float((g - 60 * k).quantile(.01))}
             for k, g in d_local.groupby(b.fuso)}
    p01 = {k: v["p01_min_recebido_local"] for k, v in teste.items()}
    recebido_brasilia = (max(p01.values()) - min(p01.values())) > 30   # se o recebido estivesse no fuso local, a diferença mínima seria igual entre fusos
    emi = b.DT_EMISSAO_BU_2 + fh; enc = b.DT_ENCERRAMENTO_2 + fh
    rec = b.DT_BU_RECEBIDO_2 if recebido_brasilia else b.DT_BU_RECEBIDO_2 + fh
    q = lambda s, p: hm(s.quantile(p))
    rs = rec.dropna().sort_values()
    j = rs[(rs >= dia + pd.Timedelta(hours=17)) & (rs <= dia + pd.Timedelta(hours=21))]
    gaps = j.diff().dt.total_seconds() / 60; ig = gaps.idxmax() if len(gaps) > 1 else None
    prorrog = enc > dia + pd.Timedelta(hours=17, minutes=30)
    antes19 = rec < dia + pd.Timedelta(hours=19)
    # votos após 17h (Brasília) nos logs
    m = pd.concat([pd.read_parquet(f) for f in glob.glob(f"{AN}/brutos/{'2t' if ano == '2026' else '2022_2t'}/minutos_*.parquet")])
    m["mun"] = m.SG_UF + m.CD_MUNICIPIO.astype(str); m = m[m.SG_UF != "ZZ"]
    m["fuso"] = m.mun.map(b.groupby("mun").fuso.first()); m = m.dropna(subset=["fuso"])
    tm = pd.to_datetime(m.minuto, format="%d/%m/%Y %H:%M") + pd.to_timedelta(m.fuso, unit="h")
    noDia = (tm >= dia + pd.Timedelta(hours=6)) & (tm <= dia + pd.Timedelta(hours=22))
    t52[ano] = {"recebido_em_hora_de_brasilia": bool(recebido_brasilia), "teste_fuso": teste,
                "emissao_mediana": q(emi, .5), "encerramento_mediana": q(enc, .5),
                "recebimento_p10": q(rec, .1), "recebimento_mediana": q(rec, .5), "recebimento_p90": q(rec, .9),
                "intervalo_mediano_min": float(((rec - emi).dt.total_seconds() / 60).median()),
                "recebidos_antes_19h": int(antes19.sum()), "frac_antes_19h": float(antes19.mean()),
                "ultimo_antes_do_vazio": hm(j.loc[:ig].iloc[-2]) if ig is not None else None, "primeiro_depois_do_vazio": hm(j.loc[ig]) if ig is not None else None,
                "maior_vazio_17_21h_min": float(gaps.max()) if len(gaps) > 1 else None,
                "urnas_prorrogadas_fecharam_apos_17h30": int(prorrog.sum()), "ultima_urna_fechou": hm(enc.max()),
                "fechamento_p99_prorrogadas": q(enc[prorrog], .99) if prorrog.any() else None,
                "primeiro_recebimento_por_uf": {u: hm(g.min()) for u, g in rec.groupby(b.SG_UF)},
                "votos_log_apos_17h": int(m.votos[noDia & (tm >= dia + pd.Timedelta(hours=17))].sum()),
                "votos_log_dia": int(m.votos[noDia].sum())}
R["T52"] = t52

# ---------------- T53 ----------------
t53 = {}
for ano, pasta in (("2026", "2t"), ("2022", "2022_2t")):
    u = pd.concat([pd.read_parquet(f, columns=CH + ["seq_hab_biometrica", "seq_hab_manual", "seq_hab_mesario", "seq_hab_outro", "seq_sem_habilitacao", "seq_votos_dia"])
                   for f in glob.glob(f"{AN}/brutos/{pasta}/urnas_*.parquet")])
    u = u[u.SG_UF != "ZZ"]
    tot = u[["seq_hab_biometrica", "seq_hab_manual", "seq_hab_mesario", "seq_hab_outro", "seq_sem_habilitacao"]].sum()
    s = tot.sum()
    b = base(ano).astype({c: str for c in CH}); u = u.astype({c: str for c in CH}).merge(b[CH + ["mun", "v13_1", "validos_1", "v13_2", "validos_2"]], on=CH)
    u = u[(u.validos_1 >= 20) & (u.validos_2 >= 20)]
    lg = lambda x, n: np.log((x + .5) / (n - x + .5))
    u["vir"] = lg(u.v13_2, u.validos_2) - lg(u.v13_1, u.validos_1)
    nb = (u.seq_hab_mesario + u.seq_hab_manual) / u[["seq_hab_biometrica", "seq_hab_manual", "seq_hab_mesario", "seq_hab_outro"]].sum(axis=1).clip(lower=1)
    u["nb"] = nb
    u = u[np.isfinite(u.vir) & np.isfinite(u.nb)]   # correção 1: seções sem contagem de habilitação no log davam NaN
    dv, dn = u.vir - u.groupby("mun").vir.transform("mean"), u.nb - u.groupby("mun").nb.transform("mean")
    t53[ano] = {"habilitacoes": {k: int(v) for k, v in tot.items()}, "frac_biometrica": float(tot.seq_hab_biometrica / s),
                "frac_mesario_ou_manual": float((tot.seq_hab_mesario + tot.seq_hab_manual) / s),
                "frac_mesario_ou_manual_por_uf": (u.groupby("SG_UF")[["seq_hab_mesario", "seq_hab_manual"]].sum().sum(axis=1) /
                                                  u.groupby("SG_UF")[["seq_hab_biometrica", "seq_hab_manual", "seq_hab_mesario", "seq_hab_outro"]].sum().sum(axis=1)).round(4).to_dict(),
                "dentro_do_municipio_inclinacao_virada_por_fracao_sem_biometria": float((dv * dn).sum() / (dn ** 2).sum()),
                "dentro_do_municipio_correlacao": float(np.corrcoef(dv, dn)[0, 1]), "secoes": int(len(u))}
R["T53"] = t53

# ---------------- T54 ----------------
t54 = {}
for ano in ("2026", "2022"):
    b = base(ano); g = b.groupby("mun")[["v13_1", "v22_1", "v13_2", "v22_2", "QT_APTOS_2", "QT_COMPARECIMENTO_1", "QT_COMPARECIMENTO_2"]].sum()
    r = {"municipios": int(len(g))}
    for nome, c in (("13", "v13"), ("22", "v22")):
        d = g[f"{c}_2"] - g[f"{c}_1"]; per = g[d < 0]
        outro = "v22" if c == "v13" else "v13"
        r[f"{nome}_perdeu_votos"] = {"municipios": int(len(per)), "votos_perdidos": int(-d[d < 0].sum()), "aptos": int(per.QT_APTOS_2.sum()),
                                     "outro_ganhou_votos_nesses": int((per[f"{outro}_2"] - per[f"{outro}_1"]).sum()),
                                     "comparecimento_caiu_em": int((per.QT_COMPARECIMENTO_2 < per.QT_COMPARECIMENTO_1).sum())}
    t54[ano] = r
R["T54"] = t54
json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1, default=str)
for k in ("T52", "T53", "T54"):
    for ano, v in R[k].items():
        v = {a: b for a, b in v.items() if a not in ("primeiro_recebimento_por_uf", "frac_mesario_ou_manual_por_uf", "teste_fuso")}
        print(k, ano, json.dumps(v, ensure_ascii=False))
print("SE", R["T52"]["2026"]["primeiro_recebimento_por_uf"].get("SE"), R["T52"]["2022"]["primeiro_recebimento_por_uf"].get("SE"))
print(json.dumps(R["T52"]["2026"]["teste_fuso"]))
