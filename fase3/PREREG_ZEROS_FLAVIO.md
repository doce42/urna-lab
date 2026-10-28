# Pré-registro: "Flávio teve zero voto em 106 urnas" (T49)

Escrito em 28/10/2026, antes de qualquer contagem. Fonte da alegação: Folha da Política, 27/10/2026, com dados atribuídos à "Paris Group" (mapeamento por IA, sem metodologia publicada). A matéria é só a origem da pergunta; a resposta vem dos dados do TSE.

**Alegações:** (1) no 2º turno de 2026, 106 seções com 0 voto para Flávio (22), somando 14.860 votos de Lula (13); (2) por região: Norte 65, Nordeste 29, Centro-Oeste 6, Sudeste 3, Sul 3; (3) Amazonas: 13 municípios citados; uma seção de Tabatinga com 354 × 0; (4) Lula venceu no 2º turno em 211 municípios onde Flávio liderou no 1º; 76 em MG; Rio de Janeiro com vantagem de 644 mil.

**Medidas (determinísticas e descritivas):**
- (a) Reproduzir (1) a (4) com `analise/base.parquet`: seção com `v22_2 == 0` e `validos_2 > 0`; exterior (ZZ) contado à parte.
- (b) Mesma definição em 2022 (Bolsonaro 0 no 2º turno), para comparar quantidade, votos e regiões.
- (c) Continuidade: nas seções zeradas de 2026, a proporção de Bolsonaro em 2022 (mesma UF, município, zona e seção) e o voto de Flávio no 1º turno de 2026. Se a seção já era quase toda de Lula em 2022, o padrão é local e anterior.
- (d) Integridade dessas seções nos arquivos da urna: assinaturas válidas e BU = RDV = tabela (como no T45, com ausente = 0).
- (e) Municípios em que o líder mudou entre turnos, em 2026 e em 2022.

**Leitura pré-fixada:** reprodução aceita se a contagem bater exatamente (ou a diferença tiver definição identificável). Em votos: o total das seções zeradas contra a margem de 4.430.191. Sinal: S0 se reproduzido, contínuo com 2022 e íntegro; S3 se houver seções zeradas sem histórico (proporção de Bolsonaro em 2022 ≥ 20%) que não se expliquem por mudança de seção; S4 se houver divergência de arquivos.

Orçamento: 1 execução + 1 correção. Script `fase3/zeros_flavio.py`, saída `fase3/resultados/zeros_flavio.json`.
