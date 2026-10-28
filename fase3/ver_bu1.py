"""F3 em revisão / BU1: seção MG 49050/196/173 (2022, 1º turno), cujo BU não foi lido. Identifica os arquivos, reproduz a
falha, decodifica o boletim do Sistema de Apuração (.busa) e confere com o texto impresso (.imgbusa, leitura independente)
e com a tabela publicada; conta as seções de 2022 que têm só arquivos do Sistema de Apuração (mesma causa).
Lê só os pacotes oficiais locais. Saída: fase3/resultados/bu1.json."""
import collections, glob, hashlib, json, os, re, sys, zipfile
import pandas as pd

os.environ["ANO"] = "2022"
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); sys.path.insert(0, RAIZ + "/analise")
import der  # noqa: E402
import processar_brutos as pb  # noqa: E402

PAC = RAIZ + "/dados/2022/brutos/1turno/bu_imgbu_logjez_rdv_vscmr_2022_1t_MG.zip"; COD = "4905001960173"
R = {"pergunta": "BU1", "secao": "MG 49050/196/173, 2022, 1º turno", "pacote": os.path.basename(PAC), "pacote_bytes": os.path.getsize(PAC)}
zf = zipfile.ZipFile(PAC)
arqs = {i.filename: i for i in zf.infolist() if COD in i.filename}
R["arquivos"] = [{"nome": n, "bytes": i.file_size, "data_zip": "%04d-%02d-%02d %02d:%02d:%02d" % i.date_time,
                  "sha512": hashlib.sha512(zf.read(n)).hexdigest(), "sha256": hashlib.sha256(zf.read(n)).hexdigest()} for n, i in sorted(arqs.items())]
# 1) reprodução da falha: o leitor de 2022 só reconhece bu, imgbu, logjez, rdv e vscmr
R["reconhecidos_pelo_leitor_2022"] = {n: pb.analisa_nome(n, "MG") for n in arqs}
dado = {n.rsplit(".", 1)[1]: zf.read(n) for n in arqs}
# 2) decodificação do .busa com o mesmo leitor de boletim (mesmo formato DER)
try: R["busa_decodificado"] = pb.ler_bu(dado["busa"], 1)
except Exception as e: R["busa_decodificado"] = {"erro": repr(e)}
# 3) leitura independente: texto do boletim impresso do Sistema de Apuração
try: R["imgbusa_lido"] = pb.ler_imgbu(dado["imgbusa"])
except Exception as e: R["imgbusa_lido"] = {"erro": repr(e)}
if not R["imgbusa_lido"]:
    env, _ = der.ler(dado["imgbusa"]); txt = None
    def acha(no):
        global txt
        if txt: return
        v = no.get("v")
        if isinstance(v, (bytes, bytearray)) and b"PRESIDENTE" in v: txt = v; return
        for f in no.get("f") or []: acha(f)
    acha(env)
    R["imgbusa_trecho_presidente"] = None if txt is None else re.search(rb"PRESIDENTE.{0,1200}", txt, re.S).group(0).decode("latin-1")
# 4) assinatura: o .vscsa tem o mesmo leiaute do .vscmr?
try:
    lista, resumo, verifica = pb.ler_vsc(dado["vscsa"])
    R["vscsa"] = {"resumo": resumo, "arquivos_listados": sorted(lista)}
    R["vscsa"]["confere"] = {n: {"tamanho_e_sha512": lista[n][:2] == (len(zf.read(n)), hashlib.sha512(zf.read(n)).digest()),
                                 "assinatura": bool(verifica(lista[n][2], lista[n][1]))} for n in arqs if n in lista}
except Exception as e:
    R["vscsa"] = {"erro": repr(e), "nota": "leiaute diferente do bloco UEAO da urna; assinatura não verificada"}
# 5) comparação com a tabela publicada (base do projeto, BU na Web)
b = pd.read_parquet(RAIZ + "/analise/base_2022.parquet")
row = b[(b.SG_UF == "MG") & (b.CD_MUNICIPIO.astype(str) == "49050") & (b.NR_ZONA.astype(str) == "196") & (b.NR_SECAO.astype(str) == "173")].iloc[0]
pub = {c: int(row[c]) for c in row.index if re.fullmatch(r"v\d+_1|branco_1|nulo_1", c) and not pd.isna(row[c])}
R["publicado"] = {"votos": pub, "comparecimento": int(row["QT_COMPARECIMENTO_1"]), "aptos": int(row["QT_APTOS_1"]), "emissao_bu": str(row["DT_EMISSAO_BU_1"])}
bu = R["busa_decodificado"]
if "erro" not in bu:
    R["busa_x_publicado"] = {c: (bu.get("bu_" + c.rsplit("_", 1)[0], 0), v) for c, v in pub.items() if bu.get("bu_" + c.rsplit("_", 1)[0], 0) != v}
    R["busa_comparecimento"] = bu.get("bu_comparecimento")
# 6) mesma causa em outras seções: seções de 2022 com boletim só do Sistema de Apuração (.busa e sem .bu), lendo só os índices
NOME = re.compile(r"o(\d{5})-(\d{13})\.(\w+)$"); cont = {}; exemplos = []
for t in (1, 2):
    for p in sorted(glob.glob(f"{RAIZ}/dados/2022/brutos/{t}turno/bu_imgbu_logjez_rdv_vscmr_2022_{t}t_*.zip")):
        uf = p.rsplit("_", 1)[1][:2]; ext = collections.defaultdict(set)
        for n in zipfile.ZipFile(p).namelist():
            m = NOME.search(n)
            if m: ext[m.group(2)].add(m.group(3))
        so_sa = [c for c, e in ext.items() if "busa" in e and "bu" not in e]
        if so_sa: cont[f"{t}T {uf}"] = len(so_sa); exemplos += [f"{t}T {uf} {c}" for c in so_sa[:2]]
R["secoes_2022_so_com_boletim_do_sistema_de_apuracao"] = {"por_turno_uf": cont, "total": sum(cont.values()), "exemplos": exemplos[:10]}
json.dump(R, open(RAIZ + "/fase3/resultados/bu1.json", "w"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: v for k, v in R.items() if k not in ("arquivos",)}, ensure_ascii=False, default=str)[:4000])
