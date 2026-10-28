import { useEffect, useMemo, useState, type ReactNode } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { Search, X, ArrowUpRight, ExternalLink } from 'lucide-react';
import { clsx } from 'clsx';
import { HistoriaCientifica } from '@/ui/Historico';
import type { Registro, Teste, TestesDados, Meta } from '@/lib/tipos';
import { useDados } from '@/lib/dados';
import { irPara } from '@/lib/rotas';
import { Botao, Chip, Eyebrow, SeloClasse, SeloEstado, SkeletonBloco, Erro, Nota, CLASSE_COR, CLASSE_EXPL } from '@/ui/base';
import { VIZ, generico, categoria, emProc, preliminar, MODS, ESTADO_TXT, AVISO_RE, MET, type Ctx, type Viz } from '@/viz/testes';
import { Processando } from '@/graficos/primitivos';

function montarCtx(d: TestesDados, reg: Registro, t: Teste): Ctx { return { d, t, reg, nv: d.novos || {}, bt22: (d.bateria || {})['2022'], bt26: (d.bateria || {})['2026'] }; }
function vizDe(c: Ctx): NonNullable<Viz> {
  const proc = emProc(c.t); let v: Viz = null;
  if (!proc || c.t.id === 'C02') { try { v = (VIZ[c.t.id] || generico)(c); } catch (e) { console.warn(c.t.id, e); v = null; } }
  if (!v || !v.el) v = proc ? { ler: 'Este teste ainda não tem resultado para exibir.', el: null } : generico(c);
  return v || { ler: '', el: null };
}
const sentencaDe = (t: Teste) => { const s = (t.resultado_atual || '').split(/(?<=\.)\s/)[0]; return { s, longo: (t.resultado_atual || '').length > s.length + 3 || s.length > 240 }; };

export function Testes({ reg, meta, partes }: { reg: Registro; meta: Meta | null; partes: string[] }) {
  const { dados: d, erro, recarregar } = useDados<TestesDados>('testes');
  const q0 = new URLSearchParams(location.hash.split('?')[1] || '');
  const [busca, setBusca] = useState(q0.get('q') || '');
  const [classes, setClasses] = useState<Set<string>>(() => new Set(q0.get('classe') ? [q0.get('classe')!] : []));
  const [estados, setEstados] = useState<Set<string>>(() => new Set(q0.get('estado') ? [q0.get('estado')!] : []));
  const [modulos, setModulos] = useState<Set<string>>(new Set());
  const [natureza, setNatureza] = useState<string | null>(null);
  const aberto = partes[0] || null;
  useEffect(() => { const q = new URLSearchParams(location.hash.split('?')[1] || ''); if (q.get('classe')) setClasses(new Set([q.get('classe')!])); if (q.get('estado')) setEstados(new Set([q.get('estado')!])); if (q.get('q') != null) setBusca(q.get('q')!); }, [location.hash.split('?')[1]]);
  const testeAberto = aberto ? reg.testes.find((t) => t.id === aberto) || null : null;
  const alternar = (set: Set<string>, k: string, f: (s: Set<string>) => void) => { const n = new Set(set); n.has(k) ? n.delete(k) : n.add(k); f(n); };
  const limpar = () => { setBusca(''); setClasses(new Set()); setEstados(new Set()); setModulos(new Set()); setNatureza(null); };
  const ativo = busca || classes.size || estados.size || modulos.size || natureza;
  const visiveis = useMemo(() => reg.testes.filter((t) => {
    const txt = [t.id, t.pergunta, t.metodo, t.resultado_atual, t.hipotese_nula, (t.anotacoes || []).join(' ')].join(' ').toLowerCase();
    return (!busca || txt.includes(busca.toLowerCase())) && (!classes.size || classes.has(t.classe_evidencia)) && (!estados.size || estados.has(categoria(t))) && (!modulos.size || modulos.has(t.modulo)) && (!natureza || t.natureza === natureza);
  }), [reg, busca, classes, estados, modulos, natureza]);
  const contClasse: Record<string, number> = {}, contEstado: Record<string, number> = {}, contMod: Record<string, number> = {};
  reg.testes.forEach((t) => { contClasse[t.classe_evidencia] = (contClasse[t.classe_evidencia] || 0) + 1; contEstado[categoria(t)] = (contEstado[categoria(t)] || 0) + 1; contMod[t.modulo] = (contMod[t.modulo] || 0) + 1; });
  const porModulo = 'ABCDEF'.split('').map((m) => ({ m, ts: visiveis.filter((t) => t.modulo === m) })).filter((x) => x.ts.length);
  return (
    <div className="container pt-10 md:pt-16 pb-8">
      <div className="max-w-[52rem]">
        <Eyebrow>Testes · {reg.testes.length} registrados</Eyebrow>
        <h1 className="t-h1 mt-2">Cada teste com pergunta, hipótese nula, resultado e limite.</h1>
        <p className="t-lead mt-4">Organizados em seis módulos, do dado bruto à forense estatística. Clique num cartão para abrir o detalhe: como ler o gráfico, método, o que o teste não consegue ver, anotações e como reproduzir.</p>
      </div>

      {/* filtros */}
      <div className="mt-8 cartao p-4 md:p-5 lg:sticky lg:top-[calc(var(--topo)+8px)] z-20 bg-surface/95 backdrop-blur">
        <div className="flex flex-wrap gap-3 items-center">
          <label className="relative flex-1 min-w-[220px]">
            <Search size={17} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-subtle" />
            <span className="vis-oculto">Buscar teste por código ou pergunta</span>
            <input value={busca} onChange={(e) => setBusca(e.target.value)} type="search" placeholder="Buscar teste (ex.: T02, assinatura, biometria)" autoComplete="off"
              className="w-full h-11 pl-10 pr-4 rounded-full border border-border bg-bg text-[15px] placeholder:text-subtle focus:border-border-strong outline-none" />
          </label>
          <div className="flex gap-1.5 flex-wrap">
            {(['ok', 'parc', 'proc'] as const).map((k) => <Chip key={k} ativo={estados.has(k)} onClick={() => alternar(estados, k, setEstados)} cor={k === 'ok' ? 'var(--ok)' : k === 'parc' ? 'var(--warn)' : 'var(--text-subtle)'}>{k === 'ok' ? 'concluído' : k === 'parc' ? 'parcial' : 'processando'} · {contEstado[k] || 0}</Chip>)}
          </div>
          <div className="text-sm text-muted ml-auto t-num" aria-live="polite">{ativo ? `${visiveis.length} de ${reg.testes.length}` : `${reg.testes.length} testes`}{ativo ? <button className="ml-3 text-accent-text font-medium underline underline-offset-4" onClick={limpar}>limpar</button> : null}</div>
        </div>
        <div className="mt-3 flex flex-wrap gap-1.5">
          {'ABCDEFG'.split('').map((k) => <Chip key={k} ativo={classes.has(k)} onClick={() => alternar(classes, k, setClasses)} cor={CLASSE_COR[k]} title={CLASSE_EXPL[k]}><b className="font-semibold">{k}</b> <span className="hidden sm:inline">{reg.classes[k].split(' / ')[0]}</span> · {contClasse[k] || 0}</Chip>)}
          <span className="w-px h-6 bg-border mx-1 self-center hidden md:block" />
          {'ABCDEF'.split('').filter((m) => contMod[m]).map((m) => <Chip key={m} ativo={modulos.has(m)} onClick={() => alternar(modulos, m, setModulos)}>módulo {m} · {contMod[m]}</Chip>)}
          <span className="w-px h-6 bg-border mx-1 self-center hidden md:block" />
          {['confirmatório', 'exploratório'].map((n) => <Chip key={n} ativo={natureza === n} onClick={() => setNatureza(natureza === n ? null : n)}>{n}</Chip>)}
        </div>
      </div>

      {erro && <div className="mt-8"><Erro erro={erro} aoTentar={recarregar} /></div>}
      {!d && !erro && <div className="mt-8 grid gap-4 md:grid-cols-2">{Array.from({ length: 6 }).map((_, i) => <SkeletonBloco key={i} altura={300} />)}</div>}

      {d && porModulo.map(({ m, ts }) => (
        <section key={m} id={`mod-${m}`} className="mt-14 scroll-mt-28">
          <div className="flex items-start gap-4">
            <span className="grid place-items-center w-11 h-11 rounded-xl bg-brand text-brand-contrast font-semibold text-lg shrink-0">{m}</span>
            <div><h2 className="t-h2">{MODS[m][0]} <span className="text-subtle font-normal text-base ml-1 t-num">{ts.length === contMod[m] ? `${ts.length} testes` : `${ts.length} de ${contMod[m]}`}</span></h2><p className="text-muted mt-1 max-w-[80ch]">{MODS[m][1]}</p></div>
          </div>
          <div className="mt-6 grid gap-4 md:grid-cols-2 items-start">
            {ts.map((t) => <Cartao key={t.id} t={t} reg={reg} d={d} />)}
          </div>
        </section>
      ))}
      {d && !porModulo.length && <div className="mt-10 cartao p-8 text-center text-muted">Nenhum teste combina com os filtros. <button className="text-accent-text underline underline-offset-4 ml-1" onClick={limpar}>Limpar filtros</button></div>}

      <Dialog.Root open={!!testeAberto} onOpenChange={(o) => { if (!o) irPara('/testes'); }}>
        <Dialog.Portal>
          <Dialog.Overlay className="gaveta-overlay" />
          <Dialog.Content className="gaveta" aria-describedby={undefined}>
            {testeAberto && d && <Detalhe t={testeAberto} reg={reg} d={d} meta={meta} />}
            {testeAberto && !d && <div className="p-6"><Dialog.Title className="t-h3">{testeAberto.id}</Dialog.Title><SkeletonBloco altura={300} className="mt-4" /></div>}
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>
    </div>
  );
}

function Cartao({ t, reg, d }: { t: Teste; reg: Registro; d: TestesDados }) {
  const v = useMemo(() => vizDe(montarCtx(d, reg, t)), [d, reg, t]);
  const cat = categoria(t), proc = emProc(t), { s } = sentencaDe(t);
  const parc = (t.resultado_atual.match(/\((AP:[^)]*)\)/) || [])[1];
  const prelim = preliminar(t) && !proc;
  return (
    <article id={`t-${t.id}`} className="cartao cartao-hover overflow-hidden flex flex-col min-w-0 scroll-mt-28" style={{ ['--cor' as string]: CLASSE_COR[t.classe_evidencia] }}>
      <a href={`#/testes/${t.id}`} className="block p-5 pb-4 group" aria-label={`${t.id}: ${t.pergunta}`}>
        <div className="flex flex-wrap items-center gap-2">
          <span className="font-mono text-xs font-medium h-7 px-2.5 inline-flex items-center rounded-md border border-border bg-surface-2">{t.id}</span>
          <SeloClasse classe={t.classe_evidencia} nome={reg.classes[t.classe_evidencia]} />
          <SeloEstado estado={cat} texto={proc ? 'em processamento' : (ESTADO_TXT[t.situacao] || t.situacao) + (t.situacao === 'em_andamento' ? ' (parcial)' : '')} />
          {prelim && <span className="inline-flex items-center h-7 px-2.5 rounded-full text-xs font-medium border border-warn/50 text-warn" style={{ background: 'var(--warn-soft)' }}>preliminar · em reprocessamento</span>}
          <ArrowUpRight size={18} className="ml-auto text-subtle group-hover:text-text transition-colors" />
        </div>
        <h3 className="t-h3 mt-3 leading-snug">{t.pergunta}</h3>
        <div className="mt-3 border-l-[3px] pl-3" style={{ borderColor: 'var(--cor)' }}>
          <div className="text-[11px] font-mono uppercase tracking-wider text-muted">Resultado</div>
          <p className="text-[15px] font-medium leading-snug mt-0.5">{proc ? 'Ainda sem resultado desta versão.' : s || 'Sem resultado registrado.'}</p>
        </div>
      </a>
      <div className="px-5 pb-5 relative">
        <div className="max-h-[260px] overflow-hidden relative">
          {v.el}
          {proc && <Processando msg="Em processamento" sub={parc ? 'Parcial já registrado: ' + parc : 'Sem resultado ainda; nenhum número foi inventado.'} />}
          <div className="absolute inset-x-0 bottom-0 h-16 pointer-events-none" style={{ background: 'linear-gradient(to bottom, transparent, var(--surface))' }} />
        </div>
        <a href={`#/testes/${t.id}`} className="mt-1 inline-flex items-center gap-1 h-10 text-sm font-medium text-accent-text">Abrir detalhe completo <ArrowUpRight size={15} /></a>
      </div>
    </article>
  );
}

function Bloco({ titulo, children, aberto }: { titulo: string; children: ReactNode; aberto?: boolean }) {
  return (
    <details open={aberto} className="group border-t border-border">
      <summary className="min-h-[52px] flex items-center gap-2 cursor-pointer font-medium text-[15px] list-none [&::-webkit-details-marker]:hidden select-none">
        <span className="w-5 h-5 grid place-items-center rounded-full bg-surface-2 text-subtle text-xs transition-transform group-open:rotate-90">▸</span>{titulo}
      </summary>
      <div className="pb-5 text-[15px] text-muted leading-relaxed">{children}</div>
    </details>
  );
}

export function Detalhe({ t, reg, d, meta }: { t: Teste; reg: Registro; d: TestesDados; meta: Meta | null }) {
  const v = useMemo(() => vizDe(montarCtx(d, reg, t)), [d, reg, t]);
  const cat = categoria(t), proc = emProc(t), { s, longo } = sentencaDe(t);
  const parc = (t.resultado_atual.match(/\((AP:[^)]*)\)/) || [])[1];
  const anots = t.anotacoes || [];
  const idx = reg.testes.findIndex((x) => x.id === t.id), ant = reg.testes[idx - 1], prox = reg.testes[idx + 1];
  useEffect(() => { document.querySelector('.gaveta')?.scrollTo({ top: 0 }); }, [t.id]);
  const met = MET[t.id];
  return (
    <div className="p-5 md:p-8">
      <div className="flex items-center gap-2 flex-wrap">
        <span className="font-mono text-xs font-medium h-7 px-2.5 inline-flex items-center rounded-md border border-border bg-surface-2">{t.id}</span>
        <span className="text-xs text-muted">módulo {t.modulo} · {MODS[t.modulo]?.[0]}</span>
        <Dialog.Close asChild><Botao icone tamanho="sm" className="ml-auto" aria-label="Fechar"><X size={18} /></Botao></Dialog.Close>
      </div>
      <Dialog.Title className="t-h2 mt-4">{t.pergunta}</Dialog.Title>
      <div className="mt-4 flex flex-wrap gap-2">
        <SeloClasse classe={t.classe_evidencia} nome={reg.classes[t.classe_evidencia]} grande />
        <SeloEstado estado={cat} texto={proc ? 'em processamento' : (ESTADO_TXT[t.situacao] || t.situacao) + (t.situacao === 'em_andamento' ? ' (parcial)' : '')} />
        {preliminar(t) && !proc && <span className="inline-flex items-center h-7 px-2.5 rounded-full text-xs font-medium border border-warn/50 text-warn" style={{ background: 'var(--warn-soft)' }}>preliminar · em reprocessamento</span>}
        {[t.natureza, t.afirmacao, t.independencia ? `independência: ${t.independencia}` : '', t.modelo_nulo ? `nulo ${t.modelo_nulo}` : ''].filter(Boolean).map((x) => <span key={x} className="inline-flex items-center h-7 px-2.5 rounded-full text-xs border border-border text-muted" title={x.startsWith('independência') ? reg.independencia[t.independencia] : x.startsWith('nulo') ? reg.modelos_nulos[t.modelo_nulo] : undefined}>{x}</span>)}
      </div>
      <div className="mt-6 rounded-lg border-l-4 pl-4 py-1" style={{ borderColor: CLASSE_COR[t.classe_evidencia] }}>
        <div className="text-[11px] font-mono uppercase tracking-wider text-muted">Resultado</div>
        <p className="text-lg font-medium leading-snug mt-1">{proc ? 'Ainda sem resultado desta versão.' : s || 'Sem resultado registrado.'}</p>
        {proc && t.resultado_atual && !/^(a fazer|em processamento)/i.test(t.resultado_atual) && <Nota className="mt-2">Registro anterior (não reexecutado): {t.resultado_atual}</Nota>}
        {longo && !proc && <p className="text-[15px] text-muted mt-2 leading-relaxed">{t.resultado_atual}</p>}
        {t.impacto_votos && !proc && <p className="text-[14px] mt-2 text-text"><b className="font-medium">Em votos:</b> <span className="text-muted">{t.impacto_votos}</span></p>}
      </div>
      <div className="mt-6 cartao p-4 md:p-5">
        {v.el}
        {proc && <Processando msg="Em processamento" sub={parc ? 'Parcial já registrado: ' + parc : 'Sem resultado ainda; nenhum número foi inventado.'} />}
        {v.ler && <p className="text-[13.5px] text-muted mt-4 pt-3 border-t border-border"><b className="text-text font-medium">Como ler:</b> {v.ler}</p>}
      </div>
      <div className="mt-6">
        <Bloco titulo="Método e hipótese nula" aberto>
          <p><b className="text-text font-medium">Método:</b> {t.metodo}</p>
          {t.hipotese_nula && <p className="mt-2"><b className="text-text font-medium">Hipótese nula:</b> {t.hipotese_nula}</p>}
          {t.pressupostos && <p className="mt-2"><b className="text-text font-medium">Pressupostos:</b> {t.pressupostos}</p>}
          {t.referencia && <p className="mt-2"><b className="text-text font-medium">Referência:</b> {t.referencia}</p>}
        </Bloco>
        <Bloco titulo="O que este teste não consegue ver" aberto><p>{t.limitacoes || 'Limitação não detalhada no registro.'}</p></Bloco>
        <Bloco titulo={`História científica (${(t.versoes || []).length} ${(t.versoes || []).length === 1 ? 'versão' : 'versões'}, ${(t.provas || []).length} ${(t.provas || []).length === 1 ? 'contestação' : 'contestações'})`} aberto><HistoriaCientifica t={t} /><a className="mt-4 inline-flex items-center gap-1 h-9 px-3 rounded-full border border-border text-sm font-medium hover:border-border-strong" href="#/linha-do-tempo">Evolução da pesquisa</a></Bloco>
        <Bloco titulo={`Anotações${anots.length ? ` (${anots.length})` : ''}`}>
          {anots.length ? <ul className="grid gap-2">{anots.map((a, i) => <li key={i} className={clsx('pl-3 border-l-[3px] rounded-r-md py-1', AVISO_RE.test(a) ? 'border-warn' : 'border-border')} style={AVISO_RE.test(a) ? { background: 'var(--warn-soft)' } : undefined}>{AVISO_RE.test(a) ? '⚠ ' : ''}{a}</li>)}</ul> : <p>Sem anotações adicionais no registro.</p>}
        </Bloco>
        <Bloco titulo={`Classe ${t.classe_evidencia} e como reproduzir`}>
          <p><b className="text-text font-medium">Classe {t.classe_evidencia}, {reg.classes[t.classe_evidencia]}:</b> {CLASSE_EXPL[t.classe_evidencia]}</p>
          <p className="mt-2 text-[13.5px]">Reproduzir: <code>{t.comando}</code> (<code>{t.script}</code>){t.saida ? <> → <code>{t.saida}</code></> : null}</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {met && <a className="inline-flex items-center gap-1 h-9 px-3 rounded-full border border-border text-sm font-medium hover:border-border-strong" href={`#/docs/metodologia?busca=${encodeURIComponent(met)}`}>Método completo (METODOLOGIA, seção {met})</a>}
            <a className="inline-flex items-center gap-1 h-9 px-3 rounded-full border border-border text-sm font-medium hover:border-border-strong" href={`${meta?.github || 'https://github.com/doce42/urna-lab'}/blob/main/${t.script}`} target="_blank" rel="noopener">Código no GitHub <ExternalLink size={13} /></a>
          </div>
        </Bloco>
      </div>
      <div className="mt-6 pt-5 border-t border-border flex justify-between gap-3">
        {ant ? <a href={`#/testes/${ant.id}`} className="text-sm font-medium text-muted hover:text-text">← {ant.id}</a> : <span />}
        {prox ? <a href={`#/testes/${prox.id}`} className="text-sm font-medium text-muted hover:text-text">{prox.id} →</a> : <span />}
      </div>
    </div>
  );
}
