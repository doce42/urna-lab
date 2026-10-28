"""Roda um teste pelo id do registro (testes/registro.json) ou lista todos.
Uso: python scripts/rodar_teste.py <id>   |   python scripts/rodar_teste.py --lista
O comando de cada teste está no registro; 'bateria' roda a bateria inteira (vários testes de uma vez).
"""
import json
import os
import subprocess
import sys

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
reg = json.load(open(os.path.join(RAIZ, "testes", "registro.json")))
EXTRA = {"bateria": "make bateria", "T08": ".venv/bin/python analise/testes.py", "T09": ".venv/bin/python analise/investigar.py",
         "T12": ".venv/bin/python analise/biometria.py", "T13": ".venv/bin/python analise/poder.py",
         "T32": ".venv/bin/python analise/totalizacao.py"}

if len(sys.argv) < 2 or sys.argv[1] == "--lista":
    for t in reg["testes"]:
        print(f"{t['id']:5} {t['modulo']}  {t['situacao']:13} {t['pergunta']}")
    sys.exit(0)
alvo = sys.argv[1]
if alvo in EXTRA:
    cmd = EXTRA[alvo]
else:
    t = next((t for t in reg["testes"] if t["id"] == alvo), None)
    if t is None:
        sys.exit(f"teste {alvo} não está no registro")
    cmd = t["comando"]
    if not cmd or cmd == "—":
        sys.exit(f"{alvo} ainda não tem comando (situação: {t['situacao']}). Veja .agents/skills e PIPELINE.md para implementar.")
    if cmd.startswith("make teste"):
        cmd = EXTRA.get(cmd.split("T=")[1].split()[0], cmd)
print(f"$ {cmd}")
sys.exit(subprocess.call(f"nice -n 10 {cmd}", shell=True, cwd=RAIZ))
