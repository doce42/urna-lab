---
name: apuracao-versoes
description: Governança e publicação do estudo da apuração — fases e rodadas congeladas (rodada.py fechar --incluir, prova), linha do tempo, publicação no GitHub só por publicar.py, tags e releases, deploy do site, preservação dos dados do TSE (manifesto SHA-256, carimbo OpenTimestamps, cópias) e pacote de dados leves. Use ao encerrar uma fase, publicar, registrar contestação ou preparar dados para terceiros.
---
# Versões, publicação e preservação

## Fases e rodadas
- **Rodada:** fotografia congelada, que nunca se reescreve. Em `rodadas/rodada-N/`, com `resumo.json` que guarda o SHA-256 de tudo.
  - Para fechar: `python scripts/rodada.py fechar N VX.Y "título" --incluir fase3 CONCLUSAO.md …`. O `--incluir` copia documentos, scripts e resultados para `arquivos/` **antes** do hash, para não repetir o desvio da rodada 4 (`rodadas/rodada-4-desvio.md`).
  - Gere `proveniencia_*.json` antes e inclua.
- **Contestação de um teste:** `python scripts/rodada.py prova TXX "tipo" alvo "descrição" resistiu|caiu|ajustado|em_andamento`.
- **Linha do tempo:** `rodadas/linha_do_tempo.json`, com fases, marcos e conclusões recentes. Cada mudança de estado de fase guarda o estado anterior em `historico`.
- **Congelar só com aprovação explícita do responsável.** "Autorizo" não substitui auditoria. A V1.2 foi congelada cedo demais e ficou preservada como registro.

## Publicar
1. `.venv/bin/python scripts/verificar.py` precisa dizer "tudo ok".
2. Build do site: `cd grafico/relatorio-app && npm run build`. O build roda `build-dados.mjs`, que lê o registro, a linha do tempo, os inventários, as respostas e o veredito.
3. Conferir as páginas com o Playwright (`chromium` do sistema), sem erros e sem rolagem horizontal no celular.
4. `python scripts/publicar.py "mensagem"`. É o único caminho para o GitHub: higieniza caminhos e procura dados pessoais. Confira a saída "publicado:" **antes** de criar tag (lição do v1.1).
5. Tag e release: no clone público `<DISCO_GRANDE>/projects/urna-lab-publico` (`git tag -a vX.Y`, `gh release create`).
6. Site: `firebase deploy --only hosting`, a partir da raiz do projeto.

Não use `pgrep` ou `pkill -f` com padrão que apareça na própria linha. Mate processos por PID em comando separado.

## Preservação dos dados (`DADOS_PRESERVACAO.md`)
- **Manifesto:** `scripts/manifesto.py` grava `dados/listas/MANIFESTO.csv` (SHA-256 de ~52 mil arquivos, ~405 GB). Recalcule e compare com o anterior antes de cada congelamento.
- **Carimbo:** `scripts/carimbo.py criar|atualizar|verificar <arquivo>` (OpenTimestamps) no manifesto e no `resumo.json` de cada rodada. Atualize os `.ots` horas depois.
- **Conteúdo:** a cópia dos bytes fora da máquina (HD externo; Internet Archive ou torrent) depende do responsável.

## Dados leves para terceiros
`scripts/dados_leves.py` → `dados_leves/` (fora do git), anexado ao release. Contém tabelas por seção, resumo por urna dos arquivos de urna, votos por minuto, perfil por seção, resultados, capturas da divulgação, manifesto e SHA256SUMS. Leia `DADOS_LEVES.md`: é preliminar e regerado a cada versão.

## Atualização da rodada 7 (28/10/2026, V1.5)
- **Rodada 7 fechada como V1.5** (28/10/2026): Operação Veracidade Geral (T58 a T65, Q40 a Q50). `rodada.py fechar --incluir` agora **ignora arquivos que o git ignora**.
- **Documentos de método atualizados depois do congelamento** (METODOLOGIA, PIPELINE, MAPA_SKILLS, REFERENCIAS, AUTOAUDITORIA, DADOS_PRESERVACAO, DIRETRIZ, CONTRIBUTING, Makefile, skills): a raiz tem a versão vigente; a cópia congelada na rodada 7 é anterior, e a rodada 8 congela a vigente. Rodada fechada não se reescreve.
- **Publicar:** `publicar.py` recusa arquivo > 20 MB e total > 120 MB; derivados grandes estão no `.gitignore`. Depois: tag `v1.5` no clone público, `gh release create`, `firebase deploy --only hosting`, `carimbo.py criar rodadas/rodada-7/resumo.json` (e `atualizar` horas depois).
- **Rodada 8 permanece aberta**: nada de `rodada.py fechar 8` sem aprovação explícita do responsável.
- Nunca `pkill -f` com padrão presente na própria linha de comando; mate por PID em comando separado.
