# 02. Auditoria documental e criptográfica

Princípio: **hash correto ≠ assinatura válida ≠ cadeia autenticada ≠ voto fiel à intenção do eleitor.** Cada degrau foi medido separadamente. Scripts em `scripts/`, saídas em `resultados/`, protocolo em `PROTOCOLO_PRE_EXECUCAO.md`.

## 1. Auditoria do código dos verificadores
| Componente | O que faz | Observação hostil | Efeito nos resultados anteriores |
|---|---|---|---|
| `ler_vsc` (lista assinada) | confere SHA-512 da lista e a assinatura da lista **com o certificado embutido no mesmo arquivo** | só prova autoconsistência: um certificado e uma lista gerados por qualquer par de chaves passam (T60b, controle sintético). A cadeia até a AC **não fazia parte do pipeline**; só havia sido conferida em 200 seções (P11) e, por terceiro, em 5% | a frase "todos verificados até a AC emissora" (Q5) não estava sustentada até esta operação; agora está (T60a) |
| `hash_ok` e `assin_ok` por arquivo | `hash_ok` compara o SHA-512 do arquivo com o da lista; `assin_ok` verifica a assinatura **do hash da lista**, não do arquivo | uma alteração do arquivo **não é detectada por `assin_ok`** (T60b: 0 de 40 rejeições por esse campo) e **é detectada por `hash_ok`** (40 de 40). O uso de `assin_ok` isolado seria enganoso | verificado em 3 pontos de uso (`processar_brutos.py`, `f2_completa.py`, P16): sempre emparelhado com `hash_ok` e `lista_ok`; nenhum resultado herdado depende de `assin_ok` sozinho |
| Ed521 (`ed521.verifica`) | EdDSA em E-521; M = SHA-512 do hash; rejeita ponto degenerado e S fora da faixa | 9 testes unitários (`ed521_unitarios.json`): controle genuíno aceito; hash alterado, bit de R, bit de S, S + L (não canônica), assinatura truncada, **chave e R neutros com S = 0**, chave de outra urna e chave vazia: todos **rejeitados** | sem efeito; reforça o R1-02 |
| ECDSA P-521 (`_verificador`) | assinatura DER; se falha, relê r e s e reconstrói a forma canônica | aceita uma codificação não canônica dos **mesmos** inteiros r e s; não enfraquece a segurança, mas esses casos não são "estritos". Nos 85 QR de ECDSA de terceiros: 0 casos de DER não canônico | sem efeito |
| P11 (cadeia de 200 seções) | testava 3 variantes de mensagem (TBS, SHA-512(TBS), SHA-512(SHA-512(TBS))) e aceitava a que validasse | procurar variantes diminui a força de cada aceite; todas validaram com `M = TBS` | T60a usou **só `M = TBS`**, sem busca: 100% |
| Certificados das ACs | AC URNA, AC UE2020 e AC UE2022 | vêm de repositório de terceiro; o SHA-256 está registrado (`cert_analise.json`); o SHA-512 oficial do TSE só é citado por terceiro; a página oficial responde HTTP 403 | limite declarado; raiz continua sem verificação |

## 2. T60a: cadeia de certificados em 100% das urnas
Extração do certificado de cada `vota.vsc`/`.vscmr` e verificação da assinatura da AC emissora (Ed521 com M = TBS fixo; ECDSA por `verify_directly_issued_by`), validade na data da eleição, unicidade. Evidência: `resultados/certs_<ano>_<turno>t.parquet` (uma linha por seção), `cert_analise.json`, `casos_certificado.csv`.

| Conjunto | Seções com certificado | Certificados únicos | Cadeia verifica | Falha | Válidos no dia | Emitidos depois da eleição | Chave pública repetida em CN diferentes |
|---|---|---|---|---|---|---|---|
| 2022, 1º turno | 471.908 | 471.906 | **471.908** | 0 | 471.908 | 0 | 0 |
| 2022, 2º turno | 471.984 | 471.983 | **471.984** | 0 | 471.984 | 0 | 0 |
| 2026, 1º turno | 499.176 | 499.176 | **499.176** | 0 | 499.176 | 0 | 0 |
| 2026, 2º turno | 499.178 | 499.177 | **499.178** | 0 | 499.178 | 0 | 0 |

Total: 1.942.246 pares seção × turno, **0 falhas de cadeia**, 0 erros de leitura, 0 CN com dois certificados, 0 certificado igual em CN diferentes. Por emissor: 2026, AC UE2020 400.967, AC UE2022 397.503, AC URNA 199.884 (2 turnos somados); 2022, AC UE2020 385.333, AC URNA 558.559.

**O que isso prova e o que não prova:** prova que **todo** certificado de urna é assinado pela chave pública da AC emissora que temos, que estava válido no dia, e que nenhuma chave de urna se repete. Não prova que a raiz é do TSE (AC RAIZ UE e AC URNA v2 não são públicas) nem que a AC que usamos é a oficial (cópia de terceiro). **Fecha a lacuna dos 200 casos do P11 e dos 5% de terceiros.**

**Achados menores, não-conclusivos sobre votos (detalhes em `06_ANOMALIAS_E_LOGS.md`):**
- Certificados emitidos depois do fim da validade do certificado público da AC URNA (18/07/2026): 45 (1º turno) e 53 (2º), todos verificam com a chave publicada, o que é compatível com renovação não publicada.
- Troca de urna entre turnos: 4.429 seções em 2026 (0,89%) e 12.540 em 2022 (2,66%), coerentes com a tabela em 4.423 e 12.533 delas.
- Modelo declarado no log × AC emissora: 132 + 87 (1º) e 216 + 182 (2º) em 2026, com datas coerentes com recertificação; não há regra pública.
- 17 seções em 2026 e 22 em 2022 com o certificado de outra urna que a da tabela; relidas por ID e data, em 16 de 17 de 2026 a urna da tabela registrou o comparecimento do BU (compatível com contingência, explicação que vem do próprio log); o 17º tem três identificações diferentes e votos iguais.

## 3. T60b: o verificador rejeita adulterações? (controles positivos e negativos)
Cópias em memória de 40 seções reais (AC 2026 e AL 2022, 2º turno). Cada célula é "quantas das 40 foram rejeitadas por esse controle".

| Mutação | Hash do arquivo × lista | Assinatura do arquivo | Assinatura da lista | Rejeitada por algum |
|---|---|---|---|---|
| 0. genuíno (controle positivo) | 0 | 0 | 0 | **0 de 40** (nenhum falso positivo) |
| 1. um byte alterado no BU | **40** | 0 | 0 | 40 |
| 2. BU truncado | **40** | 0 | 0 | 40 |
| 3. um byte alterado na lista | 0 | 0 | **40** | 40 |
| 4. um byte alterado na assinatura da lista | 0 | 0 | **40** | 40 |
| 5. certificado de outra urna | 0 | 40 | 40 | 40 |
| 6. arquivo fora da lista | 40 | 40 | 0 | 40 |
| 7. nome trocado | 40 | 0 | 0 | 40 |

Resultado idêntico em 2026 (AC) e em 2022 (AL). **Controle hostil sintético** (chave ECDSA P-521 descartável, certificado autoassinado, em memória): a verificação de lista **aceita** os dois (um com emissor desconhecido, outro **declarando ser "AC URNA"**); a verificação de cadeia dá `None` para o emissor desconhecido e **`False` para o que declara ser a AC URNA**. Isto confirma que só a cadeia separa um certificado forjado de um oficial, e que a verificação de lista sozinha não autentica.

## 4. Comparações documentais e de versões
| Comparação | Resultado | Fonte |
|---|---|---|
| Tabela × BU × RDV × imagem (seção a seção) | 0 diferenças nas seções lidas, 2022 e 2026 | Q1, Q2, T01 (interna) |
| **BU de terceiros (QR Code impresso) × tabela × BU do TSE (T61)** | **404 de 404 iguais** (votos de Lula e Flávio, brancos, nulos, comparecimento, aptos); assinatura da urna válida em 404 de 404 (319 Ed521, 85 ECDSA), `hash_final` = SHA-512 do conteúdo em 404; cadeia até a AC em 404; urna do QR = urna da tabela = certificado do `vota.vsc` em 404; 0 certificado repetido | `terceiros_qr.json` (externa parcial) |
| **Republicação (H-C): `bu.dat` baixado por terceiros do TSE (25 a 28/10) × o nosso (27 e 28/10)** | **404 de 404 SHA-256 idênticos** | `republicacao_bu.json` |
| Capturas históricas da divulgação × base final | 39 instantes, diferença máxima 0,083 ponto percentual, mesmo líder, total final igual | Q6, Q14 |
| Decodificação por terceiro (DataUrnas-BR) | 99,96% (2022) e 100% (2026, 1º turno) das seções comuns | R1-20 (implementação independente) |
| Arquivos ausentes | 173 arquivos assinados pela urna e 485 auxiliares fora do pacote de 2022; não é divergência de votos | A173 |
| Sistema de Apuração de 2022 | 159 seções-turno lidas, 0 divergências | SA22 |

Ausência de arquivo não é divergência de votos e não foi tratada como tal.

**Limites do T61 e da republicação:** os 404 boletins são uma amostra de conveniência (0,08% das seções, 22 UFs, 167 de SP), coletada e publicada pelo mesmo projeto, só do 2º turno de 2026; o relógio do servidor deles não é auditado; o `tse_sha256` que eles registram é uma declaração deles, confirmada aqui pela igualdade com o nosso download. A evidência tem **cadeia de obtenção diferente**, mas a assinatura é da mesma urna: prova que o que foi impresso na seção é o que o TSE publicou, não que o impresso reflita o voto.

## 5. Divergências objetivas
1. **Nenhuma divergência de votos entre fontes** em nenhum dos testes novos.
2. **Lacunas documentais objetivas (S4), sem efeito em votos:** 98 certificados emitidos depois da validade do certificado público da AC URNA; certificado ≠ urna da tabela em 17 seções de 2026 e 22 de 2022 (um caso com três identificações diferentes); a regra de emissão por modelo não é pública; a cadeia não chega à raiz.
3. **Artefato do projeto descoberto:** o leitor do log conta eventos de voto de logs arquivados de **outras urnas e seções** embutidos no pacote (caso ES 57932/9/85: 612 eventos para 308 votos). Pode contaminar casos herdados de "log ≠ comparecimento" (T14, T36); recomenda-se relê-los por data, ID de urna e seção.
