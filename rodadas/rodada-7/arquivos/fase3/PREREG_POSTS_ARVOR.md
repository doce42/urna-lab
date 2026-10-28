# Pré-registro: postagens de Leonardo Dias / arvor.co (T52 a T54), 28/10/2026

Escrito antes de qualquer contagem. Origem (só pergunta): posts no X de @leonardodias (26 a 28/10/2026) e o dossiê em brasil.arvor.co. Primeiro respondemos com testes já feitos; só entra teste novo onde nenhum cobre a alegação.

## Já cobertas por testes existentes (sem teste novo)
- **Prorrogação até 19h:** T09 (6.748 urnas fecharam 18h30–19h30; votaram como as vizinhas).
- **"Fortes evidências de votos sem biometria":** T12 (efeito some com idade), T28/P10 (8 urnas, 99 votos, padrão também em 2022). Complemento descritivo do 2º turno no T53.
- **Grupo atípico da mistura gaussiana (10.850 seções):** não reproduzimos o modelo deles; o próprio dossiê diz que a fatia de Flávio no grupo mudou −0,05 ponto (IC −0,19 a +0,07) e que não se liga a região nem a modelo. Nossos análogos: E02/I3 (locais atípicos), T02 (cauda), T47 (modelo).
- **Totalização paralela (286 BUs iguais ao TSE; "352 seções em que Flávio ganharia"):** Q1/T39 (0 diferenças em todas as seções lidas). Amostra enviada por voluntários não é aleatória; o placar dela não estima nada.
- **Pesquisas × urna (+5,53 pontos):** fora do escopo (só dados oficiais do TSE).

## T52: o boletim ficou parado entre a emissão e o recebimento?
- **Alegação:** 2º turno de 2026, emissão do BU com mediana 17:03 e recebimento 20:27; só 0,3% recebidos antes das 19h (2.260, todos até 17:08); nenhum entre 17:08 e ~19:30; Sergipe só a partir de 19:34; "só 34,7 mil votos após as 17h".
- **Fuso (artefato conhecido):** DT_EMISSAO e DT_BU_RECEBIDO podem estar em hora local ou de Brasília. Decide-se pelos dados, antes de medir: fuso do município pela abertura às 8h de Brasília (método do `relatorio_dados.py`); para cada campo, testa-se se a menor diferença recebido − emissão por UF fica igual nas UFs de fuso diferente (mesmo fuso) ou desloca pelo fuso.
- **Medidas (2026 e 2022, 2º turno, Brasil):** medianas e percentis de emissão e recebimento em hora de Brasília; fração recebida antes das 19h; maior intervalo sem recebimento entre 17h e 21h; primeiro recebimento por UF; votos registrados no log após 17h (Brasília).
- **Hipóteses:** H0: a recepção ficou suspensa enquanto houve urna aberta (prorrogação) e retomou depois; H1: retenção sem relação com o fechamento. Distingue: a retomada coincide (ou não) com o fechamento das últimas urnas prorrogadas; 2022 sem prorrogação mostra (ou não) o mesmo vazio.
- **Limite:** horários de sistema; não dizem a causa administrativa.

## T53: liberações sem biometria no 2º turno, 2026 × 2022
- **Medidas:** por turno e ano, votos habilitados por biometria, manual (sem biometria) e código do mesário, a partir do log; fração nacional e por UF; relação dentro do município entre a fração sem biometria e a virada de Lula (molde do T12, sem perfil; o T12 com perfil é a referência).
- **Leitura:** descritiva; o T12 continua sendo o teste da relação com o voto.

## T54: municípios em que Flávio perdeu votos do 1º para o 2º turno
- **Alegação:** 938 de 5.571, perdas de 133.900, 13,41 mi de eleitores; Lula +486.922 neles; Lula perdeu votos em 79 (16.115).
- **Medidas:** reproduzir; mesma conta em 2022 (municípios em que Lula e Bolsonaro perderam votos).
- **Leitura:** se 2022 tiver padrão de tamanho parecido para o candidato que perdeu fôlego, é comportamento de 2º turno.

Orçamento: 3 investigações, 1 execução + 1 correção. Script `fase3/posts_arvor.py`, saída `fase3/resultados/posts_arvor.json`.
