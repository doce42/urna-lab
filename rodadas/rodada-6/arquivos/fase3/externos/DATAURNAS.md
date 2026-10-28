# DataUrnas-BR usado no R1-20 (proveniência)

- **Repositório:** https://github.com/alissonlinneker/DataUrnas-BR (terceiro, licença MIT). Clone raso feito em 28/10/2026.
- **Commit:** `12f0433bd20882d305dd7b9e4987d6dcf3b321a9` (15/10/2026).
- **Local:** `<DISCO_GRANDE>/externos/DataUrnas-BR`, fora do repositório do projeto por ter 355 MB. Pode ser trocado pela variável `DATAURNAS_DIR`.
- **Arquivos lidos e SHA-256:** estão em `fase3/f3_reconcilia.py`, que confere commit e hashes antes de rodar e se recusa a continuar se não baterem.

## Lacuna registrada
A execução original de 28/10/2026 leu o clone numa pasta temporária da sessão e **não registrou** o commit nem os hashes no resultado (`fase3/resultados/R1_20_dataurnas.json`, preservado como foi gerado). O commit e os hashes acima foram obtidos depois, do **mesmo clone**:
- **Integridade:** `git status` estava limpo, então os arquivos lidos são os do commit.
- **Cópia:** o clone foi movido para o local permanente sem alteração.
- **Reexecução:** rodar de novo a partir dele (`fase3/resultados/R1_20_dataurnas_reproducao.json`) deu resultado idêntico ao original.

Não há como provar, além disso, que a execução original leu exatamente estes bytes. A reprodução idêntica é a evidência disponível.

## Confronto pendente
O README desse repositório registra 173 arquivos assinados pela urna e ausentes do pacote de dados abertos de 2022 (64 seções, a maioria do exterior). Isso não foi confrontado com a base do projeto (inventário: item A173).
