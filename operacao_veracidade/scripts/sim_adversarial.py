"""T63: poder da bateria estatística contra mecanismos adversariais sintéticos (cópias em memória da base real do 2º turno).
Protocolo: operacao_veracidade/PROTOCOLO_PRE_EXECUCAO.md (detectores, limiares, grade e critérios fixados antes).
Uso: sim_adversarial.py <ano> [processos] [reps]  →  resultados/sim_<ano>.parquet e sim_<ano>_resumo.json
Dados sintéticos: nada aqui é voto real alterado; a base real é a referência, não verdade conhecida sem fraude."""
import hashlib, json, sys, time
import numpy as np, pandas as pd
from multiprocessing import Pool
from scipy import stats

ANO = sys.argv[1]; PROC = int(sys.argv[2]) if len(sys.argv) > 2 else 12; REPS = int(sys.argv[3]) if len(sys.argv) > 3 else 20
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; OP = RAIZ + "/operacao_veracidade"
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
NE = {"AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"}
GRANDES = {("SP", "SÃO PAULO"), ("RJ", "RIO DE JANEIRO"), ("DF", "BRASÍLIA"), ("CE", "FORTALEZA"), ("BA", "SALVADOR")}
XS = [25_000, 50_000, 100_000, 250_000, 500_000, 1_000_000, 2_220_000]

# ---------------- dados ----------------
b = pd.read_parquet(f"{AN}/base.parquet" if ANO == "2026" else f"{AN}/base_{ANO}.parquet")
b = b[(b.SG_UF != "ZZ") & (b.validos_1 >= 20) & (b.validos_2 >= 20) & b.QT_APTOS_2.notna()].reset_index(drop=True)
mun, MUN = pd.factorize(b.SG_UF + "|" + b.CD_MUNICIPIO.astype(str)); zon, ZON = pd.factorize(b.SG_UF + "|" + b.CD_MUNICIPIO.astype(str) + "|" + b.NR_ZONA.astype(str))
loc, LOC = pd.factorize(b.SG_UF + "|" + b.CD_MUNICIPIO.astype(str) + "|" + b.NR_ZONA.astype(str) + "|" + b.NR_LOCAL_VOTACAO_2.astype(str))
uf, UF = pd.factorize(b.SG_UF)
nm, nz, nl, nu, N = len(MUN), len(ZON), len(LOC), len(UF), len(b)
L1, V1 = b.v13_1.values.astype(float), b.validos_1.values.astype(float)
L2, V2 = b.v13_2.values.astype(float), b.validos_2.values.astype(float); F2 = V2 - L2
BN2 = (b.branco_2 + b.nulo_2).values.astype(float); T2 = V2 + BN2; A2 = b.QT_APTOS_2.values.astype(float)
T1 = b.QT_COMPARECIMENTO_1.values.astype(float); A1 = b.QT_APTOS_1.values.astype(float)
p1 = L1 / V1; turn1 = T1 / np.maximum(A1, 1)
ABS2 = np.maximum(A2 - T2, 0)
big = np.array([(u, n.upper()) in GRANDES for u, n in zip(b.SG_UF, b.NM_MUNICIPIO_2.fillna(""))])
big_mun = np.unique(mun[big])
recv = pd.to_datetime(b.DT_BU_RECEBIDO_2).values.astype("int64"); recv = np.where(recv > 0, recv, np.nanmedian(recv))
ne = b.SG_UF.isin(NE).values
mun_of_zone = np.zeros(nz, int); mun_of_zone[zon] = mun
mun_of_loc = np.zeros(nl, int); mun_of_loc[loc] = mun
cnt = lambda ids, k: np.bincount(ids, minlength=k).astype(float)
nsec_m, nsec_z, nsec_l = cnt(mun, nm), cnt(zon, nz), cnt(loc, nl)
ufm = np.zeros(nm, int); ufm[mun] = uf
base_logit1_m = lg(np.bincount(mun, L1, nm), np.bincount(mun, V1, nm)); sz_m = np.log(np.bincount(mun, V1, nm))
X_ols = np.column_stack([np.eye(nu)[ufm], base_logit1_m, sz_m])


# ---------------- detectores ----------------
def estat(L2_, V2_, T2_, ref=None):
    """Devolve vetores/estatísticas brutas. ref: (S0, S3, S4) escalas robustas da base (fixas, como faria um analista)."""
    sw = lg(L2_, V2_) - lg(L1, V1)
    r = sw - (np.bincount(mun, sw, nm) / nsec_m)[mun]
    se = np.sqrt(1 / (L1 + .5) + 1 / (V1 - L1 + .5) + 1 / (L2_ + .5) + 1 / (V2_ - L2_ + .5))
    z0 = r / se
    tr = T2_ / np.maximum(A2, 1) - turn1; r4 = tr - (np.bincount(mun, tr, nm) / nsec_m)[mun]
    swm = lg(np.bincount(mun, L2_, nm), np.bincount(mun, V2_, nm)) - base_logit1_m
    coef, *_ = np.linalg.lstsq(X_ols, swm, rcond=None); r3 = swm - X_ols @ coef
    return z0, r4, r3


def escala(x):
    return 1.4826 * np.median(np.abs(x - np.median(x)))


z0b, r4b, r3b = estat(L2, V2, T2)
S0, S4, S3 = escala(z0b), escala(r4b), escala(r3b)


def contagens(L2_, V2_, T2_):
    z0, r4, r3 = estat(L2_, V2_, T2_)
    z = z0 / S0; z4 = r4 / S4; z3 = r3 / S3
    out = {}
    for lim in (3, 4, 5):
        out[f"d1_pos_{lim}"] = (z > lim).astype(float); out[f"d1_neg_{lim}"] = (z < -lim).astype(float)
    zl = np.bincount(loc, z, nl) / np.sqrt(np.maximum(nsec_l, 1)); zl_ok = nsec_l >= 3
    out["d2l_pos"] = ((zl > 5) & zl_ok).astype(float); out["d2l_neg"] = ((zl < -5) & zl_ok).astype(float)
    zz = np.bincount(zon, z, nz) / np.sqrt(np.maximum(nsec_z, 1)); zz_ok = nsec_z >= 10
    out["d2z_pos"] = ((zz > 5) & zz_ok).astype(float); out["d2z_neg"] = ((zz < -5) & zz_ok).astype(float)
    out["d3_pos"] = (z3 > 4).astype(float); out["d3_neg"] = (z3 < -4).astype(float)
    out["d4_pos"] = (z4 > 4).astype(float)
    out["_esc_local"] = np.array([float(np.std(zl[zl_ok]))]); out["_esc_zona"] = np.array([float(np.std(zz[zz_ok]))])
    return out, z0


# unidades de cada contagem (para reponderar no bootstrap por município): seção, local, zona ou município
UNID = {"_es": ("x", np.zeros(1, int)), "d1": ("sec", mun), "d2l": ("loc", mun_of_loc), "d2z": ("zon", mun_of_zone), "d3": ("mun", np.arange(nm)), "d4": ("sec", mun)}


def det_valores(L2_, V2_, T2_):
    out, z0 = contagens(L2_, V2_, T2_)
    tot = {k: float(v.sum()) for k, v in out.items() if not k.startswith("_")}
    tot["esc_local"] = float(out["_esc_local"][0]); tot["esc_zona"] = float(out["_esc_zona"][0])
    dig = (L2_.astype(int) % 10); obs = np.bincount(dig, minlength=10); p = stats.chisquare(obs).pvalue
    tot["d5_p"] = float(p); tot["escala_z"] = float(escala(z0) / S0)
    return tot


# limiares: percentil 97,5 do bootstrap por município (B = 200, semente 11) da contagem na base real; 2ª amostra independente mede o falso alarme conjunto
def bootstrap(seed, B=200):
    rng = np.random.default_rng(seed); out, _ = contagens(L2, V2, T2); out = {k: v for k, v in out.items() if not k.startswith("_")}; mult = rng.multinomial(nm, np.ones(nm) / nm, size=B)
    # cada contagem é somada por município (pelo mapa da sua unidade) e multiplicada pela multiplicidade sorteada do município
    return {k: mult @ np.bincount(UNID[k.split("_")[0]][1], v, nm) for k, v in out.items()}


BS1, BS2 = bootstrap(11), bootstrap(12)
LIM = {k: float(np.percentile(v, 97.5)) for k, v in BS1.items()}
base_tot = det_valores(L2, V2, T2)
ESC_LOC0, ESC_ZON0 = base_tot["esc_local"], base_tot["esc_zona"]
DIRETO = {"pos": ["d1_pos_4", "d2l_pos", "d2z_pos", "d3_pos"], "neg": ["d1_neg_4", "d2l_neg", "d2z_neg", "d3_neg"]}
falso_alarme = {}
for lado, ks in DIRETO.items():
    ks2 = ks + (["d4_pos"] if lado == "pos" else [])
    falso_alarme[lado] = float(np.mean(np.any([BS2[k] > LIM[k] for k in ks2], axis=0)))
falso_alarme["qualquer_lado"] = float(np.mean(np.any([BS2[k] > LIM[k] for k in DIRETO["pos"] + DIRETO["neg"] + ["d4_pos"]], axis=0)))


# ---------------- mecanismos ----------------
def escolhe(mec, d, X, rng):
    """Devolve (indices_das_secoes, s0_nominal) da seleção; s é ajustado depois para totalizar X."""
    if mec in ("dispersa", "bn_conversao", "enchimento"):
        ordem = rng.permutation(N); s0 = .03
    elif mec == "poucas_secoes":
        ordem = rng.permutation(N); s0 = .40
    elif mec == "reduto_alvo":
        pool = np.where(p1 >= np.quantile(p1, .8))[0] if d == 1 else np.where(p1 <= np.quantile(p1, .2))[0]; ordem = rng.permutation(pool); s0 = .05
    elif mec == "reduto_oponente":
        pool = np.where(p1 <= np.quantile(p1, .2))[0] if d == 1 else np.where(p1 >= np.quantile(p1, .8))[0]; ordem = rng.permutation(pool); s0 = .05
    elif mec in ("locais", "zonas", "municipios", "ufs"):
        ids, k = {"locais": (loc, nl), "zonas": (zon, nz), "municipios": (mun, nm), "ufs": (uf, nu)}[mec]
        cand = np.arange(k) if mec != "municipios" else np.setdiff1d(np.arange(nm), big_mun)
        ordem_u = rng.permutation(cand); vu = np.bincount(ids, V2, k)[ordem_u]; cum = np.cumsum(.10 * vu)
        n_sel = min(len(ordem_u), int(np.searchsorted(cum, X)) + 1); sel = np.zeros(k, bool); sel[ordem_u[:n_sel]] = True
        return np.where(sel[ids])[0], .10
    elif mec == "cinco_grandes":
        return np.where(big)[0], None
    elif mec == "macrorregiao":
        return np.where(ne)[0], None
    elif mec == "uniforme":
        return np.arange(N), None
    elif mec == "lote_tardio":
        return np.where(recv > np.quantile(recv, .6))[0], None
    cum = np.cumsum(s0 * V2[ordem]); n_sel = min(len(ordem), int(np.searchsorted(cum, X)) + 1)
    return ordem[:n_sel], s0


def aplica(mec, d, X, rng):
    if mec == "uniforme_logit":
        base_l = lg(L2, V2); p0 = 1 / (1 + np.exp(-base_l)); lo, hi = 0.0, 4.0
        for _ in range(50):
            mid = (lo + hi) / 2; dl = np.abs(V2 * (1 / (1 + np.exp(-(base_l + d * mid))) - p0)).sum()
            lo, hi = (mid, hi) if dl < X else (lo, mid)
        c = (lo + hi) / 2; dL = V2 * (1 / (1 + np.exp(-(base_l + d * c))) - p0)
        x = np.floor(np.abs(dL) + rng.random(N)); Ln = np.clip(L2 + np.sign(dL) * x, 0, V2)
        return Ln, V2.copy(), T2.copy(), float(np.abs(Ln - L2).sum()), N
    sel, s0 = escolhe(mec, d, X, rng)
    if mec == "enchimento":
        disp = ABS2[sel]
    elif mec == "bn_conversao":
        disp = BN2[sel]
    else:
        disp = (F2 if d == 1 else L2)[sel]
    base = V2[sel]; s = X / max(base.sum(), 1)
    for _ in range(6):                                         # água: ajusta s para totalizar X respeitando a capacidade de cada seção
        x = np.minimum(s * base, disp); tot = x.sum()
        if tot >= X * .999 or tot <= 0 or s >= 1:
            break
        s *= X / tot
    x = np.floor(np.minimum(s * base, disp) + rng.random(len(sel)))        # arredondamento estocástico
    x = np.minimum(x, disp)
    L, V, T = L2.copy(), V2.copy(), T2.copy()
    if mec == "enchimento":                                     # voto novo para um finalista, vindo da abstenção: comparecimento sobe
        V[sel] += x; T[sel] += x
        if d == 1: L[sel] += x
    elif mec == "bn_conversao":                                 # branco/nulo vira voto válido de um finalista: comparecimento igual
        V[sel] += x
        if d == 1: L[sel] += x
    else:                                                       # troca de voto entre finalistas
        L[sel] += x if d == 1 else -x
    return L, V, T, float(x.sum()), len(sel)



MEC = ["dispersa", "poucas_secoes", "locais", "zonas", "municipios", "cinco_grandes", "ufs", "macrorregiao", "reduto_alvo", "reduto_oponente", "uniforme", "uniforme_logit", "lote_tardio", "enchimento", "bn_conversao"]
DET = {"dispersa", "poucas_secoes", "locais", "zonas", "municipios", "ufs", "reduto_alvo", "reduto_oponente", "enchimento", "bn_conversao"}   # aleatórios: réplicas


def roda(args):
    mec, d, X, rep = args
    rng = np.random.default_rng(int(hashlib.sha256(f"{ANO}|{mec}|{d}|{X}|{rep}".encode()).hexdigest()[:12], 16))
    L, V, T, movidos, nsel = aplica(mec, d, X, rng)
    t = det_valores(L, V, T)
    cor = "pos" if d == 1 else "neg"; op = "neg" if d == 1 else "pos"
    row = {"ano": ANO, "mecanismo": mec, "sentido": "Flavio→Lula" if d == 1 else "Lula→Flavio", "X": X, "rep": rep, "votos_movidos": movidos, "secoes": nsel,
           "d5_p": t["d5_p"], "escala_z": t["escala_z"]}
    for k in ("d1_pos_4", "d1_neg_4", "d2l_pos", "d2l_neg", "d2z_pos", "d2z_neg", "d3_pos", "d3_neg", "d4_pos", "d1_pos_3", "d1_neg_3", "d1_pos_5", "d1_neg_5"):
        row[k] = t[k] > LIM[k]
    row["alarme_correto"] = any(row[k] for k in DIRETO[cor]) or (mec == "enchimento" and row["d4_pos"])
    row["alarme_oposto"] = any(row[k] for k in DIRETO[op])
    row["d1_correto_lim3"] = row[f"d1_{cor}_3"]; row["d1_correto_lim5"] = row[f"d1_{cor}_5"]
    row["d5_alarme"] = t["d5_p"] < 1e-3
    return row


SE_B = np.sqrt(1 / (L1 + .5) + 1 / (V1 - L1 + .5) + 1 / (L2 + .5) + 1 / (V2 - L2 + .5))


AB = (0.0, 0.0)


def ajusta_ab():
    """Grade 7x7 de (a, b) em [0; 0,3] logit: iguala escala do z, de local e de zona à base real (uma realização por ponto, semente fixa)."""
    global AB
    melhor = (1e9, None)
    for a in np.linspace(0, .3, 7):
        for b_ in np.linspace(0, .3, 7):
            AB = (a, b_); r = fabrica("calibrada_estrutura", 10_000 + int(a * 100) * 10 + int(b_ * 100), parcial=True)
            custo = abs(np.log(r["escala_z"])) + abs(np.log(r["esc_local_rel"])) + abs(np.log(r["esc_zona_rel"]))
            if custo < melhor[0]: melhor = (custo, (float(a), float(b_)))
    AB = melhor[1]; return melhor


def fabrica(modo, rep, parcial=False):
    """B2: 2º turno inteiro fabricado por um modelo (virada municipal observada + ruído por seção + sorteio binomial), mantendo o resultado nacional.
    ingenua: só ruído binomial; calibrada: acrescenta a sobredispersão que a base real tem (o atacante 'aprendeu' com a eleição real)."""
    rng = np.random.default_rng(int(hashlib.sha256(f"{ANO}|fab|{modo}|{rep}".encode()).hexdigest()[:12], 16))
    swm = lg(np.bincount(mun, L2, nm), np.bincount(mun, V2, nm)) - base_logit1_m
    if modo == "ingenua":
        p = 1 / (1 + np.exp(-(lg(L1, V1) + swm[mun]))); L = rng.binomial(V2.astype(int), p).astype(float)
    elif modo == "calibrada":                                   # sem binomial; ruído com a escala da base real
        p = 1 / (1 + np.exp(-(lg(L1, V1) + swm[mun] + rng.normal(0, 1, N) * S0 * SE_B))); L = np.floor(V2 * p + rng.random(N))
    else:                                                       # calibrada_estrutura: acrescenta efeitos de zona e de local (a, b da emenda 3)
        a, b_ = AB
        e = np.sqrt(np.maximum((S0 * SE_B) ** 2 - a ** 2 - b_ ** 2, .05 * (S0 * SE_B) ** 2))
        p = 1 / (1 + np.exp(-(lg(L1, V1) + swm[mun] + rng.normal(0, b_, nz)[zon] + rng.normal(0, a, nl)[loc] + rng.normal(0, 1, N) * e))); L = np.floor(V2 * p + rng.random(N))
    t = det_valores(L, V2, T2)
    if parcial:
        return {"escala_z": t["escala_z"], "esc_local_rel": t["esc_local"] / ESC_LOC0, "esc_zona_rel": t["esc_zona"] / ESC_ZON0}
    row = {"ano": ANO, "cenario": "fabricada_" + modo, "rep": rep, "escala_z": t["escala_z"], "d5_p": t["d5_p"], "d5_alarme": t["d5_p"] < 1e-3,
           "margem_nacional": float(L.sum() - (V2.sum() - L.sum())), "margem_real": float(L2.sum() - F2.sum())}
    for k in ("d1_pos_4", "d1_neg_4", "d2l_pos", "d2l_neg", "d2z_pos", "d2z_neg", "d3_pos", "d3_neg", "d4_pos"):
        row[k] = t[k] > LIM[k]
    row["alarme_qualquer_lado"] = any(row[k] for k in ("d1_pos_4", "d1_neg_4", "d2l_pos", "d2l_neg", "d2z_pos", "d2z_neg", "d3_pos", "d3_neg", "d4_pos"))
    row["d6_subdispersao"] = bool(t["escala_z"] < .85 or t["escala_z"] > 1.15)       # D6 (emenda 1 ao protocolo, fixado antes de rodar)
    row["esc_local_rel"] = t["esc_local"] / ESC_LOC0; row["esc_zona_rel"] = t["esc_zona"] / ESC_ZON0
    row["d7_estrutura_local"] = bool(not (.8 <= row["esc_local_rel"] <= 1.25) or not (.8 <= row["esc_zona_rel"] <= 1.25))   # D7 (emenda 2)
    return row


if __name__ == "__main__":
    t0 = time.time()
    tarefas = [(m, d, X, r) for m in MEC for d in (1, -1) for X in XS for r in (range(REPS) if m in DET else [0])]
    with Pool(PROC) as p:
        rows = p.map(roda, tarefas, chunksize=20)
    df = pd.DataFrame(rows); df.to_parquet(f"{OP}/resultados/sim_{ANO}.parquet", index=False)
    ab = ajusta_ab()
    fab = pd.DataFrame([fabrica(m, r) for m in ("ingenua", "calibrada", "calibrada_estrutura") for r in range(REPS)]); fab.to_csv(f"{OP}/resultados/sim_{ANO}_fabricada.csv", index=False)
    g = df.groupby(["mecanismo", "sentido", "X"]).agg(poder=("alarme_correto", "mean"), oposto=("alarme_oposto", "mean"), d5=("d5_alarme", "mean"), n=("rep", "size"),
                                                        d1_lim3=("d1_correto_lim3", "mean"), d1_lim5=("d1_correto_lim5", "mean"), movidos=("votos_movidos", "mean"), secoes=("secoes", "mean")).reset_index()
    def menor(s):
        ok = s[s.poder >= .8]; return int(ok.X.min()) if len(ok) else None
    res = {"ano": ANO, "reps": REPS, "base": {"secoes": int(N), "municipios": int(nm), "locais": int(nl), "zonas": int(nz), "escalas_robustas": {"z_secao": S0, "turnout": S4, "municipio": S3}},
           "limiares_p97_5": LIM, "contagens_base": {k: v for k, v in base_tot.items()}, "falso_alarme_conjunto_2a_amostra_bootstrap": falso_alarme, "fabricante_estrutura_ab": {"custo": ab[0], "a_local": ab[1][0], "b_zona": ab[1][1]},
           "fabricada": fab.groupby("cenario").agg(escala_z_media=("escala_z", "mean"), alarme_d1_a_d4=("alarme_qualquer_lado", "mean"), d5=("d5_alarme", "mean"), d6=("d6_subdispersao", "mean"), d7=("d7_estrutura_local", "mean"), esc_local_rel=("esc_local_rel", "mean"), esc_zona_rel=("esc_zona_rel", "mean"), n=("rep", "size")).round(3).to_dict("index"),
           "menor_X_com_poder_80": {f"{m}|{s}": menor(g[(g.mecanismo == m) & (g.sentido == s)]) for m in MEC for s in ("Flavio→Lula", "Lula→Flavio")},
           "tempo_s": round(time.time() - t0)}
    json.dump(res, open(f"{OP}/resultados/sim_{ANO}_resumo.json", "w"), ensure_ascii=False, indent=1, default=str)
    g.to_csv(f"{OP}/resultados/sim_{ANO}_grade.csv", index=False)
    print(json.dumps({k: v for k, v in res.items() if k != "menor_X_com_poder_80"}, ensure_ascii=False, indent=1, default=str)[:2500])
    for k, v in res["menor_X_com_poder_80"].items(): print(k, v)
