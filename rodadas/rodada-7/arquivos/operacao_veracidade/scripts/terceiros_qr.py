"""T61: boletins impressos de terceiros (QR Code), 2º turno de 2026. Protocolo: operacao_veracidade/PROTOCOLO_PRE_EXECUCAO.md.
Entrada: externo/arvor_totalizacao/bus.csv (arquivo estático público, SHA-256 em SHA256SUMS.txt). Saída: resultados/terceiros_qr.json e .csv"""
import hashlib, json, re, sys
import numpy as np, pandas as pd
sys.path.insert(0, "operacao_veracidade/scripts")
import cadeia  # noqa: E402
from cryptography.hazmat.primitives import hashes  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import ec  # noqa: E402
from cryptography.exceptions import InvalidSignature  # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); AN = RAIZ + "/analise"; OP = RAIZ + "/operacao_veracidade"
CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
b = pd.read_csv(f"{OP}/externo/arvor_totalizacao/bus.csv", dtype=str)
ac = cadeia.carrega_acs()
R = {"protocolo": "operacao_veracidade/PROTOCOLO_PRE_EXECUCAO.md", "boletins": int(len(b)), "ufs": int(b.uf.nunique())}


def campos(txt):
    d = dict(re.findall(r"\b([A-Z]{4}):(\S+)", txt))
    d["votos"] = {k: int(v) for k, v in re.findall(r"\b(\d{2}):(\d+)\b", txt) if k not in ("NO", )}
    return d


rows = []
for r in b.itertuples(index=False):
    cb = bytes.fromhex(r.cert_hex); sig = bytes.fromhex(r.assi); h = bytes.fromhex(r.hash_final); cd = campos(r.conteudo)
    c = cadeia.analisa_cert(cb, ac)
    hash_ok = hashlib.sha512(r.conteudo.encode()).digest() == h
    if c["alg"] == "Ed521":
        sig_ok = cadeia.ed521.verifica(c["pub"], sig, h); estrita = sig_ok
    else:
        try:
            c["pub"].verify(sig, h, ec.ECDSA(hashes.SHA512())); sig_ok = estrita = True
        except InvalidSignature:
            sig_ok = estrita = False
        except ValueError:
            sig_ok, estrita = None, False           # DER não canônico: contado à parte
    rows.append({"SG_UF": r.uf.upper(), "CD_MUNICIPIO": str(int(r.muni)), "NR_ZONA": str(int(r.zona)), "NR_SECAO": str(int(r.secao)), "alg": c["alg"], "cn": c["cn"], "emissor": c["emissor"],
                 "cert_sha256": c["sha256"], "cadeia_ok": c["cadeia_ok"], "nao_antes": c["nao_antes"].isoformat(), "nao_depois": c["nao_depois"].isoformat(), "hash_conteudo_ok": hash_ok,
                 "assinatura_ok": sig_ok, "assinatura_estrita": estrita, "idue": int(r.idue), "v13": cd["votos"].get("13"), "v22": cd["votos"].get("22"), "branco": int(cd["BRAN"]), "nulo": int(cd["NULO"]),
                 "comp": int(cd["COMP"]), "apto": int(cd["APTO"]), "dtfc": cd["DTFC"], "hrfc": cd["HRFC"], "recebido_app_utc": r.recebido_em, "mdue": r.mdue, "turno_qr": cd["TURN"]})
q = pd.DataFrame(rows)
R["sem_secao_repetida"] = bool(not q.duplicated(CH).any())
R["assinatura"] = {"conteudo_igual_ao_hash": int(q.hash_conteudo_ok.sum()), "assinatura_valida": int((q.assinatura_ok == True).sum()), "invalida": int((q.assinatura_ok == False).sum()), "der_nao_canonico": int(q.assinatura_ok.isna().sum()), "por_algoritmo": q.groupby("alg").assinatura_ok.agg(lambda s: int((s == True).sum())).to_dict()}
dia = pd.Timestamp("2026-10-25", tz="UTC")
R["certificado"] = {"cadeia_ok": int((q.cadeia_ok == True).sum()), "cadeia_falha": int((q.cadeia_ok == False).sum()), "emissor_sem_ac": int(q.cadeia_ok.isna().sum()),
                    "validos_no_dia": int(((pd.to_datetime(q.nao_antes) <= dia) & (pd.to_datetime(q.nao_depois) >= dia)).sum()), "emitidos_depois_da_eleicao": int((pd.to_datetime(q.nao_antes) > dia).sum()),
                    "emissores": q.emissor.value_counts().to_dict(), "emitidos_depois_de_18_07_2026_ac_urna": int(((q.emissor == "AC URNA") & (pd.to_datetime(q.nao_antes) > pd.Timestamp("2026-07-18", tz="UTC"))).sum()),
                    "mesmo_certificado_em_duas_secoes": int(q.cert_sha256.duplicated().sum()), "turno_qr": q.turno_qr.value_counts().to_dict()}

# comparação com a base do TSE (tabela) e com o BU decodificado do pacote
base = pd.read_parquet(f"{AN}/base.parquet").astype({c: str for c in CH})
m = q.merge(base[CH + ["v13_2", "v22_2", "branco_2", "nulo_2", "QT_COMPARECIMENTO_2", "QT_APTOS_2", "NR_URNA_EFETIVADA_2", "DT_EMISSAO_BU_2", "DT_BU_RECEBIDO_2", "DT_ENCERRAMENTO_2"]], on=CH, how="left", indicator=True)
R["pareamento"] = {"com_par_na_base": int((m._merge == "both").sum()), "sem_par": int((m._merge != "both").sum())}
us = pd.concat([pd.read_parquet(f"{AN}/brutos/2t/urnas_{uf}.parquet", columns=CH + ["cert_urna", "bu_v13", "bu_v22", "bu_branco", "bu_nulo", "bu_comparecimento", "rdv_v13", "rdv_v22", "modelo"]) for uf in sorted(set(q.SG_UF))]).astype({c: str for c in CH})
m = m.merge(us, on=CH, how="left")
for qr, tab, bu in (("v13", "v13_2", "bu_v13"), ("v22", "v22_2", "bu_v22"), ("branco", "branco_2", "bu_branco"), ("nulo", "nulo_2", "bu_nulo"), ("comp", "QT_COMPARECIMENTO_2", "bu_comparecimento")):
    m[f"dif_tab_{qr}"] = m[qr] - m[tab]; m[f"dif_bu_{qr}"] = m[qr] - m[bu].fillna(0)
m["dif_apto"] = m.apto - m.QT_APTOS_2
difs = {k: int((m[k] != 0).sum()) for k in m.columns if k.startswith("dif_")}
R["votos"] = {"diferencas_por_campo_contra_tabela_e_bu": difs, "boletins_com_alguma_diferenca": int((m[[k for k in m.columns if k.startswith("dif_")]] != 0).any(axis=1).sum()),
              "votos_13_total": int(m.v13.sum()), "votos_22_total": int(m.v22.sum()), "secoes_com_voto_zero_flavio": int((m.v22 == 0).sum())}
m["cn_num"] = m.cn_x.str.extract(r"(\d+)$")[0].astype(int) if "cn_x" in m else m.cn.str.extract(r"(\d+)$")[0].astype(int)
cn_col = "cn_x" if "cn_x" in m else "cn"
m["cn_num"] = m[cn_col].str.extract(r"(\d+)$")[0].astype(int)
cu_num = m.cert_urna.str.extract(r"(\d+)$")[0]
R["identidade_da_urna"] = {"idue_igual_cn_do_qr": int((m.idue == m.cn_num).sum()), "idue_igual_urna_efetivada_da_tabela": int((m.idue.astype(str).str.zfill(7) == m.NR_URNA_EFETIVADA_2.astype(str).str.zfill(7)).sum() if m.NR_URNA_EFETIVADA_2.notna().all() else (pd.to_numeric(m.NR_URNA_EFETIVADA_2, errors="coerce") == m.idue).sum()),
                           "cn_do_qr_igual_cn_do_vota_vsc": int((cu_num.astype(float) == m.cn_num).sum()), "secoes_com_vota_vsc_comparavel": int(cu_num.notna().sum()),
                           "modelos": m.modelo.value_counts().to_dict()}
# relógio: impressão (hora local da seção) × encerramento/emissão da base; recebimento no app × recebimento no TSE (hora de Brasília)
imp = pd.to_datetime(m.dtfc + m.hrfc, format="%Y%m%d%H%M%S")
emi = pd.to_datetime(m.DT_EMISSAO_BU_2); enc = pd.to_datetime(m.DT_ENCERRAMENTO_2); tse_rec = pd.to_datetime(m.DT_BU_RECEBIDO_2)
app = pd.to_datetime(m.recebido_app_utc, utc=True).dt.tz_convert("America/Sao_Paulo").dt.tz_localize(None)
d_emi = (imp - emi).dt.total_seconds() / 60; d_rec = (tse_rec - app).dt.total_seconds() / 60
R["relogio"] = {"impressao_menos_emissao_na_base_min": {"mediana": float(d_emi.median()), "p05": float(d_emi.quantile(.05)), "p95": float(d_emi.quantile(.95)), "iguais_dentro_de_2min": int((d_emi.abs() <= 2).sum())},
                "impressao_mediana": str(imp.dt.time.sort_values().iloc[len(imp) // 2]), "app_recebeu_mediana_brasilia": str(app.dt.time.sort_values().iloc[len(app) // 2]),
                "tse_recebeu_mediana_brasilia": str(tse_rec.dt.time.sort_values().iloc[len(tse_rec) // 2]),
                "tse_menos_app_min": {"mediana": float(d_rec.median()), "p05": float(d_rec.quantile(.05)), "p95": float(d_rec.quantile(.95)), "app_antes_do_tse": int((d_rec > 0).sum()), "app_depois_do_tse": int((d_rec < 0).sum())},
                "app_recebeu_antes_de_19h_no_dia_da_eleicao": int(((app >= pd.Timestamp("2026-10-25")) & (app < pd.Timestamp("2026-10-25 19:00"))).sum()), "tse_recebeu_antes_de_19h": int((tse_rec < pd.Timestamp("2026-10-25 19:00")).sum()),  # correção 1: a 1ª versão contava a hora de qualquer dia
                "nota": "o app de terceiros registra o horário no próprio servidor; o relógio dele não é auditado"}
R["cobertura"] = {"secoes_do_brasil": 499207, "fracao": float(len(q) / 499207), "por_uf": q.SG_UF.value_counts().to_dict(),
                  "aviso": "amostra de conveniência: coletores e publicador são o mesmo projeto; sem desenho probabilístico; só 2º turno de 2026"}
disc = m[(m[[k for k in m.columns if k.startswith("dif_")]] != 0).any(axis=1)][CH + ["v13", "v22", "v13_2", "v22_2"]]
R["divergencias_lista"] = disc.head(20).astype(str).to_dict("records")
q.to_csv(f"{OP}/resultados/terceiros_qr.csv", index=False)
json.dump(R, open(f"{OP}/resultados/terceiros_qr.json", "w"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
