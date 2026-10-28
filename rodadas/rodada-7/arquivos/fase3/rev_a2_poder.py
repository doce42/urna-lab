"""F3 em revisão / A2: o I1 com (1) regra de detecção no sentido correto, (2) E02 completo ao lado do simples e (3) troca no
município inteiro dos 5 municípios antes excluídos (M2G). Mesmos mundos, sementes e cenários do I1.
Ver fase3/PREREG_REVISAO.md (adendo A1/A2/A4).  Uso: rev_a2_poder.py [2026|2022]"""
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
# E02 "completo" do P9: + proporções dos eliminados no 1º turno, brancos+nulos, variação de comparecimento, log dos aptos do município
elim = [c for c in b.columns if c.startswith("v") and c.endswith("_1") and c not in ("v13_1", "v22_1", "validos_1")]
XC = np.nan_to_num(np.column_stack([X] + [b[c].fillna(0).values / V1 for c in elim] + [((b["branco_1"] + b["nulo_1"]) / b["total_1"]).values,
     (b["QT_COMPARECIMENTO_2"] / b["QT_APTOS_2"] - b["QT_COMPARECIMENTO_1"] / b["QT_APTOS_1"]).values, np.log(b.groupby("mun")["QT_APTOS_2"].transform("sum")).values]).astype(float))
PINVC = {u: (ix, np.linalg.pinv(XC[ix])) for u, ix in pd.Series(np.arange(N)).groupby(ufc).indices.items()}


def med_grupo(v, g):
    return pd.Series(v).groupby(g).transform("median").values


def e02(sw, sd, PI, MX):
    esp = np.empty(N)
    for ix, Pi in PI.values(): esp[ix] = MX[ix] @ (Pi @ sw[ix])
    zz = (sw - esp) / sd; zz = (zz - np.median(zz)) / (1.4826 * np.median(np.abs(zz - np.median(zz))))
    zl = zz[ok_loc]; sm = np.bincount(lcod, zl); mean = sm / kl; grand = zl.mean()
    ssb = (kl * (mean - grand) ** 2).sum(); sst = ((zl - mean[lcod]) ** 2).sum(); Nn = kl.sum()
    msb = ssb / (nl - 1); msw = sst / (Nn - nl); k0 = (Nn - (kl ** 2).sum() / Nn) / (nl - 1)
    rho = float(max(0, (msb - msw) / (msb + (k0 - 1) * msw)))
    zadj = mean * np.sqrt(kl) / np.sqrt(1 + (kl - 1) * rho); s = bh(2 * stats.norm.sf(np.abs(zadj)))
    return int((s & (zadj > 0)).sum()), int((s & (zadj < 0)).sum()), rho


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
    es = e02(sw, sd, PINV, X); ec = e02(sw, sd, PINVC, XC)
    v = np.array([t1p, t1n, t2, t3p, t3n, t4, es[0], es[1], ec[0], ec[1]], float); rho = es[2]
    return v, rho


NOMES = ["T1_pro", "T1_contra", "T2", "T3_pro", "T3_contra", "T4", "E02s_pro", "E02s_contra", "E02c_pro", "E02c_contra"]
real, rho_real = estatisticas(L2r)
print(ANO, "real", dict(zip(NOMES, real.round(3))), "rho", round(rho_real, 4), round(time.time() - T0), "s", flush=True)
mrg = lambda c: max(5, 5 * np.sqrt(c))
lim_real = np.array([real[0] + mrg(real[0]), real[1] + mrg(real[1]), real[2] * 3, real[3] + mrg(real[3]), real[4] + mrg(real[4]), 3.5,
                     *[real[i] + mrg(real[i]) for i in range(6, 10)]])
rng = np.random.default_rng(7100 + int(ANO) % 100)   # mesma semente e mesma ordem de sorteio do I1
mundo = lambda: rng.binomial(V2.astype(int), np.clip(L2r / V2, 0, 1)).astype(float)
cal = np.array([estatisticas(mundo())[0] for _ in range(NCAL)])
lim_cal = cal.max(0) + np.array([5, 5, .05, 5, 5, .5, 5, 5, 5, 5])
print("calibração", round(time.time() - T0), "s", flush=True)
# regras: "qualquer" = qualquer estatística, qualquer lado (regra do I1); "sentido_*" = lado certo de T1, T3 ou E02 (T2 e T4 não têm lado)
CONJ = {"qualquer_E02s": [0, 1, 2, 3, 4, 5, 6, 7], "qualquer_E02c": [0, 1, 2, 3, 4, 5, 8, 9]}
DIR = {"A": {"sentido_E02s": [0, 3, 6], "sentido_E02c": [0, 3, 8], "oposto_E02s": [1, 4, 7], "oposto_E02c": [1, 4, 9], "E02s_certo": [6], "E02c_certo": [8], "E02s_oposto": [7], "E02c_oposto": [9]},
       "B": {"sentido_E02s": [1, 4, 7], "sentido_E02c": [1, 4, 9], "oposto_E02s": [0, 3, 6], "oposto_E02c": [0, 3, 8], "E02s_certo": [7], "E02c_certo": [9], "E02s_oposto": [6], "E02c_oposto": [8]}}

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
GRANDES = [int(i) for i in np.argsort(-mun_tam)[:5]]   # os 5 maiores municípios (excluídos do M2 no I1)
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
    if mec.startswith("M2G_"):
        return mun == GRANDES[int(mec.split("_")[1])]
    if mec == "M3_regiao":
        sem = com_xy[rng.integers(len(com_xy))]; d = np.hypot(*(mun_xy[com_xy] - mun_xy[sem]).T); ordem = com_xy[np.argsort(d)]
        esc = ordem[: np.searchsorted(np.cumsum(mun_tam[ordem]), alvo) + 1]
        return np.isin(mun, esc)


R = {"ano": ANO, "secoes": N, "grandes_municipios": {mun_nomes[g]: int(mun_tam[g]) for g in GRANDES}, "alvo_secoes": alvo, "rho_real": rho_real, "real": dict(zip(NOMES, real.tolist())),
     "limiar_ancorado_no_real": dict(zip(NOMES, lim_real.tolist())), "limiar_calibrado": dict(zip(NOMES, lim_cal.tolist())), "mundos_calibracao": NCAL, "mundos_avaliacao": NAVAL}
mundos = [mundo() for _ in range(NAVAL)]
nulo = np.array([estatisticas(Lw)[0] for Lw in mundos])
R["falso_alarme"] = {rn: {c: (lambda k: {"taxa": k / NAVAL, "ic95": wil(k, NAVAL)})(int(sum((v[ix] > lim[ix]).any() for v in nulo))) for c, ix in CONJ.items()}
                     for rn, lim in (("ancorado_no_real", lim_real), ("calibrado", lim_cal))}
R["falso_alarme_por_teste_calibrado"] = dict(zip(NOMES, (nulo > lim_cal).mean(0).round(3).tolist()))
R["falso_alarme_sentido"] = {sen: {rn: {c: (lambda k: {"taxa": k / NAVAL, "ic95": wil(k, NAVAL)})(int(sum((v[ix] > lim[ix]).any() for v in nulo))) for c, ix in DIR[sen].items() if c.startswith("sentido")}
                                   for rn, lim in (("ancorado_no_real", lim_real), ("calibrado", lim_cal))} for sen in "AB"}
print("nulo", R["falso_alarme"], round(time.time() - T0), "s", flush=True)
R["resultados"] = {}
MEC = {m: [mascara(m) for _ in range(NAVAL)] for m in ("M0_disperso", "M1_locais", "M2_municipios", "M3_regiao")}   # mesma ordem do I1
MEC["M2G_grandes"] = [mascara(f"M2G_{i % 5}") for i in range(NAVAL)]
for mec, masks in MEC.items():
    for m in MAGS:
        for sentido in ("A_adv_para_Lula", "B_Lula_para_adv"):
            res = []; votos = []; nsec = []
            for Lw, sel in zip(mundos, masks):
                F = V2 - Lw
                mov = np.minimum(np.round(V2 * m), F if sentido[0] == "A" else Lw) * sel
                res.append(estatisticas(Lw + mov if sentido[0] == "A" else Lw - mov)[0]); votos.append(mov.sum()); nsec.append(sel.sum())
            res = np.array(res); chave = f"{mec}|{int(m * 100)}pct|{sentido}"; sen = sentido[0]
            d = {"votos_movidos_media": float(np.mean(votos)), "secoes_afetadas_media": float(np.mean(nsec))}
            for rn, lim in (("ancorado_no_real", lim_real), ("calibrado", lim_cal)):
                d[rn] = {c: (lambda k: {"taxa": k / NAVAL, "ic95": wil(k, NAVAL)})(int(sum((v[ix] > lim[ix]).any() for v in res))) for c, ix in CONJ.items()}
            d["por_teste_calibrado"] = dict(zip(NOMES, (res > lim_cal).mean(0).round(3).tolist()))
            for rn, lim in (("ancorado_no_real", lim_real), ("calibrado", lim_cal)):
                d[rn].update({c: (lambda k: {"taxa": k / NAVAL, "ic95": wil(k, NAVAL)})(int(sum((v[ix] > lim[ix]).any() for v in res))) for c, ix in DIR[sen].items()})
            if mec == "M2G_grandes":
                d["por_cidade_sentido_E02c_calibrado"] = {mun_nomes[GRANDES[c]]: float(np.mean([(res[i][DIR[sen]["sentido_E02c"]] > lim_cal[DIR[sen]["sentido_E02c"]]).any() for i in range(NAVAL) if i % 5 == c])) for c in range(5)}
                d["votos_por_cidade"] = {mun_nomes[GRANDES[c]]: float(np.mean([votos[i] for i in range(NAVAL) if i % 5 == c])) for c in range(5)}
            R["resultados"][chave] = d
            print(chave, int(d["votos_movidos_media"]), {c: round(d["calibrado"][c]["taxa"], 2) for c in ("qualquer_E02s", "sentido_E02s", "sentido_E02c", "E02s_oposto", "E02c_oposto")}, round(time.time() - T0), "s", flush=True)
R["tempo_s"] = round(time.time() - T0, 1)
json.dump(R, open(f"{OUT}/rev_a2_{ANO}.json", "w"), indent=1, ensure_ascii=False)
