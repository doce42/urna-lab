"""T60a: extrai o certificado de cada urna dos vota.vsc/.vscmr, verifica a assinatura da AC emissora (variante Ed521 fixada: M = TBS,
sem tentar outras) e registra validade, chave pública e CN. Protocolo: operacao_veracidade/PROTOCOLO_PRE_EXECUCAO.md.
Uso: cert_extrai.py <ano> <turno> [processos]  →  operacao_veracidade/resultados/certs_<ano>_<turno>t.parquet"""
import base64, collections, datetime, hashlib, os, sys, zipfile
from concurrent.futures import ProcessPoolExecutor

ANO, TURNO = sys.argv[1], int(sys.argv[2]); PROC = int(sys.argv[3]) if len(sys.argv) > 3 else 12
os.environ["ANO"] = ANO
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, RAIZ + "/analise")
import der, ed521, processar_brutos as PB  # noqa: E402
import pandas as pd  # noqa: E402
from cryptography import x509  # noqa: E402

DIA = {"2026": {1: "2026-10-04", 2: "2026-10-25"}, "2022": {1: "2022-10-02", 2: "2022-10-30"}}[ANO][TURNO]
UFS = "AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO ZZ".split()
OUT = f"{RAIZ}/operacao_veracidade/resultados/certs_{ANO}_{TURNO}t.parquet"
CERT = RAIZ + "/fase2/externos/certificados"


def carrega_acs():
    ac = {}
    for nome in ("acurna", "acue2020", "acue2022"):
        pem = open(f"{CERT}/{nome}_certificado_publico.txt", "rb").read(); c = x509.load_pem_x509_certificate(pem)
        cn = c.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        pub = None
        if nome != "acurna":
            r, _ = der.ler(base64.b64decode(b"".join(l for l in pem.splitlines() if not l.startswith(b"-")))); pub = r["f"][0]["f"][6]["f"][1]["v"][1:]
        ac[cn] = (c, pub, hashlib.sha256(pem).hexdigest())
    return ac


def ed_ok(pub, sig, M):
    """Ed521 com a mensagem M (variante fixada); mesma conta do ed521.verifica, mas com M dado."""
    if len(pub) != 66 or len(sig) != 132:
        return False
    A = ed521.decodifica(pub); Rb = sig[:66]; Rp = ed521.decodifica(Rb)
    if A is None or Rp is None or ed521.degenerado(A) or ed521.degenerado(Rp):
        return False
    S = ed521.mpz(int.from_bytes(sig[66:], "little"))
    if S >= ed521.L:
        return False
    k = ed521.mpz(int.from_bytes(hashlib.shake_256(ed521.DOM + Rb + pub + M).digest(132), "little")) % ed521.L
    return ed521.igual(ed521.mult_base(S), ed521.soma(Rp, ed521.mult(k, A)))


def data(no):
    s = no["v"].decode()
    f = "%y%m%d%H%M%SZ" if len(s) == 13 else "%Y%m%d%H%M%SZ"
    return datetime.datetime.strptime(s, f).replace(tzinfo=datetime.timezone.utc)


def nomes(no):
    return [x["f"][0]["f"][1]["v"].decode("latin1") for x in no["f"] if x["k"] and x["f"] and x["f"][0]["k"]]


def uf_job(uf):
    ac = carrega_acs(); pacote, pasta = PB.fonte(TURNO, uf)
    if os.path.exists(pacote):
        z = zipfile.ZipFile(pacote); ler = z.read; nomes_arq = z.namelist()
    elif TURNO == 2 and ANO == "2026" and os.path.isdir(pasta):
        nomes_arq = os.listdir(pasta); ler = lambda n: open(os.path.join(pasta, n), "rb").read()
    else:
        return []
    dia = datetime.datetime.fromisoformat(DIA).replace(tzinfo=datetime.timezone.utc)
    cache, linhas = {}, []
    for n in nomes_arq:
        a = PB.analisa_nome(n, uf)
        if not a or a[1] != "vota":
            continue
        chave = a[0]
        try:
            raiz, _ = der.ler(ler(n))
            ue = next(b for b in raiz["f"] if b["k"] and len(b["f"]) >= 5 and b["f"][2]["k"] and b["f"][2]["f"][0]["f"][0]["v"][:4].upper() == b"UEAO")
            cb = ue["f"][4]["v"]; h = hashlib.sha256(cb).hexdigest()
            if h not in cache:
                if cb.startswith(b"-----BEGIN"):
                    c = x509.load_pem_x509_certificate(cb); alg = "Ed521"
                    r, _ = der.ler(base64.b64decode(b"".join(l for l in cb.splitlines() if not l.startswith(b"-")))); tbs = r["f"][0]
                else:
                    _, fim = der.ler(cb); cb2 = cb[:fim]; c = x509.load_der_x509_certificate(cb2); alg = "ECDSA-P521"
                    r, _ = der.ler(cb2); tbs = r["f"][0]
                    pub_nome = None
                emis = c.issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
                cn = c.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
                nb, na = data(tbs["f"][4]["f"][0]), data(tbs["f"][4]["f"][1])
                pub_sha = hashlib.sha256(tbs["f"][6]["f"][1]["v"]).hexdigest()
                if emis not in ac:
                    ok = None
                elif alg == "Ed521":
                    ok = ed_ok(ac[emis][1], c.signature, c.tbs_certificate_bytes)
                else:
                    try:
                        c.verify_directly_issued_by(ac[emis][0]); ok = True
                    except Exception:
                        ok = False
                cache[h] = (alg, cn, emis, nb.isoformat(), na.isoformat(), pub_sha, ok, nb <= dia <= na, nb > dia)
            alg, cn, emis, nb, na, pub_sha, ok, valido_no_dia, emitido_depois = cache[h]
            linhas.append((*chave, h, alg, cn, emis, nb, na, pub_sha, ok, valido_no_dia, emitido_depois, ""))
        except Exception as e:
            linhas.append((*chave, "", "", "", "", "", "", "", None, None, None, str(e)[:80]))
    return linhas


if __name__ == "__main__":
    cols = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "cert_sha256", "alg", "cn", "emissor", "nao_antes", "nao_depois", "pub_sha256", "cadeia_ok", "valido_no_dia", "emitido_depois_da_eleicao", "erro"]
    rows = []
    with ProcessPoolExecutor(PROC) as ex:
        for uf, l in zip(UFS, ex.map(uf_job, UFS)):
            rows += l; print(uf, len(l), sum(1 for x in l if x[-1]), flush=True)
    pd.DataFrame(rows, columns=cols).to_parquet(OUT, index=False)
    print("ok", len(rows))
