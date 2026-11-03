"""Família G — Simulação de geração artificial.
Gera mundos sintéticos e roda os testes EA1, EB1, EC1, ED1, EE1 em cada.

Uso: python simulacoes.py [2026|2022]
Saída: ../resultados/resultado_simulacoes_<ano>.json
"""
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore", category=RuntimeWarning)

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"

print(f"=== Simulações adversariais — {ANO} ===", flush=True)

df = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/secoes_{ANO}.parquet"))
df = df[df["SG_UF"] != "ZZ"].copy()
df["mun"] = df["SG_UF"] + df["CD_MUNICIPIO"]

lg = lambda x, n: np.log((x + 0.5) / (n - x + 0.5))
rng = np.random.default_rng(73)

# Funções auxiliares de medição (versões leves dos testes)
def medir_digitos(v, n):
    """Chi-quadrado do último dígito contra uniforme, para v >= 100."""
    mask = v >= 100
    if mask.sum() < 1000:
        return 0.0
    ult = v[mask] % 10
    obs = np.bincount(ult, minlength=10).astype(float)
    esp = np.full(10, obs.sum() / 10)
    return float(np.sum((obs - esp) ** 2 / esp))

def medir_dispersao_local(df_w, turno):
    """Fração de locais subdispersos (ratio var_obs/var_esp < 0.3)."""
    local_col = "local_2" if "local_2" in df_w.columns else "mun"
    val_col = f"validos_{turno}"
    v_col = f"v13_{turno}"
    subdispersos = 0
    total = 0
    for local, grp in df_w.groupby(local_col):
        v = grp[v_col].fillna(0).values.astype(int)
        n = grp[val_col].fillna(0).values.astype(int)
        mask = n >= 20
        v, n = v[mask], n[mask]
        if len(v) < 5:
            continue
        total += 1
        p = v.sum() / n.sum()
        var_obs = np.var(v / n, ddof=1) if len(v) > 1 else 0
        var_binom = np.mean(p * (1 - p) / n)
        if var_binom > 0 and var_obs / var_binom < 0.3:
            subdispersos += 1
    return subdispersos / total if total > 0 else 0

def medir_scan_max(df_w, turno):
    """Max scan statistic por município (|z_medio| * sqrt(n))."""
    val_col = f"validos_{turno}"
    v_col = f"v13_{turno}"
    d = df_w[[val_col, v_col, "SG_UF", "mun"]].dropna().copy()
    d = d[d[val_col] >= 20]
    d["logit"] = lg(d[v_col].astype(int), d[val_col].astype(int))
    d["z_uf"] = 0.0
    for uf, idx in d.groupby("SG_UF").groups.items():
        sub = d.loc[idx]
        med = sub["logit"].median()
        mad = 1.4826 * (sub["logit"] - med).abs().median()
        d.loc[idx, "z_uf"] = (sub["logit"] - med) / (mad or 1)
    g = d.groupby("mun")["z_uf"]
    scan = (g.mean() * np.sqrt(g.size())).abs()
    return float(scan.max()) if len(scan) > 0 else 0

def medir_r2_turnos(df_w):
    """R² mediano da relação logit_2 ~ logit_1 por município."""
    d = df_w[["mun", "validos_1", "v13_1", "validos_2", "v13_2"]].dropna().copy()
    d = d[(d["validos_1"] >= 20) & (d["validos_2"] >= 20)]
    d["l1"] = lg(d["v13_1"].astype(int), d["validos_1"].astype(int))
    d["l2"] = lg(d["v13_2"].astype(int), d["validos_2"].astype(int))
    r2s = []
    for mun, grp in d.groupby("mun"):
        if len(grp) < 10:
            continue
        x, y = grp["l1"].values, grp["l2"].values
        if x.std() < 1e-8:
            continue
        beta = np.polyfit(x, y, 1)
        ss_res = ((y - np.polyval(beta, x)) ** 2).sum()
        ss_tot = ((y - y.mean()) ** 2).sum()
        r2s.append(1 - ss_res / ss_tot if ss_tot > 0 else 0)
    return float(np.median(r2s)) if r2s else 0

# Linha-base (dados reais)
print("Medindo linha-base nos dados reais...", flush=True)
df["local_2"] = df["mun"] + "_" + df["NR_ZONA"] + "_" + df["NR_LOCAL_VOTACAO_2"].astype(str)

baseline = {
    "digitos_2t": medir_digitos(df["v13_2"].fillna(0).astype(int).values, df["validos_2"].fillna(0).astype(int).values),
    "dispersao_local_2t": medir_dispersao_local(df, 2),
    "scan_max_2t": medir_scan_max(df, 2),
    "r2_turnos": medir_r2_turnos(df),
}
print(f"  Baseline: {json.dumps(baseline, indent=2)}", flush=True)

# Cenários de alteração
cenarios = [
    ("troca_dispersa_pro_lula_50k", "dispersa", "lula", 50000),
    ("troca_dispersa_contra_lula_50k", "dispersa", "adversario", 50000),
    ("troca_concentrada_pro_lula_50k", "concentrada", "lula", 50000),
    ("troca_concentrada_contra_lula_50k", "concentrada", "adversario", 50000),
    ("suavizacao_forcada", "suavizacao", None, 0),
    ("algoritmo_proporcional", "proporcional", None, 0),
]

resultados = {"ano": ANO, "baseline": baseline, "cenarios": {}}

for nome, tipo, direcao, magnitude in cenarios:
    print(f"\nSimulando: {nome}...", flush=True)
    dw = df.copy()

    if tipo == "dispersa":
        # Trocar votos em seções aleatórias (1% das seções)
        mask_val = dw["validos_2"].fillna(0) >= 50
        indices = dw[mask_val].index.values
        n_sec = max(1, int(0.01 * len(indices)))
        escolhidas = rng.choice(indices, n_sec, replace=False)
        votos_por_sec = magnitude // n_sec
        for idx in escolhidas:
            v13 = int(dw.loc[idx, "v13_2"])
            v22 = int(dw.loc[idx, "v22_2"])
            if direcao == "lula":
                troca = min(votos_por_sec, v22)
                dw.loc[idx, "v13_2"] = v13 + troca
                dw.loc[idx, "v22_2"] = v22 - troca
            else:
                troca = min(votos_por_sec, v13)
                dw.loc[idx, "v13_2"] = v13 - troca
                dw.loc[idx, "v22_2"] = v22 + troca

    elif tipo == "concentrada":
        # Trocar votos em 5 municípios médios
        mun_sizes = dw.groupby("mun").size()
        mun_medios = mun_sizes[(mun_sizes >= 50) & (mun_sizes <= 500)]
        if len(mun_medios) < 5:
            continue
        mun_alvo = rng.choice(mun_medios.index.values, 5, replace=False)
        votos_por_mun = magnitude // 5
        for m in mun_alvo:
            idx_mun = dw[dw["mun"] == m].index
            votos_por_sec = votos_por_mun // len(idx_mun)
            for idx in idx_mun:
                v13 = int(dw.loc[idx, "v13_2"])
                v22 = int(dw.loc[idx, "v22_2"])
                if direcao == "lula":
                    troca = min(votos_por_sec, v22)
                    dw.loc[idx, "v13_2"] = v13 + troca
                    dw.loc[idx, "v22_2"] = v22 - troca
                else:
                    troca = min(votos_por_sec, v13)
                    dw.loc[idx, "v13_2"] = v13 - troca
                    dw.loc[idx, "v22_2"] = v22 + troca

    elif tipo == "suavizacao":
        # Reduzir variância dentro de cada local: empurrar para a média do local
        for local, grp in dw.groupby("local_2"):
            if len(grp) < 3:
                continue
            idx = grp.index
            v = grp["v13_2"].fillna(0).values.astype(float)
            n = grp["validos_2"].fillna(0).values.astype(float)
            mask = n >= 20
            if mask.sum() < 3:
                continue
            p_local = v[mask].sum() / n[mask].sum()
            # Empurrar 50% para a média
            v_novo = np.round(v * 0.5 + p_local * n * 0.5).astype(int)
            v_novo = np.clip(v_novo, 0, n.astype(int))
            dw.loc[idx, "v13_2"] = v_novo
            dw.loc[idx, "v22_2"] = (n - v_novo).astype(int) - dw.loc[idx, "branco_2"].fillna(0).astype(int) - dw.loc[idx, "nulo_2"].fillna(0).astype(int)
            dw.loc[idx, "v22_2"] = dw.loc[idx, "v22_2"].clip(lower=0)

    elif tipo == "proporcional":
        # Gerar votos com regra determinística (proporção municipal exata)
        for mun, grp in dw.groupby("mun"):
            idx = grp.index
            v = grp["v13_2"].fillna(0).values.astype(float)
            n = grp["validos_2"].fillna(0).values.astype(float)
            mask = n >= 20
            if mask.sum() < 3:
                continue
            p_mun = v[mask].sum() / n[mask].sum()
            v_novo = np.round(p_mun * n).astype(int)
            v_novo = np.clip(v_novo, 0, n.astype(int))
            dw.loc[idx, "v13_2"] = v_novo
            dw.loc[idx, "v22_2"] = (n - v_novo).astype(int) - dw.loc[idx, "branco_2"].fillna(0).astype(int) - dw.loc[idx, "nulo_2"].fillna(0).astype(int)
            dw.loc[idx, "v22_2"] = dw.loc[idx, "v22_2"].clip(lower=0)

    dw["validos_2"] = dw["v13_2"].fillna(0).astype(int) + dw["v22_2"].fillna(0).astype(int)

    medidas = {
        "digitos_2t": medir_digitos(dw["v13_2"].fillna(0).astype(int).values, dw["validos_2"].fillna(0).astype(int).values),
        "dispersao_local_2t": medir_dispersao_local(dw, 2),
        "scan_max_2t": medir_scan_max(dw, 2),
        "r2_turnos": medir_r2_turnos(dw),
    }
    alarmes = {}
    for k in medidas:
        if k in baseline and baseline[k] > 0:
            ratio = medidas[k] / baseline[k]
            alarmes[k] = "ALARME" if ratio > 2.0 or ratio < 0.3 else "ok"
        else:
            alarmes[k] = "?"

    resultados["cenarios"][nome] = {
        "tipo": tipo,
        "direcao": direcao,
        "magnitude_votos": magnitude,
        "medidas": medidas,
        "alarmes": alarmes,
    }
    print(f"  Medidas: {json.dumps(medidas)}", flush=True)
    print(f"  Alarmes: {json.dumps(alarmes)}", flush=True)

out_path = os.path.join(AQUI, "..", "resultados", f"resultado_simulacoes_{ANO}.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
json.dump(resultados, open(out_path, "w"), ensure_ascii=False, indent=1, default=str)
print(f"\nSalvo em {out_path}", flush=True)
print("=== Fim simulações ===", flush=True)
