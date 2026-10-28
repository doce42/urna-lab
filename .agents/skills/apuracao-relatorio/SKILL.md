---
name: apuracao-relatorio
description: Gráfico interativo (lightweight-charts), relatório visual (relatorio.html), relatório em PDF montado dos JSON (grafico/montar_relatorio_pdf.py) e site React do estudo da apuração — linguagem para leigos com rigor acadêmico, paleta validada para daltonismo, conclusão em três níveis. Use ao mexer em grafico/web, grafico/relatorio-app, analise/relatorio_dados.py ou gerar o PDF.
---
# Gráfico e relatório

## Quando usar
Atualizar o gráfico ou o relatório, acrescentar uma seção, gerar o PDF.

## Comandos
- `make relatorio` (`analise/relatorio_dados.py` → `grafico/web/relatorio_dados.json`, `logs.json`).
- `make servir` → http://localhost:8765 (gráfico) e /relatorio.html (relatório interativo antigo).
- `make pdf` → `python3 -I grafico/montar_relatorio_pdf.py`: monta `grafico/web/relatorio_impresso.html` e imprime com o Chromium headless (sem servidor) em `grafico/web/relatorio.pdf`, copiado para `grafico/relatorio-app/public/relatorio.pdf` (o site linka `/relatorio.pdf`; o botão só aparece se o arquivo existir). `--sem-pdf` só gera o HTML.

## Regras
- **Linguagem:** para leigos, sem perder o rigor. Cada número com o que significa; termos técnicos explicados na primeira vez; método "desenhado" (diagramas, fluxos) no relatório, matemática completa só no METODOLOGIA.md.
- **Neutralidade:** nada de adjetivo político; conclusão em três níveis (prova determinística, evidência estatística com poder, limite dos dados) e resposta direta sobre fraude nos termos que os dados sustentam.
- **Cores** (validadas com o validador de paleta da skill dataviz, temas escuro e claro):
  - Lula `#ef4444` (claro `#dc2626`), adversário `#3b82f6` (`#2563eb`), terceira cor `#0d9488`.
  - Branco e nulo compartilham a terceira cor e se distinguem pelo traço.
  - Nunca dois eixos y no mesmo gráfico.
- **Gráfico de tempo:** a lightweight-charts espaça por quantidade de pontos, então preencha todos os segundos/minutos para o tempo ficar proporcional.
- **Antes de entregar:** abra a página (`chromium --headless --screenshot`) e olhe. O validador não vê sobreposição de rótulos.

## Site atual (React)
- **Onde:** `grafico/relatorio-app`. O build é `npm run build`, que roda `build-dados.mjs` (registro, linha do tempo, inventário, `respostas_f3.json`, `veredito_2026.json`).
- **Páginas:**
  - **Início:** com a resposta central (`RespostaHome`).
  - **Respostas** (`src/paginas/Respostas.tsx`): busca por pergunta, resposta central, perguntas com "Em votos" e os 33 itens.
  - **Testes:** com o selo de sinal (`src/ui/Sinal.tsx`).
  - **Mapas.**
  - **Evolução** (`LinhaDoTempo.tsx`).
  - **Docs:** lista em `build-dados.mjs`.
- **Deploy:** `firebase deploy --only hosting`, depois de conferir com o Playwright. A Home mostra só a fase atual; o detalhe fica em Evolução.

## Atualização da rodada 7 (28/10/2026, V1.5)
- **Site:** `build-dados.mjs` inclui os `.md` de `operacao_veracidade/` em `docs.json` (slugs `ov-*`), e a página Docs tem o grupo "Operação Veracidade Geral". As Respostas tinham 6 capítulos e 50 perguntas na V1.5 (hoje 7 capítulos e 56 perguntas; filtro por classificação, âncora `#/respostas/<id>`). O veredito mostra os avisos (`avisos` em `f3_veredito.py`) e a nota das anomalias.
- **Crédito do autor no rodapé:** vem de `grafico/relatorio-app/credito.local.json` (fora do git); não escrever em arquivo versionado.
- **Ao mudar uma conclusão:** editar `fase3/f3_veredito.py`, `f3_respostas.py`, `f3_inventario.py` (o detalhe das Respostas vem do `inventario.json`), `README.md`, `CONCLUSAO.md`, `AGENTS.md`, `rodadas/linha_do_tempo.json`; regerar, `verificar.py`, `npm run build`; conferir as páginas em 390 e 1280 px.
- Mostrar o aviso: "o poder é medido sobre uma base real que pode já conter alteração", e o da assimetria entre sentidos.

## Atualização da rodada 8 (aberta, 28/10/2026)
- **Placar da Home pelo Sinal** (S0 a S5, PC, M), igual à tela de Testes; a classe de evidência A a G é legada e fica recolhida. O selo do rodapé vem de `build-dados.mjs` e considera **todas** as fases com rodada (não só `F1` a `F3`): mostra a última versão concluída e a rodada em andamento. Números escritos à mão (README, AGENTS) devem ser conferidos a cada rodada.

## Relatório em PDF (desde 28/10/2026, rodada 8 aberta)
- **De onde vêm os dados:** `fase3/veredito_2026.json` (resposta, resumo em quatro partes e achados em `resposta_central.resumo`, alegações em `resposta_central.alegacoes`, hipóteses, anomalias, sinal por teste), `fase3/respostas_f3.json` (capítulos e as 56 perguntas), `testes/registro.json` (os testes e a evidência dos da Operação Veracidade), `rodadas/linha_do_tempo.json` (rodadas 6 a 8 e a rodada aberta), `operacao_veracidade/resultados/tabelas_sim.md` (poder do T63), `fase3/resultados/relatorio_pericial_r2b.json` (sensibilidade do corte), `fase3/proveniencia_v1_5.json` e `rodadas/rodada-7/resumo.json` (reprodutibilidade), `AUTOAUDITORIA.md` (tabelas de limites). Nenhum número é escrito no script.
- **Estrutura:** parte A (2 a 3 páginas): pergunta, resposta em quatro partes (observado, excluído, sem resposta, o que faltaria), achados, alegações com resposta curta, escala de sinal, avisos. Parte B: índice com âncoras, dedução, H1 a H10, anomalias, tabela dos testes por módulo, Operação Veracidade (poder por mecanismo, cadeia, terceiros), rodadas 6 a 8, perguntas resumidas (primeiras frases inteiras, com remissão ao site), método, limites, autoauditoria e reprodutibilidade.
- **Para mudar um texto:** mude a fonte (`f3_veredito.py`, `f3_respostas.py`, registro), regere na ordem (`f3_veredito.py`, `f3_inventario.py`, `f3_respostas.py`, `verificar.py`) e rode `make pdf`. Confira: `pdftoppm -r 60 -png grafico/web/relatorio.pdf /tmp/p` e leia ao menos as páginas 1 a 4, uma de tabela larga e a última. O sinal aparece sempre com o código (S0 a S5, PC, M) junto do nome, para funcionar em preto e branco.
- **Site:** Q51 a Q56 ficam no capítulo `pericial` das Respostas (os ids não mudam); a Home mostra as alegações com resposta curta (`AlegacoesResumo` em `src/ui/Sinal.tsx`) e recolhe hipóteses e anomalias; a página Docs põe em "Outros documentos" todo doc do `build-dados.mjs` que não estiver num grupo.


## Relatórios por fase e privacidade (28/10/2026)

- `relatorios/` tem um relatório por fase ou rodada (`fase1.md` a `rodada-8.md`, com `README.md` de índice), gerado por `python scripts/gerar_relatorios.py` a partir de `rodadas/linha_do_tempo.json`. Regerar sempre que a linha do tempo mudar; a rodada 8 aparece como em aberto.
- Medição de acessos: Google Analytics (Firebase) carregado **só depois do aceite** na faixa de privacidade (`grafico/relatorio-app/src/ui/Consentimento.tsx`); sem aceite ou com Do Not Track nada do Google é baixado. Texto em `PRIVACIDADE.md` (aba Docs). Não gravar o aceite em arquivo versionado; qualquer novo rastreador passa pelo mesmo consentimento.
