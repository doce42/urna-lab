"""Relatório em PDF (fonte única: os JSON do estudo). Monta grafico/web/relatorio_impresso.html a partir de
fase3/veredito_2026.json, fase3/respostas_f3.json, testes/registro.json e rodadas/linha_do_tempo.json (mais as tabelas de
poder da Operação Veracidade e a sensibilidade do corte da rodada 8) e imprime com o Chromium headless em
grafico/web/relatorio.pdf, copiado para grafico/relatorio-app/public/relatorio.pdf (o site linka /relatorio.pdf).
Nenhum número é escrito aqui: todos vêm dos arquivos lidos. Uso: python3 grafico/montar_relatorio_pdf.py [--sem-pdf]
(chamado por `make pdf`)."""
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
WEB = os.path.join(R, "grafico", "web")
SITE = "https://urna-lab.web.app"
GITHUB = "https://github.com/doce42/urna-lab"
ler = lambda c: json.load(open(os.path.join(R, c), encoding="utf-8"))
e = lambda x: html.escape(str(x if x is not None else ""), quote=True)

V = ler("fase3/veredito_2026.json")
Q = ler("fase3/respostas_f3.json")
REG = ler("testes/registro.json")
LT = ler("rodadas/linha_do_tempo.json")
R2B = ler("fase3/resultados/relatorio_pericial_r2b.json")
PROV = ler("fase3/proveniencia_v1_5.json")
RES7 = ler("rodadas/rodada-7/resumo.json")
RC = V["resposta_central"]
NIV = {n["id"]: n for n in V["niveis"]}
SIN = V["sinal_por_teste"]
TESTES = REG["testes"]
PERGUNTAS = [p for c in Q["capitulos"] for p in c["perguntas"]]
N = lambda n: f"{n:,}".replace(",", ".")
tag_v15 = (re.search(r"V1\.5\*\*.*?tag `(v[\d.]+)`", open(os.path.join(R, "RODADAS.md"), encoding="utf-8").read()) or [None, "v1.5"])[1]
rodada_aberta = next((f for f in reversed(LT["fases"]) if f["status"] in ("em_andamento", "em_revisao")), None)
DATA = V.get("gerado", "")
data_br = "/".join(reversed(DATA.split("-"))) if DATA else ""
versao_curta = f"{PROV['versao']} congelada" + (f" · rodada {rodada_aberta['rodada']} em andamento" if rodada_aberta else "")


sem_rodada = lambda t: re.sub(r"\s*\(rodada \d+\)", "", t)


def selo(nivel):
    n = NIV.get(nivel, {"nome": nivel})
    return f'<span class="sn sn-{e(nivel)}"><b>{e(nivel)}</b> {e(n["nome"])}</span>'


def sentencas(txt, limite=300):
    """Resumo pelas primeiras frases inteiras (não corta frase no meio)."""
    partes = re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ\"(])", txt.strip())
    out = []
    for p in partes:
        out.append(p)
        if len(" ".join(out)) >= limite:
            break
    return " ".join(out), len(out) < len(partes)


def tabela_md(md, titulo_secao):
    """Primeira tabela markdown depois do título dado (para AUTOAUDITORIA e tabelas de simulação)."""
    i = md.find(titulo_secao)
    if i < 0:
        return []
    linhas = []
    for l in md[i:].split("\n")[1:]:
        if l.startswith("|"):
            linhas.append([c.strip() for c in l.strip().strip("|").split("|")])
        elif linhas:
            break
    return [l for l in linhas if not set("".join(l)) <= set("-: ")]


def inline_md(t):
    t = e(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", t)


def sha(c):
    return hashlib.sha256(open(os.path.join(R, c), "rb").read()).hexdigest()


S = []  # seções da parte densa, para o índice
H = []
add = H.append


def secao(id_, titulo, nivel=2):
    if nivel == 2:
        S.append((id_, titulo))
    add(f'<h{nivel} id="{id_}">{e(titulo)}</h{nivel}>')


# ---------------- capa e resumão ----------------
av = RC["aviso"]
add(f"""<header class="capa">
<div class="marca">urna lab</div>
<h1>A apuração presidencial de 2026, conferida com os dados públicos do TSE</h1>
<p class="sub">Auditoria metodológica independente, com 2022 como referência. Relatório gerado a partir dos arquivos do estudo.</p>
<p class="versao"><b>{e(PROV['versao'])}</b> (rodada {PROV['rodada']}, tag <code>{e(tag_v15)}</code>) congelada em {e("/".join(reversed(PROV['data'].split('-'))))}{f" · <b>rodada {rodada_aberta['rodada']} em andamento, não congelada</b> ({e(sem_rodada(rodada_aberta['titulo']))})" if rodada_aberta else ""} · {len(TESTES)} testes e {len(PERGUNTAS)} perguntas no registro vivo · resultados de {e(data_br)} · site <a href="{SITE}">{SITE.replace('https://', '')}</a></p>
</header>""")
add(f"""<section class="aviso"><h2 class="h-aviso">{e(av['titulo'])}</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in av['itens'])}</ul></section>""")
rs = RC["resumo"]
add(f"""<section class="resposta"><div class="rot">Pergunta testada</div><h2 class="pergunta">{e(RC['pergunta'])}</h2>
<p class="lead"><b>{e(RC['resposta'].split('. ')[0])}.</b></p>
<dl class="quatro">
<dt>O que foi observado</dt><dd>{e(rs['observado'])}</dd>
<dt>O que foi excluído, no alcance testado</dt><dd>{e(rs['excluido'])}</dd>
<dt>O que ficou sem resposta</dt><dd>{e(rs['sem_resposta'])}</dd>
<dt>O que faltaria para responder</dt><dd>{e(rs['faltaria'])}</dd>
</dl></section>""")
add('<h2 class="r">Achados principais</h2><ol class="achados">' + "".join(
    f'<li><b>{e(a["titulo"])}</b> {e(a["texto"])} <span class="ref">{e(a["teste"])} · {selo(SIN.get(a["teste"], {}).get("nivel", "M"))}</span></li>' for a in rs["achados"]) + "</ol>")
al = RC["alegacoes"]
add(f'<h2 class="r">{e(al["titulo"])}: a resposta curta</h2><p>{e(al["frase"])}</p><table class="alg"><thead><tr><th style="width:31%">Alegação</th><th>Resposta curta</th><th style="width:12%">Ver</th></tr></thead><tbody>'
    + "".join(f'<tr><td><b>{e(x["alegacao"])}</b></td><td>{e(x["resposta"])}</td><td class="ids">{e(", ".join(x["perguntas"] + x["testes"]))}</td></tr>' for x in al["itens"])
    + f'</tbody></table><p class="nota">{e(al["situacao"])}</p>')
add('<h2 class="r">Como ler a escala de sinal</h2><p>Cada teste recebe um sinal, separado de "passou ou não passou". O código (S0 a S5, PC, M) vai sempre junto do nome, para a leitura não depender de cor.</p><table class="esc"><tbody>'
    + "".join(f'<tr><td style="width:30%">{selo(n["id"])}</td><td>{e(n["o_que_e"])}</td></tr>' for n in V["niveis"]) + "</tbody></table>")
add('<h2 class="r">Leia junto com os resultados</h2><ul class="avisos">' + "".join(f"<li>{e(x)}</li>" for x in RC["avisos"]) + "</ul>")
add(f'<p class="nota"><b>Nota do autor:</b> {e(av.get("nota_autor", ""))}</p>')
add('<div class="quebra"></div><div class="parteB"><div class="rot">Parte B</div><h1 class="hB">O estudo em detalhe</h1><p>Dedução, hipóteses, os testes, a Operação Veracidade, as rodadas de alegações públicas, as perguntas e respostas, método, limites e como reproduzir. A versão viva de cada item está no site.</p></div>')
INDICE_POS = len(H)  # o índice entra aqui, no começo da parte B

# ---------------- dedução e hipóteses ----------------
secao("deducao", "Dedução completa")
add(f"<p><b>{e(RC['pergunta'])}</b> {e(RC['resposta'])}</p><ol class='ded'>" + "".join(f"<li>{e(d)}</li>" for d in RC["deducao"]) + "</ol>")
add(f"<p><b>O que fecharia o que resta:</b> {e(RC['o_que_seria_preciso'])}</p>")
secao("hipoteses", f"As {len(V['hipoteses'])} hipóteses de fraude examinadas")
add(f"<p>Inverter o resultado de 2026 exigiria trocar {N(V['votos_para_inverter'])} votos de lado (metade da margem de {N(V['margem_2026'])}).</p>")
for h in V["hipoteses"]:
    add(f"""<div class="hip"><div class="hip-t"><b>{e(h['id'])}</b> {e(h['mecanismo'])} <span class="st">{e(h['status'])}</span></div>
<p><b>O que deixaria:</b> {e(h['o_que_deixaria'])} <b>Escala:</b> {e(h['escala_necessaria'])}</p>
<p><b>Resultado:</b> {e(h['resultado'])}</p><p><b>Em votos:</b> {e(h['em_votos'])} <span class="ref">Testes: {e(', '.join(h['testes']))}</span></p></div>""")
secao("anomalias", "Anomalias reais em 2026")
add('<table><thead><tr><th>O que</th><th style="width:20%">Votos</th><th style="width:22%">Sinal</th><th style="width:8%">Teste</th></tr></thead><tbody>'
    + "".join(f"<tr><td>{e(a['o_que'])}</td><td>{e(a['votos'])}</td><td>{selo(a['sinal'])}</td><td>{e(a['teste'])}</td></tr>" for a in RC["anomalias_2026"])
    + f"</tbody></table><p class='nota'>{e(RC['nota_anomalias'])}</p>")

# ---------------- os testes ----------------
MODS = {"A": "Integridade dos arquivos e da contagem", "B": "Comportamento do eleitor e da votação", "C": "Mudança entre os turnos", "D": "Forense estatística",
        "E": "Divergências e agrupamento", "F": "Referência: 2022", "G": "Fase 2: investigações aprofundadas", "H": "Fase 3, alegações públicas, Operação Veracidade e relatório pericial"}
secao("testes", f"Os {len(TESTES)} testes")
cont = {}
for t in TESTES:
    k = SIN.get(t["id"], {}).get("nivel", "M"); cont[k] = cont.get(k, 0) + 1
add("<p>Pergunta de cada teste, o sinal atual e o motivo do sinal, por módulo. O detalhe (método, hipótese nula, limites, história e comando) está no site, em "
    f"<code>{SITE.replace('https://', '')}/#/testes/&lt;id&gt;</code>. Contagem por sinal: " + ", ".join(f"{k} {cont[k]}" for k in NIV if k in cont) + ".</p>")
for m in "ABCDEFGH":
    ts = [t for t in TESTES if t["modulo"] == m]
    if not ts:
        continue
    add(f'<h3>Módulo {m}: {e(MODS.get(m, ""))} ({len(ts)})</h3><table class="tt"><thead><tr><th style="width:7%">Id</th><th style="width:31%">Pergunta</th><th style="width:13%">Sinal</th><th>Resultado (motivo do sinal)</th></tr></thead><tbody>')
    for t in ts:
        s = SIN.get(t["id"], {"nivel": "M", "motivo": t.get("resultado_atual", "")})
        add(f"<tr><td class='id'>{e(t['id'])}</td><td>{e(t['pergunta'])}</td><td>{selo(s['nivel'])}</td><td>{e(s['motivo'])}</td></tr>")
    add("</tbody></table>")

# ---------------- Operação Veracidade ----------------
op = RC["operacao"]
T = {t["id"]: t for t in TESTES}
secao("veracidade", f"{op['titulo']} ({op['versao']})")
add(f"<p><b>{e(op['pergunta'])}</b> {e(op['resposta'])}</p><ul>" + "".join(f"<li><b>{e(a['titulo'])} ({e(a['teste'])}).</b> {e(a['texto'])}</li>" for a in op["achados"]) + "</ul>")
md_sim = open(os.path.join(R, "operacao_veracidade/resultados/tabelas_sim.md"), encoding="utf-8").read()
g26 = tabela_md(md_sim, "### Poder por mecanismo e magnitude, 2026")
g22 = tabela_md(md_sim, "### Poder por mecanismo e magnitude, 2022")
if g26 and g22:
    add("<h3>Poder da bateria: a partir de quantos votos cada mecanismo é visto (T63)</h3><p>Menor troca com alarme em pelo menos 80% das réplicas, nos dois sentidos (a favor de Lula / a favor do adversário). Votos simulados sobre a base real; \"nunca\" = não visto em nenhuma magnitude testada (até 2,22 mi).</p>")
    d22 = {l[0]: l[-1] for l in g22[1:]}
    add('<table><thead><tr><th>Mecanismo</th><th style="width:24%">2026</th><th style="width:24%">2022</th></tr></thead><tbody>'
        + "".join(f"<tr><td>{e(l[0])}</td><td>{e(l[-1])}</td><td>{e(d22.get(l[0], '—'))}</td></tr>" for l in g26[1:]) + "</tbody></table>")
    add("<h3>Grade completa de 2026 (% de réplicas com alarme na direção certa, a favor de Lula / a favor do adversário)</h3><table class='grade'><thead><tr>"
        + "".join(f"<th>{e(c)}</th>" for c in g26[0][:-1]) + "</tr></thead><tbody>"
        + "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in l[:-1]) + "</tr>" for l in g26[1:]) + "</tbody></table>")
for k, tit in [("T60a", "Cadeia de certificados"), ("T60b", "Controles do verificador"), ("T61", "Boletins de terceiros"), ("T62", "Registros coerentes de fonte comprometida"), ("T64", "Zeros de votos")]:
    t = T.get(k)
    if t:
        add(f"<h3>{e(tit)} ({k}) · {selo(SIN.get(k, {}).get('nivel', 'M'))}</h3><p>{e(t.get('evidencia') or t['resultado_atual'])}</p>" + (f"<p><b>O que quer dizer:</b> {e(t['interpretacao'])}</p>" if t.get("interpretacao") else ""))
add("<p><b>Pontos cegos:</b></p><ul>" + "".join(f"<li>{e(x)}</li>" for x in op["pontos_cegos"]) + "</ul>")

# ---------------- rodadas 6, 7 e 8 ----------------
secao("rodadas", "Rodadas 6, 7 e 8: alegações públicas")
primeira = lambda t: min([v["rodada"] for v in t.get("versoes", [])] or [None]) if t.get("versoes") else None
for f in LT["fases"]:
    if f.get("rodada") not in (6, 7, 8):
        continue
    ts = [t for t in TESTES if primeira(t) == f["rodada"]] if f["status"] == "concluida" else [t for t in TESTES if not t.get("versoes")]
    est = f"{f.get('versao', '')}, congelada" if f["status"] == "concluida" else "em andamento, não congelada"
    add(f"<h3>Rodada {f['rodada']}: {e(sem_rodada(f['titulo']))} ({e(est)})</h3><p>{e(f['resumo'])}</p>")
    if ts:
        add('<table class="tt"><thead><tr><th style="width:7%">Id</th><th style="width:31%">Pergunta</th><th style="width:13%">Sinal</th><th>Em votos</th></tr></thead><tbody>'
            + "".join(f"<tr><td class='id'>{e(t['id'])}</td><td>{e(t['pergunta'])}</td><td>{selo(SIN.get(t['id'], {}).get('nivel', 'M'))}</td><td>{e(t.get('impacto_votos', ''))}</td></tr>" for t in ts) + "</tbody></table>")
sens = R2B.get("a_sensibilidade_do_corte", {})
if sens:
    add("<h3>A divisão por hora de encerramento depende do minuto do corte (T66, R2b exploratório)</h3><p>Hora local de encerramento. Vantagem de Lula = votos de Lula menos votos do adversário em cada grupo. A soma dos dois grupos cobre as seções com horário de encerramento registrado e pode diferir da margem nacional.</p>"
        '<table><thead><tr><th>Corte</th><th>Seções até o corte</th><th>Vantagem de Lula até o corte</th><th>Seções depois</th><th>Vantagem de Lula depois</th></tr></thead><tbody>'
        + "".join(f"<tr><td>{e(c)}</td><td>{N(g['antes']['secoes'])}</td><td>{N(g['antes']['vantagem_lula'])}</td><td>{N(g['depois']['secoes'])}</td><td>{N(g['depois']['vantagem_lula'])}</td></tr>" for c, g in sens.items())
        + "</tbody></table>")

# ---------------- perguntas e respostas ----------------
secao("perguntas", f"As {len(PERGUNTAS)} perguntas e respostas (resumidas)")
add(f"<p>{e(Q['aviso'])} {e(Q['margem'])} Cada resposta abaixo traz as primeiras frases; a resposta completa, com números, o que demonstra e o que não demonstra, está no site em <code>{SITE.replace('https://', '')}/#/respostas/&lt;id&gt;</code>.</p>")
for c in Q["capitulos"]:
    add(f"<h3>{e(c['titulo'])}</h3><p class='nota'>{e(c.get('descricao', ''))}</p>")
    for p in c["perguntas"]:
        txt, cortou = sentencas(p["resposta"])
        add(f"""<div class="q"><div class="q-t"><b>{e(p['id'])}</b> {e(p['pergunta'])}</div><p><span class="cl">{e(p['classificacao'])}</span> {e(txt)}{' <i>(continua no site)</i>' if cortou else ''}</p>"""
            + (f"<p class='ev'><b>Em votos:</b> {e(p.get('em_votos', ''))}</p>" if p.get("em_votos") and p["em_votos"] != "—" else "") + "</div>")

# ---------------- método, limites, autoauditoria ----------------
secao("metodo", "Metodologia e limites")
add("""<ul><li><b>Só dados oficiais do TSE:</b> dados abertos e os arquivos gravados por cada urna (boletim, registro digital do voto, log, imagem do boletim e assinaturas).</li>
<li><b>Pré-registro:</b> hipótese, modelo nulo e limiar escritos antes de rodar (<code>PROTOCOLO.md</code>, <code>fase3/PREREG_*.md</code>); desvios ficam registrados.</li>
<li><b>Poder medido:</b> cada teste forense roda nos dados reais, em 2022 e com fraude simulada; um resultado negativo vem com o que o teste conseguiria ver.</li>
<li><b>Regra adversarial:</b> concordância entre boletim, RDV, log e tabela é consistência interna; explicação que vem do próprio log é "compatível", não "verificada".</li>
<li><b>Três tipos de afirmação, sempre separados:</b> prova determinística (conta exata, criptografia), evidência estatística (com poder medido) e limite dos dados públicos.</li></ul>""")
add("<h3>Limites das fontes e dos métodos</h3><ul>" + "".join(f"<li>{e(x)}</li>" for x in Q["limites"]) + "</ul>")
add("<h3>Achados que persistem sem causa demonstrada</h3><ul>" + "".join(f"<li>{e(x)}</li>" for x in Q["achados_sem_causa"]) + "</ul>")
secao("autoauditoria", "Autoauditoria")
md_aa = open(os.path.join(R, "AUTOAUDITORIA.md"), encoding="utf-8").read()
add("<p>Trechos de <code>AUTOAUDITORIA.md</code> (mapa de ameaças, ameaças à validade e lacunas completos no arquivo).</p>")
for tit, ancora in [("Limites que os dados públicos não permitem fechar", "## 6. Limites que os dados públicos"), ("Atualização da rodada 7 (Operação Veracidade)", "### Atualização de 28/10/2026 (rodada 7"), ("Atualização da rodada 8 (em aberto)", "### Atualização de 28/10/2026 (rodada 8")]:
    tb = tabela_md(md_aa, ancora)
    if tb:
        add(f"<h3>{e(tit)}</h3><table><thead><tr>" + "".join(f"<th>{inline_md(c)}</th>" for c in tb[0]) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in l) + "</tr>" for l in tb[1:]) + "</tbody></table>")

# ---------------- reprodutibilidade ----------------
secao("reproduzir", "Reprodutibilidade")
entradas = ["fase3/veredito_2026.json", "fase3/respostas_f3.json", "testes/registro.json", "rodadas/linha_do_tempo.json"]
add(f"""<p><b>Versão congelada:</b> {e(PROV['versao'])}, rodada {PROV['rodada']}, tag <code>{e(tag_v15)}</code>, {e(RES7['placar']['testes'])} testes no congelamento; commit público antes do congelamento <code>{e(PROV.get('commit_publico_antes_do_congelamento', '—'))}</code>; Python {e(PROV.get('python', '—'))}. Manifesto SHA-256 de {len(RES7.get('arquivos_sha256', {}))} arquivos em <code>rodadas/rodada-7/resumo.json</code> (SHA-256 <code>{sha('rodadas/rodada-7/resumo.json')[:16]}…</code>), com carimbo OpenTimestamps em <code>resumo.json.ots</code>.</p>"""
    + (f"<p><b>Rodada {rodada_aberta['rodada']} ({e(sem_rodada(rodada_aberta['titulo']))}): em andamento, não congelada.</b> Os testes e perguntas dela estão no registro vivo; ganham hash, tag e conclusão própria só quando forem congelados, com aprovação do responsável.</p>" if rodada_aberta else ""))
add("<p><b>Arquivos de onde este PDF foi montado</b> (SHA-256, primeiros 16 caracteres):</p><table><tbody>" + "".join(f"<tr><td><code>{c}</code></td><td><code>{sha(c)[:16]}…</code></td></tr>" for c in entradas) + "</tbody></table>")
add(f"""<table><thead><tr><th style="width:42%">Comando</th><th>Para quê</th></tr></thead><tbody>
<tr><td><code>make ambiente</code></td><td>cria o ambiente Python com versões fixas (<code>requirements.txt</code>)</td></tr>
<tr><td><code>make dados-do-zero</code></td><td>baixa e prepara os dados oficiais do TSE (horas, centenas de GB)</td></tr>
<tr><td><code>make verificar</code></td><td>conferências rápidas: registro, totalização, cobertura, documentação</td></tr>
<tr><td><code>make teste T=&lt;id&gt;</code></td><td>roda um teste do registro (o comando de cada um está em <code>testes/registro.json</code>)</td></tr>
<tr><td><code>make veracidade-certs</code>, <code>veracidade-sim</code>, <code>veracidade-zeros</code>, <code>veracidade-externo</code></td><td>testes da Operação Veracidade (T60a a T65)</td></tr>
<tr><td><code>.venv/bin/python fase3/relatorio_pericial.py</code></td><td>testes da rodada 8 (T66 a T70); o R2b em <code>fase3/relatorio_pericial_r2b.py</code></td></tr>
<tr><td><code>make pdf</code></td><td>monta este PDF a partir dos JSON (<code>grafico/montar_relatorio_pdf.py</code>)</td></tr>
</tbody></table><p>Código: <a href="{GITHUB}">{GITHUB.replace('https://', '')}</a> (MIT). Documentação e resultados: CC BY 4.0. Manual para pessoas e agentes de IA: <code>AGENTS.md</code>; ordem de execução: <code>PIPELINE.md</code>.</p>""")

# ---------------- índice e montagem ----------------
indice = ('<nav class="indice"><h2 class="r">Índice</h2><ol><li><a href="#topo">Parte A: resumo (pergunta, resposta, achados, alegações, escala, avisos)</a></li>'
          + "".join(f'<li><a href="#{i}">{e(t)}</a></li>' for i, t in S) + "</ol></nav>")
H.insert(INDICE_POS, indice)
sora = os.path.join(R, "grafico/relatorio-app/node_modules/@fontsource-variable/sora/files/sora-latin-wght-normal.woff2")
sora_ext = sora.replace("sora-latin-wght", "sora-latin-ext-wght")
cab = f"urna lab · {versao_curta} · {data_br}".replace('"', "'")
CSS = f"""
@font-face {{ font-family: 'Sora R'; src: url('file://{sora}') format('woff2'); font-weight: 100 800; }}
@font-face {{ font-family: 'Sora R'; src: url('file://{sora_ext}') format('woff2'); font-weight: 100 800; unicode-range: U+0100-024F, U+1E00-1EFF; }}
@page {{ size: A4; margin: 17mm 16mm 17mm 16mm;
  @top-left {{ content: "{cab}"; font: 7.5pt 'Noto Sans', sans-serif; color: #555; }}
  @bottom-right {{ content: "página " counter(page) " de " counter(pages); font: 7.5pt 'Noto Sans', sans-serif; color: #555; }}
  @bottom-left {{ content: "{SITE.replace('https://', '')} · nada aqui afirma ou nega fraude além do que os números sustentam"; font: 7.5pt 'Noto Sans', sans-serif; color: #555; }} }}
@page :first {{ @top-left {{ content: none; }} }}
* {{ box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: 'Noto Sans', 'Liberation Sans', sans-serif; font-size: 10.2pt; line-height: 1.42; color: #16181c; margin: 0; }}
h1, h2, h3, .marca, .pergunta {{ font-family: 'Sora R', 'Noto Sans', sans-serif; color: #111; }}
h1 {{ font-size: 20pt; line-height: 1.15; margin: 4pt 0 6pt; font-weight: 650; }}
h2 {{ font-size: 14pt; margin: 16pt 0 6pt; font-weight: 650; break-after: avoid; }}
h2.r {{ font-size: 12pt; margin: 12pt 0 4pt; border-bottom: 1.2pt solid #222; padding-bottom: 2pt; }}
h3 {{ font-size: 11pt; margin: 12pt 0 4pt; font-weight: 650; break-after: avoid; }}
p {{ margin: 3pt 0 5pt; }} ul, ol {{ margin: 3pt 0 6pt; padding-left: 15pt; }} li {{ margin: 1.5pt 0; }}
a {{ color: #0b4f6c; text-decoration: none; }}
code {{ font-family: 'IBM Plex Mono', 'Liberation Mono', monospace; font-size: 8.4pt; overflow-wrap: anywhere; }}
.capa .marca {{ font-size: 10pt; letter-spacing: .14em; text-transform: uppercase; font-weight: 700; color: #8a3b12; }}
.sub {{ font-size: 11pt; color: #333; margin: 0 0 4pt; }}
.versao {{ font-size: 8.6pt; color: #333; border-top: .8pt solid #999; border-bottom: .8pt solid #999; padding: 3pt 0; margin: 4pt 0 6pt; }}
.aviso {{ border: 1pt solid #444; border-left: 4pt solid #444; padding: 4pt 8pt; margin: 6pt 0; font-size: 9.2pt; break-inside: avoid; }}
.h-aviso {{ font-size: 10pt; margin: 2pt 0; }}
.aviso ul {{ margin: 2pt 0; }}
.resposta {{ margin: 8pt 0; break-inside: avoid; }}
.rot {{ font-size: 7.8pt; letter-spacing: .12em; text-transform: uppercase; color: #555; font-weight: 600; }}
.pergunta {{ font-size: 13.5pt; margin: 2pt 0 4pt; }}
.lead {{ font-size: 11pt; }}
dl.quatro {{ display: grid; grid-template-columns: 31% 1fr; gap: 3pt 8pt; margin: 4pt 0; }}
dl.quatro dt {{ font-weight: 700; border-top: .6pt solid #bbb; padding-top: 2pt; }}
dl.quatro dd {{ margin: 0; border-top: .6pt solid #bbb; padding-top: 2pt; }}
ol.achados li {{ margin: 2.5pt 0; break-inside: avoid; }}
.ref {{ color: #444; font-size: 8.4pt; white-space: nowrap; }}
.nota {{ font-size: 8.8pt; color: #333; }}
table {{ width: 100%; border-collapse: collapse; margin: 4pt 0 8pt; font-size: 8.7pt; line-height: 1.33; }}
thead {{ display: table-header-group; }}
tr {{ break-inside: avoid; }}
th {{ text-align: left; font-weight: 700; border-bottom: 1.2pt solid #222; padding: 3pt 4pt; vertical-align: bottom; }}
td {{ border-bottom: .5pt solid #bbb; padding: 3pt 4pt; vertical-align: top; overflow-wrap: anywhere; }}
td.id, td.ids {{ font-family: 'IBM Plex Mono', monospace; font-size: 8pt; white-space: nowrap; }}
td.ids {{ white-space: normal; }}
table.grade {{ font-size: 7.6pt; }} table.grade td, table.grade th {{ padding: 2pt 3pt; }}
.sn {{ display: inline-block; border: .8pt solid #333; border-radius: 3pt; padding: 0 3pt; font-size: 7.8pt; line-height: 1.5; white-space: nowrap; background: #fff; }}
.sn b {{ font-family: 'IBM Plex Mono', monospace; }}
td .sn {{ white-space: normal; }}
.sn-S0, .sn-S1 {{ border-color: #1d6b45; }} .sn-S2 {{ border-color: #8a6a00; border-style: dashed; }}
.sn-S3 {{ border-color: #a04a00; border-width: 1.4pt; }} .sn-S4, .sn-S5 {{ border-color: #a0001e; border-width: 1.8pt; }}
.sn-PC {{ border-color: #666; border-style: dotted; }} .sn-M {{ border-color: #888; border-style: dashed; }}
.indice {{ break-inside: avoid; }} .indice ol {{ columns: 2; column-gap: 18pt; }}
.quebra {{ break-before: page; }}
.parteB {{ border-top: 2pt solid #111; padding-top: 4pt; }} .hB {{ font-size: 18pt; }}
.hip {{ border-left: 2.5pt solid #555; padding: 1pt 0 1pt 7pt; margin: 6pt 0; break-inside: avoid; }}
.hip-t {{ font-weight: 600; }} .hip p {{ margin: 1.5pt 0; font-size: 9.4pt; }}
.st {{ font-size: 8pt; border: .8pt solid #333; padding: 0 3pt; border-radius: 3pt; font-weight: 600; white-space: nowrap; }}
.q {{ margin: 5pt 0; break-inside: avoid; }} .q-t {{ font-weight: 600; }} .q p {{ margin: 1pt 0; font-size: 9.4pt; }}
.cl {{ font-size: 7.8pt; border: .7pt solid #444; padding: 0 3pt; border-radius: 3pt; margin-right: 3pt; white-space: nowrap; }}
.ev {{ color: #333; }}
ol.ded li {{ margin: 3pt 0; }}
"""
saida_html = os.path.join(WEB, "relatorio_impresso.html")
doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>urna lab: relatório da apuração de 2026</title><style>{CSS}</style></head>
<body><div id="topo"></div>{''.join(H)}<p class="nota" style="margin-top:14pt">Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} por <code>grafico/montar_relatorio_pdf.py</code> a partir dos arquivos do estudo.</p></body></html>"""
open(saida_html, "w", encoding="utf-8").write(doc)
print("html:", os.path.relpath(saida_html, R), f"({len(doc) // 1024} KB)")
if "--sem-pdf" in sys.argv:
    sys.exit(0)
pdf = os.path.join(WEB, "relatorio.pdf")
nav = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
if not nav:
    sys.exit("chromium não encontrado: instale ou rode com --sem-pdf e imprima o HTML à mão")
subprocess.run([nav, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", "--allow-file-access-from-files",
                f"--print-to-pdf={pdf}", "file://" + saida_html], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
destino = os.path.join(R, "grafico", "relatorio-app", "public", "relatorio.pdf")
shutil.copyfile(pdf, destino)
print("pdf:", os.path.relpath(pdf, R), "e", os.path.relpath(destino, R), f"({os.path.getsize(pdf) / 1e6:.2f} MB)")
