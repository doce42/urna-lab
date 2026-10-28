"""T34 e T35: ligação urna ↔ seção ↔ preparação (dados abertos do TSE: correspondências esperadas/efetivadas e logs do GEDAI).

T34  para cada seção: urna efetivada (CEFT) = urna do Boletim de Urna (BU na Web) = urna do certificado e do log
     (arquivos das urnas); urna esperada (preparada para a seção) x efetivada; origem do voto
T35  toda máquina que gerou mídia de carga (CEFT: nome + serial TPM + serial de instalação) tem log publicado do GEDAI,
     em versão e fase oficiais
Uso: python correspondencia.py <turno>
"""
import collections
import glob
import io
import json
import os
import re
import sys
import zipfile

import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "..", "dados", "correspondencias_gedai")
TURNO = int(sys.argv[1]) if len(sys.argv) > 1 else 2
R = {"turno": TURNO}

# ---- CEFT (correspondência efetivada), um arquivo por UF (o mais recente)
ceft = []
for uf_zip in sorted(glob.glob(os.path.join(D, f"CEFT_{TURNO}t_*.zip"))):
    with zipfile.ZipFile(uf_zip) as z:
        nome = [n for n in z.namelist() if n.endswith(".csv")][0]
        ceft.append(pd.read_csv(z.open(nome), sep=";", encoding="latin1", dtype=str))
c = pd.concat(ceft, ignore_index=True)
c["CD_MUNICIPIO"] = c["CD_MUNICIPIO"].astype(int).astype(str)
c = c.sort_values("DT_GERACAO").drop_duplicates(["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"], keep="last")
R["T34_secoes_ceft"] = int(len(c))
R["T34_origem_voto"] = c["DS_ORIGEM_VOTO"].value_counts().to_dict()
R["T34_esperada_diferente_efetivada"] = int((c["NR_URNA_ESPERADA"] != c["NR_URNA_EFETIVADA"]).sum())
R["T34_tipos_divergencia"] = c["TP_DIVERGENCIA"].fillna("(vazio)").value_counts().to_dict()

# ---- BU na Web (urna efetivada declarada no boletim)
b = pd.read_parquet(os.path.join(AQUI, "base.parquet"))
b = b[b[f"total_{TURNO}"].notna()][["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", f"NR_URNA_EFETIVADA_{TURNO}"]]
m = c.merge(b, on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"], how="outer", indicator=True)
R["T34_ceft_x_bu_cobertura"] = m["_merge"].value_counts().to_dict()
mm = m[m["_merge"] == "both"]
R["T34_ceft_urna_igual_bu"] = [int((mm["NR_URNA_EFETIVADA"].astype(int) == mm[f"NR_URNA_EFETIVADA_{TURNO}"].astype(int)).sum()), int(len(mm))]

# ---- arquivos das urnas (certificado e log)
arqs = glob.glob(os.path.join(AQUI, "brutos", f"{TURNO}t", "urnas_*.parquet"))
if arqs:
    u = pd.concat([pd.read_parquet(a, columns=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "cert_urna", "ids_urna_log", "urnas_com_voto_no_log"])
                   for a in arqs], ignore_index=True)
    x = c.merge(u, on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"], how="inner")
    efet = x["NR_URNA_EFETIVADA"].astype(int)
    cert = x["cert_urna"].fillna("").str.extract(r"(\d+)$")[0].fillna(-1).astype(int)
    no_log = x.apply(lambda r: int(r["NR_URNA_EFETIVADA"]) in {int(i) for i in str(r["ids_urna_log"] or "").split(",") if i.isdigit()}, axis=1)
    R["T34_urnas_processadas"] = int(len(x))
    R["T34_ceft_igual_certificado"] = int((efet == cert).sum())
    R["T34_ceft_entre_urnas_do_log"] = int(no_log.sum())
    sub = x[(x["NR_URNA_ESPERADA"] != x["NR_URNA_EFETIVADA"])]
    R["T34_trocas_declaradas_com_2_urnas_no_log"] = [int((sub["urnas_com_voto_no_log"] > 1).sum()), int(len(sub))]
    dif = x[efet != cert]
    R["T34_exemplos_diferenca"] = dif[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_URNA_ESPERADA", "NR_URNA_EFETIVADA", "cert_urna", "ids_urna_log"]].head(15).to_dict("records")

# ---- T35: máquinas de geração de mídia (CEFT) x logs publicados do GEDAI
gedai = {}
for gz in glob.glob(os.path.join(D, f"log_gedai_{TURNO}t_*.zip")) + glob.glob(os.path.join(D, "log_gedai_1t_*.zip")):
    with zipfile.ZipFile(gz) as z:
        for n in z.namelist():
            mm_ = re.match(r"gedai-ue-(\w\w)-\d+-oficial-(\w+)-([0-9A-F]+)-([0-9A-F]+)-log\.jez", n)
            if not mm_:
                continue
            chave = (mm_.group(2), mm_.group(3), mm_.group(4))
            if chave in gedai:
                continue
            # versão e fase, do log interno
            try:
                inner = zipfile.ZipFile(io.BytesIO(zipfile.ZipFile(io.BytesIO(z.read(n))).read(
                    [k for k in zipfile.ZipFile(io.BytesIO(z.read(n))).namelist() if k.endswith(".jez")][0])))
                t = inner.read("gedai-ue.log").decode("latin1")
                versoes = sorted(set(re.findall(r"Abertura do GEDAI-UE - Versão ([^\t]+)", t)))
                fases = sorted(set(re.findall(r"\tFase: ([^\t]+)", t)))
            except Exception as e:
                versoes, fases = [f"erro: {e}"], []
            gedai[chave] = {"versoes": versoes, "fases": fases}
maqs = c[["NM_MAQUINA_GERACAO_MIDIA", "NR_SRI_TPM_GERACAO_MIDIA", "NR_SRI_INSTAL_GERACAO_MIDIA"]].drop_duplicates()
tem = maqs.apply(lambda r: (r.iloc[0], r.iloc[1], r.iloc[2]) in gedai, axis=1)
R["T35_maquinas_geracao_midia"] = int(len(maqs))
R["T35_com_log_gedai_publicado"] = int(tem.sum())
R["T35_sem_log"] = maqs[~tem].head(20).to_dict("records")
R["T35_versoes_gedai"] = dict(collections.Counter(v for g in gedai.values() for v in g["versoes"]))
R["T35_fases_gedai"] = dict(collections.Counter(f for g in gedai.values() for f in g["fases"]))
R["T35_logs_gedai_lidos"] = len(gedai)
json.dump(R, open(os.path.join(AQUI, f"resultado_correspondencia_{TURNO}t.json"), "w"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: v for k, v in R.items() if not k.endswith("exemplos_diferenca") and k != "T35_sem_log"}, ensure_ascii=False, indent=1, default=str))
