"""T63 (B2, v2): fabricante de estrutura completa com efeitos centrados e correção do total municipal (emenda 4 do protocolo).
Uso: sim_fabricacao_v2.py <ano> [reps]"""
import hashlib, json, sys
import numpy as np, pandas as pd
ANO = sys.argv[1]; REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 20
sys.argv = ["x", ANO, "1", "1"]
sys.path.insert(0, "operacao_veracidade/scripts")
import sim_adversarial as S  # noqa: E402  (calcula base, limiares e detectores; o main não roda)
OP = S.OP


def centra(u, grupo, n_grupo, peso=None):
    """subtrai de u a média (por seção) do grupo"""
    return u - (np.bincount(grupo, u, n_grupo) / np.maximum(np.bincount(grupo, minlength=n_grupo), 1))[grupo]


def fab(ab, rep, parcial=False):
    a, b = ab
    rng = np.random.default_rng(int(hashlib.sha256(f"{ANO}|fab2|{rep}".encode()).hexdigest()[:12], 16))
    N, nm, nz, nl = S.N, S.nm, S.nz, S.nl
    swm = S.lg(np.bincount(S.mun, S.L2, nm), np.bincount(S.mun, S.V2, nm)) - S.base_logit1_m
    e = np.sqrt(np.maximum((S.S0 * S.SE_B) ** 2 - a ** 2 - b ** 2, .05 * (S.S0 * S.SE_B) ** 2))
    uz = rng.normal(0, b, nz)[S.zon]; uz = centra(uz, S.mun, nm)                 # zona centrada no município
    ul = rng.normal(0, a, nl)[S.loc]; ul = centra(ul, S.zon, nz)                 # local centrado na zona
    eta = S.lg(S.L1, S.V1) + swm[S.mun] + uz + ul + rng.normal(0, 1, N) * e
    p = 1 / (1 + np.exp(-eta)); L = S.V2 * p
    # uma iteração de correção: o total municipal fabricado volta ao total municipal real
    fab_m = S.lg(np.bincount(S.mun, L, nm), np.bincount(S.mun, S.V2, nm)); real_m = S.lg(np.bincount(S.mun, S.L2, nm), np.bincount(S.mun, S.V2, nm))
    p = 1 / (1 + np.exp(-(eta + (real_m - fab_m)[S.mun]))); L = np.floor(S.V2 * p + rng.random(N))
    t = S.det_valores(L, S.V2, S.T2)
    r = {"escala_z": t["escala_z"], "esc_local_rel": t["esc_local"] / S.ESC_LOC0, "esc_zona_rel": t["esc_zona"] / S.ESC_ZON0}
    if parcial:
        return r
    r.update({"ano": ANO, "cenario": "fabricada_calibrada_estrutura_v2", "rep": rep, "d5_alarme": t["d5_p"] < 1e-3, "d6_subdispersao": bool(t["escala_z"] < .85 or t["escala_z"] > 1.15),
              "d7_estrutura_local": bool(not (.8 <= r["esc_local_rel"] <= 1.25) or not (.8 <= r["esc_zona_rel"] <= 1.25)),
              "margem_nacional": float(L.sum() - (S.V2.sum() - L.sum())), "margem_real": float(S.L2.sum() - S.F2.sum())})
    for k in ("d1_pos_4", "d1_neg_4", "d2l_pos", "d2l_neg", "d2z_pos", "d2z_neg", "d3_pos", "d3_neg", "d4_pos"):
        r[k] = bool(t[k] > S.LIM[k])
    r["alarme_qualquer_lado"] = any(r[k] for k in ("d1_pos_4", "d1_neg_4", "d2l_pos", "d2l_neg", "d2z_pos", "d2z_neg", "d3_pos", "d3_neg", "d4_pos"))
    return r


G = [0, .005, .01, .02, .03, .05, .075, .1, .15, .2, .3]
melhor = (1e9, None)
for a in G:
    for b in G:
        r = fab((a, b), 20_000 + int(a * 1000) * 1000 + int(b * 1000), parcial=True)
        c = abs(np.log(r["escala_z"])) + abs(np.log(r["esc_local_rel"])) + abs(np.log(r["esc_zona_rel"]))
        if c < melhor[0]: melhor = (c, (a, b))
df = pd.DataFrame([fab(melhor[1], r) for r in range(REPS)]); df.to_csv(f"{OP}/resultados/sim_{ANO}_fabricada_v2.csv", index=False)
cols = ["d1_pos_4", "d1_neg_4", "d2l_pos", "d2l_neg", "d2z_pos", "d2z_neg", "d3_pos", "d3_neg", "d4_pos", "d5_alarme", "d6_subdispersao", "d7_estrutura_local", "alarme_qualquer_lado"]
out = {"ano": ANO, "custo_ab": melhor[0], "a_local": melhor[1][0], "b_zona": melhor[1][1], "reps": REPS, "alarmes": df[cols].mean().round(2).to_dict(),
       "escalas_relativas": {"z": float(df.escala_z.mean()), "local": float(df.esc_local_rel.mean()), "zona": float(df.esc_zona_rel.mean())}, "margem_nacional_media": float(df.margem_nacional.mean()), "margem_real": float(df.margem_real.iloc[0])}
json.dump(out, open(f"{OP}/resultados/sim_{ANO}_fabricada_v2.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
