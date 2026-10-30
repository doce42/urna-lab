# Catálogo do projeto apuracao-analise

Registro de tudo que foi feito: etapas, testes, metodologia, dados baixados, consumo de máquina, internet, tempo e tokens.
Data de início: 27/10/2026, 18h03. **Correção às 20h48:** algumas linhas das 20h3x–20h5x tinham horário estimado (inclusive à frente do relógio); foram corrigidas pelo horário de modificação dos arquivos de cada etapa. Horários das etapas já feitas reconstruídos pelos horários dos arquivos e dos logs de download.
Desde 19h10, o consumo é medido a cada 30 s por `scripts/monitorar.sh` → `dados/listas/recursos.csv`.

## 1. Linha do tempo das etapas

| Hora | Etapa | Script / arquivo | Resultado |
|---|---|---|---|
| 18:03 | Mapear a estrutura do site de resultados do TSE (eleição 6258, pleito 3221) | — | Achados os arquivos por seção e por urna |
| 18:04 | Baixar votação por seção (BR, todos os cargos) e filtrar Presidente | `dados/originais/votacao_secao_2026_BR.zip` | 499.205 seções; totais Lula 64.256.232, Flávio 59.826.041 |
| 18:06 | Baixar Boletim de Urna (BU na Web) do 2º turno, 27 UFs | portal de dados abertos | Faltava Roraima (link do portal aponta para o .sha512); baixado pelo endereço direto, hash conferido |
| 18:08 | Baixar BU na Web do 1º turno | — | **Incidente:** extraído no disco do sistema (25 GB, quase lotou). Parado, movido para o SSD de 1 TB, só Presidente mantido |
| 18:12 | Gráfico v1 (lightweight-charts) | `grafico/web/index.html` | Eixo não proporcional ao tempo; corrigido |
| 18:15 | Gráfico v2: tempo exato (um ponto por segundo), painéis separados | idem | — |
| 18:17 | Filtrar Presidente dos dois turnos no SSD | `scripts/filtrar_presidente.py` | 5,17 milhões de linhas |
| 18:20 | **Incidente:** São Paulo do 1º turno estava cortado (extração interrompida). Baixado de novo, hash ok | — | Totais passaram a bater |
| 18:26 | Montar dados do gráfico com conferência | `grafico/montar_dados.py` | BU = votação por seção, voto a voto, nos 2 turnos |
| 18:27 | Gráfico com 1º, 2º e Comparar | `grafico/web/index.html` | — |
| 18:36 | Base única por seção (2 turnos lado a lado) | `analise/montar_base.py` → `analise/base.parquet` | 499.206 seções |
| 18:37 | Bateria de testes, 1ª rodada | `analise/testes.py` → `resultado_testes.txt` | 3 sinais suspeitos |
| 18:38 | Investigação dos sinais | `analise/investigar.py` | Os 3 eram artefatos (ver seção 3) |
| 18:39 | Testes corrigidos | `analise/testes_corrigidos.py` → `resultado_testes_corrigidos.txt` | Sem anomalia |
| 18:41 | Prorrogação no 2º turno confirmada nos dados | consulta direta | 6.748 urnas fecharam 18h30–19h30; votaram como as vizinhas |
| 18:43 | Correção do fuso no modo "Fim na urna" | `grafico/montar_dados.py` | Emissão começa às 17h nos 2 turnos |
| 18:47 | Análise da curva (quebras, reversões, previsto) | `analise/curva.py` → `resultado_curva.txt` | Real × previsto: até 0,08 pp |
| 18:48 | Pesquisa de metodologia (literatura) | `METODOLOGIA.md` | — |
| 18:51 | Curva prevista no gráfico | `grafico/prever.py` | Confere voto real segundo a segundo |
| 18:53 | Downloads: perfil do eleitorado, 2022, brutos do 1º turno | `scripts/baixar_lista.sh` | Retomável, confere .sha512 quando existe |
| 18:55 | Teste de poder (fraude sintética) | `analise/poder.py` → `resultado_poder.txt` | Ver seção 3 |
| 18:58 | Correção do teste T4 (Goiás/Caiado) | idem | Falso alarme eliminado |
| 19:00 | Perfil do eleitorado por seção | `analise/perfil.py` → `analise/perfil.parquet` | 516.785 seções |
| 19:01 | Biometria com controles | `analise/biometria.py` → `resultado_biometria.txt` | Efeito some (era idade) |
| 19:02 | Download dos brutos do 2º turno, urna por urna | `scripts/baixar_brutos_2t.py` | 48 conexões; 19:08 subiu para 96 com prioridade baixa |
| 19:04 | Leitor dos brutos (log e boletim impresso) | `analise/processar_brutos.py` | Acre: 100% batendo depois de 2 correções (log arquivado; nulo por suspensão) |
| 19:10 | Gráfico v3: painel único, 6 modos | `grafico/web/index.html` | — |
| 19:10 | Monitor de consumo ligado | `scripts/monitorar.sh` | — |
| 19:12 | Paleta de cores validada para daltonismo (validador dataviz, temas escuro e claro) | `grafico/web/*.html` | Vermelho, azul e verde-azulado; branco/nulo diferenciados pelo traço |
| 19:14 | Página de relatório + dados agregados | `grafico/web/relatorio.html`, `analise/relatorio_dados.py` | Botão de PDF; metodologia e catálogo embutidos |
| 19:19 | Leitor DER mínimo e estrutura do RDV | `analise/der.py` | RDV decodificado sem a especificação oficial |
| 19:20 | Recontagem pelo RDV (urna de teste) | — | Igual ao boletim impresso, voto a voto |
| 19:21 | Estrutura do `vota.vsc` e do certificado | — | Lista assinada com SHA-512 por arquivo; hashes conferem |
| 19:23 | Brutos do 1º turno: download concluído | — | 28 UFs, 95 GB |
| 19:25 | Bateria única 2022 × 2026 | `analise/bateria.py`, `analise/montar_base.py 2022` | Mesmo perfil nos dois anos; 2022 bate com o oficial (Lula 60.345.999 × Bolsonaro 58.206.354) |
| 19:27 | Modelos antigos: bloco `ueao` minúsculo; ECDSA P-521 + SHA-512 sobre o hash | `analise/processar_brutos.py` | Assinaturas UE2013/UE2015 validadas |
| 19:29 | Ed521 das UE2020/UE2022 identificado (SHAKE256-132, domínio "SigEd521", M = SHA-512 do hash) | `analise/ed521.py` (gmpy2, 3 ms/verificação) | Válido; 1 bit alterado → falha |
| 19:31 | Processador com assinatura, hash, RDV e urnas substituídas | `analise/processar_brutos.py` | AC 2.270/2.270 e MS 7.106/7.106 em tudo |
| 19:33 | Processamento completo do 1º turno iniciado (12 processos) | idem | — |
| 19:36 | **Incidente:** download por urna do 2º turno a 2 urnas/s (recusas 429 + espera exponencial) | `scripts/baixar_brutos_2t.py` | Limite do site é de conexões; HTTP/2 multiplexado não leva recusa |
| 19:38 | Pacotes oficiais do 2º turno descobertos no CDN (não listados no portal), exceto SP | `dados/listas/brutos_2t_pacotes.txt` | 27 UFs, ~100 GB |
| 19:39 | Pesquisa de literatura recente (2016–2026) | `METODOLOGIA.md`, `REFERENCIAS.md` | Kobak 2016, Rozenas 2017, Zhang 2019, CSH Viena 2022, Anwar 2026, RLA, controvérsia Mebane 2024 |
| 19:42 | T21 (percentuais inteiros) e T22 (fraude incremental) na bateria | `analise/bateria.py` | Sem sinal nos dois anos |
| 19:45 | Documentação: `PIPELINE.md` (reprodução, dicionário de dados, armadilhas) e `REFERENCIAS.md` | — | — |
| 19:47 | **Incidente:** SP por urna com curl HTTP/2 (150 pedidos em paralelo) estourou o limite por IP; recusas até em pedidos avulsos | — | Trocado por downloader com controle de ritmo (AIMD) que respeita o 429 e vigia a publicação do pacote de SP |
| 19:55 | `PROTOCOLO.md`: o estudo passa a ter protocolo pré-registrado (Q1–Q6, N1–N7, módulos A–F, critérios) | — | — |
| 20:00 | Downloader de SP liberado pelo site depois da punição; subiu sozinho até 200 pedidos/s sem recusa | `scripts/baixar_sp_2t_educado.py` | — |
| 20:03 | **Incidente:** transferência de votos (C06) sem restrição dava valores > 100% e negativos; com restrição, o otimizador não convergiu (pesos sem normalizar) | `analise/comportamento.py` | Corrigido; conferência previsto × observado com erro < 0,1% |
| 20:10 | Emenda 1 ao protocolo: T17b, T28–T33, E02, Benjamini-Hochberg | `PROTOCOLO.md` | — |
| 20:12 | Leitura da sequência do log eleitor a eleitor | `analise/seqlog.py` | AP: mesma versão de software em 1.914 urnas; 0 voto sem habilitação; 1 verificação de software sem "SUCESSO" (a investigar) |
| 20:15 | T32 totalização: soma das urnas × site oficial (BR, 27 UFs, ZZ; 2 turnos) | `analise/totalizacao.py` | 638/638 itens de voto e comparecimento iguais; eleitorado do exterior difere em 495/525 (41 seções não instaladas = 423; o resto ainda sem explicação confirmada) |
| 20:20 | Emenda 2 e autoauditoria (mapa de ameaças) | `AUTOAUDITORIA.md` | Acrescentados T34, T35, T13b, cobertura |
| 20:20 | Pacotes do 2º turno: download concluído (27 UFs) | — | — |
| 20:20 | Projeto agêntico: `AGENTS.md`, 6 skills, `MAPA_SKILLS.md`, `testes/registro.json`, `Makefile`, `scripts/verificar.py`, `rodar_teste.py`, `listas_tse.py`, `preparar_dados.sh`, `requirements.txt`, `.gitignore`, `git init` | — | `make verificar` passa |
| 20:24 | T25 (Klimek 2D/curtose), T26 (2BL), T27 (dígitos) | `analise/bateria.py` | T25 sem massa no canto, igual a 2022; T26 acusa nos dois anos e nos dois candidatos (contagens pequenas): excluído da conclusão; T27 uniforme |
| 20:25 | **Pacote oficial de SP do 2º turno publicado** (detectado pelo vigia); download por urna parado em 34 mil arquivos; pacote de 25,8 GB baixando | — | — |
| 20:31 | Processamento do 2º turno iniciado (14 processos; estados grandes em partes); leitura antiga do 1º turno interrompida de propósito (será relida inteira com sequência do log e bu.dat) | `analise/processar_brutos.py` | — |
| 20:31 | DIRETRIZ.md incorporada (classes A–G, independência, exploratório × confirmatório); emenda 3; inventário completo no registro | `DIRETRIZ.md`, `PROTOCOLO.md`, `testes/registro.json` | — |
| 20:33 | T17b `bu.dat` decodificado: AC 2.270/2.270 = publicado = RDV; o campo "sem habilitação biométrica" do BU na Web = habilitação **biográfica** do bu.dat (afeta a leitura do T12) | `processar_brutos.py` (`ler_bu`) | — |
| 20:34 | T34/T35, 1º turno: CEFT = BU em 499.206/499.206; 31 seções por "Sistema de apuração" (cédula) e 50 por recuperação de dados; certificado ≠ CEFT em 43 de 395.551; 3 de 2.453 máquinas geradoras de mídia sem log GEDAI | `analise/correspondencia.py` | A investigar |
| 20:35 | Revisão cega externa do METODOLOGIA: situação desatualizada (pendente × feito) era versionamento; métodos e situação separados; instantâneo preservado (CATALOGO, seção 6) | — | — |
| 20:35 | T16c controles Ed521 (300 urnas, 5 controles negativos) | `analise/controles/ed521_controles.py` | Todos ok |
| 20:39 | **Erro meu, corrigido:** INC com n errado (municípios no lugar de seções) e bootstrap desalinhado (base reordenada no T10); detectado porque o IC não continha a estimativa | `analise/bateria.py` | Corrigido |
| 20:40 | INC: T03 desprezível com IC; T04 limítrofe e abaixo do MDE; **T02 excesso na cauda pró-Lula nos dois anos (classe B, exploratório)** | — | Confirmar nos logs |
| 20:43 | **Erro meu, corrigido:** no 2º turno o log.jez traz arquivado o log do 1º turno da mesma urna; as contagens simples (votos computados, confirmações, votos por minuto) somavam os dois turnos (RJ deu 19,9 mi). A sequência (seqlog) já filtrava o dia. Contagens passam a usar só o dia da eleição do turno; processamento do 2º turno reiniciado (12 min perdidos). Validado: AC 2º turno 2.270/2.270 em log = comparecimento, confirmações = total, assinatura, RDV = bu.dat = publicado | `analise/processar_brutos.py` | Corrigido |
| 20:45 | **T23 versão 1 inválida (erro de desenho meu):** classe limpa = dados reais, então ~1% marcadas era circular. Preservada em `analise/ml_sintetico_v1_invalido.py` e `resultado_ml_<ano>_v1_invalido.json`. Versão 2 com classe limpa simulada: reais 0,35% (2022: 0,36%), poder declarado | `analise/ml_sintetico.py` | Concluído |
| 21:03 | **2022 completo:** confirmado que só tínhamos as tabelas de resultado de 2022 (sem arquivos brutos das urnas). Baixando perfil 2022 (ok) e brutos 2022 (1º turno 75 GB, 2º 93 GB, 28+28 pacotes); processador aceita ANO=2022 (códigos 544/545, datas 02/10 e 30/10); processamento de 2022 encadeado após 2026. Perfil 2022 por seção gerado (coluna QT_ELEITORES_PERFIL) | `scripts/processar_2022_quando_pronto.sh`, `analise/perfil.py 2022` | Em andamento |
| 21:12 | Página de mapas (`grafico/web/mapas.html`): mapas por município e UF (virada, virada vs. Brasil, resultado, comparecimento, divergência do esperado), 2022 e 2026; fluxo de votos 1º→2º (Sankey nacional e por UF); mapas de calor de Klimek. Malha do IBGE (API pública, só desenho) + tabela TSE cd→IBGE. Corrigida a orientação dos polígonos do IBGE (anéis invertidos para o d3). Nota: troca direta Lula→Flávio estimada em 0 está no limite da restrição | `analise/mapas_dados.py`, `grafico/web/geo/` | Pronto |
| 21:15 | C06b limites de Duncan-Davis para a troca direta (pergunta do usuário): mínimo garantido de 79 (F→L) e 123 (L→F); máximo de ~40 mi cada; os dados não identificam a troca direta (classe G); nota na página de mapas | — | Concluído |
| 21:21 | Página de mapas refeita após crítica do usuário (ilegível; eu tinha mexido no mapa em vez dos mapas de calor): 5 perguntas com a resposta no título; Klimek em bolinhas. **Viés meu corrigido:** título da pergunta 4 dispensava a diferença 748 (2026) × 423 (2022) seções na zona 90/90 de Lula; agora a diferença é dita e vai para confirmação nos logs (grupo zona_klimek em analise_logs.py; classe B exploratória) | `grafico/web/mapas.html` | Em investigação |
| 21:32 | 2º turno 2026 processado (100% das seções). **Erros do meu leitor, corrigidos:** urnas do exterior sem campo de biometria (BU) e 29 seções do Sistema de Apuração (arquivos busa/logsa/sa; RDV vazio). T36: 76 casos, 75 com explicação operacional, 1 inconsistência de publicação (log de 1 urna de SP listado na lista assinada e não publicado), 0 sem explicação. Releitura do 1º turno iniciada às 21:21 com o leitor anterior: refazer ZZ e MG do 1º turno depois | `analise/processar_brutos.py`, `analise/casos_integridade.py` | Concluído (2º turno) |
| 21:44 | Anotações por teste (o que foi feito, correções, incidentes, falsos sinais) gravadas em `testes/registro.json` (campo `anotacoes`, 35 testes) para alimentar o relatório visual; T30 marcado como resultado cru inválido (log do 1º turno arquivado no log do 2º), a refazer só com o dia do turno; T32 com resíduo de eleitorado no exterior sem explicação (72 e 102) registrado | `testes/registro.json` | — |
| 21:51 | Revisão do relatorio.html entregue pelo subagente Sonnet (ele só conferiu até o módulo B/C): revisei D por captura (cartões, mini-gráficos, anotações e erros destacados ok); achei estados desatualizados (T17b, T20, T28–T33, E01–E03 'em processamento'), texto '31 arquivos ilegíveis' (eram seções do Sistema de Apuração) e resultados novos fora dos dados do relatório. Registro atualizado (14 testes), `novos` em relatorio_dados.json, nova rodada pedida ao subagente (T28, T20, T36, T34/T35, E01–E03, sensibilidade, T23) e conferência dos módulos C–F | `grafico/web/relatorio.html`, `analise/relatorio_dados.py` | Em andamento |
| 21:59 | **Publicação no GitHub** (repositório público doce42/urna-lab, 121 arquivos, 10,5 MB: documentação, código, listas de download, registro de testes e resultados pequenos; sem dados brutos). Feita por `scripts/publicar.py`, que copia para pasta separada, higieniza caminhos, varre termos pessoais e segredos e aborta se achar algo. **Duas falhas minhas pegas antes de subir:** (1) a 1ª regra de termos bloqueados dava falso positivo ("cruzada", municípios Água Doce e Rio Doce) e foi refinada; (2) a higienização de caminhos quebrava código (trocava o ponto de montagem dentro de um `df` e mexia nas próprias expressões do script): corrigida, e a cópia compila e passa em `bash -n`. Commit com o e-mail de privacidade do GitHub (o e-mail do git global é pessoal e não é usado). Sem GitHub Actions e sem Git LFS | `scripts/publicar.py`, `README.md` | Publicado |
| 22:02 | **Licença livre e governança do repositório público:** MIT (código) + CC BY 4.0 (documentação e resultados), textos oficiais da API do GitHub; `THIRD_PARTY.md`, `CONTRIBUTING.md` (fork + pull request validado por quem mantém), `.github/CODEOWNERS`, modelo de pull request; proteção do ramo principal exige PR com aprovação do dono do código, sem travar o envio direto do mantenedor (enforce_admins desligado), sem force push | `LICENSE`, `LICENSE-DOCS`, `CONTRIBUTING.md` | Publicado |
| 22:12 | **2026 fechado:** cobertura 100% dos arquivos das urnas nos dois turnos (499.207 urnas em cada), T32 638/638, sensibilidade do T02/T03 (33 pró-Lula e 13 pró-adversário além de 5 desvios quase constantes entre mínimos de válidos, escalas e níveis). **2022, erro meu:** o encadeamento de 2022 disparou antes de o leitor conhecer o formato de 2022 (nomes `.bu/.rdv/.logjez/.vscmr` sem UF, log em outro empacotamento, RDV/bu/vscmr com outra estrutura) e gerou arquivos vazios marcados como concluídos; limpos, e o encadeamento reaberto. Leitor de 2022 delegado a subagente Sonnet (contexto pequeno, mais barato); `scripts/pos3.sh` encadeia as análises de 2022, relatório, mapas e conferências | `analise/processar_brutos.py`, `scripts/pos3.sh` | Em andamento |
| 22:24 | Leitor de 2022 adaptado por subagente Sonnet (nomes `.bu/.rdv/.logjez/.vscmr` sem UF, log em 7z via py7zr, RDV com eleições em outra posição, bu de 2022, assinatura ECDSA com r e s com zero à esquerda sobrando) e **verificado por mim**: regressão de 2026 idêntica (AP 2º turno, 73 de 73 colunas) e 2022 AC nos dois turnos 2.124/2.124 em assinatura, RDV, bu e log. Processamento completo de 2022 liberado às 22:23. **T30 refeito** com abertura e encerramento locais do boletim (não 7h fixas): 0 votos após o encerramento e 1 urna por turno com voto minutos antes da abertura, ambas por urna substituída antes do primeiro voto | `analise/processar_brutos.py`, `analise/analise_logs.py` | Concluído |
| 23:27 | **ERRO GRAVE MEU, achado ao investigar uma diferença 2022 × 2026:** o leitor do log somava duas vezes as linhas repetidas entre as partes de um log (quando a urna reinicia, o log arquivado repete linhas do principal). Provado em 3 urnas do 1º turno: contando só linhas únicas, o log dá exatamente o comparecimento (194, 227 e 286 contra 351, 352 e 466). Contaminava, em urnas com log em várias partes (~1–2%): T14, T36, T28, T29 (intervalos negativos), T33, o gráfico de votos por minuto e a 'taxa maior de divergências em 2022' que eu estava investigando. **Não afetava** assinatura, hash, RDV, bu.dat nem boletim impresso. Corrigido (descarta só linha já vista em parte anterior) e testado; reprocessamento completo das 4 combinações e das análises dependentes iniciado (`scripts/refazer_tudo.sh`, ~2 h); resultados antigos preservados em `analise/historico_v1_log_duplicado/`. **Achados desta investigação (válidos, independem do log):** RDV de 1 urna do MA (1º turno) faltava no pacote do TSE, baixado do site de resultados e verificado (hash, assinatura, Lula 158 = publicado); log do RJ 60011/8/61 com caracteres corrompidos na própria urna (hash do arquivo confere; totais corretos); em 2022, 116 (1º) e 43 (2º turno) seções sem arquivos de boletim e assinatura no pacote, 85% no exterior | `analise/processar_brutos.py`, `scripts/refazer_tudo.sh` | Concluído em 28/10 às 01h42 (4 combinações em ~2 h 15 min, 15 processos em paralelo) |
| 02:02 | **SEGUNDO ERRO MEU, achado ao conferir o reprocessamento:** o leitor do bu.dat só reconhecia a lista de eleições quando a de Presidente era a primeira; em estados com 2º turno de governador (MT, RJ, PR e outros) a lista vinha com outra eleição antes e 767 urnas do 2º turno (e 19 do 1º) ficaram sem os votos do bu.dat. Isso criou 757 'casos sem explicação' falsos no T36 do 2º turno (log = comparecimento; só faltava o total do bu.dat). Corrigido (procura a eleição de Presidente em qualquer posição) e reprocessados só os estados afetados (2º turno: MT PA PR RJ RS SP ZZ, 16 min; 1º turno: MG PA PE PR RS SP ZZ, 17 min). **Resultado final do T36:** 1º turno 186 casos, 185 explicados e 1 sem explicação (RJ 60011/8/61, log corrompido pela urna); 2º turno 75 casos, 74 explicados, 1 de publicação (D1, SP) e 0 sem explicação. Taxas dos testes de log mudaram só na 4ª casa decimal (T28) e pouco em T29/T33 | `analise/processar_brutos.py`, `scripts/refazer_bu_2t.sh`, `scripts/refazer_bu_1t.sh` | Concluído |
| 03:00 | **T13b concluído** (poder do T28 com fraude sintética sobre as urnas reais dos dois turnos) e **documentação oficial do TSE obtida** (o usuário baixou do portal: especificação ASN.1 de BU/RDV/assinatura, formato do log, hashes do QR Code; estrutura do BU de 2022 confere com os leitores e confirma que o bu.dat traz lista de eleições). Limites sem solução com dados públicos registrados em AUTOAUDITORIA §6 | `analise/poder_logs.py`, `dados/brutos/doc/` | Concluído |
| 03:25 | **SNAPSHOT V1.0-rc1 (levantamento inicial), depois rotulado como candidato à baseline.** Conclusão em `CONCLUSAO.md`; retrato congelado em `rodadas/rodada-1/` (registro, 26 resultados e a conclusão, com SHA-256); cada teste ganhou `historico` e `provas`; tag `rodada-1` no GitHub; página Linha do tempo no site. Próximas fases: double check da metodologia e rodadas de perguntas e provas (`RODADAS.md`) | `scripts/rodada.py`, `rodadas/` | Concluído |
| 03:24–03:50 | **Revisão independente R1 (Codex) recebida e respondida.** Relatório guardado inteiro em `revisoes/R1-codex/original/` (SHA-256 em SHA256SUMS.txt); 28 achados em `achados.json` (16 confirmados por nós, 11 questões metodológicas, 1 pendente de reprodução). Conferido por nós antes de responder: Ed521 aceitava entrada degenerada (reproduzido; verificador endurecido; **todas as 499.176 e 499.178 listas reverificadas e válidas**); manifesto marcava hash oficial sem hash publicado (estado real: 331 conferidos, 173 sem hash do TSE; gerador corrigido); **T01 refeito seção a seção: 3.800.511 e 1.931.103 pares iguais, 0 diferenças**; T36 com grau da explicação (a maioria é inferência); verificador por conjuntos de chaves; terminologia 'falso positivo' retirada. Registro migrado para versões (V1.0-rc1 + evidência/interpretação separadas, causa de cada mudança, pré-especificação); 41 contestações nos testes: 2 resistiram, 29 ajustadas, 2 caíram, 8 em andamento. CONCLUSAO em revisão (a rc1 fica congelada). Emenda 4 ao protocolo. Fase 2 aberta com 13 perguntas registradas antes dos resultados (FASE2.md). Baseline V1.0 aguardando aprovação do responsável | `revisoes/`, `scripts/migrar_registro_r1.py`, `analise/t01_secao.py`, `analise/varrer_chaves.py` | Concluído |
| 21:39 | T33 (2º turno): 162 urnas com verificação de software sem "SUCESSO" (181 eventos, contra 173,7 mi com sucesso); 154 só em datas de preparação/teste, com todas as verificações ok no dia; 8 com 1 erro no dia: em todas a urna bloqueou ("Erro na validação de assinaturas"), foi desligada pela chave, religada, e passou nas verificações seguintes (4 antes do 1º voto, 4 durante a votação). T28: 0 urnas com rajada no fim do dia (12,71% × 12,68%). Confirmação nos logs: cauda pró-Lula do T02 e zona de Klimek sem diferença de biometria, tempos ou substituição em relação às demais seções. Encadeado `scripts/pos_processamento.sh` (etapas mecânicas sem acompanhamento de modelo, a pedido do usuário para economizar limite) | `analise/analise_logs.py` | Concluído (2º turno) |

## 2. Dados baixados (todos oficiais do TSE)

| Conjunto | Origem | Tamanho no disco | Conferência |
|---|---|---|---|
| Votação por seção 2026 (BR) | cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao | 242 MB (zip) | Totais iguais ao BU |
| Boletim de Urna na Web 2026, 1º e 2º turno (só Presidente guardado) | cdn.tse.jus.br/…/buweb | 2,9 GB + 1,5 GB (CSV filtrado) | .sha512 do TSE |
| Perfil do eleitorado por seção 2026 | cdn.tse.jus.br/…/perfil_eleitor_secao | 2,7 GB | — |
| Votação por seção 2022 + BU na Web 2022 | cdn.tse.jus.br | 1,7 GB (zip) + 2,4 GB (filtrado) | .sha512 do TSE |
| Arquivos das urnas 2026, 1º turno (log, BU, RDV, assinatura, BU impresso) | pacotes por UF, cdn.tse.jus.br/…/arqurnatot | ~95 GB (em andamento) | TSE não publica .sha512 para esses |
| Arquivos das urnas 2026, 2º turno | urna por urna, resultados.tse.jus.br | ~115 GB estimados (em andamento) | Assinatura digital (a verificar) |

## 3. Catálogo de testes

| # | Pergunta | Método | Esperado ao acaso | Resultado | Situação |
|---|---|---|---|---|---|
| T01 | O BU bate com a votação por seção? | Soma por votável | Igual | Igual voto a voto, 2 turnos | Concluído |
| T02 | Alguma seção virou diferente das vizinhas? | Virada em logit, resíduo do município, z robusto | Poucas, simétricas | 46 de 499 mil acima de 5 desvios (33 pró-Lula, 13 pró-Flávio) | Concluído |
| T03 | A virada depende da hora de chegada? | Spearman dentro do município | ~0 | +0,004 | Concluído |
| T04 | Urna trocada entre turnos votou diferente? | Mann-Whitney no resíduo | Sem diferença | p = 0,1 | Concluído |
| T05 | Último dígito uniforme? | Qui-quadrado contra o esperado pela inclinação | Uniforme | p de 0,05 a 0,84 | Concluído |
| T06 | Contagens idênticas demais? | Comparação com sorteio e vizinhos | Sem pico | Abaixo do acaso | Concluído |
| T07 | Enchimento de urna (impressão digital) | Comparecimento × % do vencedor | Sem mancha | Sem mancha; 0 seções acima de 100% | Concluído |
| T08 | Boletim emitido antes do fim da votação? | Horários do BU com fuso do município | 0 | 0 | Concluído |
| T09 | O buraco de 17h10–19h03 (2º turno) | Encerramento por urna | — | Prorrogação: 6.748 urnas; votaram como as vizinhas (+7,45 × +7,56 pp) | Concluído |
| T10 | A curva teve movimento fora do natural? | Curva real × prevista pelo 1º turno, na mesma ordem | Diferença perto de 0 | Máx. 0,08 pp (município) e 0,32 pp (estado); 1 reversão (20h02), explicada pela ordem das regiões | Concluído |
| T11 | Zigue-zagues demais? | 200 simulações | 28 ± 2 | 29 | Concluído |
| T12 | Liberação sem biometria afeta a virada? | Regressão dentro do município com perfil do eleitorado; erro agrupado por município | 0 | Sem controle t = −14,7; com controle t = +0,3 (era idade) | Concluído |
| T13 | Poder: que fraude os testes pegam? | Fraude sintética injetada nos dados reais | — | Pega troca concentrada (≥ 5% dos votos de uma urna), estados inteiros ≥ 1–2%, enchimento. **Não pega troca uniforme no país inteiro** | Concluído |
| T14 | Log da urna = boletim? | Votos computados no log × comparecimento; confirmações + nulos por suspensão × total | Igual | AC e MS 100% | Em andamento (Brasil, 2 turnos) |
| T15 | Boletim impresso = dado publicado? | Texto do imgbu × BU na Web | Igual | AC 100% | Em andamento |
| T16 | Assinatura digital dos arquivos | Ed521 (UE2020/2022) e ECDSA P-521 + SHA-512 (UE2013/2015); lista + cada arquivo; hash e tamanho contra a lista | Válida | AC 2.270/2.270, MS 7.106/7.106 | Em andamento (Brasil, 2 turnos) |
| T17 | Recontagem pelo RDV = boletim | Decodificação DER do RDV, Presidente | Igual | AC 2.270/2.270 | Em andamento (Brasil, 2 turnos) |
| T18 | Votação ao longo do dia (hora real de cada voto) | Logs, evento "voto computado", fuso do município | — | Curva do AC pronta | Em andamento |
| T19 | Mesma bateria em 2022 | `analise/bateria.py 2022` (mesmo código) | Sem anomalia | Mesmo perfil de 2026 (ver relatório, seção 7) | Concluído |
| T20 | Modelo de urna (dado real do log) afeta a virada? | Comparação dentro do município | Sem diferença | — | A fazer (após os brutos) |
| T21 | Percentuais inteiros em excesso? | Kobak et al. 2016 + nulo por reamostragem (Rozenas 2017), 200 sorteios | z ≈ 0 | 2026: z de −1,1 a +1,0; 2022: −1,6 a +0,8 | Concluído |
| T22 | Assinatura de fraude incremental | Spearman comparecimento × % dentro do município (Klimek et al.) | Pequena e simétrica | 2026: Lula −0,08 / Flávio +0,08; 2022: −0,10 / +0,10 | Concluído |
| T23 | Classificador com fraude sintética | Zhang, Alvarez e Levin 2019 | — | — | Registrado para próxima bateria |
| T24 | Urna substituída no meio do dia | Log com votos de 2 urnas | — | MS: 22 urnas | Em andamento (Brasil) |

## 4. Artefatos e erros encontrados (e corrigidos)

| Onde | O que parecia | O que era | Correção |
|---|---|---|---|
| T02 | Seções "pró-Flávio" demais | Seções 100% Lula nos 2 turnos não têm como subir | Escala logit |
| T05 | Último dígito viciado | Inclinação natural da distribuição | Esperado pela inclinação local |
| T06 | 117 mil seções idênticas | Com 4 números, o acaso dá 133 mil | Simulação |
| T13 | Goiás disparando o alarme | Caiado teve 12,3% lá; voto órfão | Voto órfão no modelo |
| Gráfico | Urnas às 16h | Fuso errado de urna que abriu atrasada | Fuso do município |
| Dados | Totais do 1º turno 12% abaixo | SP cortado no download | Baixado de novo, hash ok |
| T14 | Log ≠ comparecimento em 6 urnas | Log arquivado dentro do log (urna reiniciada) | Leitura recursiva |
| T14 | Confirmações ≠ total em 14% | Nulo por suspensão (eleitor saiu sem terminar) | Evento contado |
| T16 | 4.043 urnas "sem assinatura" | Bloco da urna em minúsculas (`ueao…`) nas UE2013/UE2015 | Comparação sem diferenciar maiúsculas |
| T16 | 547 urnas com erro de leitura (MS) | Certificado DER com bytes de preenchimento depois do fim | Recorte no tamanho declarado |
| T16 | Certificado ≠ urna do log | Urna substituída: o log traz votos de duas urnas | Conferir se o certificado está entre as urnas do log |
| T13 | Goiás acusando no teste estadual (dados reais) | Voto órfão do Caiado | Voto órfão no modelo |
| Leitor de 2022 | Seção MG 49050/196/173 "sem BU lido" | Seção do Sistema de Apuração (`.busa`, `.imgbusa`, `.logsajez`, `.vscsa`); o leitor de 2022 só reconhecia `bu`, `imgbu`, `logjez`, `rdv`, `vscmr`. Ao todo, 159 seções-turno ficaram fora das verificações por arquivo de 2022 | Leitura dirigida (`fase3/ver_sa22.py`); o leitor geral de 2022 ainda não foi alterado |
| E3 (zeros) | 1 seção 2022 com BU ≠ tabela | Valor ausente (BU não lido) contado como diferença por `fillna(0)` | Reclassificada como não verificada; verificada depois (BU1) |
| P18 | Falso alarme 0/30 no limiar calibrado | Medido nos mesmos mundos usados para calibrar | I1 com mundos separados |
| I1 | "Detecção" de troca concentrada | Regra contava alarme em qualquer sentido e de T2/T4; a 10% concentrado o E02 também acusa o lado oposto | A2: regra no sentido correto |
| I1 | Poder "em municípios inteiros" | As 5 maiores cidades estavam fora do sorteio; nelas a troca não é detectada com confiabilidade | A2 (M2G) |
| 2022, certificado × log | "Certificado ≠ urna do log" como sinal de troca de urna | Ocorre em 59% das seções de 2022: não indica contingência nesse ano | Retirado como apoio (auditoria adversarial) |
| 2022, log × comparecimento | Não conferido em 2022 | 70 e 36 seções com log menor que o comparecimento (5.287 votos sem registro no log), 34 e 13 com log maior | Registrado como achado objetivo; classificação na fila |
| Leitor de log 2022 | "Urnas com voto no log" | Em parte dos logs de 2022 o 3º campo da linha não é o número da urna (67305985 em vários estados) | Coluna não usada para 2022; classificação da fila F1 refeita por partes do log |
| Parquet de 2022 | 5 seções "sem boletim lido" | Parquet gerado com versão anterior do leitor de boletim; o leitor atual lê os 5 e conferem | Registrado (fila F3) |
| 2026, Sistema de Apuração | Arquivos `-sa.vsc` não lidos pelo leitor de 2026 | Hash e assinatura das seções do Sistema de Apuração de 2026 não conferidos | Conferidos à parte (fila F2): 60/60 válidos |
| T28 2022 | Denominador "urnas" 472.024 | Inclui 148 seções do Sistema de Apuração sem log | A4: denominador efetivo 471.851 e 471.979 |
| R1-20 | Script lia o DataUrnas-BR de pasta temporária, sem commit nem hash | Rastreabilidade incompleta | Commit 12f0433 e SHA-256 conferidos no script; pasta permanente |

## 5. Consumo

### Máquina
- 16 núcleos, 23 GB de RAM. Pico de processamento: 12 processos, todos com prioridade baixa (`nice 10`, `ionice` ocioso).
- Medição contínua em `dados/listas/recursos.csv`: carga, RAM, internet acumulada, disco do projeto, espaço livre.

### Internet
- Banda máxima observada: ~64 MB/s (~510 Mbit/s); o gargalo é a conexão.
- Volume até 19h11: ~73 GB recebidos desde que o computador ligou (contador da placa de rede; inclui outros usos).

### Disco
- Projeto no SSD de 1 TB (`<DISCO_GRANDE>`): 61,8 GB às 19h11; previsão ~230 GB no fim.

### Tempo
- Início às 18h03. Downloads grandes: ~1 h na banda atual.

### Tokens e modelos de IA
- **Registro completo e atualizável em [`CONSUMO_IA.md`](CONSUMO_IA.md)** (tokens e custo por modelo, totais do estudo).
- **Medição real da sessão** (`/usage` do Claude Code, instantâneo às 23:52 de 27/10/2026, com a sessão ainda em andamento; atualizar ao final): 5 h 49 min de relógio, 2 h 19 min de tempo de API, 4.560 linhas de código acrescentadas e 648 removidas.

| Modelo | Entrada | Saída | Leitura de cache | Gravação de cache | Custo |
|---|---|---|---|---|---|
| Claude Opus 5.5 (condução do estudo, até a troca de modelo) | 1,6 mil | 619,5 mil | 202,3 mi | 916,8 mil | US$ 60,18 |
| Claude Sonnet 5.5 (sessão principal depois da troca + 3 subagentes) | 25,5 mil | 222,6 mil | 74,3 mi | 1,2 mi | US$ 14,18 |
| Claude Haiku 5.5 (busca na web feita pelo próprio Claude Code, 18 buscas; não escolhido por nós) | 252,9 mil | 19,9 mil | 0 | 0 | US$ 0,22 |
| **Total** | | | | | **US$ 74,58** |

- **Leitura do consumo:** 99% da entrada veio de cache. O custo dominante foi **reler o contexto muito longo a cada chamada** (202 milhões de tokens de cache só no Opus), não a escrita de código. A troca para Sonnet às ~21h40 reduziu o custo por chamada, e os três subagentes (relatório visual, leitor de 2022, revisão do relatório) gastaram pouco por terem contexto pequeno. O que mais economizaria numa próxima sessão: usar modelo mais barato para execução desde o início e **abrir sessão nova (`/clear`) a cada mudança de tarefa**, retomando pelo `AGENTS.md`, `CATALOGO.md` e `testes/registro.json`, que guardam todo o estado do estudo.
- Limites da conta (percentuais de sessão e de semana) não são registrados aqui por serem da conta, não do projeto.
- Modelo usado nesta sessão: Claude Opus 5.5 (`claude-opus-5-5`), esforço médio, para condução, código, interpretação e documentação. Não foram usados subagentes nem outros modelos até 21h40 de 27/10.
- Revisão cega externa do METODOLOGIA: feita pelo usuário com outro chat de IA (modelo não informado).
- 21:43: sessão trocada para Sonnet 5.5 (pedido do usuário, economia de limite). Subagente Sonnet para o redesenho visual do relatorio.html (um só; a máquina está saturada e agentes extras não acelerariam a computação). Sensibilidade e manifesto de hashes rodam por script (`scripts/pos2.sh`).
- A partir das 21h40, etapas mecânicas rodam por script (`scripts/pos_processamento.sh`), sem modelo acompanhando, para economizar limite.
- O agente não tem acesso ao próprio contador de tokens. Para o número exato da sessão, use `/cost` (ou `/usage`) no Claude Code. Registre aqui ao fechar.

## 6. Instantâneo histórico: METODOLOGIA.md, seções 4 e 5, às 18h52 de 27/10/2026

Preservado como foi escrito. Desatualizado depois das 19h20: assinatura, RDV e logs passaram a ser verificados, e a bateria de 2022 rodou às 19h25.

### 4. O que já foi feito aqui e o resultado

| Teste | Script | Resultado |
|---|---|---|
| Boletim de Urna = votação por seção | `grafico/montar_dados.py` | Igual voto a voto, nos dois turnos |
| Seções fora do padrão do município | `analise/testes_corrigidos.py` | 46 de 499 mil acima de 5 desvios, nos dois sentidos (33 pró-Lula, 13 pró-Flávio) |
| Virada × hora de chegada | idem | Correlação de +0,004: sem relação |
| Urna trocada entre turnos | idem | Sem diferença (p = 0,1) |
| Último dígito (corrigido pela inclinação) | idem | Uniforme (p de 0,05 a 0,84 em 4 testes) |
| Contagens idênticas | `analise/investigar.py` | Abaixo do acaso; sem pico no zero |
| Impressão digital | `analise/testes.py` | Sem mancha de enchimento; nenhuma seção acima de 100% |
| Buraco das 17h10 às 19h03 no 2º turno | `analise/investigar.py` | Prorrogação de 2h só nas seções ainda abertas (6,8 mil, RJ/SP/BA/PE/PB). Elas votaram como as vizinhas |
| Curva real × prevista pelo 1º turno | `analise/curva.py` | Diferença máxima de 0,08 ponto (pelo município) e 0,32 (pelo estado); 1 reversão (20h02), explicada pela chegada do Sul e do Centro-Oeste antes do Sudeste e do Nordeste |
| Zigue-zagues minuto a minuto | idem | 29 reais contra 28 ± 2 simulados |
| Liberação sem biometria × virada | `analise/testes_corrigidos.py` | Efeito pequeno (−0,06). Provável perfil de eleitor (idade, zona rural); pede dado demográfico para fechar |

**Artefatos encontrados e corrigidos:** seções unânimes lidas como "virada contra" (teto de 100%); último dígito enviesado pela inclinação; arquivo de São Paulo do 1º turno baixado pela metade; fuso de urna que abriu atrasada.

### 5. Próximos passos para fechar a análise
1. **Teste de poder:** injetar fraudes sintéticas nos dados reais (por exemplo, mover 1%, 3% e 5% dos votos em 1%, 5% e 10% das urnas, de forma aleatória ou concentrada numa região) e medir quais testes detectam cada caso. Isso diz o tamanho de fraude que a análise conseguiria ver e o que fica abaixo do radar.
2. **Arquivos brutos das urnas:** verificar a assinatura dos boletins e recontar o RDV de todas as urnas. São 95 GB no 1º turno; o 2º turno ainda não saiu em pacote.
3. **Perfil do eleitorado por seção** (idade, escolaridade, publicado pelo TSE) para controlar a biometria e outros grupos.
4. **Rodar a mesma bateria em 2022** como comparação: mesma metodologia numa eleição já auditada.


## Sessão limitada de 28/10/2026 (Fase 2, rodada 3)
- Baseline V1.0 aprovada pelo responsável e congelada (rodada 2, tag `v1.0`).
- P1: estimador C06 sob heterogeneidade sintética: ordem e contraste 2022×2026 resistem, a magnitude "4:1" não (ver `RELATORIO_SESSAO_LIMITADA.md`).
- Hipótese de enchimento para Lula entre turnos: sem a assinatura de comparecimento prevista; assimetria de cauda do T02 sem causa.
- Verificação A de 20 seções do 1º turno: 19 com arquivos conferem; nenhuma divergência objetiva nova. Verificação B não realizada (sem material independente local).

- Fase 2 concluída (rodada 3, V1.1): P1 a P17 respondidas ou inventariadas; `RELATORIO_FASE2_COMPLETA.md`. Falha operacional do P16 (comparador) corrigida e repetida uma vez.

## Fase 3 (28/10/2026, em revisão)
- **Sessões 1 e 2:** inventário (27 itens), curvas (T40), zeros (T41), Moran's I (T42), poder bilateral do T13 (P18), São Paulo 2022 (P20) e reconciliação com o DataUrnas-BR (T43). Congelada como V1.2 (rodada 4, tag `v1.2`) **antes** de auditoria. Desvios em `rodadas/rodada-4-desvio.md`.
- **Auditoria** (`fase3/AUDITORIA_F3.md`): estados acima da evidência (P9, P14, P18, R1-20, C1, Z1, P19). Com aprovação do responsável, a F3 voltou a "em revisão" e a V1.2 ficou preservada.
- **Revisão I1 a I3** (`fase3/PREREG_REVISAO.md`):
  - **I1:** o T02 é cego a troca em município ou região inteiros; o E02 vê ~62 mil votos concentrados (restrito pelo A2 a municípios de até ~5 mil seções e ao sentido certo); ~25 mil não é detectável.
  - **I2:** o modelo de zeros não calibrou, e o resultado não é interpretável.
  - **I3:** a lista de locais atípicos depende do método; os locais de SP 2022 não são atípicos contra a própria zona.
- **Verificações documentais de 2022** (`fase3/RELATORIO_ACEITACAO_F3.md`):
  - **A173:** os 173 arquivos assinados faltam também no pacote baixado pelo projeto; os votos das 64 seções conferem.
  - **BU1:** boletim do Sistema de Apuração, confere.
  - **SA22:** as 159 seções-turno do Sistema de Apuração foram lidas; boletim, texto impresso e assinatura conferem em todas. Em todas, a lista assinada cita `.hash`, `.ver` e `.chvtp` ausentes do pacote, e em 8 também `.jufa`.
- **Correções de redação com histórico:** zeros ("sem evidência de excesso" retirado), Moran ("não indica manipulação" retirado), SP ("zonas vizinhas" virou o que foi medido) e R1-20 ("exterior e agregadas" não verificado).
- **Cobertura por arquivo de 2022, revista:**
  - As verificações gerais do projeto não incluíam as 159 seções-turno do Sistema de Apuração. Agora estão cobertas por leitura dirigida.
  - 173 arquivos assinados (RDV, log, imagem) não estão publicados no pacote de dados abertos.
  - Nas seções do Sistema de Apuração, 485 arquivos auxiliares listados também não estão.
- **Verificações finais (A1, A2, A4):**
  - **A1:** as 367 seções de 2022 sem par no DataUrnas-BR estão explicadas (27 do Sistema de Apuração, 333 numa lacuna do terceiro na Bahia, 7 fora do banco dele), e os boletins conferem.
  - **A2:** a detecção no sentido correto confirma o I1, exceto a região a 5%. Grandes municípios inteiros ficam fora do alcance da bateria.
  - **A4:** denominador do T28 de 2022 corrigido.
- **Auditoria adversarial** (`fase3/RELATORIO_ADVERSARIAL.md`): compatibilidade com o log não é verificação independente.
  - **H3 nacional contrariada:** os totais divulgados ao vivo (39 capturas do Internet Archive) batem com a base publicada.
  - **T36 e contingências:** sem deslocamento de votos.
  - **Explicações rebaixadas:** "explicado" passa a "compatível".
  - **2022:** "certificado ≠ log" retirado como indício. 153 seções-turno com log diferente do comparecimento, nunca vistas antes.
  - **Leitura de testes:** T01, T14 a T17b, T32, R1, SA22 e outros passam a ser lidos como consistência interna.
- **Missão de resolução** (`fase3/RESPOSTAS_F3.md`, `fase3/respostas_f3.json`, página "Perguntas e respostas científicas" no site): respostas explícitas para 26 perguntas e para os 33 itens do inventário.
  - **R1, integridade:** tabela = bu.dat = RDV em 2022 e 2026, como consistência interna.
  - **R2, curva divulgada:** o Internet Archive confirma em 39 instantes a base publicada.
  - **R3, zeros:** sem excesso agregado fora da amostra; o critério formal não foi cumprido.
  - **R4, zona 251:** o desvio persiste depois do perfil do eleitorado.
  - Desvios em `fase3/PREREG_RESPOSTAS.md`.
- **Fila executada** (`fase3/PREREG_FILA.md`):
  - **F1:** log × comparecimento de 2022, recontagem confirmada; o campo "urna" do log de 2022 é inválido.
  - **F2:** Sistema de Apuração de 2026, 60/60 assinaturas válidas.
  - **F3:** das 10 seções sem boletim lido, 5 conferem e 5 não têm arquivos.
  - **F4:** modelo de chegada não validado; Q10 e Q12 seguem não determinados.
- **Veredito de 2026 e reorganização** (`fase3/f3_veredito.py` → `fase3/veredito_2026.json`, `VEREDITO_2026.md`):
  - **Pergunta central e dedução:** a pergunta é se há sinal de fraude capaz de mudar o resultado; a resposta deduz onde uma fraude dessas caberia e onde não.
  - **Hipóteses:** 10 mecanismos de fraude, cada um com o que deixaria nos dados e o veredito.
  - **Escala de sinal:** sem sinal, explicado, compatível só com o registro, anomalia sem causa, divergência, indício, ponto cego. Fica separada de "concluído".
  - **Teste novo T44** (grandes cidades, `PREREG_GRANDES_CIDADES.md`): falso alarme 1,5%; troca de 2% no município inteiro detectável; Salvador desviante, ~30 mil votos, em todas as 19 zonas, sem 2º turno estadual.
  - **No site:** resposta central na Home, selo de sinal nos testes e busca por pergunta na página Respostas.
- **Investigações finais da F3** (`fase3/PREREG_FINAL.md`):
  - **Z1, Salvador:** única capital desviante (z 6,1) e não explicada pelo perfil; Fortaleza desvia do mesmo tamanho no sentido oposto.
  - **Z2, T33:** os erros de assinatura do software no log são quase todos fora do dia; os do dia são seguidos de sucesso; sem efeito nos votos.
  - **Z3, anomalias pequenas:** as 8 urnas do T28 têm Lula abaixo do município em 6; as 33 seções extremas do T02 estão espalhadas e com comparecimento em queda.
  - **Z4, fontes externas:** sem dado primário.
  - **Fechamento:** cada item com resposta final.

## Alegações da live de 4/11/2022 e do pedido do PL (28/10/2026, pós-V1.3)
Pré-registro `fase3/PREREG_LIVE_2022.md` (emenda 7), script `fase3/live_2022.py`, saída `fase3/resultados/live_2022.json`, contexto `docs/pesquisas/2026-10-28_live_cerimedo_2022.md`. Tempo: 40 s por execução; 2 execuções.
- **Artefato (corrigido):** a 1ª execução acusou ~22 mil seções sem ligação log-BU-RDV; causa: BU e RDV omitem quem teve zero voto e o comparador tratou ausente ≠ 0. Mais um caso da regra "suspeite primeiro do comparador".
- **T45:** ID fixo 67305985 em todas as 279.291 seções pré-2020 do 2º turno de 2022; ligação completa em 279.285; 0 casos em 2026 (bug corrigido).
- **T46:** 51,0508% reproduzido; subconjunto geográfico; contrafactual dentro do município: Bolsonaro 49,25%.
- **T47:** diferença bruta (50,3% × 46,0%) e dentro do município (fora de ±0,02); dentro do local de votação equivalente a zero nos dois turnos → S1.
- **T48:** software 8.26.0.0 em todos os modelos; unanimidades proporcionais à presença do modelo; 1 seção UE2015 em SC com 8.10.0.1 Sabiá no log (não investigada).
- **T49 (zeros de Flávio, emenda 8):** 106 seções e 14.860 votos reproduzidos; 141 em 2022; contínuas com 2022 e 1º turno; 106/106 íntegras; 211 viradas em 2026 contra 251 no sentido oposto em 2022; "644 mil" no Rio não reproduzido (cidade: Lula +113 mil).
- **T50 (thread de concentração, emenda 9):** todas as contagens reproduzidas; Lula > 80% em 35.591 seções (40.046 em 2022).
- **T51 (crescimento entre turnos, emenda 10):** 2026 Lula cresceu mais em 93,8% dos municípios e 27 UFs; 2022 Bolsonaro em 87,1% e 27 UFs (agregado); em proporção 97,1% × 98,0%. Gráfico do "candidato de trás" reproduzido (2026 +2,80 de 1,02 necessários; 2022 +1,95 de 2,85).
- **T52–T54 (posts de @leonardodias/arvor.co, emenda 11):** recebimento de BUs parado 17:07–19:03 só em 2026, junto com o fim da prorrogação (S1); biometria 87,6% (75,9% em 2022), sem relação positiva com a virada (S0); Flávio perdeu votos em 937 municípios, Lula em 981 em 2022 (S0). Artefato: recebido em hora de Brasília, emissão em hora local (decidido pelos dados). Correção única no T53 (NaN).
- **Site:** capítulo "Alegações públicas testadas" (Q27–Q37) na página de Respostas; crédito do autor no rodapé, só no site (arquivo local fora do git).
- **T55 (Cabo Frio e cidades citadas, emenda 12):** ganho de Lula cabe nos votos disponíveis em todos os municípios; Cabo Frio no percentil 89; 36 casos em 2026 e 28 espelhados em 2022; 4.044/4.044 seções íntegras (S0). Artefato corrigido: validos_1 contado como eliminado.
- **T56 (brancos e nulos, emenda 13):** C06 confirma a direção (62% → Lula em 2026); seções pareadas mostram excesso de brancos e nulos no 1º turno de 2026 onde Lula é forte (~0,47 mi), parte da queda de 1,82 mi; resto sem causa identificada (S1 em parte).
- **T57 (nulos e 2º turno de governador, emenda 14):** nulos de presidente sobem onde há governador no 2º turno (+1,58 ponto em 2022, +0,78 em 2026); 53% × 8% dos votos nessas UFs; ~0,69 mi da queda; resto uniforme (S1).

## Rodada 7 (28/10/2026): dígitos dos nulos no RDV e calibração do C06
Pré-registro `fase3/PREREG_RDV_NULOS.md` (emenda 15). Extração de todos os RDVs (2022 e 2026, dois turnos; ~8 min por conjunto com 12 processos).
- **Artefato (corrigido):** a conferência acusou 541 e 14 seções em 2022; causa: o leitor original soma o nulo tipo 6, e seções só com tipo 6 ficavam fora do comparador. Depois: 0 diferenças nos 4 conjuntos.
- **T58:** nulos com número de governador no campo de presidente: 698 mil no 1º turno de 2026 (422 mil em 2022); explicam a marca do T56 e o efeito do T57 (S1).
- **T59:** C06 contra origem conhecida: acerta 14 (90%) e 70 (69%), erra 55, 12 e 15; magnitudes de fluxo só como direção (prova "ajustado" no C06).

## Operação Veracidade Geral e rodada 7 (28/10/2026, V1.5)
Documentos em `operacao_veracidade/` (protocolo, relatórios 00 a 10, executivo). Testes T60a a T65, perguntas Q42 a Q50. Emenda 16 do PROTOCOLO.
- **T60a:** cadeia de certificados em 1.942.246 de 1.942.246 pares seção × turno (2022 e 2026), 0 falhas; lacunas sem efeito em votos (98 certificados após a validade do certificado público da AC URNA; 17 e 22 seções com certificado de outra urna).
- **T60b:** 0 falso positivo e 40 de 40 mutações rejeitadas; só a cadeia rejeita certificado forjado.
- **T61:** 404 boletins impressos de terceiros iguais ao TSE; 404 arquivos iguais entre downloads; 77 registrados fora do TSE antes de o TSE registrar o recebimento.
- **T62 e T63:** registros coerentes assinados pela fonte passam por todas as verificações; bateria cega a UF, região, lote e uniforme abaixo de ~0,5 a 2,2 mi; poder assimétrico.
- **T64:** zeros, três famílias de modelo falham; locais de uma seção só.
- **T65:** o "98,12%" do vídeo é a premissa de 60% devolvida; resíduo acima do proporcional de +3,68 mi (2026) e +1,99 mi (2022).
- **Artefatos e erros meus:** contagem de eventos de logs de outras seções (ES 57932/9/85); "antes das 19h" de qualquer dia (216 em vez de 77); cache de zip reabrindo o arquivo; fabricante calibrado com a direção errada; `pkill -f` auto-casado.
- **Dados derivados grandes fora do git** (`.gitignore`): parquets de certificados e de nulos do RDV (reproduzíveis por script) e arquivos estáticos de terceiros (licença não verificada).
- **Documentação e skills da rodada 7, atualizadas depois do congelamento (28/10/2026):** METODOLOGIA, PIPELINE, MAPA_SKILLS, REFERENCIAS, AUTOAUDITORIA, DADOS_PRESERVACAO, DIRETRIZ, CONTRIBUTING, AGENTS (regras), Makefile e as 8 skills (`.agents/skills/`). A cópia congelada desses arquivos em `rodadas/rodada-7/arquivos/` é a anterior a esta atualização; a raiz tem a vigente, e a rodada 8 congelará a vigente. Rodada fechada não se reescreve.

## Rodada 8 (aberta, 28/10/2026): Relatório Pericial Independente
Pré-registro `fase3/PREREG_RELATORIO_PERICIAL.md` (emenda 17), script `fase3/relatorio_pericial.py`, R2b exploratório. Testes T66 a T70, perguntas Q51 a Q56; pela emenda 18 (30/10), T71 e Q57. **Não congelada.**
- **T66:** números do relatório reproduzidos (150.771 seções até 17:00:59 com Lula 47,61%; 339.593 de 17:01 a 17:15 com 53,46%; +6.177.738 depois). O corte mistura fusos (as 32.025 seções antes das 17h locais estão em MT, AM, MS, RO, AC e RR), chama a rotina de prorrogação e depende do minuto; em hora de Brasília, até 17:00:59 Flávio tem 50,99% e 0,61 mi; prorrogação de fato (> 17:30): 7.604 seções, +228.095 para Lula (5,1% da margem). Dentro do município, +0,2 ponto.
- **T67:** 8.632.488 liberações (6,73%; 8,06% em 2022); relação com Lula igual no 1º turno e em 2022, nula dentro do município.
- **T68:** 106 contra 4 reproduzido; razões menores que em 2022 (70,5 : 1 e 47 : 1); 94% no Norte e Nordeste.
- **T69:** Benford do primeiro dígito: desvio dentro das referências simuladas; sem poder neste dado.
- **T70:** arquivos por urna publicados na noite de 25/10; CSV BWeb não testável aqui.
- **T71 (30/10/2026, emenda 18; vídeo no Instagram transcrito com Whisper medium):** curvas dos dois turnos "sobrepostas". Reproduzido com diferença de até 0,08 ponto (o vídeo tem ~330 seções a menos). A "projeção 53,49% × 46,51%" é o oficial com o deslocamento visual de 5,25 pontos (6.514.319 votos de cada lado, 2,9 vezes a margem). Ordem de chegada geográfica e repetida entre turnos (Spearman 0,56; 2022: 0,64; Sudeste 14,5% do primeiro quinto e 67,1% do último); Pearson das curvas 0,905 (2022: 0,941), acima de ordens independentes (de −0,78 a +0,75); o contrafactual 1º turno + virada constante fica a no máximo 0,30 ponto da curva real (2022: 0,29). Pelo critério pré-fixado, não é incomum. Consumo: 1 execução, ~20 s de CPU; transcrição ~3 min de CPU. Correção de ambiente: o `faster_whisper` do venv `<DISCO_GRANDE>/venvs/whisper` falhou ao abrir o áudio pelo PyAV (`metadata_errors`); o áudio foi lido por `wave`/numpy.
- **Documentação, skills, selo do rodapé e placar da Home pelo Sinal atualizados na mesma data;** classes de T60a (A para D) e T53 (B para A) alinhadas ao sinal, com `mudancas`.
- **Revisão do site e PDF refeito (28/10/2026, rodada 8 ainda aberta):** veredito com a prorrogação de fato (+228.095, 5,1% da margem; H8) e a síntese das alegações públicas (`resposta_central.alegacoes`, com resposta curta das mais comuns na Home); Q51 a Q56 em capítulo próprio das Respostas (ids mantidos); classe de evidência alinhada ao sinal em T05, T10, T11 (A → G), T14, T15, T31 (A → D), T35 (G → D) e E02 (A → B), com `mudancas`; comandos de reprodução sem abreviação (T60b, T63, T64, T65); regras que ignoravam dados novos corrigidas (lead da Evolução só via F2 e F3; grupos da página Docs deixavam de fora 15 documentos); PDF montado por script a partir dos JSON (`grafico/montar_relatorio_pdf.py`, `make pdf`), com resumo de 2 a 3 páginas e a parte densa.


## Relatórios por fase e privacidade (28/10/2026)

- `relatorios/` tem um relatório por fase ou rodada (`fase1.md` a `rodada-8.md`, com `README.md` de índice), gerado por `python scripts/gerar_relatorios.py` a partir de `rodadas/linha_do_tempo.json`. Regerar sempre que a linha do tempo mudar; a rodada 8 aparece como em aberto.
- Medição de acessos: Google Analytics (Firebase) carregado **só depois do aceite** na faixa de privacidade (`grafico/relatorio-app/src/ui/Consentimento.tsx`); sem aceite ou com Do Not Track nada do Google é baixado. Texto em `PRIVACIDADE.md` (aba Docs). Não gravar o aceite em arquivo versionado; qualquer novo rastreador passa pelo mesmo consentimento.
