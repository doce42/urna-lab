"""Investigação dos achados da Prova Profunda.

Cada achado é investigado para separar artefato de anomalia real.
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
pr(f"=== Investigação dos Achados — {ANO} ===\n")

u = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/urnas_{ANO}_2t.parquet"))
u = u[u["SG_UF"] != "ZZ"].copy()
u["mun"] = u["SG_UF"] + u["CD_MUNICIPIO"]

R = {"ano": ANO}

# ============================================================
# ACHADO 1: Duração do voto correlaciona com resultado (r=0.10/0.16)
# Hipótese nula: eleitores de regiões diferentes votam em ritmos diferentes
# por causa da demografia (idade, escolaridade), não por fabricação.
# ============================================================
pr("=== ACHADO 1: Duração × Resultado ===")
d = u[["mun", "SG_UF", "seq_dur_mediana", "bu_comparecimento", "bu_v13", "bu_v22", "bu_aptos", "modelo"]].dropna()
d = d[(d["bu_comparecimento"] >= 20) & (d["seq_dur_mediana"] > 0)]
d["p13"] = d["bu_v13"] / (d["bu_v13"] + d["bu_v22"]).clip(lower=1)

# 1a: A correlação persiste dentro do município?
d["r_p13"] = d["p13"] - d.groupby("mun")["p13"].transform("mean")
d["r_dur"] = d["seq_dur_mediana"] - d.groupby("mun")["seq_dur_mediana"].transform("mean")
corr_intra = float(np.corrcoef(d["r_p13"].values, d["r_dur"].values)[0, 1])
pr(f"  Correlação intra-municipal: {corr_intra:.6f}")

# 1b: A correlação persiste controlando por modelo de urna?
d["r_dur_mod"] = d["seq_dur_mediana"] - d.groupby(["mun", "modelo"])["seq_dur_mediana"].transform("mean")
d["r_p13_mod"] = d["p13"] - d.groupby(["mun", "modelo"])["p13"].transform("mean")
mask = d.groupby(["mun", "modelo"])["bu_comparecimento"].transform("size") >= 5
d_mod = d[mask]
corr_mod = float(np.corrcoef(d_mod["r_p13_mod"].values, d_mod["r_dur_mod"].values)[0, 1])
pr(f"  Controlando por município+modelo: {corr_mod:.6f}")

# 1c: Separar por UF — a correlação é universal ou concentrada?
corr_uf = {}
for uf, g in d.groupby("SG_UF"):
    if len(g) < 100: continue
    rp = g["p13"] - g.groupby("mun")["p13"].transform("mean")
    rd = g["seq_dur_mediana"] - g.groupby("mun")["seq_dur_mediana"].transform("mean")
    c = float(np.corrcoef(rp.values, rd.values)[0, 1])
    corr_uf[uf] = round(c, 4)

# Top 5 mais fortes e 5 mais fracos
sorted_uf = sorted(corr_uf.items(), key=lambda x: abs(x[1]), reverse=True)
pr(f"  Top 5 UFs por |corr|: {sorted_uf[:5]}")
pr(f"  Bottom 5 UFs por |corr|: {sorted_uf[-5:]}")

# 1d: A correlação existe no 1º turno? (mesma urna, candidatos diferentes)
u1 = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/urnas_{ANO}_1t.parquet"))
u1 = u1[u1["SG_UF"] != "ZZ"].copy()
u1["mun"] = u1["SG_UF"] + u1["CD_MUNICIPIO"]
d1t = u1[["mun", "seq_dur_mediana", "bu_comparecimento", "bu_v13", "bu_v22"]].dropna()
d1t = d1t[(d1t["bu_comparecimento"] >= 20) & (d1t["seq_dur_mediana"] > 0)]
d1t["p13"] = d1t["bu_v13"] / (d1t["bu_v13"] + d1t["bu_v22"]).clip(lower=1)
d1t["r_p13"] = d1t["p13"] - d1t.groupby("mun")["p13"].transform("mean")
d1t["r_dur"] = d1t["seq_dur_mediana"] - d1t.groupby("mun")["seq_dur_mediana"].transform("mean")
corr_1t = float(np.corrcoef(d1t["r_p13"].values, d1t["r_dur"].values)[0, 1])
pr(f"  Correlação intra-municipal NO 1T: {corr_1t:.6f}")

# 1e: Magnitude em votos
# Se a correlação fosse causal (votos mais rápidos = votos fabricados),
# quantos votos seriam afetados?
# Pegar o quartil mais rápido vs mais lento e ver a diferença de p13
q1 = d[d["seq_dur_mediana"] <= d["seq_dur_mediana"].quantile(0.25)]
q4 = d[d["seq_dur_mediana"] >= d["seq_dur_mediana"].quantile(0.75)]
diff_p13 = float(q1["p13"].mean() - q4["p13"].mean())
votos_q1 = int(q1["bu_comparecimento"].sum())
pr(f"  Q1 rápido vs Q4 lento: Δp13 = {diff_p13:.4f}, votos no Q1 = {votos_q1:,}")
pr(f"  Se 100% da diferença fosse fabricação: {abs(diff_p13) * votos_q1:,.0f} votos")

R["achado1"] = {
    "corr_intra_mun": round(corr_intra, 6),
    "corr_intra_mun_modelo": round(corr_mod, 6),
    "corr_1t": round(corr_1t, 6),
    "corr_por_uf": corr_uf,
    "diff_p13_q1_q4": round(diff_p13, 4),
    "votos_q1": votos_q1,
    "impacto_maximo_votos": round(abs(diff_p13) * votos_q1),
}

# ============================================================
# ACHADO 2: Modelo de urna prediz resíduo do resultado
# Hipótese: urnas antigas estão em locais específicos (escolas rurais)
# ============================================================
pr("\n=== ACHADO 2: Modelo × Resultado ===")
# Controlando por município E zona (mais fino que só município)
d["zona"] = d["mun"] + "_" + u.loc[d.index, "NR_ZONA"]
d["r_p13_zona"] = d["p13"] - d.groupby("zona")["p13"].transform("mean")
groups_z = [g["r_p13_zona"].values for _, g in d.groupby("modelo") if len(g) >= 100]
if len(groups_z) >= 2:
    F_z, p_z = stats.f_oneway(*groups_z)
    pr(f"  ANOVA por modelo, controlando por zona: F={F_z:.2f}, p={p_z:.6f}")
    R["achado2"] = {"F_zona": round(float(F_z), 2), "p_zona": round(float(p_z), 6)}
else:
    R["achado2"] = {"nota": "Poucos modelos"}

# Média de p13 por modelo dentro de cada UF
for uf in ["SP", "MG", "BA", "RJ", "RS"]:
    g = d[d["SG_UF"] == uf]
    g["r"] = g["p13"] - g.groupby("mun")["p13"].transform("mean")
    by_mod = g.groupby("modelo")["r"].mean()
    pr(f"  {uf}: resíduo médio por modelo = {by_mod.to_dict()}")

# ============================================================
# ACHADO 3: Falhas criptográficas em 2022
# ============================================================
pr("\n=== ACHADO 3: Falhas criptográficas ===")
hash_cols = [c for c in u.columns if c.startswith("hash_ok_") or c.startswith("assin_ok_")]
for col in hash_cols:
    falhas = u[u[col] == False]
    if len(falhas) > 0:
        pr(f"  {col}: {len(falhas)} falhas")
        for _, r_f in falhas.head(5).iterrows():
            pr(f"    {r_f['SG_UF']} mun={r_f['CD_MUNICIPIO']} zona={r_f['NR_ZONA']} seção={r_f['NR_SECAO']} modelo={r_f.get('modelo','?')}")
        # Esses votos afetam o resultado?
        v13 = falhas["bu_v13"].sum()
        v22 = falhas["bu_v22"].sum()
        pr(f"    Votos nas urnas com falha: v13={int(v13)}, v22={int(v22)}, total={int(v13+v22)}")

R["achado3"] = {}
for col in hash_cols:
    falhas = u[u[col] == False]
    if len(falhas) > 0:
        R["achado3"][col] = {
            "n_falhas": len(falhas),
            "ufs": falhas["SG_UF"].value_counts().to_dict(),
            "votos_total": int(falhas["bu_v13"].sum() + falhas["bu_v22"].sum()),
        }

# ============================================================
# ACHADO 4: BU diverge do log no comparecimento
# ============================================================
pr("\n=== ACHADO 4: BU × LOG divergem no comparecimento ===")
d4 = u[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO",
        "bu_comparecimento", "computado", "bu_v13", "bu_v22", "modelo"]].dropna()
d4 = d4[d4["bu_comparecimento"] > 0]
diff = d4[d4["bu_comparecimento"] != d4["computado"]]
pr(f"  {len(diff)} urnas com divergência BU vs LOG")
if len(diff) > 0:
    diff["delta"] = (diff["computado"] - diff["bu_comparecimento"]).astype(int)
    pr(f"  Δ médio: {diff['delta'].mean():.1f}, mediana: {diff['delta'].median():.0f}")
    pr(f"  Δ mín: {diff['delta'].min()}, Δ máx: {diff['delta'].max()}")
    for _, r_d in diff.head(10).iterrows():
        pr(f"    {r_d['SG_UF']} mun={r_d['CD_MUNICIPIO']} z={r_d['NR_ZONA']} s={r_d['NR_SECAO']}: BU={int(r_d['bu_comparecimento'])}, LOG={int(r_d['computado'])}, Δ={int(r_d['computado']-r_d['bu_comparecimento'])}")
    R["achado4"] = {
        "n_divergencias": len(diff),
        "delta_medio": round(float(diff["delta"].mean()), 1),
        "delta_mediana": round(float(diff["delta"].median()), 1),
        "votos_afetados": int(diff["bu_v13"].sum() + diff["bu_v22"].sum()),
        "ufs": diff["SG_UF"].value_counts().to_dict(),
    }
else:
    R["achado4"] = {"n_divergencias": 0}

# ============================================================
# ACHADO 5: Votos antes das 7h
# ============================================================
pr("\n=== ACHADO 5: Votos antes das 7h ===")
vpm = pd.read_parquet(os.path.join(RAIZ, f"dados_leves/votos_por_minuto_{ANO}_2t.parquet"))
vpm["ts"] = pd.to_datetime(vpm["minuto"], format="%d/%m/%Y %H:%M", errors="coerce")
vpm = vpm.dropna(subset=["ts"])
antes = vpm[vpm["ts"].dt.hour < 7]
pr(f"  Votos antes das 7h: {int(antes['votos'].sum()):,} em {len(antes)} registros")
pr(f"  UFs com votos antes das 7h:")
por_uf = antes.groupby("SG_UF")["votos"].sum().sort_values(ascending=False)
for uf, v in por_uf.head(10).items():
    pr(f"    {uf}: {int(v):,}")

# Hora mais cedo
pr(f"  Hora mais cedo: {antes['ts'].min()}")

# CONTEXTO: a urna pode abrir antes das 8h para testes internos
# Os "votos computados" antes das 7h são os votos do dia de teste?
# Verificar nas urnas
d5u = u[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO",
         "seq_votos_antes_7h", "seq_votos_dia", "bu_comparecimento",
         "primeiro_voto"]].dropna()
d5u = d5u[d5u["seq_votos_antes_7h"] > 0]
pr(f"\n  Urnas com votos antes das 7h: {len(d5u)}")
pr(f"  Total votos antes das 7h (do log): {int(d5u['seq_votos_antes_7h'].sum()):,}")
if len(d5u) > 0:
    pr(f"  Primeiro voto mais cedo: {d5u['primeiro_voto'].min()}")
    # Esses votos estão INCLUÍDOS no BU ou são votos de teste?
    # Se seq_votos_dia == bu_comparecimento, os votos antes das 7h são extras
    d5u["extra"] = d5u["seq_votos_dia"] - d5u["bu_comparecimento"]
    pr(f"  seq_votos_dia - bu_comparecimento: média={d5u['extra'].mean():.1f}, mediana={d5u['extra'].median():.0f}")

R["achado5"] = {
    "votos_antes_7h_vpm": int(antes["votos"].sum()),
    "urnas_com_voto_antes_7h": len(d5u),
    "votos_antes_7h_log": int(d5u["seq_votos_antes_7h"].sum()) if len(d5u) > 0 else 0,
    "por_uf": por_uf.to_dict(),
}

# ============================================================
# ACHADO 6: "Votos fora do dia" — número gigante (124M)
# Isso precisa de investigação: são os mesmos votos contados de outro jeito?
# ============================================================
pr("\n=== ACHADO 6: 'Votos fora do dia' — o que é? ===")
d6 = u[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO",
        "seq_votos_dia", "seq_votos_fora_dia", "bu_comparecimento",
        "computado", "primeiro_voto", "ultimo_voto"]].dropna()

# O que é seq_votos_fora_dia? Se é a GRANDE maioria, pode ser definição do campo
total_dia = d6["seq_votos_dia"].sum()
total_fora = d6["seq_votos_fora_dia"].sum()
total_bu = d6["bu_comparecimento"].sum()
pr(f"  seq_votos_dia total: {int(total_dia):,}")
pr(f"  seq_votos_fora_dia total: {int(total_fora):,}")
pr(f"  bu_comparecimento total: {int(total_bu):,}")
pr(f"  dia + fora = {int(total_dia + total_fora):,}")
pr(f"  Diferença (dia+fora) - bu: {int(total_dia + total_fora - total_bu):,}")

# Parece que "votos_dia" são os que o log registra, e "fora_dia" pode ser
# votos de outros cargos no 1t? Ou votos contados por outro evento no log?
# Verificar
pr(f"\n  Amostra de urnas com muitos votos fora do dia:")
big_fora = d6.nlargest(5, "seq_votos_fora_dia")
for _, r_b in big_fora.iterrows():
    pr(f"    {r_b['SG_UF']} mun={r_b['CD_MUNICIPIO']}: dia={int(r_b['seq_votos_dia'])}, fora={int(r_b['seq_votos_fora_dia'])}, BU={int(r_b['bu_comparecimento'])}")

R["achado6"] = {
    "total_dia": int(total_dia),
    "total_fora": int(total_fora),
    "total_bu": int(total_bu),
    "soma_dia_fora": int(total_dia + total_fora),
}

# Salvar
out = os.path.join(AQUI, "..", "resultados", f"resultado_investigacao_{ANO}.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(R, open(out, "w"), ensure_ascii=False, indent=1, default=str)
pr(f"\nSalvo em {out}")
pr("=== Fim Investigação ===")
