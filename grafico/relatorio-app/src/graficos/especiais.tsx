// Gráficos específicos do estudo: fluxo entre turnos (sankey), cascata por região, bolhas por município, grade de Klimek.
import { useMemo, type ReactNode } from 'react';
import { sum, max, quantile, ascending } from 'd3-array';
import { scaleLinear, scaleSqrt } from 'd3-scale';
import { N, P, PP, votosMil, UF, REG, regiaoDe } from '@/lib/formato';
import { dica, esc } from '@/ui/Dica';
import { COR, Grafico, Tabela, useLargura } from './comum';
import type { Fluxo } from '@/lib/tipos';

// ---------- fluxo 1º → 2º turno ----------
export const rotFluxo = (n: string) => n === 'Adversário' ? 'Flávio Bolsonaro' : n === 'Abstenção' ? 'Não votou' : n;
export function Sankey({ f, V, titulo }: { f: Fluxo; V: number[][]; titulo?: ReactNode }) {
  const [ref, W] = useLargura<HTMLDivElement>();
  const L = f.linhas.map((l) => l.replace(' (1º)', '')), C = f.colunas;
  const estreito = W < 560;
  const H = estreito ? 520 : 480, m = { l: estreito ? 118 : 200, r: estreito ? 112 : 190, t: 6, b: 6 }, gap = 8;
  const totL = V.map((r) => sum(r)), totC = C.map((_, j) => sum(V, (r) => r[j])), total = sum(totL);
  const esc1 = (H - m.t - m.b - gap * (L.length - 1)) / total, escC = (H - m.t - m.b - gap * (C.length - 1)) / total;
  let y = m.t; const yL = totL.map((t) => { const a = y; y += t * esc1 + gap; return a; });
  y = m.t; const yC = totC.map((t) => { const a = y; y += t * escC + gap; return a; });
  const cor: Record<string, string> = { Lula: COR.lula, Adversário: COR.adv, 'Branco/nulo': COR.aviso, Abstenção: COR.neutro };
  const oL = yL.slice(), oC = yC.slice(), x0 = m.l, x1 = W - m.r, xm = (x0 + x1) / 2;
  const fx: { i: number; j: number; v: number; p: string }[] = [];
  V.forEach((r, i) => r.forEach((v, j) => { if (v <= 0) return; const a = v * esc1, c = v * escC;
    fx.push({ i, j, v, p: `M${x0},${oL[i]} C${xm},${oL[i]} ${xm},${oC[j]} ${x1},${oC[j]} L${x1},${oC[j] + c} C${xm},${oC[j] + c} ${xm},${oL[i] + a} ${x0},${oL[i] + a}Z` });
    oL[i] += a; oC[j] += c; }));
  const manteve = (fl: { i: number; j: number }) => L[fl.i] === C[fl.j];
  const afasta = (ys: number[]) => { const o = ys.slice(); for (let k = 1; k < o.length; k++) o[k] = Math.max(o[k], o[k - 1] + 15); return o; };
  const tL = afasta(L.map((_, i) => yL[i] + (totL[i] * esc1) / 2 + 4));
  const mi = (v: number) => P(v / 1e6, 1) + ' mi';
  return (
    <Grafico titulo={titulo} legenda={C.map((c) => ({ nome: rotFluxo(c) + ' no 2º turno', cor: cor[c] }))}
      tabela={<Tabela cab={['1º turno ↓ / 2º turno →', ...C.map(rotFluxo)]} linhas={L.map((l, i) => [rotFluxo(l), ...V[i].map((v) => N(v))])} />}>
      <div ref={ref} className="w-full">
        {W > 0 && (
          <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Fluxo de eleitores do 1º para o 2º turno">
            {fx.map((fl, k) => <path key={k} d={fl.p} fill={cor[C[fl.j]]} fillOpacity={manteve(fl) ? 0.14 : 0.58} {...dica(`<b>${esc(rotFluxo(L[fl.i]))} → ${esc(rotFluxo(C[fl.j]))}</b><br>${N(fl.v)} eleitores <span class="fr">(${P((100 * fl.v) / totL[fl.i])}% de quem estava em “${esc(rotFluxo(L[fl.i]))}”)</span>`)} />)}
            {L.map((l, i) => <g key={l}><rect x={x0 - 7} y={yL[i]} width={7} height={Math.max(1.5, totL[i] * esc1)} fill={COR.subtle} rx={1.5} />
              <text x={x0 - 12} y={tL[i]} textAnchor="end" className="rotulo-cat" fill={COR.texto} fontSize={estreito ? 11.5 : 12.5}>{rotFluxo(l)}{!estreito && <tspan fill={COR.subtle}> {mi(totL[i])}</tspan>}</text></g>)}
            {C.map((c, j) => <g key={c}><rect x={x1} y={yC[j]} width={7} height={totC[j] * escC} fill={cor[c]} rx={1.5} />
              <text x={x1 + 12} y={yC[j] + (totC[j] * escC) / 2 + 4} className="rotulo-cat" fill={COR.texto} fontSize={estreito ? 11.5 : 13} fontWeight={500}>{rotFluxo(c)}{!estreito ? <tspan fill={COR.subtle} fontWeight={400}> {mi(totC[j])}</tspan> : null}</text>
              {estreito && <text x={x1 + 12} y={yC[j] + (totC[j] * escC) / 2 + 18} className="rotulo-eixo">{mi(totC[j])}</text>}</g>)}
          </svg>
        )}
      </div>
      <p className="text-[13px] text-muted mt-2">Faixas fortes = mudaram de opção; faixas apagadas = mantiveram a mesma opção. Estimativa de grupos (inferência ecológica), não o voto de cada pessoa.</p>
    </Grafico>
  );
}

// ---------- cascata: como a diferença mudou por região ----------
export function Cascata({ passos, titulo, sub }: { passos: { r: string; base: number; d: number; total?: boolean }[]; titulo?: ReactNode; sub?: ReactNode }) {
  const [ref, W] = useLargura<HTMLDivElement>();
  const estreito = W < 520;
  const H = estreito ? 340 : 390, m = { l: 62, r: 12, t: 26, b: estreito ? 64 : 58 };
  const vals = passos.flatMap((p) => [p.base, p.base + p.d]);
  const y = scaleLinear().domain([Math.min(0, Math.min(...vals)) * 1.12, Math.max(...vals) * 1.12]).range([H - m.b, m.t]);
  const bw = (W - m.l - m.r) / passos.length, pad = bw * 0.26;
  return (
    <Grafico titulo={titulo} sub={sub} legenda={[{ nome: 'a favor de Lula', cor: COR.lula }, { nome: 'a favor de Flávio Bolsonaro', cor: COR.adv }]}
      tabela={<Tabela cab={['etapa', 'mudança na diferença (votos)']} linhas={passos.map((p) => [p.r, votosMil(p.d)])} />}>
      <div ref={ref} className="w-full">
        {W > 0 && (
          <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Cascata da diferença Lula − Flávio por região">
            {y.ticks(5).map((t) => <g key={t}><line x1={m.l} x2={W - m.r} y1={y(t)} y2={y(t)} className="grade-linha" /><text x={m.l - 8} y={y(t) + 4} textAnchor="end" className="rotulo-eixo">{t === 0 ? '0' : votosMil(t)}</text></g>)}
            <line x1={m.l} x2={W - m.r} y1={y(0)} y2={y(0)} className="eixo-zero" />
            {passos.map((p, i) => {
              const x = m.l + i * bw + pad / 2, w = bw - pad, y0 = y(p.base), y1 = y(p.base + p.d), top = Math.min(y0, y1), h = Math.max(1.5, Math.abs(y1 - y0));
              const corB = p.d >= 0 ? COR.lula : COR.adv;
              const rot = votosMil(Math.abs(p.d)).replace('+', '');
              const rotCompleto = p.total ? `${p.d >= 0 ? 'Lula' : 'Flávio'} ${rot} à frente` : votosMil(p.d);
              const abaixo = p.d < 0; // barra negativa: rótulo abaixo da base
              const rotX = p.r === 'Centro-Oeste' && bw < 110 ? 'C.-Oeste' : p.r;
              const inclinado = bw < 60;
              return (
                <g key={p.r} {...dica(`<b>${esc(p.r)}</b><br>${p.total ? 'diferença: ' : 'mudança na diferença: '}${esc(rotCompleto)}`)}>
                  <rect x={x} y={top} width={w} height={h} rx={3} fill={corB} fillOpacity={p.total ? 1 : 0.75} />
                  <text x={x + w / 2} y={abaixo ? top + h + 14 : top - 6} textAnchor="middle" className="rotulo-valor" fontSize={bw < 90 ? 10 : 11.5}>{p.total ? rot : votosMil(p.d)}</text>
                  {inclinado ? <text transform={`translate(${x + w / 2 + 4},${H - m.b + 10}) rotate(-35)`} textAnchor="end" className="rotulo-cat" fontSize={11}>{rotX}</text>
                    : <><text x={x + w / 2} y={H - m.b + 18} textAnchor="middle" className="rotulo-cat" fontSize={bw < 100 ? 11.5 : 12.5}>{rotX}</text>
                      {p.total && <text x={x + w / 2} y={H - m.b + 33} textAnchor="middle" className="rotulo-eixo">{p.d >= 0 ? 'Lula à frente' : 'Flávio à frente'}</text>}</>}
                  {i < passos.length - 1 && <line x1={x + w} x2={x + w + pad} y1={y(p.total ? p.d : p.base + p.d)} y2={y(p.total ? p.d : p.base + p.d)} stroke={COR.subtle} strokeDasharray="3 3" />}
                </g>
              );
            })}
            {W >= 760 && <text x={m.l} y={H - 8} className="rotulo-eixo">eixo: diferença Lula − Flávio Bolsonaro, em votos (acima de zero = Lula na frente)</text>}
          </svg>
        )}
      </div>
    </Grafico>
  );
}

// ---------- bolhas: municípios por região (quanto Lula cresceu) ----------
export type PontoMun = { nome: string; uf: string; lula1: number; lula2: number; virada: number; eleitores: number };
export function Bolhas({ pts, nac, titulo, sub }: { pts: PontoMun[]; nac: number; titulo?: ReactNode; sub?: ReactNode }) {
  const [ref, W] = useLargura<HTMLDivElement>();
  const estreito = W < 520;
  const regs = Object.keys(REG);
  const faixa = estreito ? 72 : 92, m = { l: estreito ? 8 : 110, r: 16, t: 30 + (estreito ? 16 : 0), b: 36 }, H = m.t + m.b + faixa * regs.length;
  const { x, r, jit, dentro } = useMemo(() => {
    const v = pts.map((p) => p.virada).sort(ascending);
    const lo = quantile(v, 0.002) ?? -10, hi = quantile(v, 0.998) ?? 20;
    const x = scaleLinear().domain([Math.min(lo, -2), hi]).clamp(true);
    const r = scaleSqrt().domain([0, max(pts, (p) => p.eleitores) || 1]).range([0, estreito ? 16 : 22]);
    // jitter determinístico
    let s = 7; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const jit = pts.map(() => { const u = rnd(), v2 = rnd(); return Math.max(-0.45, Math.min(0.45, 0.22 * Math.sqrt(-2 * Math.log(u + 1e-9)) * Math.cos(2 * Math.PI * v2))); });
    return { x, r, jit, dentro: pts.filter((p) => Math.abs(p.virada - nac) <= 5).length };
  }, [pts, nac, estreito]);
  x.range([m.l, W - m.r]);
  const ordem = useMemo(() => pts.map((p, i) => i).sort((a, b) => pts[b].eleitores - pts[a].eleitores), [pts]);
  return (
    <Grafico titulo={titulo} sub={sub ?? `${P((100 * dentro) / pts.length, 0)}% dos municípios ficaram a menos de 5 pontos da média do país (${PP(nac)}). Tamanho = eleitores.`}
      tabela={<Tabela cab={['região', 'municípios', 'mediana da virada (pp)']} linhas={regs.map((g) => { const q = pts.filter((p) => regiaoDe(p.uf) === g).map((p) => p.virada).sort(ascending); return [g, N(q.length), PP(quantile(q, 0.5) ?? 0)]; })} />}>
      <div ref={ref} className="w-full">
        {W > 0 && (
          <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Virada por município, por região">
            {x.ticks(estreito ? 5 : 8).map((t) => <g key={t}><line x1={x(t)} x2={x(t)} y1={m.t} y2={H - m.b} className="grade-linha" /><text x={x(t)} y={H - m.b + 16} textAnchor="middle" className="rotulo-eixo">{PP(t, 0).replace(' pp', '')}</text></g>)}
            <text x={(m.l + W - m.r) / 2} y={H - 4} textAnchor="middle" className="rotulo-eixo">quanto Lula cresceu no município (pontos percentuais) →</text>
            <line x1={x(nac)} x2={x(nac)} y1={m.t - 8} y2={H - m.b} stroke={COR.texto} strokeDasharray="4 4" />
            <text x={x(nac)} y={m.t - 12} textAnchor="middle" className="rotulo-eixo" fill={COR.texto}>média do país {PP(nac)}</text>
            {regs.map((g, k) => estreito
              ? <text key={g} x={m.l} y={m.t + k * faixa + 12} className="rotulo-cat" fontWeight={500} fill={COR.texto}>{g}</text>
              : <text key={g} x={m.l - 12} y={m.t + k * faixa + faixa / 2 + 4} textAnchor="end" className="rotulo-cat" fill={COR.texto} fontSize={13}>{g}</text>)}
            {ordem.map((i) => { const p = pts[i]; const k = regs.indexOf(regiaoDe(p.uf)); if (k < 0) return null; const cy = m.t + k * faixa + faixa / 2 + jit[i] * faixa * (estreito ? 0.8 : 1) + (estreito ? 6 : 0);
              return <circle key={i} cx={x(p.virada).toFixed(1)} cy={cy.toFixed(1)} r={Math.max(1.4, r(p.eleitores)).toFixed(1)} fill={COR.s2026} fillOpacity={0.42} stroke={COR.s2026} strokeOpacity={0.9} strokeWidth={0.5}
                {...dica(`<b>${esc(p.nome)} (${p.uf})</b><br>Lula ${P(p.lula1, 1)}% → ${P(p.lula2, 1)}%: ${PP(p.virada)}<br><span class="fr">${N(p.eleitores)} eleitores</span>`)} />; })}
          </svg>
        )}
      </div>
    </Grafico>
  );
}

// ---------- Klimek em bolhas: comparecimento × voto ----------
export function Klimek({ G, nomeC, titulo, cor = COR.s2026 }: { G: number[][]; nomeC: string; titulo?: ReactNode; cor?: string }) {
  const [ref, W] = useLargura<HTMLDivElement>();
  const n = G.length, H = Math.min(W, 460), m = { l: 44, r: 10, t: 10, b: 40 };
  const cel = (W - m.l - m.r) / n, celY = (H - m.t - m.b) / n;
  const r = scaleSqrt().domain([0, max(G.flat()) || 1]).range([0, Math.min(cel, celY) * 0.62]);
  const total = sum(G.flat());
  const canto = G[18][18] + G[18][19] + G[19][18] + G[19][19];
  return (
    <Grafico titulo={titulo} tabela={<Tabela cab={['faixa', 'seções na zona de alerta', 'total']} linhas={[['comparecimento e voto ≥ 90%', N(canto), N(total)]]} />}>
      <div ref={ref} className="w-full">
        {W > 0 && (
          <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`Seções por comparecimento e voto em ${nomeC}`}>
            {[0, 25, 50, 75, 100].map((t) => { const xx = m.l + (t / 100) * (W - m.l - m.r), yy = H - m.b - (t / 100) * (H - m.t - m.b);
              return <g key={t}><line x1={xx} x2={xx} y1={m.t} y2={H - m.b} className="grade-linha" /><text x={xx} y={H - m.b + 15} textAnchor="middle" className="rotulo-eixo">{t}%</text><line x1={m.l} x2={W - m.r} y1={yy} y2={yy} className="grade-linha" /><text x={m.l - 6} y={yy + 4} textAnchor="end" className="rotulo-eixo">{t}%</text></g>; })}
            <text x={(m.l + W - m.r) / 2} y={H - 6} textAnchor="middle" className="rotulo-eixo">% de votos em {nomeC} na seção →</text>
            <text transform={`translate(11,${(m.t + H - m.b) / 2}) rotate(-90)`} textAnchor="middle" className="rotulo-eixo">comparecimento →</text>
            <rect x={m.l + 18 * cel} y={H - m.b - 20 * celY} width={2 * cel} height={2 * celY} fill={COR.aviso} fillOpacity={0.1} stroke={COR.aviso} strokeDasharray="4 3" />
            {G.map((lin, i) => lin.map((q, j) => q ? <circle key={`${i}-${j}`} cx={m.l + (j + 0.5) * cel} cy={H - m.b - (i + 0.5) * celY} r={Math.max(1, r(q))} fill={cor} fillOpacity={0.72}
              {...dica(`<b>${N(q)} seções</b><br><span class="fr">comparecimento ${i * 5}–${i * 5 + 5}%<br>${esc(nomeC)}: ${j * 5}–${j * 5 + 5}% dos votos</span>`)} /> : null))}
          </svg>
        )}
      </div>
      <p className="text-[13px] text-muted mt-1.5">Na zona tracejada (comparecimento e voto acima de 90%): <b className="text-text font-medium">{N(canto)}</b> seções, {P((100 * canto) / total, 2)}% do total.</p>
    </Grafico>
  );
}

// ---------- barras por estado com ponto de referência (2022) ----------
export function BarrasUF({ linhas, titulo, sub, fmt, nomeRef = '2022', nomeBar = '2026' }: { linhas: { k: string; v: number; ref: number | null; dica: string }[]; titulo?: ReactNode; sub?: ReactNode; fmt: (v: number) => string; nomeRef?: string; nomeBar?: string }) {
  const [ref, W] = useLargura<HTMLDivElement>();
  const estreito = W < 520;
  const lin = 22, m = { l: estreito ? 44 : 150, r: 56, t: 22, b: 8 }, H = m.t + m.b + lin * linhas.length;
  const mx = Math.max(...linhas.map((l) => Math.max(l.v, l.ref || 0)), 0.1);
  const mn = Math.min(0, ...linhas.map((l) => Math.min(l.v, l.ref ?? 0)));
  const x = scaleLinear().domain([mn, mx * 1.05]).range([m.l, W - m.r]);
  return (
    <Grafico titulo={titulo} sub={sub} legenda={nomeRef ? [{ nome: nomeBar, cor: COR.s2026 }, { nome: nomeRef, cor: COR.ref, tipo: 'ponto' }] : []}
      tabela={<Tabela cab={['estado', nomeBar, ...(nomeRef ? [nomeRef] : [])]} linhas={linhas.map((l) => [UF[l.k] || l.k, fmt(l.v), ...(nomeRef ? [l.ref == null ? '—' : fmt(l.ref)] : [])])} />}>
      <div ref={ref} className="w-full">
        {W > 0 && (
          <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="img" aria-label={typeof titulo === 'string' ? titulo : 'barras por estado'}>
            {x.ticks(fmt(mx).length > 4 ? (estreito ? 2 : 3) : 5).map((t) => <g key={t}><line x1={x(t)} x2={x(t)} y1={m.t - 6} y2={H - m.b} className="grade-linha" /><text x={x(t)} y={m.t - 10} textAnchor="middle" className="rotulo-eixo">{fmt(t)}</text></g>)}
            {mn < 0 && <line x1={x(0)} x2={x(0)} y1={m.t - 6} y2={H - m.b} className="eixo-zero" />}
            {linhas.map((l, i) => { const y = m.t + i * lin; const x0 = x(Math.min(0, l.v)), x1 = x(Math.max(0, l.v));
              return (
                <g key={l.k} {...dica(l.dica)}>
                  <rect x={x0} y={y + 4} width={Math.max(1, x1 - x0)} height={lin - 8} rx={3} fill={COR.s2026} fillOpacity={0.9} />
                  <text x={m.l - 8} y={y + lin / 2 + 4} textAnchor="end" className="rotulo-cat" fill={COR.texto}>{estreito ? l.k : UF[l.k] || l.k}</text>
                  <text x={x1 + 6} y={y + lin / 2 + 4} className="rotulo-valor" fontSize={11}>{fmt(l.v)}</text>
                  {l.ref != null && <><circle cx={x(l.ref)} cy={y + lin / 2} r={6} fill={COR.surface} /><circle cx={x(l.ref)} cy={y + lin / 2} r={4} fill={COR.ref} /></>}
                  <rect x={0} y={y} width={W} height={lin} fill="transparent" />
                </g>
              ); })}
          </svg>
        )}
      </div>
    </Grafico>
  );
}
