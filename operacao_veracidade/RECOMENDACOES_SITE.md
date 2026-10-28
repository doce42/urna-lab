# Recomendações para o site, o README e o registro (nada foi aplicado)

Esta operação **não publicou, não fez build, não alterou o site, o README, o veredito nem o `testes/registro.json`**. A integração abaixo depende de aprovação.

## 1. Texto a mudar (itens do `09`)
1. **Resposta central** (README, CONCLUSAO, VEREDITO, Home): trocar "deixariam sinais muito maiores do que os encontrados" por uma frase que diga o alcance por mecanismo (item 2 do `09`) e acrescentar a distinção entre o que foi achado e um teto (item 3).
2. **"Restam dois caminhos"**: passar a "restam caminhos fora do alcance" e listar H9, H10 e a escala regional, de UF, de lote ou uniforme (item 4).
3. **H7 (zeros):** de "Sem sinal no alcance testado" e "exatamente o previsto fora da amostra (79,1 e 101,5)" para "Não determinado (ponto cego): nenhum modelo calibrou" (item 10). É também uma inconsistência atual entre H7 e T41.
4. **T05:** de S0 para PC/M (item 15). **Q7:** trocar "falso alarme 0/30" por o intervalo medido (item 16).
5. **H1, H5, H6, H8, H3** (itens 5, 8, 9, 11, 7): ajustes de alcance e fatos novos (pausa de recebimento de 116 minutos).
6. **P6 e P21:** de "boletins de terceiros não obtidos" para "parcialmente demonstrado (404 boletins, amostra de conveniência)" (item 17).
7. **Q5:** acrescentar que a cadeia até a AC emissora vale agora para 100% das urnas e a data dessa verificação.

## 2. Para entrar no registro e nas Respostas (depende de aprovação e de uma emenda 16 ao PROTOCOLO)
- Os testes **T60a, T60b, T61, T62, T63, T64** (`resultados/registro_operacao.json`) e as perguntas **N1 a N8** (`resultados/respostas_novas.json`; já formatadas em `07`) como um capítulo "Operação Veracidade".
- As emendas internas da operação (`PROTOCOLO_PRE_EXECUCAO.md`: emendas 1 a 4) devem ser citadas na emenda do PROTOCOLO.
- O caso ES 57932/9/85 e os 17 casos de certificado relidos por ID e data como achado de "artefato do leitor" no CATALOGO (`06`).

## 3. Avisos que deveriam aparecer ao lado dos resultados
- "O poder de detecção é medido sobre uma base real que pode já conter alteração; o experimento não consegue dizer que a base está limpa."
- "O poder é assimétrico entre os sentidos, por causa da cauda pró-Lula presente na base nos dois anos."
- "Registros internamente coerentes gerados por uma fonte comprometida passam por todas as verificações internas; só evidência de fora distingue."
- "Os 404 boletins de terceiros são uma amostra de conveniência (0,08%)."

## 4. Pendências que o site não deve fingir resolvidas
Raiz da cadeia de certificados; teste de integridade com votos conhecidos (resultado não obtido); amostra probabilística de boletins impressos; releitura dos 16 casos do T14 por ID de urna, data e seção; repetição do T44 por cidade.

## 5. Para quem quiser reproduzir
`REPRODUCAO.md`. Dados externos de terceiros em `externo/arvor_totalizacao/` (arquivos estáticos públicos, com SHA-256 e data de download).

## 6. Se for publicar a pasta (o `publicar.py` recusa arquivos acima de 20 MB e totais acima de 120 MB)
- Os **quatro parquets de certificados** (`resultados/certs_<ano>_<turno>t.parquet`, 71 a 76 MB cada, ~300 MB) **abortariam a publicação**. São reproduzíveis por `cert_extrai.py`. Sugestão: acrescentar `operacao_veracidade/resultados/certs_*.parquet` ao `.gitignore` e publicar só `cert_analise.json` e `casos_certificado.csv`, que trazem os resultados e todos os casos. A decisão é do responsável; nada foi alterado no `.gitignore`.
- **Arquivos de terceiros** em `externo/arvor_totalizacao/` (1,4 MB): são arquivos estáticos públicos, sem dado pessoal, mas **a licença de redistribuição não foi verificada**. Sugestão: publicar o `SHA256SUMS.txt`, a data de download e os scripts, e não os arquivos, até a licença ser confirmada.
- `sim_<ano>.parquet` (92 KB) e os CSV de grade cabem sem problema.
