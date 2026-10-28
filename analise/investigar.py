"""Investiga os sinais estranhos da primeira rodada de testes."""
import os

import numpy as np
import pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
b = pd.read_parquet(os.path.join(AQUI, "base.parquet"))
b = b[b["total_1"].notna() & b["total_2"].notna()].copy()
b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
cand1 = [c for c in b.columns if c.startswith("v") and c.endswith("_1") and c != "validos_1"]

print("== A. Seções muito fora do padrão do município (pró-Flávio): quem tinha o voto no 1º turno?")
o = pd.read_csv(os.path.join(AQUI, "secoes_mais_fora_do_padrao.csv"), sep=";", dtype={"CD_MUNICIPIO": str})
o = o[o["z"].abs() > 5]
k = ["SG_UF", "NR_ZONA", "NR_SECAO"]
x = b.reset_index(drop=True)
x["NR_ZONA"], x["NR_SECAO"] = x["NR_ZONA"].astype(int), x["NR_SECAO"].astype(int)
m = o.merge(x, left_on=["SG_UF", "NM_MUNICIPIO_1", "NR_ZONA", "NR_SECAO"],
            right_on=["SG_UF", "NM_MUNICIPIO_1", "NR_ZONA", "NR_SECAO"], suffixes=("", "_b"))
top = (m[cand1].div(m["validos_1_b"], axis=0)).mean().sort_values(ascending=False).head(5)
nac = (b[cand1].sum() / b["validos_1"].sum()).reindex(top.index)
print("  % médio no 1º turno nessas seções x Brasil:", ", ".join(f"{c}: {100*v:.1f}% (BR {100*nac[c]:.1f}%)" for c, v in top.items()))
print("  locais de votação:", m["NR_LOCAL_VOTACAO_1"].nunique(), "| municípios:", m["NM_MUNICIPIO_1"].value_counts().head(8).to_dict())
print("  tamanho mediano (válidos 1º/2º):", m["validos_1"].median(), m["validos_2"].median(),
      "| comparecimento 1º/2º:", round((m["QT_COMPARECIMENTO_1"]/m["QT_APTOS_1"]).median(), 3), round((m["QT_COMPARECIMENTO_2"]/m["QT_APTOS_2"]).median(), 3))
print("  urna trocada:", int((m["NR_URNA_EFETIVADA_1_b"] != m["NR_URNA_EFETIVADA_2_b"]).sum()), "de", len(m))
print(m[["SG_UF", "NM_MUNICIPIO_1", "NR_ZONA", "NR_SECAO", "validos_1", "validos_2", "L1", "L2", "swing_mun", "z"]].head(12).to_string(index=False))

print("\n== B. Último dígito: o viés vem só da inclinação da distribuição? (esperado = histograma suavizado)")
for n in (1, 2):
    for c, nome in (("v13", "Lula"), ("v22", "Flávio")):
        v = b[f"{c}_{n}"].astype(int)
        v = v[v >= 100]
        h = np.bincount(v)
        suave = pd.Series(h).rolling(21, center=True, min_periods=1).mean().values  # densidade local
        esp = np.array([suave[d::10][10:].sum() for d in range(10)])
        obs = np.bincount(v % 10, minlength=10)
        esp = esp / esp.sum() * obs.sum()
        print(f"  {n}º {nome:6}: qui-quadrado contra o esperado pela inclinação p={stats.chisquare(obs, esp).pvalue:.3f}")

print("\n== C. 2º turno: buraco de chegada das 17h10 às 19h?")
r2 = b["DT_BU_RECEBIDO_2"].dt.floor("5min").value_counts().sort_index()
print("  urnas por 5 min (17h00–19h30):", {str(k)[11:16]: int(v) for k, v in r2.items() if "17:00" <= str(k)[11:16] <= "19:30"})
e = (b["DT_BU_RECEBIDO_2"] - b["DT_EMISSAO_BU_2"]).dt.total_seconds() / 60
e1 = (b["DT_BU_RECEBIDO_1"] - b["DT_EMISSAO_BU_1"]).dt.total_seconds() / 60
br = b["SG_UF"].isin(["SP", "RJ", "MG", "BA", "PE", "CE", "PR", "RS", "SC", "GO", "DF", "ES", "PB", "RN", "AL", "SE", "PI", "MA", "PA", "AP", "TO"])
print(f"  minutos entre o boletim impresso e a chegada no TSE (estados no horário de Brasília): 1º mediana {e1[br].median():.0f}, 2º mediana {e[br].median():.0f}")
print("  quem chegou às 17h no 2º:", b[b["DT_BU_RECEBIDO_2"].dt.hour == 17]["SG_UF"].value_counts().head(6).to_dict())
print("  emissão das urnas que chegaram entre 19h e 19h05 (2º):",
      b[(b["DT_BU_RECEBIDO_2"] >= "2026-10-25 19:00") & (b["DT_BU_RECEBIDO_2"] < "2026-10-25 19:05")]["DT_EMISSAO_BU_2"].dt.floor("15min").value_counts().head(5).to_dict())
print("  primeira chegada depois das 17h10 (2º):", b.loc[b["DT_BU_RECEBIDO_2"] > "2026-10-25 17:10", "DT_BU_RECEBIDO_2"].min())
print("  chegadas no 1º, 17h00–18h00 por 10 min:", b["DT_BU_RECEBIDO_1"].dt.floor("10min").value_counts().sort_index().head(8).to_dict())

print("\n== D. Resultados idênticos no 2º turno: são coincidência esperada com só 4 números?")
cols = ["v13_2", "v22_2", "branco_2", "nulo_2"]
x = b[b["total_2"] >= 100]
obs = x.duplicated(cols, keep=False).sum()
rng = np.random.default_rng(1)
sim = []
for _ in range(5):
    y = x[cols].copy()
    # preserva o tamanho e a proporção do município, sorteia os votos de cada seção
    p = x.groupby("mun")[cols].transform("sum")
    p = p.div(p.sum(axis=1), axis=0).values
    y = pd.DataFrame([rng.multinomial(t, pp) for t, pp in zip(x["total_2"].astype(int), p)], columns=cols)
    sim.append(y.duplicated(keep=False).sum())
print(f"  observado {obs:,}; simulado ao acaso {np.mean(sim):,.0f} ± {np.std(sim):,.0f}")
print("  com 15 números (1º turno) a coincidência fica rara, por isso só 42.")

print("\n== E. Mesmos votos do Flávio na mesma seção: o esperado considerando que ele mantém o eleitor")
s = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20)]
d22 = s["v22_2"] - s["v22_1"]
d13 = s["v13_2"] - s["v13_1"]
print(f"  variação típica por seção: Flávio mediana {d22.median():+.0f} (desvio {d22.std():.1f}), Lula mediana {d13.median():+.0f} (desvio {d13.std():.1f})")
print(f"  % de seções com variação exatamente 0: Flávio {100*(d22==0).mean():.2f}%, Lula {100*(d13==0).mean():.2f}%")
# esperado: distribuição suave da variação em torno do zero (média dos vizinhos -2..2 sem o 0)
for nome, d in (("Flávio", d22), ("Lula", d13)):
    vc = d.value_counts()
    viz = np.mean([vc.get(i, 0) for i in (-2, -1, 1, 2)])
    print(f"  {nome}: seções com variação 0 = {vc.get(0,0):,}; média dos vizinhos (−2,−1,+1,+2) = {viz:,.0f}")
