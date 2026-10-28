# Dados leves: pesquisar sem baixar os ~405 GB do TSE

> **Preliminar.** Este pacote é derivado dos arquivos oficiais pelo código deste repositório e é regerado a cada versão do estudo. Ele não substitui os dados oficiais. Para conclusões definitivas, confira com os brutos: o manifesto SHA-256 diz exatamente quais arquivos foram usados.

**Onde:** anexo do release no GitHub (`dados_leves_vX.Y.zip`), gerado por `python scripts/dados_leves.py`.

| Arquivo | O que tem | Linhas (aprox.) |
|---|---|---|
| `secoes_2026` e `secoes_2022` (`.parquet` e `.csv.gz`) | Resultado de Presidente por seção, 1º e 2º turnos numa linha: aptos, comparecimento, votos por candidato, brancos, nulos, horários de abertura, encerramento, emissão e recebimento do boletim, urna, local | ~500 mil por ano |
| `urnas_{ano}_{turno}t.parquet` | Resumo por urna lido dos **arquivos das urnas**: votos do boletim, RDV e imagem; eventos do log (votos computados, habilitações, biometria, horários, reinícios); conferência de hash e assinatura; modelo; certificado | ~500 mil por turno |
| `votos_por_minuto_{ano}_{turno}t.parquet` | Votos computados por minuto e município (do log) | — |
| `perfil_por_secao_2026` e `perfil_por_secao_2022` | Eleitorado por seção: total, % mulheres, escolaridade, faixas de idade | ~500 mil por ano |
| `resultados/` | Resultados de todas as investigações (JSON e CSV) | — |
| `veredito_2026.json`, `respostas_f3.json` | Hipóteses de fraude, sinal de cada teste, respostas | — |
| `capturas_divulgacao_ao_vivo/` | Capturas do Internet Archive do total nacional divulgado durante a apuração (2022 e 2026) | 39 |
| `MANIFESTO.csv` | SHA-256 de cada arquivo oficial usado | ~52 mil |
| `SHA256SUMS` | Hash de cada arquivo do pacote | — |

## O que dá para fazer só com o pacote
- Refazer os testes por seção (virada, caudas, agrupamentos, Benford, zeros) e os de comportamento (comparecimento, perfil).
- Conferir tabela × boletim × RDV pelo resumo por urna.
- Estudar a ordem de chegada dos boletins e a curva.
- Propor e testar hipóteses novas.

## O que exige os brutos
- Reler arquivos de urna (decodificar BU, RDV, log; verificar assinaturas).
- Seções do Sistema de Apuração de 2022 (o resumo por urna de 2022 não as lê).
- Qualquer coisa que dependa do log completo.

## Limitações conhecidas
- Em 2022, `ids_urna_log` e `urnas_com_voto_no_log` **não são válidos**: o campo do log não é o número da urna em parte dos arquivos.
- Em `urnas_2022_*`, 5 seções têm o boletim sem votos lidos (versão anterior do leitor). O boletim delas confere com a tabela (ver `fase3/resultados/fila_f3_semboletim.json`).
- Em 2022, `rdv_nulo` já inclui o nulo por suspensão (`rdv_tipo6`). Em 2026 é preciso somar.
- As seções do Sistema de Apuração não têm os campos de log da urna.

Para contribuir com uma hipótese ou análise, veja o `README.md` (seção "Como ajudar").
