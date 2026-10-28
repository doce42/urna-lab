"""Gera tabelas em markdown dos resultados do T63 (resultados/tabelas_sim.md)."""
import json
import numpy as np, pandas as pd
from scipy.stats import beta
R = "operacao_veracidade/resultados"
cp = lambda k, n: (beta.ppf(.025, k, n - k + 1) if k > 0 else 0.0, beta.ppf(.975, k + 1, n - k) if k < n else 1.0)
XS = [25_000, 50_000, 100_000, 250_000, 500_000, 1_000_000, 2_220_000]
NOMES = {"dispersa": "seções dispersas (3% dos válidos em cada)", "poucas_secoes": "poucas seções, alteração grande (40%)", "locais": "locais de votação inteiros (10%)", "zonas": "zonas inteiras (10%)",
         "municipios": "municípios inteiros, sem os 5 grandes (10%)", "cinco_grandes": "os 5 grandes municípios juntos", "ufs": "UFs inteiras (10%)", "macrorregiao": "macrorregião Nordeste",
         "reduto_alvo": "redutos do alvo (quintil)", "reduto_oponente": "redutos do oponente (quintil)", "uniforme": "uniforme em fatia de voto (proporcional)", "uniforme_logit": "uniforme em logit (H9)",
         "lote_tardio": "lote tardio de recebimento (40% das seções)", "enchimento": "enchimento (abstenção → finalista)", "bn_conversao": "conversão de brancos e nulos"}
out = []
for ano in ("2026", "2022"):
    g = pd.read_csv(f"{R}/sim_{ano}_grade.csv"); res = json.load(open(f"{R}/sim_{ano}_resumo.json"))
    out += [f"### Poder por mecanismo e magnitude, {ano} (% de réplicas com alarme na direção correta; Flávio→Lula / Lula→Flávio)", "",
            "| Mecanismo | " + " | ".join(f"{x/1000:.0f} mil" if x < 1e6 else f"{x/1e6:.2f} mi" for x in XS) + " | menor X com ≥80% (F→L / L→F) |", "|---|" + "---|" * (len(XS) + 1)]
    for m, nome in NOMES.items():
        cel = []
        for x in XS:
            a = g[(g.mecanismo == m) & (g.sentido == "Flavio→Lula") & (g.X == x)].poder.mean(); b = g[(g.mecanismo == m) & (g.sentido == "Lula→Flavio") & (g.X == x)].poder.mean()
            cel.append(f"{100*a:.0f}/{100*b:.0f}")
        mf, ml = res["menor_X_com_poder_80"][f"{m}|Flavio→Lula"], res["menor_X_com_poder_80"][f"{m}|Lula→Flavio"]
        fm = lambda v: "nunca" if v is None else (f"{v/1000:.0f} mil" if v < 1e6 else f"{v/1e6:.2f} mi")
        out.append(f"| {nome} | " + " | ".join(cel) + f" | {fm(mf)} / {fm(ml)} |")
    out.append("")
    fa = res["falso_alarme_conjunto_2a_amostra_bootstrap"]; n = 200
    out += [f"**Falso alarme (segunda amostra bootstrap por município, B = 200), {ano}:** união dos detectores na direção pró-Lula {100*fa['pos']:.1f}% (IC 95% Clopper-Pearson {100*cp(round(fa['pos']*n), n)[0]:.1f}–{100*cp(round(fa['pos']*n), n)[1]:.1f}), na direção pró-Flávio {100*fa['neg']:.1f}% ({100*cp(round(fa['neg']*n), n)[0]:.1f}–{100*cp(round(fa['neg']*n), n)[1]:.1f}), qualquer lado {100*fa['qualquer_lado']:.1f}% ({100*cp(round(fa['qualquer_lado']*n), n)[0]:.1f}–{100*cp(round(fa['qualquer_lado']*n), n)[1]:.1f}). Cada detector isolado tem 2,5% por construção; a união de vários fica acima disso.", ""]
    d = pd.read_parquet(f"{R}/sim_{ano}.parquet")
    out += [f"**D5 (dígito final), {ano}:** alarme em {100*d.d5_alarme.mean():.2f}% das {len(d)} execuções (qualquer mecanismo e magnitude). Poder na prática igual ao ruído.", ""]
    s = d[d.mecanismo.isin(["dispersa", "poucas_secoes"]) & d.X.isin([50_000, 100_000, 250_000])].groupby(["mecanismo", "X"])[["alarme_correto", "d1_correto_lim3", "d1_correto_lim5"]].mean().round(2)
    out += [f"**Sensibilidade do limiar do D1 (z de 3, 4 e 5), {ano}:**", "", "| Mecanismo | X | Poder (D1 a D4, D1 em 4) | D1 em 3 | D1 em 5 |", "|---|---|---|---|---|"]
    for (m, x), r in s.iterrows(): out.append(f"| {NOMES[m]} | {x/1000:.0f} mil | {r.alarme_correto:.2f} | {r.d1_correto_lim3:.2f} | {r.d1_correto_lim5:.2f} |")
    out.append("")
    out += [f"**Fabricação coerente de um 2º turno inteiro (B2), {ano}, 20 réplicas:**", "", "| Fabricante | Alarme D1–D4 | D5 | D6 (escala) | D7 (estrutura) | escala z / local / zona (relativas à base) |", "|---|---|---|---|---|---|"]
    f = pd.read_csv(f"{R}/sim_{ano}_fabricada.csv"); f2 = pd.read_csv(f"{R}/sim_{ano}_fabricada_v2.csv")
    for c, gg in f.groupby("cenario"):
        out.append(f"| {c.replace('fabricada_','')} (v1) | {100*gg.alarme_qualquer_lado.mean():.0f}% | {100*gg.d5_alarme.mean():.0f}% | {100*gg.d6_subdispersao.mean():.0f}% | {100*gg.d7_estrutura_local.mean():.0f}% | {gg.escala_z.mean():.2f} / {gg.esc_local_rel.mean():.2f} / {gg.esc_zona_rel.mean():.2f} |")
    out.append(f"| calibrada_estrutura (v2, efeitos centrados, total municipal corrigido) | {100*f2.alarme_qualquer_lado.mean():.0f}% | {100*f2.d5_alarme.mean():.0f}% | {100*f2.d6_subdispersao.mean():.0f}% | {100*f2.d7_estrutura_local.mean():.0f}% | {f2.escala_z.mean():.2f} / {f2.esc_local_rel.mean():.2f} / {f2.esc_zona_rel.mean():.2f} |")
    cols = [c for c in f2.columns if c.startswith(("d1_", "d2", "d3", "d4"))]
    out.append(f"\nDetectores que dispararam na v2 ({ano}): " + (", ".join(f"{c} {100*f2[c].mean():.0f}%" for c in cols if f2[c].mean() > 0) or "nenhum") + f". Margem fabricada {f2.margem_nacional.mean():,.0f} contra margem real {f2.margem_real.iloc[0]:,.0f}.\n".replace(",", "."))
open(f"{R}/tabelas_sim.md", "w").write("\n".join(out)); print("\n".join(out)[:9000])
