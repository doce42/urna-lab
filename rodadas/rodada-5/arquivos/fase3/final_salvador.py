"""Z1 (fase3/PREREG_FINAL.md): o desvio de Salvador em 2026 é isolado entre as capitais? Explica-se pelo perfil do eleitorado?
Saída: fase3/resultados/final_salvador.json."""
import json, zipfile
import numpy as np, pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
src = open(RAIZ + "/fase3/teste_grandes_cidades.py").read().split("LIM = 3.0")[0]; exec(src)   # d, X, y, beta, res, lg
R = {"pre_registro": "fase3/PREREG_FINAL.md (Z1)"}
# 1) capitais: maior município de cada UF
cap = d.groupby("uf").QT_APTOS_2.idxmax()
rc = pd.Series(res[d.index.get_indexer(cap.values)], index=cap.index)
out = {}
for uf, r in rc.items():
    outras = rc.drop(uf); esc = 1.4826 * np.median(np.abs(outras - np.median(outras)))
    out[uf] = {"municipio": cap[uf], "residuo": float(r), "z_entre_capitais": float((r - np.median(outras)) / esc)}
R["capitais"] = dict(sorted(out.items(), key=lambda x: -abs(x[1]["z_entre_capitais"])))
R["salvador_z_entre_capitais"] = out["BA"]["z_entre_capitais"]; R["capitais_com_abs_z_maior_3"] = [k for k, v in out.items() if abs(v["z_entre_capitais"]) > 3]
print("capitais |z|>3:", R["capitais_com_abs_z_maior_3"], "Salvador", round(out["BA"]["z_entre_capitais"], 2), flush=True)


# 2) seções das capitais do Nordeste: Δvirada (2026 − 2022) × perfil do eleitorado de 2026
def secoes(ano):
    b = pd.read_parquet(f"{RAIZ}/analise/base.parquet" if ano == "2026" else f"{RAIZ}/analise/base_{ano}.parquet")
    b = b[(b.validos_1 >= 20) & (b.validos_2 >= 20)].copy(); b["mun"] = b.SG_UF + b.CD_MUNICIPIO.astype(int).astype(str)
    b["k"] = b.mun + "/" + b.NR_ZONA.astype(int).astype(str) + "/" + b.NR_SECAO.astype(int).astype(str)
    b["sw"] = lg(b.v13_2, b.validos_2) - lg(b.v13_1, b.validos_1); return b


NE = ["BA", "PE", "CE", "MA", "PI", "RN", "PB", "AL", "SE"]
caps_ne = [cap[u] for u in NE]
s26, s22 = secoes("2026"), secoes("2022")
s26 = s26[s26.mun.isin(caps_ne)]; s22 = s22[s22.mun.isin(caps_ne)]
m = s26.set_index("k")[["mun", "SG_UF", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO_2", "sw", "v13_1", "validos_1"]].join(s22.set_index("k")[["sw"]].rename(columns={"sw": "sw22"}), how="inner")
m["dsw"] = m.sw - m.sw22; m["p1"] = m.v13_1 / m.validos_1
feats = []
for uf in NE:
    z = zipfile.ZipFile(f"{RAIZ}/dados/perfil_eleitorado/perfil_eleitor_secao_2026_{uf}.zip"); nome = [n for n in z.namelist() if n.endswith(".csv")][0]
    pf = pd.read_csv(z.open(nome), sep=";", encoding="latin-1", usecols=["CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_GENERO", "CD_FAIXA_ETARIA", "CD_GRAU_ESCOLARIDADE", "QT_ELEITORES"]).rename(columns={"QT_ELEITORES": "QT_ELEITORES_PERFIL"})   # correção: nome da coluna em 2026
    pf = pf[(uf + pf.CD_MUNICIPIO.astype(int).astype(str)).isin(caps_ne)]
    k = [pf.CD_MUNICIPIO, pf.NR_ZONA, pf.NR_SECAO]; tot = pf.groupby(k).QT_ELEITORES_PERFIL.sum()
    f = pd.DataFrame({"fem": pf[pf.CD_GENERO == 4].groupby(k).QT_ELEITORES_PERFIL.sum() / tot})
    for c in (1, 2, 3, 4, 5, 6, 7): f[f"esc{c}"] = pf[pf.CD_GRAU_ESCOLARIDADE == c].groupby(k).QT_ELEITORES_PERFIL.sum() / tot
    idade = pf.CD_FAIXA_ETARIA // 100
    for a, (lo, hi) in {"ate24": (0, 24), "25_44": (25, 44), "45_59": (45, 59)}.items(): f[f"id_{a}"] = pf[(idade >= lo) & (idade <= hi)].groupby(k).QT_ELEITORES_PERFIL.sum() / tot
    f = f.fillna(0).reset_index(); f["k"] = uf + f.CD_MUNICIPIO.astype(int).astype(str) + "/" + f.NR_ZONA.astype(int).astype(str) + "/" + f.NR_SECAO.astype(int).astype(str)
    feats.append(f.set_index("k").drop(columns=["CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]))
F = pd.concat(feats); m = m.join(F, how="inner")
cols = [c for c in F.columns] + ["p1"]
Xs = np.column_stack([np.ones(len(m))] + [m[c].values for c in cols]); ys = m.dsw.values


def avalia(alvo_mun, rng):
    a = (m.mun == alvo_mun).values; beta_s, *_ = np.linalg.lstsq(Xs[~a], ys[~a], rcond=None); r = ys - Xs @ beta_s
    orig = float(ys[a].mean() - ys[~a].mean()); resid = float(r[a].mean() - r[~a].mean())
    locs = m.loc[a, "NR_LOCAL_VOTACAO_2"].astype(str) + "-" + m.loc[a, "NR_ZONA"].astype(str); uniq = locs.unique(); idx_a = np.where(a)[0]
    grp = {l: idx_a[(locs == l).values] for l in uniq}; bs = []
    for _ in range(1000):
        pick = rng.choice(uniq, len(uniq)); ii = np.concatenate([grp[l] for l in pick]); bs.append(r[ii].mean() - r[~a].mean())
    ic = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    leitura = "explicado pelo perfil" if abs(resid) < abs(orig) / 3 else ("persiste" if (abs(resid) >= 2 * abs(orig) / 3 and not (ic[0] <= 0 <= ic[1])) else "explicado em parte")
    return {"secoes": int(a.sum()), "excesso_original_dvirada": orig, "excesso_apos_perfil": resid, "ic95_bootstrap_locais": ic, "fracao_explicada": 1 - resid / orig if orig else None, "leitura": leitura}


rng = np.random.default_rng(9900)
R["secoes_ne_pareadas"] = int(len(m))
for nome, mu in (("Salvador", "BA38490"), ("Recife (validação)", cap["PE"]), ("Fortaleza (validação)", cap["CE"])):
    R[nome] = avalia(mu, rng); print(nome, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in R[nome].items()}, flush=True)
json.dump(R, open(RAIZ + "/fase3/resultados/final_salvador.json", "w"), ensure_ascii=False, indent=1, default=float)
