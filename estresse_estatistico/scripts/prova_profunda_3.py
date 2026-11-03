#!/usr/bin/env python3
"""Prova Profunda 3 — investigação do resíduo e swing entre turnos.

H: Análise espacial do resíduo (r parcial 0,046 tem padrão geográfico?)
I: Swing 1T→2T por seção (padrão normal ou anômalo?)
J: Capturas 1T 2026 (totalização monotônica?)
"""

import json, gzip, os
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

BASE = Path(__file__).resolve().parents[2]
DADOS = BASE / "dados_leves"
CAPT = DADOS / "capturas_divulgacao_ao_vivo"

def _p(v):
    return float(f"{v:.6f}") if np.isfinite(v) else None


def carregar_com_perfil(ano, turno="2t"):
    u = pd.read_parquet(DADOS / f"urnas_{ano}_{turno}.parquet")
    pf = pd.read_parquet(DADOS / f"perfil_por_secao_{ano}.parquet")
    keys = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
    for k in keys:
        u[k] = u[k].astype(str)
        pf[k] = pf[k].astype(str)
    d = u.merge(pf, on=keys, how="inner")
    d = d.dropna(subset=["seq_dur_mediana", "bu_v13", "bu_comparecimento"])
    d = d[d["bu_comparecimento"] > 10]
    d["p13"] = d["bu_v13"] / d["bu_comparecimento"]
    return d, u


# ── H: ANÁLISE ESPACIAL DO RESÍDUO ──────────────────────────────────────

def teste_H1_residuo_por_uf(d, ano):
    """O resíduo (duração → resultado controlando demo) varia por UF?"""
    demo_cols = ["idade_60mais", "idade_ate24", "esc_1", "esc_8", "fem"]
    demo_cols = [c for c in demo_cols if c in d.columns]

    for col in ["p13", "seq_dur_mediana"] + demo_cols:
        d[f"{col}_dm"] = d.groupby("CD_MUNICIPIO")[col].transform(lambda x: x - x.mean())

    X = np.column_stack([d[f"{c}_dm"].values for c in demo_cols] + [np.ones(len(d))])
    mask = np.all(np.isfinite(X), axis=1)

    y_dur = d["seq_dur_mediana_dm"].values
    y_p13 = d["p13_dm"].values
    mask &= np.isfinite(y_dur) & np.isfinite(y_p13)

    X_m, y_dur_m, y_p13_m = X[mask], y_dur[mask], y_p13[mask]

    beta_dur = np.linalg.lstsq(X_m, y_dur_m, rcond=None)[0]
    res_dur = y_dur_m - X_m @ beta_dur
    beta_p13 = np.linalg.lstsq(X_m, y_p13_m, rcond=None)[0]
    res_p13 = y_p13_m - X_m @ beta_p13

    d_m = d[mask].copy()
    d_m["res_dur"] = res_dur
    d_m["res_p13"] = res_p13

    # Per-UF residual correlation
    por_uf = {}
    for uf, g in d_m.groupby("SG_UF"):
        if len(g) < 50:
            continue
        r, p = stats.pearsonr(g["res_dur"], g["res_p13"])
        por_uf[uf] = {"r_residual": _p(r), "p": _p(p), "n": len(g)}

    # Sort by absolute r
    por_uf = dict(sorted(por_uf.items(), key=lambda x: abs(x[1]["r_residual"]), reverse=True))

    # Is the residual correlated across UFs? (i.e., do all UFs show the same sign?)
    signs = [v["r_residual"] > 0 for v in por_uf.values()]
    pct_positivo = sum(signs) / len(signs) * 100 if signs else 0

    return {
        "teste": "H1",
        "ano": ano,
        "por_uf": por_uf,
        "pct_uf_positivo": _p(pct_positivo),
        "n_ufs": len(por_uf),
        "impacto_votos": "Se o resíduo for aleatório (50/50 positivo/negativo entre UFs), é ruído. Se >80% tiver o mesmo sinal, pode ser confundimento não observado."
    }


def teste_H2_residuo_modelo(d, ano):
    """O resíduo correlaciona com modelo da urna?"""
    demo_cols = ["idade_60mais", "idade_ate24", "esc_1", "esc_8", "fem"]
    demo_cols = [c for c in demo_cols if c in d.columns]

    for col in ["p13", "seq_dur_mediana"] + demo_cols:
        d[f"{col}_dm"] = d.groupby("CD_MUNICIPIO")[col].transform(lambda x: x - x.mean())

    X = np.column_stack([d[f"{c}_dm"].values for c in demo_cols] + [np.ones(len(d))])
    mask = np.all(np.isfinite(X), axis=1)
    y_p13 = d["p13_dm"].values
    mask &= np.isfinite(y_p13)

    X_m, y_p13_m = X[mask], y_p13[mask]
    beta = np.linalg.lstsq(X_m, y_p13_m, rcond=None)[0]
    res_p13 = y_p13_m - X_m @ beta

    d_m = d[mask].copy()
    d_m["res_p13"] = res_p13

    # Per-model residual
    if "modelo" in d_m.columns:
        por_modelo = {}
        for mod, g in d_m.groupby("modelo"):
            if len(g) < 100:
                continue
            por_modelo[mod] = {
                "media_residuo": _p(g["res_p13"].mean()),
                "std": _p(g["res_p13"].std()),
                "n": len(g),
            }

        # ANOVA on residual by model
        grupos = [g["res_p13"].values for _, g in d_m.groupby("modelo") if len(g) > 100]
        if len(grupos) > 1:
            F, p_anova = stats.f_oneway(*grupos)
        else:
            F, p_anova = np.nan, np.nan
    else:
        por_modelo = {}
        F, p_anova = np.nan, np.nan

    return {
        "teste": "H2",
        "ano": ano,
        "F_anova_residual": _p(F),
        "p_anova": _p(p_anova),
        "por_modelo": por_modelo,
        "impacto_votos": "Se o resíduo NÃO varia por modelo, o modelo não é causa. Se varia, o modelo pode ser proxy de algo não controlado (ex: zona rural)."
    }


# ── I: SWING 1T → 2T ────────────────────────────────────────────────────

def teste_I1_swing_distribuicao(ano):
    """Distribuição do swing 1T→2T por seção."""
    u2t = pd.read_parquet(DADOS / f"urnas_{ano}_2t.parquet")
    u1t_path = DADOS / f"urnas_{ano}_1t.parquet"
    if not u1t_path.exists():
        return {"teste": "I1", "ano": ano, "resultado": "sem dados do 1T"}

    u1t = pd.read_parquet(u1t_path)

    keys = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
    for k in keys:
        u2t[k] = u2t[k].astype(str)
        u1t[k] = u1t[k].astype(str)

    u2t = u2t[u2t["bu_comparecimento"] > 10].copy()
    u1t = u1t[u1t["bu_comparecimento"] > 10].copy()

    u2t["p13_2t"] = u2t["bu_v13"] / u2t["bu_comparecimento"]
    u1t["p13_1t"] = u1t["bu_v13"] / u1t["bu_comparecimento"]

    m = u2t[keys + ["p13_2t", "bu_comparecimento"]].merge(
        u1t[keys + ["p13_1t"]], on=keys, how="inner"
    )
    m["swing"] = m["p13_2t"] - m["p13_1t"]

    r, p_val = stats.pearsonr(m["p13_1t"], m["p13_2t"])

    # Distribution stats
    swing = m["swing"]
    return {
        "teste": "I1",
        "ano": ano,
        "n_secoes": len(m),
        "swing_media": _p(swing.mean()),
        "swing_mediana": _p(swing.median()),
        "swing_std": _p(swing.std()),
        "swing_p05": _p(swing.quantile(0.05)),
        "swing_p95": _p(swing.quantile(0.95)),
        "r_1t_2t": _p(r),
        "p_1t_2t": _p(p_val),
        "secoes_inverteram": int((m["swing"].abs() > 0.2).sum()),
        "impacto_votos": f"Correlação 1T-2T: r={r:.3f}. Swing médio: {swing.mean()*100:.1f}pp. {(swing.abs() > 0.2).sum()} seções com swing > 20pp."
    }


def teste_I2_swing_vs_duracao(ano):
    """O swing 1T→2T correlaciona com a mudança de duração?"""
    u2t = pd.read_parquet(DADOS / f"urnas_{ano}_2t.parquet")
    u1t_path = DADOS / f"urnas_{ano}_1t.parquet"
    if not u1t_path.exists():
        return {"teste": "I2", "ano": ano, "resultado": "sem dados do 1T"}
    u1t = pd.read_parquet(u1t_path)

    keys = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
    for k in keys:
        u2t[k] = u2t[k].astype(str)
        u1t[k] = u1t[k].astype(str)

    u2t = u2t.dropna(subset=["seq_dur_mediana", "bu_v13", "bu_comparecimento"])
    u1t = u1t.dropna(subset=["seq_dur_mediana", "bu_v13", "bu_comparecimento"])
    u2t = u2t[u2t["bu_comparecimento"] > 10].copy()
    u1t = u1t[u1t["bu_comparecimento"] > 10].copy()

    u2t["p13_2t"] = u2t["bu_v13"] / u2t["bu_comparecimento"]
    u1t["p13_1t"] = u1t["bu_v13"] / u1t["bu_comparecimento"]

    m = u2t[keys + ["p13_2t", "seq_dur_mediana"]].merge(
        u1t[keys + ["p13_1t", "seq_dur_mediana"]],
        on=keys, how="inner", suffixes=("_2t", "_1t")
    )
    m["swing"] = m["p13_2t"] - m["p13_1t"]
    m["delta_dur"] = m["seq_dur_mediana_2t"] - m["seq_dur_mediana_1t"]

    # Demean within municipality
    for c in ["swing", "delta_dur"]:
        m[f"{c}_dm"] = m.groupby("CD_MUNICIPIO")[c].transform(lambda x: x - x.mean())

    m = m.dropna(subset=["swing_dm", "delta_dur_dm"])
    r, p_val = stats.pearsonr(m["delta_dur_dm"], m["swing_dm"])

    return {
        "teste": "I2",
        "ano": ano,
        "n_secoes": len(m),
        "r_delta_dur_swing": _p(r),
        "p": _p(p_val),
        "delta_dur_media": _p(m["delta_dur"].mean()),
        "impacto_votos": f"Correlação mudança-de-duração × swing (intra-mun): r={r:.4f}. Se fraude acelerasse urnas pró-candidato, o swing seria correlacionado com Δduração."
    }


def teste_I3_swing_outliers(ano):
    """Seções com swing extremo: são explicáveis?"""
    u2t = pd.read_parquet(DADOS / f"urnas_{ano}_2t.parquet")
    u1t_path = DADOS / f"urnas_{ano}_1t.parquet"
    if not u1t_path.exists():
        return {"teste": "I3", "ano": ano, "resultado": "sem dados do 1T"}
    u1t = pd.read_parquet(u1t_path)

    keys = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
    for k in keys:
        u2t[k] = u2t[k].astype(str)
        u1t[k] = u1t[k].astype(str)

    u2t = u2t[u2t["bu_comparecimento"] > 10].copy()
    u1t = u1t[u1t["bu_comparecimento"] > 10].copy()

    u2t["p13_2t"] = u2t["bu_v13"] / u2t["bu_comparecimento"]
    u1t["p13_1t"] = u1t["bu_v13"] / u1t["bu_comparecimento"]

    m = u2t[keys + ["p13_2t", "bu_comparecimento"]].merge(
        u1t[keys + ["p13_1t"]], on=keys, how="inner"
    )
    m["swing"] = m["p13_2t"] - m["p13_1t"]

    # Municipal mean swing
    m["swing_mun"] = m.groupby("CD_MUNICIPIO")["swing"].transform("mean")
    m["swing_resid"] = m["swing"] - m["swing_mun"]

    # Outliers: > 3 std from municipal mean
    std_mun = m.groupby("CD_MUNICIPIO")["swing_resid"].transform("std")
    m["z_swing"] = m["swing_resid"] / std_mun.replace(0, np.nan)

    outliers = m[m["z_swing"].abs() > 3].copy()
    n_outliers = len(outliers)

    # Are outliers biased toward one candidate?
    if n_outliers > 0:
        swing_outlier_mean = outliers["swing_resid"].mean()
        outlier_sizes = outliers["bu_comparecimento"]
        votos_outlier = (outliers["swing_resid"] * outliers["bu_comparecimento"]).sum()
    else:
        swing_outlier_mean = 0
        votos_outlier = 0

    return {
        "teste": "I3",
        "ano": ano,
        "n_secoes": len(m),
        "n_outliers_3std": n_outliers,
        "pct_outliers": _p(n_outliers / len(m) * 100),
        "swing_medio_outliers": _p(swing_outlier_mean) if n_outliers > 0 else None,
        "votos_liquidos_outliers": int(votos_outlier),
        "impacto_votos": f"{n_outliers} seções com swing > 3σ da média municipal. Impacto líquido: {int(votos_outlier)} votos. Esperado em distribuição normal: ~0,3% = ~{int(len(m)*0.003)}."
    }


# ── J: CAPTURAS 1T 2026 ────────────────────────────────────────────────

def _parse_captura(path):
    raw = open(path, "rb").read()
    try:
        j = json.loads(gzip.decompress(raw))
    except:
        j = json.loads(raw)

    ts = f"{j['dg']} {j['hg']}"
    votos = {}

    if "carg" in j:
        s_dict = j["s"]
        secoes = int(str(s_dict["st"]).replace(".", ""))
        secoes_total = int(str(s_dict["ts"]).replace(".", ""))
        total_votos = int(str(j["v"]["tv"]).replace(".", ""))
        pres = j["carg"][0]
        for key in ("agr", "fed"):
            if key not in pres:
                continue
            for grupo in pres[key]:
                pars = grupo.get("par", [grupo])
                for par in pars:
                    cands = par.get("cand", [])
                    for c in cands:
                        nr = c.get("n", "")
                        vap = c.get("vap", c.get("tvtn", "0"))
                        if nr and vap:
                            votos[nr] = int(str(vap).replace(".", ""))
    else:
        secoes = int(str(j.get("st", "0")).replace(".", ""))
        secoes_total = int(str(j.get("s", "0")).replace(".", ""))
        total_votos = int(str(j.get("tv", "0")).replace(".", ""))
        for c in j.get("cand", []):
            nr = c.get("n", "")
            vap = c.get("vap", "0")
            if nr and vap:
                votos[nr] = int(str(vap).replace(".", ""))

    return {
        "arquivo": os.path.basename(path),
        "timestamp": ts,
        "secoes_totalizadas": secoes,
        "secoes_total": secoes_total,
        "pct_totalizado": round(secoes / secoes_total * 100, 2) if secoes_total > 0 else 0,
        "votos_total": total_votos,
        "votos": votos,
    }


def teste_J1_monotonia_1t_2026():
    """Monotonia da divulgação no 1T 2026."""
    capturas = []
    for a in sorted(CAPT.glob("2026_1T_*")):
        try:
            capturas.append(_parse_captura(a))
        except Exception as e:
            print(f"  Erro em {a.name}: {e}")

    if len(capturas) < 2:
        return {"teste": "J1", "resultado": f"apenas {len(capturas)} capturas válidas"}

    capturas.sort(key=lambda x: x["timestamp"])

    violacoes = []
    for i in range(1, len(capturas)):
        prev, curr = capturas[i-1], capturas[i]
        if curr["votos_total"] < prev["votos_total"]:
            violacoes.append({
                "de": prev["timestamp"], "para": curr["timestamp"],
                "votos_antes": prev["votos_total"], "votos_depois": curr["votos_total"]
            })
        for cand in prev["votos"]:
            if curr["votos"].get(cand, 0) < prev["votos"][cand]:
                violacoes.append({
                    "de": prev["timestamp"], "para": curr["timestamp"],
                    "candidato": cand,
                    "antes": prev["votos"][cand], "depois": curr["votos"].get(cand, 0)
                })

    timeline = []
    for c in capturas:
        entry = {"ts": c["timestamp"], "pct": c["pct_totalizado"], "votos": c["votos_total"]}
        for nr, v in c["votos"].items():
            entry[f"v{nr}"] = v
        timeline.append(entry)

    return {
        "teste": "J1",
        "ano": 2026,
        "turno": "1T",
        "capturas": len(capturas),
        "primeira": capturas[0]["timestamp"],
        "ultima": capturas[-1]["timestamp"],
        "pct_primeira": capturas[0]["pct_totalizado"],
        "pct_ultima": capturas[-1]["pct_totalizado"],
        "violacoes": len(violacoes),
        "detalhes": violacoes[:5],
        "timeline": timeline,
        "impacto_votos": f"{sum(v.get('votos_antes',0)-v.get('votos_depois',0) for v in violacoes if 'votos_antes' in v)} votos regrediram." if violacoes else "Zero votos regrediram no 1T 2026."
    }


# ── MAIN ─────────────────────────────────────────────────────────────────

def rodar(ano):
    import sys
    print(f"\n{'='*60}")
    print(f" PROVA PROFUNDA 3 — {ano}")
    print(f"{'='*60}")

    d, u = carregar_com_perfil(ano)
    print(f"  Seções com perfil: {len(d):,}")

    resultados = {}

    print("  [H1] Resíduo por UF...")
    resultados["H1"] = teste_H1_residuo_por_uf(d.copy(), ano)
    h1 = resultados["H1"]
    print(f"       {h1['n_ufs']} UFs, {h1['pct_uf_positivo']}% com resíduo positivo")

    print("  [H2] Resíduo por modelo...")
    resultados["H2"] = teste_H2_residuo_modelo(d.copy(), ano)
    print(f"       F={resultados['H2']['F_anova_residual']}")

    print("  [I1] Swing 1T→2T distribuição...")
    resultados["I1"] = teste_I1_swing_distribuicao(ano)
    if "r_1t_2t" in resultados["I1"]:
        print(f"       r(1T,2T)={resultados['I1']['r_1t_2t']}  swing médio={resultados['I1']['swing_media']}")

    print("  [I2] Swing × mudança de duração...")
    resultados["I2"] = teste_I2_swing_vs_duracao(ano)
    if "r_delta_dur_swing" in resultados["I2"]:
        print(f"       r(Δdur, swing)={resultados['I2']['r_delta_dur_swing']}")

    print("  [I3] Outliers de swing...")
    resultados["I3"] = teste_I3_swing_outliers(ano)
    if "n_outliers_3std" in resultados["I3"]:
        print(f"       {resultados['I3']['n_outliers_3std']} outliers, impacto={resultados['I3']['votos_liquidos_outliers']}")

    out = BASE / "estresse_estatistico" / "resultados" / f"resultado_profunda3_{ano}.json"
    with open(out, "w") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False, default=str)
    print(f"  Salvo em {out}")

    return resultados


if __name__ == "__main__":
    r2026 = rodar(2026)
    r2022 = rodar(2022)

    # J1: capturas 1T 2026
    print(f"\n{'='*60}")
    print(f" CAPTURAS 1T 2026")
    print(f"{'='*60}")
    j1 = teste_J1_monotonia_1t_2026()
    print(f"  J1: {j1.get('capturas', 0)} capturas, {j1.get('violacoes', '?')} violações")

    # Save J1 separately
    out = BASE / "estresse_estatistico" / "resultados" / "resultado_profunda3_j1.json"
    with open(out, "w") as f:
        json.dump(j1, f, indent=2, ensure_ascii=False, default=str)

    # Summary
    print(f"\n{'='*60}")
    print(" RESUMO PROVA PROFUNDA 3")
    print(f"{'='*60}")
    for ano, r in [(2026, r2026), (2022, r2022)]:
        h1 = r.get("H1", {})
        i1 = r.get("I1", {})
        i3 = r.get("I3", {})
        print(f"\n  {ano}:")
        print(f"    H1: {h1.get('pct_uf_positivo')}% UFs com resíduo positivo")
        print(f"    I1: swing médio = {i1.get('swing_media')}, r(1T,2T) = {i1.get('r_1t_2t')}")
        print(f"    I3: {i3.get('n_outliers_3std', '?')} outliers, impacto = {i3.get('votos_liquidos_outliers', '?')}")
