"""T60b: controles positivos e negativos do verificador de assinaturas, sobre cópias em memória de arquivos reais, e controle hostil sintético.
Protocolo: operacao_veracidade/PROTOCOLO_PRE_EXECUCAO.md. Uso: controles_mutacao.py <ano> <UF>   (2º turno)
Nada é gravado em arquivo de dados; o certificado e a chave sintéticos existem só em memória."""
import collections, datetime, hashlib, json, os, random, sys, zipfile

ANO, UF = sys.argv[1], sys.argv[2]; os.environ["ANO"] = ANO
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, RAIZ + "/analise"); sys.path.insert(0, RAIZ + "/operacao_veracidade/scripts")
import der, processar_brutos as PB, cadeia  # noqa: E402
from cryptography import x509  # noqa: E402
from cryptography.hazmat.primitives import hashes  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import ec  # noqa: E402
from cryptography.hazmat.primitives.serialization import Encoding  # noqa: E402

N = 40
pacote, _ = PB.fonte(2, UF); z = zipfile.ZipFile(pacote)
por = collections.defaultdict(dict)
for n in z.namelist():
    a = PB.analisa_nome(n, UF)
    if a:
        por[a[0]][a[1]] = n
chaves = sorted(k for k, v in por.items() if "vota" in v and "bu" in v)
random.seed(20261028 + int(ANO)); sel = random.sample(chaves, N)


def avalia(vsc, nome_arq, conteudo):
    """Reproduz a lógica do pipeline: devolve (hash_ok, assin_arquivo_ok, assin_lista_ok) ou None se a leitura falha."""
    try:
        lista, resumo, verifica = PB.ler_vsc(vsc)
    except Exception:
        return None
    item = lista.get(nome_arq)
    hash_ok = item is not None and item[:2] == (len(conteudo), hashlib.sha512(conteudo).digest())
    assin = item is not None and bool(verifica(item[2], item[1]))
    return hash_ok, assin, resumo["assin_lista_ok"]


def vira(b, pos):
    b = bytearray(b); b[pos] ^= 0x01; return bytes(b)


res = collections.defaultdict(lambda: collections.Counter())
cert_de = {}
for k in sel:                                         # certificados dos pares para a troca
    vsc = z.read(por[k]["vota"]); raiz, _ = der.ler(vsc)
    ue = next(b for b in raiz["f"] if b["k"] and len(b["f"]) >= 5 and b["f"][2]["k"] and b["f"][2]["f"][0]["f"][0]["v"][:4].upper() == b"UEAO")
    cert_de[k] = ue["f"][4]["v"]
for k in sel:
    vsc = z.read(por[k]["vota"]); bu_nome = por[k]["bu"]; bu = z.read(bu_nome)
    raiz, _ = der.ler(vsc)
    ue = next(b for b in raiz["f"] if b["k"] and len(b["f"]) >= 5 and b["f"][2]["k"] and b["f"][2]["f"][0]["f"][0]["v"][:4].upper() == b"UEAO")
    lista_bytes = ue["f"][3]["v"]; assin_lista = ue["f"][2]["f"][3]["f"][2]["v"]; cert = ue["f"][4]["v"]
    # o nome do arquivo na lista é o nome dentro do pacote
    nome_na_lista = bu_nome.split("/")[-1]
    def reg(mut, r):
        res[mut]["total"] += 1
        if r is None:
            res[mut]["falha_de_leitura"] += 1; return
        h, a, l = r
        res[mut]["hash_rejeita"] += (not h); res[mut]["assinatura_do_arquivo_rejeita"] += (not a); res[mut]["assinatura_da_lista_rejeita"] += (not l)
        res[mut]["rejeitado_por_algum_controle"] += int((not h) or (not a) or (not l))
    reg("0_genuino", avalia(vsc, nome_na_lista, bu))
    reg("1_byte_alterado_no_BU", avalia(vsc, nome_na_lista, vira(bu, len(bu) // 2)))
    reg("2_BU_truncado", avalia(vsc, nome_na_lista, bu[: len(bu) // 2]))
    p = vsc.find(lista_bytes); reg("3_byte_alterado_na_lista", avalia(vira(vsc, p + len(lista_bytes) // 2), nome_na_lista, bu) if p >= 0 else None)
    p = vsc.find(assin_lista); reg("4_byte_alterado_na_assinatura_da_lista", avalia(vira(vsc, p + len(assin_lista) // 2), nome_na_lista, bu) if p >= 0 else None)
    outro = next((o for o in sel if o != k and len(cert_de[o]) == len(cert) and cert_de[o] != cert), None)
    p = vsc.find(cert)
    reg("5_certificado_de_outra_urna", avalia(vsc[:p] + cert_de[outro] + vsc[p + len(cert):], nome_na_lista, bu) if (outro and p >= 0) else None)
    reg("6_arquivo_fora_da_lista", avalia(vsc, "arquivo-que-nao-esta-na-lista.dat", bu))
    reg("7_nome_trocado_entre_arquivos", avalia(vsc, nome_na_lista.replace("bu", "rdv").replace(".rdv", ".rdv"), bu))
R = {"ano": ANO, "uf": UF, "secoes_avaliadas": N, "semente": 20261028 + int(ANO), "controles": {m: dict(c) for m, c in sorted(res.items())}}

# ---- controle hostil sintético (só em memória) ----
def cert_sintetico(emissor_cn):
    chave = ec.generate_private_key(ec.SECP521R1())
    nome = lambda cn: x509.Name([x509.NameAttribute(x509.NameOID.COMMON_NAME, cn)])
    agora = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
    c = (x509.CertificateBuilder().subject_name(nome("TESTE-SINTETICO-0001")).issuer_name(nome(emissor_cn)).public_key(chave.public_key())
         .serial_number(1).not_valid_before(agora).not_valid_after(agora + datetime.timedelta(days=365)).sign(chave, hashes.SHA512()))
    return chave, c.public_bytes(Encoding.DER)


ac = cadeia.carrega_acs(); sint = {}
for rotulo, emis in (("emissor_desconhecido", "TESTE-SINTETICO-EMISSOR"), ("emissor_declara_ser_AC_URNA", "AC URNA")):
    chave, cb = cert_sintetico(emis); h = hashlib.sha512(b"lista sintetica").digest()
    sig = chave.sign(h, ec.ECDSA(hashes.SHA512()))
    _, cn, emissor, verifica = PB._verificador(cb)
    info = cadeia.analisa_cert(cb, ac)
    sint[rotulo] = {"verificacao_de_lista_aceita": bool(verifica(sig, h)), "cadeia_ok": info["cadeia_ok"], "emissor_declarado": emissor, "leitura": "autoconsistente; a cadeia é o que separa de um certificado oficial"}
R["controle_hostil_sintetico"] = sint
json.dump(R, open(f"{RAIZ}/operacao_veracidade/resultados/controles_mutacao_{ANO}_{UF}.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
