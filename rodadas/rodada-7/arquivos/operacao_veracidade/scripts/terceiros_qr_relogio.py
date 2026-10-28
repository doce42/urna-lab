"""T61 (complemento descritivo do relógio): só os boletins que o app de terceiros registrou antes das 19h (Brasília) no dia 25/10/2026."""
import json, sys
import pandas as pd
sys.path.insert(0, "operacao_veracidade/scripts")
R = "."; CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
q = pd.read_csv(f"{R}/operacao_veracidade/resultados/terceiros_qr.csv", dtype={c: str for c in CH})
b = pd.read_parquet(f"{R}/analise/base.parquet").astype({c: str for c in CH})
m = q.merge(b[CH + ["DT_BU_RECEBIDO_2", "DT_EMISSAO_BU_2"]], on=CH)
app = pd.to_datetime(m.recebido_app_utc, utc=True).dt.tz_convert("America/Sao_Paulo").dt.tz_localize(None)
tse = pd.to_datetime(m.DT_BU_RECEBIDO_2)
dia = pd.Timestamp("2026-10-25")
s = (app >= dia) & (app < dia + pd.Timedelta(hours=19))
d = (tse - app)[s].dt.total_seconds() / 60
out = {"boletins_registrados_pelo_app_antes_de_19h_de_25_10": int(s.sum()), "recebimento_no_tse_antes_de_19h_entre_eles": int((tse[s] < dia + pd.Timedelta(hours=19)).sum()),
       "tse_menos_app_min": {"mediana": float(d.median()), "p05": float(d.quantile(.05)), "p95": float(d.quantile(.95)), "minimo": float(d.min())},
       "tse_recebeu_depois_das_19h03_entre_eles": int((tse[s] > dia + pd.Timedelta(hours=19, minutes=3)).sum()),
       "app_primeiro_registro": str(app[s].min()), "app_ultimo_antes_de_19h": str(app[s].max()),
       "conteudo": "estes boletins coincidem em votos e assinatura com o arquivo que o TSE registrou depois (T61)",
       "limite": "o relógio do app de terceiros não é auditado; o tempo de recebimento do TSE é o campo DT_BU_RECEBIDO_2 da tabela dele"}
j = json.load(open(f"{R}/operacao_veracidade/resultados/terceiros_qr.json")); j["relogio_antes_das_19h"] = out
json.dump(j, open(f"{R}/operacao_veracidade/resultados/terceiros_qr.json", "w"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(out, ensure_ascii=False, indent=1))
