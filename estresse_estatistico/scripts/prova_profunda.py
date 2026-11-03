"""Prova Profunda: testes que vão direto nos dados brutos das urnas.

Não usa os parquets de seção (dados_leves/secoes_*.parquet).
Usa os dados extraídos dos arquivos brutos: urnas_*.parquet (78 colunas por urna
com logs, RDV, hashes, timestamps, duração de votos, habilitação) e
votos_por_minuto_*.parquet (curva temporal minuto a minuto).

Premissa: se os dados foram fabricados, o fabricante precisaria simular:
- o tempo que cada eleitor leva pra votar (distribuição de durações)
- a sequência de habilitações biométricas/manuais ao longo do dia
- o ritmo de votação minuto a minuto com a forma real (pico-platô-cauda)
- a correlação entre modelo de urna e performance
- a assinatura criptográfica de cada arquivo

Estes testes examinam essas camadas, não os totais.

Uso: python -u prova_profunda.py [2026|2022]
"""
import json, os, sys, warnings
import numpy as np
import pandas as pd
from scipy import stats
warnings.filterwarnings("ignore", category=RuntimeWarning)
pr = lambda *a, **kw: print(*a, **kw, flush=True)

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ANO = sys.argv[1] if len(sys.argv) > 1 else "2026"
rng = np.random.default_rng(42)
pr(f"=== Prova Profunda — {ANO} ===")
pr("Dados: urnas extraídas dos brutos + votos por minuto\n")

# ---------- Carregar dados das urnas (extraídos dos brutos) ----------
u = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/urnas_{ANO}_2t.parquet"))
u = u[u["SG_UF"] != "ZZ"].copy()
pr(f"  {len(u)} urnas carregadas (2t)")

u1 = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/urnas_{ANO}_1t.parquet"))
u1 = u1[u1["SG_UF"] != "ZZ"].copy()
pr(f"  {len(u1)} urnas carregadas (1t)")

vpm = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/votos_por_minuto_{ANO}_2t.parquet"))
pr(f"  {len(vpm)} registros votos/minuto (2t)")

R = {"ano": ANO, "premissa": "dados brutos sob prova"}

# ============================================================
# D1: DURAÇÃO DO VOTO — distribuição por urna
# Se fabricado, a distribuição de durações seria artificialmente regular.
# No real: log-normal com cauda pesada (eleitores que corrigem, idosos, etc.)
# ============================================================
pr("--- D1: Distribuição de durações do voto ---")
d = u[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO",
       "seq_dur_mediana", "seq_dur_min", "seq_dur_p01", "seq_dur_abaixo_5s",
       "bu_comparecimento", "bu_v13", "bu_v22", "bu_aptos"]].dropna()
d = d[d["bu_comparecimento"] >= 20]

# D1a: Distribuição da mediana de duração entre urnas
med_arr = d["seq_dur_mediana"].values
med_arr = med_arr[np.isfinite(med_arr) & (med_arr > 0)]
# Teste: se fabricado, seria muito concentrada (CV baixo)
cv_dur = float(np.std(med_arr) / np.mean(med_arr))
# Teste de normalidade do log (log-normal = comportamento humano)
log_med = np.log(med_arr[med_arr > 0])
shapiro_stat, shapiro_p = stats.shapiro(rng.choice(log_med, min(5000, len(log_med)), replace=False))
R["D1a"] = {
    "media_mediana_s": round(float(np.mean(med_arr)), 2),
    "dp_mediana_s": round(float(np.std(med_arr)), 2),
    "cv": round(cv_dur, 4),
    "p01_s": round(float(np.percentile(med_arr, 1)), 1),
    "p99_s": round(float(np.percentile(med_arr, 99)), 1),
    "log_shapiro_stat": round(float(shapiro_stat), 4),
    "log_shapiro_p": round(float(shapiro_p), 6),
    "n": len(med_arr),
}
pr(f"  Mediana de duração: média={np.mean(med_arr):.1f}s, CV={cv_dur:.4f}")
pr(f"  Log-normalidade (Shapiro): stat={shapiro_stat:.4f}, p={shapiro_p:.6f}")

# D1b: Votos abaixo de 5 segundos — se fabricado, zero ou todos
frac_rapido = d["seq_dur_abaixo_5s"] / d["bu_comparecimento"].clip(lower=1)
R["D1b"] = {
    "frac_media": round(float(frac_rapido.mean()), 4),
    "frac_p50": round(float(frac_rapido.median()), 4),
    "frac_p99": round(float(frac_rapido.quantile(0.99)), 4),
    "urnas_com_zero_rapidos": int((frac_rapido == 0).sum()),
    "frac_urnas_zero": round(float((frac_rapido == 0).sum() / len(frac_rapido)), 4),
}
pr(f"  Votos <5s: média={frac_rapido.mean():.4f}, urnas com zero={int((frac_rapido == 0).sum())} ({100*(frac_rapido == 0).sum()/len(frac_rapido):.1f}%)")

# D1c: Duração vs resultado — a duração do voto deveria ser independente do resultado
d["p13"] = d["bu_v13"] / (d["bu_v13"] + d["bu_v22"]).clip(lower=1)
d["mun"] = d["SG_UF"] + d["CD_MUNICIPIO"]
d["r_p13"] = d["p13"] - d.groupby("mun")["p13"].transform("mean")
d["r_dur"] = d["seq_dur_mediana"] - d.groupby("mun")["seq_dur_mediana"].transform("mean")
corr_dur_voto = float(np.corrcoef(d["r_p13"].values, d["r_dur"].values)[0, 1])
# Se fabricado, duração e voto seriam independentes (r≈0). No real, pode haver correlação
# porque regiões com perfil diferente votam em ritmos diferentes.
R["D1c"] = {
    "corr_duracao_vs_p13": round(corr_dur_voto, 6),
    "n": len(d),
}
pr(f"  corr(resíduo_duração, resíduo_p13) = {corr_dur_voto:.6f}")

# ============================================================
# D2: HABILITAÇÃO BIOMÉTRICA — padrão ao longo do dia
# Se fabricado, a taxa de habilitação sem biometria seria constante ou aleatória.
# No real: cresce no fim do dia (eleitores que não conseguem na biometria voltam).
# ============================================================
pr("\n--- D2: Padrão de habilitação biométrica ---")
d2_cols_base = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "bu_comparecimento", "bu_v13", "bu_v22"]
d2_cols_opt = ["bu_hab_biometrica", "bu_hab_sem_biometria", "bu_hab_biografica",
               "seq_hab_biometrica", "seq_hab_manual", "seq_hab_mesario",
               "seq_ult30_votos", "seq_ult30_sem_biometria",
               "seq_resto_votos", "seq_resto_sem_biometria"]
d2_cols = d2_cols_base + [c for c in d2_cols_opt if c in u.columns]
d2 = u[d2_cols].dropna()
d2 = d2[d2["bu_comparecimento"] >= 20]

# D2a: Taxa de sem-biometria nos últimos 30 votos vs no resto
if "seq_ult30_votos" in d2.columns and "seq_ult30_sem_biometria" in d2.columns:
    d2["frac_bio_ult30"] = d2["seq_ult30_sem_biometria"] / d2["seq_ult30_votos"].clip(lower=1)
    d2["frac_bio_resto"] = d2["seq_resto_sem_biometria"] / d2["seq_resto_votos"].clip(lower=1)
    d2_valid = d2[(d2["seq_ult30_votos"] >= 10) & (d2["seq_resto_votos"] >= 10)]
    diff_bio = d2_valid["frac_bio_ult30"] - d2_valid["frac_bio_resto"]
    t_stat, p_bio = stats.ttest_1samp(diff_bio.values, 0)
    R["D2a"] = {
        "diff_media": round(float(diff_bio.mean()), 4),
        "diff_mediana": round(float(diff_bio.median()), 4),
        "t_stat": round(float(t_stat), 2),
        "p": round(float(p_bio), 6),
        "n": len(d2_valid),
        "frac_ult30_media": round(float(d2_valid["frac_bio_ult30"].mean()), 4),
        "frac_resto_media": round(float(d2_valid["frac_bio_resto"].mean()), 4),
    }
    pr(f"  Sem-bio últimos 30: {d2_valid['frac_bio_ult30'].mean():.4f} vs resto: {d2_valid['frac_bio_resto'].mean():.4f}")
    pr(f"  Diferença: {diff_bio.mean():.4f}, t={t_stat:.2f}, p={p_bio:.6f}")
else:
    R["D2a"] = {"nota": "Colunas de sequência não disponíveis para este ano"}
    pr("  Colunas de últimos-30 não disponíveis")

# D2b: Sem-biometria vs resultado — correlação intra-municipal
if "bu_hab_sem_biometria" in d2.columns:
    d2["p13"] = d2["bu_v13"] / (d2["bu_v13"] + d2["bu_v22"]).clip(lower=1)
    d2["frac_sem_bio"] = d2["bu_hab_sem_biometria"] / d2["bu_comparecimento"].clip(lower=1)
    d2["mun"] = d2["SG_UF"] + d2["CD_MUNICIPIO"]
    d2["r_p13"] = d2["p13"] - d2.groupby("mun")["p13"].transform("mean")
    d2["r_bio"] = d2["frac_sem_bio"] - d2.groupby("mun")["frac_sem_bio"].transform("mean")
    corr_bio = float(np.corrcoef(d2["r_p13"].values, d2["r_bio"].values)[0, 1])
    R["D2b"] = {"corr_sem_bio_vs_p13": round(corr_bio, 6), "n": len(d2)}
    pr(f"  corr(resíduo_sem_bio, resíduo_p13) = {corr_bio:.6f}")
else:
    d2["p13"] = d2["bu_v13"] / (d2["bu_v13"] + d2["bu_v22"]).clip(lower=1)
    R["D2b"] = {"nota": "Coluna bu_hab_sem_biometria não disponível"}
    pr("  Coluna bu_hab_sem_biometria não disponível")

# ============================================================
# D3: CURVA TEMPORAL — ritmo de votação minuto a minuto
# Se fabricado, o ritmo seria uniforme ou com forma simples.
# No real: abertura 8h, pico ~10h, platô até ~14h, cauda até ~17h+
# ============================================================
pr("\n--- D3: Curva temporal de votação ---")
vpm["ts"] = pd.to_datetime(vpm["minuto"], format="%d/%m/%Y %H:%M", errors="coerce")
vpm = vpm.dropna(subset=["ts"])
vpm["hora"] = vpm["ts"].dt.hour + vpm["ts"].dt.minute / 60

# D3a: Forma da curva — simetria e curtose
hora_votos = vpm.groupby(vpm["hora"].round(2))["votos"].sum()
# Distribuição ponderada das horas
horas_expandidas = np.repeat(hora_votos.index.values, hora_votos.values.astype(int))
skew_hora = float(stats.skew(horas_expandidas))
kurt_hora = float(stats.kurtosis(horas_expandidas))
R["D3a"] = {
    "skewness": round(skew_hora, 4),
    "curtose": round(kurt_hora, 4),
    "hora_pico": round(float(hora_votos.idxmax()), 2),
    "total_votos": int(vpm["votos"].sum()),
}
pr(f"  Skewness={skew_hora:.4f}, Curtose={kurt_hora:.4f}, Hora pico={hora_votos.idxmax():.1f}h")

# D3b: Variabilidade entre municípios — cada município tem sua curva
# Se fabricado a partir de uma fórmula, as curvas seriam muito parecidas
vpm["mun"] = vpm["SG_UF"] + vpm["CD_MUNICIPIO"]
mun_curvas = vpm.groupby(["mun", vpm["hora"].round(0).astype(int)])["votos"].sum().unstack(fill_value=0)
# Normalizar cada município pela soma
mun_norm = mun_curvas.div(mun_curvas.sum(axis=1), axis=0)
mun_norm = mun_norm.loc[:, 6:18]  # só horário de votação
# CV entre municípios por hora
cv_por_hora = mun_norm.std() / mun_norm.mean()
R["D3b"] = {
    "cv_medio_entre_mun": round(float(cv_por_hora.mean()), 4),
    "cv_min": round(float(cv_por_hora.min()), 4),
    "cv_max": round(float(cv_por_hora.max()), 4),
    "n_mun": len(mun_norm),
}
pr(f"  CV entre municípios por hora: média={cv_por_hora.mean():.4f}, min={cv_por_hora.min():.4f}, max={cv_por_hora.max():.4f}")

# D3c: Autocorrelação da curva — suavidade minuto a minuto
# Dados reais: alta autocorrelação (o minuto 10:01 é parecido com 10:02)
# Dados fabricados por amostragem: autocorrelação pode ser muito alta (cópia) ou muito baixa (ruído)
nacional = vpm.groupby(vpm["ts"].dt.floor("min"))["votos"].sum().sort_index()
ac1 = float(nacional.autocorr(1))
ac5 = float(nacional.autocorr(5))
ac30 = float(nacional.autocorr(30))
R["D3c"] = {
    "autocorr_1min": round(ac1, 4),
    "autocorr_5min": round(ac5, 4),
    "autocorr_30min": round(ac30, 4),
}
pr(f"  Autocorrelação: 1min={ac1:.4f}, 5min={ac5:.4f}, 30min={ac30:.4f}")

# ============================================================
# D4: MODELO DE URNA — performance por modelo
# Se fabricado, não haveria diferença real entre modelos.
# No real: urnas mais antigas são mais lentas.
# ============================================================
pr("\n--- D4: Performance por modelo de urna ---")
d4 = u[["modelo", "seq_dur_mediana", "bu_comparecimento", "bu_v13", "bu_v22", "SG_UF", "CD_MUNICIPIO"]].dropna()
d4 = d4[(d4["bu_comparecimento"] >= 20) & (d4["seq_dur_mediana"] > 0)]
d4["mun"] = d4["SG_UF"] + d4["CD_MUNICIPIO"]
d4["p13"] = d4["bu_v13"] / (d4["bu_v13"] + d4["bu_v22"]).clip(lower=1)

# D4a: Duração mediana por modelo
por_modelo = d4.groupby("modelo").agg(
    n=("seq_dur_mediana", "size"),
    dur_med=("seq_dur_mediana", "median"),
    dur_p25=("seq_dur_mediana", lambda x: x.quantile(0.25)),
    dur_p75=("seq_dur_mediana", lambda x: x.quantile(0.75)),
).reset_index()
por_modelo = por_modelo[por_modelo["n"] >= 100]
R["D4a"] = {
    "modelos": por_modelo.to_dict(orient="records"),
    "n_modelos": len(por_modelo),
    "kruskal_H": None, "kruskal_p": None,
}
groups = [g["seq_dur_mediana"].values for _, g in d4.groupby("modelo") if len(g) >= 100]
if len(groups) >= 2:
    H, p_kruskal = stats.kruskal(*groups)
    R["D4a"]["kruskal_H"] = round(float(H), 2)
    R["D4a"]["kruskal_p"] = round(float(p_kruskal), 6)
    pr(f"  Kruskal-Wallis entre modelos: H={H:.2f}, p={p_kruskal:.6f}")
for _, r_m in por_modelo.iterrows():
    pr(f"    {r_m['modelo']}: n={int(r_m['n'])}, mediana={r_m['dur_med']:.1f}s")

# D4b: Modelo vs resultado, controlando por município
# Se fabricado, não haveria diferença. No real, modelos mais antigos estão em regiões específicas.
d4["r_p13"] = d4["p13"] - d4.groupby("mun")["p13"].transform("mean")
d4["r_dur"] = d4["seq_dur_mediana"] - d4.groupby("mun")["seq_dur_mediana"].transform("mean")
# ANOVA do resíduo do resultado por modelo
groups_r = [g["r_p13"].values for _, g in d4.groupby("modelo") if len(g) >= 100]
if len(groups_r) >= 2:
    F_anova, p_anova = stats.f_oneway(*groups_r)
    R["D4b"] = {"F": round(float(F_anova), 2), "p": round(float(p_anova), 6), "n": len(d4)}
    pr(f"  ANOVA resíduo p13 por modelo: F={F_anova:.2f}, p={p_anova:.6f}")

# ============================================================
# D5: INTEGRIDADE CRIPTOGRÁFICA — hashes e assinaturas
# Se os dados foram alterados DEPOIS da urna, os hashes e assinaturas falhariam.
# ============================================================
pr("\n--- D5: Integridade criptográfica ---")
hash_cols = ["hash_ok_bu", "assin_ok_bu", "hash_ok_rdv", "assin_ok_rdv",
             "hash_ok_imgbu", "assin_ok_imgbu", "hash_ok_log", "assin_ok_log"]
d5 = {}
for col in hash_cols:
    if col in u.columns:
        vals = u[col].dropna()
        ok = (vals == True).sum()
        fail = (vals == False).sum()
        na = u[col].isna().sum()
        d5[col] = {"ok": int(ok), "fail": int(fail), "na": int(na), "total": len(u)}
        if fail > 0:
            pr(f"  {col}: {ok} OK, {fail} FALHA, {na} N/A")
        else:
            pr(f"  {col}: {ok} OK, {na} N/A")

# D5a: Taxa de falha criptográfica
total_checks = sum(v["ok"] + v["fail"] for v in d5.values())
total_fail = sum(v["fail"] for v in d5.values())
R["D5"] = {
    "detalhes": d5,
    "total_checks": total_checks,
    "total_fail": total_fail,
    "taxa_falha": round(total_fail / total_checks, 8) if total_checks > 0 else 0,
}
pr(f"  Total: {total_checks} verificações, {total_fail} falhas ({100*total_fail/total_checks:.6f}%)")

# ============================================================
# D6: CONSISTÊNCIA INTERNA — BU vs RDV vs IMG vs LOG
# Três fontes independentes do mesmo dado. Se fabricado, precisa manter as três.
# ============================================================
pr("\n--- D6: Consistência BU × RDV × IMG × LOG ---")
d6 = u[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO",
        "bu_v13", "rdv_v13", "img_v13",
        "bu_v22", "rdv_v22", "img_v22",
        "bu_comparecimento", "img_comparecimento",
        "computado", "conf_presidente", "bu_aptos"]].dropna()

# BU vs RDV
diff_rdv = d6[d6["bu_v13"] != d6["rdv_v13"]]
# BU vs IMG
diff_img = d6[d6["bu_v13"] != d6["img_v13"]]
# Comparecimento: computado no log vs BU
d6c = u[["bu_comparecimento", "computado"]].dropna()
d6c = d6c[d6c["bu_comparecimento"] > 0]
diff_comp = d6c[d6c["bu_comparecimento"] != d6c["computado"]]

R["D6"] = {
    "bu_vs_rdv_v13_diff": len(diff_rdv),
    "bu_vs_img_v13_diff": len(diff_img),
    "bu_vs_log_comp_diff": len(diff_comp),
    "total_urnas": len(d6),
    "total_log": len(d6c),
}
pr(f"  BU vs RDV (v13): {len(diff_rdv)} diferenças de {len(d6)} urnas")
pr(f"  BU vs IMG (v13): {len(diff_img)} diferenças de {len(d6)} urnas")
pr(f"  BU vs LOG (comparecimento): {len(diff_comp)} diferenças de {len(d6c)} urnas")

# ============================================================
# D7: SEQUÊNCIA DE VOTOS — padrões no RDV
# O RDV tem a sequência de votos individuais. Se fabricado, pode ter padrões.
# ============================================================
pr("\n--- D7: Anomalias na sequência de votos ---")

# D7a: Votos fora do dia da eleição
d7 = u[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO",
        "seq_votos_dia", "seq_votos_fora_dia", "seq_votos_antes_7h",
        "seq_sem_habilitacao", "bu_comparecimento"]].dropna()
fora_dia = d7[d7["seq_votos_fora_dia"] > 0]
antes_7h = d7[d7["seq_votos_antes_7h"] > 0]
sem_hab = d7[d7["seq_sem_habilitacao"] > 0]
R["D7a"] = {
    "urnas_voto_fora_dia": len(fora_dia),
    "votos_fora_dia_total": int(d7["seq_votos_fora_dia"].sum()),
    "urnas_antes_7h": len(antes_7h),
    "votos_antes_7h_total": int(d7["seq_votos_antes_7h"].sum()),
    "urnas_sem_habilitacao": len(sem_hab),
    "votos_sem_hab_total": int(d7["seq_sem_habilitacao"].sum()),
    "total_urnas": len(d7),
}
pr(f"  Votos fora do dia: {len(fora_dia)} urnas, {int(d7['seq_votos_fora_dia'].sum())} votos")
pr(f"  Votos antes das 7h: {len(antes_7h)} urnas, {int(d7['seq_votos_antes_7h'].sum())} votos")
pr(f"  Votos sem habilitação: {len(sem_hab)} urnas, {int(d7['seq_sem_habilitacao'].sum())} votos")

# D7b: Intervalo mínimo entre votos — se fabricado, pode ser impossível
d7b = u[["seq_intervalo_min", "bu_comparecimento", "modelo"]].dropna()
d7b = d7b[d7b["bu_comparecimento"] >= 20]
d7b = d7b[d7b["seq_intervalo_min"] > 0]
impossivel = d7b[d7b["seq_intervalo_min"] < 3]  # <3s entre dois votos = fisicamente impossível
R["D7b"] = {
    "urnas_intervalo_lt3s": len(impossivel),
    "frac": round(len(impossivel) / len(d7b), 6) if len(d7b) > 0 else 0,
    "intervalo_min_p01": round(float(d7b["seq_intervalo_min"].quantile(0.01)), 1),
    "intervalo_min_p05": round(float(d7b["seq_intervalo_min"].quantile(0.05)), 1),
    "intervalo_min_mediana": round(float(d7b["seq_intervalo_min"].median()), 1),
}
pr(f"  Intervalo mínimo <3s: {len(impossivel)} urnas ({100*len(impossivel)/len(d7b):.4f}%)")
pr(f"  Intervalo mín: p01={d7b['seq_intervalo_min'].quantile(0.01):.1f}s, mediana={d7b['seq_intervalo_min'].median():.1f}s")

# ============================================================
# D8: COMPARAÇÃO 1T vs 2T — mesma urna, dois turnos
# Se fabricado num turno só, o outro turno não casa.
# ============================================================
pr("\n--- D8: Consistência 1T vs 2T (mesma urna) ---")
u1["chave"] = u1["SG_UF"] + "_" + u1["CD_MUNICIPIO"] + "_" + u1["NR_ZONA"] + "_" + u1["NR_SECAO"]
u["chave"] = u["SG_UF"] + "_" + u["CD_MUNICIPIO"] + "_" + u["NR_ZONA"] + "_" + u["NR_SECAO"]

m = u[["chave", "seq_dur_mediana", "bu_comparecimento", "bu_v13", "bu_v22",
       "seq_hab_biometrica", "seq_hab_manual", "modelo"]].merge(
    u1[["chave", "seq_dur_mediana", "bu_comparecimento",
        "seq_hab_biometrica", "seq_hab_manual", "modelo"]],
    on="chave", suffixes=("_2t", "_1t"))

m = m[(m["bu_comparecimento_2t"] >= 20) & (m["bu_comparecimento_1t"] >= 20)]

# D8a: Correlação de duração mediana entre turnos
corr_dur = float(np.corrcoef(
    m["seq_dur_mediana_2t"].values,
    m["seq_dur_mediana_1t"].values
)[0, 1])
R["D8a"] = {
    "corr_duracao_1t_2t": round(corr_dur, 4),
    "n": len(m),
}
pr(f"  corr(duração_1t, duração_2t) = {corr_dur:.4f} (n={len(m)})")

# D8b: Mesma urna vs urna diferente entre turnos — performance
m["mesma_urna"] = m["modelo_2t"] == m["modelo_1t"]
m["delta_dur"] = m["seq_dur_mediana_2t"] - m["seq_dur_mediana_1t"]
if m["mesma_urna"].sum() > 100 and (~m["mesma_urna"]).sum() > 100:
    mesma = m[m["mesma_urna"]]["delta_dur"]
    diff = m[~m["mesma_urna"]]["delta_dur"]
    t_mod, p_mod = stats.mannwhitneyu(mesma.values, diff.values, alternative="two-sided")
    R["D8b"] = {
        "mesma_modelo_delta_dur_med": round(float(mesma.median()), 2),
        "diff_modelo_delta_dur_med": round(float(diff.median()), 2),
        "U": float(t_mod), "p": round(float(p_mod), 6),
        "n_mesma": len(mesma), "n_diff": len(diff),
    }
    pr(f"  Mesmo modelo: Δdur_med={mesma.median():.2f}s; Diff modelo: Δdur_med={diff.median():.2f}s, p={p_mod:.6f}")

# D8c: Correlação da taxa de bio entre turnos
m["bio1"] = m["seq_hab_biometrica_1t"] / m["bu_comparecimento_1t"].clip(lower=1)
m["bio2"] = m["seq_hab_biometrica_2t"] / m["bu_comparecimento_2t"].clip(lower=1)
corr_bio_turnos = float(np.corrcoef(m["bio1"].values, m["bio2"].values)[0, 1])
R["D8c"] = {"corr_bio_1t_2t": round(corr_bio_turnos, 4), "n": len(m)}
pr(f"  corr(bio_1t, bio_2t) = {corr_bio_turnos:.4f}")

# ============================================================
# D9: VERIFICAÇÃO DE SOFTWARE — integridade do código na urna
# ============================================================
pr("\n--- D9: Verificação de software ---")
d9 = u[["sw_verif_ok", "sw_verif_falha", "sw_versoes"]].dropna()
d9 = d9[d9["sw_verif_ok"] > 0]
sw_falha = d9[d9["sw_verif_falha"] > 0]
versoes = u["sw_versoes"].dropna().value_counts()
R["D9"] = {
    "urnas_com_verif": len(d9),
    "urnas_com_falha_sw": len(sw_falha),
    "frac_falha": round(len(sw_falha) / len(d9), 6) if len(d9) > 0 else 0,
    "versoes": versoes.head(10).to_dict(),
}
pr(f"  Verificação de SW: {len(d9)} urnas verificadas, {len(sw_falha)} com falha ({100*len(sw_falha)/len(d9):.4f}%)")
pr(f"  Versões: {dict(versoes.head(5))}")

# ============================================================
# D10: ENTROPIA DA DISTRIBUIÇÃO DE VOTOS POR MUNICÍPIO
# Se fabricado com fórmula proporcional, a entropia dentro do município seria
# anomalamente baixa (todos os votos seguem a mesma proporção).
# No real: variância natural entre seções.
# ============================================================
pr("\n--- D10: Entropia da distribuição intra-municipal ---")
d10 = u[["SG_UF", "CD_MUNICIPIO", "bu_v13", "bu_v22", "bu_comparecimento"]].dropna()
d10 = d10[d10["bu_comparecimento"] >= 20]
d10["mun"] = d10["SG_UF"] + d10["CD_MUNICIPIO"]
d10["p13"] = d10["bu_v13"] / (d10["bu_v13"] + d10["bu_v22"]).clip(lower=1)

entropias = []
for mun, g in d10.groupby("mun"):
    if len(g) < 10: continue
    p = g["p13"].values
    # discretizar em bins de 0.01
    bins = np.histogram(p, bins=np.arange(0, 1.01, 0.01))[0]
    bins = bins[bins > 0]
    probs = bins / bins.sum()
    ent = float(-np.sum(probs * np.log2(probs)))
    entropias.append(ent)

ea = np.array(entropias)
R["D10"] = {
    "entropia_media": round(float(ea.mean()), 4),
    "entropia_mediana": round(float(np.median(ea)), 4),
    "entropia_p05": round(float(np.percentile(ea, 5)), 4),
    "entropia_p95": round(float(np.percentile(ea, 95)), 4),
    "n_mun": len(ea),
}
pr(f"  Entropia: média={ea.mean():.4f}, mediana={np.median(ea):.4f}, p5={np.percentile(ea,5):.4f}")

# Salvar
out = os.path.join(AQUI, "..", "resultados", f"resultado_prova_profunda_{ANO}.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(R, open(out, "w"), ensure_ascii=False, indent=1, default=str)
pr(f"\nSalvo em {out}")
pr("=== Fim Prova Profunda ===")
