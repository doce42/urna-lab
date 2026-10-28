"""F3: P18 (T13 de duas caudas), P19 (Moran's I), P20 (São Paulo 2022). Uso: f3_pendencias.py p18|p19|p20"""
import glob, json, sys, time
import numpy as np, pandas as pd
from scipy import stats

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; OUT = RAIZ + "/fase3/resultados"; Q = sys.argv[1]; T0 = time.time()
lg = lambda x, n: np.log((x + .5) / (n - x + .5)); inv = lambda z: 1 / (1 + np.exp(-z))
K = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
R = {"pergunta": Q}


def wil(k, n):
    z_ = 1.96; ph = k / n; den = 1 + z_ * z_ / n; c = (ph + z_ * z_ / (2 * n)) / den; h = z_ * np.sqrt(ph * (1 - ph) / n + z_ * z_ / (4 * n * n)) / den
    return float(max(0, c - h)), float(min(1, c + h))


if Q == "p18":
    def rodar(ano, seed, mags, reps=30):
        b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
        b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20)].reset_index(drop=True); b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
        b = b.sort_values("DT_BU_RECEBIDO_2").reset_index(drop=True)
        L1, V1 = b["v13_1"].values.astype(float), b["validos_1"].values.astype(float); ORF = 1 - (b["v13_1"].values + b["v22_1"].values) / V1
        mun = pd.factorize(b["mun"])[0]; uf = b["SG_UF"].values; minuto = b["DT_BU_RECEBIDO_2"].dt.floor("1min").values
        comp, aptos = b["QT_COMPARECIMENTO_2"].values.astype(float), b["QT_APTOS_2"].values.astype(float)

        def testes(L2, V2):
            sw = lg(L2, V2) - lg(L1, V1); s = pd.Series(sw); res = sw - s.groupby(mun).transform("median").values
            sd = np.sqrt(1/(L1+.5) + 1/(V1-L1+.5) + 1/(L2+.5) + 1/(V2-L2+.5)); z = res / sd; zr = z / (1.4826 * np.median(np.abs(z - np.median(z))))
            t1p, t1n = int((zr > 5).sum()), int((zr < -5).sum())
            prev = inv(lg(L1, V1) + s.groupby(uf).transform("median").values) * V2
            df = pd.DataFrame({"m": minuto, "L": L2, "P": prev, "V": V2}).groupby("m").sum().cumsum(); t2 = float(100 * ((df.L - df.P) / df.V).abs().max())
            F2 = V2 - L2; t3p = int(((comp / aptos >= .95) & (L2 / V2 >= .9)).sum()); t3n = int(((comp / aptos >= .95) & (F2 / V2 >= .9)).sum())
            e = pd.DataFrame({"uf": uf, "sw": sw, "p1": L1 / V1, "o": ORF}).groupby("uf").median().drop("ZZ", errors="ignore")
            X = np.column_stack([np.ones(len(e)), e.p1, e.p1 ** 2, e.o]); r = e.sw - X @ np.linalg.lstsq(X, e.sw, rcond=None)[0]
            t4 = float(np.abs((r - r.median()) / (1.4826 * np.median(np.abs(r - r.median())))).max())
            return np.array([t1p, t1n, t2, t3p, t3n, t4], float)
        L2r, V2r = b["v13_2"].values.astype(float), b["validos_2"].values.astype(float)
        base_ = testes(L2r, V2r); N = len(b); rng = np.random.default_rng(seed)
        lim_real = np.array([base_[0] + max(5, 5 * np.sqrt(base_[0])), base_[1] + max(5, 5 * np.sqrt(base_[1])), base_[2] * 3, base_[3] + max(5, 5 * np.sqrt(base_[3])), base_[4] + max(5, 5 * np.sqrt(base_[4])), 3.5])
        # mundos de referência (legítimos) e calibração alternativa dos limiares: máximo das réplicas de referência
        mundos = []
        for _ in range(reps):
            Lw = rng.binomial(V2r.astype(int), np.clip(L2r / V2r, 0, 1)).astype(float); mundos.append(Lw)
        ref = np.array([testes(Lw, V2r) for Lw in mundos]); lim_mundo = ref.max(0) * 1.0 + np.array([5, 5, 0.05, 5, 5, 0.5])
        rot = {"limiar_real": lim_real, "limiar_calibrado_no_mundo": lim_mundo}
        out = {"referencia_real": base_.tolist(), "limiar_real": lim_real.tolist(), "limiar_mundo": lim_mundo.tolist(), "urnas": N}
        nomes = ["T1_pro", "T1_contra", "T2", "T3_pro", "T3_contra", "T4"]
        for rn, lim in rot.items():
            conj = lambda a: bool((a > lim).any())
            out[rn] = {"referencia_alarme": wil(sum(conj(r) for r in ref), reps) + (sum(conj(r) for r in ref) / reps,)}
        sel_sets = [rng.random(N) < 0.01 for _ in range(reps)]
        for m in mags:
            for sentido in ("A_Flavio_para_Lula", "B_Lula_para_Flavio"):
                dets = {k: [] for k in rot}; por_t = []
                for Lw, sel in zip(mundos, sel_sets):
                    F = V2r - Lw
                    mov = np.minimum(np.round(V2r * m), F if sentido.startswith("A") else Lw) * sel
                    Lm = Lw + mov if sentido.startswith("A") else Lw - mov
                    t = testes(Lm, V2r)
                    for rn, lim in rot.items(): dets[rn].append(bool((t > lim).any()))
                    por_t.append(t > rot["limiar_calibrado_no_mundo"])
                out[f"{sentido}_{int(m*100)}pct"] = {rn: {"taxa": float(np.mean(v)), "ic95_wilson": wil(sum(v), reps)} for rn, v in dets.items()}
                out[f"{sentido}_{int(m*100)}pct"]["por_teste_limiar_mundo"] = dict(zip(nomes, np.mean(por_t, 0).round(2).tolist()))
        return out
    R["principal_2026"] = rodar("2026", 4001, [0.05, 0.10])
    R["sensibilidade_2022"] = rodar("2022", 4002, [0.05, 0.10])

elif Q == "p19":
    from scipy.spatial import cKDTree
    geo = json.load(open(RAIZ + "/grafico/relatorio-app/dist/dados/geo.json")); tse = json.load(open(RAIZ + "/grafico/web/geo/tse_municipios_2026.json"))
    ibge = {}
    for ab in tse["abr"]:
        for m in ab["mu"]:
            if str(m["cdi"]).strip().isdigit(): ibge[(ab["cd"].upper(), str(int(m["cd"])))] = int(m["cdi"])
    geoms = geo["objects"]["municipios"]["geometries"]; arcs_de = {}
    def colhe(a, acc):
        for x in a:
            if isinstance(x, list): colhe(x, acc)
            else: acc.add(x if x >= 0 else ~x)
    for g in geoms:
        s = set(); colhe(g["arcs"], s); arcs_de[g["id"]] = s
    dono = {}
    for gid, s in arcs_de.items():
        for a in s: dono.setdefault(a, []).append(gid)
    viz = {gid: set() for gid in arcs_de}
    for a, l in dono.items():
        if len(l) > 1:
            for i in l: viz[i].update(set(l) - {i})
    # centróides aproximados (média dos vértices dos arcos) para a vizinhança de k vizinhos (sensibilidade)
    sc, tr = geo["transform"]["scale"], geo["transform"]["translate"]; arcos = geo["arcs"]
    def cent(s):
        pts = []
        for a in s:
            q = np.cumsum(np.array(arcos[a]), axis=0); pts.append(q)
        q = np.concatenate(pts); return q.mean(0) * sc + tr
    ids = list(arcs_de); C = np.array([cent(arcs_de[i]) for i in ids]); idx = {g: i for i, g in enumerate(ids)}
    R["malha"] = {"municipios": len(ids), "com_vizinho_por_arco": int(sum(1 for v in viz.values() if v)), "media_vizinhos": float(np.mean([len(v) for v in viz.values()]))}
    def moran(z, W):
        zc = z - z.mean(); num = (W.multiply(np.outer(zc, zc)) if False else None)
        return None
    from scipy import sparse
    for ano in ("2026", "2022"):
        d = pd.read_csv(f"{AN}/divergencias_municipios_{ano}_completo.csv", sep=";"); d = d[d.k >= 3].copy()
        d["ibge"] = [ibge.get((r.uf, r.mun.split("-")[1]), None) for r in d.itertuples()]
        d = d[d.ibge.isin(idx)].reset_index(drop=True); pos = {g: i for i, g in enumerate(d.ibge)}
        n = len(d); rows, cols = [], []
        for g, i in pos.items():
            for h in viz[g]:
                if h in pos: rows.append(i); cols.append(pos[h])
        W = sparse.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n)); sem = np.asarray(W.sum(1)).ravel() == 0
        Wk = None
        tree = cKDTree(C[[idx[g] for g in d.ibge]]); _, nn = tree.query(C[[idx[g] for g in d.ibge]], k=6)
        rk = np.repeat(np.arange(n), 5); ck = nn[:, 1:].ravel(); Wk = sparse.csr_matrix((np.ones(len(rk)), (rk, ck)), shape=(n, n))
        z = d["zg"].values / np.sqrt(d["k"].values) * 1.0   # z médio do município (zg = média·√k)
        def I(W, v):
            Wr = sparse.diags(1 / np.maximum(np.asarray(W.sum(1)).ravel(), 1)) @ W; vc = v - v.mean(); return float(n / n * (vc @ (Wr @ vc)) / (vc @ vc))
        rng = np.random.default_rng(1900 + int(ano) % 100); res = {}
        for nome, Wm in (("rainha_por_arco", W), ("5_vizinhos_mais_proximos", Wk)):
            i0 = I(Wm, z); sims = np.array([I(Wm, rng.permutation(z)) for _ in range(999)])
            res[nome] = {"I": i0, "esperado_H0": float(-1 / (n - 1)), "p_bilateral_perm": float((1 + (np.abs(sims) >= abs(i0)).sum()) / 1000), "sim_p2_5_p97_5": [float(np.percentile(sims, 2.5)), float(np.percentile(sims, 97.5))]}
        res["municipios"] = n; res["sem_vizinho_na_amostra"] = int(sem.sum())
        # sensibilidade: sem os 5% de municípios com maior |z| (a dependência pode vir de poucos extremos)
        keep = np.abs(z) <= np.percentile(np.abs(z), 95); res["sem_5pct_extremos_rainha"] = {"I": I(W[keep][:, keep], z[keep])}
        R[ano] = res

elif Q == "p20":
    b = pd.read_parquet(f"{AN}/base_2022.parquet"); b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20) & (b["SG_UF"] != "ZZ")].copy(); b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
    x1, n1, x2, n2 = b["v13_1"], b["validos_1"], b["v13_2"], b["validos_2"]; b["sw"] = lg(x2, n2) - lg(x1, n1); b["res"] = b["sw"] - b.groupby("mun")["sw"].transform("median")
    z = b["res"] / np.sqrt(1/(x1+.5) + 1/(n1-x1+.5) + 1/(x2+.5) + 1/(n2-x2+.5)); b["z"] = z / (1.4826 * (z - z.median()).abs().median())
    b["local"] = b["mun"] + "-" + b["NR_ZONA"].astype(str) + "-" + b["NR_LOCAL_VOTACAO_2"].astype(str)
    sp = b[b.mun == "SP71072"].copy(); at = sp[sp.z > 5]
    R["sp_capital"] = {"secoes": int(len(sp)), "atipicas_pro_lula": int(len(at)), "locais_com_atipicas": int(at.local.nunique()), "atipicas_por_local": at.local.value_counts().head(8).to_dict(), "zonas": at.NR_ZONA.value_counts().head(8).to_dict()}
    # efeito de local: z médio do local sem a própria seção
    sp["loo_z"] = (sp.groupby("local")["z"].transform("sum") - sp["z"]) / (sp.groupby("local")["z"].transform("size") - 1).replace(0, np.nan)
    at = sp[sp.z > 5]
    R["efeito_do_local"] = {"z_medio_das_outras_secoes_do_local_nas_atipicas": float(at.loo_z.mean()), "z_medio_das_outras_secoes_do_local_nas_demais_de_SP": float(sp[sp.z <= 5].loo_z.mean()),
                            "atipicas_em_locais_onde_as_outras_secoes_tem_z_medio_acima_de_1": int((at.loo_z > 1).sum()), "atipicas_sem_outra_secao_no_local": int(at.loo_z.isna().sum())}
    # controles de tamanho e comportamento anterior (OLS dentro de SP capital) e z residual
    X = np.column_stack([np.ones(len(sp)), np.log(sp.validos_2), sp.v13_1 / sp.validos_1, (sp.v13_1 / sp.validos_1) ** 2, sp.QT_COMPARECIMENTO_2 / sp.QT_APTOS_2])
    beta = np.linalg.lstsq(X, sp.z.values, rcond=None)[0]; sp["z_adj"] = sp.z.values - X @ beta
    zs = sp.z_adj / (1.4826 * (sp.z_adj - sp.z_adj.median()).abs().median()); sp["z_adj_s"] = zs
    R["apos_controle_tamanho_e_historico"] = {"atipicas_com_z_ajustado_maior_que_5": int((sp.loc[at.index, "z_adj_s"] > 5).sum()), "de": int(len(at)), "r2": float(1 - ((sp.z.values - X @ beta) ** 2).sum() / ((sp.z.values - sp.z.mean()) ** 2).sum())}
    R["caracteristicas"] = {"validos_2_mediana_atipicas": float(at.validos_2.median()), "validos_2_mediana_SP": float(sp.validos_2.median()), "p1_lula_mediana_atipicas": float((at.v13_1 / at.validos_1).median()), "p1_lula_mediana_SP": float((sp.v13_1 / sp.validos_1).median()),
                            "delta_comparecimento_pp_medio_atipicas": float(100 * ((at.QT_COMPARECIMENTO_2 / at.QT_APTOS_2) - (at.QT_COMPARECIMENTO_1 / at.QT_APTOS_1)).mean()), "delta_comparecimento_pp_medio_SP": float(100 * ((sp.QT_COMPARECIMENTO_2 / sp.QT_APTOS_2) - (sp.QT_COMPARECIMENTO_1 / sp.QT_APTOS_1)).mean())}
    # as mesmas seções (zona/seção) em 2026
    b6 = pd.read_parquet(f"{AN}/base.parquet"); b6 = b6[b6.SG_UF == "SP"]
    ch = at[["NR_ZONA", "NR_SECAO"]].astype(str).assign(k=lambda d: d.NR_ZONA + "-" + d.NR_SECAO)
    b6 = b6[b6.CD_MUNICIPIO.astype(str) == "71072"].copy(); b6["k"] = b6.NR_ZONA.astype(str) + "-" + b6.NR_SECAO.astype(str)
    x1, n1, x2, n2 = b6.v13_1, b6.validos_1, b6.v13_2, b6.validos_2; b6["sw"] = lg(x2, n2) - lg(x1, n1); b6["res"] = b6["sw"] - b6["sw"].median()
    zz = b6.res / np.sqrt(1/(x1+.5) + 1/(n1-x1+.5) + 1/(x2+.5) + 1/(n2-x2+.5)); b6["z"] = zz / (1.4826 * (zz - zz.median()).abs().median())
    m26 = b6[b6.k.isin(ch.k)]
    R["mesmas_secoes_em_2026"] = {"encontradas": int(len(m26)), "z_medio_2026": float(m26.z.mean()), "z_medio_2026_demais_secoes_de_SP": float(b6[~b6.k.isin(ch.k)].z.mean()), "acima_de_3_em_2026": int((m26.z > 3).sum()),
                                   "correlacao_z_2022_2026_nas_atipicas": float(np.corrcoef(at.assign(k=at.NR_ZONA.astype(str) + "-" + at.NR_SECAO.astype(str)).set_index("k").z.reindex(m26.k).values, m26.z.values)[0, 1]) if len(m26) > 3 else None}
    # arquivos das urnas das atípicas (2º turno 2022)
    fs = glob.glob(f"{AN}/brutos/2022_2t/urnas_SP.parquet"); u = pd.read_parquet(fs[0]); u = u.astype({k: str for k in K})
    a2 = at[K].astype(str).merge(u, on=K, how="left")
    R["arquivos_das_atipicas_2t_2022"] = {"secoes": int(len(a2)), "sem_linha": int(a2.assin_lista_ok.isna().sum()), "lista_assinada_ok": int((a2.assin_lista_ok == True).sum()), "hash_bu_ok": int((a2.hash_ok_bu == True).sum()), "assin_bu_ok": int((a2.assin_ok_bu == True).sum()),
                                           "rdv_igual_bu": int(((a2.rdv_v13.fillna(0) == a2.bu_v13.fillna(0)) & (a2.rdv_v22.fillna(0) == a2.bu_v22.fillna(0))).sum()) if "rdv_v13" in a2 else None,
                                           "log_igual_comparecimento": int((a2.computado == a2.bu_comparecimento).sum()), "modelos": a2.modelo.value_counts().to_dict(), "urnas_substituidas": int((a2.urnas_com_voto_no_log.fillna(1) > 1).sum())}
R["tempo_s"] = round(time.time() - T0, 1)
json.dump(R, open(f"{OUT}/{Q}.json", "w"), indent=1, ensure_ascii=False, default=float)
print(Q, "ok", R["tempo_s"], "s")
