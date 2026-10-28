# AGENTS.md: manual para qualquer agente de IA (e para pessoas)

Estudo imparcial e reproduzível da apuração presidencial brasileira de 2026 (1º e 2º turno), com 2022 como referência. Usa só dados oficiais do TSE. Este arquivo vale para qualquer modelo (Claude, GPT, Gemini, Llama…): `CLAUDE.md` aponta para ele, e as skills por domínio ficam em `.agents/skills/` (`.claude/skills` aponta para lá).

**Referência metodológica permanente: `DIRETRIZ.md`** (pergunta do estudo, princípios, cinco níveis, classes de evidência A–G, ficha de resultado, exploratório × confirmatório, viés de confirmação). Os princípios abaixo a resumem.

## Princípios (não negociáveis)
1. **Imparcialidade.** O estudo não parte de hipótese sobre quem ganhou nem de suspeita sobre o sistema. Descreve o comportamento, define o esperado com modelos explícitos e mede as divergências. Linguagem neutra; nada de adjetivo político.
2. **Só dado oficial.** Nada estimado onde existe dado medido. Toda estimativa (inferência ecológica, previsão de curva) é rotulada como estimativa e tem conferência contra o observado.
3. **Pré-registro.**
   - Teste novo entra no `PROTOCOLO.md` (seção 8, emenda datada) e no `testes/registro.json` **antes** de olhar o resultado.
   - O critério de anomalia está no PROTOCOLO, seção 4: passa do limiar, não se explica por acaso, geografia, demografia ou artefato, e se repete em pelo menos dois testes independentes.
4. **Artefato antes de anomalia.** Todo sinal estranho é investigado como possível erro de leitura, teto de 0/100%, fuso, seção agregada, arquivo cortado ou voto órfão. Os já encontrados estão no `CATALOGO.md`, seção 4.
5. **Poder e especificidade.**
   - Teste forense novo roda nos dados reais, em 2022 e com fraude sintética (`analise/poder.py`).
   - Teste que acusa dado limpo não entra na conclusão.
6. **Três tipos de afirmação, sempre separados:**
   - prova determinística (conta exata, criptografia);
   - evidência estatística (com poder medido);
   - limite dos dados públicos (`AUTOAUDITORIA.md`).
7. **Tudo registrado.** Cada etapa, incidente e consumo de recursos vai para o `CATALOGO.md`. Cada referência vai para o `REFERENCIAS.md`, classificada.

## Mapa do projeto
- `PROTOCOLO.md`: perguntas, modelos nulos (N1–N7), módulos, critérios, emendas.
- `METODOLOGIA.md`: a matemática de cada teste.
- `AUTOAUDITORIA.md`: mapa de ameaças, validade, lacunas.
- `CATALOGO.md`: linha do tempo, testes, artefatos, consumo.
- `PIPELINE.md`: ordem de execução, dicionário de dados, armadilhas.
- `REFERENCIAS.md`: bibliografia classificada.
- `MAPA_SKILLS.md`: quais skills cobrem quais testes e arquivos.
- `testes/registro.json`: registro legível por máquina de todos os testes (id, pergunta, método, modelo nulo, script, comando, saída, situação).
- `Makefile`: `make ajuda` lista tudo.
- Código: `scripts/` (download e preparação), `analise/` (testes, leitura dos arquivos das urnas), `grafico/` (gráfico interativo e relatório em `grafico/web/`).

## Como começar (agente ou pessoa)
1. `make ambiente` (Python 3.13; `requirements.txt` com versões fixas).
2. `make dados-do-zero`: baixa e prepara tudo do TSE. São ~250 GB e horas; precisa de disco grande.
3. `make base`, `make base ANO=2022`, `make dados`, `make bateria`, `make bateria ANO=2022`, `make comportamento`, `make integridade`, `make totalizacao`, `make relatorio`.
4. `make verificar`: conferências de sanidade. Rode **sempre** depois de mudar qualquer coisa.
5. `make servir` e abra http://localhost:8765 (gráfico) e /relatorio.html; `make pdf` gera o PDF.

## Como acrescentar um teste (o fluxo que todo agente deve seguir)
1. Escreva a hipótese, o modelo nulo e o limiar no `PROTOCOLO.md` (emenda datada).
2. Registre o teste em `testes/registro.json` (próximo id livre, situação `a_fazer`).
3. Implemente seguindo a skill do domínio (`.agents/skills/`). Testes estatísticos por seção vão em `analise/bateria.py` (gravando `R["T<nn>"]`).
4. Rode em 2026 **e** 2022; meça o poder com fraude sintética; investigue artefatos.
5. Documente a matemática no `METODOLOGIA.md`, o resultado no `CATALOGO.md` e as fontes no `REFERENCIAS.md`. Atualize a situação no registro.
6. `make verificar` tem que passar.

## Regras de operação
- **Recursos:** use `nice`/`ionice` e no máximo `NPROC` processos (padrão 12), deixando folga de CPU e RAM.
- **Site de resultados do TSE:** respeite o limite. Ele devolve 429 com conexões demais; use HTTP/2 multiplexado e controle de ritmo (`scripts/baixar_sp_2t_educado.py`). Prefira sempre os pacotes do CDN.
- **Processos:** nunca use `pkill -f` com um padrão que apareça na própria linha de comando. Mate processos num comando separado.
- **Nunca edite um script de bash que está rodando.**
- **Dados brutos:** ficam fora do git (`.gitignore`). O repositório guarda código, documentação, listas de download e resultados pequenos.

- **Situação e resultados num lugar só:** `testes/registro.json` e `CATALOGO.md`. Os documentos de método (METODOLOGIA, PROTOCOLO) não carregam situação ("pendente", "feito"), para não haver versões contraditórias. Ao atualizar, preserve o texto antigo como instantâneo datado no CATALOGO (lição de 27/10, revisão cega externa).

- **Sem GitHub Actions e sem Git LFS** (têm limites pagos): toda a computação roda na máquina local; o repositório guarda só código, documentação, listas de download e resultados pequenos.
- **Publicar** só com `python scripts/publicar.py "mensagem"` (copia, higieniza caminhos, varre atrás de dados pessoais e segredos, aborta se achar algo, commita com o e-mail de privacidade do GitHub). Nunca dê `git push` direto do diretório de trabalho. Teste antes com `--simular`.


## Rodadas (linha do tempo)
O estudo avança em rodadas congeladas (`rodadas/rodada-N/`, tag `rodada-N`). Rodada fechada não se reescreve: correção entra na rodada seguinte. Toda contestação feita a um teste vai para o campo `provas` dele (`python scripts/rodada.py prova ...`). Ao fechar uma rodada: `python scripts/rodada.py fechar N "título"`, atualizar `rodadas/linha_do_tempo.json`, regerar o site, publicar e criar a tag. Detalhes em `RODADAS.md`.
