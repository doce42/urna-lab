import { useEffect, useMemo, useState } from 'react';
import { Search, Github, FileDown, ArrowRight, ExternalLink, ChevronRight } from 'lucide-react';
import { clsx } from 'clsx';
import type { Docs as DocsDados, Doc, Meta } from '@/lib/tipos';
import { useDados } from '@/lib/dados';
import { Eyebrow, BotaoLink, SkeletonBloco, Skeleton, Erro, Nota } from '@/ui/base';

const GRUPOS: [string, string[]][] = [['Começar', ['visao-geral', 'diretriz']], ['Método', ['protocolo', 'metodologia', 'autoauditoria']], ['Dados e reprodução', ['catalogo', 'pipeline', 'referencias']], ['Projeto', ['consumo', 'contribuir']]];

export function Docs({ partes, meta }: { partes: string[]; meta: Meta | null }) {
  const { dados, erro, recarregar } = useDados<DocsDados>('docs');
  const slug = partes[0] || '';
  const secaoAlvo = partes[1];
  const q = new URLSearchParams(location.hash.split('?')[1] || '');
  const [busca, setBusca] = useState(q.get('busca') || '');
  useEffect(() => { setBusca(q.get('busca') || ''); }, [partes.join('/'), location.hash.split('?')[1]]);
  const doc = dados?.docs.find((d) => d.slug === slug) || null;
  const github = dados?.github || meta?.github || 'https://github.com/doce42/urna-lab';
  useEffect(() => {
    if (!doc) return;
    if (secaoAlvo) { const el = document.getElementById(`sec-${secaoAlvo}`); if (el) el.scrollIntoView({ block: 'start' }); else scrollTo(0, 0); }
    else if (busca && /^\d+(\.\d+)?$/.test(busca)) { const el = [...document.querySelectorAll('[data-secao]')].find((e) => (e as HTMLElement).dataset.secao?.startsWith(busca)); el?.scrollIntoView({ block: 'start' }); }
    else scrollTo(0, 0);
  }, [doc?.slug, secaoAlvo]);
  const resultados = useMemo(() => {
    const t = busca.trim().toLowerCase(); if (!dados || t.length < 2) return null;
    const out: { doc: Doc; id: string; titulo: string; trecho: string }[] = [];
    for (const d of dados.docs) for (const s of d.secoes) { const txt = (s.titulo + ' ' + s.texto).toLowerCase(); const i = txt.indexOf(t); if (i >= 0) out.push({ doc: d, id: s.id, titulo: s.titulo, trecho: s.texto.slice(Math.max(0, i - 70), i + 110) }); }
    return out.slice(0, 40);
  }, [busca, dados]);

  const NavDocs = () => (<>
            <a href="#/docs" className={clsx('text-[15px] font-medium h-9 flex items-center px-3 rounded-lg', !slug ? 'bg-surface-2 text-text' : 'text-muted hover:text-text')}>Central de ajuda</a>
            {GRUPOS.map(([g, slugs]) => (
              <div key={g}><div className="t-eyebrow px-3 mb-1.5">{g}</div>
                {slugs.map((s) => { const d = dados?.docs.find((x) => x.slug === s); const ativo = slug === s; return (
                  <div key={s}>
                    <a href={`#/docs/${s}`} className={clsx('text-[15px] h-9 flex items-center px-3 rounded-lg', ativo ? 'bg-surface-2 text-text font-medium' : 'text-muted hover:text-text')}>{d?.titulo || s}</a>
                    {ativo && d && <div className="ml-3 pl-3 border-l border-border my-1 hidden lg:block">{d.secoes.map((sec) => <a key={sec.id} href={`#/docs/${s}/${sec.id}`} className="block text-[13px] text-muted hover:text-text py-1.5 leading-snug">{sec.titulo}</a>)}</div>}
                  </div>); })}
              </div>
            ))}
            <div className="px-3 grid gap-2 text-sm">
              <a href={github} target="_blank" rel="noopener" className="inline-flex items-center gap-2 text-muted hover:text-text"><Github size={15} />Repositório no GitHub</a>
              {meta?.pdf && <a href="/relatorio.pdf" download className="inline-flex items-center gap-2 text-muted hover:text-text"><FileDown size={15} />Relatório completo em PDF</a>}
            </div>
          </>);
  return (
    <div className="container pt-10 md:pt-14 pb-8">
      <div className="grid gap-8 lg:grid-cols-[250px_minmax(0,1fr)] xl:grid-cols-[250px_minmax(0,1fr)_200px]">
        {/* lateral */}
        <aside className="lg:sticky lg:top-[calc(var(--topo)+16px)] lg:self-start lg:max-h-[calc(100vh-var(--topo)-32px)] lg:overflow-y-auto">
          <label className="relative block">
            <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-subtle" /><span className="vis-oculto">Buscar na documentação</span>
            <input value={busca} onChange={(e) => setBusca(e.target.value)} type="search" placeholder="Buscar na documentação" className="w-full h-11 pl-10 pr-3 rounded-full border border-border bg-surface text-[15px] placeholder:text-subtle outline-none focus:border-border-strong" />
          </label>
          <details className="lg:hidden mt-3 cartao px-4" open={!slug}>
            <summary className="h-12 flex items-center justify-between cursor-pointer font-medium list-none [&::-webkit-details-marker]:hidden">Navegar na documentação <ChevronRight size={16} className="text-subtle" /></summary>
            <div className="pb-3">{NavDocs()}</div>
          </details>
          <nav className="mt-5 hidden lg:grid gap-5" aria-label="Documentação">
            {NavDocs()}
          </nav>
        </aside>

        {/* conteúdo */}
        <div className="min-w-0 max-w-full">
          {erro && <Erro erro={erro} aoTentar={recarregar} />}
          {resultados && (
            <div className="mb-8 cartao p-5">
              <div className="text-sm text-muted mb-3">{resultados.length ? `${resultados.length} seções encontradas para “${busca}”` : `Nada encontrado para “${busca}”`}</div>
              <div className="grid gap-2">{resultados.map((r, i) => (
                <a key={i} href={`#/docs/${r.doc.slug}/${r.id}`} onClick={() => setBusca('')} className="rounded-lg border border-border p-3 hover:border-border-strong"><div className="text-xs text-subtle">{r.doc.titulo}</div><div className="font-medium">{r.titulo}</div><div className="text-[13px] text-muted mt-1">…{r.trecho}…</div></a>))}</div>
            </div>
          )}
          {!slug && (
            <div>
              <Eyebrow>Docs e ajuda</Eyebrow>
              <h1 className="t-h1 mt-2">Tudo o que você precisa para entender, reproduzir e contestar o estudo.</h1>
              <p className="t-lead mt-4 max-w-[60ch]">A metodologia completa, os critérios fixados antes de rodar, a autoauditoria e os caminhos para repetir cada passo. O que for muito extenso aponta para o arquivo original no GitHub.</p>
              <div className="mt-6 flex flex-wrap gap-3">
                <BotaoLink href={github} target="_blank" rel="noopener" variante="primario"><Github size={17} />Repositório doce42/urna-lab</BotaoLink>
                {meta?.pdf ? <BotaoLink href="/relatorio.pdf" download><FileDown size={17} />Relatório completo em PDF</BotaoLink> : <span className="inline-flex items-center h-11 px-4 rounded-full border border-dashed border-border text-sm text-subtle">Relatório em PDF: em breve</span>}
              </div>
              {!dados && !erro && <div className="mt-8 grid gap-3 sm:grid-cols-2">{Array.from({ length: 6 }).map((_, i) => <SkeletonBloco key={i} altura={120} />)}</div>}
              {dados && GRUPOS.map(([g, slugs]) => (
                <section key={g} className="mt-10"><h2 className="t-h3 mb-3">{g}</h2>
                  <div className="grid gap-3 sm:grid-cols-2">{slugs.map((s) => { const d = dados.docs.find((x) => x.slug === s); if (!d) return null; return (
                    <a key={s} href={`#/docs/${s}`} className="cartao cartao-hover p-5 flex flex-col gap-2"><div className="flex items-center justify-between gap-2"><div className="font-semibold">{d.titulo}</div><ArrowRight size={16} className="text-subtle" /></div><p className="text-[14px] text-muted leading-relaxed">{d.resumo}</p><div className="font-mono text-[11px] text-subtle mt-auto pt-1">{d.arquivo} · {d.secoes.length} seções</div></a>); })}</div>
                </section>
              ))}
              <section className="mt-10 cartao p-6">
                <h2 className="t-h3">Licença e como contribuir</h2>
                <p className="text-[15px] text-muted mt-2 leading-relaxed">Projeto livre: pode baixar, reproduzir, fazer fork, alterar e contradizer. Código sob MIT; documentação e resultados sob CC BY 4.0 (cite a fonte). Para propor mudanças: fork + pull request, validado por quem mantém. Discordância metodológica é bem-vinda e fica registrada.</p>
                <div className="mt-3 flex flex-wrap gap-2 text-sm"><a className="underline underline-offset-4 text-accent-text" href="#/docs/contribuir">Como contribuir</a><a className="underline underline-offset-4 text-accent-text inline-flex items-center gap-1" href={`${github}/blob/main/LICENSE`} target="_blank" rel="noopener">LICENSE (MIT) <ExternalLink size={12} /></a><a className="underline underline-offset-4 text-accent-text inline-flex items-center gap-1" href={`${github}/blob/main/LICENSE-DOCS`} target="_blank" rel="noopener">LICENSE-DOCS (CC BY 4.0) <ExternalLink size={12} /></a></div>
              </section>
            </div>
          )}
          {slug && !doc && !erro && <div><Skeleton linhas={2} className="max-w-md" /><SkeletonBloco altura={400} className="mt-6" /></div>}
          {doc && (
            <article>
              <div className="flex items-center gap-1.5 text-[13px] text-muted"><a href="#/docs" className="hover:text-text">Docs</a><ChevronRight size={14} /><span className="text-text">{doc.titulo}</span></div>
              <h1 className="t-h1 mt-3">{doc.titulo}</h1>
              <p className="t-lead mt-3 max-w-[60ch]">{doc.resumo}</p>
              <div className="mt-4 flex flex-wrap gap-2 items-center"><a className="inline-flex items-center gap-1.5 h-9 px-3.5 rounded-full border border-border text-sm font-medium hover:border-border-strong" href={doc.github} target="_blank" rel="noopener">Abrir {doc.arquivo} no GitHub <ExternalLink size={13} /></a><Nota>Renderizado a partir do arquivo original; o GitHub tem sempre a versão mais recente.</Nota></div>
              <div className="mt-10 flex flex-col gap-12 min-w-0">
                {doc.secoes.map((s, i) => (
                  <section key={s.id} id={`sec-${s.id}`} data-secao={s.titulo} className="scroll-mt-24 min-w-0 max-w-full">
                    <h2 className="t-h2 mb-4 pb-3 border-b border-border">{s.titulo}</h2>
                    <div className="prose-doc" dangerouslySetInnerHTML={{ __html: s.html }} />
                    {i === doc.secoes.length - 1 && <div className="mt-8 pt-5 border-t border-border text-sm text-muted">Fim de {doc.arquivo}. <a className="text-accent-text underline underline-offset-4" href={doc.github} target="_blank" rel="noopener">Ver no GitHub</a></div>}
                  </section>
                ))}
              </div>
            </article>
          )}
        </div>

        {/* índice da página (desktop largo) */}
        {doc && (
          <aside className="hidden xl:block sticky top-[calc(var(--topo)+16px)] self-start max-h-[calc(100vh-var(--topo)-32px)] overflow-y-auto">
            <div className="t-eyebrow mb-2">Nesta página</div>
            <nav className="grid" aria-label="Índice da página">{doc.secoes.map((s) => <a key={s.id} href={`#/docs/${doc.slug}/${s.id}`} className={clsx('text-[13px] py-1.5 leading-snug border-l-2 pl-3', secaoAlvo === s.id ? 'border-accent text-text' : 'border-border text-muted hover:text-text')}>{s.titulo}</a>)}</nav>
          </aside>
        )}
      </div>
    </div>
  );
}
