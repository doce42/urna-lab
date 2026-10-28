"""F3 em revisão / I2: seções com zero votos para um finalista, com beta-binomial calibrada (ρ ajustado sem a célula zero),
controles preditivos e intervalos. Ver fase3/PREREG_REVISAO.md."""
import json, time
import numpy as np, pandas as pd
from scipy import optimize, special, stats

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; OUT = RAIZ + "/fase3/resultados"
T0 = time.time(); PESO = 50.0; NSIM, NBOOT = 4000, 1000
rng = np.random.default_rng(7200)


def carrega(ano):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
    b = b[(b["SG_UF"] != "ZZ") & (b["validos_1"].fillna(0) > 0) & (b["validos_2"].fillna(0) > 0)].reset_index(drop=True)
    b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"].astype(str); b["zona"] = b["mun"] + "-" + b["NR_ZONA"].astype(str)
    return b


def loo(y, n, g):
    gy = pd.Series(y).groupby(g).transform("sum").values - y; gn = pd.Series(n).groupby(g).transform("sum").values - n
    return gy, gn


def media_prior(b, y, n, t, nivel):
    """média μ da seção: proporção do candidato nas outras seções do local (ou da zona), encolhida para o município"""
    ym, nm = loo(y, n, b["mun"].values)
    uf = pd.Series(y).groupby(b["SG_UF"].values).transform("sum").values / pd.Series(n).groupby(b["SG_UF"].values).transform("sum").values
    mu_m = np.where(nm > 0, ym / np.maximum(nm, 1), uf)
    yz, nz = loo(y, n, b["zona"].values)
    if nivel == "local":
        yl, nl = loo(y, n, (b["zona"] + "-" + b[f"NR_LOCAL_VOTACAO_{t}"].astype(str)).values)
        yp, np_ = np.where(nl > 0, yl, np.where(nz > 0, yz, ym)), np.where(nl > 0, nl, np.where(nz > 0, nz, nm))
    else:
        yp, np_ = np.where(nz > 0, yz, ym), np.where(nz > 0, nz, nm)
    return np.clip((yp + PESO * mu_m) / (np_ + PESO), 1e-6, 1 - 1e-6)


def p0(mu, n, rho):
    s = 1 / rho - 1; a, bb = mu * s, (1 - mu) * s
    return np.exp(special.betaln(a, bb + n) - special.betaln(a, bb))


def ajusta_rho(y, n, mu):
    """máxima verossimilhança da beta-binomial truncada em zero (só seções com y ≥ 1)"""
    k = y >= 1; y, n, mu = y[k], n[k], mu[k]
    def nll(lr):
        rho = np.exp(lr); s = 1 / rho - 1; a, bb = mu * s, (1 - mu) * s
        return -(stats.betabinom.logpmf(y, n, a, bb) - np.log1p(-p0(mu, n, rho))).sum()
    r = optimize.minimize_scalar(nll, bounds=(np.log(1e-5), np.log(0.5)), method="bounded", options={"xatol": 1e-3})
    return float(np.exp(r.x))


def intervalo(p):
    """intervalo de predição de 95% para a soma de Bernoulli(p): simulação exata se o esperado é pequeno, normal caso contrário"""
    m, v = p.sum(), (p * (1 - p)).sum()
    if m > 50: return [float(m - 1.96 * np.sqrt(v)), float(m + 1.96 * np.sqrt(v))]
    q = p[p > 1e-7]; s = (rng.random((NSIM, len(q))) < q).sum(1) if len(q) else np.zeros(NSIM)
    return [float(np.percentile(s, 2.5)), float(np.percentile(s, 97.5))]


def celula(b, col, t, nivel):
    y = b[col].fillna(0).values.astype(float); n = b[f"validos_{t}"].values.astype(float)
    mu = media_prior(b, y, n, t, nivel); rho = ajusta_rho(y, n, mu); p = p0(mu, n, rho); obs = (y == 0)
    esp = float(p.sum()); pi = intervalo(p)
    om = pd.Series(obs.astype(float)).groupby(b["mun"].values).sum().values; em = pd.Series(p).groupby(b["mun"].values).sum().values
    ix = rng.integers(0, len(om), (NBOOT, len(om))); rb = om[ix].sum(1) / np.maximum(em[ix].sum(1), 1e-9)
    # calibração interna: seções com 1 e 2 votos (parte do ajuste) e de 3 a 5 votos
    pk = lambda k: stats.betabinom.pmf(k, n, mu * (1 / rho - 1), (1 - mu) * (1 / rho - 1))
    cal = {f"{k}": {"observado": int((y == k).sum()), "esperado": float(pk(k).sum())} for k in (1, 2)}
    cal["3a5"] = {"observado": int(((y >= 3) & (y <= 5)).sum()), "esperado": float(sum(pk(k).sum() for k in (3, 4, 5)))}
    return {"rho": rho, "observado": int(obs.sum()), "esperado": esp, "ic_predicao_95": pi, "dentro_do_ic": bool(pi[0] <= obs.sum() <= pi[1]),
            "razao": float(obs.sum() / esp) if esp > 0 else None, "ic95_razao_bootstrap_mun": [float(np.percentile(rb, 2.5)), float(np.percentile(rb, 97.5))],
            "votos_esperados_nas_secoes_zero": float((mu * n)[obs].sum()), "caudas": cal}, rb


CEL = {"2026": {"alvo": [("Flávio", "v22", 1), ("Flávio", "v22", 2)], "controle": [("Lula", "v13", 1), ("Lula", "v13", 2), ("cand. 70", "v70", 1), ("cand. 14", "v14", 1)]},
       "2022": {"alvo": [("Bolsonaro", "v22", 1), ("Bolsonaro", "v22", 2)], "controle": [("Lula", "v13", 1), ("Lula", "v13", 2), ("Tebet", "v15", 1), ("Ciro", "v12", 1)]}}
R = {"pre_registro": "fase3/PREREG_REVISAO.md (I2)", "peso_encolhimento": PESO}
for nivel in ("local", "zona"):          # zona = sensibilidade
    Rn = {}; boots = {}
    for ano in ("2026", "2022"):
        b = carrega(ano); Ra = {"controles": {}, "alvos": {}}
        for tipo in ("controle", "alvo"):
            for nome, c, t in CEL[ano][tipo]:
                r, rb = celula(b, f"{c}_{t}", t, nivel); Ra["controles" if tipo == "controle" else "alvos"][f"{nome} {t}T"] = r; boots[(ano, t, tipo, nome)] = rb
                print(nivel, ano, nome, t, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k not in ("caudas",)}, round(time.time() - T0), "s", flush=True)
        ctrl = [v for v in Ra["controles"].values() if v["esperado"] >= 5]
        Ra["calibrado"] = bool(ctrl) and all(v["dentro_do_ic"] for v in ctrl)
        Ra["controles_com_esperado_ao_menos_5"] = len(ctrl)
        for k, v in Ra["alvos"].items():
            if not Ra["calibrado"]: v["leitura"] = "não interpretável (modelo não calibrado nos controles)"
            elif v["observado"] > v["ic_predicao_95"][1] and v["ic95_razao_bootstrap_mun"][0] > 1: v["leitura"] = "excesso"
            elif v["ic95_razao_bootstrap_mun"][1] < 1.5: v["leitura"] = "excesso, se existir, menor que 50%"
            else: v["leitura"] = "inconclusivo"
        Rn[ano] = Ra
    Rn["comparacao_2026_vs_2022"] = {f"{t}T": {"razao_das_razoes_mediana": float(np.median(boots[("2026", t, "alvo", "Flávio")] / boots[("2022", t, "alvo", "Bolsonaro")])),
                                               "ic95": [float(np.percentile(boots[("2026", t, "alvo", "Flávio")] / boots[("2022", t, "alvo", "Bolsonaro")], q)) for q in (2.5, 97.5)]} for t in (1, 2)}
    R["principal_prior_local" if nivel == "local" else "sensibilidade_prior_zona"] = Rn
R["tempo_s"] = round(time.time() - T0, 1)
json.dump(R, open(f"{OUT}/rev_i2.json", "w"), indent=1, ensure_ascii=False)
