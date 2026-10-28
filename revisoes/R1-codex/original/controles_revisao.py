"""Controles mínimos desta revisão; lê cópias preservadas e só imprime.

Executar com o ambiente já existente do projeto, sem instalar dependências:
  ~/Projects/apuracao-analise/.venv/bin/python -B controles_revisao.py

Não reprocessa a eleição e não grava resultados no projeto.
"""
from pathlib import Path
import base64
import hashlib
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "fontes"
sys.path.insert(0, str(SOURCES / "urna-lab-local" / "analise"))
import processar_brutos as local  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "ed521_externo",
    SOURCES / "alissonlinneker__DataUrnas-BR/src/dataurnas/parsers/ed521.py",
)
external = importlib.util.module_from_spec(spec)
spec.loader.exec_module(external)

results = []
fixtures = SOURCES / "alissonlinneker__DataUrnas-BR/tests/ele2026/fixtures"
for path in sorted(fixtures.glob("vsc*.bin")):
    raw = path.read_bytes()
    entries, summary, verify = local.ler_vsc(raw)
    row = {
        "fixture": path.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "resumo_local": summary,
    }
    results.append(row)
    if summary["algoritmo"] != "Ed521":
        row["nota"] = (
            "ECDSA: leitura local da assinatura da lista válida; "
            "sem segundo verificador neste controle."
        )
        continue
    root, _ = local.der.ler(raw)
    hardware = next(
        block for block in root["f"]
        if block["k"] and len(block["f"]) >= 5
        and block["f"][2]["k"]
        and block["f"][2]["f"][0]["f"][0]["v"][:4].upper() == b"UEAO"
    )
    cert = hardware["f"][4]["v"]
    cert_der = base64.b64decode(
        b"".join(line for line in cert.splitlines() if not line.startswith(b"-"))
    )
    decoded, _ = local.der.ler(cert_der)
    public_key = decoded["f"][0]["f"][6]["f"][1]["v"][1:]
    row["itens"] = []
    for name, (_, digest, signature) in entries.items():
        row["itens"].append({
            "arquivo": name,
            "local": bool(verify(signature, digest)),
            "externo": bool(external.verificar(
                public_key, hashlib.sha512(digest).digest(), signature
            )),
            "negativo_hash_externo": bool(external.verificar(
                public_key, hashlib.sha512(bytes(64)).digest(), signature
            )),
        })

identity = (1).to_bytes(66, "little")
degenerate_signature = identity + bytes(66)
results.append({
    "chave_degenerada_identidade_local": local.ed521.verifica(
        identity, degenerate_signature, bytes(64)
    ),
    "chave_degenerada_identidade_externo": external.verificar(
        identity, bytes(64), degenerate_signature
    ),
    "pub_vazia_decodifica_local": local.ed521.decodifica(b"") is not None,
    "pub_vazia_decodifica_externo": external.decodificar_ponto(b"") is not None,
})
print(json.dumps(results, ensure_ascii=False, indent=2))
