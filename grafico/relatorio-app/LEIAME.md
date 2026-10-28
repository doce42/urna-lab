# urna lab · site estático

Site do estudo (`urna-lab.web.app`): React + Vite + TypeScript, Tailwind, componentes Radix, gráficos em SVG sob medida (d3-geo/d3-scale/d3-array só como utilitários). Build 100% estático, roteamento por hash (`#/`, `#/testes`, `#/testes/T02`, `#/mapas`, `#/docs/metodologia/<secao>`).

## Construir (um comando)

```bash
cd grafico/relatorio-app
npm install          # só na primeira vez (versões fixas no package.json)
npm run build        # = npm run dados + tsc + vite build  →  dist/
```

`npm run dados` (`build-dados.mjs`) lê os JSON locais (`../web/relatorio_dados.json`, `dados.json`, `logs.json`, `mapas_dados.json`, `geo/*.json`), o `../../testes/registro.json` e os `.md` da raiz, e gera em `public/dados/` só o que o site precisa, carregado sob demanda:

| arquivo | conteúdo | quando carrega |
|---|---|---|
| `registro.json` | todos os testes + placar | primeira carga |
| `meta.json` | data de geração, existe PDF?, link do GitHub | primeira carga |
| `home.json` | totais, apuração por minuto, fluxo, UFs, logs por minuto, resumo do poder | Início |
| `testes.json` | números de cada teste (bateria, logs, divergências, poder…) sem listas pesadas | Testes |
| `mapas.json`, `mapas-2022.json`, `geo.json` | municípios (arrays compactos) e malha IBGE simplificada (TopoJSON) | Mapas |
| `docs.json`, `docs-indice.json` | os `.md` renderizados em seções HTML | Docs |

Rode o build de novo sempre que os JSON forem regerados: nenhum número do site é escrito à mão. O script também limpa caminhos da máquina (`[disco local]`) e os `.md` viram seções por título (links `.md` viram rotas internas; o resto aponta para o GitHub).

Deploy (feito pelo dono): `firebase deploy` na raiz do projeto (`firebase.json` já aponta para `grafico/relatorio-app/dist`).

## Relatório em PDF
Coloque o arquivo em `public/relatorio.pdf` antes do build: o botão "Relatório em PDF" aparece sozinho (cabeçalho, rodapé e Docs). Sem o arquivo, o botão fica escondido.

## Identidade
Tokens e logos vêm de `grafico/identidade/final/` (copiados para `public/`). Paleta dos gráficos: cobre `#B5612F` (2026/série principal), cinza (2022/referência), verde-azulado `#1F8A70` (Lula) e violeta `#7A5CC7` (Flávio Bolsonaro), validada para daltonismo com `dataviz/validate_palette.js` nos dois temas; nunca vermelho/azul.

## Testes "preliminar · em reprocessamento"
Lista fixa em `src/viz/testes.tsx` (`EM_REPROCESSAMENTO`: T14–T17b, T20, T24, T28–T36) mais qualquer teste com `situacao = em_andamento`. Quando o reprocessamento terminar, esvazie a lista.

## Desenvolver
`npm run dev` (Vite). Os dados precisam existir em `public/dados/` (`npm run dados`).

## Tamanho (build de 28/10/2026)
`dist/` ≈ 2,5 MB no disco; primeira carga ≈ 250 KB comprimidos (JS 120 KB + CSS 8 KB + fontes latin ~60 KB + registro/meta/home ~50 KB); visita completa ≈ 1 MB comprimido (geo 240 KB e mapas 145 KB só na página Mapas).
