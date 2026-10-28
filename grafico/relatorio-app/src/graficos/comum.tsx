// Peças comuns dos gráficos: medida do contêiner, legenda, título, tabela alternativa.
import { useEffect, useRef, useState, type ReactNode } from 'react';
import { clsx } from 'clsx';

export const COR = {
  s2026: 'var(--s-2026)', ref: 'var(--s-ref)', lula: 'var(--s-lula)', adv: 'var(--s-adv)', neutro: 'var(--s-neutro)', aviso: 'var(--s-aviso)',
  ok: 'var(--ok)', erro: 'var(--erro)', texto: 'var(--text)', muted: 'var(--text-muted)', subtle: 'var(--text-subtle)', grade: 'var(--grade)', surface: 'var(--surface)', accent: 'var(--accent)',
};

export function useLargura<T extends HTMLElement>(minimo = 280) {
  const ref = useRef<T>(null);
  const [w, setW] = useState(0);
  useEffect(() => {
    const el = ref.current; if (!el) return;
    const ro = new ResizeObserver((es) => { const x = es[0].contentRect.width; if (x) setW(Math.max(minimo, Math.round(x))); });
    ro.observe(el); setW(Math.max(minimo, Math.round(el.getBoundingClientRect().width)));
    return () => ro.disconnect();
  }, [minimo]);
  return [ref, w] as const;
}

export type ItemLegenda = { nome: string; cor: string; tipo?: 'barra' | 'linha' | 'ponto'; traco?: boolean };
export function Legenda({ itens, className }: { itens: ItemLegenda[]; className?: string }) {
  if (itens.length < 2) return null;
  return (
    <div className={clsx('leg', className)} aria-hidden="true">
      {itens.map((i) => (
        <span key={i.nome}><i className={clsx(i.tipo || 'barra', i.traco && 'traco')} style={{ background: i.tipo === 'linha' ? 'transparent' : i.cor, ['--c' as string]: i.cor, borderTopColor: i.cor }} />{i.nome}</span>
      ))}
    </div>
  );
}

export function Grafico({ titulo, sub, legenda, children, tabela, className, rotuloA11y }: { titulo?: ReactNode; sub?: ReactNode; legenda?: ItemLegenda[]; children: ReactNode; tabela?: ReactNode; className?: string; rotuloA11y?: string }) {
  return (
    <figure className={clsx('grafico m-0 min-w-0', className)} aria-label={rotuloA11y}>
      {(titulo || sub) && (
        <figcaption className="mb-2">
          {titulo && <div className="text-[14px] font-semibold text-text leading-snug">{titulo}</div>}
          {sub && <div className="text-[13px] text-muted leading-snug mt-0.5">{sub}</div>}
        </figcaption>
      )}
      {legenda && <Legenda itens={legenda} className="mb-2" />}
      {children}
      {tabela && (
        <details className="mt-2 group">
          <summary className="cursor-pointer text-[13px] font-medium text-accent-text inline-flex items-center gap-1 h-9 select-none list-none [&::-webkit-details-marker]:hidden">
            <span className="transition-transform group-open:rotate-90 inline-block">▸</span> ver como tabela
          </summary>
          <div className="rolavel mt-1 border border-border rounded-lg bg-surface">{tabela}</div>
        </details>
      )}
    </figure>
  );
}

export function Tabela({ cab, linhas }: { cab: string[]; linhas: (string | number | ReactNode)[][] }) {
  return (
    <table className="tabela">
      <thead><tr>{cab.map((c, i) => <th key={i} className={i && linhas[0] && (typeof linhas[0][i] !== 'string' || /^[+−-]?\d|^—$|^</.test(linhas[0][i] as string)) ? 'text-right' : ''}>{c}</th>)}</tr></thead>
      <tbody>{linhas.map((l, i) => <tr key={i}>{l.map((c, j) => <td key={j} className={j && (typeof c !== 'string' || /^[+−-]?\d|^—$|^</.test(c)) ? 'n' : ''}>{c}</td>)}</tr>)}</tbody>
    </table>
  );
}
export const nice = (x: number) => { const p = Math.pow(10, Math.floor(Math.log10(x || 1))), f = x / p; return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * p; };
export const ticks = (lo: number, hi: number, n = 4) => {
  const passo = nice((hi - lo) / n) || 1; const out: number[] = [];
  for (let v = Math.ceil(lo / passo) * passo; v <= hi + 1e-9; v += passo) out.push(+v.toFixed(10));
  return out;
};
