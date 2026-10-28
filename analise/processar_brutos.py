"""Lê os arquivos brutos das urnas (log e boletim impresso) e extrai dados exatos por urna.

Uso: python processar_brutos.py <turno> [UF ...]
  1º turno: lê os pacotes oficiais por estado (dados/brutos/1turno/*.zip)
  2º turno: lê os arquivos baixados urna por urna (dados/brutos/2turno/<UF>/)
Saída (analise/brutos/<turno>t/):
  urnas_<UF>.parquet   uma linha por urna: modelo, votos computados no log, hora do primeiro e do último voto,
                       eventos do log, (1º turno) votos de Presidente lidos do boletim impresso,
                       recontagem de Presidente pelo RDV (rdv_*), conferência de tamanho + SHA-512 de cada
                       arquivo contra a lista assinada pela urna (hash_ok_<tipo>), e verificação criptográfica
                       das assinaturas da urna (assin_lista_ok, assin_ok_<tipo>): Ed521 nas UE2020/UE2022,
                       ECDSA P-521 + SHA-512 nas UE2013/UE2015
  minutos_<UF>.parquet votos computados por minuto (hora local da urna), por município
"""
import collections
import glob
import hashlib
import io
import os
import re
import sys
import zipfile
from concurrent.futures import ProcessPoolExecutor

import base64

import pandas as pd
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

import der
import ed521
import seqlog

# ano da eleição: variável de ambiente ANO (padrão 2026). Códigos e datas de cada ano.
ANO = os.environ.get("ANO", "2026")
DIA = {"2026": {1: "04/10/2026", 2: "25/10/2026"}, "2022": {1: "02/10/2022", 2: "30/10/2022"}}[ANO]

AQUI = os.path.dirname(os.path.abspath(__file__))
BRUTOS = os.path.join(AQUI, "..", "dados", "brutos") if ANO == "2026" else os.path.join(AQUI, "..", "dados", ANO, "brutos")
NOME = re.compile(r"o(\d{5})([a-z]{2})(\d{5})(\d{4})(\d{4})-(\w+)\.(\w+)$")
EVENTOS = {
    "computado": "O voto do eleitor foi computado",
    "conf_presidente": "Voto confirmado para [Presidente]",
    "nulo_suspensao_presidente": "Atribuido voto nulo por suspensão [Presidente]",
    "corrigiu": "Eleitor corrigiu na tela de confirmação",
    "habilitado": "Eleitor foi habilitado",
    "digital_tentativa": "Solicita digital. Tentativa",
    "sem_biometria": "Habilitação sem biometria",
    "tecla_indevida": "Tecla indevida pressionada",
    "aplicacao_iniciada": "Iniciando aplicação",
    "impressao": "Início de impressão",
}


def linhas_do_log(dado):
    """log.jez é um zip com logd.dat; se a urna foi reiniciada/trocada, traz também logs arquivados (.jez dentro do .jez)."""
    z = zipfile.ZipFile(io.BytesIO(dado))
    linhas, n = [], 0
    for nome in sorted(z.namelist(), key=lambda x: (x == "logd.dat", x)):  # arquivados primeiro, logd.dat por último
        conteudo = z.read(nome)
        if nome.endswith(".jez"):
            sub, k = linhas_do_log(conteudo)
            linhas += sub; n += k
        else:
            linhas += conteudo.decode("latin1").splitlines(); n += 1
    return linhas, n


def ler_log(dado, turno=None):
    """Devolve (resumo, contagem por minuto) do log da urna."""
    linhas, n_arquivos = linhas_do_log(dado)
    r = {k: 0 for k in EVENTOS}
    r["modelo"] = None
    minutos = collections.Counter()
    votos = []
    ids_voto = set()  # urnas que registraram votos (mais de uma = urna substituída no meio do dia)
    for l in linhas:
        p = l.split("\t")
        if len(p) < 5:
            continue
        msg = p[4]
        if r["modelo"] is None and msg.startswith("Identificação do Modelo de Urna:"):
            r["modelo"] = msg.split(":", 1)[1].strip()
        # no 2º turno a mesma urna traz, arquivado, o log do 1º turno: só contam eventos do dia da eleição do turno
        if turno in DIA and not p[0].startswith(DIA[turno]):
            continue
        for k, e in EVENTOS.items():
            if msg.startswith(e) or (k == "sem_biometria" and e in msg):
                r[k] += 1
        if msg.startswith("O voto do eleitor foi computado"):
            votos.append(p[0])
            ids_voto.add(p[2])
            minutos[p[0][:16]] += 1  # dd/mm/aaaa hh:mm (hora local da urna)
    r["primeiro_voto"] = votos[0] if votos else None
    r["ultimo_voto"] = votos[-1] if votos else None
    r["arquivos_log"] = n_arquivos
    if turno in DIA:
        r.update(seqlog.analisa(linhas, DIA[turno]))  # sequência eleitor a eleitor (T28–T31, T33)
    r["ids_urna_log"] = ",".join(sorted(ids_voto))
    r["urnas_com_voto_no_log"] = len(ids_voto)
    return r, minutos


ELEICAO_PRES = {"2026": {1: 6257, 2: 6258}, "2022": {1: 544, 2: 545}}[ANO]


def ler_rdv(dado, turno):
    """Recontagem de Presidente pelo Registro Digital do Voto.
    Tipos de voto no RDV: 2 = nominal (com o número digitado), 3 = branco, 4 = nulo; outros ficam em rdv_tipo<N>."""
    raiz, _ = der.ler(dado)
    corpo = raiz["f"][2]
    r = collections.Counter()
    for ele in corpo["f"][4]["f"]:
        if int.from_bytes(ele["f"][0]["v"], "big") != ELEICAO_PRES[turno]:
            continue
        for cargo in ele["f"][1]["f"]:
            if int.from_bytes(cargo["f"][0]["v"], "big") != 1:  # cargo 1 = Presidente
                continue
            for v in cargo["f"][2]["f"]:
                tipo = int.from_bytes(v["f"][0]["v"], "big")
                if tipo == 2:
                    r["rdv_v" + v["f"][1]["v"].decode()] += 1
                elif tipo == 3:
                    r["rdv_branco"] += 1
                elif tipo == 4:
                    r["rdv_nulo"] += 1
                else:
                    r[f"rdv_tipo{tipo}"] += 1
    return dict(r)


def _verificador(cert_bytes):
    """Devolve (algoritmo, id da urna no certificado, emissor, função verifica(assinatura, hash64))."""
    if cert_bytes.startswith(b"-----BEGIN"):  # UE2020/UE2022: certificado PEM com chave Ed521 (OID 1.3.6.1.4.1.44588.2.1)
        c, _ = der.ler(base64.b64decode(b"".join(l for l in cert_bytes.splitlines() if not l.startswith(b"-"))))
        tbs = c["f"][0]
        pub = tbs["f"][6]["f"][1]["v"][1:]
        nomes = lambda no: [x["f"][0]["f"][1]["v"].decode("latin1") for x in no["f"] if x["k"] and x["f"] and x["f"][0]["k"]]
        cn = [n for n in nomes(tbs["f"][5]) if n.upper().startswith("UEAO")]
        emissor = nomes(tbs["f"][3])[0]
        return "Ed521", (cn[0] if cn else None), emissor, lambda sig, h: ed521.verifica(pub, sig, h)
    _, fim = der.ler(cert_bytes)  # há bytes de preenchimento depois do certificado: recorta no tamanho declarado
    cert = x509.load_der_x509_certificate(cert_bytes[:fim])  # UE2013/UE2015: X.509 padrão, ECDSA P-521
    pub = cert.public_key()

    def verifica(sig, h):
        try:
            pub.verify(sig, h, ec.ECDSA(hashes.SHA512()))
            return True
        except InvalidSignature:
            return False
    cn = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    emissor = cert.issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    return "ECDSA-P521", cn, emissor, verifica


def ler_bu(dado, turno):
    """T17b: o boletim digital (bu.dat), o arquivo somado na totalização.
    Envelope → conteúdo DER: [7] habilitações (sem biometria, biométrica, biográfica); [8] eleições, cada uma com
    (código, aptos, …, resultados: (tipo, comparecimento, cargos: (código; 1 = Presidente, qtd, votáveis:
    (tipo de voto: 1 nominal, 2 branco, 3 nulo; quantidade; (partido, número); ordem; hash encadeado))))."""
    env, _ = der.ler(dado)
    bu, _ = der.ler(env["f"][4]["v"])
    num = lambda no: int.from_bytes(no["v"], "big")
    r = {}
    # os campos são localizados pelo conteúdo, não pela posição: no exterior não há o campo de habilitações
    # (sem biometria) e a lista de eleições fica uma posição antes
    hab = next((x for x in bu["f"] if x["c"] == 2 and x["t"] == 1 and x["k"] and len(x["f"]) == 3), None)
    if hab is not None:
        r["bu_hab_sem_biometria"], r["bu_hab_biometrica"], r["bu_hab_biografica"] = (num(x) for x in hab["f"])

    def eh_lista_eleicoes(x):
        return (x["c"] == 0 and x["t"] == 16 and x["k"] and x["f"] and x["f"][0]["k"] and x["f"][0]["f"]
                and not x["f"][0]["f"][0]["k"] and num(x["f"][0]["f"][0]) in set(ELEICAO_PRES.values()) | {6259, 6260, 546, 547})
    eleicoes = next((x for x in bu["f"] if eh_lista_eleicoes(x)), {"f": []})
    for ele in eleicoes["f"]:
        if num(ele["f"][0]) != ELEICAO_PRES[turno]:
            continue
        r["bu_aptos"] = num(ele["f"][1])
        for res in ele["f"][4]["f"]:
            r["bu_comparecimento"] = num(res["f"][1])
            for cargo in res["f"][2]["f"]:
                if num(cargo["f"][0]) != 1:
                    continue
                for v in cargo["f"][2]["f"]:
                    tipo, qtd = num(v["f"][0]), num(v["f"][1])
                    if tipo == 1:
                        r["bu_v" + str(num(v["f"][2]["f"][1]))] = qtd
                    elif tipo == 2:
                        r["bu_branco"] = qtd
                    elif tipo == 3:
                        r["bu_nulo"] = qtd
                    else:
                        r[f"bu_tipo{tipo}"] = qtd
    return r


def ler_vsc(dado):
    """Bloco da urna (UEAO/ueao) do vota.vsc: lista de arquivos assinada, assinatura da lista e certificado da urna.
    Devolve (lista nome -> (tamanho, sha512, assinatura), resumo, função verifica)."""
    raiz, _ = der.ler(dado)
    ue = next(b for b in raiz["f"] if b["k"] and len(b["f"]) >= 5 and b["f"][2]["k"]
              and b["f"][2]["f"][0]["f"][0]["v"][:4].upper() == b"UEAO")
    alg, cn, emissor, verifica = _verificador(ue["f"][4]["v"])
    cab = ue["f"][2]["f"][3]
    lista_bytes = ue["f"][3]["v"]
    lista_ok = cab["f"][1]["v"] == hashlib.sha512(lista_bytes).digest() and verifica(cab["f"][2]["v"], cab["f"][1]["v"])
    lista, _ = der.ler(lista_bytes)
    out = {}
    for item in lista["f"][0]["f"]:
        nome = item["f"][0]["v"].decode()
        m = item["f"][1]["f"]
        out[nome] = (int.from_bytes(m[0]["v"], "big"), m[1]["v"], m[2]["v"])
    resumo = {"algoritmo": alg, "cert_urna": cn, "cert_emissor": emissor, "assin_lista_ok": bool(lista_ok)}
    return out, resumo, verifica


PRES = re.compile(r"-+PRESIDENTE-+\n(.*?)\n-{10,}\n(.*?)Total Apurado\s+(\d+)", re.S)


def ler_imgbu(dado):
    """Lê o bloco de Presidente do boletim impresso (texto)."""
    t = dado.decode("latin1")
    m = PRES.search(t)
    if not m:
        return None
    r = {}
    for l in m.group(1).splitlines():
        c = re.match(r"\s+(.+?)\s{2,}(\d{2})\s+(\d+)\s*$", l)
        if c:
            r[f"img_v{c.group(2)}"] = int(c.group(3))
    for campo, chave in (("Brancos", "img_branco"), ("Nulos", "img_nulo")):
        c = re.search(campo + r"\s+(\d+)", m.group(2))
        r[chave] = int(c.group(1)) if c else 0
    r["img_total"] = int(m.group(3))
    c = re.search(r"Comparecimento\s+(\d+)", t)
    r["img_comparecimento"] = int(c.group(1)) if c else None
    return r


def fonte(turno, uf):
    """Pacote oficial por estado quando existe; senão, os arquivos baixados urna por urna (2º turno de SP)."""
    pasta_pac = ("1turno" if turno == 1 else "2turno_pacotes") if ANO == "2026" else f"{turno}turno"
    pacote = os.path.join(BRUTOS, pasta_pac, f"bu_imgbu_logjez_rdv_vscmr_{ANO}_{turno}t_{uf}.zip")
    pasta = os.path.join(BRUTOS, "2turno", uf)
    return pacote, pasta


def processa(turno, uf, parte=0, partes=1):
    """Processa um estado inteiro, ou só a parte `parte` de `partes` (urnas divididas pelo número da seção),
    para estados grandes rodarem em paralelo. As partes são juntadas no fim, em urnas_<UF>.parquet."""
    saida = os.path.join(AQUI, "brutos", f"{turno}t" if ANO == "2026" else f"{ANO}_{turno}t")
    os.makedirs(saida, exist_ok=True)
    pacote, pasta = fonte(turno, uf)
    if os.path.exists(pacote):
        zf = zipfile.ZipFile(pacote)
        nomes = zf.namelist()
        ler = zf.read
    elif turno == 2 and os.path.isdir(pasta):
        nomes = os.listdir(pasta)
        ler = lambda n: open(os.path.join(pasta, n), "rb").read()
    else:
        return f"{uf}: sem arquivos"
    urnas = collections.defaultdict(dict)
    minutos = collections.Counter()
    calculado = collections.defaultdict(dict)  # urna -> nome do arquivo -> (tamanho, sha512)
    assinado = {}                              # urna -> lista assinada pela urna
    for n in nomes:
        m = NOME.search(n)
        if not m or m.group(6) not in ("log", "imgbu", "rdv", "bu", "vota", "busa"):
            continue
        chave = (m.group(2).upper(), str(int(m.group(3))), str(int(m.group(4))), str(int(m.group(5))))
        if partes > 1 and (int(m.group(3)) * 7919 + int(m.group(4)) * 31 + int(m.group(5))) % partes != parte:
            continue
        u = urnas[chave]
        try:
            dado = ler(n)
            if m.group(6) == "vota":
                assinado[chave] = ler_vsc(dado)
                u.update(assinado[chave][1])
                continue
            calculado[chave][n] = (len(dado), hashlib.sha512(dado).digest())
            if m.group(6) == "log":
                r, mins = ler_log(dado, turno)
                u.update(r)
                for k, v in mins.items():
                    minutos[(chave[1], k)] += v
            elif m.group(6) == "rdv":
                try:
                    u.update(ler_rdv(dado, turno))
                except (KeyError, IndexError):
                    u["rdv_vazio_ou_outro_formato"] = True  # seções do Sistema de Apuração: RDV sem votos
            elif m.group(6) in ("bu", "busa"):
                # busa: boletim do Sistema de Apuração (seção apurada fora da urna; o RDV vem vazio)
                u.update(ler_bu(dado, turno))
                if m.group(6) == "busa":
                    u["origem"] = "sistema_de_apuracao"
            elif m.group(6) == "imgbu":
                r = ler_imgbu(dado)
                if r:
                    u.update(r)
        except Exception as e:
            u["erro"] = f"{n}: {e}"
    for chave, u in urnas.items():
        lista, _, verifica = assinado.get(chave, (None, None, None))
        u["tem_assinatura"] = lista is not None
        for nome, (tam, h) in calculado[chave].items():
            tipo = NOME.search(nome).group(6)
            item = lista.get(nome) if lista else None
            u[f"hash_ok_{tipo}"] = item is not None and item[:2] == (tam, h)
            u[f"assin_ok_{tipo}"] = item is not None and verifica(item[2], item[1])
        cn, ids = u.get("cert_urna"), u.get("ids_urna_log") or ""
        u["cert_igual_log"] = bool(cn and any(i and cn.upper().endswith(i) for i in ids.split(",")))
    df = pd.DataFrame([{"SG_UF": k[0], "CD_MUNICIPIO": k[1], "NR_ZONA": k[2], "NR_SECAO": k[3], **v} for k, v in urnas.items()])
    suf = f"_parte{parte}" if partes > 1 else ""
    df.to_parquet(os.path.join(saida, f"urnas_{uf}{suf}.parquet"))
    mi = pd.DataFrame([{"SG_UF": uf, "CD_MUNICIPIO": k[0], "minuto": k[1], "votos": v} for k, v in minutos.items()])
    mi.to_parquet(os.path.join(saida, f"minutos_{uf}{suf}.parquet"))
    return f"{uf}: {len(df)} urnas, {int(df.get('computado', pd.Series(dtype=int)).sum()):,} votos no log"


URNAS_POR_PARTE = 12000  # estados maiores que isso são divididos em partes processadas em paralelo


def juntar(turno, uf, partes):
    saida = os.path.join(AQUI, "brutos", f"{turno}t" if ANO == "2026" else f"{ANO}_{turno}t")
    for tipo in ("urnas", "minutos"):
        arqs = [os.path.join(saida, f"{tipo}_{uf}_parte{k}.parquet") for k in range(partes)]
        df = pd.concat([pd.read_parquet(a) for a in arqs], ignore_index=True)
        if tipo == "minutos" and len(df):
            df = df.groupby(["SG_UF", "CD_MUNICIPIO", "minuto"], as_index=False)["votos"].sum()
        df.to_parquet(os.path.join(saida, f"{tipo}_{uf}.parquet"))
        for a in arqs:
            os.remove(a)
    u = pd.read_parquet(os.path.join(saida, f"urnas_{uf}.parquet"), columns=["computado"])
    return f"{uf}: {len(u)} urnas, {int(u['computado'].sum()):,} votos no log ({partes} partes)"


if __name__ == "__main__":
    turno = int(sys.argv[1])
    ufs = sys.argv[2:] or "AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO ZZ".split()
    tarefas, partes_de = [], {}
    for uf in ufs:
        pacote, pasta = fonte(turno, uf)
        n = (len(zipfile.ZipFile(pacote).namelist()) if os.path.exists(pacote)
             else len(os.listdir(pasta)) if os.path.isdir(pasta) else 0) // 5
        partes_de[uf] = max(1, -(-n // URNAS_POR_PARTE))
        tarefas += [(turno, uf, k, partes_de[uf]) for k in range(partes_de[uf])]
    # maiores primeiro, para o último processo não ficar sozinho com um estado grande
    tarefas.sort(key=lambda t: -partes_de[t[1]])
    feitas = collections.Counter()
    with ProcessPoolExecutor(int(os.environ.get("NPROC", 12))) as ex:  # NPROC: processos em paralelo
        futuros = {ex.submit(processa, *t): t for t in tarefas}
        from concurrent.futures import as_completed
        for f in as_completed(futuros):
            t = futuros[f]
            msg = f.result()
            if t[3] == 1:
                print(msg, flush=True)
            else:
                feitas[t[1]] += 1
                if feitas[t[1]] == t[3]:
                    print(juntar(turno, t[1], t[3]), flush=True)
