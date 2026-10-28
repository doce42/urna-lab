# Mapa de skills, testes e arquivos

Cada skill (`.agents/skills/<nome>/SKILL.md`) cobre um domínio do estudo. Este mapa diz qual skill um agente deve carregar para cada tarefa, teste ou arquivo.

```
                          ┌────────────────────────────┐
                          │    apuracao-metodologia     │  protocolo, critérios, autoauditoria,
                          │  (rege todas as outras)     │  catálogo, referências, registro
                          └──────────────┬─────────────┘
          ┌───────────────┬──────────────┼───────────────┬──────────────────┐
          ▼               ▼              ▼               ▼                  ▼
  apuracao-dados  apuracao-integridade  apuracao-forense  apuracao-comportamento  apuracao-relatorio
  (baixar/preparar,  (arquivos das urnas)   (testes estatísticos,  (eleitor, mudança,        (site React,
   preservação)                              poder, curvas, zeros)  divergências, perfil)      relatório)
          └───────────────┴──────────────┬───────────────┴──────────────────┘
                     ┌───────────────────┴────────────────────┐
                     ▼                                        ▼
            apuracao-investigacao                    apuracao-versoes
   (hipóteses de fraude, veredito, sinal,     (rodadas, congelamento, provas,
    regra adversarial, respostas, fila)        publicação, preservação, dados leves)
```

## Por skill

| Skill | Módulo do PROTOCOLO | Testes | Arquivos principais |
|---|---|---|---|
| apuracao-metodologia | todos | (rege todos) | `PROTOCOLO.md`, `METODOLOGIA.md`, `AUTOAUDITORIA.md`, `CATALOGO.md`, `REFERENCIAS.md`, `testes/registro.json` |
| apuracao-dados | entrada | T01 (conferência na preparação) | `scripts/listas_tse.py`, `preparar_dados.sh`, `baixar_lista.sh`, `baixar_sp_2t_educado.py`, `filtrar_presidente.py`, `secao_presidente.py`, `analise/montar_base.py` |
| apuracao-integridade | A | T14, T15, T16, T17, T17b, T24, T28, T29, T30, T31, T33, T34, T35 | `analise/processar_brutos.py`, `der.py`, `ed521.py`, `seqlog.py` |
| apuracao-forense | D | T02, T03, T04, T05, T07, T10, T11, T13, T13b, T21, T22, T23, T25, T26, T27; T19 (2022) | `analise/bateria.py`, `poder.py`, `curva.py` (histórico: `testes.py`, `investigar.py`, `testes_corrigidos.py`) |
| apuracao-comportamento | B, C, E | C01, C02, C03, C06, C07, C08, T09, T12, T20, E01, E02, E03 | `analise/comportamento.py`, `perfil.py`, `biometria.py`, `grafico/prever.py` |
| apuracao-relatorio | produtos | (apresenta todos) | `grafico/montar_dados.py`, `grafico/web/index.html`, `relatorio.html`, `analise/relatorio_dados.py`, `grafico/montar_relatorio_pdf.py` (PDF), `grafico/relatorio-app/` (site) |
| (totalização) | A | T32 | `analise/totalizacao.py` (skill apuracao-integridade) |
| apuracao-investigacao | F3 | T40–T44, H1–H10, Q1–Q26, inventário de 33 itens | `fase3/f3_veredito.py`, `f3_respostas.py`, `f3_inventario.py`, `PREREG_*.md`, `RELATORIO_ADVERSARIAL.md`, `inv_*.py`, `fila_*.py`, `final_*.py`, `teste_grandes_cidades.py` |
| apuracao-investigacao | rodadas 6 e 7 (V1.4, V1.5) | T45–T65, Q27–Q50, N1–N9 | `fase3/PREREG_*.md` (T45–T59), `fase3/live_2022.py`, `zeros_flavio.py`, `thread_concentracao.py`, `crescimento_turnos.py`, `posts_arvor.py`, `cabo_frio.py`, `brancos_nulos.py`, `nulos_governador.py`, `rdv_nulos.py`, `rdv_nulos_analise.py` |
| apuracao-integridade | Operação Veracidade | T60a, T60b, T61, T62 | `operacao_veracidade/scripts/cert_extrai.py`, `cert_analise.py`, `cadeia.py`, `controles_mutacao.py`, `ed521_unitarios.py`, `terceiros_qr.py`, `republicacao_bu.py`, `identificabilidade.py`, `caso_ES.py` |
| apuracao-forense | Operação Veracidade | T63, T64, T65 | `operacao_veracidade/scripts/sim_adversarial.py`, `sim_fabricacao_v2.py`, `zeros_contagens.py`, `hipotese_video.py` |
| apuracao-forense | rodada 8 (aberta) | T66–T70, Q51–Q56 | `fase3/PREREG_RELATORIO_PERICIAL.md`, `fase3/relatorio_pericial.py`, `fase3/relatorio_pericial_r2b.py` |
| apuracao-versoes | governança | (todas as versões) | `scripts/rodada.py`, `rodadas/`, `scripts/publicar.py`, `scripts/manifesto.py`, `scripts/carimbo.py`, `scripts/dados_leves.py`, `DADOS_PRESERVACAO.md` |

## Por tarefa

| Quero… | Carregue |
|---|---|
| reproduzir tudo do zero | apuracao-dados → `make dados-do-zero` |
| acrescentar um teste estatístico | apuracao-metodologia + apuracao-forense |
| acrescentar um teste sobre logs, assinatura ou RDV | apuracao-metodologia + apuracao-integridade |
| entender o que mudou entre os turnos | apuracao-comportamento |
| incluir outra eleição (ex.: 2018) | apuracao-dados + apuracao-forense (rodar `bateria.py` com o ano) |
| atualizar o relatório ou o PDF | apuracao-relatorio |
| revisar se uma conclusão se sustenta | apuracao-metodologia (fluxo de 5 perguntas) + `AUTOAUDITORIA.md` + regra adversarial (apuracao-investigacao) |
| investigar uma anomalia ou hipótese de fraude | apuracao-investigacao (+ a skill do domínio) |
| atualizar a resposta central, as respostas ou o sinal de um teste | apuracao-investigacao → regerar veredito, inventário e respostas |
| encerrar uma fase, publicar, criar tag ou fazer deploy | apuracao-versoes |
| testar uma alegação pública (matéria, post, vídeo, live) | apuracao-investigacao (alegação vira pré-registro `fase3/PREREG_*.md` + emenda no PROTOCOLO antes de contar; a origem da pergunta não é fonte; resposta entra como pergunta no capítulo "Alegações públicas testadas") |
| dividir a apuração por hora de encerramento (ou outro corte) | apuracao-dados (fuso) + apuracao-forense (sensibilidade do corte, comparação dentro do município); `fase3/relatorio_pericial.py` |
| autenticar arquivos além do hash (assinatura, cadeia de certificados, controles de mutação) | apuracao-integridade + `operacao_veracidade/` (T60a, T60b) |
| medir o poder de uma bateria contra alterações simuladas | apuracao-forense + `operacao_veracidade/scripts/sim_adversarial.py` (T63) |
| usar evidência de terceiros (boletins impressos, capturas) | apuracao-integridade (T61): classificar proveniência, amostra, relógio |
| preparar dados para outras pessoas pesquisarem | apuracao-versoes + apuracao-dados (`scripts/dados_leves.py`) |
| conferir se os dados do TSE mudaram | apuracao-versoes (`scripts/manifesto.py`, `scripts/carimbo.py`) |

## Situação dos testes
A situação atualizada de cada teste está em `testes/registro.json` (`make registro`). O detalhe de cada resultado está no `CATALOGO.md`, seção 3.
