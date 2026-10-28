# Rodadas e linha do tempo

O estudo avança em **rodadas**. Cada rodada termina com um **retrato congelado** de todos os testes e resultados, para que o que temos hoje possa ser comparado com o que teremos amanhã, e para que cada teste possa ser posto à prova sem apagar o que ele dizia antes.

## Fases

| Fase | Rodada | Situação | O que é |
|---|---|---|---|
| F1. Levantamento inicial | 1 | **concluída em 28/10/2026** | Coleta e proveniência, análise bruta e checks padrão, validação de dados, processamento das urnas, categorização dos 48 testes e conclusão da rodada |
| F2. Double check da metodologia | 2 | próxima | Revisar método a método, pressupostos e modelos nulos, código contra método e reprodução |
| F3. Perguntas e provas | 3 em diante | planejada | Várias fases de perguntas que põem à prova o levantamento inicial; cada teste é contestado e o resultado fica registrado nele |

Fases, etapas e marcos ficam em [`rodadas/linha_do_tempo.json`](rodadas/linha_do_tempo.json). No site, a página **Linha do tempo** mostra tudo, e a gaveta de cada teste mostra o histórico dele rodada a rodada.

## O que uma rodada congela

`rodadas/rodada-N/` guarda:
- `registro.json`: o registro completo de testes naquele momento;
- `resultados/`: cópia de todos os resultados pequenos (`analise/resultado_*.json`);
- `CONCLUSAO.md`: a conclusão vigente na rodada;
- `resumo.json`: placar por classe, situação e natureza, e o SHA-256 de cada arquivo congelado.

No GitHub, cada rodada fechada tem uma **tag** (`rodada-1`, `rodada-2`…). Ela aponta para o código e os documentos exatamente como estavam.

**Rodadas fechadas não se reescrevem.** Um erro achado depois entra na rodada seguinte, com a explicação, e o retrato antigo continua lá para comparação.

## Histórico e provas de cada teste

Cada teste do [`registro`](testes/registro.json) ganhou dois campos:
- **`historico`**: uma entrada por rodada fechada, com situação, classe de evidência, natureza e resultado naquele momento. Comparar duas entradas mostra o que mudou e quando.
- **`provas`**: cada vez que o teste é posto à prova, registra-se a data, a rodada, o tipo e o resultado. O tipo pode ser revisão de método, replicação, dado independente, sensibilidade ou contestação externa. O resultado pode ser **resistiu**, **caiu**, **ajustado** ou **em andamento**.

Um teste que cai não é apagado. Ele muda de classe ou de situação na rodada seguinte, e a prova que o derrubou fica junto dele.

## Comandos

```bash
python scripts/rodada.py fechar 2 "Double check da metodologia"   # congela a rodada 2 (recusa se já existir)
python scripts/rodada.py comparar 1 2                             # lista os testes que mudaram entre as rodadas
python scripts/rodada.py prova T02 "replicação" "Refeito com nulo de Student por UF" resistiu
```

Depois de fechar uma rodada: atualizar `rodadas/linha_do_tempo.json` (fase concluída e marco), regerar o site (`cd grafico/relatorio-app && npm run build`), publicar (`python scripts/publicar.py "Rodada N"`) e criar a tag `rodada-N` no repositório público.
