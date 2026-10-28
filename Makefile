# Estudo da apuração (Presidente 2026, 1º e 2º turno; 2022 como referência).
# Uso: make ajuda. Tudo roda com prioridade baixa (nice/ionice) para não travar a máquina.
# NPROC = processos em paralelo para ler os arquivos das urnas (padrão 12).

PY      := .venv/bin/python
BAIXO   := nice -n 10 ionice -c3
NPROC   ?= 12
ANO     ?= 2026
T       ?=

.PHONY: ajuda ambiente dados-do-zero base dados bateria comportamento integridade totalizacao teste relatorio pdf servir verificar registro

ajuda:
	@echo "make ambiente        cria .venv e instala requirements.txt"
	@echo "make dados-do-zero   baixa e prepara todos os dados oficiais do TSE (~250 GB, horas)"
	@echo "make base            base por seção (ANO=2026|2022)"
	@echo "make dados           dados do gráfico + curva prevista (confere totais e para se não bater)"
	@echo "make bateria         testes forenses T02–T05, T07, T10, T11, T21, T22 (ANO=2026|2022)"
	@echo "make comportamento   C01–C08 (ANO=2026|2022)"
	@echo "make integridade     arquivos das urnas: assinatura, hash, RDV, log, sequência (NPROC=...)"
	@echo "make totalizacao     T32: soma das urnas x totais oficiais"
	@echo "make teste T=<id>    roda um teste do registro (testes/registro.json)"
	@echo "make relatorio       dados do relatório; make pdf gera o PDF; make servir abre em localhost:8765"
	@echo "make verificar       conferências rápidas (totais, registro, cobertura)"
	@echo "make registro        lista os testes e a situação de cada um"

ambiente:
	python3 -m venv .venv && $(PY) -m pip install -q -r requirements.txt

dados-do-zero:
	scripts/preparar_dados.sh

base:
	$(BAIXO) $(PY) analise/montar_base.py $(ANO)

dados:
	$(BAIXO) python3 -I grafico/montar_dados.py
	$(BAIXO) $(PY) grafico/prever.py

bateria:
	$(BAIXO) $(PY) analise/bateria.py $(ANO)

comportamento:
	$(BAIXO) $(PY) analise/comportamento.py $(ANO)

integridade:
	NPROC=$(NPROC) $(BAIXO) $(PY) analise/processar_brutos.py 1
	NPROC=$(NPROC) $(BAIXO) $(PY) analise/processar_brutos.py 2

totalizacao:
	$(BAIXO) $(PY) analise/totalizacao.py

teste:
	@$(PY) scripts/rodar_teste.py $(T)

relatorio:
	$(BAIXO) $(PY) analise/relatorio_dados.py

servir:
	cd grafico/web && python3 -m http.server 8765 --bind 127.0.0.1

pdf:
	chromium --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=20000 \
	  --print-to-pdf=grafico/web/relatorio.pdf http://127.0.0.1:8765/relatorio.html

verificar:
	$(PY) scripts/verificar.py

registro:
	@$(PY) scripts/rodar_teste.py --lista
