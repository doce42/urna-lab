# Pré-registro: alegações da live de 4/11/2022 e do pedido do PL (T45 a T48)

Escrito em 28/10/2026, **antes** de qualquer cálculo de votos por modelo. Contexto e fontes: `docs/pesquisas/2026-10-28_live_cerimedo_2022.md`. Até aqui só foi olhada a cobertura (seções por modelo: 2022 2º turno UE2020 192.691, pré-2020 279.292, sem modelo 44).

Orçamento: 4 investigações, 1 execução principal + 1 validação cada, 1 correção + 1 repetição por falha operacional. Sem subagente. Dados: `analise/base_2022.parquet`, `analise/brutos/2022_{1t,2t}/urnas_*.parquet`, `analise/base.parquet` e `analise/brutos/{1t,2t}/` (2026). Script: `fase3/live_2022.py`. Saída: `fase3/resultados/live_2022.json`.

## T45 (A3): o log das urnas anteriores à UE2020 se liga ao BU e ao RDV?
- **Hipóteses.** H0: o campo de identificação do log traz o valor fixo 67305985 nos modelos UE2009 a UE2015 (bug documentado), mas log, BU e RDV da seção estão na mesma lista assinada pela chave da urna, e o certificado aponta a urna efetivada da tabela. H1: há seções em que essa ligação falha.
- **Medidas, por ano (2022, 2026), turno e modelo:** (1) seções com ID do log = 67305985; (2) seções com lista, log, BU e RDV com hash e assinatura válidos; (3) número do certificado = `NR_URNA_EFETIVADA`; (4) votos do BU = RDV = tabela (Lula, Bolsonaro/2º colocado, brancos, nulos).
- **O que muda a conclusão:** qualquer seção com 67305985 em que (2), (3) ou (4) falhe sem artefato já catalogado vira S4 (divergência objetiva) e é listada.
- **Limite:** consistência interna (mesma urna, mesma cadeia TSE); assinatura conferida até a AC emissora (P11).

## T46 (A4): "só com UE2020, Bolsonaro teria 51,05%"
- **Medidas:** (a) Bolsonaro / (Lula + Bolsonaro) no 2º turno de 2022, só seções UE2020. Reprodução aceita se dentro de ±0,05 p.p. de 51,05%. (b) A mesma conta no 1º turno (sobre os válidos e sobre Lula + Bolsonaro). (c) Contrafactual dentro do município: em cada município com UE2020 e pré-2020, cada seção pré-2020 recebe a proporção de Lula das UE2020 do mesmo município (média ponderada por válidos); municípios sem um dos grupos ficam com o observado. Resultado nacional e diferença em votos.
- **Leitura pré-fixada:** se (a) reproduz e (c) não inverte o resultado, o 51,05% é efeito de onde as UE2020 estão, não do modelo. Se (c) inverter, vira S3 e entra na fila.

## T47 (A1): urnas anteriores a 2020 dão mais votos a Lula?
- **Hipóteses.** H0 território: a diferença entre modelos some quando se compara dentro do mesmo lugar. H1 modelo: a diferença persiste dentro do local de votação.
- **(a) Conta da live:** proporção de Lula nos válidos do 1º turno, pré-2020 × UE2020, por UF e no total, em municípios pequenos. Sem população do IBGE no projeto, o porte usa o eleitorado apto (desvio declarado): 77 mil e 38,5 mil aptos (100 mil e 50 mil habitantes × 0,77, razão eleitorado/população de 2022).
- **(b) Teste principal:** dentro do município, molde do P5, mas no **nível** do voto: logit de Lula nos válidos menos a média do município; média por grupo (pré-2020, e cada modelo) com bootstrap de 200 sorteios de municípios (semente 5). Margem de equivalência ±0,02 logit (a do P5). Feito no 1º e no 2º turno; seções com validos ≥ 20.
- **(c) Sensibilidade:** o mesmo dentro do **local de votação** (só locais com os dois grupos).
- **Calibração (antes):** embaralhar o rótulo de modelo dentro do município, 200 vezes (semente 7). O teste é inadequado se o IC95 sair de ±0,02 em mais de 10% das permutações.
- **Poder:** fraude sintética de 1% dos válidos de Bolsonaro para Lula só nas pré-2020; detecção conta só no sentido correto (IC95 acima de 0 e fora da margem).
- **O que muda a conclusão:** (b) e (c) fora da margem, no mesmo sentido, nos dois turnos → S3 (anomalia sem causa), com votos estimados. Caso contrário, S1 (explicado pelo território), com a diferença bruta de (a) em votos.

## T48 (A5 + A6): software único e unanimidades
- **A5:** versões da aplicação no log (`sw_versoes`) e falhas de verificação (`sw_verif_falha`) por modelo e turno, 2022. H0: uma versão por turno em todos os modelos.
- **A6:** seções com 100% dos válidos para um candidato (Lula, Bolsonaro), por modelo e turno; duas definições: válidos ≥ 1 e válidos ≥ 20. Comparar a fração de unânimes de cada modelo com a sua fração de seções nos mesmos municípios. Descritivo; reconciliar as contagens publicadas (71 e 143 para Lula no 2º turno).
