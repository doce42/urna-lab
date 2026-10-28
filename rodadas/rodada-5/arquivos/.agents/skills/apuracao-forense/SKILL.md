---
name: apuracao-forense
description: Testes estatísticos forenses de eleição (seções fora do padrão, curva real x prevista, dígitos, percentuais inteiros, impressão digital de Klimek, fraude incremental, poder com fraude sintética) com o mesmo código para 2026 e 2022. Use para rodar, interpretar ou acrescentar um teste do módulo D.
---
# Testes forenses

## Quando usar
Rodar ou acrescentar testes T02–T13, T21–T27, ou interpretar um sinal.

## Comandos
- `make bateria ANO=2026` e `make bateria ANO=2022` → `analise/resultado_bateria_<ano>.json`.
- Poder: `make teste T=T13` (`analise/poder.py`). Curva: `analise/curva.py`. Primeiras rodadas (com artefatos, histórico): `analise/testes.py`, `investigar.py`, `testes_corrigidos.py`.

## Como acrescentar um teste
1. Emenda no PROTOCOLO + entrada no `testes/registro.json`, **antes** de rodar.
2. Função em `analise/bateria.py`, gravando `R["T<nn>"]`; documentação no cabeçalho.
3. Rode nos dois anos. Se o teste "acusa", procure o artefato primeiro.
4. Meça o poder: acrescente o teste em `analise/poder.py` e veja quais fraudes sintéticas ele pega e que valor dá nos dados limpos (o limiar tem que não acusar os dados reais sem fraude).
5. Matemática no METODOLOGIA, resultado no CATALOGO, fonte no REFERENCIAS.

## Armadilhas conhecidas (já viraram falso sinal)
- **Teto de 0/100%:** use logit com correção de continuidade, não diferença de percentual.
- **Último dígito:** compare com o esperado pela inclinação local da distribuição, não com uniforme puro.
- **Coincidências** (resultado idêntico): com poucos números por seção o acaso produz muitas; simule.
- **Voto órfão:** candidato forte num estado (Caiado em GO) muda a virada daquele estado; entra no modelo.
- **Muitos testes:** α = 0,01 e Benjamini-Hochberg nas famílias.
- **Benford no 1º dígito não serve para votos** (Deckert et al. 2011). O modelo do Mebane acusa dado limpo (Kim 2025): não usar como veredito.

## Limite que todo relatório tem que dizer
Troca uniforme no país inteiro não deixa diferença entre urnas: nenhum teste estatístico a vê (T13). O que cobre esse caso é a camada A (skill apuracao-integridade) e as auditorias do TSE.

## F2 e F3
- **Poder no sentido correto:** `fase3/rev_a2_poder.py` (A2) e `rev_i1_poder.py` (I1). Mecanismos disperso, locais, municípios, região e grandes cidades. Regra calibrada; detecção conta só o lado certo.
- **Ponto cego e teste próprio:** o T02 não vê troca em município inteiro (a mediana absorve). Para isso há o T44, `fase3/teste_grandes_cidades.py` (histórico de 2022).
- **Curvas (T40):** `f3_curvas.py`, `f3_curvas2.py`, `fila_f4_chegada.py`. Nenhum modelo de chegada validado; T10 e T11 são descritivos. A curva divulgada ao vivo está no R2 (`inv_r2_curva_publica.py`, capturas do Internet Archive).
- **Zeros (T41):** `f3_zeros.py`, `rev_i2_zeros.py`, `inv_r3_zeros.py`. Nenhum modelo calibrado. Fora da amostra, previsto ≈ observado.
