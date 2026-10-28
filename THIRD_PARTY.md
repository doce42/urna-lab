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

## Documentação técnica do TSE (`dados/brutos/doc/`)
Material público do Tribunal Superior Eleitoral (portal, Eleições 2022, "Documentação técnica do software da urna eletrônica"), guardado aqui sem alterações para conferência: especificação ASN.1 e exemplos de BU, RDV e assinatura digital, especificação do formato do log, leia-me dos arquivos da urna e lista de hashes das chaves públicas do QR Code. Os direitos pertencem ao TSE; o arquivo `.gitignore` deixa de fora os `.zip` originais (o conteúdo extraído está na pasta). Fonte: https://www.tse.jus.br/eleicoes/eleicoes-2022/documentacao-tecnica-do-software-da-urna-eletronica
