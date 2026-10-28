# urna-lab

Estudo independente, imparcial e reproduzível da apuração presidencial brasileira de **2026** (1º e 2º turno), com **2022** como referência. Usa **somente dados oficiais do TSE** (dados abertos e arquivos gravados por cada urna).

> **Status: análise concluída em 28/10/2026** (conclusão em [`CONCLUSAO.md`](CONCLUSAO.md); site: https://urna-lab.web.app). Parte dos achados é exploratória e está marcada como tal; contribuições e contestações seguem abertas. A pergunta do estudo não é "houve fraude?", e sim: *quais padrões, anomalias e divergências existem nos dados, quais explicações científicas têm e quais hipóteses resistem a tentativas sérias de refutação.*

## O que tem aqui

| Arquivo | Para quê |
|---|---|
| [`CONCLUSAO.md`](CONCLUSAO.md) | **A conclusão** em três níveis: o que foi provado, o que a estatística mostra (com poder medido) e o que os dados públicos não alcançam |
| [`DIRETRIZ.md`](DIRETRIZ.md) | Princípios do estudo, classes de evidência A–G, ficha de resultado |
| [`PROTOCOLO.md`](PROTOCOLO.md) | Perguntas, modelos nulos, critérios fixados **antes** de rodar, emendas datadas |
| [`METODOLOGIA.md`](METODOLOGIA.md) | A matemática de cada teste |
| [`AUTOAUDITORIA.md`](AUTOAUDITORIA.md) | Mapa de ameaças, ameaças à validade, lacunas |
| [`CATALOGO.md`](CATALOGO.md) | Linha do tempo, resultados, erros encontrados e corrigidos, consumo |
| [`REFERENCIAS.md`](REFERENCIAS.md) | Bibliografia classificada |
| [`CONSUMO_IA.md`](CONSUMO_IA.md) | Quantos tokens e quanto custo de IA o estudo gastou, por modelo |
| [`testes/registro.json`](testes/registro.json) | Registro de todos os testes, legível por máquina |
| `analise/`, `scripts/`, `grafico/` | Código, páginas interativas e resultados pequenos |

## Reproduzir (inclusive com um agente de IA)

Os dados **não** estão no repositório (são ~250 GB); o repositório traz o caminho para baixá-los.

```bash
make ajuda            # lista tudo
make ambiente         # cria o ambiente Python (versões fixas em requirements.txt)
make dados-do-zero    # baixa e prepara os dados oficiais do TSE (horas, ~250 GB)
make verificar        # conferências de sanidade
```

Ou peça a um agente de IA de qualquer modelo: *"Leia `AGENTS.md` e reproduza o estudo"*. O [`AGENTS.md`](AGENTS.md) tem o manual completo (como baixar, como verificar, como acrescentar um teste), e [`PIPELINE.md`](PIPELINE.md) tem a ordem de execução e o dicionário de dados. As skills por domínio estão em `.agents/skills/`, e [`MAPA_SKILLS.md`](MAPA_SKILLS.md) diz qual usar para cada tarefa.

Tudo roda na máquina local: o projeto **não usa GitHub Actions nem Git LFS**.

## Licença e contribuições

Projeto **livre**: pode baixar, reproduzir, fazer fork, alterar e contradizer.

- **Código:** [MIT](LICENSE)
- **Documentação e resultados:** [CC BY 4.0](LICENSE-DOCS) (cite a fonte)
- Componentes e dados de terceiros: [THIRD_PARTY.md](THIRD_PARTY.md)

Para propor mudanças aqui: fork + pull request, validado por quem mantém. Detalhes em [CONTRIBUTING.md](CONTRIBUTING.md).
