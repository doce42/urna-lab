"""Verificação de assinatura Ed521 (EdDSA na curva E-521), usada pelas urnas modelo UE2020 e UE2022.

Curva de Edwards x² + y² = 1 + d·x²·y² sobre p = 2^521 − 1, d = −376014 (parâmetros públicos da E-521, SafeCurves).
Chave pública: 66 bytes (y em little-endian, bit de sinal de x no bit 527). Assinatura: R (66 bytes) || S (66 bytes, little-endian).
Desafio k = SHAKE256("SigEd521" || 0x00 || 0x00 || R || A || M, 132 bytes), little-endian, mod L.
A mensagem M que a urna assina é o SHA-512 do hash SHA-512 do conteúdo (achado nos dados: só essa combinação valida;
uma assinatura não valida por acaso).
"""
import hashlib

import gmpy2
from gmpy2 import mpz

p = mpz(2) ** 521 - 1
d = mpz(-376014) % p
L = mpz(2) ** 519 - mpz(337554763258501705789107630418782636071904961214051226618635150085779108655765)
Gx = mpz(0x752cb45c48648b189df90cb2296b2878a3bfd9f42fc6c818ec8bf3c9c0c6203913f6ecc5ccc72434b1ae949d568fc99c6059d0fb13364838aa302a940a2f19ba6c)
Gy = mpz(0x0c)
DOM = b"SigEd521\x00\x00"
ZERO = (mpz(0), mpz(1), mpz(1), mpz(0))


def soma(P, Q):
    x1, y1, z1, t1 = P; x2, y2, z2, t2 = Q
    A = x1 * x2 % p; B = y1 * y2 % p; C = d * t1 * t2 % p; D = z1 * z2 % p
    E = ((x1 + y1) * (x2 + y2) - A - B) % p
    F = (D - C) % p; G = (D + C) % p; H = (B - A) % p
    return (E * F % p, G * H % p, F * G % p, E * H % p)


def mult(k, P):
    R = ZERO
    k = int(k)
    while k:
        if k & 1:
            R = soma(R, P)
        P = soma(P, P); k >>= 1
    return R


def igual(P, Q):
    return (P[0] * Q[2] - Q[0] * P[2]) % p == 0 and (P[1] * Q[2] - Q[1] * P[2]) % p == 0


def decodifica(b):
    n = int.from_bytes(b, "little")
    sinal = n >> 527 & 1
    y = mpz(n & ((1 << 521) - 1))
    if y >= p:
        return None
    x2 = (y * y - 1) * gmpy2.invert((d * y * y - 1) % p, p) % p
    x = gmpy2.powmod(x2, (p + 1) // 4, p)
    if x * x % p != x2:
        return None
    if int(x) & 1 != sinal:
        x = p - x
    return (x, y, mpz(1), x * y % p)


B = (Gx, Gy, mpz(1), Gx * Gy % p)
# tabela do ponto base (2^i · B) para acelerar [S]B
_TAB = []
_P = B
for _ in range(522):
    _TAB.append(_P); _P = soma(_P, _P)


def mult_base(k):
    R = ZERO
    k = int(k); i = 0
    while k:
        if k & 1:
            R = soma(R, _TAB[i])
        k >>= 1; i += 1
    return R


def degenerado(P):
    """Ponto de ordem pequena (identidade ou divisor do cofator 4): não serve como chave nem como R."""
    return igual(mult(4, P), ZERO)


def verifica(pub, assinatura, h):
    """True se a assinatura Ed521 da urna sobre o hash SHA-512 h (64 bytes) é válida para a chave pública pub.
    Rejeita entradas malformadas e pontos degenerados (revisão R1, achado R1-02): sem isso, chave e R iguais à
    identidade com S = 0 passavam."""
    if len(pub) != 66 or len(assinatura) != 132:
        return False
    A = decodifica(pub)
    if A is None or degenerado(A):
        return False
    Rb = assinatura[:66]
    Rp = decodifica(Rb)
    if Rp is None or degenerado(Rp):
        return False
    S = mpz(int.from_bytes(assinatura[66:], "little"))
    if S >= L:
        return False
    M = hashlib.sha512(h).digest()
    k = mpz(int.from_bytes(hashlib.shake_256(DOM + Rb + pub + M).digest(132), "little")) % L
    return igual(mult_base(S), soma(Rp, mult(k, A)))
