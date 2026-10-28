"""Auditoria final (segunda passagem): recalcula por outro caminho quatro números centrais dos relatórios."""
import json, re, sys
import numpy as np, pandas as pd
R = "."; OP = R + "/operacao_veracidade"; CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
out = {}
# 1) total de certificados: contagem direta dos parquets
tot = {}; 
for a in ("2022", "2026"):
    for t in (1, 2):
        d = pd.read_parquet(f"{OP}/resultados/certs_{a}_{t}t.parquet", columns=["cert_sha256", "cadeia_ok", "valido_no_dia", "emitido_depois_da_eleicao", "erro"])
        tot[f"{a}_{t}t"] = {"n": int((d.cert_sha256 != "").sum()), "cadeia_ok": int((d.cadeia_ok == True).sum()), "falha": int((d.cadeia_ok == False).sum()), "invalidos_no_dia": int((d.valido_no_dia == False).sum())}
out["certificados"] = {"por_conjunto": tot, "soma_n": sum(v["n"] for v in tot.values()), "soma_cadeia_ok": sum(v["cadeia_ok"] for v in tot.values()), "soma_falhas": sum(v["falha"] for v in tot.values())}
# 2) T61 por outro caminho: usar votos.csv (tabela já analisada pelo projeto de terceiros) em vez de reler o texto do QR
b = pd.read_csv(f"{OP}/externo/arvor_totalizacao/bus.csv", dtype=str); v = pd.read_csv(f"{OP}/externo/arvor_totalizacao/votos.csv", dtype=str)
v = v[(v.cargo == "1")]; p = v.pivot_table(index="bu_id", columns="candidato", values="votos", aggfunc="first").reset_index()
j = b[["id", "uf", "muni", "zona", "secao"]].rename(columns={"id": "bu_id"}).merge(p, on="bu_id")
j["SG_UF"] = j.uf.str.upper(); j["CD_MUNICIPIO"] = j.muni.astype(int).astype(str); j["NR_ZONA"] = j.zona.astype(int).astype(str); j["NR_SECAO"] = j.secao.astype(int).astype(str)
base = pd.read_parquet(f"{R}/analise/base.parquet").astype({c: str for c in CH})
m = j.merge(base[CH + ["v13_2", "v22_2"]], on=CH)
out["terceiros_por_votos_csv"] = {"boletins": int(len(j)), "pareados": int(len(m)), "v13_iguais": int((m["13"].astype(float) == m.v13_2).sum()), "v22_iguais": int((m["22"].astype(float) == m.v22_2).sum())}
# 3) zeros: recontagem direta
zs = {}
for ano, arq in (("2022", "base_2022.parquet"), ("2026", "base.parquet")):
    x = pd.read_parquet(f"{R}/analise/{arq}"); x = x[(x.SG_UF != "ZZ") & (x.total_2 > 0)]
    zs[ano] = {"direita_zero_2t": int((x.v22_2.fillna(0) == 0).sum()), "lula_zero_2t": int((x.v13_2.fillna(0) == 0).sum()), "comparecimento_positivo": int(len(x))}
out["zeros_recontagem"] = zs
# 4) estabilidade do T63: três células com sementes novas (réplicas 100 a 119)
sys.argv = ["x", "2026", "1", "1"]; sys.path.insert(0, OP + "/scripts")
import sim_adversarial as S
est = {}
for mec, d, X in (("dispersa", 1, 50_000), ("municipios", 1, 50_000), ("zonas", -1, 25_000), ("uniforme_logit", 1, 2_220_000), ("cinco_grandes", 1, 500_000)):
    r = [S.roda((mec, d, X, k))["alarme_correto"] for k in range(100, 120)] if mec in S.DET else [S.roda((mec, d, X, 100))["alarme_correto"]]
    g = pd.read_csv(f"{OP}/resultados/sim_2026_grade.csv"); gg = g[(g.mecanismo == mec) & (g.sentido == ("Flavio→Lula" if d == 1 else "Lula→Flavio")) & (g.X == X)].poder.iloc[0]
    est[f"{mec}|{d}|{X}"] = {"poder_grade": float(gg), "poder_sementes_novas": float(np.mean(r)), "n": len(r)}
out["estabilidade_t63_2026"] = est
json.dump(out, open(f"{OP}/resultados/auditoria_final.json", "w"), ensure_ascii=False, indent=1, default=float); print(json.dumps(out, ensure_ascii=False, indent=1, default=float))
