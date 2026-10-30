# Pré-registro: "curvas do 1º e do 2º turno sobrepostas" (rodada 8, ABERTA), 30/10/2026

Escrito antes de qualquer conta. **Origem (só pergunta, não fonte):** vídeo de 2 min 18 s publicado no Instagram por um perfil de professor (gravação de tela recebida em 30/10/2026; transcrição automática com Whisper medium, conferida contra os quadros do vídeo; texto em `fase3/externos/video_curvas_sobrepostas/transcricao.txt`). As alegações **não foram verificadas** por quem as divulgou nem por este projeto antes desta rodada. A rodada 8 **permanece aberta**: nada é congelado sem aprovação explícita do responsável.

## O que o vídeo mostra (descrição, sem juízo)
- Gráfico "Primeiro e segundo turnos sobrepostos": eixo X = "total acumulado de urnas recebidas"; eixo Y = "percentual acumulado dos votos nominais válidos" de Lula e de Flávio Bolsonaro, no 1º e no 2º turno.
- No 1º turno, a soma dos dois fica abaixo de 100% (há outros candidatos); o autor aplica um "fator de correção linear" que sobe os dois igualmente até a média de 50% (no quadro: "Deslocamento visual: 1º turno +4,00 p.p.").
- No 2º turno aplica um "botão de torção": "2º turno Lula −5,25 / Flávio +5,25 p.p. (não altera os dados originais)". Com isso, as curvas dos dois turnos "ficam extremamente semelhantes".
- No fim da curva, o cursor mostra: Lula 1º turno 49,08% e Flávio 51,10% (497.571 urnas); Lula 2º turno 46,51% e Flávio 53,49% (497.565 urnas). O autor chama isso de "projeção 53% para o Flávio e 46% para o Lula".
- Premissa declarada: "as pessoas chegam em ordem aleatória, as urnas são enviadas em ordem aleatória, e a gente vê processos tão similares".

## Alegações testáveis e como serão medidas
| # | Alegação | Medida (dados do TSE, `analise/base.parquet` e `base_2022.parquet`) |
|---|---|---|
| C1 | Reprodução das curvas e dos números do fim (49,08 / 51,10 / 46,51 / 53,49; 497.571 e 497.565 urnas) | curva acumulada de Lula e de Flávio (13 e 22) sobre os votos válidos, na ordem de `DT_BU_RECEBIDO_<turno>`; número de seções com boletim recebido; valores finais com e sem o deslocamento do vídeo |
| C2 | "Projeção 53% Flávio, 46% Lula" | conta exata: valor final do 2º turno com o deslocamento de ±5,25 p.p. menos o deslocamento; quantos votos o deslocamento representa e a comparação com a margem |
| C3 | "As urnas são enviadas em ordem aleatória" | correlação de postos (Spearman) entre a ordem de recebimento da mesma seção no 1º e no 2º turno; η² da UF e da região sobre a posição na ordem; curva sob ordem aleatória (200 permutações): faixa da curva depois de 1%, 5% e 10% das urnas |
| C4 | Semelhança "extremamente" alta das curvas dos dois turnos depois do deslocamento | na grade de 5% a 100% das urnas (passo de 1%): (a) correlação de Pearson entre as duas curvas centradas; (b) raiz do erro quadrático médio (RMS) depois do melhor deslocamento constante. Medido em **2026 e em 2022** (Lula × Bolsonaro) |
| C5 | A semelhança é "curiosa" (não esperada) | duas referências calculadas: **(i)** ordens independentes: os mesmos votos, cada turno em uma ordem aleatória própria (200 sorteios), distribuição de (a) e (b); **(ii)** contrafactual estrutural: o 2º turno previsto por seção = % de Lula da seção no 1º turno (dois candidatos) + virada nacional constante em logito (ajustada ao total), com os votos válidos reais do 2º turno, **na ordem real do 2º turno**; distância (máxima e RMS, em p.p.) entre o previsto e o real, em 2026 e em 2022 |

## Leitura pré-fixada
1. **C1/C2:** o deslocamento é declarado pelo próprio gráfico como visual. Se o valor final com o deslocamento, menos o deslocamento, der o resultado oficial, a "projeção 53% × 46%" é o número que o autor escolheu no botão, não um dado. Diremos quantos votos o deslocamento de 5,25 p.p. representa.
2. **C3:** se a ordem de recebimento da mesma seção se repete entre os turnos (Spearman alto) e depende da UF e da região, a premissa "ordem aleatória" não vale, e a forma da curva é composição geográfica de quem chega antes.
3. **C4/C5:** a semelhança é **esperada** se (a) a ordem de chegada se repete entre os turnos e (b) o voto de cada seção no 2º turno acompanha o do 1º. Será considerada **incomum** só se: a semelhança de 2026 for maior que a de 2022 **e** a curva real do 2º turno se afastar do contrafactual estrutural mais do que em 2022. Semelhança igual ou parecida com 2022 e real próximo do contrafactual = propriedade estrutural da apuração, sem sinal.
4. Sob ordens independentes (referência i), a correlação das curvas centradas deve ficar perto de zero; o RMS depois do deslocamento pode ser pequeno também (curvas quase planas). Por isso o RMS sozinho não mede "semelhança suspeita"; a leitura usa a correlação e o contrafactual.
5. Nada aqui afirma nem nega fraude além do que os números sustentam. Uma curva parecida entre turnos não indica fraude; uma curva diferente também não indicaria. O que o teste responde é se a semelhança vista no vídeo é inesperada.

## Itens fora do escopo
- Opinião pública ("metade da população com a pulga atrás da orelha") e a confiança nas instituições: não é dado do TSE; não testado nem afirmado.
- O código do autor (notebook) não foi divulgado; a reprodução usa a descrição e os quadros do vídeo. Diferenças pequenas de contagem de urnas (seções sem boletim, exterior) serão explicadas, não ajustadas para bater.

**Classe:** C1 e C2 determinísticos (A); C3 a C5 estatísticos/descritivos com referência simulada. **Natureza:** confirmatório. **Orçamento:** 1 execução + 1 correção. Script `fase3/curvas_sobrepostas.py`; saída `fase3/resultados/curvas_sobrepostas.json`. Teste **T71**, pergunta **Q57**.
