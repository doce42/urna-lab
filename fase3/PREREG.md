# F3: pré-registro (28/10/2026, escrito antes das execuções)
Limites globais da sessão: 90 min (início 05:58), 4 scripts novos (f3_inventario.py, f3_curvas.py, f3_zeros.py, f3_pendencias.py), 8 experimentos, 1 sensibilidade por experimento, 1 correção e 1 repetição por falha, sem subagentes, sem deploy, sem push, sem congelar versão.

## E2 curvas (script f3_curvas.py; 2022 e 2026, 1º e 2º turno, mesmos métodos)
Ordem real = DT_BU_RECEBIDO do turno. Curva = Lula e adversário acumulados (válidos) conforme os boletins entram.
Estatísticas fixadas antes: S1 inversões da liderança parcial depois de 10% das urnas apuradas; S2 fração apurada na última inversão; S3 maior queda (vale) da margem relativa Lula − adversário em pontos percentuais do acumulado depois de 10%; S4 oscilações do acumulado por faixa de 1% apurado (mudanças de sinal da derivada, o T11); S5 maior trecho linear (maior sequência de faixas de 1% com erro quadrático da reta ≤ 0,02 pp).
Modelos nulos: A permutação irrestrita das urnas; B permutação dentro de UF mantendo a sequência de UFs da ordem real; C permutação dentro de município mantendo a sequência de municípios (blocos); 200 permutações por modelo (sementes 3001+). Reportar p de cauda dupla (proporção de simulações tão ou mais extremas) para cada estatística, e a comparação 2022 × 2026 pelas mesmas estatísticas. Sensibilidade: agregar em faixas de 0,5% e 2% (uma execução).
Modelo D (snapshots externos): não há, registrado como bloqueado.

## E3 zeros (f3_zeros.py)
Seções com zero votos para o adversário (Flávio 2026; Bolsonaro 2022) e, em separado, para Lula (controle e para 2022). Contagem, comparecimento positivo, tamanho, UF, transição entre turnos (0→+, +→0, 0→0), arquivos (BU/RDV/BU na Web) nas seções zero. Esperado: beta-binomial com prior por município estimado das demais seções (sobredispersão por município) e probabilidade de zero por seção = BB(0; n, a, b). Validação: observado × esperado por faixa de tamanho e controle (zeros de Lula em 2026 e de cada finalista em 2022 sob o mesmo modelo). Sensibilidade: prior por UF em vez de município.

## E4 P18 (f3_pendencias.py p18): regra do T13 com T1 e T3 de duas caudas (T1 conta zr>5 e zr<−5 acima do limiar do lado correspondente, T3 conta ≥90% para qualquer finalista), dois sentidos, 1% das urnas, 2%, 5% e 10% dos válidos, 30 réplicas, mundo de referência por bootstrap paramétrico; falsos alarmes = referência; sensibilidade = outro universo (2022).
## E5 P20 (p20): seções atípicas de São Paulo capital (2022): compartilhamento de local de votação, tamanho, comparecimento, escolaridade/perfil (2026 apenas), comparação com demais seções do mesmo local, e persistência com controle (z recalculado com termos de tamanho e do local).
## E6 P19 (p19): Moran's I do z municipal (média do z por município, divergencias_municipios_*.csv) com adjacência derivada de arcos compartilhados no geo.json (rainha por arco), 999 permutações; 2022 e 2026; sensibilidade: vizinhança dos k=5 vizinhos mais próximos pelo centróide.
## E7 (p21): tentativa controlada de obter AC URNA v2 / AC RAIZ UE por canal do TSE (no máximo 3 URLs/consultas); inventário de boletins de terceiros: sem coleta massiva.
## E8: síntese e revisão metodológica (sem execução nova).
Critério de resposta: fixado em PREREG de cada experimento acima; "respondida" só se as quatro condições do prompt (fenômeno definido, evidências verificadas, pressupostos, alcance) forem cumpridas.
