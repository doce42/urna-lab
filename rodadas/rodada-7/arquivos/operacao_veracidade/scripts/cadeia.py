"""Funções compartilhadas de verificação de certificados de urna (T60a, T60b, T61). Variante Ed521 fixada: M = TBS."""
import base64, datetime, hashlib, sys
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, RAIZ + "/analise")
import der, ed521  # noqa: E402
from cryptography import x509  # noqa: E402

CERT = RAIZ + "/fase2/externos/certificados"


def carrega_acs():
    ac = {}
    for nome in ("acurna", "acue2020", "acue2022"):
        pem = open(f"{CERT}/{nome}_certificado_publico.txt", "rb").read(); c = x509.load_pem_x509_certificate(pem)
        cn = c.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value; pub = None
        if nome != "acurna":
            r, _ = der.ler(base64.b64decode(b"".join(l for l in pem.splitlines() if not l.startswith(b"-")))); pub = r["f"][0]["f"][6]["f"][1]["v"][1:]
        ac[cn] = (c, pub, hashlib.sha256(pem).hexdigest())
    return ac


def ed_ok(pub, sig, M):
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
    return datetime.datetime.strptime(s, "%y%m%d%H%M%SZ" if len(s) == 13 else "%Y%m%d%H%M%SZ").replace(tzinfo=datetime.timezone.utc)


def analisa_cert(cb, ac):
    """cb: bytes do certificado (PEM ou DER). Devolve dict com algoritmo, CN, emissor, validade, chave pública (SHA-256),
    pub (bytes da chave Ed521 ou objeto da chave ECDSA) e cadeia_ok (assinatura da AC emissora; None se a AC não está disponível)."""
    if cb.startswith(b"-----BEGIN"):
        c = x509.load_pem_x509_certificate(cb); r, _ = der.ler(base64.b64decode(b"".join(l for l in cb.splitlines() if not l.startswith(b"-"))))
    else:
        _, fim = der.ler(cb); cb = cb[:fim]; c = x509.load_der_x509_certificate(cb); r, _ = der.ler(cb)
    tbs = r["f"][0]; spki = tbs["f"][6]["f"][1]["v"]
    ed = len(spki) == 67 or (len(spki) == 1 + 66)
    emis = c.issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    cn = c.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    out = {"cn": cn, "emissor": emis, "nao_antes": data(tbs["f"][4]["f"][0]), "nao_depois": data(tbs["f"][4]["f"][1]),
           "pub_sha256": hashlib.sha256(spki).hexdigest(), "sha256": hashlib.sha256(cb).hexdigest()}
    if emis not in ac:
        out.update(alg="?", cadeia_ok=None); return out
    if ed:
        out.update(alg="Ed521", pub=spki[1:], cadeia_ok=ed_ok(ac[emis][1], c.signature, c.tbs_certificate_bytes))
    else:
        try:
            c.verify_directly_issued_by(ac[emis][0]); ok = True
        except Exception:
            ok = False
        out.update(alg="ECDSA-P521", pub=c.public_key(), cadeia_ok=ok)
    return out
