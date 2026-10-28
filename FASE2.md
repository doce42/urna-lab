# Fase 2: investigação aprofundada

**Aberta em 28/10/2026; baseline V1.0 aprovada no mesmo dia. Resultados da primeira sessão limitada em `fase2/sessao_limitada_2026-10-28/` e na tabela abaixo.** Esta lista é registrada **antes** de rodar qualquer análise nova. É o que torna as perguntas confirmatórias e as separa das exploratórias. Cada pergunta diz qual hipótese concorrente ela distingue, que afirmação do estudo pode mudar e qual é o menor conjunto de dados capaz de decidir. Esse é o critério proposto na revisão R1.

A Fase 2 começou formalmente com a aprovação da baseline V1.0 (28/10/2026; ver [`revisoes/README.md`](revisoes/README.md)).

## Antes da V1.0 (fecham a R1)

| Tarefa | Achado | Situação |
|---|---|---|
| Varrer todas as chaves Ed521 reais com o verificador endurecido | R1-02 | concluída: 499.176 e 499.178 listas válidas, nenhuma chave degenerada |

## Perguntas

| Id | Pergunta | Distingue | Afirmação que pode mudar | Natureza | Menor teste que decide | Origem |
|---|---|---|---|---|---|---|
| P1 | Quanto das estimativas de fluxo entre turnos depende da hipótese de taxas homogêneas por UF? | fluxo estimado real × artefato do modelo | "abstencionistas 4:1 para Lula" (C06) | confirmatória | geradores sintéticos pequenos com taxas heterogêneas conhecidas; checar se o C06 recupera a verdade | R1-06 / P1 |
| P2 | Qual é a sensibilidade da regra completa de conclusão sob mundos legítimos e intervenções especificadas, com réplicas e nos dois sentidos? | "os testes veriam X" × "não veriam" | o nível 2 da conclusão (poder) | confirmatória | poucos mecanismos prioritários, réplicas com erro Monte Carlo, decisão conjunta e não teste a teste | R1-04, R1-09 / P2 |
| P3 | As inconsistências aparentes dependem do canal e da versão de publicação (pacote × site de resultados × BU na Web)? | erro de publicação × erro de registro | T36, T35, D1 | exploratória → confirmatória | reconciliação por chave e arquivo em amostra, com o DataUrnas como implementação independente | R1-20 / P3 |
| P4 | A curva pública pode ser reconstruída a partir dos BUs recebidos, dentro da latência esperada? | curva divulgada = chegada dos boletins × processamento próprio da divulgação | T10, T11 | exploratória | inventário de snapshots externos realmente disponíveis, sem iniciar coletor | R1-10 / P4 |
| P5 | As associações por modelo de urna sobrevivem a comparações com suporte territorial comum? | efeito do modelo × efeito do território | T20 | confirmatória | comparação dentro de municípios que têm os dois modelos | P5 |
| P6 | O que uma coleta externa de BU (boletins impressos de terceiros) permitiria validar sobre publicação e impacto agregado? | publicado = impresso na seção × divergência | T15, T32 | exploratória (novo escopo: dado não oficial) | inventário do que existe e desenho amostral, antes de coletar | P6 |
| P7 | A urna trocada entre turnos vota equivalentemente às outras, dentro de uma margem fixada antes? | equivalência × diferença pequena não detectada | T04 | confirmatória | teste de equivalência (TOST) com margem pré-definida | R1-07 |
| P8 | O intervalo do T03 continua excluindo efeito relevante quando se considera a dependência entre seções do município? | efeito desprezível × incerteza subestimada | T03 | confirmatória | bootstrap por município | R1-07 |
| P9 | Os locais de votação do E02 continuam significativos com p-valores calibrados para correlação intralocal, e 2022 × 2026 com o mesmo modelo? | agrupamento legítimo × divergência | E02, E03 | confirmatória | estimar ρ intralocal; mesmo modelo nos dois anos; Moran's I com vizinhança | R1-08 |
| P10 | A taxa sem biometria do T28 continua sinalizando as 13 urnas do 1º turno quando entra a incerteza da taxa e a composição por horário? | rajada × variação legítima | T28 | confirmatória | binomial com taxa incerta (beta-binomial) e controle por horário | R1-11 |
| P11 | Os certificados das urnas se ligam a uma âncora do TSE obtida por canal confiável? | chave autêntica × apenas coerente | T14, T16 | confirmatória | certificados intermediários públicos (DataUrnas, documentação oficial) e validação do caminho | R1-01 |
| P12 | Qual é a causa da diferença de eleitorado do exterior (−495 e −525) no T32? | cadastro × publicação | T32 | exploratória | tabelas oficiais de eleitorado do exterior por país | R1-16 |
| P13 | Incorporar o C06b (limites de troca direta) a um script reproduzível | rastreabilidade | C06b | — | script e comparação com o valor registrado | R1-17 |

## Regras da Fase 2

1. Toda pergunta nova entra nesta tabela **antes** de ser rodada, com a natureza declarada. Se nascer de um resultado, é exploratória.
2. O resultado vai para o teste correspondente: em `provas`, quando contesta um teste existente, ou como teste novo no registro. Nunca reescreve a versão anterior.
3. Toda mudança de número informa a causa: mesmos dados com código diferente, dados novos com o mesmo código, ou os dois. Quando os dois mudam, a mudança não é atribuída a uma causa só sem um teste adicional.
4. Uma detecção em dados reais não se chama falso positivo: o estado verdadeiro desses dados é desconhecido.

## Primeira sessão (28/10/2026)
Pré-registro, scripts e resultados em `fase2/sessao_limitada_2026-10-28/`; relatório em [`RELATORIO_SESSAO_LIMITADA.md`](RELATORIO_SESSAO_LIMITADA.md).
- **P1 respondida (confirmatória):** com heterogeneidade contextual a razão Abs→Lula:Abs→Adv do C06 varia de 1,7 a 11,8 contra 3 a 4 verdadeiro; a ordem de 2026 e o contraste com 2022 resistem. Resultado vai para `provas` do C06 (ajustado).
- **P2 adiada** (fila): a regra do T13 conta o T1 e o T3 só a favor de Lula; medir nos dois sentidos.
- **Novas, exploratórias, não executadas:** P14 causa da assimetria de cauda do T02 em 2022; P15 C06 com covariáveis e limites por UF; P16 comparador do RDV (tipo 6) e amostra maior; P17 teste formal de assimetria da cauda.
