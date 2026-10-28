# 08. Check geral final: auditoria da própria investigação

Segunda passagem crítica, feita depois de todos os testes. Legenda: **[x]** feito e conferido; **[~]** feito em parte (o que falta está dito); **[ ]** não feito (o motivo está dito). Evidência da passagem: `resultados/auditoria_final.json`, `resultados/integridade_snapshots.json`, saída do `scripts/verificar.py`.

## O que a segunda passagem recalculou por outro caminho
- **1.942.246 certificados com cadeia válida, 0 falhas**: contagem direta dos quatro parquets, igual aos relatórios.
- **404 boletins de terceiros iguais à tabela do TSE** (votos de Lula e de Flávio), agora pelo caminho alternativo `votos.csv` do projeto de terceiros, sem reusar o meu parser do texto do QR: 404 de 404 em cada candidato.
- **Zeros:** 141 (2022) e 106 (2026) para o candidato da direita no 2º turno, 2 e 4 para Lula: recontagem direta da base.
- **Estabilidade do T63:** cinco células refeitas com sementes novas (réplicas 100 a 119): dispersas a 50 mil 100% (igual à grade), municípios a 50 mil 95% (igual), zonas a 25 mil 100% (igual), deslocamento uniforme em logit a 2,22 mi 0% (igual), cinco grandes a 500 mil 0% (igual).
- **O projeto não foi tocado:** nenhum arquivo foi modificado fora de `operacao_veracidade/`, exceto `dados/listas/recursos.csv`, que é o log de consumo de máquina e não é dado eleitoral. `verificar.py`: "tudo ok" (638 de 638 itens iguais ao oficial; cobertura 499.206 e 499.205 seções). Rodadas 1 a 6: todos os hashes iguais; amostra de 25 arquivos brutos igual ao manifesto.

## A. Dados e código
- [x] Arquivos brutos preservados (nenhuma escrita em `dados/`).
- [x] Hashes verificados (rodadas 1 a 6 e amostra do manifesto, duas vezes).
- [x] Snapshots antigos intactos.
- [x] Seções e turnos identificados corretamente: chave (UF, município, zona, seção); as trocas de turno e o pareamento entre anos foram conferidos nos casos de certificado (4.429 e 12.540 seções com urna trocada, em linha com a tabela).
- [~] Totais recalculados: `verificar.py` (638 de 638) e as contagens de zeros e de boletins de terceiros foram recalculadas; os totais nacionais dos 4 conjuntos não foram refeitos por script novo.
- [x] Exclusões documentadas (exterior e Sistema de Apuração sem `vota.vsc`; seções com menos de 20 votos válidos no T63).
- [~] Arquivos ausentes quantificados: herdado (173 arquivos de 2022, A173); não requantificado aqui.
- [x] Scripts reproduzíveis (`REPRODUCAO.md`), parâmetros e sementes registrados, resultados preservados.
- [x] **Falhas técnicas documentadas (todas minhas):**
  1. T61: contei como "antes das 19h" os boletins registrados antes das 19h de **qualquer dia** (216); o correto é 77 do dia 25/10 (corrigido no script e no relatório).
  2. `republicacao_bu.py`: o cache reabria o zip a cada linha (timeout); corrigido.
  3. Um `pkill -f` com padrão presente na própria linha de comando matou o meu shell (erro conhecido do projeto, anotado na memória); refeito em comandos separados.
  4. Fabricante "calibrado" escrito com a direção errada da correção de dispersão (a base real é sub-dispersa, escala 0,50); corrigido antes da grade (emenda 2).
  5. Fabricante de estrutura v1 flagrado por defeito de desenho (efeitos não centrados e total municipal não corrigido); v2 feita e a v1 preservada (emenda 4).
  6. Caso ES 85: eu citei "612 votos"; eram eventos de duas seções embutidos no pacote; corrigido no relatório 06.
  7. Três afirmações do 04 e três do 03 foram corrigidas depois de relidas contra os dados (grades não reportadas, máximo × percentil 95, D5 "sem poder" × "só reage a alterações escancaradas").

## B. Autenticidade e independência
- [x] Integridade de arquivo separada de autenticidade (T60b, escada hash → assinatura → cadeia → voto).
- [x] Assinatura separada de cadeia (T60a e controle sintético).
- [~] Cadeia de confiança externa examinada: **até a AC emissora em 100%; a raiz não é pública e a página oficial do TSE responde HTTP 403 a este ambiente (não contornado)**.
- [x] Evidência interna não confundida com externa (`01_MAPA_DE_CONFIANCA.md`).
- [~] Snapshots verificados quanto a origem e data: as 39 capturas do Internet Archive **não foram reverificadas nesta operação** (herdadas de Q6); a republicação de 404 arquivos foi verificada aqui.
- [x] Boletins de terceiros classificados por proveniência (T61: obtenção diferente, assinatura da mesma urna, amostra de conveniência).
- [ ] **Auditorias com votos conhecidos examinadas: não.** O teste de integridade (votação paralela) do TSE tem página bloqueada (HTTP 403) e o resultado numérico não foi obtido; a auditoria do TCU só foi lida pela notícia. Registrado como lacuna.
- [x] Lacunas de evidência externa explicitadas (`01`, seção "Busca por evidência externa").

## C. Estatística
- [~] Modelos calibrados: os detectores do T63 têm limiar calibrado por bootstrap; os três modelos de zeros **falharam** a calibração e foram declarados.
- [~] Validação fora da amostra: UF retida no T64; no T63, só uma segunda amostra de bootstrap e sementes novas; sem validação em dados de outra eleição conhecidamente limpa (não existe).
- [~] Dependência territorial: bootstrap por município; a dependência espacial **entre** municípios (Moran 0,16 a 0,20, T42) não entrou nos limiares.
- [ ] Dependência temporal: não aplicável aos detectores por seção; não tratada nos modelos de curva (sem modelo validado).
- [~] Multiplicidade: medida pelo falso alarme da **união** dos detectores; sem correção formal (Benjamini-Hochberg) nesta operação.
- [x] Poder de detecção medido; falsos alarmes medidos (com Clopper-Pearson); direção correta conferida, alarme oposto separado; **assimetria entre sentidos descoberta e declarada**.
- [~] Grandes municípios examinados: incluídos como mecanismo (cinco juntos); o T44 por cidade não foi repetido.
- [x] Modelos falhos não usados como prova (T64: "não determinável").
- [x] Dados sintéticos separados dos observados em todos os arquivos.

## D. Perguntas principais
- [x] Veracidade dos dados do TSE: `12` e `01`. [x] Integridade dos BUs e RDV e totalização: `02`, T61, T62. [x] Registros coerentes e incorretos: T62 e T63 (B1, B2).
- [~] Curvas de 2022 e 2026 e viradas, vales e periodicidade: `04`; conclusão "não foi possível determinar" depois de seis modelos; pausa de recebimento medida.
- [x] Zeros: `05`. [x] Primeiro × segundo turno: `05`. [~] Anomalias municipais e territoriais: `06` (sem teste novo para Salvador e zona 251; o T63 dá o poder).
- [x] Logs e explicações circulares: `06`, seção B. [x] Alterações distribuídas e concentradas: T63. [~] Todas as perguntas herdadas: respondidas em `07`; a releitura dos 16 casos do T14 por ID e data **não foi feita**.

## E. Vereditos e comunicação
- [x] Conclusões históricas confrontadas com os resultados novos (`09`, 22 itens).
- [x] Nenhum ponto cego tratado como refutado (H9 e H10 mantidos; novas lacunas acrescentadas).
- [x] Nenhuma simulação tratada como fraude observada (`03`, seção 6).
- [x] Nenhuma anomalia real omitida; as novas estão em `06`.
- [x] Nenhuma ausência de sinal apresentada como certeza absoluta.
- [~] Nenhum resultado estatístico sem método validado: os resultados do T64 e das curvas estão marcados como não determináveis; os do T63 são condicionais à base real como referência.
- [x] Nenhuma soma de anomalias tratada como limite universal (corrigido em `09`, item 3).
- [x] Cada afirmação importante rastreável a script e resultado (`REPRODUCAO.md`, `SHA256SUMS.txt`).
- [x] Site e README comparados com os dados **sem publicação**: `09` e `RECOMENDACOES_SITE.md`.

## Erros da auditoria final e o que ficou invalidado
- Nenhuma conclusão dos relatórios foi invalidada pela segunda passagem; foram corrigidos trechos de relatório durante a escrita (itens 1, 6 e 7 da seção A).
- **Limitação que invalida uma leitura ingênua do T63:** o poder é medido sobre uma base real que pode já conter alteração; o experimento não consegue dizer que a base real está limpa.
- **Itens não feitos e por quê:** auditorias com votos conhecidos (bloqueio HTTP 403 do TSE, sem número); releitura dos 16 casos do T14 (fora do orçamento); correção formal de multiplicidade; repetição do T44 por cidade.
