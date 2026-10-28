// Perguntas e respostas científicas: uma resposta explícita por pergunta, com evidências, números, o que demonstra e o que não
// demonstra, validação, histórico e condições de reabertura. Lê fase3/respostas_f3.json (via dados/respostas.json).
import { useState } from 'react';
import { Eyebrow, SkeletonBloco, Erro } from '@/ui/base';
import { useDados } from '@/lib/dados';

type Pergunta = { id: string; pergunta: string; resposta: string; classificacao: string; evidencias: string[]; numeros: string; demonstra: string; nao_demonstra: string;
  robustez: string; causa: string; alcance: string; mudaria: string; validacao: string; por_ano: Record<string, string>; reabertura: string };
type Item = { id: string; pergunta: string; resposta: string; classificacao: string; perguntas_relacionadas: string[]; evidencias: string[]; limitacao: string;
  historico: { etapa: string; estado: string; resposta: string }[]; detalhe: string };
type Dados = { gerado: string; situacao: string; aviso: string; capitulos: { id: string; titulo: string; perguntas: Pergunta[] }[]; inventario: Item[]; achados_sem_causa: string[]; limites: string[] };

const COR = (c: string) => c.startsWith('Demonstrado') ? 'var(--ok)' : c.startsWith('Refutado') ? 'var(--accent)' : c.startsWith('Parcialmente') ? 'var(--warn)' : c.startsWith('Não executado') ? 'var(--erro)' : 'var(--text-subtle)';
const Selo = ({ c }: { c: string }) => (
  <span className="inline-flex items-center gap-1.5 min-h-6 px-2 rounded-full text-xs font-medium border shrink-0" style={{ color: COR(c), borderColor: COR(c) }}><i className="w-1.5 h-1.5 rounded-full" style={{ background: COR(c) }} />{c}</span>
);
const Linha = ({ r, t }: { r: string; t: string }) => t ? <div><b className="font-medium text-text">{r}: </b>{t}</div> : null;

function CartaoPergunta({ p }: { p: Pergunta }) {
  return (
    <li id={p.id} className="cartao p-4 md:p-5 scroll-mt-20">
      <div className="flex flex-wrap items-start gap-x-3 gap-y-2"><span className="font-mono text-sm font-semibold w-10 shrink-0 pt-0.5">{p.id}</span><h3 className="text-[16px] font-medium text-text leading-snug flex-1 min-w-[14rem]">{p.pergunta}</h3><Selo c={p.classificacao} /></div>
      <p className="mt-2 text-[15px] text-text leading-relaxed">{p.resposta}</p>
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

export function Respostas() {
  const { dados: d, erro, recarregar } = useDados<Dados>('respostas');
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
        <p className="mt-3 text-[14px] text-muted leading-relaxed border-l-2 border-border pl-3">{d.aviso}</p>
        <div className="mt-4 flex flex-wrap gap-1.5">{Object.entries(cont).map(([k, v]) => <Selo key={k} c={`${k}: ${v}`} />)}</div>
        <nav className="mt-5 flex flex-wrap gap-x-4 gap-y-1 text-[14px]">{d.capitulos.map((c) => <a key={c.id} href={`#${c.id}`} onClick={(e) => { e.preventDefault(); document.getElementById(c.id)?.scrollIntoView({ behavior: 'smooth' }); }} className="text-accent-text underline underline-offset-4">{c.titulo}</a>)}
          <a href="#inventario" onClick={(e) => { e.preventDefault(); document.getElementById('inventario')?.scrollIntoView({ behavior: 'smooth' }); }} className="text-accent-text underline underline-offset-4">Os 33 itens do inventário</a></nav>
      </header>
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
          <li key={i.id} className="cartao p-4">
            <div className="flex flex-wrap items-start gap-x-3 gap-y-2"><span className="font-mono text-sm font-semibold w-12 shrink-0 pt-0.5">{i.id}</span><span className="text-[15px] text-text font-medium leading-snug flex-1 min-w-[14rem]">{i.pergunta}</span><Selo c={i.classificacao} /></div>
            <p className="mt-1.5 text-[14.5px] text-muted leading-relaxed">{i.resposta}</p>
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
