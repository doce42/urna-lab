# Consumo de IA do estudo

Registro de quantos tokens e quanto custo de IA foram gastos para fazer este estudo, por modelo. Fonte: o comando `/usage` do Claude Code, copiado ao fim de cada sessão. Somar uma linha por sessão e atualizar os totais.

**Como registrar uma sessão nova:** rode `/usage`, copie a tabela "Usage by model" e some em "Sessões". Registre só os números da sessão (tokens, custo, tempo), não os limites da conta.

## Sessões

### Sessão 1: 27/10/2026 (construção do estudo, instantâneo às 23h30; a sessão continuava)
Tempo: 5 h 49 min de relógio, 2 h 19 min de tempo de API. Código: 4.560 linhas acrescentadas, 648 removidas.

| Modelo | Para quê | Entrada | Saída | Cache lido | Cache gravado | Custo (US$) |
|---|---|---|---|---|---|---|
| Claude Opus 5.5 | Condução do estudo, código, análises e documentação, até ~21h40 | 1,6 mil | 619,5 mil | 202,3 mi | 916,8 mil | 60,18 |
| Claude Sonnet 5.5 | Sessão principal depois de ~21h40 e 3 subagentes (relatório visual em 2 rodadas, leitor de 2022) | 25,5 mil | 222,6 mil | 74,3 mi | 1,2 mi | 14,18 |
| Claude Haiku 5.5 | Busca na web feita pelo próprio Claude Code (18 buscas; não foi escolha nossa) | 252,9 mil | 19,9 mil | 0 | 0 | 0,22 |
| **Total da sessão** | | **280,0 mil** | **862,0 mil** | **276,6 mi** | **2,1 mi** | **74,58** |

**Total de tokens processados na sessão: ≈ 279,9 milhões**, dos quais:
- ≈ **3,3 milhões** são tokens "novos" (entrada, saída e gravação de cache);
- ≈ **276,6 milhões** são leituras de cache, isto é, o mesmo contexto relido a cada chamada;
- **862 mil** são tokens que os modelos efetivamente escreveram (saída).

Os tokens dos 3 subagentes (≈ 278 mil no total: 158,9 mil no relatório visual em duas rodadas e 119,4 mil no leitor de 2022) estão dentro da linha do Sonnet.

## Tokens de contexto (o histórico da conversa relido a cada chamada)

Na tabela acima, "Cache lido" e "Cache gravado" são os tokens de contexto: tudo o que já estava na conversa (mensagens, arquivos lidos, resultados de comandos) e que o modelo relê a cada nova chamada. O "Cache gravado" é o contexto novo que entrou, e o "Cache lido" é o mesmo contexto relido muitas vezes.

| Modelo | Contexto gravado (novo) | Contexto relido (cache lido) | Contexto total | Parte do total do modelo |
|---|---|---|---|---|
| Claude Opus 5.5 | 916,8 mil | 202,3 mi | ≈ 203,2 mi | 99,7% |
| Claude Sonnet 5.5 | 1,2 mi | 74,3 mi | ≈ 75,5 mi | 99,7% |
| Claude Haiku 5.5 | 0 | 0 | 0 | 0% |
| **Total** | **≈ 2,1 mi** | **276,6 mi** | **≈ 278,7 mi** | **99,6% dos 279,9 mi** |

Tokens que não são contexto: entrada nova ≈ 280 mil e saída (escrita pelos modelos) ≈ 862 mil, somando ≈ 1,1 mi.
Esta sessão passou por compactação do contexto (resumo automático) quando a janela encheu; os números acima já incluem isso.

## Totais acumulados do estudo

| Modelo | Tokens processados | Custo (US$) |
|---|---|---|
| Claude Opus 5.5 | ≈ 203,8 mi | 60,18 |
| Claude Sonnet 5.5 | ≈ 75,7 mi | 14,18 |
| Claude Haiku 5.5 | ≈ 0,27 mi | 0,22 |
| **Total** | **≈ 279,9 mi** | **74,58** |

**Continuação da sessão 1 (28/10/2026, madrugada), consumo ainda não medido:** reprocessamento e correções, site React com a identidade visual, rodada 1, revisão R1 respondida. Modelos: Sonnet 5.5 na sessão principal até ≈ 03h00 e Opus 5.5 depois. Subagentes: Fable 5.1 (site, ≈ 518 mil tokens) e Opus 5.5 (identidade, ≈ 113 mil tokens). A revisão R1 foi feita pelo Codex, de outro fornecedor, em sessão separada, e o consumo dela não está aqui. **Para completar:** colar o `/usage` final desta sessão e somar na tabela.

Marcos que ainda não entraram (somar quando a sessão terminar ou em sessões novas): reprocessamento completo após a correção do log duplicado, conferência final, relatório, PDF e conclusão.

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
- O custo dominante foi **reler o contexto muito longo** a cada chamada (99% da entrada veio de cache), e não escrever código.
- Os **subagentes de contexto pequeno** saíram bem mais baratos por tarefa do que a sessão principal.
- A **computação pesada não usa IA**: processamento das urnas, testes estatísticos, mapas e relatórios rodam em scripts na máquina local (ver `Makefile` e `scripts/`). A IA só conduziu, escreveu código e documentou.
- Para a próxima sessão: usar modelo mais barato para execução desde o início, abrir sessão nova (`/clear`) a cada mudança de tarefa e retomar por `AGENTS.md`, `CATALOGO.md` e `testes/registro.json`.
