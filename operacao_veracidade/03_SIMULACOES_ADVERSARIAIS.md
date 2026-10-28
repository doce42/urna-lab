# 03. Simulações adversariais: o que a bateria estatística consegue ver

Scripts: `scripts/sim_adversarial.py` (grade principal), `scripts/sim_fabricacao_v2.py` (fabricante de estrutura completa), `scripts/identificabilidade.py` (T62), `scripts/gera_tabelas_sim.py`. Saídas: `resultados/sim_<ano>*.{parquet,csv,json}`, `resultados/identificabilidade.json`. Protocolo e emendas: `PROTOCOLO_PRE_EXECUCAO.md`.

**Tudo aqui é sintético.** Nada foi feito com arquivo real: a base de seções do 2º turno de cada ano foi copiada em memória e alterada. Nenhum resultado desta seção é voto alterado encontrado nem prova de que algo foi alterado.

## 1. O que foi medido (e a limitação central)
- **Referência:** a base real de cada ano (497.830 seções válidas em 2026; 470.964 em 2022). Ela é a referência, **não** uma verdade conhecida sem fraude. Os limiares de alarme vêm do bootstrap por município (B = 200) da própria base real.
- **Consequência que precisa ficar clara:** o experimento mede a capacidade de ver uma alteração **adicional** sobre a base observada. **Ele não consegue dizer se a base observada já contém alguma alteração**, porque uma alteração já presente é absorvida pelo limiar. Isso é inerente ao desenho: não existe eleição com verdade conhecida.
- **Detectores (fixados no protocolo):** D1 cauda de resíduos por seção; D2 efeito de local e de zona; D3 desvio de município contra UF, 1º turno e tamanho; D4 comparecimento; D5 dígito final; D6 e D7 (emendas 1 e 2) só para o experimento de fabricação. Poder = alarme em D1 a D4 no sentido correto (no enchimento, também D4, comparecimento). Alarme no sentido oposto e D5 são contados à parte.
- **Mecanismos (15), em ambos os sentidos, 7 magnitudes (25 mil a 2,22 milhões de votos movidos), 20 réplicas nos aleatórios, 1 nos determinísticos:** seções dispersas; poucas seções com alteração grande; locais, zonas e municípios inteiros; os cinco grandes juntos; UFs; macrorregião Nordeste; redutos do alvo e do oponente; deslocamento uniforme em fatia de voto e **em logit**; lote tardio de recebimento; enchimento; conversão de brancos e nulos.
- **Magnitude:** votos movidos. Numa troca, a margem muda 2X; inverter 2026 pede X = 2,22 mi; enchimento e conversão mudam a margem em X.
- **Falso alarme:** zero em 30 simulações não é taxa zero. Aqui o falso alarme é medido em bootstrap independente (200) com intervalo de Clopper-Pearson, e o da **união** dos detectores fica bem acima dos 2,5% de cada um.

## 2. Resultados

### Poder por mecanismo e magnitude, 2026 (% de réplicas com alarme na direção correta; Flávio→Lula / Lula→Flávio)

| Mecanismo | 25 mil | 50 mil | 100 mil | 250 mil | 500 mil | 1.00 mi | 2.22 mi | menor X com ≥80% (F→L / L→F) |
|---|---|---|---|---|---|---|---|---|
| seções dispersas (3% dos válidos em cada) | 35/0 | 100/80 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 50 mil / 50 mil |
| poucas seções, alteração grande (40%) | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 25 mil / 25 mil |
| locais de votação inteiros (10%) | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 25 mil / 25 mil |
| zonas inteiras (10%) | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 25 mil / 25 mil |
| municípios inteiros, sem os 5 grandes (10%) | 65/85 | 95/95 | 95/100 | 100/100 | 100/100 | 100/100 | 100/100 | 50 mil / 25 mil |
| os 5 grandes municípios juntos | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 100/0 | 100/100 | 1.00 mi / 2.22 mi |
| UFs inteiras (10%) | 0/0 | 0/0 | 5/0 | 40/40 | 55/40 | 80/75 | 100/90 | 1.00 mi / 2.22 mi |
| macrorregião Nordeste | 0/0 | 0/0 | 0/0 | 0/0 | 100/0 | 100/0 | 100/100 | 500 mil / 2.22 mi |
| redutos do alvo (quintil) | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 25 mil / 25 mil |
| redutos do oponente (quintil) | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 25 mil / 25 mil |
| uniforme em fatia de voto (proporcional) | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 100/0 | 2.22 mi / nunca |
| uniforme em logit (H9) | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | nunca / nunca |
| lote tardio de recebimento (40% das seções) | 0/0 | 0/0 | 0/0 | 0/0 | 100/0 | 100/100 | 100/100 | 500 mil / 1.00 mi |
| enchimento (abstenção → finalista) | 0/0 | 0/0 | 0/0 | 100/95 | 100/100 | 100/100 | 100/100 | 250 mil / 250 mil |
| conversão de brancos e nulos | 0/0 | 0/0 | 0/0 | 15/35 | 90/100 | 100/100 | 90/100 | 500 mil / 500 mil |

**Falso alarme (segunda amostra bootstrap por município, B = 200), 2026:** união dos detectores na direção pró-Lula 10.0% (IC 95% Clopper-Pearson 6.2–15.0), na direção pró-Flávio 4.0% (1.7–7.7), qualquer lado 11.5% (7.4–16.8). Cada detector isolado tem 2,5% por construção; a união de vários fica acima disso.

**D5 (dígito final), 2026:** alarme em 2.09% das 2870 execuções (qualquer mecanismo e magnitude). Poder na prática igual ao ruído.

**Sensibilidade do limiar do D1 (z de 3, 4 e 5), 2026:**

| Mecanismo | X | Poder (D1 a D4, D1 em 4) | D1 em 3 | D1 em 5 |
|---|---|---|---|---|
| seções dispersas (3% dos válidos em cada) | 50 mil | 0.90 | 1.00 | 0.02 |
| seções dispersas (3% dos válidos em cada) | 100 mil | 1.00 | 1.00 | 0.42 |
| seções dispersas (3% dos válidos em cada) | 250 mil | 1.00 | 1.00 | 0.50 |
| poucas seções, alteração grande (40%) | 50 mil | 1.00 | 1.00 | 1.00 |
| poucas seções, alteração grande (40%) | 100 mil | 1.00 | 1.00 | 1.00 |
| poucas seções, alteração grande (40%) | 250 mil | 1.00 | 1.00 | 1.00 |

**Fabricação coerente de um 2º turno inteiro (B2), 2026, 20 réplicas:**

| Fabricante | Alarme D1–D4 | D5 | D6 (escala) | D7 (estrutura) | escala z / local / zona (relativas à base) |
|---|---|---|---|---|---|
| calibrada (v1) | 0% | 0% | 0% | 100% | 0.99 / 0.75 / 0.27 |
| calibrada_estrutura (v1) | 100% | 0% | 0% | 100% | 0.91 / 0.95 / 2.05 |
| ingenua (v1) | 100% | 0% | 100% | 100% | 1.37 / 1.03 / 0.38 |
| calibrada_estrutura (v2, efeitos centrados, total municipal corrigido) | 0% | 0% | 0% | 5% | 0.98 / 0.97 / 0.84 |

Detectores que dispararam na v2 (2026): nenhum. Margem fabricada 4.393.174 contra margem real 4.401.157.

### Poder por mecanismo e magnitude, 2022 (% de réplicas com alarme na direção correta; Flávio→Lula / Lula→Flávio)

| Mecanismo | 25 mil | 50 mil | 100 mil | 250 mil | 500 mil | 1.00 mi | 2.22 mi | menor X com ≥80% (F→L / L→F) |
|---|---|---|---|---|---|---|---|---|
| seções dispersas (3% dos válidos em cada) | 0/0 | 0/85 | 0/100 | 70/100 | 100/100 | 100/100 | 100/100 | 500 mil / 50 mil |
| poucas seções, alteração grande (40%) | 15/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 50 mil / 25 mil |
| locais de votação inteiros (10%) | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 25 mil / 25 mil |
| zonas inteiras (10%) | 75/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 50 mil / 25 mil |
| municípios inteiros, sem os 5 grandes (10%) | 85/80 | 100/85 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 25 mil / 25 mil |
| os 5 grandes municípios juntos | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 100/100 | 2.22 mi / 2.22 mi |
| UFs inteiras (10%) | 0/0 | 10/0 | 30/0 | 25/5 | 60/30 | 90/70 | 85/70 | 1.00 mi / nunca |
| macrorregião Nordeste | 0/0 | 0/0 | 0/0 | 0/0 | 100/0 | 100/0 | 100/100 | 500 mil / 2.22 mi |
| redutos do alvo (quintil) | 95/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 25 mil / 25 mil |
| redutos do oponente (quintil) | 0/100 | 85/100 | 100/100 | 100/100 | 100/100 | 100/100 | 100/100 | 50 mil / 25 mil |
| uniforme em fatia de voto (proporcional) | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 100/0 | 100/0 | 1.00 mi / nunca |
| uniforme em logit (H9) | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | nunca / nunca |
| lote tardio de recebimento (40% das seções) | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 100/100 | 100/100 | 1.00 mi / 1.00 mi |
| enchimento (abstenção → finalista) | 0/0 | 0/0 | 0/0 | 100/100 | 100/100 | 100/100 | 100/100 | 250 mil / 250 mil |
| conversão de brancos e nulos | 0/0 | 0/0 | 0/0 | 0/45 | 0/100 | 0/100 | 0/100 | nunca / 500 mil |

**Falso alarme (segunda amostra bootstrap por município, B = 200), 2022:** união dos detectores na direção pró-Lula 11.5% (IC 95% Clopper-Pearson 7.4–16.8), na direção pró-Flávio 9.5% (5.8–14.4), qualquer lado 14.5% (9.9–20.2). Cada detector isolado tem 2,5% por construção; a união de vários fica acima disso.

**D5 (dígito final), 2022:** alarme em 2.68% das 2870 execuções (qualquer mecanismo e magnitude). Poder na prática igual ao ruído.

**Sensibilidade do limiar do D1 (z de 3, 4 e 5), 2022:**

| Mecanismo | X | Poder (D1 a D4, D1 em 4) | D1 em 3 | D1 em 5 |
|---|---|---|---|---|
| seções dispersas (3% dos válidos em cada) | 50 mil | 0.42 | 0.00 | 0.00 |
| seções dispersas (3% dos válidos em cada) | 100 mil | 0.50 | 0.50 | 0.20 |
| seções dispersas (3% dos válidos em cada) | 250 mil | 0.85 | 1.00 | 0.45 |
| poucas seções, alteração grande (40%) | 50 mil | 1.00 | 0.28 | 1.00 |
| poucas seções, alteração grande (40%) | 100 mil | 1.00 | 0.50 | 1.00 |
| poucas seções, alteração grande (40%) | 250 mil | 1.00 | 1.00 | 1.00 |

**Fabricação coerente de um 2º turno inteiro (B2), 2022, 20 réplicas:**

| Fabricante | Alarme D1–D4 | D5 | D6 (escala) | D7 (estrutura) | escala z / local / zona (relativas à base) |
|---|---|---|---|---|---|
| calibrada (v1) | 10% | 0% | 0% | 100% | 0.99 / 0.59 / 0.15 |
| calibrada_estrutura (v1) | 100% | 0% | 0% | 0% | 0.90 / 1.08 / 1.06 |
| ingenua (v1) | 100% | 0% | 100% | 100% | 1.35 / 0.81 / 0.20 |
| calibrada_estrutura (v2, efeitos centrados, total municipal corrigido) | 100% | 0% | 0% | 0% | 0.90 / 1.07 / 1.03 |

Detectores que dispararam na v2 (2022): d2z_pos 100%. Margem fabricada 2.126.200 contra margem real 2.131.560.


## 3. Leitura honesta dos resultados
1. **O que a bateria vê bem (poder ≥ 80% a partir de 25 mil a 50 mil votos):** alterações em seções dispersas ou poucas seções grandes, em locais, zonas e municípios inteiros (fora os cinco maiores) e em redutos de um dos lados. Isso sustenta a parte do veredito que diz que alterações desse tipo **de dezenas de milhares de votos** deixariam sinal.
2. **O que ela vê só em escala grande ou nunca (esta é a parte que o veredito não dizia):** UFs inteiras (a partir de 1 mi em 2026 e 2022, F→L; 2,22 mi ou nunca, L→F), os cinco grandes municípios juntos (1 a 2,22 mi), a macrorregião Nordeste (500 mil a 2,22 mi), lote tardio de recebimento (500 mil a 1 mi), conversão de brancos e nulos (500 mil, e nunca F→L em 2022), enchimento (250 mil) e o deslocamento uniforme em fatia de voto (1 mi a 2,22 mi, ou nunca). **O deslocamento uniforme em logit nunca é visto, em nenhuma magnitude, nos dois anos.** Para esses mecanismos, a frase "deixariam sinais muito maiores que os achados" **não** vale abaixo de aproximadamente 0,5 a 2,2 milhões de votos movidos.
3. **O poder é assimétrico entre os sentidos.** Em 2022, uma alteração dispersa a favor de Lula só atinge 80% de poder com 500 mil votos e a favor de Bolsonaro com 50 mil; em 2026 a assimetria aparece nos cinco grandes (1 mi contra 2,22 mi), nas UFs e na macrorregião Nordeste. A causa: a base real já tem cauda pró-Lula pesada (2026: 156 seções acima de z = 4 pró-Lula contra 53 pró-Flávio; 2022: 339 contra 107), o que eleva o limiar de alarme nesse sentido. **O experimento não é simétrico apesar de ter sido desenhado para ser.**
4. **D5 (dígito final) só reage a alterações grandes e escancaradas.** Alarme em 0% das execuções até 100 mil votos; acima disso, 4,9% a 5,1% no total, concentrado em "poucas seções com alteração grande" (21% em 2026 e 27% em 2022 das réplicas desse mecanismo, com 250 mil votos ou mais), justamente onde D1 a D4 já têm 100%. Nos outros mecanismos, quase zero. **O T05 ("dígitos uniformes", S0, "o teste tinha poder para ver o problema") não tinha esse poder para quase nenhum mecanismo:** deve ser reclassificado (09).
5. **A união dos detectores tem falso alarme de 4% a 14,5%** conforme o sentido e o ano (qualquer lado: 11,5% em 2026 e 14,5% em 2022), não 2,5%. Os poderes acima já estão calculados com esse limiar.
6. **O limiar do D1 importa:** em 2026, com seções dispersas e 100 mil votos, o D1 sozinho com z = 3 tem poder de 100%, com z = 5 tem 42%; o conjunto D1 a D4 com z = 4 (o do protocolo) tem 100%. Em 2022 (seções dispersas, 100 mil votos): 50% (z = 3), 20% (z = 5) e 50% (conjunto). A sensibilidade completa está na tabela.
7. **T44 não é um detector deste experimento.** O teste de grandes cidades do projeto usa o histórico de 2022 e tem poder em 2% dos válidos de **uma** cidade (31 mil a 139 mil votos). O "cinco grandes: 1 a 2,22 mi" desta grade é de D1 a D4 apenas; o T44 completa essa lacuna para uma cidade por vez. Não foi repetido aqui.

## 4. Experimento B: registros coerentes, mas artificiais
**B1 (registros coerentes assinados pelo próprio gerador, T62):** em 52.062 seções reais de MG, 2.497 alteradas (59.499 votos de Flávio para Lula): se tabela, BU, RDV, imagem e log são regenerados coerentes, **nenhuma** das seis verificações de consistência (tabela = BU, BU = RDV, BU = imagem, log = comparecimento, hash × lista assinada, assinatura e cadeia) acusa 1 seção. Se só a tabela é alterada, a comparação com o BU acusa as 2.497; se tabela e BU, o RDV, a imagem e o hash acusam; se tudo é alterado **sem reassinar**, só o hash da lista assinada acusa (2.497). Ver `resultados/identificabilidade.json`. **Isso mede um limite de identificabilidade, não a possibilidade operacional de comprometer urnas reais.**

**B2 (fabricar um 2º turno inteiro que mantém o resultado nacional):**
- O fabricante **ingênuo** é flagrado por D1 a D4, D6 e D7 nos dois anos.
- O **calibrado só em dispersão** passa D1 a D6 (em 2022, 10% das réplicas disparam D3) e é flagrado por D7 em 100% das réplicas (falta estrutura de local e de zona).
- O fabricante de **estrutura completa**, que replica os efeitos de zona e de local e **preserva os totais municipais**, **passa D1 a D7 em 2026** (5% das réplicas disparam D7) e mantém a margem nacional (4,393 mi contra 4,401 mi). **Em 2022 é flagrado por um detector (D2z, pró-Lula, 100% das réplicas)**, de modo que o teto não é universal: depende do ano e da implementação do atacante (aqui, efeitos gaussianos). Um atacante com acesso às respostas dos detectores poderia ajustar mais; isso não foi simulado.
- Essa v2 foi feita **depois** de ver que a v1 era flagrada por D2z e D3 por causa de um defeito de desenho do atacante (efeitos não centrados; total municipal não corrigido). Os resultados da v1 estão preservados (`sim_<ano>_fabricada.csv`).

## 5. Como o desenho evoluiu (registro honesto)
Etapas, nesta ordem: (1) protocolo com detectores D1 a D5, limiares, mecanismos e magnitudes; (2) um teste de fumaça com 2 réplicas, que mostrou que a base real tem escala robusta 0,50 e que o "uniforme" proporcional deixa rastro em logit, o que levou às emendas 1, 2 e 3 (D6 e D7, mecanismo `uniforme_logit`, fabricantes calibrado e de estrutura), todas **antes** de ver os resultados da grade; (3) a grade completa, uma execução por ano; (4) a inspeção da v1 do fabricante de estrutura (flagrado por D2z e D3 por defeito de desenho do atacante), que levou à emenda 4 e a uma segunda execução **apenas desse fabricante**. D1 a D5, os limiares e as magnitudes não mudaram em nenhum momento. Para refazer: `sim_adversarial.py <ano> 6 20` e `sim_fabricacao_v2.py <ano> 20`.

## 6. O que esta seção **não** conclui
- Que a base real foi alterada ou que não foi.
- Que alguém consegue, na prática, produzir os registros coerentes do experimento B.
- Que alterações menores que os limiares de cada mecanismo existam ou não: **abaixo do limiar de 80% de poder, o resultado é "sem alarme", e isso não exclui a alteração.**
- Que a soma das anomalias encontradas (dezenas de milhares de votos) seja um teto para alterações indetectadas: a tabela mostra mecanismos em que centenas de milhares de votos passam sem alarme.
