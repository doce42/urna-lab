# Consumo de IA do estudo

Registro de quantos tokens e quanto custo de IA foram gastos para fazer este estudo, por modelo. Fonte: o comando `/usage` do Claude Code, copiado ao fim de cada sessão. Somar uma linha por sessão e atualizar os totais.

**Como registrar uma sessão nova:** rode `/usage`, copie a tabela "Usage by model" e some em "Sessões". Registre só os números da sessão (tokens, custo, tempo), não os limites da conta.

## Sessões

### Sessão 1: 27 e 28/10/2026 (rodada 1, site, revisão R1), medição final
Medida pelo `/usage` ao fim da sessão. Tempo: **9 h 47 min de relógio**, 4 h 3 min de tempo de API. Código: 9.257 linhas acrescentadas e 923 removidas. Houve uma compactação automática do contexto no meio da sessão.

| Modelo | Para quê | Entrada | Saída | Cache lido | Cache gravado | Custo (US$) |
|---|---|---|---|---|---|---|
| Claude Opus 5.5 | Sessão principal até ≈ 21h40 de 27/10 e depois de ≈ 03h00 de 28/10 (rodada 1, revisão R1, migração do registro); subagente de identidade visual | 12,7 mil | 824,2 mil | 250,7 mi | 1,5 mi | 78,48 |
| Claude Sonnet 5.5 | Sessão principal de ≈ 21h40 a 03h00 (reprocessamento, correções de leitura, publicação); subagentes do relatório visual e do leitor de 2022 | 29,3 mil | 318,4 mil | 97,0 mi | 1,6 mi | 18,92 |
| Claude Fable 5.1 | Subagente que construiu o site (React, páginas, gráficos, tela de carregamento) | 271,7 mil | 287,1 mil | 40,7 mi | 1,0 mi | 40,17 |
| Claude Haiku 5.5 | Buscas na web do próprio Claude Code (20 buscas) | 280,8 mil | 22,0 mil | 0 | 0 | 0,24 |
| **Total da sessão** | | **594,5 mil** | **1,45 mi** | **388,4 mi** | **4,1 mi** | **137,81** |

**Tokens processados: ≈ 394,6 milhões.** Por modelo: Opus ≈ 253,0 mi, Sonnet ≈ 99,0 mi, Fable ≈ 42,3 mi e Haiku ≈ 0,3 mi.

Fora desta conta: a revisão independente R1 foi feita pelo Codex, de outro fornecedor, em sessão separada, e o consumo dela não foi medido aqui. O instantâneo parcial das 23h30 de 27/10 (US$ 74,58) está incluído nestes totais.

## Tokens de contexto (o histórico da conversa relido a cada chamada)

"Cache lido" e "cache gravado" são os tokens de contexto: tudo o que já estava na conversa (mensagens, arquivos lidos, resultados de comandos) e que o modelo relê a cada nova chamada.

| Modelo | Contexto gravado (novo) | Contexto relido | Contexto total |
|---|---|---|---|
| Claude Opus 5.5 | 1,5 mi | 250,7 mi | ≈ 252,2 mi |
| Claude Sonnet 5.5 | 1,6 mi | 97,0 mi | ≈ 98,6 mi |
| Claude Fable 5.1 | 1,0 mi | 40,7 mi | ≈ 41,7 mi |
| Claude Haiku 5.5 | 0 | 0 | 0 |
| **Total** | **4,1 mi** | **388,4 mi** | **≈ 392,5 mi (99,5% de tudo)** |

Os tokens que não são contexto somam ≈ 2,0 mi: 594,5 mil de entrada nova e 1,45 mi escritos pelos modelos. Segundo o próprio `/usage`, 99% da entrada da sessão principal veio de cache, em 734 chamadas.

## Totais acumulados do estudo

| Modelo | Tokens processados | Custo (US$) |
|---|---|---|
| Claude Opus 5.5 | ≈ 253,0 mi | 78,48 |
| Claude Sonnet 5.5 | ≈ 99,0 mi | 18,92 |
| Claude Fable 5.1 | ≈ 42,3 mi | 40,17 |
| Claude Haiku 5.5 | ≈ 0,3 mi | 0,24 |
| **Total** | **≈ 394,6 mi** | **137,81** |

**Como registrar a próxima sessão:** rode `/usage`, copie "Usage by model" e acrescente uma seção "Sessão 2" acima, somando nesta tabela. Registre só tokens, custo e tempo. Os percentuais de limite da conta ficam de fora, porque este arquivo é público.


## Consumo de máquina, rede, disco e tempo (o que a IA não gastou)

Medido por `scripts/monitorar.sh` (a cada 30 s, `dados/listas/recursos.csv`, 565 amostras de 19h11 a 23h56 de 27/10/2026) e por contagem dos arquivos. O cálculo pesado roda todo na máquina local do autor.

**Máquina:** 16 núcleos, 23 GB de RAM, SSD de 1 TB (`<DISCO_GRANDE>`); processos com `nice 10` e `ionice` ocioso.

| Item | Valor |
|---|---|
| Carga média (1 min) na janela medida | 12,4 de 16 (pico 32,1) |
| RAM usada | média 10,4 GB, pico 18,2 GB de 23 GB |
| Internet recebida na janela medida | ≈ 399 GB (73,4 → 472,6 GB no contador da placa de rede; inclui outros usos do computador) |
| Banda máxima observada | ≈ 64 MB/s (≈ 510 Mbit/s) |
| Arquivos oficiais baixados (manifesto SHA-256) | 51.846 arquivos, **404,9 GB** |
| Dados no disco (`dados/`) | ≈ 380 GB: 2026 brutos 1º turno 89 GB, 2º turno 116 GB (pacotes) + 5,9 GB (SP urna a urna); 2022 brutos 157 GB; tabelas e perfis ≈ 12 GB |
| Resultados derivados (`analise/`) | ≈ 333 MB, dos quais 145 MB de saídas por urna e 73 MB de bases em parquet |
| Repositório público (sem dados) | ≈ 499 MB na pasta; publicado bem menos, com limite de 20 MB por arquivo e 120 MB no total |
| Processamento das urnas | ≈ 499 mil urnas por turno, 4 combinações (2026 e 2022, 1º e 2º turno); reprocessamento completo em andamento desde 23h27 |
| Tempo total do estudo | início às 18h03 de 27/10; sessão de IA de 5 h 49 min; downloads grandes ≈ 1 h cada na banda disponível |

**Reprocessamento completo (28/10/2026, `scripts/refazer_tudo.sh`)**, 15 processos em paralelo, ~2 h 15 min no total: 2026 1º turno 35 min, 2026 2º turno 37 min, 2022 1º turno 30 min, 2022 2º turno ≈ 31 min, análises ≈ 2 min. Correção do leitor do bu.dat: 2º turno (7 UFs) 16 min e 1º turno (7 UFs) 17 min. Volume lido nesse reprocessamento: ≈ 400 GB de pacotes oficiais, 4 × ≈ 499 mil urnas. Site publicado: `dist` de 5,0 MB (inclui o PDF de 2,5 MB, 85 páginas); `relatorio_dados.json` caiu de 118 MB para 225 KB depois de remover uma lista redundante.

## Leitura do consumo e lições
- O custo dominante foi **reler o contexto muito longo** a cada chamada (99,5% dos tokens são contexto relido), e não escrever código. Uma sessão de quase 10 horas sem recomeçar acumula isso.
- Os **subagentes de contexto pequeno** saíram bem mais baratos por tarefa do que a sessão principal. O do site (Fable) foi a maior tarefa delegada (US$ 40), e valeu pelo tamanho do trabalho.
- A **computação pesada não usa IA**: processamento das urnas, testes estatísticos, mapas e relatórios rodam em scripts na máquina local (ver `Makefile` e `scripts/`). A IA só conduziu, escreveu código e documentou.
- Para a próxima sessão: usar modelo mais barato para execução desde o início, abrir sessão nova (`/clear`) a cada mudança de tarefa e retomar por `AGENTS.md`, `CATALOGO.md` e `testes/registro.json`.
