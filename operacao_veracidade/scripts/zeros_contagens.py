"""T64: seções com zero e poucos votos (2022 e 2026) + modelo beta-binomial com UF retida. Critério fixado antes (PROTOCOLO_PRE_EXECUCAO.md)."""
import json
import numpy as np, pandas as pd
from scipy.special import gammaln

R = "."; AN = R + "/analise"
CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
out = {"descritivo": {}, "modelo": {}}
rng = np.random.default_rng(64)
for ano, arq in (("2022", "base_2022.parquet"), ("2026", "base.parquet")):
    b = pd.read_parquet(f"{AN}/{arq}"); b = b[b.SG_UF != "ZZ"].copy()
    b["mun"] = b.SG_UF + "|" + b.CD_MUNICIPIO.astype(str)
    for t in (1, 2):
        c = b[b[f"total_{t}"] > 0]
        for nome, col in (("Lula", f"v13_{t}"), ("Direita", f"v22_{t}")):
            x = c[col].fillna(0)
            d = {"secoes_com_comparecimento": int(len(c)), "zero": int((x == 0).sum()), "um": int((x == 1).sum()), "dois": int((x == 2).sum()), "tres_a_cinco": int(x.between(3, 5).sum()),
                 "votos_dos_zeros_do_outro": int(c.loc[x == 0, f"v{'22' if col.startswith('v13') else '13'}_{t}"].sum())}
            if t == 2:
                z = c[x == 0]; col1 = col.replace("_2", "_1")
                d["dos_zeros_tambem_zero_no_1t"] = int((z[col1].fillna(0) == 0).sum()); d["por_uf_top5"] = z.SG_UF.value_counts().head(5).to_dict()
            out["descritivo"][f"{ano}_{t}t_{nome}"] = d
    # ---- modelos: só 2º turno; 3 famílias = o nível em que a participação esperada é estimada (município, zona, local de votação) ----
    b["zon"] = b.mun + "|" + b.NR_ZONA.astype(str); b["loc"] = b.zon + "|" + b.NR_LOCAL_VOTACAO_2.astype(str)
    for nivel, grosso in (("municipio", "SG_UF"), ("zona", "mun"), ("local", "zon")):
        chave = {"municipio": "mun", "zona": "zon", "local": "loc"}[nivel]
        for nome, col in (("Lula", "v13_2"), ("Direita", "v22_2")):
            c = b[(b.validos_2 > 0)].copy(); c["x"] = c[col].fillna(0); c["n"] = c.validos_2
            g1x = c.groupby(chave).x.transform("sum"); g1n = c.groupby(chave).n.transform("sum"); g2x = c.groupby(grosso).x.transform("sum"); g2n = c.groupby(grosso).n.transform("sum")
            d1 = g1n - c.n; d2 = g2n - c.n
            p_fino = np.where(d1 > 0, (g1x - c.x) / d1.where(d1 > 0, 1), np.nan); p_gros = np.where(d2 > 0, (g2x - c.x) / d2.where(d2 > 0, 1), c.groupby("SG_UF").x.transform("sum") / c.groupby("SG_UF").n.transform("sum"))
            c["p"] = np.where(np.isnan(p_fino), p_gros, p_fino).clip(1e-4, 1 - 1e-4)
            mom = ((c.x - c.n * c.p) ** 2 - c.n * c.p * (1 - c.p)); dn = c.n * c.p * (1 - c.p) * (c.n - 1).clip(lower=1)
            ok = (c.n >= 2) & (c.p.between(.02, .98))
            A = mom[ok].groupby(c.SG_UF[ok]).sum(); B = dn[ok].groupby(c.SG_UF[ok]).sum()
            linhas, dentro, elegiveis = [], 0, 0
            for u in sorted(c.SG_UF.unique()):
                rho = float(np.clip((A.sum() - A.get(u, 0)) / (B.sum() - B.get(u, 0)), 1e-6, .999))
                s = c[c.SG_UF == u]; a = s.p * (1 / rho - 1); bb = (1 - s.p) * (1 / rho - 1)
                p0 = np.exp(gammaln(bb + s.n) + gammaln(a + bb) - gammaln(bb) - gammaln(a + bb + s.n))
                esp = float(p0.sum()); obs = int((s.x == 0).sum())
                idx = np.where(p0 > 1e-7)[0]; sim = np.zeros(500)
                if len(idx):
                    for k in range(0, 500, 50):
                        pp = rng.beta(a.values[idx][None, :], bb.values[idx][None, :], size=(50, len(idx))); xs = rng.binomial(s.n.values[idx][None, :].astype(int), pp)
                        sim[k:k + 50] = (xs == 0).sum(axis=1)
                lo, hi = np.percentile(sim, [2.5, 97.5]); linhas.append({"uf": u, "rho": rho, "esperado": esp, "observado": obs, "pi95": [float(lo), float(hi)], "dentro": bool(lo <= obs <= hi)})
                if esp >= 1:
                    elegiveis += 1; dentro += int(lo <= obs <= hi)
            frac = dentro / elegiveis if elegiveis else None
            out["modelo"][f"{nivel}_{ano}_{nome}"] = {"ufs_elegiveis_esperado_ge_1": elegiveis, "ufs_dentro_do_pi95": dentro, "fracao": frac, "adequado": bool(frac is not None and frac >= .8),
                                                       "zeros_observados": int(sum(l["observado"] for l in linhas)), "zeros_esperados": round(float(sum(l["esperado"] for l in linhas)), 1),
                                                       "ufs_fora": [l for l in linhas if (l["esperado"] >= 1 and not l["dentro"])][:12], "rho_mediano": float(np.median([l["rho"] for l in linhas]))}
json.dump(out, open(f"{R}/operacao_veracidade/resultados/zeros_contagens.json", "w"), ensure_ascii=False, indent=1)
for k, v in out["descritivo"].items(): print(k, {a: b for a, b in v.items() if a != "por_uf_top5"})
for k, v in out["modelo"].items(): print(k, {a: b for a, b in v.items() if a not in ("ufs_fora",)})
