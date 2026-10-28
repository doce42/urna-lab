# F3: execução da fila (28/10/2026), pré-registro

Escrito antes de rodar. Quatro investigações, cada uma com um teste principal e uma validação, uma correção e uma repetição por falha operacional. Sem subagente, sem reprocessamento nacional. Regra adversarial: registro do próprio sistema é "compatível", não "verificado".

## F1. As 153 seções-turno de 2022 com log diferente do comparecimento (`fase3/fila_f1_log2022.py`)
**Pergunta:** por que o log publicado registra menos (70 + 36 seções) ou mais (34 + 13) votos que o comparecimento do boletim? É erro do leitor do projeto ou ausência real no arquivo?

**Procedimento:** para cada seção, abrir o `.logjez` do pacote local e listar todos os arquivos de log dentro dele. Contar, por arquivo e por número de urna, os eventos "O voto do eleitor foi computado", o primeiro e o último voto e os reinícios. Comparar com o comparecimento do boletim, a "urna efetivada" da tabela e o certificado do boletim.

**Categorias, por regra fixa, na ordem:**
1. **Artefato do leitor:** a soma recontada a partir de todos os arquivos do log é igual ao comparecimento.
2. **Log da urna substituta ausente:** log de uma só urna, diferente da urna do boletim, e o último voto bem antes do encerramento.
3. **Log com votos de outra urna ou dia:** recontagem maior que o comparecimento, com votos fora do dia ou de urna que não é a do boletim.
4. **Outra:** com a descrição.

**Validação:** a recontagem própria é comparada com a coluna `computado` do parquet. Deve ser igual nas seções em que a regra 1 não se aplica.

**Leitura:** nenhuma categoria verifica a causa real, que é "compatível". Divergência objetiva é preservada.

## F2. Assinatura das seções do Sistema de Apuração de 2026 (`fase3/fila_f2_sa2026.py`)
**Pergunta:** nas seções de 2026 com arquivos do Sistema de Apuração (`-busa.dat`, `-imgbusa.dat`, `-sa.vsc`, `-logsa.jez`), a lista assinada é válida, os arquivos conferem e o boletim coincide com a tabela?

**Procedimento:** o mesmo do SA22. Decodificar o `-sa.vsc` com o leitor da urna e conferir tamanho, SHA-512 e assinatura de cada arquivo. Decodificar o `-busa.dat` e comparar com a tabela. A validação é a leitura do texto do `-imgbusa.dat`.

**Fonte:** pacotes do 1º turno e do 2º turno. No 2º turno de SP, os arquivos baixados urna a urna.

## F3. As 10 seções-turno de 2022 sem boletim lido (`fase3/fila_f3_semboletim.py`)
**Seções:**
- 1º turno: ZZ 29505/1/78, ZZ 29564/1/91, ZZ 29505/1/79, ZZ 29416/1/38, PA 4383/91/73.
- 2º turno: RS 86568/100/15, PA 4499/17/41, ZZ 29505/1/78, ZZ 29564/1/91, ZZ 29505/1/79.

**Procedimento:** listar os arquivos de cada seção no pacote, ler o boletim (`.bu` ou `.busa`) e a lista assinada, e comparar com a tabela. Se não houver boletim, a seção fica "não verificável", com o motivo.

**Validação:** leitura do texto da imagem, quando houver.

## F4. Modelo de chegada dos boletins (Q10, Q12) (`fase3/fila_f4_chegada.py`)
**Pergunta:** dadas as horas reais de emissão dos boletins, a ordem de recebimento produz um número de viradas e uma posição da última virada incomuns?

**Modelo:**
- **Atraso:** atraso = recebimento − emissão do BU (minutos, em log). É regredido em UF, log do tamanho do município, capital, zona e faixa de 30 minutos da emissão.
- **Ordens simuladas:** emissão real + atraso previsto + resíduo sorteado com reposição dentro da UF. São 200 simulações por eleição.
- **Estatísticas, fixadas antes:**
  - V, o número de trocas de liderança na grade de 1% a partir de 10% das urnas;
  - U, a fração apurada na última troca;
  - S3, o maior vale.

**Validação, fixada antes:**
- **Pelos anos:** o modelo é **validado** se, em 2022 (1º e 2º turnos), os valores observados de V, U e S3 caem dentro dos percentis 2,5 a 97,5 das simulações.
- **Pela divulgação:** nas capturas do R2 de 2022 (2º turno), a proporção de Lula divulgada no mesmo número de seções cai dentro da faixa de 95% das simulações.

**Leitura (só se validado):** para 2026, o observado fora dos percentis 2,5 a 97,5 é "incomum sob o modelo"; dentro, "não incomum".

**Parada:** se não validar, Q10 e Q12 ficam "não determinado" e nenhum outro modelo é tentado nesta sessão.

**Limite já conhecido:** a hora de emissão vem do relógio da própria urna, então o modelo toma como dada a ordem de emissão e só testa a parte de transmissão e recebimento.

## Execução e desvios (registrados depois de rodar)
- **F3:** executado como previsto.
  - 5 das 10 seções foram lidas e conferem com a tabela.
  - Elas tinham linha no parquet geral de 2022 sem votos: o parquet foi gerado com versão anterior do leitor de boletim.
  - 5 do exterior não têm nenhum arquivo no pacote local e ficam não verificáveis.
- **F1:** uma correção operacional (chave em tupla no JSON).
  - **Achado de método:** em 2022, o terceiro campo da linha do log, usado pelo leitor como número da urna, não é o número da urna em parte dos logs. O valor 67305985 aparece em seções de vários estados. A classificação por urna (categorias 2, 2b e 3) **não é válida** e foi substituída pela descrição das partes do log (`revisao_da_classificacao` no resultado).
  - **Também afeta:**
    - a coluna `urnas_com_voto_no_log` de 2022;
    - o subconjunto "duas urnas no log" da validação de 2022 do caso C adversarial.
  - A recontagem em si foi validada: 153 de 153 iguais ao leitor.
- **F2:** executado como previsto.
- **F4:** executado como previsto. O modelo **não foi validado** em 2022, e nenhum outro modelo foi tentado.
