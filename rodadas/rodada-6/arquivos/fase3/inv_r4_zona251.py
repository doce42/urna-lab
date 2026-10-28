"""F3 / R4: o desvio da virada nas zonas 251 e 259 de São Paulo capital (2022) persiste depois de controlar o perfil do eleitorado
da seção (escolaridade, faixa etária, sexo, estado civil, log dos aptos)? Regressão ajustada fora das zonas 251 e 259; resíduo médio
das zonas com IC por bootstrap de locais. Ver fase3/PREREG_RESPOSTAS.md (R4). Saída: fase3/resultados/r4_zona251.json."""
import json, zipfile
import numpy as np, pandas as pd

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
src = open(RAIZ + "/fase3/rev_i3_espacial.py").read().split('R = {"pre_registro"')[0]; exec(src)   # prepara(): zz do modelo completo do P9
b = prepara("2022"); sp = b[b.mun == "SP71072"].copy()
z = zipfile.ZipFile(RAIZ + "/dados/2022/perfil_eleitorado/perfil_eleitor_secao_2022_SP.zip")
pf = pd.read_csv(z.open("perfil_eleitor_secao_2022_SP.csv"), sep=";", encoding="latin-1",
                 usecols=["CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_GENERO", "CD_ESTADO_CIVIL", "CD_FAIXA_ETARIA", "CD_GRAU_ESCOLARIDADE", "QT_ELEITORES_PERFIL"])
pf = pf[pf.CD_MUNICIPIO == 71072].copy()
idade = pf.CD_FAIXA_ETARIA // 100
pf["fx"] = pd.cut(idade, [0, 24, 34, 44, 59, 200], labels=["ate24", "25_34", "35_44", "45_59", "60mais"])
k = ["NR_ZONA", "NR_SECAO"]; tot = pf.groupby(k).QT_ELEITORES_PERFIL.sum()
feat = pd.DataFrame({"fem": pf[pf.CD_GENERO == 4].groupby(k).QT_ELEITORES_PERFIL.sum() / tot,
                     "casado": pf[pf.CD_ESTADO_CIVIL == 3].groupby(k).QT_ELEITORES_PERFIL.sum() / tot})
for c in sorted(pf.CD_GRAU_ESCOLARIDADE.unique()):
    if c > 0: feat[f"esc{c}"] = pf[pf.CD_GRAU_ESCOLARIDADE == c].groupby(k).QT_ELEITORES_PERFIL.sum() / tot
for c in ["ate24", "25_34", "35_44", "45_59"]:
    feat[f"id_{c}"] = pf[pf.fx == c].groupby(k).QT_ELEITORES_PERFIL.sum() / tot
feat = feat.fillna(0).reset_index(); feat["NR_ZONA"] = feat.NR_ZONA.astype(str); feat["NR_SECAO"] = feat.NR_SECAO.astype(str)
sp["NR_ZONA"] = sp.NR_ZONA.astype(int).astype(str); sp["NR_SECAO"] = sp.NR_SECAO.astype(int).astype(str)
m = sp.merge(feat, on=["NR_ZONA", "NR_SECAO"], how="inner")
cols = [c for c in feat.columns if c not in k]
esc = [c for c in cols if c.startswith("esc")]; cols = [c for c in cols if c != esc[-1]]   # uma categoria de referência
X = np.column_stack([np.ones(len(m)), np.log(m.QT_APTOS_2.astype(float))] + [m[c].values for c in cols]); y = m.zz.values
alvo = m.NR_ZONA.isin(["251", "259"]).values


def ajusta(fora):
    beta, *_ = np.linalg.lstsq(X[fora], y[fora], rcond=None); return y - X @ beta


R = {"pre_registro": "fase3/PREREG_RESPOSTAS.md (R4)", "secoes_sp_capital": int(len(sp)), "com_perfil": int(len(m)), "covariaveis": ["log_aptos"] + cols}
rng = np.random.default_rng(9400)
for nome, fora in (("principal_ajuste_fora_das_zonas", ~alvo), ("sensibilidade_ajuste_com_todas", np.ones(len(m), bool))):
    res = ajusta(fora); R[nome] = {"r2_fora": float(1 - (res[~alvo] ** 2).sum() / ((y[~alvo] - y[~alvo].mean()) ** 2).sum())}
    for zz in ("251", "259"):
        s = (m.NR_ZONA == zz).values; locs = m.loc[s, "local"].values; uniq = np.unique(locs)
        orig = float(y[s].mean() - y[~alvo].mean()); resid = float(res[s].mean() - res[~alvo].mean())
        bs = []
        for _ in range(2000):
            pick = rng.choice(uniq, len(uniq)); idx = np.concatenate([np.where(s & (m.local.values == l))[0] for l in pick])
            bs.append(res[idx].mean() - res[~alvo].mean())
        ic = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
        leitura = "explicado" if (abs(resid) < abs(orig) / 3 and ic[0] <= 0 <= ic[1]) else ("persiste" if (not (ic[0] <= 0 <= ic[1]) and abs(resid) >= 2 * abs(orig) / 3) else "explicado em parte")
        R[nome][f"zona_{zz}"] = {"secoes": int(s.sum()), "locais": int(len(uniq)), "desvio_original": orig, "desvio_residual": resid, "ic95_residual_bootstrap_locais": ic, "fracao_explicada": 1 - resid / orig if orig else None, "leitura": leitura}
    print(nome, json.dumps(R[nome], ensure_ascii=False), flush=True)
json.dump(R, open(RAIZ + "/fase3/resultados/r4_zona251.json", "w"), ensure_ascii=False, indent=1)
