"""T51: crescimento entre turnos por município (pré-registro em fase3/PREREG_CRESCIMENTO_ENTRE_TURNOS.md)."""
import json
import pandas as pd

AN = "analise"; OUT = "fase3/resultados/crescimento_turnos.json"
R = {"pre_registro": "fase3/PREREG_CRESCIMENTO_ENTRE_TURNOS.md"}
for ano, arq in (("2026", "base.parquet"), ("2022", "base_2022.parquet")):
    b = pd.read_parquet(f"{AN}/{arq}"); b = b[b.SG_UF != "ZZ"]
    m = b.groupby(["SG_UF", "CD_MUNICIPIO"])[["v13_1", "v22_1", "v13_2", "v22_2"]].sum()
    d = (m.v13_2 - m.v13_1) - (m.v22_2 - m.v22_1)          # > 0: Lula cresceu mais que o rival
    pr = m.v13_2 / (m.v13_2 + m.v22_2) - m.v13_1 / (m.v13_1 + m.v22_1)
    uf = m.groupby("SG_UF").sum(); duf = (uf.v13_2 - uf.v13_1) - (uf.v22_2 - uf.v22_1)
    porf = pd.DataFrame({"lula_mais": (d > 0).groupby("SG_UF").sum(), "rival_mais": (d < 0).groupby("SG_UF").sum(), "empate": (d == 0).groupby("SG_UF").sum()})
    t = b[["v13_1", "v22_1", "v13_2", "v22_2"]].sum()
    s1, s2 = t.v13_1 / (t.v13_1 + t.v22_1), t.v13_2 / (t.v13_2 + t.v22_2)
    atras = "lula" if s1 < .5 else "rival"; a1, a2 = (s1, s2) if atras == "lula" else (1 - s1, 1 - s2)
    R[ano] = {"municipios": int(len(m)), "lula_cresceu_mais": int((d > 0).sum()), "rival_cresceu_mais": int((d < 0).sum()), "empate": int((d == 0).sum()),
              "frac_lula_mais": float((d > 0).mean()), "frac_rival_mais": float((d < 0).mean()),
              "variante_proporcao_lula_subiu": int((pr > 0).sum()), "variante_proporcao_rival_subiu": int((pr < 0).sum()),
              "ufs_lula_mais_agregado": int((duf > 0).sum()), "ufs_rival_mais_agregado": int((duf < 0).sum()),
              "ufs_maioria_municipios_lula": int((porf.lula_mais > porf.rival_mais).sum()),
              "por_uf": porf.astype(int).to_dict("index"),
              "grafico": {"de_tras_no_1t": atras, "prop_1t_pct": round(100 * a1, 2), "prop_2t_pct": round(100 * a2, 2),
                          "cresceu_pp": round(100 * (a2 - a1), 2), "precisava_pp": round(100 * (.5 - a1), 2)}}
json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1)
for a in ("2026", "2022"):
    x = dict(R[a]); x.pop("por_uf"); print(a, json.dumps(x, ensure_ascii=False))
print("CE 2022", R["2022"]["por_uf"]["CE"], "MG 2022", R["2022"]["por_uf"]["MG"])
