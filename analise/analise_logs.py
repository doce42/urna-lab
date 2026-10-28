"""Testes sobre a sequência dos logs das urnas (T28–T31, T33), modelo de urna (T20) e confirmação, em dados
independentes (logs), dos achados exploratórios das tabelas (cauda do T02).

Uso: python analise_logs.py <turno>        (precisa de analise/brutos/<t>t/urnas_*.parquet com as colunas seq_*)
Saída: resultado_logs_<t>t.json

T28  rajada de habilitações sem biometria no fim do dia: por urna, nº de habilitações não biométricas (biográfica +
     sem biometria cadastrada + manual) nos últimos 30 min x o esperado pela taxa da própria urna no resto do dia
     (binomial); z por urna; Benjamini-Hochberg; distribuição e relação com a virada
T29  durações habilitação → voto e intervalo mínimo entre votos (física: votar leva segundos)
T30  votos fora do dia da eleição
T31  votos sem habilitação anterior
T33  versões de software e verificações de assinatura de software sem sucesso
T20  modelo de urna (log) x virada, dentro do município (2º turno)
CONF seções da cauda do T02 (|z| > 5) x demais, nas variáveis do log
"""
import glob
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
T = int(sys.argv[1]) if len(sys.argv) > 1 else 2
arqs = glob.glob(os.path.join(AQUI, "brutos", f"{T}t", "urnas_*.parquet"))
u = pd.concat([pd.read_parquet(a) for a in arqs], ignore_index=True)
if "seq_votos_dia" not in u:
    sys.exit("sem colunas seq_* (rode processar_brutos.py com a versão que lê a sequência do log)")
R = {"turno": T, "urnas": int(len(u)), "urnas_com_sequencia": int(u["seq_votos_dia"].notna().sum())}
u = u[u["seq_votos_dia"].notna()].copy()


def bh(p, q=0.05):
    p = np.asarray(p); n = len(p); o = np.argsort(p)
    passa = p[o] <= q * np.arange(1, n + 1) / n
    k = np.max(np.where(passa)[0]) + 1 if passa.any() else 0
    s = np.zeros(n, bool); s[o[:k]] = True
    return s


# T28
ult, ult_sb = u["seq_ult30_votos"].fillna(0), u["seq_ult30_sem_biometria"].fillna(0)
res, res_sb = u["seq_resto_votos"].fillna(0), u["seq_resto_sem_biometria"].fillna(0)
taxa = (res_sb + 0.5) / (res + 1)                       # taxa da própria urna no resto do dia (suavizada)
esp = ult * taxa
sd = np.sqrt(np.maximum(ult * taxa * (1 - taxa), 1e-9))
u["z28"] = np.where(ult > 0, (ult_sb - esp) / sd, 0.0)
p28 = stats.binom.sf(ult_sb - 1, ult.astype(int), taxa)  # P(X >= observado)
u["sig28"] = bh(np.where(ult > 0, p28, 1.0))
R["T28"] = {"urnas_com_votos_nos_ultimos_30min": int((ult > 0).sum()),
            "taxa_sem_biometria_resto_do_dia": float(res_sb.sum() / res.sum()),
            "taxa_sem_biometria_ultimos_30min": float(ult_sb.sum() / max(ult.sum(), 1)),
            "urnas_significativas_BH": int(u["sig28"].sum()),
            "z28_percentis": {q: float(np.percentile(u["z28"], q)) for q in (50, 90, 99, 99.9)},
            "exemplos": u.loc[u["sig28"]].sort_values("z28", ascending=False)[
                ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "seq_ult30_votos", "seq_ult30_sem_biometria", "seq_resto_votos", "seq_resto_sem_biometria", "z28"]
            ].head(15).to_dict("records")}

# T29
d = u["seq_dur_min"].dropna()
R["T29"] = {"duracao_min_global_s": float(d.min()), "duracao_min_p01_s": float(np.percentile(d, 1)),
            "urnas_com_algum_voto_abaixo_5s": int((u["seq_dur_abaixo_5s"].fillna(0) > 0).sum()),
            "votos_abaixo_5s": int(u["seq_dur_abaixo_5s"].fillna(0).sum()),
            "intervalo_min_entre_votos_s_p01": float(np.percentile(u["seq_intervalo_min"].dropna(), 1)),
            "intervalo_min_entre_votos_s_min": float(u["seq_intervalo_min"].min())}
# T30, T31
# o log do 2º turno traz arquivado o do 1º (e testes de preparação): "fora do dia" cru NÃO é achado. O teste válido é o
# horário do voto dentro do dia da eleição: votos antes das 07h00 locais e depois do encerramento (+ prorrogação)
R["T30"] = {"votos_fora_do_dia_cru_NAO_USAR": int(u["seq_votos_fora_dia"].sum()),
            "votos_antes_das_7h_locais_no_dia": int(u["seq_votos_antes_7h"].sum()),
            "urnas_com_voto_antes_das_7h": int((u["seq_votos_antes_7h"] > 0).sum())}
R["T31"] = {"votos_sem_habilitacao": int(u["seq_sem_habilitacao"].sum()), "urnas": int((u["seq_sem_habilitacao"] > 0).sum())}
# T33
R["T33"] = {"versoes": u["sw_versoes"].value_counts().to_dict(),
            "urnas_com_verificacao_sem_sucesso": int((u["sw_verif_falha"] > 0).sum()),
            "verificacoes_sem_sucesso": int(u["sw_verif_falha"].sum()), "verificacoes_ok": int(u["sw_verif_ok"].sum())}

# T20 e CONF precisam da virada (base)
b = pd.read_parquet(os.path.join(AQUI, "base.parquet"))
b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20)].copy()
b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
x1, n1, x2, n2 = b["v13_1"], b["validos_1"], b["v13_2"], b["validos_2"]
b["sw"] = lg(x2, n2) - lg(x1, n1)
b["res"] = b["sw"] - b.groupby("mun")["sw"].transform("median")
z = b["res"] / np.sqrt(1/(x1+.5) + 1/(n1-x1+.5) + 1/(x2+.5) + 1/(n2-x2+.5))
b["z"] = z / (1.4826 * (z - z.median()).abs().median())
m = u.merge(b[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "z", "res", "mun", "QT_APTOS_2", "QT_COMPARECIMENTO_2", "v13_2", "validos_2"]],
            on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"], how="inner")
if T == 2:
    # T20: modelo de urna x virada dentro do município (diferença de cada modelo para a média do município)
    m["res_mun"] = m["res"] - m.groupby("mun")["res"].transform("mean")
    R["T20"] = {k: {"urnas": int(len(g)), "residuo_medio": float(g["res_mun"].mean()),
                    "ic95": [float(g["res_mun"].mean() - 1.96 * g["res_mun"].std() / np.sqrt(len(g))),
                             float(g["res_mun"].mean() + 1.96 * g["res_mun"].std() / np.sqrt(len(g)))]}
                for k, g in m.groupby("modelo")}
    R["T20"]["kruskal_p"] = float(stats.kruskal(*[g["res_mun"].values for _, g in m.groupby("modelo")]).pvalue)
# CONF: cauda do T02 x demais
m["sem_bio_frac"] = (m["seq_hab_mesario"] + m["seq_hab_outro"] + m["seq_hab_manual"]) / m["seq_votos_dia"].clip(lower=1)
comp2 = m["QT_COMPARECIMENTO_2"] / m["QT_APTOS_2"] if "QT_COMPARECIMENTO_2" in m else None
grupos = {"cauda_pro_lula_z>5": m["z"] > 5, "cauda_pro_adversario_z<-5": m["z"] < -5, "demais": m["z"].abs() <= 5}
if comp2 is not None:  # zona de alerta de Klimek (comparecimento e % Lula >= 90%): mais seções em 2026 que em 2022
    grupos["zona_klimek_lula_90_90"] = (comp2 >= 0.9) & (m["v13_2"] / m["validos_2"] >= 0.9)
R["CONF_T02"] = {}
for nome, sel in grupos.items():
    g = m[sel]
    R["CONF_T02"][nome] = {"secoes": int(len(g)), "eleitores_mediana": float(g["QT_APTOS_2"].median()),
                           "frac_sem_biometria_mediana": float(g["sem_bio_frac"].median()),
                           "z28_mediana": float(g["z28"].median()), "urnas_sig28": int(g["sig28"].sum()),
                           "duracao_mediana_s": float(g["seq_dur_mediana"].median()),
                           "votos_abaixo_5s": int(g["seq_dur_abaixo_5s"].fillna(0).sum()),
                           "urna_substituida": int((g["urnas_com_voto_no_log"] > 1).sum()),
                           "lula_2t_mediana": float((g["v13_2"] / g["validos_2"]).median()),
                           "modelos": g["modelo"].value_counts().to_dict()}
cauda = m[m["z"] > 5].sort_values("z", ascending=False)
R["CONF_T02_lista"] = cauda[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "z", "QT_APTOS_2", "sem_bio_frac", "z28", "seq_dur_mediana", "modelo"]].head(40).to_dict("records")
json.dump(R, open(os.path.join(AQUI, f"resultado_logs_{T}t.json"), "w"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: v for k, v in R.items() if k not in ("CONF_T02_lista",) and not (isinstance(v, dict) and "exemplos" in v)}, ensure_ascii=False, indent=1, default=str)[:4000])
print("T28 exemplos:", R["T28"]["exemplos"][:3])
