// Evolução da pesquisa. Visível: o caminho em etapas, as fases com o estado atual, as versões congeladas, as perguntas
// da Fase 2 com situação e resposta, e o inventário da Fase 3 com o estado final de cada item. Recolhido: revisão R1, critérios da baseline, comparação teste a teste, contestações e marcos.
import { useMemo, useState } from 'react';
import { clsx } from 'clsx';
import { Check, CircleDot, Circle, Clock, GitBranch, ExternalLink, FileText } from 'lucide-react';
import type { LinhaDoTempo as LT, Registro, Fase, Prova } from '@/lib/tipos';
import { useDados } from '@/lib/dados';
import { dataBR, N } from '@/lib/formato';
import { Eyebrow, SkeletonBloco, Erro, Nota, CLASSE_COR, SeloClasse, Chip } from '@/ui/base';
import { SeloProva, SeloCausa, CAUSA_ROT, PROVA_ROT } from '@/ui/Historico';

const ST: Record<string, { rot: string; cor: string; Ic: typeof Check }> = {
  concluida: { rot: 'concluída', cor: 'var(--ok)', Ic: Check },
  em_andamento: { rot: 'em andamento', cor: 'var(--accent)', Ic: CircleDot },
  em_revisao: { rot: 'em revisão', cor: 'var(--warn)', Ic: Clock },
  proxima: { rot: 'próxima', cor: 'var(--accent)', Ic: CircleDot },
  pendente: { rot: 'pendente', cor: 'var(--warn)', Ic: Clock },
  planejada: { rot: 'planejada', cor: 'var(--text-subtle)', Ic: Circle },
  disponivel: { rot: 'disponível', cor: 'var(--ok)', Ic: Check },
  vivo: { rot: 'vivo', cor: 'var(--accent)', Ic: CircleDot },
};
const CLASSIF: Record<string, string> = { confirmado: 'confirmado por nós', pendente_de_reproducao: 'pendente de reprodução', questao_metodologica: 'questão metodológica' };
const SITU: Record<string, { rot: string; cor: string }> = {
  aberto: { rot: 'aberto', cor: 'var(--erro)' }, em_andamento: { rot: 'em andamento', cor: 'var(--warn)' }, respondido: { rot: 'respondido', cor: 'var(--ok)' },
  aceito_como_limite: { rot: 'aceito como limite', cor: 'var(--text-subtle)' }, adiado_fase2: { rot: 'vira Fase 2', cor: 'var(--accent)' }, rejeitado: { rot: 'rejeitado', cor: 'var(--text-subtle)' },
};
const F2: Record<string, { rot: string; cor: string }> = {
  respondida: { rot: 'respondida', cor: 'var(--ok)' }, parcial: { rot: 'em parte', cor: 'var(--accent)' }, inventariada: { rot: 'inventariada', cor: 'var(--accent)' },
  adiada: { rot: 'adiada', cor: 'var(--warn)' }, 'sem_avanço': { rot: 'sem avanço', cor: 'var(--warn)' }, aberta: { rot: 'aberta', cor: 'var(--text-subtle)' },
};
// estado final dos itens da Fase 3 (fase3/inventario.json)
const F3: Record<string, { rot: string; cor: string }> = {
  respondida: { rot: 'respondida', cor: 'var(--ok)' }, 'respondida (revisada pelo P18)': { rot: 'respondida (revisada)', cor: 'var(--ok)' },
  'respondida parcialmente': { rot: 'em parte', cor: 'var(--accent)' }, 'não identificável com estes dados': { rot: 'não identificável', cor: 'var(--text-subtle)' },
  'bloqueada por evidência externa': { rot: 'bloqueada (fonte externa)', cor: 'var(--warn)' },
  'não executada nesta sessão': { rot: 'não executada', cor: 'var(--erro)' }, 'em revisão': { rot: 'em revisão', cor: 'var(--warn)' },
  'não decidível com os modelos disponíveis': { rot: 'não decidível', cor: 'var(--text-subtle)' },
};
const f3st = (e: string) => F3[e] || { rot: e, cor: 'var(--text-subtle)' };
const PRIO: Record<string, string> = { alta: 'alta', media_alta: 'média/alta', media: 'média', informativo: 'informativo', pergunta: 'pergunta' };

const Sec = ({ id, eyebrow, titulo, lead, children, fechado }: { id: string; eyebrow: string; titulo: string; lead?: string; children: React.ReactNode; fechado?: boolean }) => fechado ? (
  <details id={id} className="mt-3 scroll-mt-20 cartao group">
    <summary className="cursor-pointer list-none p-4 md:p-5 flex items-baseline gap-3 flex-wrap"><Eyebrow>{eyebrow}</Eyebrow><h2 className="t-h3">{titulo}</h2><span className="ml-auto text-xs text-subtle group-open:hidden">abrir</span><span className="ml-auto text-xs text-subtle hidden group-open:inline">fechar</span></summary>
    <div className="px-4 md:px-5 pb-5">{lead && <p className="text-muted text-[15px] max-w-[48rem] mb-5">{lead}</p>}{children}</div>
  </details>
) : (
  <section id={id} className="mt-16 md:mt-20 scroll-mt-20"><div className="max-w-[48rem]"><Eyebrow>{eyebrow}</Eyebrow><h2 className="t-h2 mt-2">{titulo}</h2>{lead && <p className="t-lead mt-3 text-[17px]">{lead}</p>}</div><div className="mt-6">{children}</div></section>
);
const Selo = ({ cor, children }: { cor: string; children: React.ReactNode }) => (
  <span className="inline-flex items-center gap-1.5 h-6 px-2 rounded-full text-xs font-medium border shrink-0" style={{ color: cor, borderColor: cor }}><i className="w-1.5 h-1.5 rounded-full" style={{ background: cor }} />{children}</span>
);
const irPara = (link: string) => (e: React.MouseEvent) => { if (link.startsWith('#') && !link.startsWith('#/')) { e.preventDefault(); (() => { const el = document.getElementById(link.slice(1)); if (el instanceof HTMLDetailsElement) el.open = true; return el; })()?.scrollIntoView({ behavior: 'smooth', block: 'start' }); } };

export function LinhaDoTempo({ reg }: { reg: Registro }) {
  const { dados: lt, erro, recarregar } = useDados<LT>('linha-do-tempo');
  const [fClass, setFClass] = useState('');
  const [fSit, setFSit] = useState('');
  const [fCausa, setFCausa] = useState('');
  const rev = lt?.revisoes?.[0];
  const achados = rev?.achados || [];
  const filtrados = achados.filter((a) => (!fClass || a.classificacao === fClass) && (!fSit || a.situacao === fSit));
  const provas = useMemo(() => reg.testes.flatMap((t) => (t.provas || []).map((p) => ({ ...p, id: t.id, pergunta: t.pergunta }))), [reg]);
  const contaProva = (r: Prova['resultado']) => provas.filter((p) => p.resultado === r).length;
  const mudaram = useMemo(() => reg.testes.filter((t) => (t.mudancas || []).length || (t.provas || []).length)
    .filter((t) => !fCausa || (t.mudancas || []).some((m) => m.causa === fCausa)), [reg, fCausa]);
  const causas = useMemo(() => { const c: Record<string, number> = {}; reg.testes.forEach((t) => new Set((t.mudancas || []).map((m) => m.causa)).forEach((k) => (c[k] = (c[k] || 0) + 1))); return c; }, [reg]);

  if (erro) return <div className="container py-16"><Erro erro={erro} aoTentar={recarregar} /></div>;
  if (!lt) return <div className="container py-16 grid gap-4"><SkeletonBloco altura={220} /><SkeletonBloco altura={320} /></div>;

  // critérios conferidos na aprovação da V1.0 (28/10/2026): história fixa, não recalculada sobre o registro vivo
  const criterios = [
    { t: 'Todo achado da R1 respondido, aceito como limite ou adiado para a Fase 2 com justificativa', d: `${achados.filter((a) => a.situacao === 'respondido').length} respondidos e ${achados.filter((a) => a.situacao === 'adiado_fase2').length} adiados para a Fase 2` },
    { t: 'Ações de prioridade alta com alvo V1.0 concluídas', d: 'cumprido' },
    { t: 'Verificador passa comparando conjuntos de chaves', d: 'make verificar: todas as seções do Boletim de Urna processadas nos dois turnos' },
    { t: 'Conclusão revisada coerente com o registro', d: 'CONCLUSAO.md revisado, com a tabela de mudanças em relação à rc1' },
    { t: 'Proveniência completa', d: 'commit, manifesto de dados, ambiente, sementes e parâmetros em rodadas/rodada-2/proveniencia.json' },
    { t: 'Aprovação explícita do responsável pelo estudo', d: 'dada em 28/10/2026; aprovar não significa que os resultados sejam infalíveis, e sim que o levantamento foi documentado e auditado por critérios explícitos' },
  ];
  const etapas = lt.caminho.filter((e) => e.status !== 'disponivel' && e.status !== 'vivo');
  const contF2: Record<string, number> = {};
  lt.fase2.forEach((q) => { const k = q.situacao || 'aberta'; contF2[k] = (contF2[k] || 0) + 1; });
  const ultima = lt.rodadas[lt.rodadas.length - 1];
  const f2 = lt.fases.find((f) => f.id === 'F2');
  const fila = lt.fase2.filter((q) => (q.situacao || 'aberta') === 'aberta');
  const feitas = lt.fase2.filter((q) => (q.situacao || 'aberta') !== 'aberta');
  const v0 = lt.rodadas[0];
  const fase3 = lt.fase3 || [];
  const f3 = lt.fases.find((f) => f.id === 'F3');
  const f3Ativos = fase3.filter((i) => i.estado_inicial_f3 !== 'respondida' || i.reaberta_na_revisao);
  const f3Herdados = fase3.filter((i) => i.estado_inicial_f3 === 'respondida' && !i.reaberta_na_revisao);
  const contF3: Record<string, number> = {};
  f3Ativos.forEach((i) => { const k = f3st(i.estado_final).rot; contF3[k] = (contF3[k] || 0) + 1; });
  const corF3 = (rot: string) => Object.values(F3).find((x) => x.rot === rot)?.cor || 'var(--text-subtle)';
  const bloqueadas = f3Ativos.filter((i) => /bloquead/.test(i.estado_final));
  const pergF2 = (id: string) => lt.fase2.find((q) => q.id === id)?.pergunta;
  // todas as fases com rodada e versão congelada depois da baseline (F2, F3 e as rodadas 6, 7...), não só as numeradas como F2, F3
  const concluidas = lt.fases.filter((f) => f.rodada != null && f.rodada >= 3 && f.status === 'concluida' && /^V\d/.test(f.versao || ''));
  const emAndamento = [...lt.fases].reverse().find((f) => f.status === 'em_andamento' || f.status === 'em_revisao');
  const nomeFase = (f: Fase) => (/^F\d+$/.test(f.id) ? `a ${f.id.replace('F', 'Fase ')}` : `a rodada ${f.rodada} (${f.titulo})`);

  return (
    <div className="container pb-24">
      <header className="pt-10 md:pt-16 max-w-[54rem]">
        <Eyebrow>Evolução da pesquisa</Eyebrow>
        <h1 className="t-h1 mt-3">A pesquisa se corrige sem reescrever o próprio passado</h1>
        <p className="t-lead mt-4 text-[18px]">Cada versão do estudo fica congelada; revisões tentam derrubá-la e cada contestação fica no teste que contesta. {lt.situacao_atual ? <b className="font-medium text-text">{lt.situacao_atual}.</b> : null}</p>
      </header>

      {/* caminho em etapas */}
      <nav aria-label="Etapas da pesquisa" className="mt-10">
        <ol className={clsx('grid gap-2 grid-cols-2', etapas.length >= 5 ? 'lg:grid-cols-5' : 'lg:grid-cols-4')}>
          {etapas.map((e, i) => {
            const s = ST[e.status] || ST.planejada;
            return (
              <li key={e.id}>
                <a href={e.link} onClick={irPara(e.link)} className="cartao h-full p-3.5 flex flex-col gap-1.5 hover:border-border-strong transition-colors" style={{ borderTop: `3px solid ${s.cor}` }}>
                  <div className="flex items-center gap-2 text-[12px]"><span className="w-6 h-6 grid place-items-center rounded-full font-semibold" style={{ background: s.cor, color: 'var(--bg)' }}><s.Ic size={13} strokeWidth={2.8} /></span><span className="font-mono text-subtle">{i + 1} · {e.versao}</span></div>
                  <div className="text-[16px] font-semibold text-text leading-tight">{e.titulo}</div>
                  <div className="text-[13px] font-medium" style={{ color: s.cor }}>{s.rot}</div>
                </a>
              </li>
            );
          })}
        </ol>
        <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-[13.5px]"><a href="#comparar" onClick={irPara('#comparar')} className="text-accent-text underline underline-offset-4">O que mudou da rc1 para hoje, teste a teste</a><a href="#/testes" className="text-accent-text underline underline-offset-4">Registro vivo dos testes</a></div>
      </nav>

      {/* fases */}
      <Sec id="fases" eyebrow="Fases" titulo="Onde a pesquisa está" lead={`O levantamento da Fase 1 foi congelado como V1.0-rc1, revisado (R1) e aprovado como baseline V1.0. Depois, ${concluidas.map((f) => `${nomeFase(f)} foi concluída e congelada como ${f.versao}`).join('; ')}.${emAndamento ? ` ${emAndamento.titulo}: ${ST[emAndamento.status]?.rot || 'em andamento'}, ainda não congelada.` : ''}`}>
        <ol className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {lt.fases.map((f: Fase) => {
            const s = ST[f.status] || ST.planejada;
            return (
              <li key={f.id} className="cartao p-5" style={{ borderTop: `3px solid ${s.cor}` }}>
                <div className="flex items-center gap-2 text-[13px]"><span className="w-7 h-7 grid place-items-center rounded-full" style={{ background: s.cor, color: 'var(--bg)' }}><s.Ic size={15} strokeWidth={2.6} /></span><span className="font-mono text-subtle">{f.id}{f.versao && f.versao !== f.id ? ` · ${f.versao}` : ''}</span><span className="ml-auto font-medium" style={{ color: s.cor }}>{s.rot}</span></div>
                <h3 className="t-h3 mt-3">{f.titulo}</h3>
                {(f.inicio || f.fim) && <div className="text-[13px] text-subtle mt-1">{f.inicio ? dataBR(f.inicio) : ''}{f.fim ? ` a ${dataBR(f.fim)}` : ''}</div>}
                <p className="text-[14.5px] text-muted mt-2 leading-relaxed">{f.resumo}</p>
                {f.etapas.length > 0 && <details className="mt-3 group/et">
                  <summary className="cursor-pointer list-none text-[13px] font-medium text-accent-text"><span className="group-open/et:hidden">Ver as {f.etapas.length} etapas</span><span className="hidden group-open/et:inline">Recolher etapas</span></summary>
                  <ul className="mt-3 grid gap-2.5">{f.etapas.map((e) => (
                    <li key={e.titulo} className="flex gap-2.5"><span className="mt-1 w-4 h-4 shrink-0 grid place-items-center rounded-full" style={{ background: f.status === 'concluida' ? 'var(--ok)' : 'var(--surface-2)', color: 'var(--bg)' }}>{f.status === 'concluida' && <Check size={11} strokeWidth={3} />}</span><div><div className="text-[14px] font-medium text-text">{e.titulo}</div><div className="text-[13px] text-muted leading-snug mt-0.5">{e.texto}</div></div></li>
                  ))}</ul>
                </details>}
              </li>
            );
          })}
        </ol>
        <div className="mt-4 cartao divide-y divide-border">
          {emAndamento && emAndamento.rodada != null && !lt.rodadas.some((r) => r.rodada === emAndamento.rodada) && (
            <div className="p-4 md:p-5">
              <div className="flex flex-wrap items-baseline gap-x-2 gap-y-1"><span className="text-xl font-semibold tracking-tight">Rodada {emAndamento.rodada}</span><span className="text-[13px] text-subtle">{emAndamento.titulo.replace(/\s*\(rodada \d+\)/, "")} · aberta, não congelada</span><Selo cor="var(--accent)">{ST[emAndamento.status]?.rot || 'em andamento'}</Selo></div>
              <p className="mt-1.5 text-[13.5px] text-muted">Está no registro vivo dos testes e nas respostas; ganha hash, tag e conclusão própria só quando for congelada, com aprovação do responsável.</p>
            </div>
          )}
          {[...lt.rodadas].reverse().map((r) => (
            <div key={r.rodada} className="p-4 md:p-5 grid gap-3 lg:grid-cols-[1fr_auto] lg:items-center">
              <div>
                <div className="flex flex-wrap items-baseline gap-x-2 gap-y-1"><span className="text-xl font-semibold tracking-tight">{r.versao || `Rodada ${r.rodada}`}</span><span className="text-[13px] text-subtle">rodada {r.rodada} · congelada em {dataBR(r.data)}{r.tag ? ` · tag ${r.tag}` : ''}</span>{r === ultima ? <Selo cor="var(--ok)">versão vigente</Selo> : <Selo cor="var(--text-subtle)">histórico</Selo>}</div>
                <div className="mt-2 flex h-2.5 rounded-full overflow-hidden gap-[2px] max-w-[420px]">{'ABCDEFG'.split('').filter((k) => r.placar.classes[k]).map((k) => <div key={k} title={`${k}: ${r.placar.classes[k]}`} style={{ width: `${(100 * r.placar.classes[k]) / r.placar.testes}%`, background: CLASSE_COR[k] }} />)}</div>
                <div className="mt-1.5 text-[13px] text-muted">{N(r.placar.testes)} testes · classes da Fase 1: {'ABCDEFG'.split('').filter((k) => r.placar.classes[k]).map((k) => `${k} ${r.placar.classes[k]}`).join(' · ')} · {r.arquivos} arquivos com SHA-256</div>
              </div>
              {r.tag && <div className="flex flex-wrap gap-2">
                <a className="inline-flex items-center gap-1.5 min-h-10 py-2 px-4 rounded-full border border-border text-sm font-medium hover:border-border-strong" href={`${lt.github}/tree/${r.tag}/rodadas/rodada-${r.rodada}`} target="_blank" rel="noopener"><GitBranch size={15} />Arquivos congelados <ExternalLink size={13} /></a>
                <a className="inline-flex items-center gap-1.5 min-h-10 py-2 px-4 rounded-full border border-border text-sm font-medium hover:border-border-strong" href={`${lt.github}/blob/${r.tag}/rodadas/rodada-${r.rodada}/CONCLUSAO.md`} target="_blank" rel="noopener"><FileText size={15} />Conclusão desta versão <ExternalLink size={13} /></a>
              </div>}
            </div>
          ))}
        </div>
      </Sec>
      {/* fase 2 */}
      <Sec id="fase2" eyebrow={`Fase 2 · ${ST[f2?.status || 'em_andamento']?.rot || ''}`} titulo="O que a Fase 2 respondeu" lead="Cada pergunta foi registrada antes de rodar e tenta derrubar um método ou uma conclusão. Abaixo, a resposta em poucas palavras e o que ela representa em votos; o detalhe técnico fica recolhido.">
        <div className="mb-3 flex flex-wrap gap-1.5">{Object.keys(F2).filter((k) => k !== 'aberta' && contF2[k]).map((k) => <Selo key={k} cor={F2[k].cor}>{contF2[k]} {contF2[k] > 1 && !['parcial', 'sem_avanço'].includes(k) ? F2[k].rot + 's' : F2[k].rot}</Selo>)}{fila.length > 0 && <Selo cor="var(--text-subtle)">{fila.length} {fila.every((q) => q.f3) ? 'levadas à Fase 3' : 'na fila'}</Selo>}</div>
        <ul className="cartao divide-y divide-border">
          {feitas.map((q) => {
            const st = F2[q.situacao || 'aberta'] || F2.aberta;
            return (
              <li key={q.id} className="p-3 md:p-4">
                <div className="flex items-start gap-3">
                  <span className="font-mono text-sm font-semibold w-9 shrink-0 pt-0.5">{q.id}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex flex-wrap items-start gap-x-3 gap-y-1.5"><span className="text-[15px] text-text font-medium leading-snug flex-1 min-w-[14rem]">{q.pergunta}</span><Selo cor={st.cor}>{st.rot}</Selo></div>
                    {(q.resumo_claro || q.resposta) && <p className="mt-1.5 text-[14.5px] text-muted leading-relaxed">{q.resumo_claro || q.resposta}</p>}
                    <div className="mt-1.5 flex flex-wrap items-center gap-x-3 gap-y-1.5 text-[13px]">
                      {q.em_votos && <span><b className="font-medium text-text">Em votos:</b> <span className="text-muted">{q.em_votos}</span></span>}
                      {q.testes && q.testes.length > 0 && <span className="inline-flex flex-wrap gap-1">{q.testes.map((t) => <a key={t} href={`#/testes/${t}`} className="font-mono text-xs h-6 px-2 inline-flex items-center rounded-md border border-border hover:border-border-strong">{t}</a>)}</span>}
                    </div>
                    <details className="mt-1.5 group/q">
                      <summary className="cursor-pointer list-none text-[12.5px] text-subtle hover:text-text"><span className="group-open/q:hidden">detalhe técnico</span><span className="hidden group-open/q:inline">recolher</span></summary>
                      <div className="mt-2 text-[13.5px] text-muted grid gap-1.5">
                        {q.resumo_claro && q.resposta && <div><b className="font-medium text-text">Resposta técnica: </b>{q.resposta}</div>}
                        <div><b className="font-medium text-text">Distingue: </b>{q.distingue}</div>
                        <div><b className="font-medium text-text">Pode mudar: </b>{q.afirmacao}</div>
                        <div><b className="font-medium text-text">Menor teste: </b>{q.teste}</div>
                        <div className="text-xs text-subtle">{q.natureza} · origem: {q.origem}</div>
                      </div>
                    </details>
                  </div>
                </div>
              </li>
            );
          })}
        </ul>
        {fila.length > 0 && <div className="mt-8">
          <h3 className="t-h3">{fila.every((q) => q.f3) ? 'O que ficou para a Fase 3' : 'O que ficou para depois'}</h3>
          <p className="text-muted text-[15px] mt-1 max-w-[48rem]">Perguntas que nasceram dos resultados da Fase 2. {fila.some((q) => q.f3) ? <>Foram levadas à Fase 3; o estado final está abaixo e o detalhe, <a href="#fase3" onClick={irPara('#fase3')} className="text-accent-text underline underline-offset-4">na seção da Fase 3</a>.</> : 'Estão registradas, ainda sem resposta.'}</p>
          <ul className="mt-3 cartao divide-y divide-border">
            {fila.map((q) => (
              <li key={q.id} className="p-3 md:p-4 flex items-start gap-3">
                <span className="font-mono text-sm font-semibold w-9 shrink-0 pt-0.5">{q.id}</span>
                <div className="flex-1 min-w-0">
                  <div className="flex flex-wrap items-start gap-x-3 gap-y-1.5"><span className="text-[15px] text-text leading-snug flex-1 min-w-[14rem]">{q.pergunta}</span>{q.f3 && <Selo cor={f3st(q.f3.estado_final).cor}>Fase 3 · {f3st(q.f3.estado_final).rot}</Selo>}</div>
                  {q.f3 ? <p className="mt-1.5 text-[14px] text-muted leading-relaxed">{q.f3.resposta}</p> : <div className="mt-1 text-[13px] text-muted"><b className="font-medium text-text">Como responder:</b> {q.teste} <span className="text-subtle">· nasceu de {q.origem}</span></div>}
                </div>
              </li>
            ))}
          </ul>
        </div>}
        <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-[13.5px]"><a href="#/docs/fase2" className="text-accent-text underline underline-offset-4">FASE2.md completo</a><a href="#/testes?modulo=G" className="text-accent-text underline underline-offset-4">Testes da Fase 2 (módulo G)</a></div>
      </Sec>

      {/* fase 3 */}
      {fase3.length > 0 && <Sec id="fase3" eyebrow={`Fase 3 · ${f3?.versao || ''} · ${ST[f3?.status || 'em_andamento']?.rot || ''}`} titulo={f3?.status === 'em_revisao' ? 'Fase 3 em revisão: o estado de cada item' : 'O que a Fase 3 resolveu'} lead={`${fase3.length} itens inventariados: as pendências da Fase 2, a fila P18 a P21 e perguntas novas sobre curvas, zeros e reconciliação externa. Cada item tem o estado final e a resposta, ou o motivo de não ter resposta.`}>
        <div className="mb-3 flex flex-wrap gap-1.5">{Object.keys(contF3).map((k) => <Selo key={k} cor={corF3(k)}>{contF3[k]} {k}</Selo>)}<Selo cor="var(--text-subtle)">{f3Herdados.length} da Fase 2, não reabertas</Selo></div>
        {bloqueadas.length > 0 && <div className="mb-3 rounded-lg border-l-4 p-3 md:p-4 text-[14px] text-muted" style={{ borderColor: 'var(--warn)', background: 'var(--warn-soft)' }}><b className="font-medium text-text">{bloqueadas.length} pendências bloqueadas por fonte externa ({bloqueadas.map((i) => i.id).join(', ')}).</b> Só andam com dado que o estudo não tem: {[...new Set(bloqueadas.map((i) => i.proxima_evidencia.replace(/\.$/, '')))].join('; ')}.</div>}
        <ul className="cartao divide-y divide-border">
          {f3Ativos.map((i) => {
            const st = f3st(i.estado_final);
            return (
              <li key={i.id} className="p-3 md:p-4">
                <div className="flex items-start gap-3">
                  <span className="font-mono text-sm font-semibold w-12 shrink-0 pt-0.5">{i.id}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex flex-wrap items-start gap-x-3 gap-y-1.5"><span className="text-[15px] text-text font-medium leading-snug flex-1 min-w-[14rem]">{i.pergunta}</span><Selo cor={st.cor}>{st.rot}</Selo></div>
                    <p className="mt-1.5 text-[14.5px] text-muted leading-relaxed">{i.resposta_ou_motivo}</p>
                    {i.historico?.map((h) => <div key={h.etapa} className="mt-1.5 text-[13px] text-subtle"><b className="font-medium text-muted">Antes da revisão ({h.etapa}):</b> {h.estado}{i.revisao ? <> · motivo da mudança: {i.revisao}</> : null}</div>)}
                    {i.alcance_em_votos && i.alcance_em_votos !== 'n/a' && <div className="mt-1.5 text-[13px]"><b className="font-medium text-text">Em votos:</b> <span className="text-muted">{i.alcance_em_votos}</span></div>}
                    <details className="mt-1.5 group/q">
                      <summary className="cursor-pointer list-none text-[12.5px] text-subtle hover:text-text"><span className="group-open/q:hidden">detalhe técnico</span><span className="hidden group-open/q:inline">recolher</span></summary>
                      <div className="mt-2 text-[13.5px] text-muted grid gap-1.5">
                        <div><b className="font-medium text-text">Trabalho na Fase 3: </b>{i.trabalho_na_f3}</div>
                        {i.o_que_a_f2_demonstrou && <div><b className="font-medium text-text">O que a Fase 2 já mostrava: </b>{i.o_que_a_f2_demonstrou}</div>}
                        {i.hipoteses_concorrentes && <div><b className="font-medium text-text">Distingue: </b>{i.hipoteses_concorrentes}</div>}
                        {i.criterio_de_encerramento && <div><b className="font-medium text-text">Critério de encerramento: </b>{i.criterio_de_encerramento}</div>}
                        <div><b className="font-medium text-text">Próxima evidência: </b>{i.proxima_evidencia}</div>
                        <div className="text-xs text-subtle">estado no início da Fase 3: {i.estado_inicial_f3} · origem: {i.origem}</div>
                      </div>
                    </details>
                  </div>
                </div>
              </li>
            );
          })}
        </ul>
        {f3Herdados.length > 0 && <details className="mt-3 cartao group/h">
          <summary className="cursor-pointer list-none p-3 md:p-4 text-[14px] font-medium text-text flex items-center gap-2">{f3Herdados.length} perguntas respondidas na Fase 2, não reabertas<span className="ml-auto text-xs text-subtle group-open/h:hidden">abrir</span><span className="ml-auto text-xs text-subtle hidden group-open/h:inline">fechar</span></summary>
          <ul className="divide-y divide-border border-t border-border">
            {f3Herdados.map((i) => (
              <li key={i.id} className="p-3 md:p-4 flex items-start gap-3">
                <span className="font-mono text-sm font-semibold w-12 shrink-0 pt-0.5">{i.id}</span>
                <div className="flex-1 min-w-0"><div className="flex flex-wrap items-start gap-x-3 gap-y-1.5"><span className="text-[14.5px] text-text leading-snug flex-1 min-w-[14rem]">{pergF2(i.id) || i.pergunta}</span><Selo cor={f3st(i.estado_final).cor}>{f3st(i.estado_final).rot}</Selo></div><p className="mt-1 text-[13.5px] text-muted leading-relaxed">{i.resposta_ou_motivo}</p>{i.trabalho_na_f3 !== 'não reaberta' && <p className="mt-1 text-xs text-subtle">{i.trabalho_na_f3}</p>}</div>
              </li>
            ))}
          </ul>
        </details>}
        <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-[13.5px]"><a href="#/docs/fase3" className="text-accent-text underline underline-offset-4">Relatório da Fase 3</a><a href="#/docs/fase3-inventario" className="text-accent-text underline underline-offset-4">Inventário completo</a><a href="#/testes?modulo=H" className="text-accent-text underline underline-offset-4">Testes da Fase 3 (módulo H)</a></div>
      </Sec>}

      {/* detalhe e história, recolhidos */}
      <div className="mt-16 md:mt-20 max-w-[48rem]"><Eyebrow>Detalhe e história</Eyebrow><h2 className="t-h2 mt-2">Como chegamos até aqui</h2><p className="t-lead mt-3 text-[17px]">A revisão, a aprovação da baseline, o que mudou em cada teste e os marcos. Abra o que interessar.</p></div>
      {/* revisão */}
      {rev && <Sec fechado id="revisao" eyebrow={`Revisão ${rev.revisao}`} titulo="A primeira auditoria independente" lead={`${rev.revisor}, ${dataBR(rev.data)}. Alvo: ${rev.alvo}. O relatório foi guardado inteiro; cada achado foi conferido por nós e respondido no registro.`}>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {[['resistiu', 'contestações que o teste resistiu'], ['ajustado', 'ajustadas (método, redação ou alcance)'], ['caiu', 'afirmações que caíram'], ['em_andamento', 'contestações ainda em andamento']].map(([k, r]) => (
            <div key={k} className="cartao p-5 border-t-[3px]" style={{ borderTopColor: `var(--${k === 'resistiu' ? 'ok' : k === 'caiu' ? 'erro' : k === 'ajustado' ? 'warn' : 'text-subtle'})` }}>
              <div className="text-3xl font-semibold tracking-tight">{contaProva(k as Prova['resultado'])}</div><div className="text-[13px] text-muted mt-1">{r}</div>
            </div>
          ))}
        </div>
        <div className="mt-6 flex flex-wrap items-center gap-2">
          <span className="text-[13px] text-muted mr-1">Classificação</span>
          <Chip ativo={!fClass} onClick={() => setFClass('')}>todas · {achados.length}</Chip>
          {Object.keys(CLASSIF).map((k) => <Chip key={k} ativo={fClass === k} onClick={() => setFClass(fClass === k ? '' : k)}>{CLASSIF[k]} · {achados.filter((a) => a.classificacao === k).length}</Chip>)}
        </div>
        <div className="mt-2 flex flex-wrap items-center gap-2">
          <span className="text-[13px] text-muted mr-1">Situação</span>
          <Chip ativo={!fSit} onClick={() => setFSit('')}>todas</Chip>
          {Object.keys(SITU).filter((k) => achados.some((a) => a.situacao === k)).map((k) => <Chip key={k} ativo={fSit === k} onClick={() => setFSit(fSit === k ? '' : k)}>{SITU[k].rot} · {achados.filter((a) => a.situacao === k).length}</Chip>)}
        </div>
        <div className="mt-4 grid gap-3 lg:grid-cols-2">
          {filtrados.map((a) => (
            <article key={a.id} className="cartao p-4 md:p-5">
              <div className="flex flex-wrap items-center gap-2"><span className="font-mono text-sm font-semibold">{a.id}</span><span className="text-xs text-subtle">§{a.secao} · prioridade {PRIO[a.prioridade] || a.prioridade}</span><span className="ml-auto flex gap-1.5 flex-wrap"><Selo cor="var(--text-subtle)">{CLASSIF[a.classificacao] || a.classificacao}</Selo><Selo cor={SITU[a.situacao]?.cor || 'var(--text-subtle)'}>{SITU[a.situacao]?.rot || a.situacao}</Selo></span></div>
              <h3 className="mt-2 text-[15.5px] font-medium text-text leading-snug">{a.titulo}</h3>
              <p className="mt-2 text-[14px] text-muted"><b className="font-medium text-text">O que conferimos:</b> {a.verificacao_interna}</p>
              <p className="mt-1.5 text-[14px] text-muted"><b className="font-medium text-text">Resposta:</b> {a.resposta}</p>
              {a.pendente && <p className="mt-1.5 text-[13.5px] text-subtle"><b className="font-medium">{a.situacao === 'respondido' ? 'Encaminhamento:' : a.situacao === 'adiado_fase2' ? 'Na Fase 2:' : 'Pendente:'}</b> {a.pendente}</p>}
              {a.testes.length > 0 && <div className="mt-3 flex flex-wrap gap-1.5">{a.testes.map((t) => <a key={t} href={`#/testes/${t}`} className="font-mono text-xs h-7 px-2.5 inline-flex items-center rounded-md border border-border hover:border-border-strong">{t}</a>)}</div>}
            </article>
          ))}
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          <a className="inline-flex items-center gap-1.5 min-h-10 py-2 px-4 rounded-full border border-border text-sm font-medium hover:border-border-strong" href={`${lt.github}/blob/main/revisoes/${rev.pasta}/original/RELATORIO.md`} target="_blank" rel="noopener"><FileText size={15} />Relatório original do revisor <ExternalLink size={13} /></a>
          <a className="inline-flex items-center gap-1.5 min-h-10 py-2 px-4 rounded-full border border-border text-sm font-medium hover:border-border-strong" href="#/docs/revisao-r1">Como a revisão foi respondida</a>
        </div>
      </Sec>}
      {/* baseline */}
      <Sec fechado id="baseline" eyebrow="Baseline aprovada" titulo="Como a V1.0 foi aprovada" lead="Aprovada em 28/10/2026, com os seis critérios cumpridos e registrados (rodada 2, tag v1.0). Não houve aprovação automática.">
        <ul className="cartao divide-y divide-border">
          {criterios.map((c) => (
            <li key={c.t} className="p-4 md:p-5 flex gap-3">
              <span className="mt-0.5 w-6 h-6 shrink-0 grid place-items-center rounded-full" style={{ background: 'var(--ok)', color: 'var(--bg)' }}><Check size={14} strokeWidth={3} /></span>
              <div><div className="text-[15px] font-medium text-text">{c.t}</div><div className="text-[13.5px] text-muted mt-0.5">{c.d}</div></div>
            </li>
          ))}
        </ul>
      </Sec>

      {/* comparar */}
      <Sec fechado id="comparar" eyebrow="Comparações" titulo={`${v0?.versao || 'Rodada 1'} → estado atual, teste a teste`} lead="Só os testes que foram contestados ou mudaram. Cada mudança traz a causa; quando há mais de uma causa, a diferença não se atribui a uma só.">
        <div className="flex flex-wrap items-center gap-2 mb-4">
          <span className="text-[13px] text-muted mr-1">Causa</span>
          <Chip ativo={!fCausa} onClick={() => setFCausa('')}>todas</Chip>
          {Object.keys(causas).map((k) => <Chip key={k} ativo={fCausa === k} onClick={() => setFCausa(fCausa === k ? '' : k)}>{CAUSA_ROT[k] || k} · {causas[k]}</Chip>)}
        </div>
        <div className="grid gap-3">
          {mudaram.map((t) => {
            const v = (t.versoes || [])[0];
            const pr = t.provas || [];
            const pior = (['caiu', 'em_andamento', 'em_revisao', 'ajustado', 'inalterado', 'resistiu'] as const).find((r) => pr.some((p) => p.resultado === r));
            return (
              <a key={t.id} href={`#/testes/${t.id}`} className="cartao p-4 md:p-5 grid gap-3 hover:border-border-strong transition-colors">
                <div className="flex flex-wrap items-center gap-2"><span className="font-mono text-sm font-semibold">{t.id}</span><span className="text-[15px] text-text flex-1 min-w-[12rem]">{t.pergunta}</span>{pior && <SeloProva r={pior} />}</div>
                <div className="flex flex-wrap gap-1.5">{[...new Set((t.mudancas || []).map((m) => m.causa))].map((c) => <SeloCausa key={c} c={c} />)}{v && v.classe_evidencia !== t.classe_evidencia && <span className="inline-flex items-center gap-1 text-xs"><SeloClasse classe={v.classe_evidencia} />→<SeloClasse classe={t.classe_evidencia} /></span>}{(t.metodo_versao || 1) > 1 && <span className="text-xs text-subtle self-center">método v1 → v{t.metodo_versao}</span>}</div>
                <div className="grid md:grid-cols-2 gap-3 text-[14px] text-muted">
                  <div className="rounded-lg bg-surface-2/70 p-3"><div className="text-xs text-subtle mb-1">{v?.versao || 'versão anterior'}</div>{v?.resultado || '—'}</div>
                  <div className="rounded-lg bg-surface-2/70 p-3"><div className="text-xs text-subtle mb-1">estado atual</div>{t.evidencia || t.resultado_atual}{t.interpretacao && <span className="block mt-1.5 text-text/80">{t.interpretacao}</span>}</div>
                </div>
              </a>
            );
          })}
        </div>
      </Sec>

      {/* provas */}
      <Sec fechado id="provas" eyebrow="Contestações" titulo="Todas as tentativas de derrubar os testes" lead="Revisão de método, replicação, dado independente, sensibilidade ou revisão externa. O resultado fica no próprio teste e não apaga o que ele dizia antes.">
        <div className="grid gap-2">
          {(['caiu', 'em_andamento', 'em_revisao', 'ajustado', 'inalterado', 'resistiu'] as const).flatMap((r) => provas.filter((p) => p.resultado === r)).map((p, i) => (
            <a key={i} href={`#/testes/${p.id}`} className="cartao p-3.5 md:p-4 flex flex-wrap items-start gap-x-3 gap-y-1.5 hover:border-border-strong">
              <SeloProva r={p.resultado} /><span className="font-mono text-sm font-semibold">{p.id}</span>
              <span className="text-[14px] text-muted flex-1 min-w-[16rem]">{p.descricao}</span>
              <span className="text-xs text-subtle basis-full sm:basis-auto">{p.tipo} · {dataBR(p.data)}</span>
            </a>
          ))}
        </div>
        <Nota className="mt-4">Contagem: {(['resistiu', 'inalterado', 'ajustado', 'caiu', 'em_andamento', 'em_revisao'] as const).filter((r) => contaProva(r)).map((r) => `${contaProva(r)} ${PROVA_ROT[r]}`).join(' · ')}.</Nota>
      </Sec>

      {/* marcos */}
      <Sec fechado id="marcos" eyebrow="Marcos" titulo="O que aconteceu, em ordem" lead="Os principais momentos, incluindo os erros do próprio estudo que foram achados e corrigidos. O registro completo, hora a hora, está no Catálogo.">
        <ol className="relative grid gap-5 pl-7 before:absolute before:left-[9px] before:top-2 before:bottom-2 before:w-px before:bg-border max-w-[52rem]">
          {lt.marcos.map((m, i) => {
            const e = /erro/i.test(m.titulo);
            return (
              <li key={i} className="relative">
                <span className={clsx('absolute -left-7 top-1 w-[19px] h-[19px] rounded-full border-[3px] border-bg')} style={{ background: e ? 'var(--warn)' : /revis/i.test(m.titulo) ? 'var(--ok)' : 'var(--accent)' }} />
                <div className="text-[13px] font-mono text-subtle">{dataBR(m.data)}{m.hora ? ` · ${m.hora}` : ''}</div>
                <div className="text-[16px] font-medium text-text mt-0.5">{m.titulo}</div>
                <p className="text-[14.5px] text-muted mt-0.5 leading-relaxed">{m.texto}</p>
              </li>
            );
          })}
        </ol>
        <div className="mt-6 flex flex-wrap gap-2"><a className="inline-flex items-center gap-1.5 h-10 px-4 rounded-full border border-border text-sm font-medium hover:border-border-strong" href="#/docs/catalogo">Catálogo completo, hora a hora</a><a className="inline-flex items-center gap-1.5 h-10 px-4 rounded-full border border-border text-sm font-medium hover:border-border-strong" href="#/docs/rodadas">Como funcionam versões e revisões</a></div>
      </Sec>
    </div>
  );
}
