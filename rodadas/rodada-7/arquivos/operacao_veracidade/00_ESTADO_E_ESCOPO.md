# 00. Estado e escopo da Operação Veracidade Geral

Execução: 28/10/2026, 18h00 em diante (hora de Brasília). Evidência bruta: `resultados/estado_inicial.txt`, `resultados/integridade_snapshots.json`.

## O estado real do projeto (diferente do que a ordem supunha)
- **As fases F4, F5, F6 e F7 não existem.** Não há diretório nem pré-registro dessas fases. O que existe: F1 (V1.0-rc1), revisão R1, baseline V1.0, F2 (V1.1), F3 (V1.3, rodada 5), "Alegações públicas" (V1.4, rodada 6) e a **rodada 7**, que está só no registro vivo (T58 e T59, perguntas Q40 e Q41) e **não foi congelada**. A linha do tempo (`rodadas/linha_do_tempo.json`) lista F1, R1, V1.0, F2, F3 e AP.
- Fase e rodada não são a mesma coisa aqui: a rodada 6 é a fase "AP"; a rodada 5 é a F3.
- Último teste registrado antes da operação: **T59**. O registro vivo tem 71 entradas (T01–T59 mais C, E, INC).
- Tudo que veio depois do T51 está documentado: T52–T57 (rodada 6), T58–T59 (rodada 7, registro vivo).

## Git e publicação
| Item | Estado |
|---|---|
| Clone público (`<DISCO_GRANDE>/projects/urna-lab-publico`) | branch `main`, HEAD `7c71fd8` ("T58: campo script"), sem alterações pendentes |
| Tags | `v1.0`, `v1.1`, `v1.2`, `v1.3`, `v1.4`, `rodada-1` |
| Diretório de trabalho do projeto | **não é um repositório com commits** (`master` sem nenhum commit); a publicação é por cópia higienizada (`scripts/publicar.py`) para o clone público |
| Alterações locais não publicadas | tudo o que está em `operacao_veracidade/` (novo) e nada mais; o último `publicar.py` rodou depois de T58–T59 |
| Processos concorrentes | nenhum agente. Um servidor HTTP local (`grafico/web`, porta 57885) de sessão anterior, sem relação. Os processos de extração desta operação (certificados) foram iniciados por ela |
| Rodada 7 em execução | não: o processamento terminou antes; nada foi tocado em arquivos em uso |

## Integridade dos snapshots (verificada hoje)
- **Rodadas 1 a 6: 100% dos arquivos com SHA-256 igual ao do `resumo.json`** (28, 30, 45, 30, 196 e 278 arquivos; 0 diferentes, 0 ausentes). A rodada 6 carrega uma nota: o comando de fechamento copiou por engano um arquivo local de termos pessoais e 43 logs ignorados pelo git, retirados antes da publicação; `rodada.py` passou a ignorar arquivos fora do git.
- **Manifesto dos dados brutos:** 51.883 linhas; amostra aleatória de 25 arquivos (semente 20261028) com SHA-256 igual ao do manifesto.
- **Achado de proveniência:** o manifesto traz um hash oficial de download só para **331** arquivos ("conferido"); 173 são "não publicado pelo TSE" e **51.379** estão "sem registro de download" (só o hash local). A integridade desses 51.379 arquivos apoia-se na lista assinada pela própria urna (hash de cada arquivo dentro de `vota.vsc`), não em hash publicado separadamente pelo TSE.

## Inventário de dados disponíveis (sem baixar de novo)
- Brutos do TSE (pacotes por UF com BU, imagem do BU, RDV, log e lista assinada): 2026, 1º turno (≈89 GB), 2º turno (≈6 GB em arquivos individuais de SP e ≈116 GB em pacotes por UF); 2022, 1º e 2º turnos (≈157 GB). Total ≈ 390 GB no disco de 1 TB, fora do git.
- Derivados: `analise/base.parquet` e `base_2022.parquet` (uma linha por seção, dois turnos), `analise/brutos/*/urnas_<UF>.parquet` (uma linha por seção com campos lidos de BU, RDV, imagem, log e assinatura), `minutos_<UF>.parquet`.
- Externos já usados: capturas do Internet Archive (39 instantes), DataUrnas-BR (implementação independente, só para decodificação e certificados de AC), documentos de formato do TSE.
- Baixados nesta operação (públicos, com SHA-256 e data): 404 boletins do 2º turno de 2026 lidos do QR Code impresso por terceiros (`externo/arvor_totalizacao/`).

## Matriz inicial (por grupo de perguntas)
Detalhe pergunta a pergunta em `07_RESPOSTAS_TODAS_AS_PERGUNTAS.md`.

| Pergunta | Fase | Teste | Fonte | Independência | Resultado herdado | Limite herdado | Novo teste nesta operação |
|---|---|---|---|---|---|---|---|
| Tabela = BU = RDV = imagem | F1–F3 | T01, T17b, Q1–Q3 | TSE | interna (mesma origem) | 0 diferenças nas seções lidas | consistência interna, não veracidade | T62 mede o limite; T61 compara com origem diferente |
| Assinaturas e cadeia | F1–F3 | T16, P11, Q5 | arquivos da urna; ACs de terceiro | interna (lista) + 200 seções (cadeia) | "todos até a AC emissora" | raiz não pública; 200 seções | **T60a (100%), T60b** |
| Totalização e divulgação ao vivo | F2–F3 | T32, Q6, P4 | Internet Archive, TSE | externa parcial (captura de terceiro de conteúdo do TSE) | 0 voto de diferença nas capturas | captura prova versão publicada, não voto | T61 (relógio e conteúdo de terceiros) |
| Curvas, viradas, vales | F3 | T40, Q8–Q14, T52 | recebimento do BU | interna | nenhum modelo de chegada validado | sem modelo; pausa de recebimento é fato | reuso (sem teste novo) |
| Zeros | F3 | T41, Q15–Q20, T49 | tabela, BU, RDV | interna | "sem sinal" no veredito; PC no T41 | modelo não calibrado | **T64** (3 famílias) |
| Entre turnos | F3 | Q21–Q26, T50–T51, T56–T59 | tabela | aritmética exata | identidade contábil; fluxos não identificáveis | voto secreto | reuso |
| Anomalias territoriais | F2–F3 | T44, T02, E02, I3 | tabela, perfil, log | interna + estatística | Salvador, zona 251 sem causa | sem fonte externa | T63 (poder por mecanismo) |
| Poder da bateria | F1–F3 | T13, I1, A2 | simulação | sintética | 2% numa cidade; ~123 mil disperso | só alguns mecanismos | **T63, T62** (14 mecanismos, 2 sentidos, 7 magnitudes) |
| Evidência externa | F3 | P6, P21 | — | — | "sem boletins de terceiros" | busca sem resultado | **T61** (404 boletins) |
