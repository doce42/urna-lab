"""Publica o projeto no GitHub a partir de uma cópia higienizada, com trava de vazamento.

Fluxo: lista os arquivos que o .gitignore deixa versionar → copia para a pasta de publicação (fora do projeto) →
troca caminhos da máquina por relativos → varre a cópia atrás de termos pessoais e de segredos → confere tamanhos →
commita com a identidade de privacidade do GitHub e envia. Se a varredura achar qualquer coisa, aborta antes do commit.

Termos pessoais a bloquear (e-mail, nome de usuário do computador, nomes de outros projetos) ficam em
scripts/.privado.txt (uma expressão regular por linha, ignorada pelo git): este script não os traz escritos.
Regras do projeto: sem GitHub Actions e sem Git LFS (limites pagos); a computação roda na máquina local.

Uso:  python scripts/publicar.py --simular            só prepara e varre, sem commitar
      python scripts/publicar.py "mensagem do commit"  prepara, varre, commita e envia
"""
import os
import re
import shutil
import subprocess
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DEST = os.path.abspath(os.path.join(RAIZ, "..", "urna-lab-publico"))
REMOTO = "https://github.com/doce42/urna-lab.git"
NOME, EMAIL = "doce42", "208726053+doce42@users.noreply.github.com"  # e-mail de privacidade do GitHub (nunca o pessoal)
MAX_ARQUIVO, MAX_TOTAL = 20e6, 120e6
SEGREDOS = [r"gh[pousr]_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}", r"sk-[A-Za-z0-9]{20,}", r"AKIA[0-9A-Z]{16}",
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"(?i)\b(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"][^'\"\s]{8,}"]
NAO_COPIAR = {".git"}


def privados():
    f = os.path.join(RAIZ, "scripts", ".privado.txt")
    if not os.path.exists(f):
        sys.exit("falta scripts/.privado.txt (termos pessoais a bloquear); crie antes de publicar")
    return [l.strip() for l in open(f, encoding="utf-8") if l.strip() and not l.startswith("#")]


def arquivos():
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=RAIZ, capture_output=True, check=True).stdout
    return [p.decode() for p in out.split(b"\0") if p]


DISCO = os.path.dirname(os.path.dirname(RAIZ))  # ponto de montagem do disco grande (dois níveis acima do projeto)


def higieniza(texto, codigo):
    """Caminhos da máquina viram relativos, sem quebrar código: em .py/.sh/Makefile só os ajustes seguros;
    as trocas por texto (<DISCO_GRANDE>, ~) ficam só para documentação e dados."""
    r = re.escape(RAIZ)
    texto = re.sub(rf'(?m)^(\s*)P={r}\s*$', r'\1P="$(cd "$(dirname "$0")/.." && pwd)"', texto)
    texto = re.sub(rf'(?m)^(P|RAIZ)\s*=\s*"{r}"', r'\1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")', texto)
    texto = texto.replace(RAIZ + "/", "").replace(RAIZ, ".")
    if codigo:
        return texto.replace(DISCO, ".")  # em shell/python, o ponto de montagem vira o diretório atual (ex.: df -BG .)
    texto = re.sub(r"/tmp/claude-[^\s\"')]+", "<tmp>", texto)
    texto = re.sub(r"/home/[^/\s\"')]+", "~", texto)
    return texto.replace(DISCO, "<DISCO_GRANDE>")


def copia():
    for item in os.listdir(DEST) if os.path.isdir(DEST) else []:
        if item not in NAO_COPIAR:
            p = os.path.join(DEST, item)
            shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)
    os.makedirs(DEST, exist_ok=True)
    n = 0
    for rel in arquivos():
        src, dst = os.path.join(RAIZ, rel), os.path.join(DEST, rel)
        if not os.path.lexists(src):
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.islink(src):
            os.symlink(os.readlink(src), dst)
            continue
        try:
            texto = open(src, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            shutil.copy2(src, dst)  # binário: copiado como está
        else:
            codigo = rel.endswith((".py", ".sh")) or os.path.basename(rel) == "Makefile"
            open(dst, "w", encoding="utf-8").write(higieniza(texto, codigo))
        n += 1
    return n


def varre(termos):
    padroes = [(t, re.compile(t, re.I)) for t in termos] + [("segredo", re.compile(s)) for s in SEGREDOS]
    achados, total = [], 0
    for pasta, dirs, nomes in os.walk(DEST):
        dirs[:] = [d for d in dirs if d not in NAO_COPIAR]
        for n in nomes:
            p = os.path.join(pasta, n)
            if os.path.islink(p):
                continue
            rel = os.path.relpath(p, DEST)
            tam = os.path.getsize(p)
            total += tam
            if tam > MAX_ARQUIVO:
                achados.append((rel, "arquivo grande demais", f"{tam / 1e6:.1f} MB"))
            if re.search(r"(?i)(\.env|\.pem|\.key|id_rsa|credentials)$", n):
                achados.append((rel, "nome de arquivo sensível", n))
            try:
                texto = open(p, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            for rotulo, rx in padroes:
                m = rx.search(texto) or rx.search(rel)
                if m:
                    achados.append((rel, "termo bloqueado" if rotulo != "segredo" else "possível segredo", "(oculto)" if rotulo != "segredo" else m.group(0)[:6] + "…"))
    if total > MAX_TOTAL:
        achados.append(("(total)", "repositório grande demais", f"{total / 1e6:.0f} MB"))
    return achados, total


def git(*args, **kw):
    return subprocess.run(["git", *args], cwd=DEST, check=kw.get("check", True), capture_output=kw.get("capture", False), text=True)


def main():
    simular = "--simular" in sys.argv
    msg = next((a for a in sys.argv[1:] if not a.startswith("--")), "Atualização do projeto")
    n = copia()
    achados, total = varre(privados())
    print(f"{n} arquivos preparados em {DEST} ({total / 1e6:.1f} MB)")
    if achados:
        print("PUBLICAÇÃO BLOQUEADA, a varredura encontrou:")
        for rel, tipo, detalhe in achados:
            print(f"  {tipo}: {rel} {detalhe}")
        sys.exit(2)
    print("varredura limpa: nenhum termo pessoal, segredo ou arquivo grande")
    if simular:
        return
    if not os.path.isdir(os.path.join(DEST, ".git")):
        git("init", "-b", "main")
        git("remote", "add", "origin", REMOTO)
    git("config", "user.name", NOME)
    git("config", "user.email", EMAIL)
    git("add", "-A")
    if git("diff", "--cached", "--quiet", check=False).returncode == 0:
        print("nada novo para publicar")
        return
    git("commit", "-m", msg + "\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>")
    git("-c", "credential.helper=", "-c", "credential.helper=!gh auth git-credential", "push", "-u", "origin", "main")
    print("publicado:", REMOTO)


main()
