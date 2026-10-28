import { clsx } from 'clsx';
import type { ReactNode, ButtonHTMLAttributes, AnchorHTMLAttributes } from 'react';

type BotaoProps = { variante?: 'primario' | 'secundario' | 'fantasma' | 'cobre'; tamanho?: 'sm' | 'md' | 'lg'; icone?: boolean; className?: string; children?: ReactNode };
const botaoClasses = ({ variante = 'secundario', tamanho = 'md', icone = false, className }: BotaoProps) =>
  clsx(
    'inline-flex items-center justify-center gap-2 font-medium rounded-full whitespace-nowrap select-none transition-[background,border-color,color,transform,box-shadow] duration-200 ease-out',
    'focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50 disabled:pointer-events-none active:scale-[.98]',
    tamanho === 'sm' && (icone ? 'h-9 w-9 text-sm' : 'h-9 px-3.5 text-sm'),
    tamanho === 'md' && (icone ? 'h-11 w-11 text-[15px]' : 'h-11 px-5 text-[15px]'),
    tamanho === 'lg' && (icone ? 'h-12 w-12 text-base' : 'h-12 px-6 text-base'),
    variante === 'primario' && 'bg-brand text-brand-contrast border border-brand hover:opacity-90',
    variante === 'cobre' && 'bg-accent text-white border border-accent hover:brightness-95',
    variante === 'secundario' && 'bg-surface text-text border border-border hover:border-border-strong hover:bg-surface-2',
    variante === 'fantasma' && 'bg-transparent text-muted border border-transparent hover:bg-surface-2 hover:text-text',
    className,
  );
export function Botao({ variante, tamanho, icone, className, children, ...rest }: BotaoProps & ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button type="button" className={botaoClasses({ variante, tamanho, icone, className })} {...rest}>{children}</button>;
}
export function BotaoLink({ variante, tamanho, icone, className, children, ...rest }: BotaoProps & AnchorHTMLAttributes<HTMLAnchorElement>) {
  return <a className={botaoClasses({ variante, tamanho, icone, className })} {...rest}>{children}</a>;
}

export function Eyebrow({ children, className }: { children: ReactNode; className?: string }) {
  return <div className={clsx('t-eyebrow', className)}>{children}</div>;
}

export function Chip({ ativo, cor, children, className, ...rest }: { ativo?: boolean; cor?: string; children: ReactNode; className?: string } & ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button type="button" aria-pressed={!!ativo}
      className={clsx('inline-flex items-center gap-2 h-10 px-3.5 rounded-full border text-sm font-medium transition-colors duration-150 t-num',
        ativo ? 'bg-brand text-brand-contrast border-brand' : 'bg-surface text-muted border-border hover:border-border-strong hover:text-text', className)} {...rest}>
      {cor && <i className="w-2.5 h-2.5 rounded-full shrink-0" style={{ background: cor, outline: ativo ? '2px solid var(--brand-contrast)' : undefined, outlineOffset: -1 }} />}
      {children}
    </button>
  );
}

export const CLASSE_COR: Record<string, string> = { A: 'var(--cA)', B: 'var(--cB)', C: 'var(--cC)', D: 'var(--cD)', E: 'var(--cE)', F: 'var(--cF)', G: 'var(--cG)' };
export const CLASSE_EXPL: Record<string, string> = {
  A: 'O dado se comporta como esperado.', B: 'Algo fora do esperado estatístico, sem prova de que seja problema.', C: 'Anomalia que resiste a controles e alternativas.',
  D: 'Uma conta que deveria fechar não fecha, e dá para verificar.', E: 'Evidência de possível irregularidade.', F: 'Evidência de manipulação.', G: 'Ainda sem resultado ou inconclusivo.',
};
export function SeloClasse({ classe, nome, grande }: { classe: string; nome?: string; grande?: boolean }) {
  return (
    <span className={clsx('inline-flex items-center gap-2 rounded-full border border-border bg-surface font-medium text-text', grande ? 'h-9 pl-1 pr-3.5 text-sm' : 'h-7 pl-0.5 pr-2.5 text-xs')}
      title={CLASSE_EXPL[classe]}>
      <b className={clsx('grid place-items-center rounded-full text-white font-semibold', grande ? 'w-7 h-7 text-sm' : 'w-6 h-6 text-xs')} style={{ background: CLASSE_COR[classe] }}>{classe}</b>
      {nome && <span>{nome}</span>}
    </span>
  );
}

export type Estado = 'ok' | 'parc' | 'proc';
export const ESTADO_ROT: Record<Estado, string> = { ok: 'concluído', parc: 'parcial', proc: 'em processamento' };
export function SeloEstado({ estado, texto }: { estado: Estado; texto?: string }) {
  const cor = estado === 'ok' ? 'var(--ok)' : 'var(--warn)';
  return (
    <span className="inline-flex items-center gap-1.5 h-7 px-2.5 rounded-full text-xs font-medium border border-border bg-surface-2 text-muted">
      <i className="w-2 h-2 rounded-full" style={{ background: cor, boxShadow: estado === 'proc' ? `0 0 0 3px color-mix(in srgb, ${cor} 25%, transparent)` : undefined }} />
      {texto || ESTADO_ROT[estado]}
    </span>
  );
}

export function Skeleton({ className, linhas = 1 }: { className?: string; linhas?: number }) {
  return (
    <div className={clsx('grid gap-2', className)} aria-hidden="true">
      {Array.from({ length: linhas }).map((_, i) => <div key={i} className="skeleton h-4" style={{ width: `${100 - (i % 3) * 14}%` }} />)}
    </div>
  );
}
export function SkeletonBloco({ altura = 240, className }: { altura?: number; className?: string }) {
  return <div className={clsx('skeleton w-full', className)} style={{ height: altura }} aria-hidden="true" />;
}

export function Erro({ erro, aoTentar, compacto }: { erro: Error | string; aoTentar?: () => void; compacto?: boolean }) {
  const msg = typeof erro === 'string' ? erro : erro.message;
  return (
    <div role="alert" className={clsx('cartao flex flex-col items-start gap-3 border-erro/30', compacto ? 'p-4' : 'p-6')}>
      <div className="flex items-center gap-2 text-erro font-medium"><span className="grid place-items-center w-6 h-6 rounded-full bg-erro/10 text-sm">!</span>Não foi possível carregar</div>
      <p className="text-sm text-muted">{msg}</p>
      {aoTentar && <Botao variante="primario" tamanho="sm" onClick={aoTentar}>Tentar de novo</Botao>}
    </div>
  );
}

export function Nota({ children, className }: { children: ReactNode; className?: string }) {
  return <p className={clsx('text-[13px] leading-relaxed text-muted', className)}>{children}</p>;
}
