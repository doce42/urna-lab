---
name: apuracao-integridade
description: Ler e verificar os arquivos gravados por cada urna (log, BU, RDV, imagem do BU, assinaturas vota.vsc) — assinatura Ed521/ECDSA, hashes, recontagem do RDV, sequência eleitor a eleitor do log. Use para os testes T14–T17, T24, T28–T31, T33–T35 ou ao mexer em analise/processar_brutos.py, der.py, ed521.py, seqlog.py. Desde a rodada 7: cadeia de certificados em 100% das urnas (T60a), controles de mutação (T60b), boletins de terceiros (T61), identificabilidade (T62) e a regra de que o log de um pacote traz logs de outras urnas e seções.
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

## Lições da F2 e da F3 (leia antes de mexer nos arquivos das urnas)
- **Nulo por suspensão em 2022:** o leitor de 2022 já soma o tipo 6 em `rdv_nulo` e o grava também em `rdv_tipo6`. Não some de novo. Em 2026 é preciso somar.
- **Sistema de Apuração:**
  - 2022: o leitor geral não reconhece `.busa`, `.imgbusa`, `.logsajez` e `.vscsa`. Leitura à parte em `fase3/ver_sa22.py` (159 seções-turno) e `fila_f3_semboletim.py`.
  - 2026: os `-sa.vsc` não são conferidos pelo leitor; conferência à parte em `fase3/fila_f2_sa2026.py`.
- **Log de 2022:**
  - O 3º campo da linha **não é** o número da urna em parte dos logs (o mesmo valor aparece em vários estados). `ids_urna_log` e `urnas_com_voto_no_log` não valem para 2022.
  - "Certificado ≠ urna do log" ocorre em 59% das seções e não indica troca de urna.
- **Parquet de 2022:** gerado com versão anterior do leitor de boletim (5 seções sem votos lidos). Regerar com `processar_brutos.py` atual se for usar boletins de 2022.
- **"Verificação de assinatura … [ERRO]" no log:** quase sempre fora do dia da eleição, e as do dia são seguidas de sucesso (`fase3/final_t33.py`). O leitor conta como falha qualquer linha sem SUCESSO.
- **Investigações por arquivo:** `fase3/inv_r1_integridade.py` (tabela × bu × RDV × imagem, 2022 e 2026), `ver_a173.py`, `ver_bu1.py`, `fila_f1_log2022.py` (log × comparecimento 2022).
- **Regra adversarial:** concordância entre arquivos da mesma urna é consistência interna (skill apuracao-investigacao).

## Atualização da rodada 7 (28/10/2026, V1.5)
- **T60a:** `operacao_veracidade/scripts/cert_extrai.py` verifica a assinatura da AC emissora de cada certificado (Ed521 com M = TBS fixo; **não** tente variantes) em todas as urnas; 1.942.246 de 1.942.246 em 2022 e 2026. As ACs são cópia de terceiro em `fase2/externos/certificados/`; a raiz não é pública.
- **`assin_lista_ok` é autoconsistência** (certificado embutido no mesmo arquivo). `assin_ok_<tipo>` assina o hash da lista, não o arquivo: use sempre com `hash_ok_<tipo>` (T60b: byte alterado no BU, 40 de 40 pelo hash e 0 pela assinatura do arquivo).
- **Verificação em três vias:** certificado (emitido antes pela AC), tabela do TSE (urna efetivada) e log (ID da urna) têm origens parcialmente distintas; diferença entre elas é achado (17 seções em 2026, 22 em 2022), lido por data, ID e seção.
- **Log de pacote traz logs de outras urnas e seções** (contingência): conte eventos de voto por data da eleição, ID e seção declarada.
- **T61:** boletim de terceiros pelo QR Code: `hash_final` = SHA-512 do conteúdo; mesma assinatura da urna, cadeia de obtenção diferente; amostra de conveniência não se extrapola; relógio do servidor de terceiros não é auditado.
- **T62:** verificações de consistência não separam registros coerentes assinados pela fonte dos genuínos; mede o limite, não a possibilidade operacional.
- A página oficial de certificados do TSE responde HTTP 403 a este ambiente: não contornar.
