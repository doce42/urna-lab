"""F3 / auditoria adversarial, casos B e C (fase3/PREREG_ADVERSARIAL.md): as seções cujas anomalias foram explicadas por
registros do próprio sistema (T36: contas de integridade; T34/T16/T30: contingências de urna) votam de forma deslocada em relação
ao resto da UF? z robusto da virada do T02; permutação estratificada por UF, 10.000 sorteios.
Saída: fase3/resultados/adv_casos.json."""
import glob, json
import numpy as np, pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; NPERM = 10000
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
K = lambda uf, m, z, s: f"{str(uf).upper()}/{int(m)}/{int(z)}/{int(s)}"


def base(ano):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet")
    b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20)].copy(); b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"].astype(str)
    x1, n1, x2, n2 = b["v13_1"], b["validos_1"], b["v13_2"], b["validos_2"]
    sw = lg(x2, n2) - lg(x1, n1); res = sw - sw.groupby(b["mun"]).transform("median")
    z = res / np.sqrt(1/(x1+.5) + 1/(n1-x1+.5) + 1/(x2+.5) + 1/(n2-x2+.5)); b["z"] = z / (1.4826 * (z - z.median()).abs().median())
    b["k"] = [K(*r) for r in zip(b.SG_UF, b.CD_MUNICIPIO, b.NR_ZONA, b.NR_SECAO)]
    return b.reset_index(drop=True)


def teste(b, chaves, limiar, seed):
    s = b.k.isin(chaves).values; n = int(s.sum())
    if n == 0: return {"secoes_no_universo": 0}
    z = b.z.values; uf = b.SG_UF.values; obs_m = float(z[s].mean()); obs_t = float((np.abs(z[s]) > 3).mean())
    rng = np.random.default_rng(seed); sims_m = np.zeros(NPERM); sims_t = np.zeros(NPERM)
    for u in np.unique(uf[s]):
        pool = z[uf == u]; k = int((s & (uf == u)).sum())
        amostra = pool[rng.integers(0, len(pool), (NPERM, k))]
        sims_m += amostra.sum(1); sims_t += (np.abs(amostra) > 3).sum(1)
    sims_m /= n; sims_t /= n
    esp_m = float(sims_m.mean()); p_m = float(min(1, 2 * min((1 + (sims_m >= obs_m).sum()) / (NPERM + 1), (1 + (sims_m <= obs_m).sum()) / (NPERM + 1))))
    p_t = float((1 + (sims_t >= obs_t).sum()) / (NPERM + 1))
    dif = obs_m - esp_m
    leitura = "deslocamento" if (p_m < 0.01 and abs(dif) >= limiar) else ("sem deslocamento detectável" if p_m >= 0.01 else "diferença estatística abaixo do limiar de relevância")
    return {"secoes_no_universo": n, "media_z": obs_m, "media_z_esperada_mesma_UF": esp_m, "diferenca": dif, "ic95_nulo_da_media": [float(np.percentile(sims_m, 2.5)), float(np.percentile(sims_m, 97.5))],
            "p_bilateral_media": p_m, "fracao_abs_z_maior_3": obs_t, "fracao_esperada": float(sims_t.mean()), "p_excesso_cauda": p_t, "pro_lula_z_maior_3": int((z[s] > 3).sum()), "pro_adv_z_menor_menos_3": int((z[s] < -3).sum()),
            "leitura": leitura, "limiar": limiar}


R = {"pre_registro": "fase3/PREREG_ADVERSARIAL.md", "nperm": NPERM}
b26 = base("2026"); b22 = base("2022")
# Caso B: casos do T36 (contas de integridade), 1º turno (principal) e 2º turno (validação), 2026
for t in (1, 2):
    d = json.load(open(f"{AN}/resultado_casos_integridade_{t}t.json")); casos = d["casos_lista"]
    ch = {K(c["uf"], c["municipio"], c["zona"], c["secao"]) for c in casos}
    grupos = {"todos": ch}
    for g in ("declarado_oficialmente", "compativel", "inferido", "sem_explicacao"):
        grupos[g] = {K(c["uf"], c["municipio"], c["zona"], c["secao"]) for c in casos if c.get("grau") == g}
    R[f"caso_B_T36_{t}T_2026"] = {g: teste(b26, c, 0.3, 9500 + t) for g, c in grupos.items()} | {"casos_listados": len(casos)}
    print("B", t, {g: (v.get("secoes_no_universo"), round(v.get("diferenca", 0), 3), v.get("p_bilateral_media"), v.get("leitura")) for g, v in R[f"caso_B_T36_{t}T_2026"].items() if isinstance(v, dict)}, flush=True)
# Caso C: contingências de urna (2º turno), 2026 principal, 2022 validação
for ano, b, pas in (("2026", b26, "2t"), ("2022", b22, "2022_2t")):
    u = pd.concat([pd.read_parquet(f) for f in glob.glob(f"{AN}/brutos/{pas}/urnas_*.parquet")], ignore_index=True)
    u["k"] = [K(*r) for r in zip(u.SG_UF, u.CD_MUNICIPIO, u.NR_ZONA, u.NR_SECAO)]
    duas = u.get("urnas_com_voto_no_log", pd.Series(np.nan, index=u.index)).fillna(0) >= 2
    cert = (u.get("cert_urna").notna() & (u.get("cert_igual_log") == False)) if "cert_igual_log" in u else pd.Series(False, index=u.index)
    orig = u.get("origem", pd.Series("", index=u.index)).fillna("").astype(str).str.contains("recupera|sistema", case=False)
    grupos = {"qualquer_contingencia": set(u.k[duas | cert | orig]), "duas_urnas_no_log": set(u.k[duas]), "certificado_diferente_do_log": set(u.k[cert]), "RED_ou_sistema_de_apuracao": set(u.k[orig])}
    R[f"caso_C_contingencias_2T_{ano}"] = {g: teste(b, c, 0.1, 9600 + int(ano) % 100) for g, c in grupos.items()} | {"definicao": "urnas_com_voto_no_log ≥ 2, ou certificado lido ≠ urna do log, ou origem RED/Sistema de Apuração"}
    print("C", ano, {g: (v.get("secoes_no_universo"), round(v.get("diferenca", 0), 3), v.get("p_bilateral_media"), v.get("leitura")) for g, v in R[f"caso_C_contingencias_2T_{ano}"].items() if isinstance(v, dict)}, flush=True)
json.dump(R, open(f"{RAIZ}/fase3/resultados/adv_casos.json", "w"), ensure_ascii=False, indent=1, default=float)
