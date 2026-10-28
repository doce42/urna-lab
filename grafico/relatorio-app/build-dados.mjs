// Gera os arquivos enxutos do site a partir dos JSON locais e dos .md do estudo.
// Entrada: ../web/*.json, ../web/geo/*.json, ../../testes/registro.json, ../../*.md
// Saída:   public/dados/*.json (carregados sob demanda pelo site)
// Rode de novo sempre que os JSON forem regerados: `npm run dados` (o `npm run build` já chama).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import { topology } from 'topojson-server';
import { presimplify, simplify, quantile } from 'topojson-simplify';
import { geoArea } from 'd3-geo';
import { quantize } from 'topojson-client';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const WEB = path.join(AQUI, '..', 'web');
const RAIZ = path.join(AQUI, '..', '..');
const SAIDA = path.join(AQUI, 'public', 'dados');
fs.mkdirSync(path.join(SAIDA, 'docs'), { recursive: true });

const ler = (f) => {
  const t = fs.readFileSync(f, 'utf8');
  // o Python grava NaN/Infinity; o JSON do navegador não aceita
  return JSON.parse(t.replace(/\bNaN\b/g, 'null').replace(/-?\bInfinity\b/g, 'null'));
};
const existe = (f) => fs.existsSync(f);
const r = (v, d = 3) => (v == null || Number.isNaN(v) ? null : Math.round(v * 10 ** d) / 10 ** d);
const kb = (o) => (JSON.stringify(o).length / 1024).toFixed(0) + ' KB';
const gravar = (nome, obj) => {
  const f = path.join(SAIDA, nome);
  fs.writeFileSync(f, JSON.stringify(obj));
  console.log(`  ${nome.padEnd(28)} ${(fs.statSync(f).size / 1024).toFixed(0).padStart(6)} KB`);
};
// Nada de caminhos da máquina nem dados pessoais no dist.
const sanear = (s) => String(s).replace(/\/mnt\/dados\/?[\w./-]*/g, '[disco local]').replace(/\/home\/[\w./-]+/g, '[pasta local]');

console.log('urna lab · build dos dados');

// ---------- registro de testes ----------
const registro = ler(path.join(RAIZ, 'testes', 'registro.json'));
const testes = registro.testes.map((t) => {
  const o = {};
  for (const k of Object.keys(t)) o[k] = typeof t[k] === 'string' ? sanear(t[k]) : Array.isArray(t[k]) ? t[k].map(sanear) : t[k];
  return o;
});
const emProc = (t) => t.situacao === 'a_fazer' || /^(a fazer|em processamento)/i.test(t.resultado_atual || '');
const categoria = (t) => (emProc(t) ? 'proc' : t.situacao === 'em_andamento' ? 'parc' : 'ok');
const placar = { total: testes.length, concluidos: 0, parciais: 0, processando: 0, exploratorios: 0, confirmatorios: 0, classes: {}, situacoes: {} };
for (const t of testes) {
  const c = categoria(t);
  if (c === 'ok') placar.concluidos++; else if (c === 'parc') placar.parciais++; else placar.processando++;
  if (t.natureza === 'exploratório') placar.exploratorios++; else placar.confirmatorios++;
  placar.classes[t.classe_evidencia] = (placar.classes[t.classe_evidencia] || 0) + 1;
  placar.situacoes[t.situacao] = (placar.situacoes[t.situacao] || 0) + 1;
}
gravar('registro.json', { descricao: registro.descricao, modelos_nulos: registro.modelos_nulos, classes: registro.classes, independencia: registro.independencia, testes, placar });

// ---------- dados do relatório (118 MB local) → testes.json (enxuto) ----------
const rd = ler(path.join(WEB, 'relatorio_dados.json'));
const novos = { ...(rd.novos || {}) };
for (const k of Object.keys(novos)) {
  const v = novos[k];
  if (v && typeof v === 'object' && Array.isArray(v.casos_lista)) {
    const { casos_lista, ...resto } = v;
    novos[k] = { ...resto, casos_lista_n: casos_lista.length };
  }
}
const bateria = {};
for (const ano of Object.keys(rd.bateria || {})) {
  const b = JSON.parse(JSON.stringify(rd.bateria[ano]));
  if (b.T25) for (const k of Object.keys(b.T25)) if (b.T25[k] && typeof b.T25[k] === 'object') delete b.T25[k].hist2d;
  bateria[ano] = b;
}
const testesDados = {
  totais_1: rd.totais_1, urnas_1: rd.urnas_1, totais_2: rd.totais_2, urnas_2: rd.urnas_2,
  z_hist: rd.z_hist, curva_max_desvio: rd.curva_max_desvio, curva: rd.curva, poder: rd.poder, biometria: rd.biometria,
  log_resumo: rd.log_resumo, bateria, novos,
};
gravar('testes.json', testesDados);

// ---------- home ----------
const dados = ler(path.join(WEB, 'dados.json'));
const logs = existe(path.join(WEB, 'logs.json')) ? ler(path.join(WEB, 'logs.json')) : null;
const mapas = ler(path.join(WEB, 'mapas_dados.json'));

// curva da apuração por minuto (a partir dos segundos do dados.json), por eixo de chegada no TSE
function apuracaoPorMinuto(turno, chavesPct, prev) {
  const s = dados[turno].recebido;
  const cands = dados[turno].chaves.filter((c) => c[0] === 'c');
  const ini = Math.floor(s.t[0] / 60), fim = Math.floor(s.t[s.t.length - 1] / 60);
  const min = [], urnas = [], pct = {}, pv = {};
  chavesPct.forEach((c) => (pct[c] = []));
  (prev || []).forEach((p) => (pv[p] = []));
  const ac = {}; [...dados[turno].chaves, ...(prev || [])].forEach((c) => (ac[c] = 0));
  let uAc = 0, i = 0;
  for (let m = ini; m <= fim; m++) {
    while (i < s.t.length && s.t[i] < (m + 1) * 60) {
      for (const c of Object.keys(ac)) if (s[c]) ac[c] += s[c][i];
      uAc += s.urnas[i]; i++;
    }
    const val = cands.reduce((a, c) => a + ac[c], 0);
    const tot = val + (ac.branco || 0) + (ac.nulo || 0);
    min.push(m); urnas.push(uAc);
    for (const c of chavesPct) pct[c].push(val ? r((100 * ac[c]) / (c === 'branco' || c === 'nulo' ? tot : val), 3) : null);
    for (const p of prev || []) pv[p].push(val ? r((100 * ac[p]) / val, 3) : null);
  }
  return { min, urnas, pct, prev: pv, total_urnas: dados[turno].total_urnas, nomes: dados[turno].nomes };
}
const top1 = dados.t1.chaves.filter((c) => c[0] === 'c').slice(0, 5);
const apuracao = {
  t1: apuracaoPorMinuto('t1', [...top1, 'branco', 'nulo']),
  t2: apuracaoPorMinuto('t2', ['c13', 'c22', 'branco', 'nulo'], ['p13m', 'p13e']),
};
// logs: votos por minuto (hora do dia, Brasília)
const BASE_T = { t1: 0, t2: 0 };
const logsMin = logs ? Object.fromEntries(Object.entries(logs).map(([k, v]) => [k, { t: v.t, votos: v.votos }])) : (rd.logs || null);

const nacional = {};
for (const ano of Object.keys(mapas.anos)) nacional[ano] = { ...mapas.anos[ano].nacional, virada_nacional: mapas.anos[ano].virada_nacional };
const ufs = {};
for (const ano of Object.keys(mapas.anos)) {
  ufs[ano] = {};
  for (const [uf, v] of Object.entries(mapas.anos[ano].ufs)) ufs[ano][uf] = Object.fromEntries(Object.entries(v).map(([k, x]) => [k, r(x, 3)]));
}
const fluxo = {};
for (const ano of Object.keys(mapas.anos)) if (mapas.anos[ano].fluxo) fluxo[ano] = mapas.anos[ano].fluxo;

const home = {
  gerado_em: new Date().toISOString().slice(0, 10),
  fonte: mapas.fonte,
  totais_1: rd.totais_1, urnas_1: rd.urnas_1, totais_2: rd.totais_2, urnas_2: rd.urnas_2,
  nomes_1: dados.t1.nomes, nomes_2: dados.t2.nomes, datas: { t1: dados.t1.data, t2: dados.t2.data },
  margem_votos: rd.poder.margem_real_votos,
  nacional, ufs, fluxo,
  apuracao, logs: logsMin, curva: rd.curva, curva_max_desvio: rd.curva_max_desvio,
  z_hist: rd.z_hist,
  log_resumo: rd.log_resumo,
  poder: { margem_real_votos: rd.poder.margem_real_votos, cenarios: rd.poder.linhas.length, detectados: rd.poder.linhas.filter((l) => l.algum).length,
    maior_passou_votos: Math.max(0, ...rd.poder.linhas.filter((l) => !l.algum && !/uniforme/i.test(l.grupo)).map((l) => l.votos)),
    grupos: [...new Set(rd.poder.linhas.map((l) => l.grupo))].map((g) => ({ grupo: g, n: rd.poder.linhas.filter((l) => l.grupo === g).length, detectados: rd.poder.linhas.filter((l) => l.grupo === g && l.algum).length })) },
  placar,
  klimek20: Object.fromEntries(Object.keys(mapas.anos).map((a) => [a, mapas.anos[a].klimek20 || null])),
};
gravar('home.json', home);

// ---------- mapas ----------
const codigos = Object.keys(mapas.anos['2026'].municipios);
const m26 = codigos.map((c) => { const m = mapas.anos['2026'].municipios[c]; return [r(m.lula1, 1), r(m.lula2, 1), r(m.virada, 1), r(m.comp1, 1), r(m.comp2, 1), m.eleitores, m.ganho_lula, m.ganho_adv]; });
gravar('mapas.json', {
  fonte: mapas.fonte, nacional, campos: ['lula1', 'lula2', 'virada', 'comp1', 'comp2', 'eleitores', 'ganho_lula', 'ganho_adv'],
  codigos, nomes: codigos.map((c) => mapas.anos['2026'].municipios[c].nome), uf: codigos.map((c) => mapas.anos['2026'].municipios[c].uf),
  municipios: m26, ufs, fluxo, klimek20: home.klimek20,
});
if (mapas.anos['2022']) {
  const m22 = codigos.map((c) => { const m = mapas.anos['2022'].municipios[c]; return m ? [r(m.lula1, 1), r(m.lula2, 1), r(m.virada, 1), m.eleitores] : null; });
  gravar('mapas-2022.json', { campos: ['lula1', 'lula2', 'virada', 'eleitores'], municipios: m22 });
}

// geo: malha IBGE simplificada (só para desenho)
function rewind(geo) {
  for (const f of geo.features) if (geoArea(f) > 2 * Math.PI) {
    const g = f.geometry;
    if (g.type === 'Polygon') g.coordinates = g.coordinates.map((x) => x.slice().reverse());
    else g.coordinates = g.coordinates.map((p) => p.map((x) => x.slice().reverse()));
  }
  return geo;
}
const gm = rewind(ler(path.join(WEB, 'geo', 'municipios.json')));
const gu = rewind(ler(path.join(WEB, 'geo', 'ufs.json')));
for (const f of gm.features) f.id = +f.properties.codarea, f.properties = {};
for (const f of gu.features) f.id = +f.properties.codarea, f.properties = {};
let topo = topology({ municipios: gm, ufs: gu });
topo = presimplify(topo);
topo = simplify(topo, quantile(topo, +(process.env.GEO_Q || 0.15))); // menor p = menos pontos (quantil do peso)
// remove anéis minúsculos que viraram pontos
for (const o of Object.values(topo.objects)) o.geometries = o.geometries.map((g) => { if (g.type === 'MultiPolygon') { const rs = g.arcs.filter((p) => p[0].length); return rs.length ? { ...g, arcs: rs } : { ...g, type: 'Polygon', arcs: g.arcs[0] }; } return g; });
topo = quantize(topo, +(process.env.GEO_N || 2000));
gravar('geo.json', topo);

// ---------- documentos (markdown → seções HTML) ----------
const DOCS = [
  ['visao-geral', 'README.md', 'Visão geral', 'O que é o estudo, o que tem no repositório e como reproduzir.'],
  ['diretriz', 'DIRETRIZ.md', 'Diretriz científica', 'Princípios, cinco níveis de investigação e classes de evidência A–G.'],
  ['protocolo', 'PROTOCOLO.md', 'Protocolo', 'Perguntas, modelos nulos, critérios fixados antes de rodar e emendas datadas.'],
  ['metodologia', 'METODOLOGIA.md', 'Metodologia matemática', 'A matemática de cada teste, camada por camada.'],
  ['autoauditoria', 'AUTOAUDITORIA.md', 'Autoauditoria', 'Mapa de ameaças, ameaças à validade, lacunas e como fechar.'],
  ['catalogo', 'CATALOGO.md', 'Catálogo', 'Linha do tempo, dados baixados, erros encontrados e corrigidos.'],
  ['pipeline', 'PIPELINE.md', 'Como reproduzir', 'Ordem de execução, dicionário de dados e formatos dos arquivos das urnas.'],
  ['referencias', 'REFERENCIAS.md', 'Referências', 'Bibliografia classificada: métodos forenses, Brasil, criptografia e dados.'],
  ['consumo', 'CONSUMO_IA.md', 'Consumo de IA', 'Tokens, custo e tempo de IA gastos pelo estudo, por modelo.'],
  ['contribuir', 'CONTRIBUTING.md', 'Como contribuir', 'Fork, pull request, discordância metodológica e licenças.'],
];
const GITHUB = 'https://github.com/doce42/urna-lab';
const slugify = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
const docSlug = Object.fromEntries(DOCS.map(([slug, arq]) => [arq, slug]));
marked.use({ gfm: true });
const ajustarLinks = (html) => html.replace(/href="([^"]*)"/g, (_, href) => {
  const m = href.match(/^([A-Za-z_./-]+\.md)(#.*)?$/);
  if (m) {
    const base = m[1].replace(/^\.\//, '');
    return `href="${docSlug[base] ? `#/docs/${docSlug[base]}` : `${GITHUB}/blob/main/${base}`}"`;
  }
  if (!/^(https?:|#|mailto:)/.test(href)) return `href="${GITHUB}/blob/main/${href.replace(/^\.\//, '')}" target="_blank" rel="noopener"`;
  if (/^https?:/.test(href)) return `href="${href}" target="_blank" rel="noopener"`;
  return `href="${href}"`;
});
const limparHtml = (h) => h.replace(/<[^>]+>/g, ' ').replace(/&[a-z]+;/g, ' ').replace(/\s+/g, ' ').trim();
const docs = [];
for (const [slug, arq, titulo, resumo] of DOCS) {
  const f = path.join(RAIZ, arq);
  if (!existe(f)) { console.warn('  (sem ' + arq + ')'); continue; }
  const md = sanear(fs.readFileSync(f, 'utf8'));
  const tokens = marked.lexer(md);
  // seções por título de nível 1/2 (H3 fica dentro)
  const secoes = [];
  let atual = { id: 'inicio', titulo: 'Introdução', nivel: 2, tokens: [] };
  for (const tk of tokens) {
    if (tk.type === 'heading' && tk.depth <= 2) {
      if (tk.depth === 1 && !secoes.length && !atual.tokens.length) continue; // título do arquivo
      if (atual.tokens.length) secoes.push(atual);
      atual = { id: slugify(tk.text).slice(0, 60) || 'secao-' + secoes.length, titulo: tk.text, nivel: tk.depth, tokens: [] };
    } else atual.tokens.push(tk);
  }
  if (atual.tokens.length) secoes.push(atual);
  const vistos = new Set();
  const out = secoes.map((s) => {
    let id = s.id; let n = 1; while (vistos.has(id)) id = `${s.id}-${++n}`; vistos.add(id);
    let html = ajustarLinks(marked.parser(s.tokens));
    html = html.replace(/<h3[^>]*>(.*?)<\/h3>/g, (_, t) => `<h3 id="${id}--${slugify(limparHtml(t)).slice(0, 50)}">${t}</h3>`);
    return { id, titulo: s.titulo, html, texto: limparHtml(html).slice(0, 4000) };
  });
  docs.push({ slug, arquivo: arq, titulo, resumo, github: `${GITHUB}/blob/main/${arq}`, secoes: out });
}
gravar('docs.json', { github: GITHUB, docs });

// índice leve (para menu e busca sem baixar tudo)
gravar('docs-indice.json', { github: GITHUB, docs: docs.map((d) => ({ slug: d.slug, arquivo: d.arquivo, titulo: d.titulo, resumo: d.resumo, secoes: d.secoes.map((s) => ({ id: s.id, titulo: s.titulo })) })) });

// relatório em PDF: o site mostra o botão só se o arquivo existir em public/
const pdf = path.join(AQUI, 'public', 'relatorio.pdf');
gravar('meta.json', { gerado_em: home.gerado_em, pdf: existe(pdf), github: GITHUB, testes: placar.total });
console.log('ok');
