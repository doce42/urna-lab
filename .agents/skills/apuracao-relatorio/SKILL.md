---
name: apuracao-relatorio
description: Gráfico interativo (lightweight-charts) e relatório visual (relatorio.html + PDF) do estudo da apuração — linguagem para leigos com rigor acadêmico, paleta validada para daltonismo, conclusão em três níveis. Use ao mexer em grafico/web, analise/relatorio_dados.py ou gerar o PDF.
---
# Gráfico e relatório

## Quando usar
Atualizar o gráfico ou o relatório, acrescentar uma seção, gerar o PDF.

## Comandos
- `make relatorio` (`analise/relatorio_dados.py` → `grafico/web/relatorio_dados.json`, `logs.json`).
- `make servir` → http://localhost:8765 (gráfico) e /relatorio.html. `make pdf` → `grafico/web/relatorio.pdf` (o botão "Baixar relatório completo (PDF)" aponta para ele).

## Regras
- **Linguagem:** para leigos, sem perder o rigor. Cada número com o que significa; termos técnicos explicados na primeira vez; método "desenhado" (diagramas, fluxos) no relatório, matemática completa só no METODOLOGIA.md.
- **Neutralidade:** nada de adjetivo político; conclusão em três níveis (prova determinística, evidência estatística com poder, limite dos dados) e resposta direta sobre fraude nos termos que os dados sustentam.
- **Cores** (validadas com o validador de paleta da skill dataviz, temas escuro e claro):
  - Lula `#ef4444` (claro `#dc2626`), adversário `#3b82f6` (`#2563eb`), terceira cor `#0d9488`.
  - Branco e nulo compartilham a terceira cor e se distinguem pelo traço.
  - Nunca dois eixos y no mesmo gráfico.
- **Gráfico de tempo:** a lightweight-charts espaça por quantidade de pontos, então preencha todos os segundos/minutos para o tempo ficar proporcional.
- **Antes de entregar:** abra a página (`chromium --headless --screenshot`) e olhe. O validador não vê sobreposição de rótulos.
