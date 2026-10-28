"""Fase 2 completa: uso  f2_completa.py <P2|P5|P7|P8|P9|P10|P12|P13|P14|P15|P16|P17|P11>  (pré-registro em sessao_limitada_2026-10-28/PREREG.md)."""
import glob, hashlib, json, os, sys, time, zipfile
import numpy as np, pandas as pd
from scipy import stats

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; OUT = RAIZ + "/fase2/resultados"
sys.path.insert(0, AN)
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
inv = lambda z: 1 / (1 + np.exp(-z))
P = sys.argv[1]; MODO = sys.argv[2] if len(sys.argv) > 2 else ""; T0 = time.time()


def base(ano, excl_zz=False):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
    b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20)].copy()
    if excl_zz: b = b[b.SG_UF != "ZZ"].copy()
    b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
    x1, n1, x2, n2 = b["v13_1"], b["validos_1"], b["v13_2"], b["validos_2"]
    b["sw"] = lg(x2, n2) - lg(x1, n1)
    b["res"] = b["sw"] - b.groupby("mun")["sw"].transform("median")
    z = b["res"] / np.sqrt(1/(x1+.5) + 1/(n1-x1+.5) + 1/(x2+.5) + 1/(n2-x2+.5))
    b["z"] = z / (1.4826 * (z - z.median()).abs().median())
    return b.reset_index(drop=True)


def boot_mun(codm, nm, rng):
    """índices de municípios sorteados (com reposição)"""
    return rng.integers(0, nm, nm)


def bh(p, q=0.05):
    p = np.asarray(p); n = len(p); o = np.argsort(p); passa = p[o] <= q * np.arange(1, n + 1) / n
    k = np.max(np.where(passa)[0]) + 1 if passa.any() else 0
    s = np.zeros(n, bool); s[o[:k]] = True; return s


R = {"pergunta": P}

if P == "P8":
    for ano in ("2026", "2022"):
        b = base(ano); g = b[b.groupby("mun")["mun"].transform("size") >= 20].copy()
        g["ord"] = g.groupby("mun")["DT_BU_RECEBIDO_2"].rank(pct=True)
        ro, rr = g["ord"].rank().values, g["res"].rank().values
        r0 = float(np.corrcoef(ro, rr)[0, 1])
        cod, un = pd.factorize(g["mun"]); idx = pd.Series(np.arange(len(g))).groupby(cod).apply(np.array)
        rng = np.random.default_rng(8); rs = []
        for _ in range(200):
            ii = np.concatenate([idx[m] for m in rng.integers(0, len(un), len(un))])
            rs.append(np.corrcoef(ro[ii], rr[ii])[0, 1])
        R[ano] = {"n": int(len(g)), "municipios": int(len(un)), "spearman": r0, "ic95_boot_mun": [float(np.percentile(rs, 2.5)), float(np.percentile(rs, 97.5))],
                  "desprezivel_abs_le_0_05": bool(max(abs(np.percentile(rs, 2.5)), abs(np.percentile(rs, 97.5))) <= 0.05)}

elif P == "P7":
    for ano in ("2026", "2022"):
        b = base(ano); tr = (b["NR_URNA_EFETIVADA_1"] != b["NR_URNA_EFETIVADA_2"]).values; z = b["z"].values
        cod, un = pd.factorize(b["mun"]); nm = len(un)
        s1 = np.bincount(cod, weights=z * tr, minlength=nm); c1 = np.bincount(cod, weights=tr, minlength=nm)
        s0 = np.bincount(cod, weights=z * ~tr, minlength=nm); c0 = np.bincount(cod, weights=(~tr).astype(float), minlength=nm)
        d0 = s1.sum() / c1.sum() - s0.sum() / c0.sum(); rng = np.random.default_rng(7); ds = []
        for _ in range(500):
            k = rng.integers(0, nm, nm); ds.append(s1[k].sum() / c1[k].sum() - s0[k].sum() / c0[k].sum())
        lo, hi = np.percentile(ds, [5, 95])
        R[ano] = {"urnas_trocadas": int(tr.sum()), "diferenca_z": float(d0), "ic90_boot_mun": [float(lo), float(hi)], "margem": 0.10, "equivalente": bool(lo > -0.10 and hi < 0.10)}

elif P == "P5":
    for ano, pas in (("2026", "2t"), ("2022", "2022_2t")):
        b = base(ano)
        u = pd.concat([pd.read_parquet(f, columns=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "modelo"]) for f in glob.glob(f"{AN}/brutos/{pas}/urnas_*.parquet")])
        m = b.merge(u.astype(str), on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]); m = m[m.modelo.notna() & (m.modelo != "None")]
        nmod = m.groupby("mun")["modelo"].transform("nunique"); m = m[nmod >= 2].copy()
        m["d"] = m["res"] - m.groupby("mun")["res"].transform("mean")
        mods = sorted(m.modelo.unique()); cod, un = pd.factorize(m["mun"]); nm = len(un)
        S = np.stack([np.bincount(cod, weights=m.d.values * (m.modelo == k).values, minlength=nm) for k in mods], 1)
        C = np.stack([np.bincount(cod, weights=(m.modelo == k).values.astype(float), minlength=nm) for k in mods], 1)
        est = S.sum(0) / C.sum(0); rng = np.random.default_rng(5); bs = []
        for _ in range(200):
            k = rng.integers(0, nm, nm); bs.append(S[k].sum(0) / C[k].sum(0))
        bs = np.array(bs)
        R[ano] = {"municipios_com_2_ou_mais_modelos": int(nm), "secoes": int(len(m)),
                  "modelos": {k: {"secoes": int(C[:, i].sum()), "media_residuo_logit": float(est[i]), "ic95": [float(np.percentile(bs[:, i], 2.5)), float(np.percentile(bs[:, i], 97.5))]} for i, k in enumerate(mods)},
                  "equivalente_em_0_02_logit": all(abs(np.percentile(bs[:, i], 2.5)) <= .02 and abs(np.percentile(bs[:, i], 97.5)) <= .02 for i in range(len(mods)))}

elif P == "P9":
    for ano in ("2026", "2022"):
        b = base(ano); b = b[b.SG_UF != "ZZ"].copy(); b["local"] = b["mun"] + "-" + b["NR_ZONA"] + "-" + b["NR_LOCAL_VOTACAO_2"].astype(str)
        x1, n1, x2, n2 = b["v13_1"], b["validos_1"], b["v13_2"], b["validos_2"]
        b["p1"] = x1 / n1; b["orf"] = 1 - (b["v13_1"] + b["v22_1"]) / n1
        elim = [c for c in b.columns if c.startswith("v") and c.endswith("_1") and c not in ("v13_1", "v22_1", "validos_1")]
        for modelo in ("simples", "completo"):
            cols = [np.ones(len(b)), b.p1, b.p1 ** 2, b.orf]
            if modelo == "completo":
                cols += [b[c].fillna(0) / n1 for c in elim] + [(b["branco_1"] + b["nulo_1"]) / b["total_1"],
                         b["QT_COMPARECIMENTO_2"] / b["QT_APTOS_2"] - b["QT_COMPARECIMENTO_1"] / b["QT_APTOS_1"], np.log(b.groupby("mun")["QT_APTOS_2"].transform("sum"))]
            X = np.nan_to_num(np.column_stack([np.asarray(c, float) for c in cols])); esp = np.zeros(len(b))
            for uf, ix in b.groupby("SG_UF").indices.items():
                beta, *_ = np.linalg.lstsq(X[ix], b["sw"].values[ix], rcond=None); esp[ix] = X[ix] @ beta
            sd = np.sqrt(1/(x1+.5) + 1/(n1-x1+.5) + 1/(x2+.5) + 1/(n2-x2+.5)); zz = (b["sw"].values - esp) / sd
            zz = (zz - np.median(zz)) / (1.4826 * np.median(np.abs(zz - np.median(zz)))); b["zz"] = zz
            g = b.groupby("local")["zz"].agg(["size", "mean", "sum"]); g = g[g["size"] >= 3]
            k = g["size"].values.astype(float); grand = b[b.local.isin(g.index)]["zz"].mean()
            gm = b[b.local.isin(g.index)].groupby("local")["zz"]
            ssb = (k * (g["mean"].values - grand) ** 2).sum(); sst = ((b[b.local.isin(g.index)]["zz"] - gm.transform("mean")) ** 2).sum()
            ng = len(g); N = k.sum(); msb = ssb / (ng - 1); msw = sst / (N - ng); k0 = (N - (k ** 2).sum() / N) / (ng - 1)
            rho = float(max(0, (msb - msw) / (msb + (k0 - 1) * msw)))
            zg = g["mean"].values * np.sqrt(k); p0 = 2 * stats.norm.sf(np.abs(zg)); deff = 1 + (k - 1) * rho; zadj = zg / np.sqrt(deff); p1_ = 2 * stats.norm.sf(np.abs(zadj))
            R[f"{ano}_{modelo}"] = {"locais": int(ng), "rho_intralocal": rho, "significativos_BH_original": int(bh(p0).sum()), "significativos_BH_ajustado_rho": int(bh(p1_).sum()),
                                    "pro_lula_ajustado": int((bh(p1_) & (zadj > 0)).sum()), "pro_adversario_ajustado": int((bh(p1_) & (zadj < 0)).sum()), "dp_zg": float(zg.std())}
    R["moran_i"] = "não feito: sem arquivo de adjacência municipal no material local (fila: obter malha de vizinhança do IBGE)"

elif P == "P10":
    for ano, turno, pas in (("2026", 1, "1t"), ("2026", 2, "2t"), ("2022", 1, "2022_1t"), ("2022", 2, "2022_2t")):
        fs = glob.glob(f"{AN}/brutos/{pas}/urnas_*.parquet")
        if not fs: continue
        u = pd.concat([pd.read_parquet(f, columns=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "modelo", "seq_ult30_votos", "seq_ult30_sem_biometria", "seq_resto_votos", "seq_resto_sem_biometria"]) for f in fs], ignore_index=True)
        u = u.dropna(subset=["seq_ult30_votos"]).copy(); u = u[u.seq_ult30_votos > 0].copy()
        n, x, N, y = u.seq_resto_votos.values, u.seq_resto_sem_biometria.values, u.seq_ult30_votos.values.astype(int), u.seq_ult30_sem_biometria.values.astype(int)
        u["g"] = u.SG_UF.astype(str) + "|" + u.modelo.astype(str); p = np.ones(len(u)); ratios = []
        for gname, ix in u.groupby("g").indices.items():
            nn, xx = n[ix], x[ix]; ok = nn > 0
            if ok.sum() < 30:
                a_, b_ = 1.0, 7.0
            else:
                m = xx[ok].sum() / nn[ok].sum(); rr = xx[ok] / nn[ok]; vobs = np.var(rr); vnoise = np.mean(m * (1 - m) / nn[ok]); vb = max(vobs - vnoise, 1e-6)
                s = max(m * (1 - m) / vb - 1, 2.0); a_, b_ = m * s, (1 - m) * s
            p[ix] = stats.betabinom.sf(y[ix] - 1, N[ix], a_ + xx, b_ + nn - xx)
        u["p"] = p; u["sig"] = bh(p)
        # original (binomial, taxa suavizada)
        taxa = (x + .5) / (n + 1); p_orig = stats.binom.sf(y - 1, N, taxa); sig_o = bh(p_orig)
        ch = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
        ko = set(map(tuple, u.loc[sig_o, ch].astype(str).values)); kn = set(map(tuple, u.loc[u.sig, ch].astype(str).values))
        R[f"{ano}_{turno}t"] = {"urnas": int(len(u)), "original_binomial_BH": int(sig_o.sum()), "beta_binomial_BH": int(u.sig.sum()), "em_ambos": len(ko & kn), "so_no_original": len(ko - kn),
                                "razao_ult30_sobre_resto": float((y.sum() / N.sum()) / (x.sum() / n.sum())),
                                "votos_ult30_nas_urnas_beta_binomial": int(N[u.sig.values].sum()), "sem_biometria_ult30_nessas": int(y[u.sig.values].sum())}

elif P == "P12":
    b0 = pd.read_parquet(f"{AN}/base.parquet"); zz = b0[b0.SG_UF == "ZZ"]
    zc = zipfile.ZipFile(f"{RAIZ}/dados/perfil_eleitorado/perfil_eleitor_secao_2026_ZZ.zip")
    d = pd.read_csv(zc.open("perfil_eleitor_secao_2026_ZZ.csv"), sep=";", encoding="latin1", usecols=["CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO", "QT_ELEITORES"])
    for t in (1, 2):
        of = json.load(open(f"{RAIZ}/dados/totais_oficiais/zz-e00625{6+t}-u.json")); e, s_ = of["e"], of["s"]
        bu = float(zz[f"QT_APTOS_{t}"].sum())
        R[f"{t}t"] = {"oficial_eleitorado_total": int(e["te"]), "oficial_eleitorado_secoes_instaladas": int(e["esi"]), "oficial_eleitorado_secoes_nao_instaladas": int(e["esni"]),
                      "oficial_secoes_total": int(s_["ts"]), "oficial_secoes_instaladas": int(s_["si"]), "oficial_secoes_nao_instaladas": int(s_["sni"]),
                      "soma_aptos_dos_bu": int(bu), "secoes_com_bu": int(len(zz)),
                      "diferenca_total_oficial_menos_bu": int(e["te"]) - int(bu), "diferenca_instaladas_oficial_menos_bu": int(e["esi"]) - int(bu),
                      "explicado_por_secoes_nao_instaladas": int(e["esni"]), "residuo_nao_explicado": int(e["esi"]) - int(bu),
                      "cadastro_perfil_14_07_2026_total": int(d.QT_ELEITORES.sum())}
        ub = pd.read_parquet(f"{AN}/brutos/{t}t/urnas_ZZ.parquet")
        zt = zz[zz[f"QT_APTOS_{t}"].notna()]; chaves = set(zip(zt.CD_MUNICIPIO.astype(str), zt.NR_ZONA.astype(str), zt.NR_SECAO.astype(str)))
        so_urna = ub[[(a_, b_, c_) not in chaves for a_, b_, c_ in zip(ub.CD_MUNICIPIO.astype(str), ub.NR_ZONA.astype(str), ub.NR_SECAO.astype(str))]]
        R[f"{t}t"]["secoes_so_nos_arquivos_das_urnas"] = [{"municipio": r.CD_MUNICIPIO, "zona": r.NR_ZONA, "secao": r.NR_SECAO, "aptos_no_bu_da_urna": int(r.bu_aptos)} for r in so_urna.itertuples()]
        R[f"{t}t"]["soma_aptos_secoes_so_nos_arquivos_das_urnas"] = int(so_urna.bu_aptos.sum())
        R[f"{t}t"]["residuo_depois_das_secoes_so_nas_urnas"] = int(e["esi"]) - int(bu) - int(so_urna.bu_aptos.sum())
    R["nota"] = "O total oficial inclui as seções não instaladas; o residuo é o que sobra depois de descontá-las. O cadastro (perfil, gerado em 14/07) está só como ordem de grandeza: é anterior à eleição."

elif P == "P13":
    for rot, zz in (("sem_exterior", False), ("com_exterior", True)):
        b = pd.read_parquet(f"{AN}/base.parquet")
        if not zz: b = b[b.SG_UF != "ZZ"]
        F1, L1, F2, L2 = (b[c].values.astype(float) for c in ("v22_1", "v13_1", "v22_2", "v13_2"))
        for nome, N in (("aptos_1t", b.QT_APTOS_1.values.astype(float)), ("aptos_2t", b.QT_APTOS_2.values.astype(float)), ("comparecimento_2t", b.QT_COMPARECIMENTO_2.values.astype(float)), ("comparecimento_1t", b.QT_COMPARECIMENTO_1.values.astype(float))):
            R[f"{rot}/{nome}"] = {"F_L_min": float(np.maximum(0, F1 + L2 - N).sum()), "F_L_max": float(np.minimum(F1, L2).sum()), "L_F_min": float(np.maximum(0, L1 + F2 - N).sum()), "L_F_max": float(np.minimum(L1, F2).sum())}
    R["registrado_C06b"] = {"F_L": [79, 43.6e6], "L_F": [123, 39.5e6]}

elif P == "P15":
    for ano in ("2026", "2022"):
        b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet"); b = b[b.SG_UF != "ZZ"]
        b = b[(b.QT_APTOS_1 >= 50) & (b.QT_APTOS_2 >= 50)]
        N = b.QT_APTOS_1.values.astype(float); A = N - b.QT_COMPARECIMENTO_1.values; L2, F2 = b.v13_2.values.astype(float), b.v22_2.values.astype(float)
        lm, lM = np.maximum(0, A + L2 - N).sum(), np.minimum(A, L2).sum(); fm, fM = np.maximum(0, A + F2 - N).sum(), np.minimum(A, F2).sum()
        c06 = json.load(open(f"{AN}/resultado_comportamento_{ano}.json"))["C06"]; i = c06["linhas"].index("Abstenção (1º)"); ab = A.sum()
        por_uf = {}
        for uf, g in b.groupby("SG_UF"):
            Ag = g.QT_APTOS_1 - g.QT_COMPARECIMENTO_1
            por_uf[uf] = {"A_L_min": float(np.maximum(0, Ag + g.v13_2 - g.QT_APTOS_1).sum()), "A_L_max": float(np.minimum(Ag, g.v13_2).sum())}
        R[ano] = {"abstencao_1t": float(ab), "abs_para_lula": {"min": float(lm), "max": float(lM)}, "abs_para_adv": {"min": float(fm), "max": float(fM)},
                  "razao_possivel": {"min": float(lm / fM), "max": float(lM / max(fm, 1))}, "c06_estimativa": {"lula": float(c06["matriz"][i][0] * ab), "adv": float(c06["matriz"][i][1] * ab)},
                  "nota": "limites por seção (Fréchet) somados; a população de cada seção é o eleitorado apto do 1º turno"}

elif P == "P14":
    rng = np.random.default_rng(14)
    for ano in ("2026", "2022"):
        b = base(ano, excl_zz=True); b["local"] = b["mun"] + "-" + b["NR_ZONA"] + "-" + b["NR_LOCAL_VOTACAO_2"].astype(str)
        for nome, sel in (("pro_lula", b.z > 5), ("pro_outro", b.z < -5)):
            o = b[sel]; n = len(o)
            multi = lambda s: int((s.value_counts() >= 2).sum())
            obs_loc, obs_mun = multi(o["local"]), multi(o["mun"])
            sim_loc, sim_mun = [], []
            for _ in range(500):
                pick = []
                for uf, k in o.SG_UF.value_counts().items():
                    pool = b.index[b.SG_UF == uf]; pick.append(rng.choice(pool, k, replace=False))
                s = b.loc[np.concatenate(pick)]; sim_loc.append(multi(s["local"])); sim_mun.append(multi(s["mun"]))
            R[f"{ano}/{nome}"] = {"n": int(n), "municipios_distintos": int(o["mun"].nunique()), "locais_distintos": int(o["local"].nunique()), "locais_com_2_ou_mais": obs_loc, "esperado_locais_2_ou_mais_sorteio_por_UF": [float(np.mean(sim_loc)), float(np.percentile(sim_loc, 97.5))],
                                  "municipios_com_2_ou_mais": obs_mun, "esperado_municipios_2_ou_mais": [float(np.mean(sim_mun)), float(np.percentile(sim_mun, 97.5))],
                                  "top_municipios": o["mun"].value_counts().head(5).to_dict(), "validos_2_mediana": float(o.validos_2.median()), "validos_2_mediana_todas": float(b.validos_2.median())}

elif P == "P17":
    rng = np.random.default_rng(17)
    for ano in ("2026", "2022"):
        b = base(ano, excl_zz=True); cod, un = pd.factorize(b["mun"]); nm = len(un); out = {}
        for t in (3, 4, 5):
            pl = np.bincount(cod, weights=(b.z > t).values.astype(float), minlength=nm); po = np.bincount(cod, weights=(b.z < -t).values.astype(float), minlength=nm)
            r0 = np.log(pl.sum() / po.sum()); rs = []
            for _ in range(1000):
                k = rng.integers(0, nm, nm); rs.append(np.log(max(pl[k].sum(), .5) / max(po[k].sum(), .5)))
            out[str(t)] = {"pro_lula": int(pl.sum()), "pro_outro": int(po.sum()), "log_razao": float(r0), "ic95": [float(np.percentile(rs, 2.5)), float(np.percentile(rs, 97.5))], "assimetria_significativa": bool(np.percentile(rs, 2.5) > 0)}
        R[ano] = out

elif P == "P2":
    # regra do T13 (analise/poder.py), cópia literal de testes() e dos limiares; dois sentidos; mundo de referência por bootstrap paramétrico
    def wil(k, n, method=None):
        z_ = 1.96; ph = k / n; den = 1 + z_ * z_ / n; c = (ph + z_ * z_ / (2 * n)) / den; h = z_ * np.sqrt(ph * (1 - ph) / n + z_ * z_ / (4 * n * n)) / den
        return c - h, c + h
    modo = sys.argv[2] if len(sys.argv) > 2 else "principal"
    seed, mags = (1001, [0.05]) if modo == "principal" else (2002, [0.02, 0.10])
    b = pd.read_parquet(f"{AN}/base.parquet"); b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20)].reset_index(drop=True)
    b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]; b = b.sort_values("DT_BU_RECEBIDO_2").reset_index(drop=True)
    L1, V1 = b["v13_1"].values.astype(float), b["validos_1"].values.astype(float); ORF = 1 - (b["v13_1"].values + b["v22_1"].values) / V1
    mun = pd.factorize(b["mun"])[0]; uf = b["SG_UF"].values; minuto = b["DT_BU_RECEBIDO_2"].dt.floor("1min").values
    comp, aptos = b["QT_COMPARECIMENTO_2"].values.astype(float), b["QT_APTOS_2"].values.astype(float)

    def testes(L2, V2):
        sw = lg(L2, V2) - lg(L1, V1); s = pd.Series(sw); res = sw - s.groupby(mun).transform("median").values
        sd = np.sqrt(1/(L1+.5) + 1/(V1-L1+.5) + 1/(L2+.5) + 1/(V2-L2+.5)); z = res / sd; zr = z / (1.4826 * np.median(np.abs(z - np.median(z))))
        t1 = int((zr > 5).sum()); sw_uf = s.groupby(uf).transform("median").values; prev = inv(lg(L1, V1) + sw_uf) * V2
        df = pd.DataFrame({"m": minuto, "L": L2, "P": prev, "V": V2}).groupby("m").sum().cumsum(); t2 = float(100 * ((df.L - df.P) / df.V).abs().max())
        t3 = int(((comp / aptos >= .95) & (L2 / V2 >= .9)).sum())
        e = pd.DataFrame({"uf": uf, "sw": sw, "p1": L1 / V1, "o": ORF}).groupby("uf").median().drop("ZZ", errors="ignore")
        X = np.column_stack([np.ones(len(e)), e.p1, e.p1 ** 2, e.o]); r = e.sw - X @ np.linalg.lstsq(X, e.sw, rcond=None)[0]
        t4 = float(np.abs((r - r.median()) / (1.4826 * np.median(np.abs(r - r.median())))).max())
        return t1, t2, t3, t4, int((zr < -5).sum())
    L2r, V2r = b["v13_2"].values.astype(float), b["validos_2"].values.astype(float); F2r = b["v22_2"].values.astype(float)
    base_ = testes(L2r, V2r)
    lim = (base_[0] + max(5, 5 * np.sqrt(base_[0])), base_[1] * 3, base_[2] + max(5, 5 * np.sqrt(base_[2])), 3.5)
    R["referencia_real"] = {"T1": base_[0], "T2": base_[1], "T3": base_[2], "T4": base_[3], "limiar": list(lim)}
    rng = np.random.default_rng(seed); N = len(b); reps = 30
    def det(t): return [t[i] > lim[i] for i in range(4)]
    acc = {}
    for rep in range(reps):
        Lw = rng.binomial(V2r.astype(int), np.clip(L2r / V2r, 0, 1)).astype(float); Fw = V2r - Lw
        d0 = det(testes(Lw, V2r)); acc.setdefault("ref", []).append(d0 + [any(d0)])
        sel = rng.random(N) < 0.01
        for m in mags:
            mov_a = np.minimum(np.round(V2r * m), Fw) * sel          # Flávio -> Lula
            mov_b = np.minimum(np.round(V2r * m), Lw) * sel          # Lula -> Flávio
            ta = testes(Lw + mov_a, V2r); tb = testes(Lw - mov_b, V2r)
            acc.setdefault(f"A_{m}", []).append(det(ta) + [any(det(ta))]); acc.setdefault(f"B_{m}", []).append(det(tb) + [any(det(tb))])
            acc.setdefault(f"T1neg_B_{m}", []).append([tb[4]])
    for k, v in acc.items():
        a = np.array(v, float)
        if k.startswith("T1neg"): R[k] = {"media_secoes_abaixo_de_menos_5": float(a.mean()), "referencia_real": base_[4]}; continue
        taxa = a.mean(0); ci = [wil(int(a[:, j].sum()), reps, method="wilson") for j in range(a.shape[1])]
        R[k] = {nome: {"taxa": float(taxa[j]), "ic95_wilson": [float(ci[j][0]), float(ci[j][1])]} for j, nome in enumerate(["T1", "T2", "T3", "T4", "conjunta"])}
    R["config"] = {"modo": modo, "seed": seed, "magnitudes_pct_validos": mags, "urnas_sorteadas": "1%", "replicas": reps}

elif P == "P16":
    import hashlib as H, collections
    import processar_brutos as PB
    RNG = np.random.default_rng(2028); NS = 200
    univ = pd.concat([pd.read_parquet(f, columns=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]) for f in sorted(glob.glob(AN + "/brutos/1t/urnas_*.parquet"))], ignore_index=True).astype(str).drop_duplicates().reset_index(drop=True)
    sel = univ.iloc[RNG.choice(len(univ), NS, replace=False)]
    zips = {}; res = []
    for r_ in sel.itertuples(index=False):
        uf, mun, zona, sec = r_; pacote, _ = PB.fonte(1, uf)
        if not os.path.exists(pacote): res.append({"chave": [uf, mun, zona, sec], "erro": "sem pacote"}); continue
        zf = zips.setdefault(uf, zipfile.ZipFile(pacote)); idx = zips.setdefault(("idx", uf), {})
        if not idx:
            for n in zf.namelist():
                a = PB.analisa_nome(n, uf)
                if a: idx[(a[0], a[1])] = n
        mem = {t: idx[((uf, mun, zona, sec), t)] for t in ("bu", "log", "rdv", "imgbu", "vota") if ((uf, mun, zona, sec), t) in idx}
        r = {"chave": [uf, mun, zona, sec], "arquivos": sorted(mem)}
        if "vota" not in mem: r["erro"] = "sem lista assinada"; res.append(r); continue
        dados = {t: zf.read(n) for t, n in mem.items()}
        lista, resumo, ver = PB.ler_vsc(dados["vota"]); r["emissor"] = resumo.get("cert_emissor"); r["algoritmo"] = resumo.get("algoritmo"); r["lista_ok"] = bool(resumo.get("assin_lista_ok"))
        r["hash_ok"] = all(lista.get(mem[t]) and lista[mem[t]][:2] == (len(d), H.sha512(d).digest()) for t, d in dados.items() if t != "vota")
        r["assin_ok"] = all(lista.get(mem[t]) and ver(lista[mem[t]][2], lista[mem[t]][1]) for t in dados if t != "vota")
        bu = PB.ler_bu(dados["bu"], 1) if "bu" in dados else {}
        try: rdv = PB.ler_rdv(dados["rdv"], 1) if "rdv" in dados else {}
        except (KeyError, IndexError): rdv = {}
        img = PB.ler_imgbu(dados["imgbu"]) if "imgbu" in dados else None; lg_ = PB.ler_log(dados["log"], 1)[0] if "log" in dados else {}
        cand = [k for k in bu if k.startswith("bu_v")]
        r["rdv_igual_bu"] = bool(rdv) and all(rdv.get("rdv_" + k[3:], 0) == bu[k] for k in cand) and rdv.get("rdv_branco", 0) == bu.get("bu_branco", 0) and rdv.get("rdv_nulo", 0) + rdv.get("rdv_tipo6", 0) == bu.get("bu_nulo", 0)
        r["img_igual_bu"] = bool(img) and all(img.get("img_" + k[3:], 0) == bu[k] for k in cand) and img.get("img_branco", 0) == bu.get("bu_branco", 0) and img.get("img_nulo", 0) == bu.get("bu_nulo", 0)
        r["log_igual_comparecimento"] = lg_.get("computado") == bu.get("bu_comparecimento")
        r["bu"] = {k: v for k, v in bu.items() if k.startswith(("bu_v", "bu_b", "bu_n", "bu_comp"))}; r["cert"] = resumo.get("cert_urna"); r["_cert_bytes_ok"] = True
        res.append(r)
    # BU na Web
    por_uf = collections.defaultdict(dict)
    for r in res:
        if "bu" in r: por_uf[r["chave"][0]][tuple(r["chave"][1:])] = r
    for uf, ks in por_uf.items():
        f = f"{RAIZ}/dados/1turno/bweb_1t_{uf}_presidente.csv"; acc = collections.defaultdict(lambda: collections.defaultdict(int)); comp_ = {}
        for ch in pd.read_csv(f, sep=";", encoding="latin1", dtype=str, chunksize=500000, usecols=["CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_VOTAVEL", "QT_VOTOS", "QT_COMPARECIMENTO", "DS_TIPO_VOTAVEL"]):
            ch["k"] = list(zip(ch.CD_MUNICIPIO.astype(int).astype(str), ch.NR_ZONA.astype(int).astype(str), ch.NR_SECAO.astype(int).astype(str)))
            for k, g in ch[ch.k.isin(list(ks))].groupby("k"):
                for x in g.itertuples():
                    t = x.DS_TIPO_VOTAVEL.lower(); nm = "branco" if "branco" in t else "nulo" if "nulo" in t else f"v{int(x.NR_VOTAVEL)}"; acc[k][nm] += int(x.QT_VOTOS)
                comp_[k] = int(g.QT_COMPARECIMENTO.iloc[0])
        for k, r in ks.items():
            web = dict(acc.get(k, {})); bun = {kk[3:]: v for kk, v in r["bu"].items() if kk.startswith(("bu_v", "bu_branco", "bu_nulo"))}
            r["web_igual_bu"] = bool(web) and all(web.get(kk, 0) == v for kk, v in bun.items()) and all(bun.get(kk, 0) == v for kk, v in web.items()); r["web_comparecimento_igual"] = comp_.get(k) == r["bu"].get("bu_comparecimento")
    ok = [r for r in res if "bu" in r]
    cont = lambda c: sum(1 for r in ok if r.get(c) is True)
    R["amostra"] = {"sorteadas": NS, "com_arquivos_e_lista": len(ok), "sem_lista_ou_pacote": NS - len(ok), "hash_ok": cont("hash_ok"), "assinatura_ok": cont("assin_ok"), "lista_ok": cont("lista_ok"), "rdv_igual_bu": cont("rdv_igual_bu"),
                    "imagem_igual_bu": cont("img_igual_bu"), "bu_na_web_igual": cont("web_igual_bu"), "comparecimento_web_igual": cont("web_comparecimento_igual"), "log_igual_comparecimento": cont("log_igual_comparecimento"),
                    "emissores": dict(collections.Counter(r["emissor"] for r in ok))}
    R["divergentes"] = [r for r in ok if not all(r.get(c) is True for c in ("hash_ok", "assin_ok", "lista_ok", "rdv_igual_bu", "img_igual_bu", "web_igual_bu", "web_comparecimento_igual", "log_igual_comparecimento"))]
    R["semente"] = 2028

elif P == "P11":
    import hashlib as H, collections, base64
    import processar_brutos as PB, der, ed521
    from cryptography import x509
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import hashes
    CERT = RAIZ + "/fase2/externos/certificados"
    ac = {}
    for nome in ("acurna", "acue2020", "acue2022"):
        pem = open(f"{CERT}/{nome}_certificado_publico.txt", "rb").read(); c = x509.load_pem_x509_certificate(pem); ac[c.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value] = (c, pem)
    def pub_ed(pem):
        raiz_, _ = der.ler(base64.b64decode(b"".join(l for l in pem.splitlines() if not l.startswith(b"-")))); return raiz_["f"][0]["f"][6]["f"][1]["v"][1:]
    def ed_var(pub, sig, M):
        if len(pub) != 66 or len(sig) != 132: return False
        A = ed521.decodifica(pub); Rb = sig[:66]; Rp = ed521.decodifica(Rb)
        if A is None or Rp is None: return False
        S = ed521.mpz(int.from_bytes(sig[66:], "little"))
        if S >= ed521.L: return False
        k = ed521.mpz(int.from_bytes(H.shake_256(ed521.DOM + Rb + pub + M).digest(132), "little")) % ed521.L
        return ed521.igual(ed521.mult_base(S), ed521.soma(Rp, ed521.mult(k, A)))
    # as 3 variantes de mensagem para a assinatura dos certificados das ACs (e das urnas) nas Ed521
    amostra = json.load(open(f"{RAIZ}/fase2/resultados/P16.json"))
    chaves = [tuple(r["chave"]) for r in amostra["divergentes"]] if False else None
    univ = None
    rng = np.random.default_rng(2028)
    u = pd.concat([pd.read_parquet(f, columns=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]) for f in sorted(glob.glob(AN + "/brutos/1t/urnas_*.parquet"))], ignore_index=True).astype(str).drop_duplicates().reset_index(drop=True)
    sel = u.iloc[rng.choice(len(u), 200, replace=False)]   # a mesma amostra do P16 (mesma semente e universo)
    zips = {}; cont = collections.Counter(); var_ok = collections.Counter(); falhas = []
    for r_ in sel.itertuples(index=False):
        uf, mun, zona, sec = r_; pacote, _ = PB.fonte(1, uf); zf = zips.setdefault(uf, zipfile.ZipFile(pacote))
        idx = zips.setdefault(("i", uf), {})
        if not idx:
            for n in zf.namelist():
                a_ = PB.analisa_nome(n, uf)
                if a_: idx[(a_[0], a_[1])] = n
        n = idx.get(((uf, mun, zona, sec), "vota"))
        raiz_, _ = der.ler(zf.read(n)); ue = next(bl for bl in raiz_["f"] if bl["k"] and len(bl["f"]) >= 5 and bl["f"][2]["k"] and bl["f"][2]["f"][0]["f"][0]["v"][:4].upper() == b"UEAO")
        cb = ue["f"][4]["v"]
        if cb.startswith(b"-----BEGIN"):
            c = x509.load_pem_x509_certificate(cb); emis = c.issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value; cont[emis] += 1
            if emis not in ac: cont["emissor_sem_certificado"] += 1; continue
            pub = pub_ed(ac[emis][1]); tbs, sig = c.tbs_certificate_bytes, c.signature; ok = None
            for nome, M in (("M=TBS", tbs), ("M=SHA512(TBS)", H.sha512(tbs).digest()), ("M=SHA512(SHA512(TBS))", H.sha512(H.sha512(tbs).digest()).digest())):
                if ed_var(pub, sig, M): ok = nome; break
            cont["cert_urna_ed521_assinatura_ok" if ok else "cert_urna_ed521_assinatura_falhou"] += 1
            if ok: var_ok[ok] += 1
            else: falhas.append([uf, mun, zona, sec, emis])
        else:
            _, fim = der.ler(cb); c = x509.load_der_x509_certificate(cb[:fim]); emis = c.issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value; cont[emis] += 1
            try: c.verify_directly_issued_by(ac["AC URNA"][0]); cont["cert_urna_ecdsa_assinatura_ok"] += 1
            except Exception as e: cont["cert_urna_ecdsa_assinatura_falhou"] += 1; falhas.append([uf, mun, zona, sec, emis, str(e)[:80]])
    # elo AC -> AC URNA v2 / AC RAIZ: os certificados de AC UE2020/2022 são assinados pela AC URNA v2, que não temos
    R["amostra"] = 200; R["contagens"] = dict(cont); R["variante_de_mensagem_que_validou_ed521"] = dict(var_ok); R["falhas"] = falhas[:10]
    R["acs_obtidas"] = {k: {"sha256_pem": H.sha256(v[1]).hexdigest(), "emissor": v[0].issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value, "fonte": "github.com/alissonlinneker/DataUrnas-BR (terceiro)"} for k, v in ac.items()}
    R["limite"] = "Elo verificado: certificado da urna assinado pela chave da AC UE2020/UE2022/URNA. A origem desses certificados de AC é um repositório de terceiros; o elo AC → AC URNA v2 → AC RAIZ UE não foi verificado (AC URNA v2 e AC RAIZ UE não obtidas por canal do TSE)."

else:
    sys.exit("pergunta sem implementação aqui: " + P)

R["tempo_s"] = round(time.time() - T0, 1)
json.dump(R, open(f"{OUT}/{P}{'_' + MODO if MODO else ''}.json", "w"), indent=1, ensure_ascii=False, default=float)
print(P, "ok", R["tempo_s"], "s")
