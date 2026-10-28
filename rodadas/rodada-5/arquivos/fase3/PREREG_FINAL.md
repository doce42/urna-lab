# F3: investigações finais para fechar a Evolução (28/10/2026), pré-registro

Escrito antes de rodar. Quatro investigações, cada uma com um teste principal e uma validação, uma correção e uma repetição por falha operacional. Sem subagente, sem reprocessamento nacional. Regra adversarial mantida: registro do próprio sistema é "compatível", não "verificado".

## Z1. Salvador: o desvio de ~30 mil votos se explica? (`fase3/final_salvador.py`)
1. **Resíduo das capitais:** mesmo modelo do T44 (virada de 2026 com histórico de 2022, perfil do 1º turno, eleitorado e UF), resíduo de todas as 27 capitais. Salvador é desviante **entre as capitais** se o z dela, na escala robusta das capitais sem ela, for maior que 3.
2. **Controle por perfil, nas seções:** seções de Salvador e das outras capitais do Nordeste. Δvirada (2026 − 2022, mesma seção) regredido em escolaridade, idade, sexo (perfil de 2026 por seção) e proporção do 1º turno de 2026, sem Salvador no ajuste.
   - **"Explicado pelo perfil":** o excesso médio de Salvador cai abaixo de 1/3.
   - **"Persiste":** fica acima de 2/3 com IC por bootstrap de locais excluindo 0.
   - **Fora disso:** "explicado em parte".
- **Validação:** a mesma conta para Recife e Fortaleza como controles. Espera-se que não apareçam como desviantes.
- **Leitura:** nenhum resultado demonstra causa. "Persiste" mantém a anomalia; "explicado" a rebaixa a S1.

## Z2. T33: verificações de assinatura do software sem sucesso no log (`fase3/final_t33.py`)
- **Pergunta:** que mensagens são, quando ocorreram (antes da abertura, durante ou depois da votação), em que modelos de urna, e as urnas com falha votam diferente?
- **Procedimento:**
  - ler o log de todas as urnas de 2026 com `sw_verif_falha` > 0 (1º e 2º turno) e extrair as linhas de falha com hora e texto;
  - classificar por momento (antes das 8h, 8h a 17h, depois de 17h) e por texto;
  - fazer o teste de votação do caso B adversarial (z do T02 contra a UF, permutação estratificada, limiar 0,3).
- **Validação:** o mesmo teste de votação no outro turno.
- **Leitura:** a explicação vem do próprio log ("compatível"). Deslocamento de votos detectado vira S3; ausência fica sem deslocamento no limiar.

## Z3. Anomalias pequenas de 2026: rajada sem biometria (T28) e seções extremas (T02) (`fase3/final_anomalias.py`)
- **T28:** para as 8 urnas sinalizadas (1º turno), do log, a sequência dos últimos 30 minutos: tipo de habilitação, intervalos e votos. Também a proporção de Lula na urna contra o município.
- **T02:** para as seções com |z| > 5 em 2026, o local de votação, se outras seções do mesmo local também desviam, a variação de comparecimento e a conferência dos arquivos (já no R1).
- **Validação:** as mesmas medidas em 2022.
- **Leitura:** descritiva e documental, sem causa demonstrada.

## Z4. Evidência externa, rodada única e de escopo fixo (`fase3/final_externo.md`)
1. **Certificados:** AC URNA v2 e AC RAIZ UE em páginas oficiais do TSE (`tse.jus.br`, `justicaeleitoral.jus.br`), no máximo 3 tentativas de acesso.
2. **Boletins impressos fotografados por terceiros em 2026,** com seção identificável (sites de fiscalização de partidos, projetos independentes, auditorias): uma busca. Havendo conjunto aberto, uma amostra é comparada com a tabela.
3. **Canal alternativo para os 173 arquivos de 2022:** uma tentativa.
- **Parada:** sem dado primário acessível, o item fica "bloqueado por fonte externa", com o que foi tentado. Nada de redes sociais nem vídeos como fonte.

## Fechamento
Ao final, cada um dos 33 itens do inventário e das 26 perguntas recebe uma resposta final:
- **Respondida no escopo:** demonstrada ou refutada.
- **Limite dos dados ou do método:** com o motivo.
- **Bloqueada por fonte externa:** com o que seria preciso.

Nada fica como "em andamento" sem dizer por quê. O congelamento depende do responsável.

## Execução e desvios (registrados depois de rodar)
- **Z1:** uma correção operacional (coluna `QT_ELEITORES` no perfil de 2026).
  - **Validação:** Fortaleza também apareceu desviante no teste por seção, no sentido oposto (−0,105). O teste por seção não isola Salvador como caso único.
  - **O que fica:** Salvador continua a única capital desviante no modelo municipal (z 6,1).
- **Z2:** a classificação por momento foi complementada com uma extração descritiva das linhas do próprio dia da eleição, para verificar se cada erro é seguido de sucesso do mesmo arquivo. Leitura dos mesmos logs, sem teste novo.
- **Z3:** executado como previsto. Um erro de nome de coluna foi corrigido antes da execução.
- **Z4:** duas buscas, sem dado primário. Itens bloqueados, com as tentativas em `fase3/final_externo.md`.
