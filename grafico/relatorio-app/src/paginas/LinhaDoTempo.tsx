// Evolução da pesquisa: Estado inicial → Revisão → Baseline aprovada → Novas investigações → Comparações → Estado atual.
// Versões congeladas, revisões independentes com achados respondidos, critérios da baseline, perguntas da Fase 2,
// comparação teste a teste com a causa de cada mudança, contestações e marcos.
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
const PRIO: Record<string, string> = { alta: 'alta', media_alta: 'média/alta', media: 'média', informativo: 'informativo', pergunta: 'pergunta' };

const Sec = ({ id, eyebrow, titulo, lead, children }: { id: string; eyebrow: string; titulo: string; lead?: string; children: React.ReactNode }) => (
  <section id={id} className="mt-16 md:mt-20 scroll-mt-20"><div className="max-w-[48rem]"><Eyebrow>{eyebrow}</Eyebrow><h2 className="t-h2 mt-2">{titulo}</h2>{lead && <p className="t-lead mt-3 text-[17px]">{lead}</p>}</div><div className="mt-6">{children}</div></section>
);
const Selo = ({ cor, children }: { cor: string; children: React.ReactNode }) => (
  <span className="inline-flex items-center gap-1.5 h-6 px-2 rounded-full text-xs font-medium border shrink-0" style={{ color: cor, borderColor: cor }}><i className="w-1.5 h-1.5 rounded-full" style={{ background: cor }} />{children}</span>
);
const irPara = (link: string) => (e: React.MouseEvent) => { if (link.startsWith('#') && !link.startsWith('#/')) { e.preventDefault(); document.getElementById(link.slice(1))?.scrollIntoView({ behavior: 'smooth', block: 'start' }); } };

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

  const abertos = achados.filter((a) => a.situacao === 'aberto' || a.situacao === 'em_andamento');
  const criterios = [
    { ok: abertos.length === 0, t: 'Todo achado da R1 respondido, aceito como limite ou adiado para a Fase 2 com justificativa', d: abertos.length ? `faltam: ${abertos.map((a) => a.id).join(', ')}` : 'cumprido' },
    { ok: !achados.some((a) => a.prioridade === 'alta' && a.fase_alvo === 'V1.0' && a.situacao !== 'respondido'), t: 'Ações de prioridade alta com alvo V1.0 concluídas', d: achados.filter((a) => a.prioridade === 'alta' && a.fase_alvo === 'V1.0' && a.situacao !== 'respondido').map((a) => `${a.id}: ${a.pendente}`).join(' ') || 'cumprido' },
    { ok: true, t: 'Verificador passa comparando conjuntos de chaves', d: 'make verificar: todas as seções do Boletim de Urna processadas nos dois turnos' },
    { ok: true, t: 'Conclusão revisada coerente com o registro', d: 'CONCLUSAO.md em revisão, com a tabela de mudanças em relação à rc1' },
    { ok: true, t: 'Proveniência completa', d: 'commit, manifesto de dados, ambiente, sementes e parâmetros em rodadas/rodada-1/proveniencia.json' },
    { ok: false, t: 'Aprovação explícita do responsável pelo estudo', d: 'aguardando; aprovar não significa que os resultados sejam infalíveis, e sim que o levantamento foi documentado e auditado por critérios explícitos' },
  ];
  const v0 = lt.rodadas[0];

  return (
    <div className="container pb-24">
      <header className="pt-10 md:pt-16 max-w-[54rem]">
        <Eyebrow>Evolução da pesquisa</Eyebrow>
        <h1 className="t-h1 mt-3">A pesquisa se corrige sem reescrever o próprio passado</h1>
        <p className="t-lead mt-4 text-[18px]">Cada versão do estudo fica congelada. Revisões independentes tentam derrubá-la, e cada contestação fica registrada no teste que contesta, com o resultado. Assim dá para ver o que concluímos hoje, como chegamos até aqui, o que mudou e por quê.</p>
      </header>

      {/* caminho em 6 etapas */}
      <nav aria-label="Etapas da pesquisa" className="mt-10">
        <ol className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
          {lt.caminho.map((e, i) => {
            const s = ST[e.status] || ST.planejada;
            return (
              <li key={e.id}>
                <a href={e.link} onClick={irPara(e.link)} className="cartao h-full p-4 flex flex-col gap-2 hover:border-border-strong transition-colors" style={{ borderTop: `3px solid ${s.cor}` }}>
                  <div className="flex items-center gap-2 text-[12px]"><span className="w-6 h-6 grid place-items-center rounded-full font-semibold" style={{ background: s.cor, color: 'var(--bg)' }}><s.Ic size={13} strokeWidth={2.8} /></span><span className="font-mono text-subtle">{i + 1} · {e.versao}</span></div>
                  <div className="text-[16px] font-semibold text-text leading-tight">{e.titulo}</div>
                  <div className="text-[13px] font-medium" style={{ color: s.cor }}>{s.rot}</div>
                  <p className="text-[13px] text-muted leading-snug">{e.texto}</p>
                </a>
              </li>
            );
          })}
        </ol>
      </nav>

      {/* fases */}
      <Sec id="fases" eyebrow="Estado inicial" titulo="O levantamento da Fase 1 e o que vem depois" lead="A Fase 1 levantou e validou o que os dados públicos permitem e foi congelada como snapshot preliminar (V1.0-rc1). A baseline só é aprovada depois da revisão.">
        <ol className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {lt.fases.map((f: Fase) => {
            const s = ST[f.status] || ST.planejada;
            return (
              <li key={f.id} className="cartao p-5" style={{ borderTop: `3px solid ${s.cor}` }}>
                <div className="flex items-center gap-2 text-[13px]"><span className="w-7 h-7 grid place-items-center rounded-full" style={{ background: s.cor, color: 'var(--bg)' }}><s.Ic size={15} strokeWidth={2.6} /></span><span className="font-mono text-subtle">{f.id}{f.versao ? ` · ${f.versao}` : ''}</span><span className="ml-auto font-medium" style={{ color: s.cor }}>{s.rot}</span></div>
                <h3 className="t-h3 mt-3">{f.titulo}</h3>
                {(f.inicio || f.fim) && <div className="text-[13px] text-subtle mt-1">{f.inicio ? dataBR(f.inicio) : ''}{f.fim ? ` a ${dataBR(f.fim)}` : ''}</div>}
                <p className="text-[14.5px] text-muted mt-2 leading-relaxed">{f.resumo}</p>
                {f.etapas.length > 0 && <ul className="mt-4 grid gap-2.5">{f.etapas.map((e) => (
                  <li key={e.titulo} className="flex gap-2.5"><span className="mt-1 w-4 h-4 shrink-0 grid place-items-center rounded-full" style={{ background: f.status === 'concluida' ? 'var(--ok)' : 'var(--surface-2)', color: 'var(--bg)' }}>{f.status === 'concluida' && <Check size={11} strokeWidth={3} />}</span><div><div className="text-[14px] font-medium text-text">{e.titulo}</div><div className="text-[13px] text-muted leading-snug mt-0.5">{e.texto}</div></div></li>
                ))}</ul>}
              </li>
            );
          })}
        </ol>
        {v0 && <div className="mt-4 cartao p-5 md:p-6 grid gap-4 lg:grid-cols-[1fr_auto] lg:items-center">
          <div>
            <div className="flex flex-wrap items-baseline gap-2"><span className="text-2xl font-semibold tracking-tight">{v0.versao || `Rodada ${v0.rodada}`}</span><span className="text-[13px] text-subtle">congelada em {dataBR(v0.data)}{v0.commit ? ` · commit ${v0.commit.slice(0, 7)}` : ''}</span></div>
            <p className="text-[14.5px] text-muted mt-1">{v0.estado}</p>
            <div className="mt-3 flex h-3 rounded-full overflow-hidden gap-[2px] max-w-[520px]">{'ABCDEFG'.split('').filter((k) => v0.placar.classes[k]).map((k) => <div key={k} title={`${k}: ${v0.placar.classes[k]}`} style={{ width: `${(100 * v0.placar.classes[k]) / v0.placar.testes}%`, background: CLASSE_COR[k] }} />)}</div>
            <div className="mt-2 text-[13px] text-muted">{N(v0.placar.testes)} testes · {'ABCDEFG'.split('').filter((k) => v0.placar.classes[k]).map((k) => `${k} ${v0.placar.classes[k]}`).join(' · ')} · {v0.arquivos} arquivos com SHA-256</div>
          </div>
          {v0.tag && <div className="flex flex-wrap gap-2">
            <a className="inline-flex items-center gap-1.5 min-h-10 py-2 px-4 rounded-full border border-border text-sm font-medium hover:border-border-strong" href={`${lt.github}/tree/${v0.tag}/rodadas/rodada-${v0.rodada}`} target="_blank" rel="noopener"><GitBranch size={15} />Arquivos congelados <ExternalLink size={13} /></a>
            <a className="inline-flex items-center gap-1.5 min-h-10 py-2 px-4 rounded-full border border-border text-sm font-medium hover:border-border-strong" href={`${lt.github}/blob/${v0.tag}/CONCLUSAO.md`} target="_blank" rel="noopener"><FileText size={15} />Conclusão original <ExternalLink size={13} /></a>
          </div>}
        </div>}
      </Sec>

      {/* revisão */}
      {rev && <Sec id="revisao" eyebrow={`Revisão ${rev.revisao}`} titulo="A primeira auditoria independente" lead={`${rev.revisor}, ${dataBR(rev.data)}. Alvo: ${rev.alvo}. O relatório foi guardado inteiro; cada achado foi conferido por nós e respondido no registro.`}>
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
              {a.pendente && <p className="mt-1.5 text-[13.5px] text-subtle"><b className="font-medium">Pendente:</b> {a.pendente}</p>}
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
      <Sec id="baseline" eyebrow="Baseline aprovada" titulo="O que falta para a V1.0" lead="A rc1 só vira baseline com todos estes critérios cumpridos e registrados. Não há aprovação automática.">
        <ul className="cartao divide-y divide-border">
          {criterios.map((c) => (
            <li key={c.t} className="p-4 md:p-5 flex gap-3">
              <span className="mt-0.5 w-6 h-6 shrink-0 grid place-items-center rounded-full" style={{ background: c.ok ? 'var(--ok)' : 'var(--warn)', color: 'var(--bg)' }}>{c.ok ? <Check size={14} strokeWidth={3} /> : <Clock size={14} strokeWidth={2.6} />}</span>
              <div><div className="text-[15px] font-medium text-text">{c.t}</div><div className="text-[13.5px] text-muted mt-0.5">{c.d}</div></div>
            </li>
          ))}
        </ul>
      </Sec>

      {/* fase 2 */}
      <Sec id="fase2" eyebrow="Novas investigações" titulo="Perguntas da Fase 2, registradas antes dos resultados" lead="Cada pergunta diz qual hipótese concorrente distingue e que afirmação do estudo pode mudar. Perguntas que nascem de um resultado entram como exploratórias.">
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {lt.fase2.map((q) => (
            <article key={q.id} className="cartao p-4 md:p-5">
              <div className="flex items-center gap-2"><span className="font-mono text-sm font-semibold">{q.id}</span><span className="ml-auto"><Selo cor={/confirmat/.test(q.natureza) ? 'var(--accent)' : 'var(--text-subtle)'}>{q.natureza}</Selo></span></div>
              <h3 className="mt-2 text-[15px] font-medium text-text leading-snug">{q.pergunta}</h3>
              <dl className="mt-2 grid gap-1 text-[13.5px] text-muted">
                <div><dt className="inline font-medium text-text">Distingue: </dt><dd className="inline">{q.distingue}</dd></div>
                <div><dt className="inline font-medium text-text">Pode mudar: </dt><dd className="inline">{q.afirmacao}</dd></div>
                <div><dt className="inline font-medium text-text">Menor teste: </dt><dd className="inline">{q.teste}</dd></div>
              </dl>
              <div className="mt-2 text-xs text-subtle">origem: {q.origem}</div>
            </article>
          ))}
        </div>
      </Sec>

      {/* comparar */}
      <Sec id="comparar" eyebrow="Comparações" titulo={`${v0?.versao || 'Rodada 1'} → estado atual, teste a teste`} lead="Só os testes que foram contestados ou mudaram. Cada mudança traz a causa; quando há mais de uma causa, a diferença não se atribui a uma só.">
        <div className="flex flex-wrap items-center gap-2 mb-4">
          <span className="text-[13px] text-muted mr-1">Causa</span>
          <Chip ativo={!fCausa} onClick={() => setFCausa('')}>todas</Chip>
          {Object.keys(causas).map((k) => <Chip key={k} ativo={fCausa === k} onClick={() => setFCausa(fCausa === k ? '' : k)}>{CAUSA_ROT[k] || k} · {causas[k]}</Chip>)}
        </div>
        <div className="grid gap-3">
          {mudaram.map((t) => {
            const v = (t.versoes || [])[0];
            const pr = t.provas || [];
            const pior = (['caiu', 'em_andamento', 'ajustado', 'resistiu'] as const).find((r) => pr.some((p) => p.resultado === r));
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
      <Sec id="provas" eyebrow="Contestações" titulo="Todas as tentativas de derrubar os testes" lead="Revisão de método, replicação, dado independente, sensibilidade ou revisão externa. O resultado fica no próprio teste e não apaga o que ele dizia antes.">
        <div className="grid gap-2">
          {(['caiu', 'em_andamento', 'ajustado', 'resistiu'] as const).flatMap((r) => provas.filter((p) => p.resultado === r)).map((p, i) => (
            <a key={i} href={`#/testes/${p.id}`} className="cartao p-3.5 md:p-4 flex flex-wrap items-start gap-x-3 gap-y-1.5 hover:border-border-strong">
              <SeloProva r={p.resultado} /><span className="font-mono text-sm font-semibold">{p.id}</span>
              <span className="text-[14px] text-muted flex-1 min-w-[16rem]">{p.descricao}</span>
              <span className="text-xs text-subtle basis-full sm:basis-auto">{p.tipo} · {dataBR(p.data)}</span>
            </a>
          ))}
        </div>
        <Nota className="mt-4">Contagem: {(['resistiu', 'ajustado', 'caiu', 'em_andamento'] as const).map((r) => `${contaProva(r)} ${PROVA_ROT[r]}`).join(' · ')}.</Nota>
      </Sec>

      {/* marcos */}
      <Sec id="marcos" eyebrow="Marcos" titulo="O que aconteceu, em ordem" lead="Os principais momentos, incluindo os erros do próprio estudo que foram achados e corrigidos. O registro completo, hora a hora, está no Catálogo.">
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
