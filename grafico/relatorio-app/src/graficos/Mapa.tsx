// Mapa coroplético dos municípios (malha IBGE simplificada no build), com contorno dos estados e escala divergente neutra.
import { useMemo, useState, type ReactNode } from 'react';
import { createPortal } from 'react-dom';
import { geoMercator, geoPath, geoTransform } from 'd3-geo';
import { feature, mesh } from 'topojson-client';
import { scaleLinear } from 'd3-scale';
import { quantile, ascending } from 'd3-array';
import type { Topology, GeometryCollection } from 'topojson-specification';
import type { FeatureCollection, Geometry } from 'geojson';
import { N, P, PP } from '@/lib/formato';
import { Grafico, COR, Tabela } from './comum';
import { esc } from '@/ui/Dica';

export type MedidaMapa = 'lula2' | 'virada';
type Info = { lula1: number; lula2: number; virada: number; eleitores: number } | null;
const W = 720, H = 700;

export function Mapa({ topo, valor, nome, medida, titulo, uf }: { topo: Topology; valor: (cod: number) => number | null; nome: (cod: number) => string; medida: MedidaMapa; titulo?: ReactNode; uf?: (cod: number) => Info }) {
  const [hover, setHover] = useState<{ cod: number; x: number; y: number } | null>(null);
  const { caminhos, bordas } = useMemo(() => {
    const mun = feature(topo, topo.objects.municipios as GeometryCollection) as unknown as FeatureCollection<Geometry>;
    const ufs = feature(topo, topo.objects.ufs as GeometryCollection) as unknown as FeatureCollection<Geometry>;
    // projeção planar (sem recorte esférico): anéis que a simplificação deixou invertidos não viram "o globo inteiro"
    const merc = geoMercator().fitSize([W, H], ufs);
    const plano = geoTransform({ point(x, y) { const p = merc([x, y]); if (p) this.stream.point(p[0], p[1]); } });
    const path = geoPath(plano);
    const caminhos = mun.features.map((f) => ({ cod: +(f.id as number), d: path(f) || '' }));
    const bordas = path(mesh(topo, topo.objects.ufs as GeometryCollection)) || '';
    return { caminhos, bordas };
  }, [topo]);
  const meio = medida === 'lula2' ? 50 : 0;
  const tema = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-theme') : null;
  const { cores, lim } = useMemo(() => {
    const vals = caminhos.map((c) => valor(c.cod)).filter((v): v is number => v != null);
    const lim = quantile(vals.map((v) => Math.abs(v - meio)).sort(ascending), 0.98) || 1;
    const cs = getComputedStyle(document.documentElement);
    const lula = cs.getPropertyValue('--s-lula').trim() || '#1F8A70', adv = cs.getPropertyValue('--s-adv').trim() || '#7A5CC7', neu = cs.getPropertyValue('--s-neutro').trim() || '#B9BDC4';
    return { lim, cores: scaleLinear<string>().domain([meio - lim, meio, meio + lim]).range([adv, neu, lula]).clamp(true) };
  }, [caminhos, valor, meio, tema]);
  const fmt = (v: number) => (medida === 'lula2' ? P(v, 0) + '%' : PP(v, 0));
  const info = hover ? uf?.(hover.cod) : null;
  return (
    <Grafico titulo={titulo} tabela={<Tabela cab={['escala', 'cor']} linhas={[[fmt(meio - lim), 'a favor de Flávio Bolsonaro (violeta)'], [fmt(meio), 'equilíbrio (cinza)'], [fmt(meio + lim), 'a favor de Lula (verde-azulado)']]} />}>
      <div className="relative">
        <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto" role="img" aria-label="Mapa dos municípios" onPointerLeave={() => setHover(null)}>
          <g>{caminhos.map((c) => { const v = valor(c.cod); return <path key={c.cod} d={c.d} fill={v == null ? 'var(--surface-2)' : cores(v)} onPointerMove={(e) => setHover({ cod: c.cod, x: e.clientX, y: e.clientY })} />; })}</g>
          <path d={bordas} fill="none" stroke="var(--bg)" strokeWidth={1.1} pointerEvents="none" />
          {hover && <path d={caminhos.find((c) => c.cod === hover.cod)?.d} fill="none" stroke="var(--text)" strokeWidth={1.4} pointerEvents="none" />}
        </svg>
        {hover && createPortal(
          <div className="dica" style={{ left: Math.min(hover.x + 14, innerWidth - 280), top: hover.y + 14 }}
            dangerouslySetInnerHTML={{ __html: `<b>${esc(nome(hover.cod))}</b>${info ? `<br>Lula ${P(info.lula1, 1)}% → ${P(info.lula2, 1)}% (${PP(info.virada)})<br><span class="fr">${N(info.eleitores)} eleitores</span>` : '<br><span class="fr">sem dado</span>'}` }} />, document.body)}
      </div>
      <div className="leg mt-3 items-center">
        <span className="font-mono text-xs">{fmt(meio - lim)}</span>
        <span className="flex-1 h-2.5 rounded-full min-w-[120px]" style={{ background: `linear-gradient(90deg, ${COR.adv}, var(--s-neutro), ${COR.lula})` }} />
        <span className="font-mono text-xs">{fmt(meio + lim)}</span>
        <span className="text-xs basis-full">verde-azulado = mais para Lula · violeta = mais para Flávio Bolsonaro · cinza = equilíbrio</span>
      </div>
    </Grafico>
  );
}
