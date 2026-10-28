# Evolução da pesquisa: versões, revisões e rodadas

O Urna Lab precisa permitir que qualquer pessoa veja o que o estudo concluiu hoje e também como chegou até aí, o que mudou e por quê. **A pesquisa se corrige sem reescrever o próprio passado.**

## O caminho

| Etapa | Versão | Situação | O que é |
|---|---|---|---|
| Estado inicial | **V1.0-rc1** | congelada em 28/10/2026 (tag `rodada-1`) | Levantamento da Fase 1: coleta, processamento, checks padrão, validação, 48 testes categorizados e a conclusão original. Snapshot preliminar; depois da revisão, aprovado como baseline V1.0 |
| Revisão | **R1** | respondida | Revisão independente (Codex). Ver [`revisoes/`](revisoes/) |
| Baseline aprovada | **V1.0** | **aprovada em 28/10/2026** (rodada 2, tag `v1.0`) | Critérios de [`revisoes/README.md`](revisoes/README.md) cumpridos e aprovação do responsável |
| Novas investigações | **Fase 2 → V1.1** | **concluída em 28/10/2026** (rodada 3, tag `v1.1`) | Perguntas registradas antes dos resultados em [`FASE2.md`](FASE2.md); respostas em [`RELATORIO_FASE2_COMPLETA.md`](RELATORIO_FASE2_COMPLETA.md); P18 a P21 na fila |
| Comparações | rc1 → V1.0 → V1.1 → atual | disponível | O que mudou em cada teste, com a causa |
| Estado atual | registro vivo | — | [`testes/registro.json`](testes/registro.json), com provas e mudanças ainda não congeladas |

No site, a página **Evolução da pesquisa** percorre essas etapas, e a gaveta de cada teste mostra a história científica dele.

## O que uma versão congela

`rodadas/rodada-N/` guarda:
- `registro.json`: o registro de testes;
- `resultados/`: os resultados pequenos;
- `CONCLUSAO.md`: a conclusão vigente;
- `resumo.json`: o placar e o SHA-256 de cada arquivo;
- `proveniencia.json`: commit, SHA-256 do manifesto de dados, ambiente, sementes e parâmetros.

Os dados de cerca de 405 GB ficam fora do git, verificáveis pelo manifesto. Cada versão tem uma tag no GitHub.

**Versão congelada não se edita.** O `proveniencia.json` da V1.0-rc1 foi acrescentado depois do congelamento, para completar a proveniência, e diz isso no próprio arquivo. Nenhum arquivo congelado foi alterado.

## A história de cada teste

Cada teste do registro tem um identificador persistente e estes campos:
- **`versoes`**: o estado em cada versão congelada (rótulo, commit, manifesto de dados, versão do método, situação, classe, evidência, interpretação, resultado e as mudanças daquela versão).
- **`evidencia`** e **`interpretacao`**: separadas a partir da revisão R1. Na rc1 estavam juntas no campo `resultado`.
- **`metodo_versao`**: sobe quando o método muda (exemplo: T01 v2 passou de soma nacional a comparação seção a seção).
- **`pre_especificacao`**: `anterior_ao_protocolo` para os testes rodados antes do protocolo (19h55 de 27/10), que não são pré-registrados; `protocolo_ou_emenda` para os demais.
- **`revisoes`**: os achados de revisão que tocam o teste.
- **`provas`**: cada contestação, com o alvo (evidência, método, interpretação, redação ou rastreabilidade) e o resultado: **resistiu**, **ajustado**, **caiu** ou **em andamento**.
- **`mudancas`**: o que mudou desde a última versão congelada, com a **causa**:

| Causa | Quer dizer |
|---|---|
| `dados` | mesmo código, dados novos ou atualizados |
| `codigo` | mesmos dados, implementação corrigida |
| `metodo` | o procedimento mudou |
| `nova_evidencia` | entrou informação que não existia |
| `interpretacao` | o número é o mesmo e a leitura mudou |
| `redacao` | o texto dizia mais (ou outra coisa) do que o teste sustenta |
| `rastreabilidade` | script, comando ou origem registrados |

Quando código e dados mudam juntos, a comparação diz isso e não atribui a mudança a uma causa só.

## Comandos

```bash
python scripts/rodada.py fechar 2 V1.0 "Baseline aprovada"     # congela a versão (recusa se já existir)
python scripts/rodada.py comparar 1 2                          # o que mudou em cada teste, com as causas
python scripts/rodada.py prova T02 "replicação" metodo "Refeito com nulo por UF" resistiu
```

Depois de congelar: atualizar `rodadas/linha_do_tempo.json`, regerar o site (`cd grafico/relatorio-app && npm run build`), publicar (`python scripts/publicar.py "V1.0"`) e criar a tag.
