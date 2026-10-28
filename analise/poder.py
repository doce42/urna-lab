"""Teste de poder: injeta fraudes sintéticas no 2º turno real e mede quais testes detectam.

Cenários (sempre tirando votos de um candidato e dando ao outro, ou enchendo urna):
  - troca em urnas sorteadas no país (fração de urnas x % dos válidos movidos)
  - troca em todas as urnas de um estado
  - troca uniforme em todas as urnas do país
  - enchimento: votos extras para um candidato usando os eleitores que faltaram
Testes (os mesmos usados na análise):
  T1 seções fora do padrão do município (|z robusto| > 5 no sentido da fraude)
  T2 curva real x prevista pelo 1º turno com a virada do ESTADO (maior desvio, pp)
  T3 impressão digital: seções com comparecimento >= 95% e >= 90% para o beneficiado
  T4 virada do estado fora do esperado pelo perfil dele no 1º turno (% do Lula e voto órfão de candidatos eliminados).
     Sem o voto órfão, Goiás acusava sozinho nos dados reais (Caiado teve 12% lá): por isso ele entra no modelo.
"""
import json
import os

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(42)
b = pd.read_parquet(os.path.join(AQUI, "base.parquet"))
b = b[(b["validos_1"] >= 20) & (b["validos_2"] >= 20)].reset_index(drop=True)
b["mun"] = b["SG_UF"] + b["CD_MUNICIPIO"]
b = b.sort_values("DT_BU_RECEBIDO_2").reset_index(drop=True)
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
inv = lambda z: 1 / (1 + np.exp(-z))
L1, V1 = b["v13_1"].values.astype(float), b["validos_1"].values.astype(float)
ORF = 1 - (b["v13_1"].values + b["v22_1"].values) / V1  # voto de candidatos eliminados no 1º turno
mun = pd.factorize(b["mun"])[0]
uf = b["SG_UF"].values
minuto = b["DT_BU_RECEBIDO_2"].dt.floor("1min").values


def testes(L2, V2, comp2, aptos):
    sw = lg(L2, V2) - lg(L1, V1)
    s = pd.Series(sw)
    res = sw - s.groupby(mun).transform("median").values
    sd = np.sqrt(1/(L1+.5) + 1/(V1-L1+.5) + 1/(L2+.5) + 1/(V2-L2+.5))
    z = res / sd
    zr = z / (1.4826 * np.median(np.abs(z - np.median(z))))
    t1 = int((zr > 5).sum())
    sw_uf = s.groupby(uf).transform("median").values
    prev = inv(lg(L1, V1) + sw_uf) * V2
    df = pd.DataFrame({"m": minuto, "L": L2, "P": prev, "V": V2}).groupby("m").sum().cumsum()
    t2 = float(100 * ((df.L - df.P) / df.V).abs().max())
    t3 = int(((comp2 / aptos >= .95) & (L2 / V2 >= .9)).sum())
    # T4: o estado virou diferente do que o 1º turno dele indicaria pela relação nacional (regressão virada x % no 1º)
    e = pd.DataFrame({"uf": uf, "sw": sw, "p1": L1 / V1, "o": ORF}).groupby("uf").median().drop("ZZ", errors="ignore")
    X = np.column_stack([np.ones(len(e)), e.p1, e.p1 ** 2, e.o])
    r = e.sw - X @ np.linalg.lstsq(X, e.sw, rcond=None)[0]
    t4 = float(np.abs((r - r.median()) / (1.4826 * np.median(np.abs(r - r.median())))).max())
    return t1, t2, t3, t4


L2r, V2r = b["v13_2"].values.astype(float), b["validos_2"].values.astype(float)
F2r = b["v22_2"].values.astype(float)
comp, aptos = b["QT_COMPARECIMENTO_2"].values.astype(float), b["QT_APTOS_2"].values.astype(float)
base = testes(L2r, V2r, comp, aptos)
lim = (base[0] + max(5, 5 * np.sqrt(base[0])), base[1] * 3, base[2] + max(5, 5 * np.sqrt(base[2])), 3.5)
print(f"dados reais (sem fraude): T1 {base[0]}  T2 {base[1]:.2f} pp  T3 {base[2]}  T4 {base[3]:.2f}")
print(f"limiar de alarme:          T1 >{lim[0]:.0f}  T2 >{lim[1]:.2f} pp  T3 >{lim[2]:.0f}  T4 >{lim[3]}\n")
total_val = V2r.sum()
LINHAS = []


def roda(nome, sel, frac_votos=None, encher=None):
    L2, F2, V2, c = L2r.copy(), F2r.copy(), V2r.copy(), comp.copy()
    if frac_votos is not None:
        mov = np.minimum(np.round(V2[sel] * frac_votos), F2[sel])
        L2[sel] += mov; F2[sel] -= mov
        votos = mov.sum()
    else:
        add = np.round((aptos[sel] - c[sel]) * encher)
        L2[sel] += add; V2[sel] += add; c[sel] += add
        votos = add.sum()
    t = testes(L2, V2, c, aptos)
    det = [t[i] > lim[i] for i in range(4)]
    margem = 100 * votos / total_val
    LINHAS.append({"cenario": nome.strip(), "grupo": GRUPO, "votos": int(votos), "pct_validos": round(margem, 3),
                   "T1": t[0], "T2": round(t[1], 3), "T3": t[2], "T4": round(t[3], 2), "detectou": det, "algum": any(det)})
    marca = lambda d: "SIM" if d else " - "
    print(f"{nome:46} | {int(votos):>9,} votos ({margem:4.2f}% dos válidos) | T1 {t[0]:>6} {marca(det[0])} | "
          f"T2 {t[1]:5.2f} {marca(det[1])} | T3 {t[2]:>5} {marca(det[2])} | T4 {t[3]:5.2f} {marca(det[3])} | "
          f"{'DETECTADA' if any(det) else 'passou batido'}")


N = len(b)
print("== Troca de votos (Flávio -> Lula) em urnas sorteadas no país")
GRUPO = "Troca de votos (Flávio -> Lula) em urnas sorteadas no país"
for f in (0.001, 0.01, 0.05, 0.20):
    for m in (0.02, 0.05, 0.10, 0.20):
        sel = rng.random(N) < f
        roda(f"{100*f:>4.1f}% das urnas, {100*m:>2.0f}% dos válidos", sel, frac_votos=m)
print("\n== Troca em todas as urnas de um estado")
GRUPO = "Troca em todas as urnas de um estado"
for e in ("BA", "MG", "SP", "PR"):
    for m in (0.01, 0.02, 0.05):
        roda(f"todas as urnas de {e}, {100*m:.0f}% dos válidos", uf == e, frac_votos=m)
print("\n== Troca uniforme no país inteiro")
GRUPO = "Troca uniforme no país inteiro"
for m in (0.005, 0.01, 0.02):
    roda(f"todas as urnas, {100*m:.1f}% dos válidos", np.ones(N, bool), frac_votos=m)
print("\n== Enchimento de urna (eleitores que faltaram 'votando' no Lula)")
GRUPO = "Enchimento de urna (eleitores que faltaram 'votando' no Lula)"
for f in (0.001, 0.01, 0.05):
    for k in (0.5, 1.0):
        roda(f"{100*f:.1f}% das urnas, {100*k:.0f}% das abstenções", rng.random(N) < f, encher=k)

json.dump({"base": {"T1": base[0], "T2": base[1], "T3": base[2], "T4": base[3]},
           "limiar": {"T1": lim[0], "T2": lim[1], "T3": lim[2], "T4": lim[3]},
           "margem_real_votos": int(L2r.sum() - F2r.sum()), "linhas": LINHAS},
          open(os.path.join(AQUI, "resultado_poder.json"), "w"), ensure_ascii=False, indent=1, default=int)
