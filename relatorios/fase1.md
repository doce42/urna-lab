# Levantamento inicial

**Versão:** V1.0-rc1 · **Situação:** concluída · **Início:** 2026-10-27 · **Fim:** 2026-10-28

## Resumo

Primeira rodada grossa: coleta de todos os dados oficiais, processamento das urnas, verificações padrão da literatura, validação criptográfica e de totais, e categorização de cada teste com classe de evidência. Congelada como snapshot preliminar V1.0-rc1, que depois da revisão R1 foi aprovada como baseline V1.0.

## O que foi feito

1. **Coleta e proveniência.** 51.846 arquivos oficiais do TSE (≈ 405 GB) com SHA-256 no manifesto: tabelas de resultado, Boletim de Urna na Web, perfil do eleitorado e os arquivos de cada urna de 2026 e 2022.
2. **Análise bruta e checks padrão.** Bateria forense da literatura (dígitos, impressão digital de Klimek, percentuais inteiros, fraude incremental), curva da apuração minuto a minuto e comparação com 2022.
3. **Validação de dados.** Boletim × votação por seção (T01; na rc1 só a soma nacional, refeito seção a seção na R1), soma das urnas = total oficial (T32, 638/638), assinaturas e hashes (T14, T16), recontagem pelo RDV (T17).
4. **Processamento das urnas.** ≈ 499 mil urnas por turno, 4 combinações (2026 e 2022, 1º e 2º turno): log eleitor a eleitor, boletim digital, RDV, imagem do boletim e assinatura. Dois erros de leitura achados e corrigidos.
5. **Categorização dos testes.** 48 testes no registro, cada um com hipótese nula, pressupostos, limitações, natureza (confirmatório ou exploratório) e classe de evidência A–G; poder medido com fraude simulada.
6. **Snapshot preliminar V1.0-rc1.** Retrato congelado (tag rodada-1) com a conclusão original; a baseline aprovada é a V1.0 (rodada 2).

## Onde está o detalhe

- [`RODADAS.md`](../RODADAS.md)
- [`revisoes/README.md`](../revisoes/README.md)
- [`CONCLUSAO.md`](../CONCLUSAO.md)

Nada aqui afirma nem nega fraude além do que os números sustentam.
