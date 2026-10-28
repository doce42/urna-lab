// Gráficos pequenos e reutilizáveis: barras, pontos com intervalo, histograma, medidores, figuras, igualdade, dumbbell, faixa, quadrados.
import type { ReactNode } from 'react';
import { clsx } from 'clsx';
import { N, P, nice } from '@/lib/formato';
import { dica, esc } from '@/ui/Dica';
import { COR, Grafico, Tabela, useLargura, ticks, type ItemLegenda } from './comum';

// ---------- barras horizontais ----------
export type Barra = { nome?: string; cor: string; v: number | null; txt: string; dica?: string };
export type LinhaBarras = { l: string; bars: Barra[] };
export function Barras({ linhas, titulo, sub, max, refs = [], nota }: { linhas: LinhaBarras[]; titulo?: ReactNode; sub?: ReactNode; max?: number; refs?: { v: number; rot: string }[]; nota?: ReactNode }) {
  const nomes: ItemLegenda[] = [];
  linhas.forEach((r) => r.bars.forEach((b) => { if (b.nome && !nomes.find((x) => x.nome === b.nome)) nomes.push({ nome: b.nome, cor: b.cor }); }));
  const vals = linhas.flatMap((r) => r.bars.map((b) => b.v ?? 0)).concat(refs.map((r) => r.v)).filter((v) => isFinite(v));
  const mx = max || nice(Math.max(...vals, 1e-9) * 1.02);
  return (
    <Grafico titulo={titulo} sub={sub} legenda={nomes} tabela={<Tabela cab={['', ...(nomes.length ? nomes.map((n) => n.nome) : ['valor'])]} linhas={linhas.map((r) => [r.l, ...(nomes.length ? nomes.map((n) => r.bars.find((b) => b.nome === n.nome)?.txt ?? '—') : r.bars.map((b) => b.txt))])} />}>
      <div className="relative" style={{ paddingTop: refs.length ? 18 : 0 }}>
        {refs.map((r) => (
          <div key={r.rot} className="absolute top-0 bottom-0 border-l border-dashed border-subtle pointer-events-none z-[1]" style={{ left: `calc(34% + 10px + (100% - 34% - 10px - 72px) * ${Math.min(1, r.v / mx)})` }}>
            <span className="absolute -top-0.5 left-1 text-[11px] text-muted whitespace-nowrap bg-surface px-1 rounded">{r.rot}</span>
          </div>
        ))}
        {linhas.map((r, i) => (
          <div key={i} className="grid items-center gap-x-2.5 my-2" style={{ gridTemplateColumns: 'minmax(96px, 34%) 1fr' }}>
            <div className="text-[13px] text-muted leading-tight" dangerouslySetInnerHTML={{ __html: r.l }} />
            <div className="min-w-0 pr-[72px] relative">
              {r.bars.map((b, j) => {
                const f = Math.max(0, Math.min(1, (b.v ?? 0) / mx));
                return (
                  <div key={j} className="relative h-[18px] my-[3px] rounded-r-md bg-surface-2" {...dica(b.dica || `<b>${esc(b.txt)}</b>${b.nome ? '<br>' + esc(b.nome) : ''}<br><span class="fr">${esc(r.l.replace(/<[^>]+>/g, ''))}</span>`)}>
                    <div className="h-full rounded-r-md transition-[width] duration-500 ease-out" style={{ width: `${(f * 100).toFixed(2)}%`, background: b.cor }} />
                    <span className="absolute top-0 ml-2 font-mono text-[12px] font-medium text-text whitespace-nowrap leading-[18px]" style={{ left: `${(f * 100).toFixed(2)}%` }}>{b.txt}</span>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
      {nota && <p className="text-[13px] text-muted mt-1">{nota}</p>}
    </Grafico>
  );
}

// ---------- pontos com intervalos ----------
export type SeriePonto = { nome?: string; cor: string; v?: number | null; lo?: number | null; hi?: number | null; rot?: string; dica?: string };
export type LinhaPontos = { l: string; s: SeriePonto[] };
export function Pontos({ linhas, min, max, refs = [], faixa, zonas = [], fmt, titulo, sub }: { linhas: LinhaPontos[]; min: number; max: number; refs?: { v: number; rot?: string; solido?: boolean }[]; faixa?: [number, number, string] | null; zonas?: [number, number, string][]; fmt: (v: number) => string; titulo?: ReactNode; sub?: ReactNode }) {
  const [ref, W] = useLargura<HTMLDivElement>();
  const estreito = W < 480;
  const mr = 16, rh = 26, top = 14, nS = Math.max(...linhas.map((l) => l.s.length));
  const ml = estreito ? 8 : Math.min(220, 16 + Math.max(...linhas.map((l) => l.l.replace(/<[^>]+>/g, '').length)) * 7);
  const bh = nS * rh + 8 + (estreito ? 18 : 0), H = top + linhas.length * bh + 32;
  const X = (v: number) => ml + (W - ml - mr) * ((v - min) / (max - min));
  const cl = (v: number) => Math.max(min, Math.min(max, v));
  const nomes: ItemLegenda[] = [];
  linhas.forEach((l) => l.s.forEach((s) => { if (s.nome && !nomes.find((x) => x.nome === s.nome)) nomes.push({ nome: s.nome, cor: s.cor, tipo: 'ponto' }); }));
  return (
    <Grafico titulo={titulo} sub={sub} legenda={nomes} tabela={<Tabela cab={['', 'valor', 'intervalo']} linhas={linhas.flatMap((l) => l.s.map((s) => [l.l.replace(/<[^>]+>/g, '') + (s.nome ? ` · ${s.nome}` : ''), s.v != null ? fmt(s.v) : '—', s.lo != null ? `${fmt(s.lo)} a ${fmt(s.hi!)}` : '—']))} />}>
      <div ref={ref} className="w-full">
        {W > 0 && (
          <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="img" aria-label={typeof titulo === 'string' ? titulo : 'gráfico de pontos'}>
            {zonas.map((z, i) => <g key={i}><rect x={X(cl(z[0]))} y={top - 6} width={X(cl(z[1])) - X(cl(z[0]))} height={H - top - 24} fill={COR.aviso} opacity=".12" /><text x={X(cl(z[0])) + 4} y={top + 4} className="rotulo-eixo">{z[2]}</text></g>)}
            {faixa && <g><rect x={X(cl(faixa[0]))} y={top - 6} width={X(cl(faixa[1])) - X(cl(faixa[0]))} height={H - top - 24} fill={COR.s2026} opacity=".1" /><text x={X(cl(faixa[1])) - 4} y={top + 4} textAnchor="end" className="rotulo-eixo">{faixa[2]}</text></g>}
            {ticks(min, max, 4).map((v) => <g key={v}><line x1={X(v)} x2={X(v)} y1={top - 6} y2={H - 26} className="grade-linha" /><text x={X(v)} y={H - 10} textAnchor="middle" className="rotulo-eixo">{fmt(v)}</text></g>)}
            {refs.map((r, i) => <g key={i}><line x1={X(r.v)} x2={X(r.v)} y1={top - 6} y2={H - 26} stroke={COR.subtle} strokeDasharray={r.solido ? undefined : '4 3'} />{r.rot && <text x={X(r.v) + 4} y={H - 28} className="rotulo-eixo">{r.rot}</text>}</g>)}
            {linhas.map((l, i) => {
              const y0 = top + i * bh;
              return (
                <g key={i}>
                  {i > 0 && <line x1={ml - 6} x2={W - mr} y1={y0 - 4} y2={y0 - 4} className="grade-linha" />}
                  {estreito ? <text x={ml} y={y0 + 10} className="rotulo-cat" fontWeight={500}>{l.l.replace(/<[^>]+>/g, '')}</text>
                    : <text x={ml - 10} y={y0 + bh / 2 + 2} textAnchor="end" className="rotulo-cat">{l.l.replace(/<[^>]+>/g, '')}</text>}
                  {l.s.map((s, j) => {
                    const y = y0 + 4 + j * rh + 8 + (estreito ? 18 : 0);
                    return (
                      <g key={j}>
                        {s.lo != null && s.hi != null && <line x1={X(cl(s.lo))} x2={X(cl(s.hi))} y1={y} y2={y} stroke={s.cor} strokeWidth={s.v == null ? 8 : 2.5} strokeLinecap="round" opacity={s.v == null ? 0.85 : 1} />}
                        {s.v != null && <><circle cx={X(cl(s.v))} cy={y} r={7} fill={COR.surface} /><circle cx={X(cl(s.v))} cy={y} r={5} fill={s.cor} /></>}
                        {s.rot && <text x={X(cl(s.v ?? s.hi ?? 0)) + 10} y={y + 4} className="rotulo-valor">{s.rot}</text>}
                        <rect x={ml} y={y - 13} width={W - ml - mr} height={26} fill="transparent" {...dica(s.dica || `<b>${s.v != null ? fmt(s.v) : ''}${s.lo != null ? ` [${fmt(s.lo)}; ${fmt(s.hi!)}]` : ''}</b><br><span class="fr">${esc(l.l.replace(/<[^>]+>/g, ''))}${s.nome ? ' · ' + esc(s.nome) : ''}</span>`)} />
                      </g>
                    );
                  })}
                </g>
              );
            })}
          </svg>
        )}
      </div>
    </Grafico>
  );
}

// ---------- histograma (raiz quadrada) ----------
export function Histograma({ z, titulo }: { z: { bordas: number[]; contagem: number[]; n: number; acima5_lula?: number; acima5_flavio?: number }; titulo?: ReactNode }) {
  const [ref, W] = useLargura<HTMLDivElement>();
  const H = 250, m = { l: 48, r: 8, t: 16, b: 44 }, v = z.contagem, n = v.length;
  const hi = Math.max(...v), bw = (W - m.l - m.r) / n;
  const Y = (q: number) => m.t + (H - m.t - m.b) * (1 - Math.sqrt(q / hi));
  const tk = [0, 10, 100, 1000, 10000, 100000, 1000000].filter((t) => t <= hi);
  const cauda = (i: number) => Math.abs(z.bordas[i]) >= 5 || Math.abs(z.bordas[i + 1]) > 5;
  const rot = z.bordas.slice(0, -1).map((b) => P(b, 1));
  return (
    <Grafico titulo={titulo} legenda={[{ nome: 'dentro de 5 desvios', cor: COR.s2026 }, { nome: 'caudas, além de 5 desvios', cor: COR.aviso }]}
      tabela={<Tabela cab={['faixa (desvios)', 'seções']} linhas={v.map((q, i) => [`${rot[i]} a ${P(z.bordas[i + 1], 1)}`, N(q)])} />}>
      <div ref={ref} className="w-full">
        {W > 0 && (
          <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Histograma das seções por distância do padrão do município">
            {tk.map((q) => <g key={q}><line x1={m.l} x2={W - m.r} y1={Y(q)} y2={Y(q)} className="grade-linha" /><text x={m.l - 6} y={Y(q) + 4} textAnchor="end" className="rotulo-eixo">{q >= 1e6 ? '1 mi' : q >= 1e3 ? `${q / 1e3} mil` : q}</text></g>)}
            {v.map((q, i) => (
              <g key={i}>
                <rect x={m.l + i * bw + 1} y={Y(q)} width={Math.max(1, bw - 2)} height={Math.max(0, H - m.b - Y(q))} rx={2} fill={cauda(i) ? COR.aviso : COR.s2026}
                  {...dica(`<b>${N(q)}</b> seções<br><span class="fr">faixa ${rot[i]} a ${P(z.bordas[i + 1], 1)} desvios</span>`)} />
                {i % (W < 480 ? 8 : 4) === 0 && <text x={m.l + i * bw + bw / 2} y={H - 26} textAnchor="middle" className="rotulo-eixo">{rot[i]}</text>}
              </g>
            ))}
            {[-5, 5].map((b) => { const i = z.bordas.findIndex((x) => x >= b); if (i < 0) return null; const x = m.l + i * bw;
              return <g key={b}><line x1={x} x2={x} y1={m.t} y2={H - m.b} stroke={COR.aviso} strokeDasharray="4 3" /><text x={x + (b > 0 ? 4 : -4)} y={m.t + 10} textAnchor={b > 0 ? 'start' : 'end'} className="rotulo-eixo" fill={COR.muted}>{b > 0 ? '+' : ''}{b} desvios</text></g>; })}
            <text x={m.l + (W - m.l - m.r) / 2} y={H - 8} textAnchor="middle" className="rotulo-eixo">distância do padrão do município (0 = igual às vizinhas) · altura em raiz quadrada</text>
          </svg>
        )}
      </div>
    </Grafico>
  );
}

// ---------- medidores de cobertura (frações perto de 100%) ----------
export type Cobertura = { l: string; ok: number; tot: number; nome?: string; cor: string };
export function Coberturas({ itens, titulo }: { itens: Cobertura[]; titulo?: ReactNode }) {
  return (
    <Grafico titulo={titulo} tabela={<Tabela cab={['conferência', 'ok', 'de', '%']} linhas={itens.map((i) => [i.l + (i.nome ? ` (${i.nome})` : ''), N(i.ok), N(i.tot), P(100 * (i.tot ? i.ok / i.tot : 0), 3)])} />}>
      <div className="grid gap-1">
        {itens.map((i, k) => {
          const f = i.tot ? i.ok / i.tot : 0, falta = i.tot - i.ok, cheio = falta === 0;
          return (
            <div key={k} className="grid gap-x-3 gap-y-1 items-center py-2.5 border-t border-grade first:border-t-0" style={{ gridTemplateColumns: 'minmax(120px, 1.2fr) auto 2fr' }}
              {...dica(`<b>${N(i.ok)} de ${N(i.tot)}</b> (${P(100 * f, f === 1 ? 0 : 4)}%)${i.nome ? '<br>' + esc(i.nome) : ''}${falta ? `<br>faltam ${N(falta)}` : '<br>todas'}`)}>
              <div className="text-[13.5px] text-muted leading-snug">{i.l}{i.nome && <span className="block text-xs text-subtle mt-0.5"><i className="inline-block w-2.5 h-2.5 rounded-sm mr-1.5 align-middle" style={{ background: i.cor }} />{i.nome}</span>}</div>
              <div className={clsx('text-[22px] font-semibold tracking-tight leading-none whitespace-nowrap', cheio ? 'text-ok' : 'text-warn')}>{P(100 * f, f === 1 ? 0 : f > 0.999 ? 3 : 2)}%</div>
              <div className="min-w-0 max-sm:col-span-2">
                <div className="medidor"><i style={{ width: `${(100 * f).toFixed(3)}%`, background: i.cor }} /></div>
                <div className="text-xs text-subtle mt-1 t-num">{N(i.ok)} de {N(i.tot)}{falta ? <b className="text-muted font-medium"> · faltam {N(falta)}</b> : <b className="text-ok font-medium"> · todas ✓</b>}</div>
              </div>
            </div>
          );
        })}
      </div>
    </Grafico>
  );
}

// ---------- figuras (stat tiles) ----------
export type Figura = { n: string; r: string; estado?: 'ok' | 'aviso' | 'ruim'; dica?: string };
export function Figuras({ itens, titulo }: { itens: Figura[]; titulo?: ReactNode }) {
  return (
    <Grafico titulo={titulo}>
      <div className="grid gap-2" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))' }}>
        {itens.map((i, k) => (
          <div key={k} className="rounded-lg border border-border bg-surface-2 px-3.5 py-3 border-t-[3px]" style={{ borderTopColor: i.estado === 'ok' ? 'var(--ok)' : i.estado === 'aviso' ? 'var(--warn)' : i.estado === 'ruim' ? 'var(--erro)' : 'var(--border-strong)' }} {...(i.dica ? dica(i.dica) : {})}>
            <div className="text-[22px] font-semibold tracking-tight leading-tight">{i.n}{i.estado === 'ok' && <span className="text-ok text-base ml-1">✓</span>}{i.estado === 'ruim' && <span className="text-erro text-base ml-1">!</span>}</div>
            <div className="text-xs text-muted mt-1 leading-snug">{i.r}</div>
          </div>
        ))}
      </div>
    </Grafico>
  );
}

// ---------- igualdade (dois totais lado a lado) ----------
export function Igualdade({ a, ta, b, tb, iguais, titulo }: { a: string; ta: string; b: string; tb: string; iguais: boolean; titulo?: ReactNode }) {
  const lado = (n: string, r: string) => <div className="rounded-lg border border-border bg-surface-2 px-4 py-3.5 text-center"><div className="text-[22px] font-semibold tracking-tight leading-tight">{n}</div><div className="text-xs text-muted mt-1">{r}</div></div>;
  return (
    <Grafico titulo={titulo}>
      <div className="grid items-center gap-2.5 max-sm:grid-cols-1 sm:grid-cols-[1fr_auto_1fr]">
        {lado(a, ta)}
        <div className={clsx('w-10 h-10 rounded-full grid place-items-center text-xl font-semibold mx-auto', iguais ? 'bg-ok-soft text-ok' : 'bg-erro-soft text-erro')} style={{ background: iguais ? 'var(--ok-soft)' : 'var(--erro-soft)' }}>{iguais ? '=' : '≠'}</div>
        {lado(b, tb)}
      </div>
    </Grafico>
  );
}

// ---------- dumbbell: esperado → observado ----------
export type LinhaDumb = { l: string; a: number; b: number; z: number; dica: string };
export function Dumbbell({ linhas, titulo, fmt, na, nb }: { linhas: LinhaDumb[]; titulo?: ReactNode; fmt: (v: number) => string; na: string; nb: string }) {
  const [ref, W] = useLargura<HTMLDivElement>();
  const estreito = W < 520;
  const ml = estreito ? 8 : 200, mr = 60, rh = estreito ? 40 : 26, top = 12, H = top + linhas.length * rh + 30;
  const vals = linhas.flatMap((r) => [r.a, r.b]);
  let min = Math.min(...vals, 0), max = Math.max(...vals, 0); const pad = (max - min) * 0.08 || 1; min -= pad; max += pad;
  const X = (v: number) => ml + (W - ml - mr) * ((v - min) / (max - min));
  return (
    <Grafico titulo={titulo} legenda={[{ nome: na, cor: COR.ref, tipo: 'ponto' }, { nome: nb, cor: COR.s2026, tipo: 'ponto' }]}
      tabela={<Tabela cab={['grupo', na, nb, 'z']} linhas={linhas.map((r) => [r.l, fmt(r.a), fmt(r.b), P(r.z, 1)])} />}>
      <div ref={ref} className="w-full">
        {W > 0 && (
          <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="img" aria-label={typeof titulo === 'string' ? titulo : 'esperado e observado'}>
            {ticks(min, max, 4).map((v) => <g key={v}><line x1={X(v)} x2={X(v)} y1={top - 4} y2={H - 26} className="grade-linha" /><text x={X(v)} y={H - 10} textAnchor="middle" className="rotulo-eixo">{fmt(v)}</text></g>)}
            {min < 0 && max > 0 && <line x1={X(0)} x2={X(0)} y1={top - 4} y2={H - 26} className="eixo-zero" />}
            {linhas.map((r, i) => { const y = top + i * rh + (estreito ? rh - 10 : rh / 2); const rot = r.l.length > 30 ? r.l.slice(0, 29) + '…' : r.l;
              return (
                <g key={i}>
                  {estreito ? <text x={ml} y={top + i * rh + 12} className="rotulo-cat">{rot}</text> : <text x={ml - 10} y={y + 4} textAnchor="end" className="rotulo-cat">{rot}</text>}
                  <line x1={X(r.a)} x2={X(r.b)} y1={y} y2={y} stroke={COR.subtle} strokeWidth={2} opacity=".6" />
                  <circle cx={X(r.a)} cy={y} r={5} fill={COR.ref} /><circle cx={X(r.b)} cy={y} r={7} fill={COR.surface} /><circle cx={X(r.b)} cy={y} r={5} fill={COR.s2026} />
                  <text x={W - mr + 8} y={y + 4} className="rotulo-valor">z {P(r.z, 1)}</text>
                  <rect x={0} y={y - 13} width={W} height={26} fill="transparent" {...dica(r.dica)} />
                </g>
              ); })}
          </svg>
        )}
      </div>
    </Grafico>
  );
}

// ---------- faixa de percentis ----------
export function FaixaPontos({ itens, min, max, fmt, titulo, refs = [] }: { itens: { rot: string; v: number }[]; min: number; max: number; fmt: (v: number) => string; titulo?: ReactNode; refs?: { v: number }[] }) {
  const [ref, W] = useLargura<HTMLDivElement>();
  const ml = 16, mr = 16, H = 90, y = 52;
  const X = (v: number) => ml + (W - ml - mr) * ((v - min) / (max - min));
  return (
    <Grafico titulo={titulo} tabela={<Tabela cab={['percentil', 'valor']} linhas={itens.map((i) => [i.rot, fmt(i.v)])} />}>
      <div ref={ref} className="w-full">
        {W > 0 && (
          <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="img" aria-label={typeof titulo === 'string' ? titulo : 'faixa de percentis'}>
            {ticks(min, max, 4).map((v) => <g key={v}><line x1={X(v)} x2={X(v)} y1={y - 14} y2={y + 14} className="grade-linha" /><text x={X(v)} y={H - 6} textAnchor="middle" className="rotulo-eixo">{fmt(v)}</text></g>)}
            {refs.map((r, i) => <line key={i} x1={X(r.v)} x2={X(r.v)} y1={y - 22} y2={y + 18} stroke={COR.subtle} strokeDasharray="4 3" />)}
            <line x1={ml} x2={W - mr} y1={y} y2={y} className="grade-linha" />
            {itens.map((it, i) => { const x = X(Math.max(min, Math.min(max, it.v))), cima = i % 2 === 0;
              return <g key={i}><circle cx={x} cy={y} r={7} fill={COR.surface} /><circle cx={x} cy={y} r={5} fill={COR.s2026} {...dica(`<b>${fmt(it.v)}</b><br><span class="fr">percentil ${esc(it.rot)}</span>`)} /><text x={x} y={cima ? y - 14 : y + 26} textAnchor="middle" className="rotulo-eixo">{it.rot}</text></g>; })}
          </svg>
        )}
      </div>
    </Grafico>
  );
}

// ---------- quadrados: cenários detectados ou não ----------
export function Quadrados({ grupos, titulo, nota }: { grupos: { nome: string; itens: { on: boolean; dica: string }[] }[]; titulo?: ReactNode; nota?: ReactNode }) {
  return (
    <Grafico titulo={titulo} legenda={[{ nome: 'detectada', cor: COR.s2026 }, { nome: 'passou batido', cor: COR.neutro }]}
      tabela={<Tabela cab={['grupo', 'cenários', 'detectados']} linhas={grupos.map((g) => [g.nome, g.itens.length, g.itens.filter((i) => i.on).length])} />}>
      {grupos.map((g) => (
        <div key={g.nome} className="mt-2.5">
          <div className="text-xs font-mono uppercase tracking-wider text-muted mb-1">{g.nome} <span className="text-subtle normal-case tracking-normal font-sans">· {g.itens.filter((i) => i.on).length} de {g.itens.length} detectados</span></div>
          <div className="flex flex-wrap gap-1">
            {g.itens.map((it, i) => <span key={i} tabIndex={0} className="w-5 h-5 rounded-[5px] outline-offset-1" style={{ background: it.on ? COR.s2026 : COR.neutro }} {...dica(it.dica)} />)}
          </div>
        </div>
      ))}
      {nota && <p className="text-[13px] text-muted mt-3">{nota}</p>}
    </Grafico>
  );
}

// ---------- dupla: hipótese nula → observado ----------
export function Dupla({ a, ta, b, tb }: { a: string; ta: string; b: string; tb: string }) {
  return (
    <div className="flex flex-wrap items-stretch gap-2">
      <div className="flex-1 min-w-[160px] rounded-lg border border-border bg-surface-2 px-3 py-2.5 text-[13px] text-muted"><b className="block text-text text-[11px] uppercase tracking-wider mb-0.5 font-mono">{a}</b>{ta}</div>
      <div className="self-center text-xl text-subtle" aria-hidden="true">→</div>
      <div className="flex-1 min-w-[160px] rounded-lg border border-border bg-surface-2 px-3 py-2.5 text-[13px] text-muted"><b className="block text-text text-[11px] uppercase tracking-wider mb-0.5 font-mono">{b}</b>{tb}</div>
    </div>
  );
}
export function Processando({ msg, sub }: { msg: string; sub?: string }) {
  return (
    <div className="rounded-lg border border-dashed border-warn/70 px-4 py-5 text-center my-1" style={{ background: 'repeating-linear-gradient(135deg, transparent 0 10px, var(--warn-soft) 10px 20px)' }}>
      <div className="font-medium text-warn">{msg}</div>
      {sub && <div className="text-[13px] text-muted mt-1">{sub}</div>}
    </div>
  );
}
