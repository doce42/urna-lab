"""T60a: relê, por data de eleição e ID de urna, o log dos 17 casos em que o certificado não é o da urna efetivada da tabela (2026)."""
import io, os, sys, zipfile, collections
os.environ["ANO"] = "2026"; R = "."; sys.path.insert(0, R + "/analise")
import pandas as pd, processar_brutos as PB
casos = pd.read_csv(f"{R}/operacao_veracidade/resultados/casos_certificado.csv", dtype=str); a = casos[(casos.ano == "2026") & casos.tipo.str.startswith("A_")]
DIA = {"1": "04/10/2026", "2": "25/10/2026"}; zips = {}; out = []


def le(b):
    zz = zipfile.ZipFile(io.BytesIO(b)); res = []
    for nm in zz.namelist():
        c = zz.read(nm); res += le(c) if nm.endswith((".jez", ".logjez")) else [c.decode("latin1")]
    return res


for r in a.itertuples(index=False):
    t = int(r.turno); pac, _ = PB.fonte(t, r.SG_UF)
    if (t, r.SG_UF) not in zips: zips[(t, r.SG_UF)] = zipfile.ZipFile(pac)
    z = zips[(t, r.SG_UF)]
    nome = next(n for n in z.namelist() if (lambda x: x and x[0] == (r.SG_UF, r.CD_MUNICIPIO, r.NR_ZONA, r.NR_SECAO) and x[1] == "log")(PB.analisa_nome(n, r.SG_UF)))
    vistas, v = set(), collections.Counter()
    for txt in le(z.read(nome)):
        for l in txt.splitlines():
            if l in vistas: continue
            vistas.add(l); c = l.split("\t")
            if len(c) >= 5 and c[0][:10] == DIA[r.turno] and "O voto do eleitor foi computado" in c[4]: v[c[2]] += 1
    da_tabela = next((q for k, q in v.items() if k.lstrip("0") == str(r.urna_tabela)), -1)
    out.append({"turno": t, "uf": r.SG_UF, "secao": r.NR_SECAO, "comparecimento": int(float(r.comparecimento)), "urna_tabela": r.urna_tabela, "cert": r.cn_certificado, "votos_do_dia_por_id": dict(v), "soma_no_pacote": sum(v.values()), "votos_da_urna_da_tabela": da_tabela})
df = pd.DataFrame(out); df["urna_da_tabela_bate_com_comparecimento"] = df.votos_da_urna_da_tabela == df.comparecimento
print(df[["turno", "uf", "secao", "comparecimento", "soma_no_pacote", "votos_da_urna_da_tabela", "urna_da_tabela_bate_com_comparecimento"]].to_string())
print("urna da tabela registrou o comparecimento do BU:", int(df.urna_da_tabela_bate_com_comparecimento.sum()), "de", len(df))
df.to_csv(f"{R}/operacao_veracidade/resultados/casos_A_relidos_por_id_e_data.csv", index=False)
