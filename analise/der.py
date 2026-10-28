"""Leitor DER mínimo (ASN.1): devolve a árvore (classe, construído, etiqueta, conteúdo/filhos) sem precisar do esquema."""


def ler(buf, i=0):
    b = buf[i]; i += 1
    classe, cons, tag = b >> 6, bool(b & 0x20), b & 0x1F
    if tag == 0x1F:  # etiqueta longa
        tag = 0
        while True:
            x = buf[i]; i += 1
            tag = (tag << 7) | (x & 0x7F)
            if not x & 0x80:
                break
    n = buf[i]; i += 1
    if n & 0x80:
        k = n & 0x7F
        n = int.from_bytes(buf[i:i + k], "big"); i += k
    conteudo = buf[i:i + n]
    no = {"c": classe, "k": cons, "t": tag, "v": conteudo}
    if cons:
        no["f"] = filhos(conteudo)
    return no, i + n


def filhos(buf):
    out, i = [], 0
    while i < len(buf):
        no, i = ler(buf, i)
        out.append(no)
    return out


def mostrar(no, d=0, lim=None, maxd=12):
    lim = lim if lim is not None else [0]
    if lim[0] > 220 or d > maxd:
        return
    lim[0] += 1
    nome = "UACP"[no["c"]] + str(no["t"])
    if no["k"]:
        print("  " * d + f"[{nome}] ({len(no['f'])})")
        for f in no["f"]:
            mostrar(f, d + 1, lim, maxd)
    else:
        v = no["v"]
        txt = v[:48].decode("latin1") if v and all(32 <= c < 127 for c in v[:48]) else v[:24].hex()
        print("  " * d + f"[{nome}] {len(v)}B: {txt}")
