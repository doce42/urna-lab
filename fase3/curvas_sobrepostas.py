"""Rodada 8 / T71: curvas acumuladas do 1º e do 2º turno "sobrepostas" (vídeo no Instagram). Ver fase3/PREREG_CURVAS_SOBREPOSTAS.md.
C1 reprodução, C2 conta do deslocamento visual, C3 ordem de chegada, C4 semelhança 2026 × 2022, C5 ordens independentes e contrafactual."""
import json, time
import numpy as np, pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; OUT = RAIZ + "/fase3/resultados/curvas_sobrepostas.json"
NPERM = 200; T0 = time.time(); rng = np.random.default_rng(20261030)
GRADE = np.arange(5, 101) / 100                    # 5% a 100% das urnas, passo de 1%
DESL_VIDEO = {"1": 4.00, "2": 5.25}                # p.p. mostrados no vídeo (1º turno: os dois sobem; 2º: Lula −, Flávio +)
REG = {"AC": "N", "AM": "N", "AP": "N", "PA": "N", "RO": "N", "RR": "N", "TO": "N", "AL": "NE", "BA": "NE", "CE": "NE", "MA": "NE",
       "PB": "NE", "PE": "NE", "PI": "NE", "RN": "NE", "SE": "NE", "DF": "CO", "GO": "CO", "MS": "CO", "MT": "CO", "ES": "SE", "MG": "SE",
       "RJ": "SE", "SP": "SE", "PR": "S", "RS": "S", "SC": "S", "ZZ": "ZZ"}


def base(ano):
    return pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")


def curva(L, A, V, ordem):
    """% acumulado de Lula e do adversário sobre os válidos, na ordem dada"""
    CV = np.cumsum(V[ordem]); return np.cumsum(L[ordem]) / CV * 100, np.cumsum(A[ordem]) / CV * 100


def na_grade(c):
    n = len(c); return c[(GRADE * n).astype(int).clip(1, n) - 1]


def dois(L, A):
    """% de Lula entre os dois (1º turno normalizado; no 2º turno é o próprio % de Lula)"""
    return L / (L + A) * 100


def semelhanca(c1, c2):
    a, b = c1 - c1.mean(), c2 - c2.mean()
    return {"pearson": float(np.corrcoef(a, b)[0, 1]), "rms_pp": float(np.sqrt(((a - b) ** 2).mean())), "desloc_otimo_pp": float(c2.mean() - c1.mean())}


def logit(p): return np.log(p / (1 - p))


def inv(z): return 1 / (1 + np.exp(-z))


R = {"teste": "T71", "pre_registro": "fase3/PREREG_CURVAS_SOBREPOSTAS.md", "nperm": NPERM, "anos": {}}
for ano in ("2026", "2022"):
    b = base(ano)
    out = {}
    # C1: curvas na ordem de recebimento, cada turno com as seções que têm boletim recebido
    for t in ("1", "2"):
        d = b[b[f"DT_BU_RECEBIDO_{t}"].notna() & (b[f"validos_{t}"] > 0)].sort_values(f"DT_BU_RECEBIDO_{t}")
        L, A, V = (d[f"v13_{t}"].to_numpy(float), d[f"v22_{t}"].to_numpy(float), d[f"validos_{t}"].to_numpy(float))
        cL, cA = curva(L, A, V, np.arange(len(d)))
        out[f"T{t}"] = {"secoes": int(len(d)), "lula_validos_final": float(cL[-1]), "adv_validos_final": float(cA[-1]),
                        "lula_dois_final": float(L.sum() / (L.sum() + A.sum()) * 100), "validos": int(V.sum()), "lula": int(L.sum()), "adv": int(A.sum()),
                        "curva_lula_validos_grade": [round(float(x), 3) for x in na_grade(cL)]}
        if ano == "2026":
            dl = DESL_VIDEO[t]
            out[f"T{t}"]["com_desloc_video"] = ({"lula": float(cL[-1] + dl), "adv": float(cA[-1] + dl)} if t == "1"
                                               else {"lula": float(cL[-1] - dl), "adv": float(cA[-1] + dl)})
    # C2: o deslocamento do vídeo em votos
    if ano == "2026":
        V2, m = out["T2"]["validos"], out["T2"]["lula"] - out["T2"]["adv"]
        out["C2"] = {"desloc_pp": 5.25, "votos_que_o_desloc_move_de_cada_lado": int(round(V2 * 0.0525)),
                     "virada_de_margem_votos": int(round(V2 * 0.105)), "margem_oficial": int(m),
                     "margem_com_desloc": int(round(m - V2 * 0.105))}

    # seções com boletim recebido nos dois turnos (C3 a C5)
    d = b[b["DT_BU_RECEBIDO_1"].notna() & b["DT_BU_RECEBIDO_2"].notna() & (b["validos_1"] > 0) & (b["validos_2"] > 0)].reset_index(drop=True)
    n = len(d)
    L1, A1, L2, A2 = (d[c].to_numpy(float) for c in ("v13_1", "v22_1", "v13_2", "v22_2"))
    V1d, V2d = L1 + A1, L2 + A2                       # dois candidatos nos dois turnos (o 1º turno "normalizado" do vídeo)
    o1 = np.argsort(d["DT_BU_RECEBIDO_1"].to_numpy(), kind="stable"); o2 = np.argsort(d["DT_BU_RECEBIDO_2"].to_numpy(), kind="stable")
    r1 = np.empty(n); r1[o1] = np.arange(n); r2 = np.empty(n); r2[o2] = np.arange(n)
    reg = d["SG_UF"].map(REG).fillna("ZZ")

    def eta2(rot, val):
        g = pd.Series(val).groupby(rot.to_numpy())
        return float(((g.transform("mean") - val.mean()) ** 2).sum() / ((val - val.mean()) ** 2).sum())
    from scipy.stats import spearmanr
    # C3: a ordem se repete entre turnos? depende da geografia? quanto a curva oscila sob ordem aleatória?
    faixa_aleat = {f: [] for f in (0.01, 0.05, 0.10)}
    for _ in range(NPERM):
        c, _a = curva(L2, A2, V2d, rng.permutation(n))
        for f in faixa_aleat: faixa_aleat[f].append(float(np.abs(c[int(f * n):] - c[-1]).max()))
    c2real, _ = curva(L2, A2, V2d, o2)
    out["C3"] = {"secoes_nos_dois_turnos": int(n), "spearman_ordem_1T_2T": float(spearmanr(r1, r2)[0]),
                 "eta2_UF_posicao_2T": eta2(d["SG_UF"], r2 / n), "eta2_regiao_posicao_2T": eta2(reg, r2 / n),
                 "eta2_UF_posicao_1T": eta2(d["SG_UF"], r1 / n),
                 "desvio_max_do_final_pp_real": {str(f): float(np.abs(c2real[int(f * n):] - c2real[-1]).max()) for f in faixa_aleat},
                 "desvio_max_do_final_pp_ordem_aleatoria_p95": {str(f): float(np.percentile(v, 95)) for f, v in faixa_aleat.items()},
                 "regiao_por_quintil_de_chegada_2T": pd.crosstab(pd.qcut(r2, 5, labels=False), reg.to_numpy(), normalize="index").round(3).to_dict(orient="index")}

    # C4: semelhança real (1º turno normalizado entre os dois × 2º turno, mesmas seções, cada um na sua ordem)
    c1real, _ = curva(L1, A1, V1d, o1)
    g1, g2 = na_grade(c1real), na_grade(c2real)
    out["C4"] = {**semelhanca(g1, g2), "curva_1T_dois_grade": [round(float(x), 3) for x in g1], "curva_2T_grade": [round(float(x), 3) for x in g2],
                 "final_1T_dois": float(c1real[-1]), "final_2T": float(c2real[-1])}

    # C5 (i): ordens independentes, os mesmos votos
    ps, rs = [], []
    for _ in range(NPERM):
        a, _a = curva(L1, A1, V1d, rng.permutation(n)); c, _c = curva(L2, A2, V2d, rng.permutation(n))
        s = semelhanca(na_grade(a), na_grade(c)); ps.append(s["pearson"]); rs.append(s["rms_pp"])
    out["C5_ordens_independentes"] = {"pearson_p05_p50_p95": [float(np.percentile(ps, q)) for q in (5, 50, 95)],
                                      "rms_p05_p50_p95": [float(np.percentile(rs, q)) for q in (5, 50, 95)],
                                      "fracao_pearson_maior_ou_igual_real": float(np.mean(np.array(ps) >= out["C4"]["pearson"]))}
    # C5 (ii): contrafactual estrutural: % do 1º turno da seção + virada nacional constante em logito, votos reais do 2º turno, ordem real do 2º turno
    p1 = (L1 + 0.5) / (V1d + 1)
    lo, hi = -3.0, 3.0
    for _ in range(60):                               # virada que reproduz o total de Lula no 2º turno
        k = (lo + hi) / 2
        if (inv(logit(p1) + k) * V2d).sum() > L2.sum(): hi = k
        else: lo = k
    prev = inv(logit(p1) + k) * V2d
    cprev, _ = curva(prev, V2d - prev, V2d, o2)
    dif = c2real - cprev; ini = int(0.05 * n)
    out["C5_contrafactual"] = {"virada_logito": float(k), "dist_max_pp_desde_5pct": float(np.abs(dif[ini:]).max()),
                               "rms_pp_grade": float(np.sqrt(((na_grade(c2real) - na_grade(cprev)) ** 2).mean())),
                               "pearson_prev_real_centradas": float(np.corrcoef(na_grade(cprev) - na_grade(cprev).mean(), g2 - g2.mean())[0, 1]),
                               "curva_prevista_grade": [round(float(x), 3) for x in na_grade(cprev)],
                               "corr_secao_1T_2T": float(np.corrcoef(L1 / V1d, L2 / V2d)[0, 1])}
    R["anos"][ano] = out
    print(ano, "ok", round(time.time() - T0), "s", flush=True)

a, b22 = R["anos"]["2026"], R["anos"]["2022"]
R["leitura"] = {"semelhanca_2026_maior_que_2022": a["C4"]["pearson"] > b22["C4"]["pearson"],
                "real_mais_longe_do_contrafactual_que_2022": a["C5_contrafactual"]["dist_max_pp_desde_5pct"] > b22["C5_contrafactual"]["dist_max_pp_desde_5pct"]}
R["leitura"]["incomum_pelo_criterio"] = R["leitura"]["semelhanca_2026_maior_que_2022"] and R["leitura"]["real_mais_longe_do_contrafactual_que_2022"]
R["segundos"] = round(time.time() - T0)
json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1)
print(json.dumps({ano: {k: v for k, v in R["anos"][ano].items() if k not in ("C4",)} | {"C4": {k: v for k, v in R["anos"][ano]["C4"].items() if "grade" not in k}}
                  for ano in R["anos"]}, ensure_ascii=False, indent=1, default=str)[:9000])
print(R["leitura"])
