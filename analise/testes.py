"""Testes de padrões entre o 1º e o 2º turno (Presidente 2026). Cada teste compara o observado com o esperado ao acaso."""
import os

import numpy as np
import pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
b = pd.read_parquet(os.path.join(AQUI, "base.parquet"))
b = b[b["total_1"].notna() & b["total_2"].notna()].copy()
NE = {"AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"}
REG = {**{u: "NE" for u in NE}, **{u: "N" for u in ["AC", "AM", "AP", "PA", "RO", "RR", "TO"]},
       **{u: "CO" for u in ["DF", "GO", "MS", "MT"]}, **{u: "SE" for u in ["ES", "MG", "RJ", "SP"]},
       **{u: "S" for u in ["PR", "RS", "SC"]}, "ZZ": "EX"}
b["reg"] = b["SG_UF"].map(REG)
b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
ok = (b["validos_1"] >= 20) & (b["validos_2"] >= 20)
b["L1"] = b["v13_1"] / b["validos_1"]
b["L2"] = b["v13_2"] / b["validos_2"]
b["F1"] = b["v22_1"] / b["validos_1"]
b["swing"] = b["L2"] - b["L1"]
b["comp1"] = b["QT_COMPARECIMENTO_1"] / b["QT_APTOS_1"]
b["comp2"] = b["QT_COMPARECIMENTO_2"] / b["QT_APTOS_2"]
R = {}


def tit(t):
    print("\n" + "=" * 8, t)


# 1. Virada de cada seção comparada com a das seções vizinhas (mesmo município)
tit("1. Virada por seção (Lula 2º − Lula 1º, % dos válidos), comparada com o próprio município")
s = b[ok].copy()
s["swing_mun"] = s.groupby("mun")["swing"].transform("median")
s["res"] = s["swing"] - s["swing_mun"]
p = (s["L1"] + s["L2"]) / 2
s["z"] = s["res"] / np.sqrt(p * (1 - p) * (1 / s["validos_1"] + 1 / s["validos_2"]))
print(f"seções analisadas {len(s):,}; virada mediana {100*s['swing'].median():.2f} pp; desvio do resíduo {100*s['res'].std():.2f} pp")
for k in (3, 4, 5, 6):
    a, z = (s["z"] > k).sum(), (s["z"] < -k).sum()
    print(f"  |z|>{k}: pró-Lula {a:,}  pró-Flávio {z:,}  (simetria: {a/(a+z):.3f})")
print(f"  assimetria (skew) do z: {stats.skew(s['z']):.3f}; curtose: {stats.kurtosis(s['z']):.2f}")
s[["SG_UF", "NM_MUNICIPIO_1", "NR_ZONA", "NR_SECAO", "validos_1", "validos_2", "L1", "L2", "swing_mun", "z",
   "NR_URNA_EFETIVADA_1", "NR_URNA_EFETIVADA_2"]].reindex(s["z"].abs().sort_values(ascending=False).index).head(200)\
    .to_csv(os.path.join(AQUI, "secoes_mais_fora_do_padrao.csv"), sep=";", index=False)
fora = s[s["z"].abs() > 5]
print("  concentração dos |z|>5 por UF (top 5, % das seções da UF):")
uf = (fora.groupby("SG_UF").size() / s.groupby("SG_UF").size()).dropna().sort_values(ascending=False).head(5)
print("   ", ", ".join(f"{k} {100*v:.2f}%" for k, v in uf.items()), f"| média nacional {100*len(fora)/len(s):.2f}%")
R["s"] = s

# 2. Virada x hora de chegada, dentro do município
tit("2. A virada depende da hora em que a urna chegou ao TSE? (dentro do município)")
s["ord2"] = s.groupby("mun")["DT_BU_RECEBIDO_2"].rank(pct=True)
s["ord1"] = s.groupby("mun")["DT_BU_RECEBIDO_1"].rank(pct=True)
grandes = s[s.groupby("mun")["mun"].transform("size") >= 20]
for col, nome in (("ord2", "chegada no 2º"), ("ord1", "chegada no 1º")):
    r, pv = stats.spearmanr(grandes[col], grandes["res"])
    print(f"  Spearman(resíduo da virada, ordem de {nome}): r={r:+.4f} p={pv:.2g} (n={len(grandes):,})")
grandes = grandes.assign(dec=pd.qcut(grandes["ord2"], 10, labels=False, duplicates="drop"))
print("  resíduo médio da virada por décimo da ordem de chegada no 2º (pp):",
      " ".join(f"{100*v:+.2f}" for v in grandes.groupby("dec")["res"].mean()))
r, pv = stats.spearmanr(s["ord1"], s["ord2"])
print(f"  mesma seção chega em posição parecida nos dois turnos? Spearman={r:.3f}")

# 3. Voto x hora de chegada, dentro do estado, em cada turno
tit("3. % do Lula x ordem de chegada dentro do estado, em cada turno")
for n in (1, 2):
    x = b[ok].copy()
    x["o"] = x.groupby("SG_UF")[f"DT_BU_RECEBIDO_{n}"].rank(pct=True)
    x["l"] = x[f"v13_{n}"] / x[f"validos_{n}"]
    rs = x.groupby("SG_UF").apply(lambda g: stats.spearmanr(g["o"], g["l"])[0], include_groups=False)
    print(f"  {n}º turno: correlação mediana entre UFs {rs.median():+.3f}; positivas {int((rs>0).sum())}/{len(rs)}")
    R[f"rs{n}"] = rs
print("  mesma direção nos dois turnos por UF:", int((np.sign(R['rs1']) == np.sign(R['rs2'])).sum()), "de", len(R["rs1"]),
      f"; correlação entre turnos {stats.pearsonr(R['rs1'], R['rs2'])[0]:.2f}")

# 4. Composição regional explica a curva?
tit("4. A forma da curva vem da ordem em que as regiões chegaram?")
for n in (1, 2):
    x = b[ok & b[f"DT_BU_RECEBIDO_{n}"].notna()].copy()
    x["j"] = x[f"DT_BU_RECEBIDO_{n}"].dt.floor("10min")
    g = x.groupby("j").agg(lula=(f"v13_{n}", "sum"), val=(f"validos_{n}", "sum"), urnas=("reg", "size"),
                           ne=("reg", lambda r: (r == "NE").mean()))
    g = g[g["urnas"] >= 200]
    g["pl"] = g["lula"] / g["val"]
    # esperado: cada urna com o % que a região dela teve no turno inteiro
    regp = x.groupby("reg").apply(lambda r: r[f"v13_{n}"].sum() / r[f"validos_{n}"].sum(), include_groups=False)
    x["esp"] = x["reg"].map(regp) * x[f"validos_{n}"]
    g["pe"] = x.groupby("j")["esp"].sum().reindex(g.index) / g["val"]
    print(f"  {n}º turno: {len(g)} janelas de 10 min; correlação % Lula na janela x fatia do Nordeste {stats.pearsonr(g['pl'], g['ne'])[0]:.2f}; "
          f"x % esperado só pela região {stats.pearsonr(g['pl'], g['pe'])[0]:.2f}")
x = b.copy()
print("  urnas por hora de chegada, 2º turno:", x["DT_BU_RECEBIDO_2"].dt.hour.value_counts().sort_index().to_dict())
print("  urnas por hora de chegada, 1º turno:", x["DT_BU_RECEBIDO_1"].dt.hour.value_counts().sort_index().to_dict())

# 5. Urna trocada entre os turnos
tit("5. Seções que trocaram de urna entre os turnos")
s["trocou"] = s["NR_URNA_EFETIVADA_1"] != s["NR_URNA_EFETIVADA_2"]
t, n_ = s[s["trocou"]]["res"], s[~s["trocou"]]["res"]
print(f"  trocaram: {s['trocou'].sum():,} ({100*s['trocou'].mean():.1f}%); resíduo médio trocou {100*t.mean():+.3f} pp x não trocou {100*n_.mean():+.3f} pp; "
      f"Mann-Whitney p={stats.mannwhitneyu(t, n_).pvalue:.2g}")

# 6. Último dígito (deveria ser uniforme)
tit("6. Último dígito das contagens (≥ 100 votos), qui-quadrado contra uniforme")
for n in (1, 2):
    for c, nome in (("v13", "Lula"), ("v22", "Flávio"), ("branco", "branco"), ("nulo", "nulo")):
        v = b[f"{c}_{n}"].dropna().astype(int)
        v = v[v >= 100]
        if len(v) < 1000:
            continue
        obs = np.bincount(v % 10, minlength=10)
        print(f"  {n}º {nome:7}: n={len(v):>7,} p={stats.chisquare(obs).pvalue:.3f}  dígitos {' '.join(f'{100*o/obs.sum():.1f}' for o in obs)}")

# 7. Contagens idênticas entre turnos x acaso (embaralhando dentro do município)
tit("7. Mesmo número de votos na mesma seção nos dois turnos, comparado ao acaso")
rng = np.random.default_rng(1)
for c, nome in (("v13", "Lula"), ("v22", "Flávio")):
    obs = (s[f"{c}_1"] == s[f"{c}_2"]).sum()
    esp = []
    for _ in range(20):
        emb = s.groupby("mun")[f"{c}_2"].transform(lambda v: rng.permutation(v.values))
        esp.append((s[f"{c}_1"] == emb).sum())
    print(f"  {nome}: idênticas {obs:,}; ao acaso {np.mean(esp):,.0f} ± {np.std(esp):.0f} (embaralhando a mesma seção dentro do município)")
for n in (1, 2):
    cols = [c for c in b.columns if c.endswith(f"_{n}") and (c.startswith("v") or c in (f"branco_{n}", f"nulo_{n}"))]
    x = b[b[f"total_{n}"] >= 100]
    d = x.duplicated(cols, keep=False).sum()
    print(f"  {n}º turno: seções (≥100 votos) com resultado completo idêntico a outra seção: {d}")

# 8. Impressão digital: comparecimento x % do vencedor da seção
tit("8. 'Impressão digital' da eleição: comparecimento alto + votação quase unânime")
for n in (1, 2):
    x = b[b[f"validos_{n}"] >= 50]
    c = x[f"QT_COMPARECIMENTO_{n}"] / x[f"QT_APTOS_{n}"]
    for k, nome in (("v13", "Lula"), ("v22", "Flávio")):
        sh = x[f"{k}_{n}"] / x[f"validos_{n}"]
        print(f"  {n}º {nome:6}: seções com comparecimento ≥95% e ≥90% dos válidos: {int(((c>=.95)&(sh>=.9)).sum())}; "
              f"≥90% dos válidos (qualquer comparecimento): {int((sh>=.9).sum()):,}; correlação comparecimento x % {stats.spearmanr(c, sh)[0]:+.3f}")
    print(f"  {n}º comparecimento > 100%: {int((c > 1).sum())}; = 100%: {int((c == 1).sum())}")

# 9. Liberação sem biometria
tit("9. Eleitores liberados sem biometria x virada")
s["bio"] = s["QT_ELEI_BIOM_SEM_HABILITACAO_2"] / s["QT_COMPARECIMENTO_2"]
r, pv = stats.spearmanr(s["bio"], s["res"])
print(f"  mediana {100*s['bio'].median():.1f}% do comparecimento; Spearman(sem biometria, resíduo da virada) r={r:+.4f} p={pv:.2g}")
for n in (1, 2):
    x = b[ok]
    bio = x[f"QT_ELEI_BIOM_SEM_HABILITACAO_{n}"] / x[f"QT_COMPARECIMENTO_{n}"]
    print(f"  {n}º: Spearman(sem biometria, % Lula) {stats.spearmanr(bio, x[f'v13_{n}']/x[f'validos_{n}'])[0]:+.3f}; "
          f"seções com >50% sem biometria: {int((bio>.5).sum())}")

# 10. Mudança de comparecimento x virada
tit("10. Mudança de comparecimento x virada")
r, pv = stats.spearmanr(s["comp2"] - s["comp1"], s["res"])
print(f"  comparecimento mudou {100*(s['comp2']-s['comp1']).median():+.2f} pp (mediana); Spearman com resíduo da virada r={r:+.4f}")

# 11. Boletins emitidos antes das 17h de Brasília
tit("11. Boletins emitidos antes do fim da votação")
for n in (1, 2):
    x = b[b["SG_UF"] != "ZZ"]
    hl = x[f"DT_ENCERRAMENTO_{n}"].dt.hour + x[f"DT_ENCERRAMENTO_{n}"].dt.minute / 60
    ab = x[f"DT_ABERTURA_{n}"].dt.hour
    # fecha às 17h de Brasília: hora local esperada de encerramento = 17 - (8 - hora de abertura)
    esperado = 17 - (8 - ab.clip(6, 8))
    cedo = x[hl < esperado - 0.02]
    print(f"  {n}º: encerradas antes do horário local esperado: {len(cedo)}; UFs: {cedo['SG_UF'].value_counts().head(6).to_dict()}")
    if len(cedo):
        print("     exemplos:", cedo[["SG_UF", "NM_MUNICIPIO_1", "NR_ZONA", "NR_SECAO", f"DT_ABERTURA_{n}", f"DT_ENCERRAMENTO_{n}", f"QT_COMPARECIMENTO_{n}", f"QT_APTOS_{n}"]].head(3).to_string(index=False, header=False).replace("\n", "\n              "))
