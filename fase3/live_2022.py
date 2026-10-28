"""T45 a T48: alegações da live de 4/11/2022 e do pedido do PL (pré-registro em fase3/PREREG_LIVE_2022.md)."""
import glob, json, time
import numpy as np, pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; OUT = RAIZ + "/fase3/resultados/live_2022.json"
ID_FIXO = "67305985"; ANTIGOS = {"UE2009", "UE2010", "UE2011", "UE2013", "UE2015"}
CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
T0 = time.time(); R = {"pre_registro": "fase3/PREREG_LIVE_2022.md"}


def urnas(pasta, cols):
    return pd.concat([pd.read_parquet(f, columns=CH + cols) for f in glob.glob(f"{AN}/brutos/{pasta}/urnas_*.parquet")]).astype({c: str for c in CH})


def base(ano):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
    return b.astype({c: str for c in CH})


def juntar(ano, t, cols):
    pasta = {"2022": f"2022_{t}t", "2026": f"{t}t"}[ano]
    m = base(ano).merge(urnas(pasta, cols + ["modelo"]), on=CH, how="inner")
    m = m[m.modelo.notna() & (m.modelo != "None")].copy()
    m["mun"] = m.SG_UF + m.CD_MUNICIPIO
    m["grupo"] = np.where(m.modelo.isin(ANTIGOS), "pre2020", m.modelo)
    return m


# ---------------- T45: ID fixo e ligação log -> BU -> RDV ----------------
t45 = {}
for ano in ("2022", "2026"):
    for t in (1, 2):
        m = juntar(ano, t, ["ids_urna_log", "cert_urna", "assin_lista_ok", "hash_ok_log", "assin_ok_log", "hash_ok_bu", "assin_ok_bu",
                            "hash_ok_rdv", "assin_ok_rdv", "bu_v13", "bu_v22", "bu_branco", "bu_nulo", "rdv_v13", "rdv_v22", "rdv_branco", "rdv_nulo"])
        m["id_fixo"] = m.ids_urna_log.fillna("").str.split(",").apply(lambda l: ID_FIXO in l)
        assin = m[["assin_lista_ok", "hash_ok_log", "assin_ok_log", "hash_ok_bu", "assin_ok_bu", "hash_ok_rdv", "assin_ok_rdv"]].fillna(False).astype(bool).all(axis=1)
        num_cert = pd.to_numeric(m.cert_urna.fillna("").str.extract(r"(\d+)$")[0], errors="coerce")
        cert_ok = num_cert == pd.to_numeric(m[f"NR_URNA_EFETIVADA_{t}"], errors="coerce")
        agreg = m[f"DS_SECOES_AGREGADAS_{t}"].fillna("").astype(str).str.strip().isin(["", "#NULO#", "nan"]).eq(False) if f"DS_SECOES_AGREGADAS_{t}" in m else pd.Series(False, m.index)
        # correção 1 (artefato do comparador): o BU e o RDV omitem quem teve zero voto; ausente = 0 quando o arquivo foi lido
        lido = m[["bu_v13", "bu_v22", "bu_branco", "bu_nulo"]].notna().any(axis=1).values
        votos = lido.copy()
        for c in ("v13", "v22", "branco"):
            bu, rdv = m[f"bu_{c}"].fillna(0).values, m[f"rdv_{c}"].fillna(0).values
            votos &= (bu == rdv) & (bu == m[f"{c}_{t}"].fillna(-1).values)
        nulo_ok = lido & (m.bu_nulo.fillna(0).values == m.rdv_nulo.fillna(0).values)
        m["liga"] = assin & cert_ok & votos
        por = {}
        for mod, g in m.groupby("modelo"):
            f = g[g.id_fixo]
            por[mod] = {"secoes": int(len(g)), "com_id_fixo_67305985": int(g.id_fixo.sum()),
                        "id_fixo_assinaturas_ok": int(assin[f.index].sum()), "id_fixo_certificado_igual_urna_efetivada": int(cert_ok[f.index].sum()),
                        "id_fixo_votos_bu_rdv_tabela_iguais": int(votos[m.index.get_indexer(f.index)].sum()),
                        "id_fixo_nulo_bu_igual_rdv": int(nulo_ok[m.index.get_indexer(f.index)].sum())}
        falha = m[m.id_fixo & ~m.liga]
        sem_bu = ~lido
        t45[f"{ano}_{t}t"] = {"por_modelo": por, "id_fixo_sem_ligacao": int(len(falha)),
                               "id_fixo_sem_ligacao_agregadas": int(agreg[falha.index].sum()),
                               "id_fixo_sem_bu_lido": int((m.id_fixo.values & sem_bu).sum()),
                               "exemplos_sem_ligacao": falha[CH + ["modelo", "cert_urna", f"NR_URNA_EFETIVADA_{t}"]].head(20).astype(str).to_dict("records")}
R["T45"] = t45; print("T45", round(time.time() - T0), "s", flush=True)

# ---------------- T46: 51,05% só UE2020 ----------------
t46 = {}
for t in (1, 2):
    m = juntar("2022", t, [])
    nova = m[m.modelo == "UE2020"]
    L, B = nova[f"v13_{t}"].sum(), nova[f"v22_{t}"].sum()
    r = {"so_ue2020_bolsonaro_sobre_lula_mais_bolsonaro": float(B / (L + B)), "so_ue2020_lula": int(L), "so_ue2020_bolsonaro": int(B),
         "so_ue2020_bolsonaro_sobre_validos": float(B / nova[f"validos_{t}"].sum()), "so_ue2020_lula_sobre_validos": float(L / nova[f"validos_{t}"].sum()),
         "todas_bolsonaro_sobre_lula_mais_bolsonaro": float(m[f"v22_{t}"].sum() / (m[f"v13_{t}"].sum() + m[f"v22_{t}"].sum()))}
    # contrafactual dentro do município
    m["lb"] = m[f"v13_{t}"] + m[f"v22_{t}"]
    pn = nova.assign(lb=nova[f"v13_{t}"] + nova[f"v22_{t}"]).groupby("mun").apply(lambda g: g[f"v13_{t}"].sum() / g.lb.sum(), include_groups=False)
    tem = m.groupby("mun")["grupo"].agg(lambda s: {"pre2020", "UE2020"} <= set(s))
    m["p_nova"] = m.mun.map(pn); m["ambos"] = m.mun.map(tem)
    troca = (m.grupo == "pre2020") & m.ambos
    lula_cf = np.where(troca, m.p_nova * m.lb, m[f"v13_{t}"])
    bols_cf = np.where(troca, (1 - m.p_nova) * m.lb, m[f"v22_{t}"])
    r["contrafactual_mun"] = {"municipios_com_os_dois": int(tem.sum()), "secoes_pre2020_substituidas": int(troca.sum()),
                              "secoes_pre2020_sem_ue2020_no_municipio": int(((m.grupo == "pre2020") & ~m.ambos).sum()),
                              "bolsonaro_sobre_lula_mais_bolsonaro": float(bols_cf.sum() / (lula_cf.sum() + bols_cf.sum())),
                              "diferenca_lula_em_votos": float(lula_cf.sum() - m[f"v13_{t}"].sum())}
    t46[f"{t}t"] = r
R["T46"] = t46; print("T46", round(time.time() - T0), "s", flush=True)


# ---------------- T47: nível do voto por modelo ----------------
def efeito(x, n, cod, grp, grupos, nm, reps=200, semente=5):
    """média, por grupo, do logit de Lula menos a média do bloco; IC por bootstrap de blocos"""
    z = lg(x, n); d = z - (np.bincount(cod, z, nm) / np.bincount(cod, minlength=nm))[cod]
    S = np.stack([np.bincount(cod, d * (grp == k), nm) for k in grupos], 1)
    C = np.stack([np.bincount(cod, (grp == k).astype(float), nm) for k in grupos], 1)
    est = S.sum(0) / C.sum(0); rng = np.random.default_rng(semente); bs = []
    for _ in range(reps):
        k = rng.integers(0, nm, nm); bs.append(S[k].sum(0) / C[k].sum(0))
    bs = np.array(bs)
    return est, np.percentile(bs, 2.5, 0), np.percentile(bs, 97.5, 0), C.sum(0)


t47 = {}
for t in (1, 2):
    m = juntar("2022", t, []); m = m[m[f"validos_{t}"] >= 20].copy()
    x, n = m[f"v13_{t}"].values.astype(float), m[f"validos_{t}"].values.astype(float)
    r = {}
    # (a) conta da live: municípios pequenos pelo eleitorado apto
    aptos_mun = m.groupby("mun")[f"QT_APTOS_{t}"].transform("sum")
    for corte in (77000, 38500):
        p = m[aptos_mun < corte]; agg = p.groupby(["SG_UF", "grupo"])[[f"v13_{t}", f"validos_{t}"]].sum()
        uf = (agg[f"v13_{t}"] / agg[f"validos_{t}"]).unstack()
        tot = p.groupby("grupo")[[f"v13_{t}", f"validos_{t}"]].sum()
        r[f"a_conta_live_aptos_menor_{corte}"] = {"total": (tot[f"v13_{t}"] / tot[f"validos_{t}"]).to_dict(),
                                                  "ufs_pre2020_maior": int((uf.pre2020 > uf.UE2020).sum()), "ufs_comparadas": int(uf.dropna().shape[0]),
                                                  "por_uf": uf.round(4).to_dict("index")}
    tot = m.groupby("grupo")[[f"v13_{t}", f"validos_{t}"]].sum(); r["a_bruto_brasil"] = (tot[f"v13_{t}"] / tot[f"validos_{t}"]).to_dict()
    # (b) dentro do município e (c) dentro do local, só blocos com os dois grupos
    for nivel, chave in (("b_municipio", m.mun), ("c_local", m.mun + "-" + m.NR_ZONA + "-" + m[f"NR_LOCAL_VOTACAO_{t}"].astype(str))):
        ok = m.assign(k=chave).groupby("k")["grupo"].transform(lambda s: s.eq("pre2020").any() and s.eq("UE2020").any()).values
        cod, un = pd.factorize(chave[ok]); nm = len(un); grp2 = np.where(m.grupo.values[ok] == "pre2020", "pre2020", "UE2020")
        est, lo, hi, cnt = efeito(x[ok], n[ok], cod, grp2, ["pre2020", "UE2020"], nm)
        rr = {"blocos": int(nm), "secoes": {k: int(c) for k, c in zip(["pre2020", "UE2020"], cnt)},
              "media_residuo_logit": {k: float(e) for k, e in zip(["pre2020", "UE2020"], est)},
              "ic95": {k: [float(a), float(b)] for k, a, b in zip(["pre2020", "UE2020"], lo, hi)},
              "equivalente_em_0_02": bool(all(abs(a) <= .02 and abs(b) <= .02 for a, b in zip(lo, hi)))}
        # por modelo
        mods = sorted(set(m.modelo.values[ok]))
        e2, l2, h2, c2 = efeito(x[ok], n[ok], cod, m.modelo.values[ok], mods, nm)
        rr["por_modelo"] = {k: {"secoes": int(c), "media": float(e), "ic95": [float(a), float(b)]} for k, e, a, b, c in zip(mods, e2, l2, h2, c2)}
        # votos: diferença pré2020 − UE2020 traduzida para as seções pré-2020
        p_ = x[ok] / n[ok]; pre = grp2 == "pre2020"
        rr["votos_lula_equivalentes_a_diferenca"] = float((est[0] - est[1]) * (p_[pre] * (1 - p_[pre]) * n[ok][pre]).sum())
        if nivel == "b_municipio":
            # calibração: rótulo embaralhado dentro do município
            rng = np.random.default_rng(7); fora = 0; ests = []
            semi = (hi - lo) / 2
            ordem = np.argsort(cod, kind="stable")
            z = lg(x[ok], n[ok]); d = z - (np.bincount(cod, z, nm) / np.bincount(cod, minlength=nm))[cod]
            for _ in range(200):
                perm = grp2.copy(); k = np.lexsort((rng.random(len(cod)), cod)); perm[ordem] = grp2[k]
                e = np.array([d[perm == g].mean() for g in ("pre2020", "UE2020")]); ests.append(e.tolist())
                fora += bool(any(abs(e - semi) > .02) or any(abs(e + semi) > .02))
            rr["calibracao"] = {"permutacoes": 200, "fracao_ic_fora_da_margem": fora / 200, "adequado": fora / 200 <= .10,
                                "nota": "IC das permutações aproximado com a semi-amplitude do bootstrap real (desvio declarado)"}
            # poder: 1% dos válidos de Bolsonaro para Lula só nas pré-2020
            xs = x[ok].copy(); xb = m[f"v22_{t}"].values[ok].astype(float)
            mov = np.minimum(np.round(.01 * n[ok]), xb) * pre; xs = xs + mov
            e3, l3, h3, _ = efeito(xs, n[ok], cod, grp2, ["pre2020", "UE2020"], nm, semente=6)
            rr["poder_fraude_1pct"] = {"media_pre2020": float(e3[0]), "ic95_pre2020": [float(l3[0]), float(h3[0])],
                                       "detectou_no_sentido_correto": bool(l3[0] > 0 and h3[0] > .02),
                                       "votos_movidos": int(mov.sum())}
        r[nivel] = rr
    t47[f"{t}t"] = r
R["T47"] = t47; print("T47", round(time.time() - T0), "s", flush=True)

# ---------------- T48: software e unanimidades ----------------
t48 = {}
for t in (1, 2):
    m = juntar("2022", t, ["sw_versoes", "sw_verif_falha"])
    sw = m.groupby("modelo")["sw_versoes"].value_counts().rename("n").reset_index()
    r = {"versoes_por_modelo": {k: dict(zip(g.sw_versoes.astype(str), g.n.astype(int))) for k, g in sw.groupby("modelo")},
         "falhas_verificacao_sw_por_modelo": m.groupby("modelo")["sw_verif_falha"].sum().astype(int).to_dict()}
    frac_mun = m.groupby(["mun", "modelo"]).size() / m.groupby("mun").size()
    for minv in (1, 20):
        q = m[m[f"validos_{t}"] >= minv]
        for cand, col in (("lula", "v13"), ("bolsonaro", "v22")):
            u = q[q[f"{col}_{t}"] == q[f"validos_{t}"]]
            obs = u.modelo.value_counts().to_dict()
            esp = {}
            for mod in sorted(m.modelo.unique()):
                esp[mod] = float(sum(frac_mun.get((mu, mod), 0.0) for mu in u.mun))
            r[f"unanimes_{cand}_validos_min_{minv}"] = {"total": int(len(u)), "observado_por_modelo": {k: int(v) for k, v in obs.items()},
                                                       "esperado_pela_presenca_no_municipio": {k: round(v, 1) for k, v in esp.items()},
                                                       "votos": int(u[f"{col}_{t}"].sum())}
    t48[f"{t}t"] = r
R["T48"] = t48
R["tempo_s"] = round(time.time() - T0)
json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1, default=str)
print("ok", R["tempo_s"], "s")
