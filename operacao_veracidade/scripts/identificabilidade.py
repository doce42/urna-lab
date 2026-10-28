"""T62: experimentos A e B de identificabilidade, sobre cópias sintéticas de colunas reais (MG, 2º turno de 2026).
Matriz: escopo da alteração × verificação de consistência. Protocolo: operacao_veracidade/PROTOCOLO_PRE_EXECUCAO.md."""
import json
import numpy as np, pandas as pd
R = "."; CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
UF = "MG"
b = pd.read_parquet(f"{R}/analise/base.parquet").astype({c: str for c in CH}); b = b[b.SG_UF == UF]
u = pd.read_parquet(f"{R}/analise/brutos/2t/urnas_{UF}.parquet", columns=CH + ["bu_v13", "bu_v22", "rdv_v13", "rdv_v22", "img_v13", "img_v22", "computado", "hash_ok_bu", "hash_ok_rdv", "assin_ok_bu", "assin_ok_rdv", "assin_lista_ok"]).astype({c: str for c in CH})
m = b.merge(u, on=CH).dropna(subset=["bu_v13", "rdv_v13", "img_v13"]).reset_index(drop=True)
rng = np.random.default_rng(20261028)
alvo = rng.random(len(m)) < .05; V = (m.v13_2 + m.v22_2).values
x = np.minimum(np.floor(.10 * V), m.v22_2.values) * alvo           # 10% dos válidos de Flávio → Lula em 5% das seções
tot_votos = int(x.sum())
tab13, tab22 = m.v13_2.values.copy(), m.v22_2.values.copy()
rep = {"tab": (tab13, tab22), "bu": (m.bu_v13.values.astype(float), m.bu_v22.fillna(0).values.astype(float)), "rdv": (m.rdv_v13.values.astype(float), m.rdv_v22.fillna(0).values.astype(float)),
       "img": (m.img_v13.values.astype(float), m.img_v22.fillna(0).values.astype(float))}
log = m.computado.values.astype(float); comp = m.QT_COMPARECIMENTO_2.values.astype(float)


def alterado(quais, stuffing=False):
    r = {k: (a.copy(), c.copy()) for k, (a, c) in rep.items()}
    for k in quais:
        if k in r:
            r[k][0][:] += x; r[k][1][:] -= (0 if stuffing else x)
    lg = log + (x if stuffing and "log" in quais else 0)
    return r, lg


def checa(r, lg, tab_comp_alterado=False, modificados_apos_assinar=()):
    c1 = ((r["tab"][0] != r["bu"][0]) | (r["tab"][1] != r["bu"][1]))
    c2 = ((r["bu"][0] != r["rdv"][0]) | (r["bu"][1] != r["rdv"][1]))
    c3 = ((r["bu"][0] != r["img"][0]) | (r["bu"][1] != r["img"][1]))
    comp_a = comp + (x if tab_comp_alterado else 0)
    c4 = lg != comp_a                                              # log × comparecimento: o log conta todo voto, qualquer candidato
    c5 = np.full(len(m), bool(modificados_apos_assinar)) & alvo    # hash do arquivo × lista assinada: falha se o arquivo foi mexido sem reassinar
    return {"C1_tabela=BU": int(c1.sum()), "C2_BU=RDV": int(c2.sum()), "C3_BU=imagem": int(c3.sum()), "C4_log=comparecimento": int(c4.sum()), "C5_hash_x_lista_assinada": int(c5.sum()),
            "C6_assinatura_e_cadeia": 0}


# controle: sem alteração (todas as verificações devem dar 0)
r0, l0 = alterado([]); out = {"uf": UF, "secoes": int(len(m)), "secoes_alteradas": int(alvo.sum()), "votos_movidos_de_flavio_para_lula": tot_votos, "semente": 20261028, "cenarios": {}}
out["cenarios"]["0_sem_alteracao"] = checa(r0, l0)
cen = {"A1_so_tabela": (["tab"], (), False),
       "A2_tabela_e_BU_sem_reassinar": (["tab", "bu"], ("bu",), False),
       "A3_BU_e_RDV_sem_tabela_sem_reassinar": (["bu", "rdv"], ("bu", "rdv"), False),
       "A4_tabela_BU_RDV_imagem_sem_reassinar": (["tab", "bu", "rdv", "img"], ("bu", "rdv", "img"), False),
       "B1_tudo_regenerado_e_assinado_pelo_gerador (voto trocado)": (["tab", "bu", "rdv", "img"], (), False),
       "B2_tudo_regenerado_e_assinado_pelo_gerador (enchimento: comparecimento sobe)": (["tab", "bu", "rdv", "img", "log"], (), True)}
for nome, (quais, mod, stuff) in cen.items():
    r, lg = alterado(quais, stuffing=stuff)
    if stuff:                                                     # enchimento: o voto novo vem da abstenção; ninguém subtrai de Flávio
        for k in quais:
            if k in r: r[k][1][:] = rep[k][1]
    out["cenarios"][nome] = checa(r, lg, tab_comp_alterado=stuff and "tab" in quais, modificados_apos_assinar=mod)
out["nota"] = ("B1 e B2 representam registros internamente coerentes gerados por um gerador comprometido (assinados pela própria urna): nenhuma consistência interna os separa de registros genuínos. "
               "Isso mede o limite de identificabilidade e não a possibilidade operacional de comprometer urnas reais.")
json.dump(out, open(f"{R}/operacao_veracidade/resultados/identificabilidade.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
