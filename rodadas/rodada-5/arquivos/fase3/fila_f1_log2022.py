"""F3 / fila F1: as 153 seções-turno de 2022 com log diferente do comparecimento do boletim. Recontagem dos votos computados
direto do .logjez (todas as partes, por urna), em três formas (como o leitor: sem linhas já vistas em parte anterior; soma
simples das partes; só a parte principal logd.dat). Ver fase3/PREREG_FILA.md (F1). Saída: fase3/resultados/fila_f1_log2022.json."""
import collections, json, os, sys, zipfile
import pandas as pd

os.environ["ANO"] = "2022"
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); sys.path.insert(0, RAIZ + "/analise")
import processar_brutos as pb  # noqa: E402

DIA = {1: "02/10/2022", 2: "30/10/2022"}
lst = json.load(open(RAIZ + "/fase3/resultados/adv_log_x_comparecimento.json"))["lista_2022"]
base = pd.read_parquet(RAIZ + "/analise/base_2022.parquet")
base["k"] = base.SG_UF + "/" + base.CD_MUNICIPIO.astype(int).astype(str) + "/" + base.NR_ZONA.astype(int).astype(str) + "/" + base.NR_SECAO.astype(int).astype(str)
base = base.drop_duplicates("k").set_index("k")


def partes(dado, prefixo=""):
    """[(nome, linhas)] de todas as partes, abrindo pacotes aninhados"""
    out = []
    for nome, c in pb._abre_log(dado).items():
        if nome.endswith((".jez", ".logjez")): out += partes(c, prefixo + nome + "/")
        else: out.append((prefixo + nome, c.decode("latin1").splitlines()))
    return out


zips = {}
res = []
for x in lst:
    t, uf = int(x["turno"]), x["SG_UF"]; m, z, s = int(x["CD_MUNICIPIO"]), int(x["NR_ZONA"]), int(x["NR_SECAO"]); k = f"{uf}/{m}/{z}/{s}"
    key = (t, uf)
    if key not in zips: zips[key] = zipfile.ZipFile(f"{RAIZ}/dados/2022/brutos/{t}turno/bu_imgbu_logjez_rdv_vscmr_2022_{t}t_{uf}.zip")
    zf = zips[key]; cod = f"{m:05d}{z:04d}{s:04d}"
    nome = next((n for n in zf.namelist() if n.endswith(cod + ".logjez")), None)
    L = {"turno": t, "secao": k, "comparecimento_bu": int(x["bu_comparecimento"]), "computado_parquet": int(x["computado"]), "cert_urna": x.get("cert_urna")}
    row = base.loc[k] if k in base.index else None
    if row is not None:
        L["urna_efetivada_tabela"] = str(row[f"NR_URNA_EFETIVADA_{t}"]); L["encerramento"] = str(row[f"DT_ENCERRAMENTO_{t}"]); L["emissao_bu"] = str(row[f"DT_EMISSAO_BU_{t}"])
    if not nome:
        L["classe"] = "4 outra: sem .logjez no pacote"; res.append(L); continue
    ps = partes(zf.read(nome)); L["partes"] = []
    vistas = set(); dedup = 0; simples = 0; por_urna = collections.Counter(); fora_dia = 0
    for nm, linhas in sorted(ps, key=lambda p: (p[0].endswith("logd.dat"), p[0])):
        v = [l for l in linhas if "\t" in l and l.split("\t")[4:5] and l.split("\t")[4].startswith("O voto do eleitor foi computado")]
        vd = [l for l in v if l.startswith(DIA[t])]; fora_dia += len(v) - len(vd)
        novos = [l for l in vd if l not in vistas]
        L["partes"].append({"parte": nm, "votos_no_dia": len(vd), "votos_fora_do_dia": len(v) - len(vd), "novos_em_relacao_a_partes_anteriores": len(novos),
                            "urnas": sorted({l.split("\t")[2] for l in vd}), "primeiro": vd[0][:19] if vd else None, "ultimo": vd[-1][:19] if vd else None})
        simples += len(vd); dedup += len(novos); vistas.update(linhas)
        for l in novos: por_urna[l.split("\t")[2]] += 1
    principal = next((p["votos_no_dia"] for p in L["partes"] if p["parte"].endswith("logd.dat")), None)
    L.update({"recontagem_como_leitor": dedup, "soma_simples_das_partes": simples, "so_logd_dat": principal, "votos_por_urna": dict(por_urna), "votos_fora_do_dia": fora_dia,
              "validacao_recontagem_igual_parquet": dedup == L["computado_parquet"]})
    comp = L["comparecimento_bu"]; ult = max((p["ultimo"] for p in L["partes"] if p["ultimo"]), default=None)
    urnas_log = set(por_urna); efet = L.get("urna_efetivada_tabela", "")
    efet_no_log = any(u.lstrip("0") == efet.lstrip("0") for u in urnas_log)
    L["urna_efetivada_tem_votos_no_log"] = efet_no_log; L["ultimo_voto_no_log"] = ult
    if dedup != comp and (simples == comp or principal == comp): L["classe"] = "1 artefato do leitor (outra forma de contar o log dá o comparecimento)"
    elif dedup < comp and not efet_no_log: L["classe"] = "2 log da urna efetivada ausente (o log publicado é de outra urna)"
    elif dedup < comp: L["classe"] = "2b log menor que o comparecimento, com a urna efetivada no log"
    elif dedup > comp and (len(urnas_log) > 1 or fora_dia): L["classe"] = "3 log com votos de mais de uma urna ou fora do dia"
    elif dedup > comp: L["classe"] = "3b log maior que o comparecimento, uma só urna"
    else: L["classe"] = "4 outra"
    res.append(L)
df = pd.DataFrame([{k: v for k, v in r.items() if k != "partes"} for r in res])
R = {"pergunta": "fila F1", "secoes": len(res), "por_classe": df.classe.value_counts().to_dict(),
     "por_classe_e_turno": {f"{t}T | {c}": int(n) for (t, c), n in df.groupby(["turno", "classe"]).size().items()},   # correção: chave em tupla
     "validacao_recontagem_igual_parquet": int(df.get("validacao_recontagem_igual_parquet", pd.Series(dtype=bool)).fillna(False).sum()),
     "votos_sem_log_por_classe": {c: int((g.comparecimento_bu - g.recontagem_como_leitor).clip(lower=0).sum()) for c, g in df.groupby("classe")} if "recontagem_como_leitor" in df else {},
     "secoes_detalhe": res}
json.dump(R, open(RAIZ + "/fase3/resultados/fila_f1_log2022.json", "w"), ensure_ascii=False, indent=1, default=str)
print({k: v for k, v in R.items() if k != "secoes_detalhe"})
