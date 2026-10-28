"""T55: Cabo Frio e cidades citadas (pré-registro em fase3/PREREG_CABO_FRIO.md)."""
import glob, json
import numpy as np, pandas as pd

AN = "analise"; OUT = "fase3/resultados/cabo_frio.json"
CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
CIDADES = [("RJ", "CABO FRIO"), ("SP", "SANTANA DE PARNAÍBA"), ("RJ", "CAMPOS DOS GOYTACAZES"), ("RJ", "SÃO GONÇALO")]
R = {"pre_registro": "fase3/PREREG_CABO_FRIO.md"}


def municipios(ano):
    b = pd.read_parquet(f"{AN}/base.parquet" if ano == "2026" else f"{AN}/base_{ano}.parquet"); b = b[b.SG_UF != "ZZ"]
    elim = [c for c in b.columns if c.startswith("v") and c.endswith("_1") and c not in ("v13_1", "v22_1", "validos_1")]  # correção 1: validos_1 entrava como eliminado
    b["elim_1"] = b[elim].fillna(0).sum(axis=1); b["bn_1"] = b.branco_1 + b.nulo_1; b["bn_2"] = b.branco_2 + b.nulo_2
    g = b.groupby(["SG_UF", "NM_MUNICIPIO_2"])[["v13_1", "v22_1", "v13_2", "v22_2", "elim_1", "bn_1", "bn_2", "QT_COMPARECIMENTO_1", "QT_COMPARECIMENTO_2"]].sum()
    g["g13"] = g.v13_2 - g.v13_1; g["g22"] = g.v22_2 - g.v22_1
    g["disponivel"] = g.elim_1 + (g.QT_COMPARECIMENTO_2 - g.QT_COMPARECIMENTO_1) + (g.bn_1 - g.bn_2)
    g["frac_13_do_ganho"] = g.g13 / (g.g13 + g.g22)
    g["excede"] = g.g13 + g.g22 > g.disponivel + 1
    return b, g


for ano in ("2026", "2022"):
    b, g = municipios(ano)
    ok = (g.g13 + g.g22) > 500                      # municípios com ganho conjunto relevante
    avancou = "frac_13_do_ganho"
    r = {"municipios": int(len(g)), "ganho_excede_disponivel": int(g.excede.sum()),
         "frac_13_do_ganho_mediana": float(g.loc[ok, avancou].median()), "frac_13_do_ganho_p90": float(g.loc[ok, avancou].quantile(.9)),
         "frac_13_do_ganho_p10": float(g.loc[ok, avancou].quantile(.1)), "cidades": {}}
    for uf, nome in CIDADES:
        if (uf, nome) not in g.index: r["cidades"][nome] = "não encontrada"; continue
        x = g.loc[(uf, nome)]
        r["cidades"][nome] = {k: int(x[k]) for k in ("v13_1", "v22_1", "v13_2", "v22_2", "elim_1", "bn_1", "bn_2", "QT_COMPARECIMENTO_1", "QT_COMPARECIMENTO_2", "g13", "g22", "disponivel")}
        r["cidades"][nome]["frac_13_do_ganho"] = float(x.frac_13_do_ganho)
        r["cidades"][nome]["percentil_nacional"] = float((g.loc[ok, avancou] < x.frac_13_do_ganho).mean())
        r["cidades"][nome]["excede_disponivel"] = bool(x.excede)
    # municípios com perfil parecido: o líder do 1º turno com ≥ 60% de Lula+rival e o rival do líder com ≥ 90% do ganho
    lider22 = g.v22_1 / (g.v13_1 + g.v22_1) >= .6
    r["municipios_rival_lider_60pct_e_13_com_90pct_do_ganho"] = int((lider22 & ok & (g.frac_13_do_ganho >= .9)).sum())
    r["municipios_13_lider_60pct_e_22_com_90pct_do_ganho"] = int((~lider22 & (g.v13_1 / (g.v13_1 + g.v22_1) >= .6) & ok & (g.frac_13_do_ganho <= .1)).sum())
    R[ano] = r
# integridade (2026, 2º turno)
b, _ = municipios("2026"); b = b.astype({c: str for c in CH})
sel = b[[(u, n) in CIDADES for u, n in zip(b.SG_UF, b.NM_MUNICIPIO_2)]]
u = pd.concat([pd.read_parquet(f, columns=CH + ["assin_lista_ok", "hash_ok_bu", "assin_ok_bu", "hash_ok_rdv", "assin_ok_rdv", "bu_v13", "bu_v22", "rdv_v13", "rdv_v22"])
               for f in glob.glob(f"{AN}/brutos/2t/urnas_RJ.parquet") + glob.glob(f"{AN}/brutos/2t/urnas_SP.parquet")]).astype({c: str for c in CH})
d = sel.merge(u, on=CH, how="left")
assin = d[["assin_lista_ok", "hash_ok_bu", "assin_ok_bu", "hash_ok_rdv", "assin_ok_rdv"]].fillna(False).astype(bool).all(axis=1)
vot = (d.bu_v13.fillna(0) == d.v13_2) & (d.bu_v22.fillna(0) == d.v22_2.fillna(0)) & (d.rdv_v13.fillna(0) == d.v13_2) & (d.rdv_v22.fillna(0) == d.v22_2.fillna(0)) & d.bu_v13.notna()
R["integridade_2026"] = {n: {"secoes": int((d.NM_MUNICIPIO_2 == n).sum()), "ok": int(((d.NM_MUNICIPIO_2 == n) & assin & vot).sum())} for _, n in CIDADES}
json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
