"""Carimbo de tempo independente (OpenTimestamps, ancorado no Bitcoin) para provar que um arquivo existia numa data.

Uso:  python scripts/carimbo.py criar  <arquivo> [...]   grava <arquivo>.ots (pendente até a confirmação no Bitcoin, algumas horas)
      python scripts/carimbo.py atualizar <arquivo> [...] completa o .ots depois da confirmação
      python scripts/carimbo.py verificar <arquivo> [...] confere o arquivo contra o .ots
Serve para o manifesto dos dados do TSE (dados/listas/MANIFESTO.csv) e para o resumo de cada versão congelada: se o TSE trocar
um arquivo no futuro, o hash diferente e o carimbo mostram o que existia antes. Não guarda o conteúdo (para isso, ver
DADOS_PRESERVACAO.md).
"""
import os
import subprocess
import sys

OTS = os.path.join(os.path.dirname(sys.executable), "ots")
if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("criar", "atualizar", "verificar"):
        sys.exit(__doc__)
    cmd = {"criar": "stamp", "atualizar": "upgrade", "verificar": "verify"}[sys.argv[1]]
    for arq in sys.argv[2:]:
        alvo = arq if cmd == "stamp" else arq + ".ots"
        r = subprocess.run([OTS, cmd, alvo], capture_output=True, text=True)
        print(arq, "→", (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "ok")
