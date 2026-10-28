// História científica de um teste: versão original congelada → contestações (provas) → mudanças com causa → estado atual.
// Usado na gaveta do teste e na página Evolução da pesquisa.
import type { Teste, Prova, Mudanca, LinhaDoTempo, Achado } from '@/lib/tipos';
import { useDados } from '@/lib/dados';
import { dataBR } from '@/lib/formato';
import { SeloClasse } from './base';

export const PROVA_ROT: Record<Prova['resultado'], string> = { resistiu: 'resistiu', caiu: 'caiu', ajustado: 'ajustado', em_andamento: 'em andamento', em_revisao: 'em revisão', inalterado: 'inalterado' };
export const PROVA_COR: Record<Prova['resultado'], string> = { resistiu: 'var(--ok)', caiu: 'var(--erro)', ajustado: 'var(--warn)', em_andamento: 'var(--text-subtle)', em_revisao: 'var(--accent)', inalterado: 'var(--ok)' };
export const CAUSA_ROT: Record<string, string> = { dados: 'dados', codigo: 'código', metodo: 'método', nova_evidencia: 'nova evidência', interpretacao: 'interpretação', redacao: 'redação', rastreabilidade: 'rastreabilidade' };
const ALVO_ROT: Record<string, string> = { evidencia: 'evidência', metodo: 'método', interpretacao: 'interpretação', redacao: 'redação', rastreabilidade: 'rastreabilidade' };
const SIT = (s: string) => s.replace(/_/g, ' ').replace('concluido', 'concluído');

export function SeloProva({ r }: { r: Prova['resultado'] }) {
  return <span className="inline-flex items-center gap-1.5 h-6 px-2 rounded-full text-xs font-medium border shrink-0" style={{ color: PROVA_COR[r], borderColor: PROVA_COR[r] }}><i className="w-1.5 h-1.5 rounded-full" style={{ background: PROVA_COR[r] }} />{PROVA_ROT[r]}</span>;
}
export function SeloCausa({ c }: { c: string }) {
  return <span className="inline-flex items-center h-6 px-2 rounded-md text-xs font-mono border border-border bg-surface-2 text-muted shrink-0">{CAUSA_ROT[c] || c}</span>;
}

function Passo({ n, titulo, children, cor = 'var(--accent)' }: { n: number; titulo: string; children: React.ReactNode; cor?: string }) {
  return (
    <li className="relative pl-9">
      <span className="absolute left-0 top-0 w-6 h-6 grid place-items-center rounded-full text-[12px] font-semibold" style={{ background: cor, color: 'var(--bg)' }}>{n}</span>
      <div className="text-[13px] font-semibold text-text uppercase tracking-wide">{titulo}</div>
      <div className="mt-1.5">{children}</div>
    </li>
  );
}

export function HistoriaCientifica({ t }: { t: Teste }) {
  const { dados: lt } = useDados<LinhaDoTempo>('linha-do-tempo');
  const achados = new Map<string, Achado>((lt?.revisoes || []).flatMap((r) => r.achados.map((a) => [a.id, a] as [string, Achado])));
  const versoes = t.versoes || [];
  const provas = t.provas || [];
  const mud: Mudanca[] = t.mudancas || [];
  const v0 = versoes[0];
  if (!v0 && !provas.length) return <p>Este teste ainda não está em nenhuma versão congelada.</p>;
  return (
    <ol className="grid gap-5 relative before:absolute before:left-[11px] before:top-3 before:bottom-3 before:w-px before:bg-border">
      {versoes.map((v, i) => (
        <Passo key={v.versao} n={i + 1} titulo={`${v.versao} · ${i === 0 ? 'resultado e interpretação originais' : 'versão congelada'}`} cor="var(--text-subtle)">
          <div className="flex flex-wrap items-center gap-2 text-[13px]"><SeloClasse classe={v.classe_evidencia} /><span className="text-subtle">{SIT(v.situacao)} · {v.natureza} · método v{v.metodo_versao} · {dataBR(v.data)}{v.commit ? ` · commit ${v.commit.slice(0, 7)}` : ''}</span></div>
          <p className="mt-1.5 text-[14px] leading-relaxed">{v.resultado}</p>
          {v.nota && <p className="mt-1 text-xs text-subtle">{v.nota}</p>}
          {i > 0 && (v.mudancas || []).length > 0 && <ul className="mt-2 grid gap-1.5">{v.mudancas!.map((m, k) => <li key={k} className="flex flex-wrap items-start gap-2 text-[13.5px]"><SeloCausa c={m.causa} /><span className="text-subtle font-mono text-xs mt-1">{m.campo} · {m.origem}</span><span className="basis-full sm:basis-auto sm:flex-1 min-w-0">{m.justificativa}</span></li>)}</ul>}
        </Passo>
      ))}
      <Passo n={versoes.length + 1} titulo={`Contestações (${provas.length})`} cor={provas.some((p) => p.resultado === 'caiu') ? 'var(--erro)' : 'var(--warn)'}>
        {provas.length ? (
          <ul className="grid gap-2">{provas.map((p, i) => {
            const id = p.tipo.match(/(R\d+-\d+|A-\d+)/)?.[1];
            const a = id ? achados.get(id) : undefined;
            return (
              <li key={i} className="rounded-lg border border-border p-3 bg-surface-2/60">
                <div className="flex flex-wrap items-center gap-2 text-[13px]"><SeloProva r={p.resultado} />{p.alvo && <span className="text-subtle">alvo: {ALVO_ROT[p.alvo] || p.alvo}</span>}<span className="text-subtle">· {p.tipo} · {dataBR(p.data)}</span>{p.rodada && <span className="font-mono text-xs h-6 px-2 inline-flex items-center rounded-md border border-border text-muted">{versoes.find((v) => v.rodada === p.rodada)?.versao || `rodada ${p.rodada}`}</span>}</div>
                {a && <p className="mt-1.5 text-[13px] text-subtle"><b className="font-medium text-muted">{a.id}:</b> {a.titulo}</p>}
                <p className="mt-1 text-[14px]">{p.descricao}</p>
              </li>
            );
          })}</ul>
        ) : <p className="text-[14px]">Ainda não foi contestado. Cada contestação fica registrada aqui com o resultado: resistiu, ajustado, caiu, em andamento, em revisão ou inalterado.</p>}
      </Passo>
      {mud.length > 0 && (
        <Passo n={versoes.length + 2} titulo="Mudanças e justificativas" cor="var(--accent)">
          <ul className="grid gap-1.5">{mud.map((m, i) => (
            <li key={i} className="flex flex-wrap items-start gap-2 text-[14px]"><SeloCausa c={m.causa} /><span className="text-subtle font-mono text-xs mt-1">{m.campo} · {m.origem}</span><span className="basis-full sm:basis-auto sm:flex-1 min-w-0">{m.justificativa}</span></li>
          ))}</ul>
          {new Set(mud.map((m) => m.causa)).size > 1 && <p className="mt-2 text-xs text-subtle">Mais de uma causa: a diferença em relação à versão anterior não se atribui a uma causa só.</p>}
        </Passo>
      )}
      <Passo n={versoes.length + (mud.length ? 3 : 2)} titulo="Resultado e interpretação atuais" cor="var(--ok)">
        <div className="flex flex-wrap items-center gap-2 text-[13px]"><SeloClasse classe={t.classe_evidencia} /><span className="text-subtle">{SIT(t.situacao)} · método v{t.metodo_versao || 1}{t.pre_especificacao === 'anterior_ao_protocolo' ? ' · executado antes do protocolo (não pré-registrado)' : ''}</span></div>
        <p className="mt-1.5 text-[14px] leading-relaxed"><b className="text-text font-medium">Evidência:</b> {t.evidencia || t.resultado_atual}</p>
        {t.interpretacao && <p className="mt-1.5 text-[14px] leading-relaxed"><b className="text-text font-medium">Interpretação:</b> {t.interpretacao}</p>}
        {!t.interpretacao && <p className="mt-1.5 text-xs text-subtle">Interpretação ainda não separada da evidência neste teste.</p>}
      </Passo>
    </ol>
  );
}
