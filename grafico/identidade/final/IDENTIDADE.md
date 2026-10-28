# urna lab — identidade final

**Símbolo:** urna isométrica (caixa vista de cima, três faces, fenda no topo). Topo em cobre, laterais em grafite; no escuro, laterais claras. Lê como "caixa de dados", não como urna eletrônica nem logo oficial.
**Nome:** `urna lab`, minúsculo, Sora SemiBold convertida em paths (não depende de fonte instalada).

## Arquivos
- `logo.svg` = `logo-claro.svg` (fundo claro) · `logo-escuro.svg` (fundo escuro)
- `logo-simbolo.svg` / `logo-simbolo-escuro.svg`: só a urna (avatar)
- `favicon.svg`: urna mais cheia e fenda grossa para 16 px; troca as cores com `prefers-color-scheme` · `favicon-32.png` de reserva
- `apple-touch-icon.png` (180, fundo grafite) · `og-image.png` (1200×630) · `tokens.css`

```html
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:image" content="/og-image.png">
```

## Regras
- Área livre = metade da largura da urna. Mínimo: urna 16 px; logo completo 96 px de largura.
- Não esticar, girar, recolorir faces nem pôr sombra. Sobre foto: só o símbolo.

## Paleta
| Papel | Claro | Escuro |
|---|---|---|
| Fundo / superfície | `#F6F5F3` / `#FFFFFF` | `#0F1012` / `#18191C` |
| Texto / apoio | `#1B1D21` / `#61656E` | `#EEECE8` / `#9EA1A8` |
| Marca (grafite) | `#1B1D21` | `#EEECE8` |
| Acento (cobre) | `#B5612F` (texto `#9A4F22`) | `#E08A55` |
| Borda | `#E4E2DE` | `#2A2C30` |

**Gráficos (`--cat-1..6`):** cobre `#B5612F`, lilás `#CC79A7`, verde-azulado `#009E73`, céu `#56B4E9`, mostarda `#C9A227`, grafite `#6B7280` (escuro: `#E08A55 #D98DB8 #2BB98C #6CC0EE #E3C04A #7A808C`). Simulação de daltonismo conferida nas três deficiências. Até 6 séries; rotular direto, não só por cor.

## Tipografia
Sora (400–700) para tudo; IBM Plex Mono para números tabulares, rótulos e código. Fallback: `system-ui, Segoe UI, Roboto, Arial` / `ui-monospace, Menlo, Consolas`.

## Neutralidade
Sem vermelho/azul como marca (são os lados da disputa; nos gráficos de candidatos a cor vem da legenda, nunca da marca), sem verde com amarelo, sem bandeira/estrela, nada de brasão, balança, cores ou urna eletrônica do TSE. Escrever "dados oficiais do TSE", nunca o TSE como autor.
