# Rodada 4 (V1.2): desvios no congelamento

Este arquivo fica fora da pasta congelada e **não altera** `rodadas/rodada-4/`.

1. **Arquivos acrescentados depois de congelar.** A rodada 4 foi fechada por `scripts/rodada.py fechar 4 V1.2` às 12:49:46 de 28/10/2026. O `resumo.json` registra SHA-256 de 30 arquivos (resultados de `analise/` e o registro). Às 12:50:03, 17 s depois, foram copiados para a pasta `CONCLUSAO.md`, `INVENTARIO.md` e `fase3_resultados/`, que não constam do `resumo.json`. Os SHA-256 desses arquivos, calculados em 28/10/2026 na auditoria, estão abaixo. Eles servem para detectar mudança daqui em diante, **não** provam o conteúdo no instante da cópia.
2. **Sem `proveniencia.json`.** A rodada 3 tem; a rodada 4 não. Ele não foi gerado depois para não inventar proveniência.
3. **Encerramento antes da auditoria.** A F3 foi marcada como concluída e congelada antes de uma revisão científica. A auditoria (`fase3/AUDITORIA_F3.md`) encontrou problemas de classificação e de método. Com aprovação do responsável, a F3 voltou a "em revisão" na linha do tempo viva. A V1.2 e a tag `v1.2` ficam como estão, como registro do que foi publicado naquele momento.

## SHA-256 dos arquivos acrescentados (calculados na auditoria)
    d38c507507f6208be0cdcdbc520bcf4e5f0be19272cb25693fd67cd3bf205091  CONCLUSAO.md
    cda232ba5715b315adc4410a87cc53aa47dbd09fed5aa5f14ae887992dbc85b7  INVENTARIO.md
    867a6650a4d5a02c07d4721b18be08231fc0fd0b14b034636054ce21dc4ad4fb  fase3_resultados/E2b_curvas.json
    37f75708fa24a340dbb3ecda792172b1b0085d1d5b2facfc9df3e90890bdb1bd  fase3_resultados/E2_curvas.json
    cb8396568cf1807a5b106d7fecdc04369e75372e334f411e584265920123e8d6  fase3_resultados/E3_zeros.json
    7dd47be123c63b32784d79349f42dede7486f6ce592827bdfe09097482b9cf72  fase3_resultados/p18.json
    ef7e6eb79753d7f7a8ff705c27014cac096f71ece9bd94ce020a68ba9471f743  fase3_resultados/p19.json
    43680b001bde54d03707a0d02c61579efa606db9bd8b6625c004fdb0ef254c2d  fase3_resultados/p20.json
    719dcf94dd30d26e707cdc59b7ee7dcb441e510826ef6cda006bc8f619a403b3  fase3_resultados/R1_20_dataurnas.json
