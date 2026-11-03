#!/usr/bin/env python3
"""Prova Profunda 2 — três frentes independentes de verificação.

E: Controle demográfico (a correlação duração×resultado sobrevive?)
F: bweb CSV bruto × parquet (os dados que o site público mostra batem?)
G: Auditoria da divulgação ao vivo (totalização cresceu monotonicamente?)

Roda em 2026 e 2022.
"""

import json, gzip, glob, os, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

BASE = Path(__file__).resolve().parents[2]
DADOS = BASE / "dados_leves"
BWEB = BASE / "dados" / "2turno"
CAPT = DADOS / "capturas_divulgacao_ao_vivo"

def _p(v):
    return float(f"{v:.6f}") if np.isfinite(v) else None

def carregar(ano, turno="2t"):
    u = pd.read_parquet(DADOS / f"urnas_{ano}_{turno}.parquet")
    pf_path = DADOS / f"perfil_por_secao_{ano}.parquet"
    pf = pd.read_parquet(pf_path) if pf_path.exists() else None
    return u, pf

# ── E: CONTROLE DEMOGRÁFICO ──────────────────────────────────────────────

def teste_E1_correlacao_parcial(u, pf, ano):
    """Correlação parcial duração×resultado controlando idade+escolaridade+gênero."""
    if pf is None:
        return {"teste": "E1", "resultado": "sem perfil demográfico", "ano": ano}

    keys = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
    for k in keys:
        u[k] = u[k].astype(str)
        pf[k] = pf[k].astype(str)

    d = u.merge(pf, on=keys, how="inner")
    d = d.dropna(subset=["seq_dur_mediana", "bu_v13", "bu_comparecimento"])
    d = d[d["bu_comparecimento"] > 10]
    d["p13"] = d["bu_v13"] / d["bu_comparecimento"]

    # Within-municipality: demean
    for col in ["p13", "seq_dur_mediana", "idade_60mais", "idade_ate24",
                "esc_1", "esc_8", "fem"]:
        if col not in d.columns:
            continue
        d[f"{col}_dm"] = d.groupby("CD_MUNICIPIO")[col].transform(
            lambda x: x - x.mean()
        )

    # Simple correlation (without demographics)
    r_simples, p_simples = stats.pearsonr(d["seq_dur_mediana_dm"], d["p13_dm"])

    # Partial correlation: regress both on demographics, correlate residuals
    demo_cols = [f"{c}_dm" for c in ["idade_60mais", "idade_ate24", "esc_1", "esc_8", "fem"]
                 if f"{c}_dm" in d.columns]

    if demo_cols:
        X = d[demo_cols].values
        X = np.column_stack([X, np.ones(len(X))])

        # Residualize duration
        y_dur = d["seq_dur_mediana_dm"].values
        mask = np.isfinite(y_dur) & np.all(np.isfinite(X), axis=1)

        y_p13 = d["p13_dm"].values
        mask &= np.isfinite(y_p13)

        X_m, y_dur_m, y_p13_m = X[mask], y_dur[mask], y_p13[mask]

        beta_dur = np.linalg.lstsq(X_m, y_dur_m, rcond=None)[0]
        res_dur = y_dur_m - X_m @ beta_dur

        beta_p13 = np.linalg.lstsq(X_m, y_p13_m, rcond=None)[0]
        res_p13 = y_p13_m - X_m @ beta_p13

        r_parcial, p_parcial = stats.pearsonr(res_dur, res_p13)
    else:
        r_parcial, p_parcial = np.nan, np.nan

    # R² of demographics alone predicting p13
    if demo_cols:
        beta_demo = np.linalg.lstsq(X_m, y_p13_m, rcond=None)[0]
        ss_res = np.sum((y_p13_m - X_m @ beta_demo) ** 2)
        ss_tot = np.sum((y_p13_m - y_p13_m.mean()) ** 2)
        r2_demo = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    else:
        r2_demo = np.nan

    reducao = 1 - abs(r_parcial) / abs(r_simples) if r_simples != 0 else np.nan

    return {
        "teste": "E1",
        "ano": ano,
        "n_secoes": int(mask.sum()) if demo_cols else len(d),
        "r_simples_intra_mun": _p(r_simples),
        "p_simples": _p(p_simples),
        "r_parcial_controlando_demo": _p(r_parcial),
        "p_parcial": _p(p_parcial),
        "reducao_pct": _p(reducao * 100) if reducao is not None and np.isfinite(reducao) else None,
        "r2_demo_sozinha": _p(r2_demo),
        "demo_controles": demo_cols,
        "impacto_votos": "Se r_parcial → 0, a correlação é 100% demográfica (0 votos fraudados). Se r_parcial ≈ r_simples, a demografia não explica."
    }


def teste_E2_regressao_completa(u, pf, ano):
    """Regressão: p13 ~ duração + todas as demográficas (intra-município)."""
    if pf is None:
        return {"teste": "E2", "resultado": "sem perfil", "ano": ano}

    keys = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
    for k in keys:
        u[k] = u[k].astype(str)
        pf[k] = pf[k].astype(str)

    d = u.merge(pf, on=keys, how="inner")
    d = d.dropna(subset=["seq_dur_mediana", "bu_v13", "bu_comparecimento"])
    d = d[d["bu_comparecimento"] > 10]
    d["p13"] = d["bu_v13"] / d["bu_comparecimento"]

    # Demean within municipality
    reg_cols = ["seq_dur_mediana", "idade_60mais", "idade_ate24", "esc_1", "esc_8", "fem"]
    reg_cols = [c for c in reg_cols if c in d.columns]

    for col in ["p13"] + reg_cols:
        d[f"{col}_dm"] = d.groupby("CD_MUNICIPIO")[col].transform(lambda x: x - x.mean())

    y = d["p13_dm"].values
    X_all = np.column_stack([d[f"{c}_dm"].values for c in reg_cols] + [np.ones(len(d))])
    mask = np.all(np.isfinite(X_all), axis=1) & np.isfinite(y)

    X_m, y_m = X_all[mask], y[mask]
    beta = np.linalg.lstsq(X_m, y_m, rcond=None)[0]

    ss_res = np.sum((y_m - X_m @ beta) ** 2)
    ss_tot = np.sum((y_m - y_m.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

    # Beta and t-stat for duration
    n, k = X_m.shape
    mse = ss_res / (n - k)
    cov = mse * np.linalg.inv(X_m.T @ X_m)
    se = np.sqrt(np.diag(cov))
    t_stats = beta / se

    coefs = {}
    for i, c in enumerate(reg_cols):
        coefs[c] = {"beta": _p(beta[i]), "t": _p(t_stats[i]), "se": _p(se[i])}

    return {
        "teste": "E2",
        "ano": ano,
        "n": int(mask.sum()),
        "r2_completo": _p(r2),
        "coeficientes": coefs,
        "impacto_votos": f"Beta da duração = {_p(beta[0])} pp por segundo. Se fraude artificial acelerasse 1s por urna, mudaria ~{abs(beta[0])*d['bu_comparecimento'].mean():.0f} votos por seção."
    }


def teste_E3_estratificado(u, pf, ano):
    """Correlação duração×resultado em estratos demográficos homogêneos."""
    if pf is None:
        return {"teste": "E3", "resultado": "sem perfil", "ano": ano}

    keys = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
    for k in keys:
        u[k] = u[k].astype(str)
        pf[k] = pf[k].astype(str)

    d = u.merge(pf, on=keys, how="inner")
    d = d.dropna(subset=["seq_dur_mediana", "bu_v13", "bu_comparecimento"])
    d = d[d["bu_comparecimento"] > 10]
    d["p13"] = d["bu_v13"] / d["bu_comparecimento"]

    resultados = {}

    # Stratify by age_60+
    if "idade_60mais" in d.columns:
        d["q_idoso"] = pd.qcut(d["idade_60mais"], 4, labels=["Q1_jovem", "Q2", "Q3", "Q4_idoso"], duplicates="drop")
        for q in d["q_idoso"].dropna().unique():
            sub = d[d["q_idoso"] == q]
            # Demean within municipality in this stratum
            sub = sub.copy()
            for c in ["p13", "seq_dur_mediana"]:
                sub[f"{c}_dm"] = sub.groupby("CD_MUNICIPIO")[c].transform(lambda x: x - x.mean())
            sub = sub.dropna(subset=["p13_dm", "seq_dur_mediana_dm"])
            if len(sub) > 30:
                r, p = stats.pearsonr(sub["seq_dur_mediana_dm"], sub["p13_dm"])
                resultados[str(q)] = {"r": _p(r), "p": _p(p), "n": len(sub)}

    # Stratify by education
    if "esc_8" in d.columns:
        d["q_esc"] = pd.qcut(d["esc_8"], 4, labels=["Q1_baixa", "Q2", "Q3", "Q4_alta"], duplicates="drop")
        for q in d["q_esc"].dropna().unique():
            sub = d[d["q_esc"] == q]
            sub = sub.copy()
            for c in ["p13", "seq_dur_mediana"]:
                sub[f"{c}_dm"] = sub.groupby("CD_MUNICIPIO")[c].transform(lambda x: x - x.mean())
            sub = sub.dropna(subset=["p13_dm", "seq_dur_mediana_dm"])
            if len(sub) > 30:
                r, p = stats.pearsonr(sub["seq_dur_mediana_dm"], sub["p13_dm"])
                resultados[f"esc_{q}"] = {"r": _p(r), "p": _p(p), "n": len(sub)}

    return {
        "teste": "E3",
        "ano": ano,
        "estratos": resultados,
        "impacto_votos": "Se r→0 nos estratos homogêneos, toda a correlação era demográfica. Se r persiste, pode haver outro fator."
    }


# ── F: BWEB CSV BRUTO × PARQUET ─────────────────────────────────────────

def teste_F1_bweb_vs_parquet(u, ano):
    """Lê todos os CSVs do bweb e compara votos por seção contra o parquet."""
    if ano == 2026:
        bweb_dir = BASE / "dados" / "2turno"
    else:
        bweb_dir = BASE / "dados" / "2022" / "2turno"
        if not bweb_dir.exists():
            bweb_dir = BASE / "dados" / "2turno"

    csvs = sorted(bweb_dir.glob(f"bweb_*_presidente.csv"))
    if not csvs:
        return {"teste": "F1", "ano": ano, "resultado": "nenhum CSV bweb encontrado"}

    frames = []
    for csv_path in csvs:
        try:
            df = pd.read_csv(csv_path, sep=";", encoding="latin1", dtype=str, low_memory=False)
            sub = df[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO",
                       "NR_VOTAVEL", "QT_VOTOS"]].copy()
            sub["QT_VOTOS"] = pd.to_numeric(sub["QT_VOTOS"], errors="coerce")
            sub = sub.rename(columns={"NR_VOTAVEL": "NR_CAND",
                                      "QT_VOTOS": "votos_bweb"})
            frames.append(sub)
        except Exception as e:
            print(f"  Erro lendo {csv_path.name}: {e}", file=sys.stderr)

    if not frames:
        return {"teste": "F1", "ano": ano, "resultado": "falha na leitura dos CSVs"}

    bweb = pd.concat(frames, ignore_index=True)

    # Pivot: one row per section with v13_bweb, v22_bweb
    bweb["NR_CAND"] = bweb["NR_CAND"].astype(str).str.strip()

    v13 = bweb[bweb["NR_CAND"] == "13"].groupby(
        ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
    )["votos_bweb"].sum().reset_index().rename(columns={"votos_bweb": "v13_bweb"})

    v22 = bweb[bweb["NR_CAND"] == "22"].groupby(
        ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
    )["votos_bweb"].sum().reset_index().rename(columns={"votos_bweb": "v22_bweb"})

    bweb_sec = v13.merge(v22, on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"], how="outer")

    # Merge with parquet
    keys = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
    for k in keys:
        u[k] = u[k].astype(str).str.strip()
        bweb_sec[k] = bweb_sec[k].astype(str).str.strip()

    m = u[keys + ["bu_v13", "bu_v22"]].merge(bweb_sec, on=keys, how="outer", indicator=True)

    only_parquet = int((m["_merge"] == "left_only").sum())
    only_bweb = int((m["_merge"] == "right_only").sum())
    both = m[m["_merge"] == "both"].copy()

    both["diff_v13"] = both["bu_v13"].round(0) - both["v13_bweb"].round(0)
    both["diff_v22"] = both["bu_v22"].round(0) - both["v22_bweb"].round(0)

    divergentes_v13 = int((both["diff_v13"].abs() > 0.5).sum())
    divergentes_v22 = int((both["diff_v22"].abs() > 0.5).sum())

    # Details of divergent sections
    div_details = []
    div = both[(both["diff_v13"].abs() > 0) | (both["diff_v22"].abs() > 0)]
    for _, row in div.head(20).iterrows():
        div_details.append({
            "uf": row["SG_UF"],
            "mun": row["CD_MUNICIPIO"],
            "zona": row["NR_ZONA"],
            "secao": row["NR_SECAO"],
            "bu_v13": _p(row["bu_v13"]) if pd.notna(row["bu_v13"]) else None,
            "bweb_v13": _p(row["v13_bweb"]) if pd.notna(row["v13_bweb"]) else None,
            "diff_v13": _p(row["diff_v13"]) if pd.notna(row["diff_v13"]) else None,
            "diff_v22": _p(row["diff_v22"]) if pd.notna(row["diff_v22"]) else None,
        })

    total_votos_div = int(div["diff_v13"].abs().sum() + div["diff_v22"].abs().sum()) if len(div) > 0 else 0

    return {
        "teste": "F1",
        "ano": ano,
        "csvs_lidos": len(csvs),
        "secoes_bweb": len(bweb_sec),
        "secoes_parquet": len(u),
        "secoes_ambos": len(both),
        "so_parquet": only_parquet,
        "so_bweb": only_bweb,
        "divergentes_v13": divergentes_v13,
        "divergentes_v22": divergentes_v22,
        "total_votos_divergentes": total_votos_div,
        "exemplos": div_details[:10],
        "impacto_votos": f"{total_votos_div} votos divergem entre o CSV público e o BU extraído da urna."
    }


# ── G: AUDITORIA DA DIVULGAÇÃO AO VIVO ──────────────────────────────────

def _parse_captura(path):
    """Extrai timestamp, seções totalizadas e votos por candidato."""
    raw = open(path, "rb").read()
    try:
        j = json.loads(gzip.decompress(raw))
    except gzip.BadGzipFile:
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


def teste_G1_monotonia(ano, turno_label):
    """Verifica que votos só crescem ao longo da divulgação."""
    pattern = f"{ano}_{turno_label}_*"
    arquivos = sorted(CAPT.glob(pattern))

    capturas = []
    for a in arquivos:
        try:
            capturas.append(_parse_captura(a))
        except Exception as e:
            print(f"  Erro em {a.name}: {e}", file=sys.stderr)

    if len(capturas) < 2:
        return {"teste": "G1", "ano": ano, "turno": turno_label,
                "resultado": f"apenas {len(capturas)} capturas válidas"}

    capturas.sort(key=lambda x: x["timestamp"])

    violacoes_secoes = []
    violacoes_votos = []

    for i in range(1, len(capturas)):
        prev, curr = capturas[i-1], capturas[i]

        if curr["secoes_totalizadas"] < prev["secoes_totalizadas"]:
            violacoes_secoes.append({
                "de": prev["timestamp"],
                "para": curr["timestamp"],
                "secoes_antes": prev["secoes_totalizadas"],
                "secoes_depois": curr["secoes_totalizadas"],
            })

        if curr["votos_total"] < prev["votos_total"]:
            violacoes_votos.append({
                "de": prev["timestamp"],
                "para": curr["timestamp"],
                "votos_antes": prev["votos_total"],
                "votos_depois": curr["votos_total"],
                "diferenca": prev["votos_total"] - curr["votos_total"],
            })

        # Per-candidate monotonicity
        for cand in prev["votos"]:
            v_prev = prev["votos"].get(cand, 0)
            v_curr = curr["votos"].get(cand, 0)
            if v_curr < v_prev:
                violacoes_votos.append({
                    "de": prev["timestamp"],
                    "para": curr["timestamp"],
                    "candidato": cand,
                    "votos_antes": v_prev,
                    "votos_depois": v_curr,
                    "diferenca": v_prev - v_curr,
                })

    # Timeline summary
    timeline = []
    for c in capturas:
        entry = {
            "ts": c["timestamp"],
            "pct": c["pct_totalizado"],
            "votos": c["votos_total"],
        }
        for cand_nr, cand_votos in c["votos"].items():
            entry[f"v{cand_nr}"] = cand_votos
        timeline.append(entry)

    return {
        "teste": "G1",
        "ano": ano,
        "turno": turno_label,
        "capturas": len(capturas),
        "primeira": capturas[0]["timestamp"],
        "ultima": capturas[-1]["timestamp"],
        "pct_primeira": capturas[0]["pct_totalizado"],
        "pct_ultima": capturas[-1]["pct_totalizado"],
        "violacoes_secoes": len(violacoes_secoes),
        "violacoes_votos": len(violacoes_votos),
        "detalhes_violacoes_secoes": violacoes_secoes[:5],
        "detalhes_violacoes_votos": violacoes_votos[:5],
        "timeline": timeline,
        "impacto_votos": f"{sum(v.get('diferenca',0) for v in violacoes_votos)} votos regrediram durante a totalização." if violacoes_votos else "Zero votos regrediram — totalização estritamente crescente."
    }


def teste_G2_final_vs_oficial(u, ano, turno_label):
    """Compara última captura da divulgação com o resultado oficial (BU)."""
    pattern = f"{ano}_{turno_label}_*"
    arquivos = sorted(CAPT.glob(pattern))

    # Last capture
    capturas = []
    for a in sorted(CAPT.glob(pattern)):
        try:
            capturas.append(_parse_captura(a))
        except:
            pass

    if not capturas:
        return {"teste": "G2", "ano": ano, "resultado": "sem capturas válidas"}

    capturas.sort(key=lambda x: x["timestamp"])
    ultima = capturas[-1]

    # Official totals from BU
    oficial_v13 = int(u["bu_v13"].sum())
    oficial_v22 = int(u["bu_v22"].sum())
    oficial_total = int(u["bu_comparecimento"].sum())

    div_v13 = ultima["votos"].get("13", 0)
    div_v22 = ultima["votos"].get("22", 0)

    diff_13 = div_v13 - oficial_v13
    diff_22 = div_v22 - oficial_v22

    return {
        "teste": "G2",
        "ano": ano,
        "turno": turno_label,
        "ultima_captura": ultima["timestamp"],
        "pct_totalizado": ultima["pct_totalizado"],
        "divulgacao_v13": div_v13,
        "oficial_bu_v13": oficial_v13,
        "diff_v13": diff_13,
        "divulgacao_v22": div_v22,
        "oficial_bu_v22": oficial_v22,
        "diff_v22": diff_22,
        "divulgacao_total": ultima["votos_total"],
        "oficial_total": oficial_total,
        "impacto_votos": f"Diferença entre divulgação ({ultima['pct_totalizado']}%) e BU oficial: cand 13 = {diff_13:+d}, cand 22 = {diff_22:+d}. Se a última captura não é 100%, a diferença são seções não totalizadas até aquele momento."
    }


def teste_G3_share_monotonia(ano, turno_label):
    """Verifica se a fatia (%) de cada candidato oscila além do esperado."""
    pattern = f"{ano}_{turno_label}_*"
    arquivos = sorted(CAPT.glob(pattern))

    capturas = []
    for a in sorted(CAPT.glob(pattern)):
        try:
            capturas.append(_parse_captura(a))
        except:
            pass

    if len(capturas) < 3:
        return {"teste": "G3", "ano": ano, "resultado": f"apenas {len(capturas)} capturas válidas"}

    capturas.sort(key=lambda x: x["timestamp"])

    # Track share of each candidate over time
    shares = []
    for c in capturas:
        total = sum(c["votos"].values()) or 1
        entry = {"ts": c["timestamp"], "pct_total": c["pct_totalizado"]}
        for cand, v in c["votos"].items():
            entry[f"share_{cand}"] = round(v / total * 100, 4)
        shares.append(entry)

    # Compute max swing between consecutive captures
    swings = {}
    for i in range(1, len(shares)):
        for k in shares[i]:
            if k.startswith("share_"):
                prev = shares[i-1].get(k, 0)
                curr = shares[i][k]
                swing = abs(curr - prev)
                if k not in swings or swing > swings[k]["max_swing"]:
                    swings[k] = {
                        "max_swing": round(swing, 4),
                        "de": shares[i-1]["ts"],
                        "para": shares[i]["ts"],
                        "pct_de": shares[i-1]["pct_total"],
                        "pct_para": shares[i]["pct_total"],
                    }

    return {
        "teste": "G3",
        "ano": ano,
        "turno": turno_label,
        "capturas": len(capturas),
        "shares": shares,
        "max_swings": swings,
        "impacto_votos": "Oscilações na fatia são normais durante a totalização (seções de diferentes regiões entram em blocos). Swing > 2pp entre capturas consecutivas com > 50% totalizado seria preocupante."
    }


# ── MAIN ─────────────────────────────────────────────────────────────────

def rodar(ano):
    turno = "2t"
    turno_label = "2T"

    print(f"\n{'='*60}")
    print(f" PROVA PROFUNDA 2 — {ano}")
    print(f"{'='*60}")

    u, pf = carregar(ano, turno)
    print(f"  Urnas: {len(u):,}  |  Perfil: {len(pf) if pf is not None else 0:,}")

    resultados = {}

    # E: Demographics
    print("  [E1] Correlação parcial controlando demografia...")
    resultados["E1"] = teste_E1_correlacao_parcial(u.copy(), pf.copy() if pf is not None else None, ano)
    print(f"       r_simples={resultados['E1'].get('r_simples_intra_mun')}  r_parcial={resultados['E1'].get('r_parcial_controlando_demo')}")

    print("  [E2] Regressão completa...")
    resultados["E2"] = teste_E2_regressao_completa(u.copy(), pf.copy() if pf is not None else None, ano)
    print(f"       R²={resultados['E2'].get('r2_completo')}")

    print("  [E3] Correlação estratificada...")
    resultados["E3"] = teste_E3_estratificado(u.copy(), pf.copy() if pf is not None else None, ano)
    n_strats = len(resultados["E3"].get("estratos", {}))
    print(f"       {n_strats} estratos analisados")

    # F: bweb
    print("  [F1] bweb CSV × parquet...")
    resultados["F1"] = teste_F1_bweb_vs_parquet(u.copy(), ano)
    print(f"       divergentes v13={resultados['F1'].get('divergentes_v13')}  v22={resultados['F1'].get('divergentes_v22')}")

    # G: Divulgação ao vivo
    print("  [G1] Monotonia da divulgação...")
    resultados["G1"] = teste_G1_monotonia(ano, turno_label)
    print(f"       violações seções={resultados['G1'].get('violacoes_secoes')}  votos={resultados['G1'].get('violacoes_votos')}")

    print("  [G2] Final da divulgação × oficial...")
    resultados["G2"] = teste_G2_final_vs_oficial(u.copy(), ano, turno_label)
    print(f"       diff v13={resultados['G2'].get('diff_v13')}  diff v22={resultados['G2'].get('diff_v22')}")

    print("  [G3] Oscilação da fatia durante totalização...")
    resultados["G3"] = teste_G3_share_monotonia(ano, turno_label)
    print(f"       capturas={resultados['G3'].get('capturas')}")

    # Save
    out = BASE / "estresse_estatistico" / "resultados" / f"resultado_profunda2_{ano}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n  Salvo em {out}")

    return resultados


if __name__ == "__main__":
    r2026 = rodar(2026)
    r2022 = rodar(2022)

    # Summary
    print("\n" + "="*60)
    print(" RESUMO")
    print("="*60)

    for ano, r in [(2026, r2026), (2022, r2022)]:
        e1 = r.get("E1", {})
        print(f"\n  {ano}:")
        print(f"    E1: r_simples={e1.get('r_simples_intra_mun')}  →  r_parcial(demo)={e1.get('r_parcial_controlando_demo')}  redução={e1.get('reducao_pct')}%")
        f1 = r.get("F1", {})
        print(f"    F1: {f1.get('divergentes_v13',0)} divergências v13, {f1.get('divergentes_v22',0)} v22, total {f1.get('total_votos_divergentes',0)} votos")
        g1 = r.get("G1", {})
        print(f"    G1: {g1.get('violacoes_votos',0)} violações de monotonia")
