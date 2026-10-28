// Histórico de um teste rodada a rodada e as provas a que ele foi submetido (usado na gaveta do teste e na linha do tempo).
import { clsx } from 'clsx';
import type { HistoricoTeste, Prova } from '@/lib/tipos';
import { dataBR } from '@/lib/formato';
import { SeloClasse } from './base';

export const PROVA_ROT: Record<Prova['resultado'], string> = { resistiu: 'resistiu', caiu: 'caiu', ajustado: 'ajustado', em_andamento: 'em andamento' };
export const PROVA_COR: Record<Prova['resultado'], string> = { resistiu: 'var(--ok)', caiu: 'var(--erro, #c2410c)', ajustado: 'var(--warn)', em_andamento: 'var(--text-subtle)' };
const SIT = (s: string) => s.replace(/_/g, ' ').replace('concluido', 'concluído');

export function SeloProva({ r }: { r: Prova['resultado'] }) {
  return <span className="inline-flex items-center gap-1.5 h-6 px-2 rounded-full text-xs font-medium border" style={{ color: PROVA_COR[r], borderColor: PROVA_COR[r] }}><i className="w-1.5 h-1.5 rounded-full" style={{ background: PROVA_COR[r] }} />{PROVA_ROT[r]}</span>;
}

export function HistoricoDoTeste({ historico = [], provas = [] }: { historico?: HistoricoTeste[]; provas?: Prova[] }) {
  if (!historico.length && !provas.length) return <p>Este teste ainda não está em nenhuma rodada fechada.</p>;
  return (
    <div className="grid gap-5">
      <ol className="relative grid gap-3 pl-5 before:absolute before:left-[7px] before:top-2 before:bottom-2 before:w-px before:bg-border">
        {historico.map((h, i) => {
          const ant = historico[i - 1];
          const mudou = ant && (['situacao', 'classe_evidencia', 'natureza', 'resultado_atual'] as const).filter((k) => ant[k] !== h[k]);
          return (
            <li key={h.rodada} className="relative">
              <span className="absolute -left-5 top-1.5 w-[15px] h-[15px] rounded-full border-2 border-bg" style={{ background: 'var(--accent)' }} />
              <div className="flex flex-wrap items-center gap-2 text-[13px]">
                <b className="text-text font-semibold">Rodada {h.rodada}</b><span className="text-subtle">{dataBR(h.data)}</span>
                <SeloClasse classe={h.classe_evidencia} /><span className="text-subtle">{SIT(h.situacao)} · {h.natureza}</span>
              </div>
              {mudou && mudou.length > 0 && <div className="mt-1 text-xs font-medium" style={{ color: 'var(--warn)' }}>mudou desde a rodada {ant.rodada}: {mudou.map((k) => ({ situacao: 'situação', classe_evidencia: 'classe', natureza: 'natureza', resultado_atual: 'resultado' })[k]).join(', ')}</div>}
              <p className="mt-1.5 text-[14px] leading-relaxed">{h.resultado_atual}</p>
            </li>
          );
        })}
      </ol>
      <div>
        <div className="text-[13px] font-medium text-text mb-2">Provas a que foi submetido</div>
        {provas.length ? (
          <ul className="grid gap-2">{provas.map((p, i) => (
            <li key={i} className={clsx('rounded-lg border border-border p-3 bg-surface-2/60')}>
              <div className="flex flex-wrap items-center gap-2 text-[13px]"><SeloProva r={p.resultado} /><b className="text-text font-medium">{p.tipo}</b><span className="text-subtle">rodada {p.rodada} · {dataBR(p.data)}</span></div>
              <p className="mt-1.5 text-[14px]">{p.descricao}</p>
            </li>))}
          </ul>
        ) : <p className="text-[14px]">Ainda não foi posto à prova. A próxima fase do estudo (double check da metodologia) revisa este teste, e cada contestação fica registrada aqui com o resultado: resistiu, caiu ou ajustado.</p>}
      </div>
    </div>
  );
}
