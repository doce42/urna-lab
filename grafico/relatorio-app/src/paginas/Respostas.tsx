// Perguntas e respostas científicas: uma resposta explícita por pergunta, com evidências, números, o que demonstra e o que não
// demonstra, validação, histórico e condições de reabertura. Lê fase3/respostas_f3.json (via dados/respostas.json).
import { useMemo, useState } from 'react';
import type { Registro } from '@/lib/tipos';
import { RespostaCentral, SeloSinal, useVeredito, type Veredito } from '@/ui/Sinal';
import { Eyebrow, SkeletonBloco, Erro } from '@/ui/base';
import { useDados } from '@/lib/dados';

type Pergunta = { id: string; pergunta: string; resposta: string; classificacao: string; evidencias: string[]; numeros: string; demonstra: string; nao_demonstra: string;
  robustez: string; causa: string; alcance: string; mudaria: string; validacao: string; por_ano: Record<string, string>; reabertura: string; em_votos: string };
type Item = { id: string; pergunta: string; resposta: string; classificacao: string; perguntas_relacionadas: string[]; evidencias: string[]; limitacao: string;
  historico: { etapa: string; estado: string; resposta: string }[]; detalhe: string; em_votos: string; fechamento?: string };
type Dados = { gerado: string; situacao: string; aviso: string; margem: string; capitulos: { id: string; titulo: string; perguntas: Pergunta[] }[]; inventario: Item[]; achados_sem_causa: string[]; limites: string[] };

const COR = (c: string) => c.startsWith('Demonstrado') ? 'var(--ok)' : c.startsWith('Refutado') ? 'var(--accent)' : c.startsWith('Parcialmente') ? 'var(--warn)' : c.startsWith('Não executado') ? 'var(--erro)' : 'var(--text-subtle)';
const Selo = ({ c }: { c: string }) => (
  <span className="inline-flex items-center gap-1.5 min-h-6 px-2 rounded-full text-xs font-medium border shrink-0" style={{ color: COR(c), borderColor: COR(c) }}><i className="w-1.5 h-1.5 rounded-full" style={{ background: COR(c) }} />{c}</span>
);
const EmVotos = ({ t }: { t: string }) => t && t !== '—' ? <p className="mt-2 text-[14.5px] leading-relaxed rounded-lg px-3 py-2" style={{ background: 'color-mix(in srgb, var(--accent) 8%, transparent)' }}><b className="font-medium text-text">Em votos: </b><span className="text-text">{t}</span></p> : null;
const Linha = ({ r, t }: { r: string; t: string }) => t ? <div><b className="font-medium text-text">{r}: </b>{t}</div> : null;

// Busca: a pessoa escreve uma pergunta e acha respostas, hipóteses e testes relacionados (sem acento, com sinônimos simples)
const norm = (x: string) => x.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
const PARADAS = new Set('a o os as de da do das dos e em no na nos nas um uma uns umas que se por para com sem foi ser ha houve teve tem como qual quais quanto quantos quantas onde quando isso esse essa este esta mais menos ou ao aos sobre entre ate pelo pela pelos pelas eh nao sim'.split(' '));
const SIN: Record<string, string[]> = { fraude: ['fraude', 'manipul', 'irregular', 'alter', 'troca'], fraudada: ['fraude', 'manipul', 'alter'], urna: ['urna', 'boletim', 'bu'], urnas: ['urna', 'boletim'],
  zero: ['zero', 'zeros'], zerada: ['zero'], virada: ['virada', 'lideranca', 'curva'], curva: ['curva', 'virada', 'apuracao'], biometria: ['biometria', 'biometr'], log: ['log'],
  assinatura: ['assinatura', 'certificado', 'criptograf'], hacker: ['manipul', 'software', 'alter'], software: ['software'], flavio: ['flavio', 'adversario'], bolsonaro: ['bolsonaro', 'adversario'],
  salvador: ['salvador'], manipulada: ['manipul', 'fabric', 'alter'], manipulado: ['manipul', 'fabric', 'alter'], alterado: ['alter', 'manipul'], alterados: ['alter', 'manipul'], batem: ['bate', 'iguais', 'conferem', 'coincid', 'diferen'], boletins: ['boletim', 'boletins', 'bu'], paulo: ['paulo', 'sp'], turno: ['turno', 'turnos'], abstencao: ['abstenc', 'comparecimento'], comparecimento: ['comparecimento', 'abstenc'] };
type Achado = { tipo: string; id: string; titulo: string; texto: string; link: string; pontos: number; sinal?: string };
function buscar(q: string, d: Dados, reg: Registro | undefined, v: Veredito | null): Achado[] {
  const toks = norm(q).split(/[^a-z0-9]+/).filter((t) => t.length > 2 && !PARADAS.has(t));
  if (!toks.length) return [];
  const grupos = toks.map((t) => SIN[t] || [t.length > 6 ? t.slice(0, 6) : t]);
  // peso de cada palavra pela raridade no conteúdo todo (palavras raras, como 'Salvador', valem mais que 'voto')
  const corpus = [...d.capitulos.flatMap((c) => c.perguntas.map((p) => p.pergunta + ' ' + p.resposta)), ...d.inventario.map((i) => i.pergunta + ' ' + i.resposta),
    ...(v?.hipoteses || []).map((h) => h.mecanismo + ' ' + h.resultado), ...(reg?.testes || []).map((t) => t.pergunta + ' ' + (t.resultado_atual || ''))].map(norm);
  const idf = grupos.map((g) => Math.log((corpus.length + 1) / (1 + corpus.filter((c) => g.some((x) => c.includes(x))).length)));
  const pont = (txt: string, peso: number) => { const n = norm(txt); return grupos.reduce((a, g, k) => a + (g.some((x) => n.includes(x)) ? peso * idf[k] : 0), 0); };
  const out: Achado[] = [];
  d.capitulos.forEach((c) => c.perguntas.forEach((p) => out.push({ tipo: 'Pergunta', id: p.id, titulo: p.pergunta, texto: p.resposta, link: `#${p.id}`, pontos: pont(p.pergunta, 3) + pont(p.resposta + ' ' + p.em_votos, 1) })));
  d.inventario.forEach((i) => out.push({ tipo: 'Item', id: i.id, titulo: i.pergunta, texto: i.resposta, link: `#inv-${i.id}`, pontos: pont(i.pergunta, 3) + pont(i.resposta, 1) }));
  v?.hipoteses.forEach((h) => out.push({ tipo: 'Hipótese', id: h.id, titulo: h.mecanismo, texto: `${h.status}. ${h.resultado}`, link: '#hipoteses', pontos: pont(h.mecanismo, 3) + pont(h.resultado + ' ' + h.o_que_deixaria, 1) }));
  reg?.testes.forEach((t) => out.push({ tipo: 'Teste', id: t.id, titulo: t.pergunta, texto: v?.sinal_por_teste[t.id]?.motivo || t.resultado_atual || '', link: `#/testes/${t.id}`, sinal: v?.sinal_por_teste[t.id]?.nivel,
    pontos: pont(t.pergunta, 3) + pont(`${t.resultado_atual || ''} ${t.interpretacao || ''} ${t.metodo || ''}`, 1) }));
  const maxPossivel = idf.reduce((x, y) => x + y, 0) * 4; const min = Math.max(0.18 * maxPossivel, 0.5);
  return out.filter((a) => a.pontos >= min).sort((a, b) => b.pontos - a.pontos).slice(0, 12);
}

function Busca({ d, reg, v }: { d: Dados; reg?: Registro; v: Veredito | null }) {
  const [q, setQ] = useState('');
  const res = useMemo(() => buscar(q, d, reg, v), [q, d, reg, v]);
  const nivel = (id?: string) => v?.niveis.find((n) => n.id === id)?.nome;
  const ir = (link: string) => (e: React.MouseEvent) => { if (link.startsWith('#') && !link.startsWith('#/')) { e.preventDefault(); const el = document.getElementById(link.slice(1)); if (el) el.scrollIntoView({ behavior: 'smooth' }); } };
  return (
    <div className="cartao p-4 md:p-5">
      <label htmlFor="busca-pergunta" className="t-h3 block">Faça a sua pergunta</label>
      <p className="text-muted text-[14px] mt-1">Escreva como falaria (por exemplo: "teve urna com zero voto para o Flávio?", "a virada foi manipulada?", "os boletins batem com o resultado?"). Mostramos as respostas, as hipóteses e os testes relacionados.</p>
      <input id="busca-pergunta" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Sua pergunta sobre a apuração de 2026" className="mt-3 w-full h-11 px-3 rounded-lg border border-border bg-surface text-[15px] outline-none focus:border-accent" />
      {q.trim().length > 2 && (res.length ? (
        <ul className="mt-3 grid gap-1.5">{res.map((a) => (
          <li key={a.tipo + a.id}><a href={a.link} onClick={ir(a.link)} className="block rounded-lg border border-border p-3 hover:border-accent">
            <div className="flex flex-wrap items-center gap-2"><span className="text-[11px] font-mono uppercase tracking-wider text-subtle">{a.tipo}</span><span className="font-mono text-xs font-semibold">{a.id}</span>{a.sinal && <SeloSinal nivel={a.sinal} nome={nivel(a.sinal)} />}</div>
            <div className="mt-1 text-[14.5px] text-text font-medium leading-snug">{a.titulo}</div>
            <div className="mt-0.5 text-[13.5px] text-muted line-clamp-2">{a.texto}</div>
          </a></li>
        ))}</ul>
      ) : <p className="mt-3 text-[14px] text-muted">Nada encontrado com essas palavras. Tente outras (urna, boletim, zero, virada, biometria, log, assinatura, Salvador).</p>)}
    </div>
  );
}

function CartaoPergunta({ p }: { p: Pergunta }) {
  return (
    <li id={p.id} className="cartao p-4 md:p-5 scroll-mt-20">
      <div className="flex flex-wrap items-start gap-x-3 gap-y-2"><span className="font-mono text-sm font-semibold w-10 shrink-0 pt-0.5">{p.id}</span><h3 className="text-[16px] font-medium text-text leading-snug flex-1 min-w-[14rem]">{p.pergunta}</h3><Selo c={p.classificacao} /></div>
      <p className="mt-2 text-[15px] text-text leading-relaxed">{p.resposta}</p>
      <EmVotos t={p.em_votos} />
      {Object.keys(p.por_ano).length > 0 && <div className="mt-2 grid gap-1 text-[14px] text-muted">{Object.entries(p.por_ano).map(([a, t]) => <div key={a}><b className="font-medium text-text">{a}: </b>{t}</div>)}</div>}
      <details className="mt-2 group/q">
        <summary className="cursor-pointer list-none text-[13px] text-accent-text hover:underline"><span className="group-open/q:hidden">números, evidências e limites</span><span className="hidden group-open/q:inline">recolher</span></summary>
        <div className="mt-2 grid gap-1.5 text-[14px] text-muted leading-relaxed">
          <Linha r="Números principais" t={p.numeros} /><Linha r="O que demonstra" t={p.demonstra} /><Linha r="O que não demonstra" t={p.nao_demonstra} />
          <Linha r="Robustez" t={p.robustez} /><Linha r="Causa" t={p.causa} /><Linha r="Alcance" t={p.alcance} /><Linha r="O que mudaria a resposta" t={p.mudaria} />
          <Linha r="Estado de validação" t={p.validacao} /><Linha r="Condição de reabertura" t={p.reabertura} />
          <div className="text-xs text-subtle break-words"><b className="font-medium">Evidências: </b>{p.evidencias.join(' · ')}</div>
        </div>
      </details>
    </li>
  );
}

export function Respostas({ reg }: { reg?: Registro }) {
  const { dados: d, erro, recarregar } = useDados<Dados>('respostas');
  const v = useVeredito();
  const [filtro, setFiltro] = useState('');
  if (erro) return <div className="container py-16"><Erro erro={erro} aoTentar={recarregar} /></div>;
  if (!d) return <div className="container py-16 grid gap-4"><SkeletonBloco altura={220} /><SkeletonBloco altura={320} /></div>;
  const todas = d.capitulos.flatMap((c) => c.perguntas);
  const cont: Record<string, number> = {};
  todas.forEach((p) => { const k = p.classificacao.split(' (')[0]; cont[k] = (cont[k] || 0) + 1; });
  const inv = d.inventario.filter((i) => !filtro || i.classificacao.startsWith(filtro));
  return (
    <div className="container pb-24">
      <header className="pt-10 md:pt-16 max-w-[54rem]">
        <Eyebrow>Fase 3 · {d.situacao}</Eyebrow>
        <h1 className="t-h1 mt-2">Perguntas e respostas científicas</h1>
        <p className="t-lead mt-4 text-[17px]">Uma resposta explícita para cada pergunta que motivou a pesquisa: o que foi demonstrado, o que foi refutado, o que ficou em parte e o que não pôde ser determinado com os dados disponíveis, e por quê.</p>
        <p className="mt-3 text-[14px] text-muted leading-relaxed border-l-2 border-border pl-3">{d.aviso} <b className="font-medium text-text">{d.margem}</b></p>
        <div className="mt-4 flex flex-wrap gap-1.5">{Object.entries(cont).map(([k, v]) => <Selo key={k} c={`${k}: ${v}`} />)}</div>
        <nav className="mt-5 flex flex-wrap gap-x-4 gap-y-1 text-[14px]">{d.capitulos.map((c) => <a key={c.id} href={`#${c.id}`} onClick={(e) => { e.preventDefault(); document.getElementById(c.id)?.scrollIntoView({ behavior: 'smooth' }); }} className="text-accent-text underline underline-offset-4">{c.titulo}</a>)}
          <a href="#inventario" onClick={(e) => { e.preventDefault(); document.getElementById('inventario')?.scrollIntoView({ behavior: 'smooth' }); }} className="text-accent-text underline underline-offset-4">Os 33 itens do inventário</a></nav>
      </header>
      <section className="mt-8"><Busca d={d} reg={reg} v={v} /></section>
      {v && <section id="hipoteses" className="mt-12 scroll-mt-20"><RespostaCentral v={v} /></section>}
      {d.capitulos.map((c) => (
        <section key={c.id} id={c.id} className="mt-14 md:mt-16 scroll-mt-20">
          <h2 className="t-h2">{c.titulo}</h2>
          <ul className="mt-5 grid gap-3">{c.perguntas.map((p) => <CartaoPergunta key={p.id} p={p} />)}</ul>
        </section>
      ))}
      <section id="sem-causa" className="mt-14 scroll-mt-20 max-w-[54rem]">
        <h2 className="t-h2">Achados que persistem sem causa demonstrada</h2>
        <ul className="mt-4 grid gap-2 text-[15px] text-muted list-disc pl-5">{d.achados_sem_causa.map((a) => <li key={a}>{a}</li>)}</ul>
        <h2 className="t-h2 mt-10">Limites das fontes e dos métodos</h2>
        <ul className="mt-4 grid gap-2 text-[15px] text-muted list-disc pl-5">{d.limites.map((a) => <li key={a}>{a}</li>)}</ul>
      </section>
      <section id="inventario" className="mt-14 scroll-mt-20">
        <h2 className="t-h2">Os 33 itens do inventário</h2>
        <p className="text-muted text-[15px] mt-2 max-w-[48rem]">Cada pergunta herdada da Fase 2 e cada pergunta nova da Fase 3, com a resposta direta, a ligação com as perguntas acima e o histórico de correções.</p>
        <div className="mt-3 flex flex-wrap gap-1.5 text-xs">{['', 'Demonstrado', 'Refutado', 'Parcialmente', 'Não determinado'].map((f) => <button key={f || 'todos'} onClick={() => setFiltro(f)} className={`h-7 px-2.5 rounded-full border ${filtro === f ? 'border-accent text-accent-text' : 'border-border text-muted'}`}>{f || 'todos'}</button>)}</div>
        <ul className="mt-4 grid gap-2">{inv.map((i) => (
          <li key={i.id} id={`inv-${i.id}`} className="cartao p-4 scroll-mt-20">
            <div className="flex flex-wrap items-start gap-x-3 gap-y-2"><span className="font-mono text-sm font-semibold w-12 shrink-0 pt-0.5">{i.id}</span><span className="text-[15px] text-text font-medium leading-snug flex-1 min-w-[14rem]">{i.pergunta}</span><Selo c={i.classificacao} /></div>
            <p className="mt-1.5 text-[14.5px] text-muted leading-relaxed">{i.resposta}</p>
            <EmVotos t={i.em_votos} />
            {i.fechamento && <div className="mt-1.5 text-[13px] text-subtle"><b className="font-medium text-muted">Fechamento: </b>{i.fechamento}</div>}
            {i.perguntas_relacionadas.length > 0 && <div className="mt-1 text-[13px] text-subtle">Ver {i.perguntas_relacionadas.map((q, k) => <span key={q}>{k ? ', ' : ''}<a href={`#${q}`} onClick={(e) => { e.preventDefault(); document.getElementById(q)?.scrollIntoView({ behavior: 'smooth' }); }} className="text-accent-text underline underline-offset-2">{q}</a></span>)}</div>}
            <details className="mt-1.5 group/q">
              <summary className="cursor-pointer list-none text-[12.5px] text-subtle hover:text-text"><span className="group-open/q:hidden">detalhe, evidências e histórico</span><span className="hidden group-open/q:inline">recolher</span></summary>
              <div className="mt-2 grid gap-1.5 text-[13.5px] text-muted">
                <Linha r="Detalhe" t={i.detalhe} /><Linha r="O que falta" t={i.limitacao} />
                {i.historico.map((h, k) => <div key={k} className="text-xs text-subtle"><b className="font-medium">Antes ({h.etapa}):</b> {h.estado}</div>)}
                <div className="text-xs text-subtle break-words"><b className="font-medium">Evidências: </b>{i.evidencias.join(' · ')}</div>
              </div>
            </details>
          </li>
        ))}</ul>
      </section>
    </div>
  );
}
