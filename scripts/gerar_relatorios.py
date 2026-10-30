"""Gera relatorios/*.md (um relatório por fase ou rodada) a partir de rodadas/linha_do_tempo.json,
para que nenhum número fique escrito à mão. Uso: python scripts/gerar_relatorios.py"""
import json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
T = json.load(open(R / "rodadas/linha_do_tempo.json"))
SAIDA = R / "relatorios"; SAIDA.mkdir(exist_ok=True)
ALVOS = {  # id da fase -> (arquivo, onde ler o detalhe)
    "F1": ("fase1.md", ["RODADAS.md", "revisoes/README.md", "CONCLUSAO.md"]),
    "F2": ("fase2.md", ["FASE2.md", "RELATORIO_FASE2_COMPLETA.md"]),
    "F3": ("fase3.md", ["RELATORIO_F3.md", "fase3/VEREDITO_2026.md", "fase3/RESPOSTAS_F3.md"]),
    "AP": ("rodada-6.md", ["fase3/RESPOSTAS_F3.md", "testes/registro.json"]),
    "OV": ("rodada-7.md", ["operacao_veracidade/OPERACAO_VERACIDADE_GERAL.md", "operacao_veracidade/REPRODUCAO.md"]),
    "RP": ("rodada-8.md", ["fase3/PREREG_RELATORIO_PERICIAL.md", "fase3/resultados/relatorio_pericial.json", "fase3/resultados/relatorio_pericial_r2b.json", "fase3/PREREG_CURVAS_SOBREPOSTAS.md", "fase3/resultados/curvas_sobrepostas.json"]),
}
ROT = {"concluida": "concluída", "em_andamento": "EM ABERTO (não congelada)"}
ind = ["# Relatórios por fase e rodada", "",
       "Um relatório por etapa do estudo, gerado de [`rodadas/linha_do_tempo.json`](../rodadas/linha_do_tempo.json) por `scripts/gerar_relatorios.py`. O detalhe completo de cada etapa fica nos documentos citados em cada relatório. Versão congelada não se reescreve; a rodada em aberto muda até ser congelada com aprovação explícita.", "",
       "| Etapa | Versão | Situação | Relatório |", "|---|---|---|---|"]
for f in T["fases"]:
    if f["id"] not in ALVOS: continue
    arq, fontes = ALVOS[f["id"]]
    out = [f"# {f['titulo']}", "",
           f"**Versão:** {f.get('versao') or '—'} · **Situação:** {ROT.get(f['status'], f['status'])} · **Início:** {f.get('inicio', '—')}" + (f" · **Fim:** {f['fim']}" if f.get("fim") else ""), "",
           "## Resumo", "", f["resumo"], ""]
    if f.get("etapas"):
        out += ["## O que foi feito", ""] + [f"{i}. **{e['titulo']}.** {e['texto']}" for i, e in enumerate(f["etapas"], 1)] + [""]
    if f.get("historico"):
        out += ["## Histórico", ""] + [f"- {h}" if isinstance(h, str) else f"- **{h.get('titulo', h.get('data', ''))}** {h.get('texto', '')}".strip() for h in f["historico"]] + [""]
    out += ["## Onde está o detalhe", ""] + [f"- [`{s}`](../{s})" for s in fontes] + [""]
    if f["status"] == "em_andamento":
        out += ["> Esta rodada está **aberta**: nada foi congelado, não há tag, e os resultados podem mudar. Alegações de posts e vídeos são a origem da pergunta, nunca fonte.", ""]
    out += ["Nada aqui afirma nem nega fraude além do que os números sustentam.", ""]
    (SAIDA / arq).write_text("\n".join(out), encoding="utf-8")
    ind.append(f"| {f['titulo']} | {f.get('versao') or '—'} | {ROT.get(f['status'], f['status'])} | [{arq}]({arq}) |")
(SAIDA / "README.md").write_text("\n".join(ind) + "\n", encoding="utf-8")
print("relatorios/: " + ", ".join(sorted(p.name for p in SAIDA.iterdir())))
