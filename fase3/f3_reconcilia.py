"""F3 / R1-20: reconciliação seção a seção dos votos de Presidente da base do projeto com o DataUrnas-BR (decodificação independente, terceiro)."""
import json, re
import numpy as np, pandas as pd
import hashlib, os, subprocess, sys
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
# clone do DataUrnas-BR fora do repositório (355 MB); caminho por variável de ambiente
DU = os.environ.get("DATAURNAS_DIR", "./externos/DataUrnas-BR"); P = DU + "/data/parquet/"
COMMIT = "12f0433bd20882d305dd7b9e4987d6dcf3b321a9"   # commit usado na execução original (28/10/2026)
SHA = {"2026/votos_presidente_2026.parquet": "b5654e7b692e2cf2eddb818be2365affd99b613ad17757c3b88f88430114d422",
       "2026/secoes_2026.parquet": "cb0e3ecfdc13e14de77be40b87040983d55b26675f2c497474b4543473b30916",
       "votos_t1_a.parquet": "fcb78b9c6be25ea78bbb208175d4242ff4bbc3598507759a6e7726fffe418176",
       "votos_t1_b.parquet": "d4cb49542cd65c11d916a348d4aaedc8d19f2db24cbc421c4a35d7a945aca303",
       "votos_t2.parquet": "97fe1abcdbd88c30de14e2d5f47076de119a8c7c980ab863dc69111aeae6fc80",
       "totais_cargo.parquet": "d63b224cb9645dc2c68598e513e40b677c303e207f15839fc6fbcba39846db61"}
head = subprocess.run(["git", "-C", DU, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
if head != COMMIT: sys.exit(f"DataUrnas-BR em {head}, esperado {COMMIT}: git -C {DU} checkout {COMMIT}")
for f, h in SHA.items():
    if hashlib.sha256(open(P + f, "rb").read()).hexdigest() != h: sys.exit(f"SHA-256 diferente em {f}")
SAIDA = sys.argv[1] if len(sys.argv) > 1 else "R1_20_dataurnas.json"
R = {"pergunta": "R1-20 reconciliação com DataUrnas-BR", "fonte": "github.com/alissonlinneker/DataUrnas-BR (terceiro; clone raso, sem baixar arquivos do TSE)",
     "commit": COMMIT, "sha256_entradas": SHA, "resultados": {}}


def compara(nome, ours, theirs, cols):
    """ours/theirs: DataFrames com chave k e colunas de votos (mesmos nomes)."""
    o = ours.set_index("k"); t = theirs.set_index("k")
    so, st = set(o.index), set(t.index)
    comuns = sorted(so & st)
    solo_o, solo_t = so - st, st - so
    d = (o.loc[comuns, cols] - t.loc[comuns, cols]).fillna(0)
    dif = d[(d != 0).any(axis=1)]
    res = {"secoes_nossas": len(so), "secoes_deles": len(st), "em_comum": len(comuns), "so_nossas": len(solo_o), "so_deles": len(solo_t),
           "secoes_com_diferenca": int(len(dif)), "soma_abs_diferenca_votos": int(d.abs().sum().sum()),
           "votos_nossos_em_comum": int(o.loc[comuns, cols].sum().sum()), "votos_deles_em_comum": int(t.loc[comuns, cols].sum().sum())}
    res["exemplos_diferenca"] = [{"k": k, **{c: int(d.loc[k, c]) for c in cols if d.loc[k, c] != 0}} for k in dif.index[:8]]
    res["exemplos_so_nossas"] = sorted(solo_o)[:5]; res["exemplos_so_deles"] = sorted(solo_t)[:5]
    # votos nas seções que só um lado tem
    res["votos_so_nossas"] = int(o.loc[sorted(solo_o), cols].fillna(0).sum().sum()) if solo_o else 0
    res["votos_so_deles"] = int(t.loc[sorted(solo_t), cols].fillna(0).sum().sum()) if solo_t else 0
    R["resultados"][nome] = res
    print(nome, {k: v for k, v in res.items() if not k.startswith("exemplos")})


# 2026 1º turno: candidatos 13,14,16,...: usa as colunas v*_1 da base
b = pd.read_parquet(f"{RAIZ}/analise/base.parquet")
v = pd.read_parquet(P + "2026/votos_presidente_2026.parquet")
v = v[v.tipo_voto == "nominal"].copy(); v["numero"] = v.numero.astype(int)
piv = v.pivot_table(index=["uf", "cd_mun", "zona", "secao"], columns="numero", values="votos", aggfunc="sum").fillna(0)
piv.columns = [f"v{c}_1" for c in piv.columns]
piv = piv.reset_index(); piv["k"] = piv.uf.str.upper() + "/" + piv.cd_mun.astype(int).astype(str) + "/" + piv.zona.astype(int).astype(str) + "/" + piv.secao.astype(int).astype(str)
b = b[b.total_1.notna()].copy()
b["k"] = b.SG_UF + "/" + b.CD_MUNICIPIO.astype(int).astype(str) + "/" + b.NR_ZONA.astype(int).astype(str) + "/" + b.NR_SECAO.astype(int).astype(str)
cols = sorted(set(piv.columns) & set(b.columns) - {"k"}); cols = [c for c in cols if re.fullmatch(r"v\d+_1", c)]
R["colunas_2026"] = cols
compara("2026_1T_nominais", b[["k"] + cols].drop_duplicates("k"), piv[["k"] + cols].drop_duplicates("k"), cols)
# brancos e nulos: tabela secoes_2026
s = pd.read_parquet(P + "2026/secoes_2026.parquet")
s = s[s.votos_total.notna()].copy(); s["k"] = s.uf.str.upper() + "/" + s.cd_mun.astype(int).astype(str) + "/" + s.zona.astype(int).astype(str) + "/" + s.secao.astype(int).astype(str)
s = s.rename(columns={"votos_brancos": "branco_1", "votos_nulos": "nulo_1"})
compara("2026_1T_brancos_nulos", b[["k", "branco_1", "nulo_1"]].drop_duplicates("k"), s[["k", "branco_1", "nulo_1"]].drop_duplicates("k"), ["branco_1", "nulo_1"])

# 2022: presidente turnos 1 e 2
b2 = pd.read_parquet(f"{RAIZ}/analise/base_2022.parquet")
frames = {1: [pd.read_parquet(P + "votos_t1_a.parquet"), pd.read_parquet(P + "votos_t1_b.parquet")], 2: [pd.read_parquet(P + "votos_t2.parquet")]}
tot = pd.read_parquet(P + "totais_cargo.parquet")
for t in (1, 2):
    x = pd.concat(frames[t]); x = x[(x.cargo == "Presidente") & (x.tipo_voto == "nominal")].copy()
    x["numero"] = x.codigo_candidato.astype(int)
    pv = x.pivot_table(index="secao_id", columns="numero", values="quantidade", aggfunc="sum").fillna(0)
    pv.columns = [f"v{c}_{t}" for c in pv.columns]; pv = pv.reset_index()
    sp = pv.secao_id.str.split("/", expand=True)
    pv["k"] = sp[1].str.upper() + "/" + sp[2].astype(int).astype(str) + "/" + sp[3].astype(int).astype(str) + "/" + sp[4].astype(int).astype(str)
    bb = b2[b2[f"total_{t}"].notna()].copy()
    bb["k"] = bb.SG_UF + "/" + bb.CD_MUNICIPIO.astype(int).astype(str) + "/" + bb.NR_ZONA.astype(int).astype(str) + "/" + bb.NR_SECAO.astype(int).astype(str)
    cc = [c for c in pv.columns if re.fullmatch(rf"v\d+_{t}", c) and c in bb.columns]
    R.setdefault("colunas_2022", {})[str(t)] = cc
    compara(f"2022_{t}T_nominais", bb[["k"] + cc].drop_duplicates("k"), pv[["k"] + cc].drop_duplicates("k"), cc)
    # brancos/nulos
    tc = tot[(tot.cargo == "Presidente") & tot.secao_id.str.startswith(f"{t}T/")].copy()
    sp = tc.secao_id.str.split("/", expand=True)
    tc["k"] = sp[1].str.upper() + "/" + sp[2].astype(int).astype(str) + "/" + sp[3].astype(int).astype(str) + "/" + sp[4].astype(int).astype(str)
    tc = tc.rename(columns={"brancos": f"branco_{t}", "nulos": f"nulo_{t}"})
    compara(f"2022_{t}T_brancos_nulos", bb[["k", f"branco_{t}", f"nulo_{t}"]].drop_duplicates("k"), tc[["k", f"branco_{t}", f"nulo_{t}"]].drop_duplicates("k"), [f"branco_{t}", f"nulo_{t}"])
json.dump(R, open(f"{RAIZ}/fase3/resultados/{SAIDA}", "w"), ensure_ascii=False, indent=1, default=str)
