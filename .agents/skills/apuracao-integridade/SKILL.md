---
name: apuracao-integridade
description: Ler e verificar os arquivos gravados por cada urna (log, BU, RDV, imagem do BU, assinaturas vota.vsc) — assinatura Ed521/ECDSA, hashes, recontagem do RDV, sequência eleitor a eleitor do log. Use para os testes T14–T17, T24, T28–T31, T33–T35 ou ao mexer em analise/processar_brutos.py, der.py, ed521.py, seqlog.py.
---
# Integridade dos arquivos das urnas

## Quando usar
Testes do módulo A e da sequência do log, leitura de um formato novo, diagnóstico de "urna com erro".

## Comandos
- `make integridade NPROC=12`, ou `analise/processar_brutos.py <turno> [UF...]`. Lê o pacote oficial por UF (ou a pasta urna por urna).
- Saída: `analise/brutos/<t>t/urnas_<UF>.parquet` (uma linha por urna) e `minutos_<UF>.parquet`.
- Custo: ~16 ms/urna/núcleo. O Brasil inteiro, num turno, leva ~40 min com 12 processos.

## Formatos (descobertos nos dados; conferir com a especificação oficial quando disponível)
- **DER/ASN.1:** `analise/der.py` (leitor mínimo, sem esquema).
- **RDV:**
  - raiz[2] = corpo; corpo[4] = eleições (código, cargos);
  - cada cargo = (código; 1 = Presidente, qtd, votos);
  - cada voto = (tipo: 2 nominal, 3 branco, 4 nulo, 6 nulo por suspensão; número digitado).
- **vota.vsc:**
  - bloco da urna `UEAO…`/`ueao…` (maiúsculas ou minúsculas conforme o modelo);
  - cabeçalho com SHA-512 da lista e a assinatura dela;
  - lista DER de (nome, (tamanho, SHA-512, assinatura));
  - certificado da urna: PEM nas UE2020/2022, DER com bytes de preenchimento nas UE2013/2015 (recortar no tamanho declarado).
- **Assinaturas:**
  - **UE2013/2015:** ECDSA P-521 + SHA-512 sobre o hash de 64 bytes (`cryptography`).
  - **UE2020/2022:** Ed521 (E-521, p = 2^521 − 1, d = −376014; SHAKE256-132 com domínio "SigEd521"‖0‖0; mensagem = SHA-512 do hash; little-endian), em `analise/ed521.py` (gmpy2, ~3 ms). Controle negativo: 1 bit alterado → falha.
- **log.jez:**
  - zip com `logd.dat` (latin-1, TAB: data hora, nível, id urna, aplicação, mensagem, hash) e logs arquivados (`.jez` dentro do `.jez`) quando a urna reinicia ou é trocada. Ler recursivamente.
  - Sequência de um eleitor: "Aguardando digitação…" → identificador → foto/digital → "Tipo de habilitação [biométrica]" ou "habilitação manual" ou "Solicita digital do mesário" → "Eleitor foi habilitado" → "Voto confirmado para [cargo]" ou "Atribuido voto nulo por suspensão [cargo]" → "O voto do eleitor foi computado". Ver `analise/seqlog.py`.
- **imgbu.dat:** texto do boletim impresso (latin-1) dentro de um envelope binário; bloco "PRESIDENTE".

## Validação obrigatória ao mudar o leitor
Rode numa UF pequena (AC) e numa com urnas antigas (MS). Tudo tem que dar 100%:
- `assin_lista_ok`, `hash_ok_*`, `assin_ok_*`;
- RDV = BU, log = comparecimento;
- confirmações + nulos por suspensão = total;
- `cert_igual_log`.

Um resultado abaixo de 100% é, primeiro, suspeita de erro de leitura (aconteceu 4 vezes, ver CATALOGO, seção 4).
