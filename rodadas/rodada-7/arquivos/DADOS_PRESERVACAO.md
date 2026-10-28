# Preservação dos dados do TSE

**O risco:** os arquivos do TSE podem ser trocados, retirados ou republicados no futuro, ou quem baixar de novo pode receber outra versão. Uma pesquisa que não guarda prova do que usou fica impossível de reproduzir ou de defender.

**As camadas de proteção:**

| Camada | O que garante | Onde | Estado |
|---|---|---|---|
| 1. Manifesto SHA-256 | Identifica, byte a byte, cada arquivo usado (~52 mil arquivos, ~405 GB) | `dados/listas/MANIFESTO.csv` | Recalculado em 28/10/2026 e congelado na V1.3 |
| 2. Assinatura das urnas | Cada arquivo de urna (BU, RDV, log, imagem) é assinado pela própria urna. Uma cópia alterada falha na conferência, mesmo sem o nosso manifesto | Lista assinada `.vscmr`/`.vsc` dentro dos pacotes | Conferida (T14 a T17, SA22). A cadeia até a raiz do TSE não foi verificada |
| 3. Carimbo de tempo (OpenTimestamps) | Prova que o manifesto e cada versão congelada existiam em 28/10/2026, ancorados no Bitcoin, sem depender de nós nem do TSE | `dados/listas/MANIFESTO.csv.ots` e `rodadas/rodada-5/resumo.json.ots` | Criado em 28/10/2026, às 15:49. O `.ots` do resumo é gravado depois do congelamento (prova sobre o resumo, não entra no próprio hash). Completar com `scripts/carimbo.py atualizar` depois da confirmação no Bitcoin |
| 4. Cópia do conteúdo | Guarda os bytes, para reproduzir mesmo se o TSE retirar os arquivos | Fora desta máquina | **Pendente:** HD externo do responsável e cópia pública (Internet Archive ou torrent acadêmico) |
| 5. Dados derivados leves | Permite repetir boa parte das análises sem os 405 GB | Release `v1.3` do GitHub, `dados_leves_v1.3.zip` (ver `DADOS_LEVES.md`) | Publicado em 28/10/2026 (262 MB, SHA-256 no `.sha256` do release) |

## Como conferir se um arquivo baixado hoje é o mesmo que usamos
```
sha256sum bweb_2t_SP_presidente.csv
grep bweb_2t_SP_presidente.csv dados/listas/MANIFESTO.csv
```
Se o SHA-256 for diferente, o arquivo mudou. Isso deve ser reportado, porque nenhuma análise deste repositório vale automaticamente para a versão nova.

## Como conferir o carimbo de tempo
```
python scripts/carimbo.py verificar dados/listas/MANIFESTO.csv
```
O carimbo confirma que esses hashes existiam na data, pela blockchain do Bitcoin, sem confiar no projeto.

## Limites
- Hash e carimbo **detectam** troca, mas **não guardam** o conteúdo. Sem a camada 4, uma versão retirada pelo TSE não pode ser recuperada daqui.
- A assinatura da urna prova integridade desde a urna, não que a urna seja autêntica até a raiz (P11).
- O manifesto cobre os arquivos baixados. Os 173 arquivos de 2022 que nunca estiveram no pacote do TSE não podem ser preservados (A173).
