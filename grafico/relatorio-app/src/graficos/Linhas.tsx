// Gráfico de linhas com mira (crosshair), dica e rótulo direto no fim de cada série.
import { useMemo, useRef, useState, type ReactNode } from 'react';
import { createPortal } from 'react-dom';
import { COR, Grafico, Tabela, useLargura, ticks, type ItemLegenda } from './comum';

export type SerieLinha = { nome: string; cor: string; valores: (number | null)[]; traco?: string; largura?: number; area?: boolean };
export function Linhas({ x, series, fmt, fmtX, zero, altura = 260, titulo, sub, rotulosFim = true, marcas = [], ariaRotulo, tabelaPasso = 1, rotulosX }: {
  x: (string | number)[]; series: SerieLinha[]; fmt: (v: number) => string; fmtX?: (v: string | number) => string; zero?: number; altura?: number;
  titulo?: ReactNode; sub?: ReactNode; rotulosFim?: boolean; marcas?: { i: number; rot: string }[]; ariaRotulo?: string; tabelaPasso?: number; rotulosX?: number[];
}) {
  const [ref, W] = useLargura<HTMLDivElement>();
  const [hover, setHover] = useState<{ i: number; px: number; py: number } | null>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  const H = altura, m = { l: 52, r: rotulosFim ? 64 : 16, t: 12, b: 28 };
  const fx = fmtX || ((v) => String(v));
  const { lo, hi } = useMemo(() => {
    const todos = series.flatMap((s) => s.valores).filter((v): v is number => v != null);
    let lo = Math.min(...todos), hi = Math.max(...todos);
    if (zero !== undefined) { lo = Math.min(lo, zero); hi = Math.max(hi, zero); }
    const pad = (hi - lo) * 0.06 || 1; if (!(zero !== undefined && lo === zero)) lo -= pad; hi += pad;
    return { lo, hi };
  }, [series, zero]);
  const n = x.length;
  const X = (i: number) => m.l + ((W - m.l - m.r) * i) / Math.max(1, n - 1);
  const Y = (v: number) => m.t + (H - m.t - m.b) * (1 - (v - lo) / (hi - lo));
  const caminhos = useMemo(() => series.map((s) => {
    let d = '', ab = false;
    s.valores.forEach((v, i) => { if (v == null) { ab = false; return; } d += `${ab ? 'L' : 'M'}${X(i).toFixed(1)},${Y(v).toFixed(1)}`; ab = true; });
    return d;
  }), [series, W, lo, hi]);
  const fins = useMemo(() => {
    const f = series.map((s) => { let i = s.valores.length - 1; while (i >= 0 && s.valores[i] == null) i--; return i >= 0 ? { i, v: s.valores[i] as number, s } : null; })
      .filter((v): v is { i: number; v: number; s: SerieLinha } => !!v).sort((a, b) => Y(a.v) - Y(b.v));
    let ultimo = -99; return f.map((q) => { const y = Y(q.v); const mostra = y - ultimo > 13; if (mostra) ultimo = y; return { ...q, mostra }; });
  }, [series, W, lo, hi]);
  const passoX = Math.max(1, Math.round(n / (W < 480 ? 4 : 7)));
  const mover = (e: React.PointerEvent<SVGSVGElement>) => {
    const r = svgRef.current!.getBoundingClientRect();
    const px = e.clientX - r.left;
    const i = Math.max(0, Math.min(n - 1, Math.round(((px - m.l) / (W - m.l - m.r)) * (n - 1))));
    setHover({ i, px: e.clientX, py: e.clientY });
  };
  const legenda: ItemLegenda[] = series.map((s) => ({ nome: s.nome, cor: s.cor, tipo: 'linha', traco: !!s.traco }));
  const linhasTabela = x.filter((_, i) => i % tabelaPasso === 0 || i === n - 1).map((xv) => { const i = x.indexOf(xv); return [fx(xv), ...series.map((s) => (s.valores[i] == null ? '—' : fmt(s.valores[i] as number)))]; });
  return (
    <Grafico titulo={titulo} sub={sub} legenda={legenda} tabela={<Tabela cab={['', ...series.map((s) => s.nome)]} linhas={linhasTabela} />}>
      <div ref={ref} className="w-full relative">
        {W > 0 && (
          <svg ref={svgRef} width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="img" aria-label={ariaRotulo || (typeof titulo === 'string' ? titulo : 'gráfico de linhas')}
            onPointerMove={mover} onPointerLeave={() => setHover(null)} style={{ touchAction: 'pan-y' }}>
            {ticks(lo, hi, 4).map((v) => <g key={v}><line x1={m.l} x2={W - m.r} y1={Y(v)} y2={Y(v)} className="grade-linha" /><text x={m.l - 8} y={Y(v) + 4} textAnchor="end" className="rotulo-eixo">{fmt(v)}</text></g>)}
            {(rotulosX ? rotulosX.filter((_, k) => W >= 480 || k % 2 === 0) : x.map((_, i) => i).filter((i) => i % passoX === 0 && i < n - passoX / 2)).map((i) => <text key={i} x={X(i)} y={H - 8} textAnchor={i === 0 ? 'start' : 'middle'} className="rotulo-eixo">{fx(x[i])}</text>)}
            {zero !== undefined && <line x1={m.l} x2={W - m.r} y1={Y(zero)} y2={Y(zero)} className="eixo-zero" />}
            {marcas.map((mk, k) => <g key={k}><line x1={X(mk.i)} x2={X(mk.i)} y1={m.t} y2={H - m.b} stroke={COR.subtle} strokeDasharray="3 3" /><text x={X(mk.i) + 4} y={m.t + 10} className="rotulo-eixo">{mk.rot}</text></g>)}
            {series.map((s, k) => s.area && caminhos[k] ? <path key={'a' + k} d={`${caminhos[k]}L${X(s.valores.length - 1)},${Y(zero ?? lo)}L${X(0)},${Y(zero ?? lo)}Z`} fill={s.cor} opacity=".08" /> : null)}
            {series.map((s, k) => <path key={k} d={caminhos[k]} fill="none" stroke={s.cor} strokeWidth={s.largura || 2} strokeDasharray={s.traco} strokeLinejoin="round" strokeLinecap="round" />)}
            {fins.map((f, k) => (
              <g key={k}>
                <circle cx={X(f.i)} cy={Y(f.v)} r={6} fill={COR.surface} /><circle cx={X(f.i)} cy={Y(f.v)} r={4} fill={f.s.cor} />
                {rotulosFim && f.mostra && <text x={X(f.i) + 9} y={Y(f.v) + 4} className="rotulo-valor">{fmt(f.v)}</text>}
              </g>
            ))}
            {hover && (
              <g>
                <line x1={X(hover.i)} x2={X(hover.i)} y1={m.t} y2={H - m.b} stroke={COR.subtle} />
                {series.map((s, k) => s.valores[hover.i] == null ? null : <g key={k}><circle cx={X(hover.i)} cy={Y(s.valores[hover.i] as number)} r={6} fill={COR.surface} /><circle cx={X(hover.i)} cy={Y(s.valores[hover.i] as number)} r={4} fill={s.cor} /></g>)}
              </g>
            )}
            <rect x={m.l} y={m.t} width={Math.max(0, W - m.l - m.r)} height={H - m.t - m.b} fill="transparent" />
          </svg>
        )}
        {hover && createPortal(
          <div className="dica" style={{ left: Math.min(hover.px + 14, innerWidth - 300), top: hover.py + 14 }}>
            <b>{fx(x[hover.i])}</b>
            {series.map((s) => <div key={s.nome}><i className="inline-block w-3 h-[3px] rounded mr-1.5 align-middle" style={{ background: s.cor }} /><b>{s.valores[hover.i] == null ? '—' : fmt(s.valores[hover.i] as number)}</b> <span className="fr">{s.nome}</span></div>)}
          </div>, document.body)}
      </div>
    </Grafico>
  );
}
