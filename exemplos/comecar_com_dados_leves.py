"""Exemplo: pesquisar com o pacote de dados leves (sem baixar os ~405 GB do TSE).
Baixe dados_leves_vX.Y.zip do release no GitHub, descompacte e rode:  python exemplos/comecar_com_dados_leves.py caminho/dados_leves
Reproduz três números do estudo: o total do 2º turno de 2026, as seções com zero voto para Flávio e as seções com virada
muito fora do padrão do município (T02). Requer pandas, numpy e pyarrow."""
import sys
import numpy as np
import pandas as pd

D = sys.argv[1] if len(sys.argv) > 1 else "dados_leves"
s = pd.read_parquet(f"{D}/secoes_2026.parquet")
print(f"2º turno de 2026: Lula {int(s.v13_2.sum()):,} × Flávio {int(s.v22_2.sum()):,}; margem {int(s.v13_2.sum() - s.v22_2.sum()):,}".replace(",", "."))
b = s[(s.SG_UF != "ZZ") & (s.validos_1.fillna(0) > 0) & (s.validos_2.fillna(0) > 0)]
print(f"seções com zero voto para Flávio: {int((b.v22_1 == 0).sum())} (1º turno) e {int((b.v22_2 == 0).sum())} (2º)")
# T02: virada da seção (logit) contra a mediana do município, em desvios robustos
c = s[(s.validos_1 >= 20) & (s.validos_2 >= 20)].copy()
lg = lambda x, n: np.log((x + .5) / (n - x + .5))
c["mun"] = c.SG_UF + c.CD_MUNICIPIO.astype(str)
sw = lg(c.v13_2, c.validos_2) - lg(c.v13_1, c.validos_1)
z = (sw - sw.groupby(c.mun).transform("median")) / np.sqrt(1/(c.v13_1+.5) + 1/(c.validos_1-c.v13_1+.5) + 1/(c.v13_2+.5) + 1/(c.validos_2-c.v13_2+.5))
z = z / (1.4826 * (z - z.median()).abs().median())
print(f"seções além de 5 desvios: {int((z > 5).sum())} pró-Lula e {int((z < -5).sum())} pró-Flávio (o estudo registra 33 e 13)")
print("Próximos passos: urnas_2026_2t.parquet (resumo dos arquivos das urnas), perfil_por_secao_2026.parquet, veredito_2026.json")
