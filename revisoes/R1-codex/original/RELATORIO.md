# Revisão científica e técnica comparativa do Urna Lab

**Data da pesquisa:** 28/10/2026. **Objeto:** capacidade dos métodos, cobertura efetiva, interpretações e possibilidades de validação. **Este relatório não emite veredito sobre fraude.**

O Urna Lab já implementa uma investigação consideravelmente mais ampla do que a descrita no contexto inicial. Seu principal valor atual é reunir verificações dos arquivos, reconciliação de resultados, análises entre turnos e documentação dos próprios erros. A principal necessidade científica é ajustar a força das conclusões à força das verificações: coerência dos registros, identificação de comportamento individual, autenticidade da origem e probabilidade de detectar uma intervenção são questões diferentes.

## Como esta revisão foi feita

Examinei o projeto de trabalho em `~/Projects/apuracao-analise`, a cópia de publicação em `~/Projects/urna-lab-publico`, os documentos solicitados, o registro de testes, os principais leitores e scripts científicos, saídas pequenas e as seis skills locais. Também li o `CONCLUSAO.md`, inclusive novamente após o pedido do responsável. Na releitura, seu SHA-256 foi `7e27542563567e9a459416d88703dcf45718055b0e75bd489f1b43312a92400b`, igual ao instantâneo preservado. [Manifesto da leitura local](~/output/revisao-urna-lab-2026-10-28/manifesto_fontes_locais.json).

Preservei um instantâneo dos arquivos examinados fora do projeto, a partir das 03h08 de Brasília. Os links locais deste relatório apontam para essa cópia, para manter as referências verificáveis mesmo se o trabalho continuar. A publicação local estava inicialmente no commit `2df77bfccbf53090df88601a8475970644b0e512` e passou a `f69baec28d060f75fb0481fce60eefdb1af54165` durante a revisão; portanto, diferenças entre local e público precisam ser datadas. [Fontes e hashes preservados](~/output/revisao-urna-lab-2026-10-28/manifesto_fontes_pesquisa.json).

Usei três rótulos:

- **Verificado:** inspeção de código, documento, arquivo de saída ou controle mínimo executado nesta revisão. A presença de uma saída não significa que refiz seu cálculo integral.
- **Declarado:** resultado relatado pelo próprio Urna Lab ou por terceiros, sem replicação integral nesta pesquisa.
- **Inferência:** minha avaliação do alcance lógico ou estatístico do procedimento identificado.

Não alterei o projeto, testes, metodologia ou resultados; não reiniciei downloads, não instalei dependências e não executei a investigação pesada. As únicas execuções científicas novas foram controles mínimos de verificação de assinatura, em menos de um segundo por chamada, com saídas nesta pasta. O inventário de processos mostrou o monitor de recursos e um servidor HTTP local; não identifiquei os coletores ou leitores pesados citados no histórico naquele momento. Isso é uma observação pontual de processos, não uma garantia de que todo trabalho externo à revisão terminou.

## 1. Diagnóstico atual do Urna Lab

### 1.1 O que está implementado e possui resultados

**Verificado:** o registro preservado contém **48 entradas: 47 marcadas como concluídas e uma concluída/excluída da conclusão, T26**. Há saídas da bateria para 2022 e 2026, de logs para os quatro pares ano/turno, de comportamento, divergências, sensibilidade e aprendizado de máquina para ambos os anos. O catálogo contém instantâneos históricos que ainda dizem “em andamento”; eles não descrevem necessariamente a situação atual. [Registro](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:1), [catálogo](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CATALOGO.md:1).

| Frente | Implementação efetiva | Evidência de execução e alcance |
|---|---|---|
| Base eleitoral | Leitura dos BUs CSV; normalização de nomes de colunas de 2022; votos por seção; junção externa dos turnos | `base.parquet` e `base_2022.parquet` locais; construção por chave UF/município/zona/seção. [Código](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/montar_base.py:15) |
| Reconciliação T01/T32 | T01 soma nacional por votável; T32 compara BR, UFs e exterior com JSON de resultados | CSV de T32 contém 638 comparações de votos/comparecimento iguais e quatro divergências de eleitorado. Não há comparação municipal em T32. [T01](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/grafico/montar_dados.py:49), [T32](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/totalizacao.py:54), [saída](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/resultado_totalizacao.csv:1) |
| Integridade T14–T17b/T24 | Leitores de BU, RDV, imagem digital do BU, logs aninhados e listas assinadas; hashes, tamanhos, Ed521 e ECDSA P-521 | Há resultados processados de ambos os anos e turnos; as sínteses e exceções precisam manter denominadores próprios para cada arquivo. [Leitores](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/processar_brutos.py:118), [assinaturas](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/processar_brutos.py:207) |
| Logs T28–T31/T33 | Tipos de habilitação, janela final de 30 minutos, durações, habilitações ausentes, versões e eventos de verificação | Quatro JSON de logs. T28: 13/0 urnas sinalizadas em 2026, primeiro/segundo turno; 23/25 em 2022. [Código](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/analise_logs.py:46), [resumo das saídas preservadas](~/output/revisao-urna-lab-2026-10-28/resumo_saidas_preservadas.json) |
| Correspondência e preparação T34/T35 | CEFT × BU × certificado/log; presença de log da máquina de geração de mídia | JSON dos dois turnos de 2026. T35 verifica disponibilidade por máquina, não demonstra cada evento de carga de cada urna. [Código](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/correspondencia.py:25) |
| Exceções T36 | Regras que classificam divergências como contingência, RED, substituição, interrupção, energia ou publicação | Saídas com 186 casos no primeiro turno e 75 no segundo. São classificações dos próprios registros, com forças explicativas diferentes. [Regras](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/casos_integridade.py:93) |
| Contrafactuais T02–T04/T10/T11 | Virada em logit, resíduos municipais, MAD, correlação com chegada, comparação de urnas trocadas e reconstrução de curvas | Saídas para os dois anos. As previsões usam resultados do segundo turno para estimar a virada territorial. [Bateria](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:46) |
| Forense T05/T07/T21/T22/T25–T27 | Dígitos com ajuste local; cantos de comparecimento/votação; percentuais inteiros exatos; correlações; histogramas e momentos; Benford | Implementações presentes e resultados para ambos os anos; T26 excluído. T27 só produziu resultados de comparecimento nas saídas examinadas. [Bateria](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:62) |
| T12 e C01/C03/C06/C07/C08 | Regressões por perfil, descrições territoriais e Goodman restrito por UF | Saídas existentes; controles de perfil em `comportamento.py` estão condicionados a 2026. [T12](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/biometria.py:15), [C06](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/comportamento.py:78), [perfil](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/comportamento.py:145) |
| E01–E03 | Regressão por UF, fração de variância entre grupos, estatística de média por grupo com BH, lista de extremos | Modelos simples/completo para 2022 e 2026. Não encontrei implementação de Moran's I no código inspecionado. [Código](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/divergencias.py:33) |
| Poder/sensibilidade | T13: perturbações nos dados reais; T13b: conversão sintética de habilitações; T23: classificador em mundo simulado; sensibilidade de T02/T03 | Todos possuem saídas. Não são equivalentes entre si nem cobrem todos os testes registrados. [T13](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/poder.py:36), [T13b](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/poder_logs.py:33), [T23](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/ml_sintetico.py:57), [sensibilidade](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/sensibilidade.py:26) |

O Apêndice A inventaria todas as 48 entradas. T06 e T18 aparecem no catálogo histórico, mas não como entradas próprias no registro preservado; C04/C05 estão absorvidos por análises territoriais e pelo T20. Isso é uma questão de mapeamento, não demonstra ausência de trabalho. [Catálogo](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CATALOGO.md:77), [mapa de skills](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/MAPA_SKILLS.md:22).

### 1.2 Cobertura: o que os números realmente representam

**Declarado nas saídas do projeto, verificado como conteúdo dessas saídas:**

| Indicador de 2026 | Primeiro turno | Segundo turno |
|---|---:|---:|
| Linhas de arquivos processados no resumo | 499.207 | 499.207 |
| Seções com BU na base | 499.206 | 499.205 |
| Assinatura da lista válida no resumo | 499.176 | 499.178 |
| BU com hash/assinatura válidos no resumo | 499.176/499.176 | 499.178/499.178 |
| Log com hash/assinatura válidos no resumo | 499.176/499.176 | 499.177/499.177 |
| RDV igual ao boletim, segundo a síntese | 499.176 | 499.180 |
| Seções via Sistema de Apuração, segundo CEFT | 31 | 29 |
| T36: casos / classificados operacionais / publicação / sem explicação | 186 / 185 / 0 / 1 | 75 / 74 / 1 / 0 |

Fontes: [síntese gravada do relatório](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/grafico/web/relatorio_dados.json), [CEFT primeiro turno](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/resultado_correspondencia_1t.json:1), [CEFT segundo turno](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/resultado_correspondencia_2t.json:1), [T36 primeiro turno](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/resultado_casos_integridade_1t.json:1), [T36 segundo turno](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/resultado_casos_integridade_2t.json:1).

**Inferência:** “100%” precisa especificar o universo: seções cadastradas, BUs presentes, arquivos disponíveis, urnas eletrônicas ou urnas com determinada verificação. As duas linhas extras de arquivos no segundo turno, as seções de apuração não eletrônica e o log ausente não podem desaparecer por arredondamento. O verificador atual imprime contagem de linhas e percentual, sem validar igualdade de conjuntos de chaves ou falhar por cobertura incompleta. [Verificador](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/scripts/verificar.py:34).

A frase do `CONCLUSAO.md` sobre BU, log e lista válidos em todas as 499.178 urnas do segundo turno conflita com o próprio reconhecimento do log não publicado e com a síntese que conta 499.177 logs verificados. É preciso formular a afirmação por tipo de arquivo disponível. Essa observação não é uma alegação de assinatura inválida. [Conclusão](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:21), [exceção expressa](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:30).

O manifesto existe: seu log registra **51.846 arquivos e 404,9 GB**. Logo, manifesto e processamento completo já não são apenas planos. Entretanto, a semântica da marca de hash oficial exige correção documental e futura correção de código, descrita em 3.3. [Log](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/dados/listas/pos_manifesto.log:1), [gerador](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/scripts/manifesto.py:39).

O CSV de T32 contém 696 comparações ao incluir eleitorado. As quatro diferenças nessa variável são as seguintes; as linhas BR e ZZ são hierarquicamente relacionadas e não representam quatro ocorrências independentes:

| Turno / abrangência | Soma de aptos dos BUs | Eleitorado no JSON oficial | Diferença soma − oficial |
|---|---:|---:|---:|
| Primeiro / BR | 158.745.007 | 158.745.502 | −495 |
| Primeiro / ZZ | 916.039 | 916.534 | −495 |
| Segundo / BR | 158.744.977 | 158.745.502 | −525 |
| Segundo / ZZ | 916.158 | 916.683 | −525 |

**Verificado como conteúdo do arquivo:** essas diferenças não são divergências de votos. Sua causa cadastral/publicacional não foi esclarecida nesta revisão. O `make verificar` exclui eleitorado ao afirmar que todos os itens de voto/comparecimento conferem; a seleção é explícita no código. [CSV preservado](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/resultado_totalizacao.csv:1), [filtro do verificador](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/scripts/verificar.py:25).

### 1.3 O que está confirmado, exploratório ou pendente

**Confirmado por esta revisão:** existência e lógica das implementações indicadas; presença das saídas; conteúdo de T32; ausência de validação da cadeia no leitor local; controle mínimo Ed521; limitações de escopo identificáveis diretamente no código. Não confirmei de forma independente todas as assinaturas e contagens do país.

**Resultados registrados, com alcance condicionado aos métodos:** T02 encontra 33 seções na cauda positiva e 13 na negativa em 2026; o modelo t ajustado aos mesmos resíduos espera aproximadamente 9 e 8. Em 2022, observa 90 e 13, contra cerca de 36 e 35. Isso é sinal exploratório sobre a adequação de um modelo de virada; sua causa não está identificada. [Saída 2026](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/resultado_bateria_2026.json:1), [saída 2022](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/resultado_bateria_2022.json:1), [ajuste do nulo](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:175).

**Exploratórios:** listas E03, associações por perfil e estimativas de transições de C06. A frase “abstencionistas foram 4:1 para Lula” deve continuar sendo uma estimativa condicionada à homogeneidade das taxas por UF, não uma observação direta de eleitores. A faixa entre UFs é heterogeneidade geográfica, não intervalo de confiança da matriz nacional. [C06](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/comportamento.py:85), [faixas](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/comportamento.py:111), [conclusão atual](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:70).

**Pendências científicas reais:** validação criptográfica até uma âncora autenticada; verificação de formatos por uma implementação independente; validação de calibração/poder fora dos geradores já usados; confirmação de hipóteses em dados de fato não utilizados para descobri-las; explicação documental das exceções; reprodução integral a partir de clone limpo. Não são novos downloads obrigatórios nesta etapa. [Limites reconhecidos](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/AUTOAUDITORIA.md:103).

**Pendências de rastreabilidade:** sete entradas concluídas ainda apontam `script: (a fazer)` — T17b, T20, T34, T35 e E01–E03 — embora haja código efetivo. C06b tem resultado registrado, mas diz que o cálculo ainda deve ser incorporado ao script; não localizei sua implementação reproduzível no código examinado. O executor não roda entradas cujo comando é `—`. [Registro](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:1), [executor](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/scripts/rodar_teste.py:24).

**Não verificado:** funcionamento integral do site público, reprodução dos ~405 GB, todos os casos individuais de T36, disponibilidade universal dos certificados raiz e da especificação de 2026. Falha de acesso por uma ferramenta não prova inexistência pública desses materiais.

## 2. Comparação com projetos externos

As referências abaixo usam commits preservados nesta pesquisa. Li código selecionado e documentos; não executei integralmente os pipelines externos. “Independente” refere-se à implementação ou à coleta indicada, sem presumir independência completa dos autores, dos dados ou dos erros.

### 2.1 DataUrnas-BR

**Versão:** `12f0433bd20882d305dd7b9e4987d6dcf3b321a9`.

**Verificado no código:** leitores ASN.1 com versões de esquema, recontagem de RDV, assinaturas, scripts de análise de certificados e confronto com QR de BU coletado externamente. Há verificação do elo urna→AC e subida da cadeia até os certificados disponíveis. Isso acrescenta uma camada concreta em relação ao leitor local, que extrai a chave do certificado sem verificar sua emissão. [Parser](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/src/dataurnas/parsers/signature.py), [certificados](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/scripts/ele2026/analisar_certificados.py#L413), [recontagem](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/src/dataurnas/parsers/rdv.py).

**Declarado:** o relatório de integridade cobre 944.051 seções/turnos de 2022, com assinaturas válidas, mas só 941.653 comparações presidenciais com sua base; explica exclusões e lacunas. Para 2026, o relatório examinado cobre o primeiro turno e declara 499.207 seções. O README também menciona 941.987 seções da base de 2022: os universos não devem ser confundidos. [2022](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/docs/integridade-2022.md#L3), [2026](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/docs/relatorio-integridade-2026.md#L53), [README](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/README.md).

**Limite relevante:** a cadeia publicada nos relatórios termina nas ACs intermediárias; não chega à raiz. Há ainda observação sobre validade temporal do certificado disponibilizado da AC URNA em 2026. Não tratei essa observação como prova de certificado eleitoral inválido: o próprio projeto pede esclarecimento sobre possível renovação. [Certificados disponíveis e proveniência](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/data/certificados/README.md#L27), [limites](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/docs/relatorio-integridade-2026.md#L248).

**Contribuição externa específica:** o projeto relata confronto de 38 BUs de primeiro turno de 2026, provenientes de leitura de QR em papel, com os dados oficiais. É uma amostra de conveniência muito pequena, sem base para estimar uma taxa nacional de divergência. A coleta pode ser externa ao canal de publicação, mas BU e certificado continuam sendo produtos da urna. Não repliquei essa coleta. [Procedimento e cobertura](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/docs/confronto-fontes-externas.md#L3), [código](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/scripts/externo/confrontar_bu_externo.py).

**Validação mínima realizada aqui:** comparei as duas implementações Ed521 nas 11 assinaturas de arquivos listadas em uma fixture pública de AC; ambas aceitaram as legítimas, e a implementação externa rejeitou a mensagem de controle alterada. Outra fixture teve a assinatura da lista ECDSA aceita pelo leitor local. Isso não valida o país nem a cadeia. Ambas as implementações aceitam o controle com chave degenerada de identidade; portanto, trocar uma pela outra não fecha essa lacuna. [Resultado reproduzível desta revisão](~/output/revisao-urna-lab-2026-10-28/comparacao_ed521.json), [implementação externa](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/src/dataurnas/parsers/ed521.py#L131).

**Uso mais valioso:** comparação por arquivo e chave de seção, separando divergência de parser, de versão publicada, de cobertura e de totalização. O caso MA 7846/74/228 aparece como lacuna de publicação no DataUrnas e como arquivo obtido posteriormente no Urna Lab: isso sugere uma comparação de versões/proveniência, não dois resultados incompatíveis automaticamente. [Relatório externo](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/docs/relatorio-integridade-2026.md#L139), [registro local](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:31).

### 2.2 Ricardo Maia — eleicoes_2026

**Versão:** `a79a52ccac8f770735a053083d0bd8c665e8db0b`.

**Verificado:** modelos de inferência ecológica, margens com entradas/saídas cadastrais, limites de Fréchet, auditoria por programação linear, cenários sintéticos com verdade conhecida, heterogeneidade contextual, bootstrap por municípios e validação preditiva agrupada. O cenário B2 constrói fluxos diferentes com as mesmas esperanças agregadas por seção. Essa é uma contribuição particularmente pertinente ao C06 do Urna Lab. [Margens e limites](https://github.com/ricardomaia/eleicoes_2026/blob/a79a52ccac8f770735a053083d0bd8c665e8db0b/src/fluxos.py#L31), [gerador adversarial](https://github.com/ricardomaia/eleicoes_2026/blob/a79a52ccac8f770735a053083d0bd8c665e8db0b/src/auditoria_02_sintetico.py#L18), [validação](https://github.com/ricardomaia/eleicoes_2026/blob/a79a52ccac8f770735a053083d0bd8c665e8db0b/src/auditoria_08_validacao_cruzada.py#L1).

**Declarado:** a auditoria distingue previsão dos totais de identificação dos fluxos e mostra sensibilidade dos pontos estimados aos pressupostos. Há limitações de convergência dos modelos contextuais e de custo dos bootstraps. Algumas passagens ainda descrevem a amostra antiga, enquanto a seção 4.11 apresenta recálculo com todas as seções; a versão usada deve acompanhar cada número. [Auditoria, atualização](https://github.com/ricardomaia/eleicoes_2026/blob/a79a52ccac8f770735a053083d0bd8c665e8db0b/AUDITORIA_METODOLOGICA.md#L688), [limitações](https://github.com/ricardomaia/eleicoes_2026/blob/a79a52ccac8f770735a053083d0bd8c665e8db0b/AUDITORIA_METODOLOGICA.md#L830).

**Cuidado adicional encontrado no código:** a semente de um procedimento usa `hash(uf)`, que pode mudar entre processos/sessões Python sem `PYTHONHASHSEED` fixo. Não verifiquei todo o ambiente de execução, portanto isso é um ponto de reprodutibilidade a confirmar, não invalidação dos resultados. [Linha relevante](https://github.com/ricardomaia/eleicoes_2026/blob/a79a52ccac8f770735a053083d0bd8c665e8db0b/src/auditoria_08_validacao_cruzada.py#L50).

**Uso mais valioso:** submeter o estimador C06 aos geradores adversariais e comparar conjuntos de fluxos compatíveis, conservando as diferenças entre WLS restrito do Urna Lab e os modelos externos. Concordância de dois pontos estimados sob homogeneidade semelhante não é validação independente dessa homogeneidade.

### 2.3 Turicas — eleicoes-brasil

**Versão:** `1450e4a98a3159c45029ea933aaa0e1d1af7d89c`, ramo `develop`.

**Verificado:** pipeline histórico de extração, esquemas e cabeçalhos por formato, normalização, tratamento de codificações e sentinelas, além de testes de download e transformação. O projeto tem finalidade principalmente de engenharia de dados; não é substituto da auditoria criptográfica ou de inferência do Urna Lab. [Extratores](https://github.com/turicas/eleicoes-brasil/blob/1450e4a98a3159c45029ea933aaa0e1d1af7d89c/extractors.py), [pipeline](https://github.com/turicas/eleicoes-brasil/blob/1450e4a98a3159c45029ea933aaa0e1d1af7d89c/tse.py), [testes](https://github.com/turicas/eleicoes-brasil/blob/1450e4a98a3159c45029ea933aaa0e1d1af7d89c/tests/test_download.py).

**Declarado e relevante:** categorias desconhecidas podem interromper a conversão; códigos de cargo são preservados. A normalização também transforma diferentes motivos de ausência em células vazias e reconhece inconsistências ainda não resolvidas. [Regras de normalização](https://github.com/turicas/eleicoes-brasil/blob/1450e4a98a3159c45029ea933aaa0e1d1af7d89c/README.md#L22).

**Uso mais valioso:** adotar o princípio de adaptadores por versão e falha explícita em campos inesperados. Para pesquisa de integridade, manter também o valor bruto e o motivo da ausência; normalização conveniente para análise não deve apagar a distinção entre “não registrado”, “não aplicável” e “não divulgado”.

### 2.4 Vinícius Azevedo — tse-eleicoes-2026

**Versão:** `7a2618d31e484844e6d24417a6e327b63862939e`.

**Verificado:** análise descritiva de comparecimento e apoio, efeitos fixos de município e local, versões ponderadas e não ponderadas, erro agrupado por município e pareamento um para um com aptos/local estáveis. O código separa média das mudanças por seção de mudança das razões agregadas. [Modelos](https://github.com/viniciusazeved/tse-eleicoes-2026/blob/7a2618d31e484844e6d24417a6e327b63862939e/scripts/analyze.py#L47), [pareamento](https://github.com/viniciusazeved/tse-eleicoes-2026/blob/7a2618d31e484844e6d24417a6e327b63862939e/scripts/analyze.py#L135).

**Declarado:** o próprio plano ressalta que candidatos do segundo turno são complementares, que razões por aptos contêm comparecimento mecanicamente e que aptos/local iguais não demonstram identidade dos eleitores. As saídas registram cobertura dos recortes. [Metodologia](https://github.com/viniciusazeved/tse-eleicoes-2026/blob/7a2618d31e484844e6d24417a6e327b63862939e/METODOLOGIA.md#L13), [tabela de pareamento](https://github.com/viniciusazeved/tse-eleicoes-2026/blob/7a2618d31e484844e6d24417a6e327b63862939e/reports/pareamento_secoes.csv).

**Uso mais valioso:** comparação do T22 e das análises por perfil sob denominadores e universos idênticos. Efeito fixo de local e análise do suporte comum dos modelos de urna são extensões aos controles municipais; não eliminam confusão não observada nem identificam intenção de voto.

### 2.5 Marçal — apuracao-eleicoes-2026

**Versão:** `c39def899ae68c0318eeec089c3d004e58376de2`.

**Verificado:** originais recebidos são gravados com horário e fragmento do hash no nome, em modo de criação exclusiva; snapshots são acrescentados em NDJSON e o “latest” é gravado por troca de arquivo. O ingestor calcula SHA-256, mantém horário oficial e de recebimento e ignora resultados oficiais que retrocedem no tempo na publicação corrente. [Arquivo](https://github.com/marcal1981/apuracao-eleicoes-2026/blob/c39def899ae68c0318eeec089c3d004e58376de2/apps/web/lib/server/archive.ts#L19), [ingestor](https://github.com/marcal1981/apuracao-eleicoes-2026/blob/c39def899ae68c0318eeec089c3d004e58376de2/apps/web/lib/server/ingestor.ts#L203).

**Inferência:** é referência útil de proveniência e reconstrução do que foi observado pelo coletor. Hash local comprova identidade posterior do conteúdo preservado, não autenticidade independente nem impossibilidade de alteração conjunta do arquivo e da trilha. O próprio modo “nunca sobrescreve” é uma propriedade do código de gravação; não torna o disco inviolável.

Não encontrei, no material de código lido, um acervo público completo de capturas históricas que pudesse usar imediatamente para replicar a curva. Disponibilidade e continuidade do acervo precisam ser confirmadas antes de prometer reconstrução integral.

### 2.6 gabrielandr/apuracao-2026

**Verificado:** acesso direto ao GitHub, API do repositório e README bruto retornou 404; a API de repositórios públicos do usuário retornou lista vazia. O mecanismo de busca ainda mostrou uma descrição indexada recente. Índice de busca não equivale a repositório acessível. Não confirmei renomeação, arquivamento, exclusão ou privatização. [Registro das consultas](~/output/revisao-urna-lab-2026-10-28/verificacao_gabrielandr.json), [endereço consultado](https://github.com/gabrielandr/apuracao-2026).

Não atribuo implementação ou resultados atuais a esse endereço. O projeto de Marçal é alternativa de engenharia para preservação temporal, mas não substitui automaticamente o suposto acervo histórico perdido.

### 2.7 Referências acadêmicas: correspondência entre artigo e código

| Referência conferida | O que fundamenta e o que precisa ser distinguido |
|---|---|
| Klimek et al., 2012, DOI `10.1073/pnas.1210722109` | O artigo inclui modelo paramétrico e análise em níveis de agregação. T07/T22/T25 implementam diagnósticos inspirados nessa literatura, não sua reprodução integral. O próprio texto discute dependência dos momentos à agregação. [Original](https://arxiv.org/html/1201.3087), [código local](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:142) |
| Deckert, Myagkov e Ordeshook, 2011, DOI `10.1093/pan/mpr014`; comentário de Mebane, DOI `10.1093/pan/mpr024` | Há crítica forte a Benford e uma controvérsia publicada sobre simulação, agregação e expectativas eleitorais. Isso recomenda avaliação do nulo e do poder no domínio, sem tratar um dos artigos como regra universal. [Artigo dos autores](https://authors.library.caltech.edu/records/5jbtk-8wn05), [comentário original](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/BC29680D8B5469A54C7C9D865029FE7C/S104719870001281Xa.pdf/comment-on-benfords-law-and-the-detection-of-election-fraud.pdf) |
| Beber e Scacco, 2012, DOI `10.1093/pan/mps003` | A motivação é fabricação humana de números e pressupostos para dígitos finais. O ajuste exponencial local de T05 é uma adaptação do Urna Lab; sua distribuição nula precisa de calibração própria. [Original](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/AD86EEBC2F199E2C8A2FD36BD3799DF9/S1047198700013103a.pdf), [adaptação](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:62) |
| Kobak, Shpilkin e Pshenichnikov, 2016, DOI `10.1214/16-AOAS904` | O artigo usa janela próxima de inteiros, exclusões e simulações, incluindo sensibilidades. T21 usa igualdade modular exata, 200 binomiais e filtros próprios. São estatísticas diferentes, embora aparentadas. [Original, métodos](https://arxiv.org/html/1410.6059v4), [T21](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:111) |
| Rozenas, 2017, DOI `10.1017/pan.2016.9` | O método RKD trata picos e leis numéricas com densidade reamostrada. Não identifiquei RKD/`spikes` implementado no Urna Lab; citar a referência ao lado de T21 não equivale a implementá-la. [Original](https://www.cambridge.org/core/journals/political-analysis/article/detecting-election-fraud-from-irregularities-in-voteshare-distributions/1C48196DDCECC891F913CE0CEE948F3E), [T21](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:117) |
| Zhang, Alvarez e Levin, 2019, DOI `10.1371/journal.pone.0223950` | Fundamenta treinamento com dados sintéticos para detecção potencial de anomalias. T23 usa outro gerador e HistGradientBoosting; é adaptação, com validade dependente desse gerador. [Original](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0223950), [T23](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/ml_sintetico.py:57) |
| Figueiredo Filho, Silva e Carvalho, 2022, DOI `10.1016/j.fsisyn.2022.100286` | Estudo sobre 2018 com dígitos, correlação e RKD. Sua conclusão abrangente não pode ser transferida para outros anos, nem converter testes negativos de padrões em exclusão universal de fraude. Unidades, filtros e estatísticas diferem do Urna Lab. [Original](https://pmc.ncbi.nlm.nih.gov/articles/PMC9513110/) |
| Mebane/eforensics | A página institucional apresenta uma mistura bayesiana; não é especificação suficiente para validar uma implementação. Não encontrei esse modelo estimado no código local. Acrescentá-lo só teria valor após calibração contra alternativas legítimas. [Descrição institucional](https://democracy.umich.edu/michigan-expertise/election-forensics-identifying-election-fraud/), [referência local](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/REFERENCIAS.md:31) |

O `REFERENCIAS.md` cita Kim como “2025”. A referência de preprint indicada teve acesso original bloqueado nesta pesquisa, e os metadados encontrados apontam outra data; recomendo conferir versão, título e data antes de usá-la. **Não usei os resultados quantitativos dessa crítica como fundamento deste parecer.** Também não auditei toda a bibliografia periférica — imprensa, relatórios políticos, TCCs e panoramas — e não lhes atribuo o mesmo peso dos procedimentos originais examinados. [Entrada local](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/REFERENCIAS.md:33), [referência original a conferir](https://doi.org/10.31235/osf.io/6ka47_v1).

## 3. Lacunas metodológicas e diferenças verificáveis

As prioridades indicam risco para a interpretação e a reprodução. Não são categorias de suspeita sobre a eleição.

### 3.1 Prioridade alta: autenticidade ainda não fecha a cadeia de confiança

**Verificado:** `_verificador` extrai a chave e o nome do emissor do certificado; não verifica sua assinatura pela AC, validade, política ou caminho até uma raiz autenticada. `ler_vsc` verifica a lista com essa chave. [Código](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/processar_brutos.py:207), [lista](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/processar_brutos.py:315).

**Inferência:** isso demonstra coerência criptográfica com a chave fornecida, sujeita à correção do verificador. Ainda não demonstra, por si só, que essa chave pertence a uma urna autorizada pelo TSE. Uma raiz autoassinada qualquer também não resolve: é necessário autenticar a âncora por canal confiável. As comparações com CEFT/log ajudam a coerência de identidade, mas os registros continuam vindo do sistema avaliado.

A afirmação “toda alteração depois da urna quebra a assinatura” depende de hipóteses: chave autêntica e preservada, verificador correto, conjunto completo, vinculação correta seção/eleição/turno e controle de versões. Assinaturas isoladas não impedem omissão de arquivos, substituição de um pacote por outro pacote validamente assinado ou apresentação de uma versão anterior. Não identifiquei esses eventos nos dados; são limites da demonstração, relevantes à formulação da conclusão. [Afirmação da autoauditoria](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/AUTOAUDITORIA.md:37), [conclusão](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:33).

**Verificação proposta:** primeiro comparar os certificados intermediários disponíveis no DataUrnas com a documentação oficial e hashes oficiais; depois validar o caminho, o tempo relevante e a identidade. Até lá, preservar explicitamente o alcance condicionado da assinatura. A indisponibilidade de raiz para esta coleta é pendência de autenticação, não evidência de intervenção.

### 3.2 Prioridade alta: controles criptográficos não cobrem entradas degeneradas

**Verificado por controle mínimo:** `ed521.verifica(I, I || 0, h)` retorna verdadeiro para chave e ponto R iguais à identidade; `decodifica(b'')` também aceita uma entrada sem comprimento válido. A função mascara os bits de coordenada e não confere tamanho da chave nem rejeita explicitamente a identidade/subgrupos pequenos. [Código](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/ed521.py:45), [resultado do controle](~/output/revisao-urna-lab-2026-10-28/controle_ed521.json).

O resultado é matematicamente explicável: com A=R=identidade e S=0, a igualdade de grupo é satisfeita sem uma assinatura de uma chave regular. Isso é uma lacuna de validação de entradas do verificador. **Não demonstra que qualquer chave real das urnas seja degenerada ou que uma assinatura real aceita seja falsa.** Não fiz uma varredura de todas as chaves para essa propriedade.

Os cinco controles aleatórios T16c são úteis, mas não cobrem esse caso. A implementação do DataUrnas também aceitou a identidade no controle equivalente; sua checagem de tamanho é mais restrita. [T16c](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/controles/ed521_controles.py:39), [comparação](~/output/revisao-urna-lab-2026-10-28/comparacao_ed521.json), [código externo](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/src/dataurnas/parsers/ed521.py#L161).

**Verificação proposta:** vetores oficiais e adversariais de codificação, comprimento, pontos degenerados e subgrupo; definição explícita do perfil Ed521 aceito; validação das chaves pela cadeia. A RFC 8032 descreve Ed25519/Ed448 e não constitui sozinha uma especificação completa do perfil Ed521 da urna. Há material oficial do ITI sobre E521 a confrontar com a implementação e sua versão. [RFC](https://www.rfc-editor.org/rfc/rfc8032), [documento do ITI](https://repositorio.iti.gov.br/instrucoes-normativas/IN2018_15_DOC-ICP-01.01.htm).

### 3.3 Prioridade alta: manifesto confunde sucesso do download com hash oficial conferido

**Verificado:** o downloader cria `.ok` tanto quando o SHA-512 confere quanto no ramo `ok sem-hash`. O manifesto define `sha512_oficial_conferido` apenas pela existência dessa marca. Portanto, o campo pode dizer verdadeiro sem comparação com hash oficial. [Downloader, linhas 14–18](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/scripts/baixar_lista.sh:14), [manifesto, linha 44](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/scripts/manifesto.py:44).

**Alcance:** o SHA-256 calculado localmente continua sendo um identificador do conteúdo lido. O problema é a afirmação sobre autenticação/comparação oficial. Não concluí que os arquivos tenham hashes errados.

**Verificação proposta:** reconstruir esse estado pelos logs e arquivos de hash existentes; separar download concluído, hash local calculado, hash oficial disponível e comparação oficial realizada. O `mtime` gravado no manifesto tampouco equivale necessariamente ao horário de aquisição; a URL por nome de arquivo pode faltar ou ser ambígua. [Gerador](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/scripts/manifesto.py:19).

### 3.4 Prioridade alta: T13 não autoriza probabilidade geral de detecção

**Verificado:** T13 faz uma realização por combinação de cenário, todos os deslocamentos de votos favorecendo o candidato 13. Três limiares dependem das estatísticas da própria base; há um quarto limiar fixo. Não há ciclo de réplicas por cenário para estimar frequência de detecção e erro Monte Carlo. Seu teste de curva também toma máximo sem o corte de 5% utilizado na bateria principal. [Limiares](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/poder.py:60), [cenários](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/poder.py:89), [curva de poder](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/poder.py:46), [curva principal](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:95).

**Inferência:** “25 de 37 cenários detectados” é uma descrição dessa grade, não uma estimativa de 67,6% de poder geral. Não existe uma distribuição cientificamente justificada de intervenções representada por 37 casos equiprováveis. Detectar todos os exemplos acima de certo número de votos também não cria um limite superior universal para alterações não detectadas.

Consequentemente, a frase de `CONCLUSAO.md` segundo a qual uma intervenção localizada grande o bastante para mudar o vencedor “muito provavelmente” apareceria é mais forte do que o experimento atual permite. A magnitude e a forma da intervenção importam: mudanças heterogêneas alinhadas ao perfil, a efeitos territoriais ou a variáveis usadas no ajuste podem ser absorvidas. Isso não implica que tenham ocorrido. [Conclusão, linhas 53–59](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:53).

**Já há avanços:** T13b repete cinco vezes por cenário e T23 mede recall em simulações. Mas T13b só avalia T28, e T23 só cobre seu gerador. Nenhum deles valida automaticamente T05, T21, T22, T25 ou a regra conjunta de conclusão. [T13b](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/poder_logs.py:43), [T23](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/ml_sintetico.py:99).

### 3.5 Prioridade alta: referência histórica não é verdade conhecida sem fraude

O projeto reconhece limites, mas usa expressões como “dados reais (sem fraude)” em T13 e chama as sinalizações basais do T13b de falsos positivos. A base observada não vem com rótulo conhecido de ausência de toda intervenção. Em particular, as 13 sinalizações basais de T28 são achados, não falsos positivos demonstrados. [T13](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/poder.py:62), [T13b](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/poder_logs.py:41).

**Inferência:** 2022 é referência histórica útil, não controle negativo perfeito. Repetição de um padrão em 2022 pode favorecer explicações estruturais; não prova legitimidade do mecanismo nem especificidade do teste. Controlar especificidade exige mundos sem intervenção por construção e, idealmente, dados com rótulos independentes — preservando heterogeneidade legítima suficiente para desafiar o método.

Também convém evitar “teste que acusa dado limpo não entra” como regra de seleção pós-resultado: deve-se investigar e documentar falhas de calibração, com critérios definidos antes. Excluir T26 de um veredito pode ser adequado; isso não confirma os demais testes por contraste. [Princípio atual](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/AGENTS.md:17), [T26](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:155).

### 3.6 Prioridade alta: identificação ecológica não se resolve pelo ajuste dos totais

C06 minimiza erro de margens sob matriz constante por UF, com não negatividade e soma de linhas. A boa reprodução dos totais verifica coerência do ajuste, não demonstra que os fluxos latentes sejam os verdadeiros. Estimativas distintas podem reproduzir as mesmas margens quando as taxas variam com contexto. O projeto já reconhece C06b e a falácia ecológica; a lacuna é testar a robustez dos pontos como “4:1” contra essas alternativas. [Estimador](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/comportamento.py:85), [checagem](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/comportamento.py:114), [C06b no registro](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:918).

A função `goodman` descrita como efeitos fixos de município está definida, mas o fluxo efetivamente usado é `restrito` por UF. Portanto, o leitor não deve concluir que a estimativa final tem efeito fixo municipal pela presença da função anterior. [Função não utilizada no ajuste final](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/comportamento.py:57), [laço efetivo](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/comportamento.py:101).

As frações de X e Y são normalizadas por aptos de turnos diferentes. Para identidade de populações, mudanças cadastrais/temporárias e agregações exigem tratamento explícito; igualdade de tamanho não basta. Para os limites determinísticos de C06b, “usar o menor eleitorado” não substitui justificar uma população comum e entradas/saídas. [Normalização local](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/comportamento.py:38), [alternativa externa explícita](https://github.com/ricardomaia/eleicoes_2026/blob/a79a52ccac8f770735a053083d0bd8c665e8db0b/src/fluxos.py#L31).

### 3.7 Prioridade alta: não detecção não demonstra equivalência

T04 registra Mann–Whitney e diferença de médias com bootstrap municipal. Não rejeitar uma diferença não prova “urnas trocadas votaram igual”. O resultado precisa ser formulado como estimativa e intervalo, associado a uma margem de equivalência relevante e predefinida. O intervalo de 95% e o MDE calculado para α=0,01 também têm funções distintas. [T04](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:57), [INC](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:188), [frase atual](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:40).

T03 tem intervalo/MDE de Fisher usando o número de seções, sem ajuste de dependência municipal, enquanto o próprio projeto reconhece agrupamento. Esse cálculo não garante a precisão sob correlação intramunicipal. Em 2022, a correlação gravada é −0,0284, diferente dos +0,0043 de 2026; “2022 igual” não deve substituir a comparação quantitativa. O efeito pode ser pequeno sem ser numericamente igual. [INC T03](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:182), [conclusão](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:39).

### 3.8 Prioridade média/alta: agrupamento legítimo e p-valores de E02

E02 usa `sqrt(k) * média(z)` e distribuição normal padrão, supondo independência e escala apropriada. Se houver correlação positiva ρ entre seções de um local, a variância dessa estatística pode aumentar aproximadamente por `1 + (k−1)ρ`, sob uma estrutura simples de correlação. BH não corrige p-valores individuais mal calibrados. O agrupamento observado torna necessária essa avaliação. [Código](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/divergencias.py:87).

O modelo completo acrescenta perfil apenas para 2026; assim, comparar 683 locais de 2026 com 766 de 2022 não é uma comparação de especificações idênticas. E a diminuição dos extremos ao acrescentar covariáveis é evidência de sensibilidade do resíduo, não identificação causal da explicação. Recomendo comparar universos e modelos comuns antes da versão com controles adicionais. [Condição de ano](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/divergencias.py:47), [registro E02](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:1001).

Não encontrei matriz de vizinhança ou cálculo de Moran's I, embora o protocolo e o registro o citem. O procedimento atual mede agrupamento em unidades administrativas/locais; não uma autocorrelação espacial completa. [Protocolo](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/PROTOCOLO.md:84), [implementação](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/divergencias.py:70).

### 3.9 Prioridade média/alta: independência entre testes é mais que formato diferente

Tabelas, BU, RDV e log têm formatos diferentes, mas compartilham equipamento, software ou cadeia de publicação. Podem fornecer checagens complementares e falhar de maneira comum. Uma assinatura também não constitui uma terceira medida estatisticamente independente da intenção de voto. A emenda que exige “origem diferente” melhora a regra, mas não demonstra independência dos erros. [Diretriz](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/DIRETRIZ.md:59), [emenda](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/PROTOCOLO.md:101).

Há dependências matemáticas exatas: no segundo turno, participações entre válidos somam 1. No T22, correlações opostas dos candidatos decorrem dessa complementaridade; não são dois indícios independentes de comportamento legítimo. No T21, ser percentual inteiro exato para um finalista implica o mesmo para o outro. [T22](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:131), [T21](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:112), [interpretação da metodologia](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/METODOLOGIA.md:250).

**Verificação proposta:** mapa explícito de fontes e pressupostos compartilhados; separar independência de coleta, de implementação e de informação; avaliar a regra conjunta em simulações, em vez de contar testes favoráveis.

### 3.10 Prioridade média/alta: curvas ajustadas retrospectivamente

T10 utiliza a virada média das outras seções do município e a mediana da UF, ambas estimadas com resultados do segundo turno. Deixar a própria seção fora reduz uma forma de reutilização, mas o município inteiro continua informando a expectativa. Uma intervenção comum ao município pode ser absorvida. A versão estadual também usa o segundo turno; é menos local, não uma previsão ex ante independente. [Código](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:88).

T11 permuta resíduos nacionais sem preservar necessariamente tamanho, heteroscedasticidade e agrupamento territorial. Esses são pressupostos a verificar antes de interpretar o número de oscilações como diagnóstico calibrado. [Simulação](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:101).

A curva por recebimento de BUs é reconstrução da chegada registrada dos boletins. Não demonstra, sem snapshots, o que o público viu a cada instante no JSON de divulgação, que pode ter processamento e atualização próprios. A comparação com capturas preservadas por coletores resolve uma pergunta adicional de proveniência temporal.

### 3.11 Prioridade média: log, preparação e software precisam de linguagem estrita

T33 conta versões declaradas no log e eventos textuais de verificação. “Mesma versão registrada” não demonstra identidade dos binários executados nem eficácia independente da checagem. A frase “o software foi o mesmo em todas as urnas” deve ser limitada ao que foi observado. [Extração](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/seqlog.py:40), [conclusão](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:45).

T35 busca log de cada máquina mencionada na geração de mídia e resume versão/fase. Isso não reconcilia individualmente toda carga da urna, código de carga, data, seção e evento de preparação. A pergunta registrada é mais ampla do que a verificação efetiva. A saída do segundo turno também registra duas máquinas sem log entre 2.479, enquanto a conclusão cita apenas as três do primeiro. [T35](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/correspondencia.py:64), [saída segundo turno](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/resultado_correspondencia_2t.json:1), [conclusão](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:68).

T30 compara primeiro/último evento na ordem lida com abertura/encerramento e tolerância de 60 segundos; não testa literalmente ausência de qualquer voto após o encerramento. T29 já reconhece intervalos negativos e usa percentis. Essa correção documental é útil, mas a monotonicidade e segmentação por urna/reinício continuam condições para tratar extremos como tempos físicos. [T30](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/analise_logs.py:72), [ordem de leitura](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/processar_brutos.py:123), [T29 no registro](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:671).

T28 usa taxa não biométrica estimada do restante do dia como parâmetro binomial fixo. A incerteza dessa taxa, composição dos eleitores por horário e variação legítima devem entrar na calibração. Seu teste de poder altera contagens resumidas; não mede falhas do leitor de eventos nem a capacidade de detectar votos com habilitação aparentemente coerente. [T28](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/analise_logs.py:49), [T13b](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/poder_logs.py:49).

### 3.12 Prioridade média: “caso explicado” mistura graus de demonstração

No T36, qualquer explicação não vazia torna o caso `explicado`. A presença de troca/RED pode ser contexto relevante sem explicar quantitativamente toda diferença. E4 infere interrupção da diferença de uma confirmação; E5 procura reinício depois da habilitação, mas não exige explicitamente no código que tenha havido confirmação entre ambos. São hipóteses operacionais de forças distintas. [Regras](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/casos_integridade.py:114), [busca E5](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/casos_integridade.py:66).

O registro reconhece que E4 é mais fraca; os 149/48 casos E4 não deveriam entrar em uma frase de “prova determinística” da causa operacional. É possível preservar a conclusão de igualdade dos totais gravados sem afirmar que cada causa foi demonstrada. [Saída primeiro turno](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/resultado_casos_integridade_1t.json:1), [saída segundo turno](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/resultado_casos_integridade_2t.json:1), [limitação no registro](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:1070).

### 3.13 Prioridade média: rótulos de método, execução e pré-registro

T27 só calcula uma variável quando mais de mil contagens são ≥100. As saídas examinadas contêm apenas comparecimento; portanto, citar T27 como resultado de dígitos de brancos/nulos excede sua execução efetiva. [Filtro](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:167), [saída](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/resultado_bateria_2026.json:1).

O primeiro conjunto de testes foi executado por volta de 18h37; o protocolo diz ter sido escrito às 19h55, antes dos módulos seguintes. Hipóteses e correções anteriores não se tornam prospectivas por receber depois o campo “confirmatório”. Emendas são boa prática, mas o histórico precisa distinguir pré-especificação, adaptação após olhar resultados e confirmação posterior. [Cronologia](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CATALOGO.md:23), [protocolo](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/PROTOCOLO.md:7), [definição de confirmação](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/DIRETRIZ.md:76).

T23 separa municípios de treino e teste, uma proteção útil. Porém o gerador é calibrado usando resíduos reais do país inteiro, e o conjunto de teste também define o limiar de 1% usado na avaliação. É validação condicionada ao gerador com reutilização para calibração, não um teste final totalmente intocado. A fração real marcada, ~0,346% em 2026 e ~0,362% em 2022, não estima a fração real de irregularidades. [Gerador](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/ml_sintetico.py:59), [partição/limiar](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/ml_sintetico.py:91), [resultados](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/resultado_ml_2026.json:1).

## 4. Novas perguntas científicas e extensões justificadas

Não proponho simplesmente acrescentar Benford, ML, sensibilidade, RDV, logs ou limites de fluxos: o projeto já possui essas frentes. As seis propostas abaixo investigam aspectos ainda não cobertos ou tornam explícita uma extensão necessária. Nenhuma foi implementada nesta revisão.

### P1 — Quanto das estimativas de fluxo depende de hipóteses de homogeneidade?

1. **Pergunta:** quais transições entre turnos permanecem limitadas de forma útil se permitirmos taxas dependentes de contexto e mudanças cadastrais?
2. **Justificativa:** o C06 ajusta bem margens, mas isso não identifica necessariamente fluxos. O projeto externo fornece alternativas observacionalmente próximas. [C06](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/comportamento.py:85), [cenários adversariais](https://github.com/ricardomaia/eleicoes_2026/blob/a79a52ccac8f770735a053083d0bd8c665e8db0b/src/auditoria_02_sintetico.py#L18).
3. **H0/H1:** para a validade do modelo, H0: homogeneidade contextual dentro da UF fornece previsões calibradas e recuperação aceitável de fluxos nos geradores definidos; H1: heterogeneidade legítima produz viés relevante. Para fluxos individuais sem restrições, o produto é um conjunto identificado, não um teste binário.
4. **Dados:** margens por seção, cadastro por turno, agregações/transferências, perfil; populações sintéticas com fluxos verdadeiros conhecidos. Painel individual independente seria evidência adicional, se disponível.
5. **Método:** limites de transporte/Fréchet com entradas e saídas; estimadores irrestrito/restrito e modelos contextuais; programação linear sob graus declarados de heterogeneidade; validação agrupada.
6. **Alternativas:** comparar modelos com diferentes mobilizações, abstenções seletivas e fidelidades, inclusive fluxos distintos com margens equivalentes.
7. **Validação:** recuperar verdades conhecidas nas simulações com cobertura apropriada; publicar sensibilidade do conjunto identificado, convergência e previsão em municípios reservados.
8. **Limitações:** previsão boa não seleciona a matriz verdadeira; um painel também teria não resposta e erro de memória.
9. **Interpretação:** positivo para heterogeneidade enfraquece o ponto “4:1”; negativo o sustenta somente nos mundos/pressupostos testados; conjunto amplo significa não identificação. Nenhuma dessas saídas implica fraude.
10. **Já existe?** C06/C06b parcialmente. Falta a validação adversarial/contextual do estimador local e uma implementação rastreável do cálculo C06b.

### P2 — Qual é a sensibilidade da regra completa sob mundos legítimos e intervenções especificadas?

1. **Pergunta:** com falsos alarmes controlados, que magnitudes e formas de alteração a regra de decisão do projeto detecta com probabilidade estimável?
2. **Justificativa:** o T13 atual dá exemplos, sem uma probabilidade geral; T13b/T23 cobrem subconjuntos. [T13](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/poder.py:60).
3. **H0/H1:** H0: mundo gerado sem intervenção segundo uma família de modelos legítimos; H1: intervenção explicitamente definida sobre esse mundo. Definir famílias, não uma H1 universal chamada “fraude”.
4. **Dados:** covariáveis e distribuição de tamanhos reais, geradores legítimos com heterogeneidade, simulações preservando dependência territorial/temporal e, quando possível, evidência externa rotulada.
5. **Método:** réplicas por cenário e direção; separação entre calibração e avaliação; mesma implementação dos testes usados na conclusão; intervalos de Monte Carlo; cenários alinhados a covariáveis e mecanismos compensatórios.
6. **Alternativas:** incluir mobilização legítima, candidatos regionais, mudanças de comparecimento, substituição de urna, atrasos e erros de leitura simulados.
7. **Validação:** controle de erro na regra conjunta, poder com intervalo, sementes/gerador fixados e desempenho em geradores não usados para calibrar.
8. **Limitações:** cobertura é sempre relativa à família escolhida; nenhuma grade finita exclui todos os mecanismos.
9. **Interpretação:** alto poder permite uma afirmação condicional para aquele cenário; baixo poder limita o valor da não detecção; falha de calibração invalida o uso decisório desse teste até revisão. Não dá probabilidade de fraude a partir de não rejeição.
10. **Já existe?** T13, T13b e T23 parcialmente; a pergunta nova é a calibração da decisão conjunta e a robustez entre geradores. Começar pequeno para não refazer a investigação inteira.

### P3 — As inconsistências aparentes dependem do canal e da versão de publicação?

1. **Pergunta:** o mesmo objeto eleitoral, obtido no pacote por UF, por arquivo individual e por implementações distintas, possui os mesmos bytes e significado em uma versão definida?
2. **Justificativa:** o RDV ausente do MA, o log de SP e as diferenças de cobertura externa tornam versão/canal hipóteses concretas. [Casos locais](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:29), [caso externo](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/docs/relatorio-integridade-2026.md#L139).
3. **H0/H1:** H0: conteúdos equivalentes por chave/versão e diferenças limitadas a disponibilidade ou envelope documentado; H1: divergência semântica ou criptográfica persistente.
4. **Dados:** arquivos já preservados, listas assinadas, URLs, horários de aquisição, hashes e catálogos externos; pequenas novas coletas dirigidas, se necessárias em etapa futura.
5. **Método:** comparação diferencial de parsers, chaves e bytes; tabela de esperado/presente/verificado por tipo; trilha de revisões.
6. **Alternativas:** separar parser incorreto, seção agregada, recuperação de dados, arquivo atualizado, cache/CDN e canal desatualizado.
7. **Validação:** amostra estratificada fixada antes, todos os casos discrepantes e controle de arquivos propositalmente truncados/corrompidos; só expandir se houver desacordo.
8. **Limitações:** dois canais do TSE não são duas medições independentes do voto; hash local não autentica sozinho a origem.
9. **Interpretação:** igualdade fortalece equivalência de implementação/publicação no universo comparado; divergência persistente estabelece uma inconsistência específica cuja causa precisa de investigação; ausência de um canal é inconclusiva sobre conteúdo.
10. **Já existe?** T16/T17/T36 e manifesto parcialmente; falta uma comparação externa sistemática por versão e canal.

### P4 — A curva pública pode ser reconstruída pelos BUs recebidos, dentro da latência esperada?

1. **Pergunta:** diferenças entre snapshots de divulgação e soma de BUs por recebimento são compatíveis com processamento e publicação em lotes?
2. **Justificativa:** a curva reconstruída atual não é automaticamente a série que os usuários receberam. O arquivo de snapshots de Marçal oferece um desenho técnico complementar. [T10](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/bateria.py:88), [arquivo externo](https://github.com/marcal1981/apuracao-eleicoes-2026/blob/c39def899ae68c0318eeec089c3d004e58376de2/apps/web/lib/server/archive.ts#L19).
3. **H0/H1:** H0: discrepâncias limitadas a uma banda de latência/retificação definida e verificável; H1: diferenças persistentes fora dela. Uma H0 numérica depende primeiro de documentação operacional suficiente.
4. **Dados:** snapshots originais, horário oficial/recebimento, hashes, BUs, retificações e frequência de captura. O acervo histórico precisa estar realmente disponível.
5. **Método:** reconciliação por diferenças acumuladas, intervalos de captura e alinhamento temporal; teste da banda em períodos reservados.
6. **Alternativas:** fusos, relógio do coletor, perda de capturas, cache, processamento por lote e republicação.
7. **Validação:** reproduzir valores observados sem interpolação inventada; comparar dois coletores quando disponíveis; analisar separadamente lacunas da série.
8. **Limitações:** captura a cada vários minutos não reconstrói atualizações intermediárias; carimbo do servidor não prova todos os eventos internos.
9. **Interpretação:** discrepância positiva é problema de reconciliação temporal a esclarecer, não prova de votos manipulados; concordância valida a publicação observada; falta de snapshots impede responder retrospectivamente.
10. **Já existe?** T03/T10/T11 cobrem parte da pergunta temporal, sem confronto demonstrado com histórico independente de capturas.

### P5 — As associações por modelo de urna sobrevivem a comparações com suporte territorial comum?

1. **Pergunta:** diferenças de virada/comparecimento entre modelos persistem em locais comparáveis, após controlar composição e seleção do equipamento?
2. **Justificativa:** T20 usa resíduos municipais; modelos podem ocupar locais demograficamente distintos dentro do mesmo município. [T20](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/analise_logs.py:107), [controle por local externo](https://github.com/viniciusazeved/tse-eleicoes-2026/blob/7a2618d31e484844e6d24417a6e327b63862939e/scripts/analyze.py#L53).
3. **H0/H1:** H0: contraste condicional dentro de suporte comum é compatível com uma margem de equivalência substantiva fixada; H1: contraste excede essa margem. Não chamar o contraste de efeito causal sem desenho adicional.
4. **Dados:** modelo pelo log, local/seção, aptos/perfil, substituições, regra de distribuição e, se disponíveis, coordenadas/atas.
5. **Método:** efeitos fixos de local quando houver variação, pareamento/ponderação com diagnóstico de sobreposição, erros por conglomerado e testes de equivalência.
6. **Alternativas:** idade/escolaridade, transporte, ruralidade, alocação administrativa, disponibilidade e manutenção dos equipamentos.
7. **Validação:** equilíbrio de covariáveis, tamanho efetivo, estimativas com e sem pesos e municípios reservados; distinguir locais sem contraste identificável.
8. **Limitações:** falta de sobreposição pode impedir inferência; controle observado não remove toda seleção não observada.
9. **Interpretação:** contraste persistente é associação a investigar com registros operacionais; equivalência restringe contrastes maiores que a margem no suporte estudado; baixa precisão ou ausência de suporte é inconclusiva.
10. **Já existe?** T04/T20 parcialmente. Esta proposta refina identificação e precisão; não acrescenta outro teste nacional redundante por modelo.

### P6 — O que uma coleta externa de BU permitiria validar sobre publicação e impacto agregado?

1. **Pergunta:** BUs coletados no local por fonte externa conferem com a publicação, e que alcance amostral pode ser atribuído a essa comparação?
2. **Justificativa:** T15 lê `imgbu.dat`, não uma via física coletada de modo independente. O DataUrnas já tem procedimento de QR com amostra de conveniência. [T15](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/processar_brutos.py:338), [projeto externo](https://github.com/alissonlinneker/DataUrnas-BR/blob/12f0433bd20882d305dd7b9e4987d6dcf3b321a9/docs/confronto-fontes-externas.md#L7).
3. **H0/H1:** por BU, H0: igualdade dos campos por cargo/candidato; H1: discrepância. Para extrapolação, é necessário desenho amostral e um estimando definidos antes.
4. **Dados:** cópia/QR original, proveniência da coleta, chave completa, validação da assinatura/chave e dados oficiais correspondentes; inclusão probabilística ou descrição explícita de conveniência.
5. **Método:** comparação independente, dupla leitura dos desacordos e, apenas com desenho adequado, limites de erro e de margem agregada.
6. **Alternativas:** OCR/QR incompleto, seção/turno trocado, duplicação, versão oficial, seleção geográfica e fraude na própria coleta.
7. **Validação:** rastreabilidade, controles de leitura, todos os desacordos abertos à reprodução e cobertura documentada; não generalizar 38 concordâncias de conveniência ao país.
8. **Limitações:** BU físico ainda é saída da mesma urna. Mesmo perfeita concordância não verifica intenção digitada nem habilitação legítima de cada eleitor. Não constitui, por si só, RLA do registro individual.
9. **Interpretação:** discrepância validada demonstra desacordo entre publicação e via coletada; igualdade valida os BUs observados; amostra seletiva impede estimar prevalência nacional. Nenhuma dessas saídas isoladamente demonstra intenção deliberada.
10. **Já existe?** T15 digital e procedimentos externos parcialmente. Coleta externa com desenho de inferência não está implementada no Urna Lab. Ela ampliaria a regra atual de usar só dados oficiais; requer uma decisão futura explícita de escopo, sem mudar o projeto agora.

## 5. Possíveis validações independentes, sem circularidade

| Validação | Independência obtida | O que ainda permanece compartilhado | Começo de menor custo |
|---|---|---|---|
| Urna Lab × DataUrnas em BU/RDV/assinatura | Implementações, esquemas e caminhos de leitura distintos | Arquivo e equipamento de origem; possíveis padrões/pressupostos comuns | Fixtures por ano/modelo e amostra de exceções; expandir após concordância |
| Leitor mínimo × ASN.1 oficial | Interpretação estrutural, desde que o esquema seja autenticado | Mesmos bytes | Exemplos oficiais locais, campos ignorados e eleições múltiplas |
| Verificador Ed521 × implementação/vetores independentes | Aritmética e rejeição de entradas inválidas | Perfil criptográfico e âncora de confiança | Vetores pequenos, identidade/subgrupos/codificações; já há controle mínimo nesta pesquisa |
| C06 × geradores adversariais | Verdade sintética conhecida e recuperação de parâmetro | Escolha do gerador e hipóteses de identificação | Casos pequenos com margens equivalentes e fluxos diferentes |
| T22 × estudo descritivo de Vinícius | Implementação, controles e ponderações | Dados do TSE e confusores não medidos | Mesmas chaves, filtros, denominadores e universo de locais |
| Curva reconstruída × snapshots de coletores | Captura do que foi publicado em cada instante | Backend de divulgação e relógios potencialmente relacionados | Manifesto de snapshots e período curto com duas capturas |
| BU publicado × papel/QR de observadores | Canal de aquisição e preservação | Urna que gerou o BU | BUs já coletados; não iniciar coleta maciça sem desenho |
| Saídas da urna × auditoria externa de software/teste de integridade | Referência sobre execução/registro além dos arquivos de saída | Possíveis limites de seleção e condições do teste | Protocolos, amostragem e microdados de auditoria disponíveis, sem tratar notícias como base completa |

As comparações propostas se apoiam nos procedimentos examinados acima e nas opções de auditoria descritas pelo próprio TSE, que distingue hashes, assinaturas, comparação com BU impresso, atas, código e RDV. [TSE — auditoria](https://www.tse.jus.br/eleicoes/urna-eletronica/seguranca-da-urna/como-realizar-auditoria).

Para reduzir circularidade, cada replicação deve congelar hipóteses e critérios antes de conhecer os resultados do outro projeto, usar uma implementação própria ou previamente existente, comparar desacordos por unidade e conservar resultados negativos. Usar a mesma base já preparada e o mesmo algoritmo só testa repetibilidade da execução.

A documentação oficial de 2022 já publica ASN.1 e exemplos; essa lacuna está parcialmente resolvida no local. A disponibilidade do material foi confirmada no portal. A extensão a 2026 exige distinguir campos adicionais e versões; “não consegui acessar” não deve virar “o TSE não publica”. [Documentação oficial de 2022](https://www.tse.jus.br/eleicoes/eleicoes-2022/documentacao-tecnica-do-software-da-urna-eletronica), [atualização da autoauditoria](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/AUTOAUDITORIA.md:118).

## 6. Limites científicos e a pergunta original

A pergunta “houve fraude nas eleições brasileiras?” reúne hipóteses sobre fases, agentes, mecanismos, escala e intenção. Um projeto centrado na disputa presidencial de 2026 e referência em 2022 não responde automaticamente por todos os cargos, anos ou formas de irregularidade. A unidade da conclusão deve acompanhar a unidade do teste.

| Pergunta específica | Evidência necessária | Capacidade dos dados/métodos examinados |
|---|---|---|
| O conteúdo baixado mudou depois de preservado? | Hash local, manifesto/versionamento e preservação da referência | Respondível para o conteúdo preservado; depende da integridade da referência usada na comparação |
| O arquivo corresponde à assinatura apresentada? | Verificador correto e bytes completos | Respondível condicionalmente; não autentica sozinho quem forneceu a chave |
| A chave é de uma urna autorizada e válida no contexto? | Cadeia, âncora autenticada, identidade, validade e contexto eleitoral | Parcial no Urna Lab; falta validação da cadeia; disponibilidade pública não foi esgotada universalmente |
| A publicação soma fielmente os registros eleitorais examinados? | Reconciliação por unidade e agregado, controle de conjunto e exceções | Grande parte é respondível; T01 atual só soma por votável e T32 tem escopo territorial limitado |
| O RDV corresponde ao BU? | Leitura independente e comparação por cargo/votável | Respondível para os registros disponíveis; ambos podem compartilhar um erro anterior à gravação |
| O voto digitado foi registrado corretamente? | Evidência independente do mecanismo de registro; auditoria de software/execução e testes de integridade com desenho conhecido | Não se resolve somente por RDV=BU=log. O segredo do voto não impede toda auditoria, mas impede inferir identidade individual a partir desses agregados |
| Cada habilitação correspondeu a eleitor legitimamente presente? | Documentação de comparecimento/identificação, atas e ocorrências, sob acesso adequado | Logs permitem padrões e inconsistências específicas; não autenticam independentemente a presença de todas as pessoas |
| Existe uma irregularidade estatística? | Nulo adequado, calibração, controles, multiplicidade e reprodução | Respondível relativamente a um modelo e unidade. Rejeição não identifica causa nem intenção |
| Houve uma intervenção específica? | Predições discriminantes, registros documentais/técnicos e confronto independente | Pode ser investigada se o mecanismo deixa rastros distinguíveis; atualmente não há identificação geral por classes de padrão |
| Uma irregularidade alterou o vencedor? | Erros/intervenções demonstrados, direção e magnitude ou limite rigoroso da margem | Não se obtém somando outliers nem usando o maior cenário sintético não detectado como teto universal |
| Houve intenção deliberada? | Evidência específica de ação, autoria, processo e contexto | Não se deduz de p-valores, hash divergente ou erro de software isoladamente |

As distinções entre arquivos públicos, BU impresso, atas e software acompanham o leque de auditorias do TSE. [Fonte oficial](https://www.tse.jus.br/eleicoes/urna-eletronica/seguranca-da-urna/como-realizar-auditoria). Os limites sobre o que os procedimentos locais efetivamente demonstram são inferências desta revisão a partir do código citado nas seções 1 e 3.

Uma intervenção uniforme que preserve todos os registros pode ser não identificável nesse conjunto de observações. **A uniformidade não é a única forma possível de não identificação:** qualquer alternativa que produza os mesmos observáveis, ou seja absorvida pelos ajustes, exige informação adicional para ser distinguida. Isso é uma propriedade dos modelos, não uma afirmação de que tais alternativas aconteceram.

O limite de risco de uma auditoria pós-eleitoral é uma garantia probabilística vinculada a um protocolo e a registros auditáveis independentes adequados. O Urna Lab não adquire essa garantia por ter muitos testes ou ter detectado cenários sintéticos grandes. A literatura de RLA exige trilha confiável, preservação e desenho de amostragem/verificação; BUs e RDVs provenientes do mesmo mecanismo não satisfazem automaticamente a verificação da escolha individual. [Lindeman et al., 2012, requisitos](https://www.stat.berkeley.edu/~stark/Preprints/RLAwhitepaper12.pdf).

### 6.1 Revisão específica do CONCLUSAO.md relido

| Formulação atual | Avaliação metodológica e formulação possível para revisão futura |
|---|---|
| “Não foi encontrada evidência de manipulação” | Pode descrever o resultado classificado pelo estudo, desde que acompanhado de universo, hipóteses alcançadas e validações ainda não fechadas; não adoto aqui essa frase como veredito independente. [Linha 9](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:9) |
| “O resultado publicado é exatamente o que as urnas gravaram e assinaram” | Requer explicitar universo/arquivos disponíveis, cadeia ainda não validada e exceções. Formulação proporcional: os registros disponíveis examinados apresentam as igualdades e validações listadas, sob os pressupostos declarados. [Linha 11](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:11) |
| “As fraudes que os testes conseguiriam ver não aparecem” | A não rejeição não informa retrospectivamente que toda intervenção detectável teria sido encontrada. Publicar a família de cenários e probabilidades estimadas é mais preciso. [Linha 12](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:12) |
| “Voto a voto” no T01 | O código só compara soma nacional por votável; não confronta cada seção das duas fontes. [Linha 19](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:19), [implementação](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/grafico/montar_dados.py:49) |
| Todos os logs válidos em 499.178 urnas no segundo turno | Um log não estava disponível; a verificação gravada cobre 499.177. Ausência não é assinatura inválida. [Linhas 21/30](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:21) |
| “Nenhum voto depois do encerramento” | Código registra zero urnas cujo último evento lido excede encerramento+60s; esse é o enunciado diretamente sustentado. [Linha 44](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:44), [teste](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/analise/analise_logs.py:78) |
| “O software foi o mesmo” | O observado é mesma versão textual nos logs examinados. [Linha 45](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:45) |
| Uma fraude localizada que mudasse o vencedor “muito provavelmente” apareceria | A grade de 37 realizações não fundamenta essa probabilidade para a classe ampla de mecanismos. [Linha 59](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:59) |
| “Abstencionistas ... 4:1” como padrão | Deve vir sempre como estimativa sob modelo; não é fluxo diretamente observado. [Linha 70](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/CONCLUSAO.md:70) |

Não alterei nenhuma dessas passagens. A tabela oferece fundamentos para uma revisão futura das afirmações, não um novo texto conclusivo sobre a eleição.

## 7. Recomendações por valor científico e custo

### Imediatas: custo baixo, sem nova análise nacional

1. **Consolidar o estado observado e a terminologia.** Atualizar futuramente os caminhos/comandos das oito entradas incompletas de rastreabilidade; distinguir histórico de estado atual; trocar “todos/igual/prova” por universos e verificações precisos onde o código é mais estreito. Há resultados úteis que podem permanecer, com alcance mais claro.
2. **Tratar primeiro a semântica do manifesto e a confiança criptográfica.** Registrar a distinção `.ok`/hash oficial; documentar o controle degenerado; confrontar o perfil e certificados disponíveis com fonte oficial. São falhas técnicas/limites identificáveis sem reprocessar 405 GB.
3. **Revisar a afirmação de poder.** Descrever T13 como grade de perturbações efetivamente executada; não apresentar o maior cenário não detectado como limite de alteração possível. T13b/T23 devem manter seus alcances separados.
4. **Separar execução de validade científica.** “Concluído” significa que houve execução registrada; não significa que o método identificou a causa, atingiu poder adequado ou passou por auditoria independente.
5. **Preservar as exceções e seus graus explicativos.** Distinguir contagem demonstrada, classificação operacional compatível e causa documentalmente confirmada, especialmente em T36.

Estas prioridades derivam das verificações das seções 3.1–3.7 e 3.12–3.13, com arquivos e linhas ali indicados.

### Próxima rodada pequena e delimitada

| Ação futura | Valor científico | Custo relativo e condição de expansão |
|---|---|---|
| Corpus pequeno de fixtures oficiais e casos adversariais dos leitores/Ed521 | Detectar erro de interpretação/validação antes de qualquer nova execução nacional | Muito baixo; expandir só após concordância |
| Reconciliação por chaves e arquivo, com DataUrnas | Diferenciar erro comum, cobertura e versão de publicação | Baixo em amostra; expandir se houver desacordo ou para uma cobertura formal definida |
| Desafio adversarial do C06 | Medir identificabilidade dos fluxos que alimentam narrativas substantivas | Baixo/moderado em geradores pequenos; posterior análise completa se houver valor |
| Calibração de T03/E02 e equivalência T04/T20 | Tornar incertezas e resultados negativos interpretáveis | Moderado nos dados tabulares existentes; sem download bruto |
| Poder replicado de poucos mecanismos prioritários, com dois sentidos e decisão conjunta | Sustentar afirmações quantitativas condicionais | Moderado; começar com réplicas pequenas e erro Monte Carlo explícito |
| Inventário de snapshots externos realmente disponíveis | Saber se P4 é respondível retrospectivamente | Baixo, de consulta; não iniciar coletor nem prometer série integral |

As comparações externas são propostas de P1–P6; não exigem copiar conclusões ou substituir a metodologia atual antes da revisão.

### Investigações futuras, após estabilização

- Extensões P1–P6 pré-especificadas, com conjuntos reservados e dados versionados.
- Mais eleições apenas se responderem uma questão comparativa definida; adicionar anos sem harmonizar unidades e formatos pode multiplicar artefatos.
- Coleta documental externa de casos específicos e, se houver desenho viável, amostragem probabilística para avaliar publicação/totalização. Qualquer ampliação para dados não oficiais deve ser declarada como novo escopo.
- Reprodução integral a partir de clone limpo como validação de engenharia, planejada à parte, com orçamento realista superior à estimativa antiga de 250 GB. Ela não substitui a validação metodológica.

**Critério para escolher o próximo trabalho:** qual hipótese concorrente o resultado poderá distinguir, que afirmação mudará, e qual é o menor conjunto de dados/cálculos capaz de decidir isso. Se duas explicações permanecerem observacionalmente equivalentes, registrar esse limite pode valer mais cientificamente que acrescentar um teste com alta significância.

## Apêndice A — Inventário do registro de testes

A tabela abaixo foi gerada do instantâneo de `testes/registro.json`. “Concluído” é o estado declarado pelo projeto. A coluna de implementação foi confrontada com os scripts examinados; a presença de resultado não equivale a validação independente.

| ID | Pergunta registrada | Implementação localizada | Estado declarado |
|---|---|---|---|
| [T01](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:14) | O Boletim de Urna bate com a votação por seção, voto a voto? | grafico/montar_dados.py | concluido |
| [T02](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:39) | Alguma seção virou diferente das vizinhas? | analise/bateria.py | concluido |
| [T03](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:64) | A virada depende da hora de chegada ao TSE? | analise/bateria.py | concluido |
| [T04](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:87) | Urna trocada entre turnos votou diferente? | analise/bateria.py | concluido |
| [T05](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:110) | Último dígito uniforme? | analise/bateria.py | concluido |
| [T07](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:133) | Assinatura de enchimento de urna? | analise/bateria.py | concluido |
| [T08](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:156) | Boletim emitido antes do fim da votação? | analise/testes.py | concluido |
| [T09](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:179) | O buraco de 17h10–19h03 (2º turno) e a prorrogação | analise/investigar.py | concluido |
| [T10](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:202) | A curva da apuração teve movimento fora do natural? | analise/bateria.py, analise/curva.py | concluido |
| [T11](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:225) | Zigue-zagues demais na curva? | analise/bateria.py | concluido |
| [T12](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:245) | Liberação sem biometria afeta a virada? | analise/biometria.py | concluido |
| [T13](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:269) | Que fraude os testes conseguiriam ver (poder)? | analise/poder.py | concluido |
| [T13b](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:293) | Poder dos testes de log (eleitor fantasma sintético) | analise/poder_logs.py | concluido |
| [T14](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:313) | Votos no log = comparecimento? Confirmações + nulos por suspensão = total? | analise/processar_brutos.py | concluido |
| [T15](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:338) | Boletim impresso = dado publicado? | analise/processar_brutos.py | concluido |
| [T16](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:358) | Assinatura digital válida e arquivos íntegros? | analise/processar_brutos.py, analise/ed521.py, analise/der.py | concluido |
| [T16c](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:383) | A implementação Ed521 rejeita o que deve rejeitar? | analise/controles/ed521_controles.py | concluido |
| [T17](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:406) | Recontagem pelo RDV = boletim? | analise/processar_brutos.py | concluido |
| [T17b](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:426) | O bu.dat (somado na totalização) = RDV = publicado? | analise/processar_brutos.py | concluido; caminho/comando incompleto no registro |
| [T19](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:449) | A mesma bateria em 2022 | analise/bateria.py, analise/montar_base.py | concluido |
| [T20](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:472) | Modelo de urna (lido do log) afeta a virada? | analise/analise_logs.py | concluido; caminho/comando incompleto no registro |
| [T21](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:492) | Percentuais inteiros em excesso? | analise/bateria.py | concluido |
| [T22](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:515) | Assinatura de fraude incremental? | analise/bateria.py | concluido |
| [T23](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:538) | Classificador com fraude sintética | analise/ml_sintetico.py | concluido |
| [T24](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:561) | Urnas substituídas no meio do dia | analise/processar_brutos.py | concluido |
| [T25](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:584) | Impressão digital 2D e curtose | analise/bateria.py | concluido |
| [T26](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:604) | 2º dígito de Benford | analise/bateria.py | concluido excluido da conclusao |
| [T27](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:627) | Dígitos de branco, nulo e comparecimento | analise/bateria.py | concluido; saída só de comparecimento |
| [T28](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:647) | Rajada de habilitações sem biometria no fim do dia (eleitor fantasma)? | analise/seqlog.py | concluido |
| [T29](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:670) | Votos rápidos demais? | analise/seqlog.py | concluido |
| [T30](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:693) | Há voto antes da abertura ou depois do encerramento da própria urna? | analise/seqlog.py | concluido |
| [T31](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:717) | Voto computado sem habilitação? | analise/seqlog.py | concluido |
| [T32](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:740) | Soma das urnas = total oficial divulgado? | analise/totalizacao.py | concluido |
| [T33](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:764) | Software oficial em todas as urnas? | analise/seqlog.py | concluido |
| [T34](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:787) | Urna usada = urna preparada para a seção? | analise/correspondencia.py | concluido; caminho/comando incompleto no registro |
| [T35](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:811) | Toda urna usada tem carga registrada? | analise/correspondencia.py | concluido; caminho/comando incompleto no registro |
| [C01](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:834) | Comparecimento por região, porte e perfil | analise/comportamento.py | concluido |
| [C02](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:854) | A que horas o eleitor votou? | analise/relatorio_dados.py | concluido |
| [C03](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:874) | Voto x perfil demográfico | analise/comportamento.py | concluido |
| [C06](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:894) | Para onde foram os votos do 1º turno? | analise/comportamento.py | concluido |
| [C06b](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:918) | Quantos eleitores trocaram diretamente de um finalista para o outro? | não localizado como cálculo executável; registro indica incorporar | concluido |
| [C07](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:941) | Mudança de comparecimento x perfil | analise/comportamento.py | concluido |
| [C08](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:961) | Geografia da virada (região, UF, porte) | analise/comportamento.py | concluido |
| [E01](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:981) | Divergências em vários níveis | analise/divergencias.py | concluido; caminho/comando incompleto no registro |
| [E02](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:1001) | Divergências agrupadas no espaço? | analise/divergencias.py | concluido; caminho/comando incompleto no registro |
| [E03](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:1024) | Lista das maiores divergências e explicação | analise/divergencias.py | concluido; caminho/comando incompleto no registro |
| [INC](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:1047) | Qual a incerteza e o poder dos resultados negativos? | analise/bateria.py | concluido |
| [T36](~/output/revisao-urna-lab-2026-10-28/fontes/urna-lab-local/testes/registro.json:1070) | As urnas cujas contas de integridade não fecham exatamente têm explicação? | analise/casos_integridade.py | concluido |

## Apêndice B — Material da revisão e reprodução dos controles mínimos

- [Manifesto dos arquivos locais](~/output/revisao-urna-lab-2026-10-28/manifesto_fontes_locais.json) e [manifesto das fontes preservadas](~/output/revisao-urna-lab-2026-10-28/manifesto_fontes_pesquisa.json).
- [Controle Ed521](~/output/revisao-urna-lab-2026-10-28/controle_ed521.json), [comparação mínima entre implementações](~/output/revisao-urna-lab-2026-10-28/comparacao_ed521.json) e [resumo das saídas de logs](~/output/revisao-urna-lab-2026-10-28/resumo_saidas_preservadas.json).
- [Verificação de disponibilidade do repositório Gabriel](~/output/revisao-urna-lab-2026-10-28/verificacao_gabrielandr.json).
- [Script dos controles mínimos](~/output/revisao-urna-lab-2026-10-28/controles_revisao.py), que lê as fontes preservadas e imprime resultados, sem escrever no projeto.

As fontes preservadas contêm apenas código, documentação, metadados e pequenas fixtures públicas selecionadas; não são uma cópia dos dados eleitorais completos. As bibliografias citadas não foram todas replicadas. Os resultados nacionais e os resultados declarados de terceiros permanecem sujeitos à reprodução independente descrita neste relatório.
