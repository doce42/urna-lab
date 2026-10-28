"""F3 em revisão / I1: poder da bateria (T02, regra do T13, E02 corrigido) contra trocas de votos concentradas em locais,
municípios e regiões, nos dois sentidos. Ver fase3/PREREG_REVISAO.md.  Uso: rev_i1_poder.py [2026|2022]"""
import json, sys, time
import numpy as np, pandas as pd
from scipy import stats

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; OUT = RAIZ + "/fase3/resultados"
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"
NCAL, NAVAL, MAGS = 20, 30, (0.02, 0.05, 0.10)
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
inv = lambda z: 1 / (1 + np.exp(-z))
T0 = time.time()


def wil(k, n):
    z_ = 1.96; ph = k / n; den = 1 + z_ * z_ / n; c = (ph + z_ * z_ / (2 * n)) / den; h = z_ * np.sqrt(ph * (1 - ph) / n + z_ * z_ / (4 * n * n)) / den
    return [float(max(0, c - h)), float(min(1, c + h))]


def bh(p, q=0.05):
    n = len(p); o = np.argsort(p); passa = p[o] <= q * np.arange(1, n + 1) / n
    k = np.max(np.where(passa)[0]) + 1 if passa.any() else 0
    s = np.zeros(n, bool); s[o[:k]] = True; return s


b = pd.read_parquet(f"{AN}/base.parquet" if ANO == "2026" else f"{AN}/base_{ANO}.parquet")
b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20) & (b["SG_UF"] != "ZZ")].copy()
b = b.sort_values("DT_BU_RECEBIDO_2").reset_index(drop=True)
b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"].astype(str)
b["local"] = b["mun"] + "-" + b["NR_ZONA"].astype(str) + "-" + b["NR_LOCAL_VOTACAO_2"].astype(str)
N = len(b)
L1, V1 = b["v13_1"].values.astype(float), b["validos_1"].values.astype(float); A1 = b["v22_1"].values.astype(float)
ORF = 1 - (L1 + A1) / V1; P1 = L1 / V1
L2r, V2 = b["v13_2"].values.astype(float), b["validos_2"].values.astype(float)
mun = pd.factorize(b["mun"])[0]; nmun = mun.max() + 1
ufc, ufs = pd.factorize(b["SG_UF"]); nuf = len(ufs)
minuto = pd.factorize(b["DT_BU_RECEBIDO_2"].dt.floor("1min"))[0]   # já em ordem cronológica
comp, aptos = b["QT_COMPARECIMENTO_2"].values.astype(float), b["QT_APTOS_2"].values.astype(float)
loc = pd.factorize(b["local"])[0]; nloc = loc.max() + 1
tam_loc = np.bincount(loc, minlength=nloc); ok_loc = tam_loc[loc] >= 3          # E02: locais com 3 ou mais seções
lsel = loc[ok_loc]; lcod, lun = pd.factorize(lsel); nl = len(lun); kl = np.bincount(lcod).astype(float)
# E02 "simples" do P9: virada esperada por regressão dentro da UF em (1, p1, p1², órfão); pseudo-inversas pré-calculadas
X = np.column_stack([np.ones(N), P1, P1 ** 2, ORF]); PINV = {u: (ix, np.linalg.pinv(X[ix])) for u, ix in pd.Series(np.arange(N)).groupby(ufc).indices.items()}


def med_grupo(v, g):
    return pd.Series(v).groupby(g).transform("median").values


def estatisticas(L2, rho_fixo=None):
    sw = lg(L2, V2) - lg(L1, V1)
    sd = np.sqrt(1 / (L1 + .5) + 1 / (V1 - L1 + .5) + 1 / (L2 + .5) + 1 / (V2 - L2 + .5))
    # T02 / T1: z robusto contra a mediana municipal
    z = (sw - med_grupo(sw, mun)) / sd; zr = z / (1.4826 * np.median(np.abs(z - np.median(z))))
    t1p, t1n = int((zr > 5).sum()), int((zr < -5).sum())
    # T2: maior desvio (pp) da curva acumulada por minuto contra a previsão pela mediana da UF
    prev = inv(lg(L1, V1) + med_grupo(sw, ufc)) * V2
    cL, cP, cV = (np.cumsum(np.bincount(minuto, w)) for w in (L2, prev, V2)); t2 = float(100 * np.abs((cL - cP) / cV).max())
    # T3: seções com comparecimento ≥ 95% e ≥ 90% dos válidos para um finalista
    F2 = V2 - L2; t3p = int(((comp / aptos >= .95) & (L2 / V2 >= .9)).sum()); t3n = int(((comp / aptos >= .95) & (F2 / V2 >= .9)).sum())
    # T4: UF atípica na regressão das medianas estaduais
    e = pd.DataFrame({"g": ufc, "sw": sw, "p1": P1, "o": ORF}).groupby("g").median()
    Xe = np.column_stack([np.ones(len(e)), e.p1, e.p1 ** 2, e.o]); r = e.sw - Xe @ np.linalg.lstsq(Xe, e.sw, rcond=None)[0]
    t4 = float(np.abs((r - r.median()) / (1.4826 * np.median(np.abs(r - r.median())))).max())
    # E02 corrigido: z por seção contra a regressão da UF, média por local, correção por rho intralocal, BH
    esp = np.empty(N)
    for ix, Pi in PINV.values(): esp[ix] = X[ix] @ (Pi @ sw[ix])
    zz = (sw - esp) / sd; zz = (zz - np.median(zz)) / (1.4826 * np.median(np.abs(zz - np.median(zz))))
    zl = zz[ok_loc]; sm = np.bincount(lcod, zl); mean = sm / kl; grand = zl.mean()
    ssb = (kl * (mean - grand) ** 2).sum(); sst = ((zl - mean[lcod]) ** 2).sum(); Nn = kl.sum()
    msb = ssb / (nl - 1); msw = sst / (Nn - nl); k0 = (Nn - (kl ** 2).sum() / Nn) / (nl - 1)
    rho = float(max(0, (msb - msw) / (msb + (k0 - 1) * msw)))
    zg = mean * np.sqrt(kl); out = {}
    for nome, rr in (("E02", rho), ("E02_rho_fixo", rho if rho_fixo is None else rho_fixo)):
        zadj = zg / np.sqrt(1 + (kl - 1) * rr); s = bh(2 * stats.norm.sf(np.abs(zadj)))
        out[nome] = (int((s & (zadj > 0)).sum()), int((s & (zadj < 0)).sum()))
    v = np.array([t1p, t1n, t2, t3p, t3n, t4, *out["E02"], *out["E02_rho_fixo"]], float)
    return v, rho


NOMES = ["T1_pro", "T1_contra", "T2", "T3_pro", "T3_contra", "T4", "E02_pro", "E02_contra", "E02rf_pro", "E02rf_contra"]
real, rho_real = estatisticas(L2r)
real, _ = estatisticas(L2r, rho_real)
print(ANO, "real", dict(zip(NOMES, real.round(3))), "rho", round(rho_real, 4), round(time.time() - T0), "s", flush=True)
mrg = lambda c: max(5, 5 * np.sqrt(c))
lim_real = np.array([real[0] + mrg(real[0]), real[1] + mrg(real[1]), real[2] * 3, real[3] + mrg(real[3]), real[4] + mrg(real[4]), 3.5,
                     *[real[i] + mrg(real[i]) for i in range(6, 10)]])
rng = np.random.default_rng(7100 + int(ANO) % 100)
mundo = lambda: rng.binomial(V2.astype(int), np.clip(L2r / V2, 0, 1)).astype(float)
cal = np.array([estatisticas(mundo(), rho_real)[0] for _ in range(NCAL)])
lim_cal = cal.max(0) + np.array([5, 5, .05, 5, 5, .5, 5, 5, 5, 5])
print("calibração", round(time.time() - T0), "s", flush=True)
CONJ = {"T13": [0, 1, 2, 3, 4, 5], "E02": [6, 7], "bateria": [0, 1, 2, 3, 4, 5, 6, 7]}

# mecanismos: máscaras de ~1% das seções
alvo = int(round(0.01 * N))
mun_tam = np.bincount(mun, minlength=nmun)
geo = json.load(open(RAIZ + "/grafico/relatorio-app/dist/dados/geo.json")); tse = json.load(open(RAIZ + "/grafico/web/geo/tse_municipios_2026.json"))
ibge = {}
for ab in tse["abr"]:
    for m in ab["mu"]:
        if str(m["cdi"]).strip().isdigit(): ibge[ab["cd"].upper() + str(int(m["cd"]))] = int(m["cdi"])
sc, tr = geo["transform"]["scale"], geo["transform"]["translate"]; arcos = geo["arcs"]


def colhe(a, acc):
    for x in a:
        if isinstance(x, list): colhe(x, acc)
        else: acc.add(x if x >= 0 else ~x)


cent = {}
for g in geo["objects"]["municipios"]["geometries"]:
    s = set(); colhe(g["arcs"], s)
    q = np.concatenate([np.cumsum(np.array(arcos[a]), axis=0) for a in s]); cent[int(g["id"])] = q.mean(0) * sc + tr
mun_nomes = pd.factorize(b["mun"])[1]
mun_xy = np.array([cent.get(ibge.get(m, -1), [np.nan, np.nan]) for m in mun_nomes], float); com_xy = np.where(~np.isnan(mun_xy[:, 0]))[0]


def mascara(mec):
    if mec == "M0_disperso":
        return rng.random(N) < 0.01
    if mec == "M1_locais":
        ordem = rng.permutation(nloc); tam = np.bincount(loc, minlength=nloc)[ordem]; esc = ordem[: np.searchsorted(np.cumsum(tam), alvo) + 1]
        return np.isin(loc, esc)
    if mec == "M2_municipios":   # municípios maiores que o alvo não cabem e são pulados (SP capital, por exemplo)
        ordem = rng.permutation(nmun); ordem = ordem[mun_tam[ordem] <= alvo]; esc = ordem[: np.searchsorted(np.cumsum(mun_tam[ordem]), alvo) + 1]
        return np.isin(mun, esc)
    if mec == "M3_regiao":
        sem = com_xy[rng.integers(len(com_xy))]; d = np.hypot(*(mun_xy[com_xy] - mun_xy[sem]).T); ordem = com_xy[np.argsort(d)]
        esc = ordem[: np.searchsorted(np.cumsum(mun_tam[ordem]), alvo) + 1]
        return np.isin(mun, esc)


R = {"ano": ANO, "secoes": N, "alvo_secoes": alvo, "rho_real": rho_real, "real": dict(zip(NOMES, real.tolist())),
     "limiar_ancorado_no_real": dict(zip(NOMES, lim_real.tolist())), "limiar_calibrado": dict(zip(NOMES, lim_cal.tolist())), "mundos_calibracao": NCAL, "mundos_avaliacao": NAVAL}
mundos = [mundo() for _ in range(NAVAL)]
nulo = np.array([estatisticas(Lw, rho_real)[0] for Lw in mundos])
R["falso_alarme"] = {rn: {c: (lambda k: {"taxa": k / NAVAL, "ic95": wil(k, NAVAL)})(int(sum((v[ix] > lim[ix]).any() for v in nulo))) for c, ix in CONJ.items()}
                     for rn, lim in (("ancorado_no_real", lim_real), ("calibrado", lim_cal))}
R["falso_alarme_por_teste_calibrado"] = dict(zip(NOMES, (nulo > lim_cal).mean(0).round(3).tolist()))
print("nulo", R["falso_alarme"], round(time.time() - T0), "s", flush=True)
R["resultados"] = {}
for mec in ("M0_disperso", "M1_locais", "M2_municipios", "M3_regiao"):
    masks = [mascara(mec) for _ in range(NAVAL)]
    for m in MAGS:
        for sentido in ("A_adv_para_Lula", "B_Lula_para_adv"):
            res = []; votos = []; nsec = []
            for Lw, sel in zip(mundos, masks):
                F = V2 - Lw
                mov = np.minimum(np.round(V2 * m), F if sentido[0] == "A" else Lw) * sel
                res.append(estatisticas(Lw + mov if sentido[0] == "A" else Lw - mov, rho_real)[0]); votos.append(mov.sum()); nsec.append(sel.sum())
            res = np.array(res); chave = f"{mec}|{int(m * 100)}pct|{sentido}"
            d = {"votos_movidos_media": float(np.mean(votos)), "secoes_afetadas_media": float(np.mean(nsec))}
            for rn, lim in (("ancorado_no_real", lim_real), ("calibrado", lim_cal)):
                d[rn] = {c: (lambda k: {"taxa": k / NAVAL, "ic95": wil(k, NAVAL)})(int(sum((v[ix] > lim[ix]).any() for v in res))) for c, ix in CONJ.items()}
            d["por_teste_calibrado"] = dict(zip(NOMES, (res > lim_cal).mean(0).round(3).tolist()))
            d["E02_rho_reestimado_vs_fixo_calibrado"] = [float((res[:, 6:8] > lim_cal[6:8]).any(1).mean()), float((res[:, 8:10] > lim_cal[8:10]).any(1).mean())]
            R["resultados"][chave] = d
            print(chave, int(d["votos_movidos_media"]), {c: d["calibrado"][c]["taxa"] for c in CONJ}, "real:", {c: d["ancorado_no_real"][c]["taxa"] for c in CONJ}, round(time.time() - T0), "s", flush=True)
R["tempo_s"] = round(time.time() - T0, 1)
json.dump(R, open(f"{OUT}/rev_i1_{ANO}.json", "w"), indent=1, ensure_ascii=False)
