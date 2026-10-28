# Pipeline: como reproduzir e estender a análise

Guia para rodar de novo do zero e para acrescentar baterias novas rápido. Tudo fica no SSD de 1 TB (`<DISCO_GRANDE>`), nunca no disco do sistema.

## 1. Estrutura

```
apuracao-analise/
  METODOLOGIA.md   REFERENCIAS.md   CATALOGO.md   PIPELINE.md
  .venv/           Python 3.13: numpy pandas scipy pyarrow aiohttp httpx[http2] asn1crypto cryptography gmpy2
  scripts/         download e preparação
  analise/         testes e leitura dos arquivos das urnas (+ resultados *.txt / *.json / *.parquet)
  grafico/         montar_dados.py, prever.py e web/ (index.html, relatorio.html, dados JSON)
  dados/
    originais/           votação por seção BR 2026 (zip oficial) + leiame do TSE
    1turno/ 2turno/      BU na Web 2026 filtrado (só Presidente) + votação por seção por turno
    2022/                o mesmo para 2022 (originais/ zips oficiais, 1turno/ 2turno/ filtrados)
    perfil_eleitorado/   perfil por seção 2026 (zips oficiais)
    brutos/1turno/       arquivos das urnas, pacotes oficiais por UF (bu, imgbu, log, rdv, vota.vsc)
    brutos/2turno_pacotes/  idem, 2º turno (27 UFs)
    brutos/2turno/SP/    São Paulo 2º turno, urna por urna (sem pacote oficial em 27/10/2026)
    listas/              listas de URLs, logs de download/processamento, recursos.csv (consumo)
```

## 2. Ordem de execução (do zero)

Na coluna "Tempo", os valores medidos em 27/10/2026, numa máquina com 16 núcleos, 23 GB de RAM e ~500 Mbit/s.

| # | Comando | Entrada | Saída | Tempo |
|---|---|---|---|---|
| 1 | `scripts/baixar_lista.sh <lista> <pasta> 4` | listas de URL (`dados/listas/*.txt`) | zips oficiais (+ `.ok`, confere `.sha512` quando existe) | ~64 MB/s |
| 2 | `unzip -p … \| .venv/bin/python -I scripts/filtrar_presidente.py /dev/stdin <saída>` | BU na Web por UF | `bweb_<t>t_<UF>_presidente.csv` (UTF-8) | segundos/UF |
| 3 | `.venv/bin/python analise/montar_base.py [2026\|2022]` | BU filtrado dos 2 turnos | `analise/base.parquet` (ou `base_2022.parquet`): uma linha por seção, 2 turnos lado a lado | ~1 min |
| 4 | `python3 -I grafico/montar_dados.py` | BU filtrado + votação por seção | `grafico/web/dados.json` (**para se os totais não baterem**) | ~1 min |
| 5 | `.venv/bin/python grafico/prever.py` | base + dados.json | curva prevista dentro de `dados.json` (rodar **depois** do 4) | ~30 s |
| 6 | `.venv/bin/python analise/bateria.py <ano>` | base | `resultado_bateria_<ano>.json` (T02–T05, T07, T10, T11, T21, T22) | ~3 min |
| 7 | `analise/curva.py`, `poder.py`, `biometria.py`, `perfil.py` | base, perfil | `resultado_*.txt/json`, `curva_2turno_por_minuto.csv`, `perfil.parquet` | 1–3 min cada |
| 8 | `.venv/bin/python analise/processar_brutos.py <turno> [UF…]` | arquivos das urnas | `analise/brutos/<t>t/urnas_<UF>.parquet` e `minutos_<UF>.parquet` | ~16 ms/urna/núcleo; 12 processos |
| 9 | `.venv/bin/python analise/relatorio_dados.py` | tudo acima | `grafico/web/relatorio_dados.json`, `grafico/web/logs.json` | ~1 min |
| 10 | `cd grafico/web && python3 -m http.server 8765 --bind 127.0.0.1` | — | http://localhost:8765 (gráfico) e /relatorio.html | — |
| 11 | `chromium --headless --print-to-pdf=relatorio.pdf http://127.0.0.1:8765/relatorio.html` | página | `grafico/web/relatorio.pdf` | segundos |

Rode tudo que é pesado com `nice -n 10 ionice -c3` para não travar o computador.

## 3. Como acrescentar uma bateria nova

1. Escreva a hipótese e o esperado **antes** (METODOLOGIA, seção 1).
2. Acrescente a função em `analise/bateria.py`:
   - grave em `R["T<nn>"] = {...}`;
   - documente no cabeçalho do arquivo;
   - use a próxima numeração livre do CATALOGO (T23 em diante).
3. Rode nos dois anos: `for a in 2022 2026; do .venv/bin/python analise/bateria.py $a; done`. O 2022 serve de referência.
4. Se o teste acusar algo, procure o artefato antes de concluir. Os padrões conhecidos estão no CATALOGO, seção 4: teto de 0/100%, inclinação, fuso, seção agregada, arquivo cortado, voto órfão.
5. Para medir poder: injete a fraude sintética no cenário certo (`analise/poder.py`) e veja se o teste novo pega.
6. Registre no `CATALOGO.md` (seções 1, 3 e 4) e, se for para o relatório, acrescente em `relatorio_dados.py` e `relatorio.html`.

## 4. Dicionário de dados

### `analise/base.parquet` (uma linha por seção; sufixo `_1` = 1º turno, `_2` = 2º turno)
- Chave: `SG_UF`, `CD_MUNICIPIO` (texto, sem zeros à esquerda), `NR_ZONA`, `NR_SECAO`
- Votos:
  - `v<NN>_<t>`: votos no candidato de número NN (13 = Lula; 22 = Flávio em 2026, Bolsonaro em 2022);
  - `branco_<t>`, `nulo_<t>`, `validos_<t>`, `total_<t>`.
- Horários (datetime, **hora local da urna**, exceto `DT_BU_RECEBIDO`, que é horário de Brasília):
  - `DT_ABERTURA`, `DT_ENCERRAMENTO`, `DT_EMISSAO_BU`, `DT_BU_RECEBIDO`.
- Outros:
  - `QT_APTOS`, `QT_COMPARECIMENTO`;
  - `QT_ELEI_BIOM_SEM_HABILITACAO` (liberados sem biometria);
  - `NR_URNA_EFETIVADA`;
  - `DS_SECOES_AGREGADAS`.
- Fuso: a abertura é às 8h de Brasília, então `8 − hora local de abertura` dá o fuso. Use a moda do município, só com urnas que abriram nos primeiros 15 min.

### `analise/brutos/<t>t/urnas_<UF>.parquet` (uma linha por urna)
- **Log:**
  - `modelo` (UE2013/2015/2020/2022);
  - contagens de eventos: `computado` (votos computados), `conf_presidente`, `nulo_suspensao_presidente`, `corrigiu`, `habilitado`, `digital_tentativa`, `sem_biometria`, `tecla_indevida`, `aplicacao_iniciada`, `impressao`;
  - `primeiro_voto` e `ultimo_voto` (hora local);
  - `arquivos_log` (mais de 1 = log arquivado);
  - `ids_urna_log` e `urnas_com_voto_no_log` (mais de 1 = urna substituída).
- **Boletim impresso** (1º turno): `img_v<NN>`, `img_branco`, `img_nulo`, `img_total`, `img_comparecimento`.
- **RDV:**
  - `rdv_v<NN>`, `rdv_branco`, `rdv_nulo`;
  - `rdv_tipo<N>` para outros tipos (6 = nulo por suspensão, somar ao nulo).
- **Assinatura:**
  - `algoritmo` (Ed521 / ECDSA-P521), `cert_urna`, `cert_emissor`;
  - `assin_lista_ok`;
  - `hash_ok_<bu|rdv|imgbu|log>` e `assin_ok_<…>`;
  - `cert_igual_log`.
- **Erros:** `erro` (texto, quando algum arquivo não pôde ser lido).

### `analise/brutos/<t>t/minutos_<UF>.parquet`
- `SG_UF`, `CD_MUNICIPIO`, `minuto` (dd/mm/aaaa hh:mm, hora local), `votos` (votos computados naquele minuto)

## 5. Formatos dos arquivos das urnas (descobertos nos dados; ver METODOLOGIA, camada A)
- **DER/ASN.1:** leitor mínimo em `analise/der.py`, sem esquema.
- **RDV:**
  - raiz → [2] corpo → [4] eleições;
  - cada eleição = (código, cargos); cada cargo = (código, qtd, votos);
  - cada voto = (tipo, número digitado). Cargo 1 = Presidente; eleição 6257 = 1º turno, 6258 = 2º turno.
- **`vota.vsc`:**
  - bloco da urna `UEAO…`/`ueao…`: (data, versão, cabeçalho (…, (alg, SHA-512 da lista, assinatura da lista)), lista DER, certificado);
  - lista = sequência de (nome, (tamanho, SHA-512, assinatura)).
- **`log.jez`:**
  - zip com `logd.dat` (texto latin-1, separado por TAB: data hora, nível, id da urna, aplicação, mensagem, hash);
  - pode conter outros `.jez` dentro, com logs arquivados.
- **`imgbu.dat`:** texto do boletim impresso (latin-1), com um envelope binário.

## 6. Armadilhas já encontradas
- **Disco:** nunca extrair zip grande no disco do sistema. Prefira `unzip -p | filtro` direto para o destino.
- **`pkill -f <padrão>` mata o próprio comando** quando o padrão aparece na linha de comando. Use `pgrep -f "[p]adrão"` com `kill`.
- **Portal de dados abertos:**
  - às vezes lista o `.sha512` no lugar do zip (Roraima, BU 2º turno);
  - às vezes não lista pacotes que já estão no CDN (arquivos das urnas do 2º turno). Teste o endereço direto.
- **Site de resultados:** limita **conexões** simultâneas (HTTP 429), não pedidos. Use HTTP/2 multiplexado (`curl -Z --http2 --parallel-max 150 -K lista`). Com aiohttp (HTTP/1.1), 96 conexões viram recusa e espera.
- **Seções agregadas:** não têm urna própria (o índice dá 404). Não é erro.
- **2022:** usa `DS_AGREGADAS` e `QT_ELEITORES_BIOMETRIA_NH` no lugar dos nomes de 2026, e as datas vêm como dd/mm/aaaa.
- **Certificados das urnas UE2013/UE2015:** trazem bytes de preenchimento depois do DER. Recorte no tamanho declarado.
- **Gráfico:** a lightweight-charts espaça os pontos por quantidade, não por tempo. Preencha todos os segundos ou minutos.

## 7. Rodada 7 e Operação Veracidade (V1.5)
**Ordem para reproduzir** (detalhes em `operacao_veracidade/REPRODUCAO.md`):
1. `fase3/rdv_nulos.py <ano> <turno>` (uma vez por ano e turno; ~8 min com 12 processos): lê o número digitado em cada voto nulo e branco no RDV, por seção. Depois `fase3/rdv_nulos_analise.py` (T58 e T59).
2. `operacao_veracidade/scripts/cert_extrai.py <ano> <turno> 12` (13 a 25 min por combinação), depois `cert_analise.py`, `casos_certificado.py`, `casos_A_relidos.py` (T60a).
3. `controles_mutacao.py <ano> <UF>`, `ed521_unitarios.py` (T60b); `terceiros_qr.py`, `terceiros_qr_relogio.py`, `republicacao_bu.py` (T61); `identificabilidade.py` (T62).
4. `sim_adversarial.py <ano> 6 20`, `sim_fabricacao_v2.py <ano> 20`, `gera_tabelas_sim.py` (T63, ~1 min por ano); `zeros_contagens.py`, `zeros_locais.py` (T64); `hipotese_video.py`, `hipotese_video_m6.py` (T65).
5. Regerar `fase3/f3_veredito.py`, `f3_inventario.py`, `f3_respostas.py`, `scripts/verificar.py`, build do site.

**Dados derivados novos (fora do git, reproduzíveis):** `operacao_veracidade/resultados/certs_<ano>_<turno>t.parquet` (uma linha por seção: UF, município, zona, seção, `cert_sha256`, `alg`, `cn`, `emissor`, `nao_antes`, `nao_depois`, `pub_sha256`, `cadeia_ok`, `valido_no_dia`, `emitido_depois_da_eleicao`, `erro`; ~75 MB cada) e `fase3/resultados/rdv_nulos_<ano>_<turno>t.parquet` (seção, cargo, tipo de voto, dígitos, quantidade) com `_gov.json` (números com voto nominal para governador por UF). O `.gitignore` os exclui porque o `publicar.py` recusa arquivo > 20 MB e total > 120 MB.
**Dados externos (terceiros, fora do git, SHA-256 em `operacao_veracidade/externo/arvor_totalizacao/SHA256SUMS.txt`):** arquivos estáticos públicos de um projeto de totalização paralela (404 boletins do 2º turno de 2026); a licença de redistribuição não foi verificada.

**Armadilhas novas:**
- **O log de um pacote pode trazer logs arquivados de outras urnas e de outras seções** (contingência: ES 57932/9/85, 612 eventos de voto para 308 votos). Contar eventos por **data da eleição, ID de urna e seção declarada**, nunca o total do pacote.
- **Fuso:** `DT_ENCERRAMENTO` e `DT_EMISSAO_BU` estão em hora local; `DT_BU_RECEBIDO` está em hora de Brasília. O fuso do município vem da abertura às 8h de Brasília. "Antes das 19h" é do **dia** da eleição, não da hora de qualquer dia.
- **`dict.setdefault(k, zipfile.ZipFile(p))` reabre o zip a cada chamada** (o argumento é sempre avaliado): guarde o objeto e o conjunto de nomes em cache.
- **BU e RDV omitem candidato com zero voto:** ausente = 0 ao comparar, quando o arquivo foi lido; senão milhares de falsas divergências.
- **O tipo 6 do RDV (nulo sem número)** é somado ao nulo em 2022; seções só com tipo 6 ficam fora do comparador se isso não for tratado.
- **A verificação de lista (`assin_lista_ok`) usa o certificado embutido no mesmo arquivo:** é autoconsistência. Só a cadeia (`cert_extrai.py`) autentica até a AC emissora. `assin_ok_<tipo>` assina o **hash da lista**, não o arquivo: use sempre junto com `hash_ok_<tipo>`.
- **A página oficial de certificados do TSE responde HTTP 403 a este ambiente:** não contornar.
- **`rodada.py fechar --incluir` agora ignora arquivos que o git ignora** (antes copiou por engano `scripts/.privado.txt` e 43 logs na rodada 6).
