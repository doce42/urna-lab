---
name: apuracao-dados
description: Baixar e preparar dados oficiais do TSE (votação por seção, Boletim de Urna, perfil do eleitorado, arquivos das urnas, correspondências, GEDAI) para o estudo da apuração. Use ao reproduzir do zero, acrescentar um ano/turno ou quando um download falhar.
---
# Dados oficiais do TSE

## Quando usar
Montar os dados do zero, acrescentar outra eleição (ex.: 2018), refazer um download ou diagnosticar arquivo faltando ou cortado.

## Comandos
- `make dados-do-zero` (= `scripts/preparar_dados.sh`): gera as listas (`scripts/listas_tse.py`), baixa, confere hashes e filtra só Presidente.
- Um conjunto só: `scripts/baixar_lista.sh dados/listas/<lista>.txt <pasta> <paralelos>`. Retoma downloads interrompidos e confere o `.sha512` quando existe (`.ok` = conferido).
- São Paulo do 2º turno, sem pacote: `.venv/bin/python scripts/baixar_sp_2t_educado.py` (controle de ritmo; vigia a publicação do pacote).

## Fontes
- Portal: https://dadosabertos.tse.jus.br (API CKAN `package_search`).
- CDN: `https://cdn.tse.jus.br/estatistica/sead/...`.
- Site de resultados: `https://resultados.tse.jus.br/oficial/ele2026/...` (config `ele-c.json`, totais `<uf>-c0001-e00<ele>-u.json`, arquivos por urna `arquivo-urna/<pleito>/...`).
- Códigos: eleição 6257 (1º turno) e 6258 (2º turno) de 2026; pleitos 3220 e 3221; 2022: 544/545, pleitos 406/407.

## Armadilhas (já aconteceram)
- **Disco:** só no SSD grande do projeto. Nunca extrair zip grande no disco do sistema; use `unzip -p | filtro`.
- **Portal de dados abertos:**
  - às vezes lista o `.sha512` no lugar do zip (RR, BU 2º turno 2026): use a URL sem `.sha512`;
  - não listou os pacotes das urnas do 2º turno, que já estavam no CDN: teste o endereço direto.
- **Download interrompido** deixa arquivo cortado (aconteceu com SP do 1º turno). Confira os totais depois (`make dados` para se não bater).
- **Site de resultados:** recusa (429) conexões demais e pune o IP se você insistir. HTTP/2 multiplexado + ritmo adaptativo; nunca mais de ~100 pedidos/s.
- **Seção agregada:** não tem urna própria (índice 404). Normal.
- **2022:** colunas `DS_AGREGADAS` e `QT_ELEITORES_BIOMETRIA_NH`; datas dd/mm/aaaa (`analise/montar_base.py` já trata).

## Validação
`make dados` confere BU × votação por seção voto a voto e para se não bater. `make verificar` mostra a cobertura.

## Preservação e dados leves
- **Manifesto e carimbo:** manifesto SHA-256 (`scripts/manifesto.py`) e carimbo de tempo (`scripts/carimbo.py`); ver `DADOS_PRESERVACAO.md`.
- **Pacote para terceiros:** `scripts/dados_leves.py` (ver `DADOS_LEVES.md`).
- **Fontes externas usadas:**
  - DataUrnas-BR (commit 12f0433) em `<DISCO_GRANDE>/externos/DataUrnas-BR`;
  - capturas do Internet Archive em `fase3/externos/wayback_capturas`.

## Atualização da rodada 7 (28/10/2026, V1.5)
- **Dados derivados novos fora do git** (`.gitignore`): `certs_<ano>_<turno>t.parquet` (~75 MB cada) e `rdv_nulos_<ano>_<turno>t.parquet`; reproduzíveis pelos scripts (ver `PIPELINE.md`, seção 7). O `publicar.py` recusa arquivo > 20 MB e total > 120 MB.
- **Dados de terceiros** ficam em `operacao_veracidade/externo/` fora do git (licença de redistribuição não verificada), com `SHA256SUMS.txt` e data de download.
- **Cobertura de hash oficial no manifesto:** 331 de 51.883 arquivos; o resto só tem hash local.
- **Fuso:** emissão e encerramento em hora local; recebimento em hora de Brasília.
- **Extração do RDV com o número digitado** (`fase3/rdv_nulos.py <ano> <turno>`): ~8 min por conjunto com 12 processos.

## Atualização da rodada 8 (aberta, 28/10/2026)
- **Hora de encerramento e de abertura estão em hora local.** MT, AM, MS, RO e RR: 7h a 16h; AC: 6h a 15h; os demais, 8h a 17h de Brasília. O fuso do município = 8 menos a hora de abertura (aberturas de 6h a 8h15). **Converta para Brasília antes de cortar em "17h"** (as 32.025 seções "antes das 17h locais" são desses estados). `DT_BU_RECEBIDO` já é Brasília.
- O encerramento de rotina cai de 17:00 a 17:15 (98%; mediana 17:01); a prorrogação de fato é depois de ~17:30.
