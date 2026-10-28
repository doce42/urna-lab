# Componentes e dados de terceiros

Este repositório usa o que está abaixo, cada um com a sua própria licença ou condição de uso. As licenças MIT e CC BY deste projeto **não** se aplicam a eles.

| Componente | Uso | Licença / condição |
|---|---|---|
| [TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts) v5 | gráfico interativo (`grafico/web/lightweight-charts.js`, cópia local com o aviso de licença no próprio arquivo) | Apache-2.0; exige manter o aviso de autoria e o atributo "TradingView" na página do gráfico |
| [D3](https://d3js.org) | mapas e gráficos (carregado de CDN) | ISC |
| [marked](https://github.com/markedjs/marked) | mostra os `.md` no relatório (carregado de CDN) | MIT |
| Malha territorial do [IBGE](https://servicodados.ibge.gov.br/api/docs/malhas) | só para desenhar os mapas (`grafico/web/geo/`) | dados públicos do IBGE; cite a fonte |
| Dados abertos do [TSE](https://dadosabertos.tse.jus.br) | origem de todos os dados do estudo; **não são redistribuídos aqui**, só os scripts para baixá-los | política de dados abertos do TSE |
| Parâmetros da curva E-521 ([SafeCurves](https://safecurves.cr.yp.to/)) | verificação das assinaturas das urnas (`analise/ed521.py`) | parâmetros matemáticos públicos |
