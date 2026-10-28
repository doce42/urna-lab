# Como reproduzir a Operação Veracidade Geral

Pré-requisitos: ambiente do projeto (`make ambiente`, Python 3.13, `.venv`), dados do TSE já no disco (`make dados-do-zero` leva horas e ~250 GB), 12 núcleos de CPU. Tudo roda a partir da raiz do projeto com `nice`. Nenhum comando abaixo escreve em dados brutos, versões congeladas ou `testes/registro.json`.

| Etapa | Comando | Tempo aproximado |
|---|---|---|
| Estado, integridade dos snapshots | `.venv/bin/python operacao_veracidade/scripts/integridade_snapshots.py` | 1 min |
| T60a: extrair e verificar os certificados (4 combinações ano × turno) | `for a in 2026 2022; do for t in 1 2; do nice .venv/bin/python operacao_veracidade/scripts/cert_extrai.py $a $t 12; done; done` e depois `cert_analise.py`, `casos_certificado.py` | 13 a 25 min por combinação |
| T60b: controles de mutação | `controles_mutacao.py 2026 AC` e `controles_mutacao.py 2022 AL` | segundos |
| T61: boletins de terceiros | baixar os arquivos estáticos para `externo/arvor_totalizacao/` (lista em `SHA256SUMS.txt`), depois `terceiros_qr.py` e `terceiros_qr_relogio.py` | segundos |
| T62: identificabilidade | `identificabilidade.py` | segundos |
| T63: grade adversarial | `sim_adversarial.py 2026 6 20` e `sim_adversarial.py 2022 6 20`; depois `sim_fabricacao_v2.py <ano> 20` e `gera_tabelas_sim.py` | ~1 min por ano |
| T64: zeros | `zeros_contagens.py` e `zeros_locais.py` | ~10 min |
| Documento 07 | `gera_respostas.py` | segundos |
| Hashes | `sha256sum` do conteúdo (ver `SHA256SUMS.txt`) | segundos |

**Sementes:** integridade, 20261028; mutação, 20261028 + ano; grade, derivada de `sha256(ano|mecanismo|sentido|X|réplica)`; bootstrap de limiares, 11 (limiar) e 12 (falso alarme); fabricantes, `sha256(ano|fab|...)`; zeros, 64. **Parâmetros** de cada teste estão no cabeçalho do próprio script e em `PROTOCOLO_PRE_EXECUCAO.md`.

**Entradas externas:** `fase2/externos/certificados/*.txt` (ACs de terceiro, SHA-256 em `resultados/cert_analise.json`), `externo/arvor_totalizacao/` (arquivos estáticos públicos de terceiros, baixados em 28/10/2026).
