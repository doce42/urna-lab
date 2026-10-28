// Linha do tempo: fases do estudo, rodadas congeladas (para comparar hoje × amanhã), estado de cada teste por rodada, provas e marcos.
import { useMemo, useState } from 'react';
import { clsx } from 'clsx';
import { Check, CircleDot, Circle, GitBranch, ExternalLink } from 'lucide-react';
import type { LinhaDoTempo as LT, Registro, Fase } from '@/lib/tipos';
import { useDados } from '@/lib/dados';
import { dataBR, N } from '@/lib/formato';
import { Botao, Eyebrow, SkeletonBloco, Erro, Nota, CLASSE_COR, SeloClasse } from '@/ui/base';
import { SeloProva } from '@/ui/Historico';

const STATUS: Record<Fase['status'], { rot: string; cor: string; Ic: typeof Check }> = {
  concluida: { rot: 'concluída', cor: 'var(--ok)', Ic: Check },
  em_andamento: { rot: 'em andamento', cor: 'var(--accent)', Ic: CircleDot },
  proxima: { rot: 'próxima', cor: 'var(--accent)', Ic: CircleDot },
  planejada: { rot: 'planejada', cor: 'var(--text-subtle)', Ic: Circle },
};

const Sec = ({ id, eyebrow, titulo, lead, children }: { id: string; eyebrow: string; titulo: string; lead?: string; children: React.ReactNode }) => (
  <section id={id} className="mt-16 md:mt-20 scroll-mt-20"><div className="max-w-[46rem]"><Eyebrow>{eyebrow}</Eyebrow><h2 className="t-h2 mt-2">{titulo}</h2>{lead && <p className="t-lead mt-3 text-[17px]">{lead}</p>}</div><div className="mt-6">{children}</div></section>
);

export function LinhaDoTempo({ reg }: { reg: Registro }) {
  const { dados: lt, erro, recarregar } = useDados<LT>('linha-do-tempo');
  const rodadas = lt?.rodadas || [];
  const [ra, setRa] = useState<number | null>(null);
  const [rb, setRb] = useState<number | null>(null);
  const a = ra ?? (rodadas.length > 1 ? rodadas[rodadas.length - 2].rodada : rodadas[0]?.rodada);
  const b = rb ?? rodadas[rodadas.length - 1]?.rodada;
  const ultima = rodadas[rodadas.length - 1];

  // estado de cada teste numa rodada (pelo histórico gravado no registro)
  const naRodada = (n: number | undefined) => reg.testes.map((t) => ({ t, h: (t.historico || []).find((x) => x.rodada === n) })).filter((x) => x.h);
  const mudancas = useMemo(() => {
    if (a == null || b == null || a === b) return [];
    return reg.testes.map((t) => {
      const ha = t.historico?.find((x) => x.rodada === a), hb = t.historico?.find((x) => x.rodada === b);
      if (!hb) return null;
      if (!ha) return { t, ha, hb, campos: ['novo'] };
      const campos = (['classe_evidencia', 'situacao', 'natureza', 'resultado_atual'] as const).filter((k) => ha[k] !== hb[k]);
      return campos.length ? { t, ha, hb, campos: campos as string[] } : null;
    }).filter((x): x is NonNullable<typeof x> => !!x);
  }, [reg, a, b]);
  const provas = useMemo(() => reg.testes.flatMap((t) => (t.provas || []).map((p) => ({ ...p, id: t.id }))).sort((x, y) => y.data.localeCompare(x.data)), [reg]);

  if (erro) return <div className="container py-16"><Erro erro={erro} aoTentar={recarregar} /></div>;
  if (!lt) return <div className="container py-16 grid gap-4"><SkeletonBloco altura={220} /><SkeletonBloco altura={320} /></div>;

  return (
    <div className="container pb-24">
      {/* topo */}
      <header className="pt-10 md:pt-16 max-w-[52rem]">
        <Eyebrow>Linha do tempo</Eyebrow>
        <h1 className="t-h1 mt-3">Como o estudo avança, rodada a rodada</h1>
        <p className="t-lead mt-4 text-[18px]">Cada rodada termina com um retrato congelado de todos os testes e resultados. Assim dá para comparar o que o estudo dizia ontem com o que diz hoje, e ver como cada teste se saiu quando foi posto à prova. Rodada fechada não se reescreve: correções entram na seguinte.</p>
        {ultima && <div className="mt-6 flex flex-wrap gap-2">
          <a href="#fases" className="inline-flex items-center gap-2 h-11 px-5 rounded-full bg-brand text-brand-contrast font-medium text-[15px]">Ver as fases</a>
          {ultima.tag && <a href={`${lt.github}/tree/${ultima.tag}`} target="_blank" rel="noopener" className="inline-flex items-center gap-2 min-h-11 py-2 px-5 rounded-full border border-border font-medium text-[15px] hover:border-border-strong"><GitBranch size={16} />Rodada {ultima.rodada} no GitHub (tag {ultima.tag})</a>}
        </div>}
      </header>

      {/* fases */}
      <Sec id="fases" eyebrow="Fases" titulo="Do levantamento inicial às provas" lead="A rodada 1 levantou e validou tudo o que os dados públicos permitem. As próximas revisam o método e põem cada teste à prova.">
        <ol className="grid gap-4 lg:grid-cols-3">
          {lt.fases.map((f, i) => {
            const s = STATUS[f.status];
            return (
              <li key={f.id} className={clsx('cartao p-5 md:p-6 relative', f.status === 'planejada' && 'opacity-90')} style={{ borderTop: `3px solid ${s.cor}` }}>
                <div className="flex items-center gap-2 text-[13px]">
                  <span className="w-7 h-7 grid place-items-center rounded-full" style={{ background: s.cor, color: 'var(--bg)' }}><s.Ic size={15} strokeWidth={2.6} /></span>
                  <span className="font-mono text-subtle">{f.id} · rodada {f.rodada}{f.rodada === 3 ? '+' : ''}</span>
                  <span className="ml-auto font-medium" style={{ color: s.cor }}>{s.rot}</span>
                </div>
                <h3 className="t-h3 mt-3">{f.titulo}</h3>
                {(f.inicio || f.fim) && <div className="text-[13px] text-subtle mt-1">{f.inicio ? dataBR(f.inicio) : ''}{f.fim ? ` a ${dataBR(f.fim)}` : ''}</div>}
                <p className="text-[15px] text-muted mt-2 leading-relaxed">{f.resumo}</p>
                {f.etapas.length > 0 && (
                  <ul className="mt-4 grid gap-2.5">
                    {f.etapas.map((e) => (
                      <li key={e.titulo} className="flex gap-2.5">
                        <span className="mt-1 w-4 h-4 shrink-0 grid place-items-center rounded-full" style={{ background: f.status === 'concluida' ? 'var(--ok)' : 'var(--surface-2)', color: 'var(--bg)' }}>{f.status === 'concluida' && <Check size={11} strokeWidth={3} />}</span>
                        <div><div className="text-[14px] font-medium text-text">{e.titulo}</div><div className="text-[13.5px] text-muted leading-snug mt-0.5">{e.texto}</div></div>
                      </li>
                    ))}
                  </ul>
                )}
                {i < lt.fases.length - 1 && <span aria-hidden className="hidden lg:block absolute top-9 -right-[13px] w-[22px] h-px bg-border-strong z-10" />}
              </li>
            );
          })}
        </ol>
      </Sec>

      {/* rodadas congeladas */}
      <Sec id="rodadas" eyebrow="Rodadas congeladas" titulo="O retrato de cada rodada" lead="Placar de evidência no momento em que a rodada foi fechada. Os arquivos congelados têm SHA-256 e ficam no repositório.">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {rodadas.map((r) => {
            const tot = r.placar.testes;
            return (
              <div key={r.rodada} className="cartao p-5 md:p-6">
                <div className="flex items-baseline gap-2"><span className="text-3xl font-semibold tracking-tight">Rodada {r.rodada}</span><span className="text-[13px] text-subtle">{dataBR(r.data)}</span></div>
                <div className="text-[15px] text-muted mt-1">{r.titulo}</div>
                <div className="mt-5 text-[13px] text-subtle mb-1.5">{N(tot)} testes por classe de evidência</div>
                <div className="flex h-3.5 rounded-full overflow-hidden gap-[2px]">
                  {'ABCDEFG'.split('').filter((k) => r.placar.classes[k]).map((k) => <div key={k} title={`${k}: ${r.placar.classes[k]} (${reg.classes[k]})`} style={{ width: `${(100 * r.placar.classes[k]) / tot}%`, background: CLASSE_COR[k] }} />)}
                </div>
                <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1.5 text-[13px]">
                  {'ABCDEFG'.split('').filter((k) => r.placar.classes[k]).map((k) => <span key={k} className="inline-flex items-center gap-1.5"><i className="w-2.5 h-2.5 rounded-sm" style={{ background: CLASSE_COR[k] }} /><b className="font-semibold text-text">{r.placar.classes[k]}</b><span className="text-muted">{reg.classes[k]}</span></span>)}
                </div>
                <div className="mt-4 pt-4 border-t border-border grid grid-cols-2 gap-3 text-sm">
                  <div><div className="text-xs text-subtle">confirmatórios</div><div className="font-semibold">{r.placar.natureza['confirmatório'] || 0}</div></div>
                  <div><div className="text-xs text-subtle">exploratórios</div><div className="font-semibold">{r.placar.natureza['exploratório'] || 0}</div></div>
                </div>
                {r.tag && <div className="mt-4 flex flex-wrap gap-2">
                  <a className="inline-flex items-center gap-1.5 h-9 px-3 rounded-full border border-border text-sm font-medium hover:border-border-strong" href={`${lt.github}/tree/${r.tag}/rodadas/rodada-${r.rodada}`} target="_blank" rel="noopener">Arquivos congelados ({r.arquivos}) <ExternalLink size={13} /></a>
                  <a className="inline-flex items-center gap-1.5 h-9 px-3 rounded-full border border-border text-sm font-medium hover:border-border-strong" href={`${lt.github}/blob/${r.tag}/rodadas/rodada-${r.rodada}/CONCLUSAO.md`} target="_blank" rel="noopener">Conclusão da rodada <ExternalLink size={13} /></a>
                </div>}
              </div>
            );
          })}
          {lt.fases.filter((f) => !rodadas.some((r) => r.rodada === f.rodada)).slice(0, 1).map((f) => (
            <div key={f.id} className="rounded-xl border border-dashed border-border-strong p-5 md:p-6 grid content-center">
              <div className="text-3xl font-semibold tracking-tight text-subtle">Rodada {f.rodada}</div>
              <div className="text-[15px] text-muted mt-1">{f.titulo}</div>
              <p className="text-[14px] text-subtle mt-3">Ainda aberta. Quando fechar, o retrato dela aparece aqui e a comparação abaixo mostra o que mudou em cada teste.</p>
            </div>
          ))}
        </div>
      </Sec>

      {/* comparar */}
      <Sec id="comparar" eyebrow="Comparar" titulo={rodadas.length > 1 ? 'O que mudou entre rodadas' : `Estado de cada teste na rodada ${ultima?.rodada ?? 1}`}
        lead={rodadas.length > 1 ? 'Escolha duas rodadas: aparecem só os testes que mudaram de classe, situação, natureza ou resultado.' : 'Esta é a linha de base. Quando a rodada 2 for fechada, esta seção passa a mostrar teste a teste o que mudou. Clique num teste para ver o histórico dele.'}>
        {rodadas.length > 1 ? (
          <>
            <div className="flex flex-wrap items-center gap-2 mb-4">
              <span className="text-[13px] text-muted">De</span>{rodadas.map((r) => <Botao key={'a' + r.rodada} tamanho="sm" variante={a === r.rodada ? 'primario' : 'secundario'} onClick={() => setRa(r.rodada)}>Rodada {r.rodada}</Botao>)}
              <span className="text-[13px] text-muted ml-2">para</span>{rodadas.map((r) => <Botao key={'b' + r.rodada} tamanho="sm" variante={b === r.rodada ? 'primario' : 'secundario'} onClick={() => setRb(r.rodada)}>Rodada {r.rodada}</Botao>)}
            </div>
            {mudancas.length ? (
              <div className="grid gap-3">{mudancas.map(({ t, ha, hb, campos }) => (
                <a key={t.id} href={`#/testes/${t.id}`} className="cartao p-4 md:p-5 grid gap-2 hover:border-border-strong transition-colors">
                  <div className="flex flex-wrap items-center gap-2"><span className="font-mono text-sm font-semibold">{t.id}</span><span className="text-[15px] text-text">{t.pergunta}</span></div>
                  <div className="flex flex-wrap items-center gap-2 text-[13px]">{ha ? <SeloClasse classe={ha.classe_evidencia} /> : <span className="text-subtle">novo</span>}<span className="text-subtle">→</span><SeloClasse classe={hb.classe_evidencia} /><span className="text-subtle">mudou: {campos.join(', ').replace('classe_evidencia', 'classe').replace('resultado_atual', 'resultado').replace('situacao', 'situação')}</span></div>
                  <div className="grid md:grid-cols-2 gap-3 text-[14px] text-muted">
                    <div className="rounded-lg bg-surface-2/70 p-3"><div className="text-xs text-subtle mb-1">rodada {a}</div>{ha?.resultado_atual || '—'}</div>
                    <div className="rounded-lg bg-surface-2/70 p-3"><div className="text-xs text-subtle mb-1">rodada {b}</div>{hb.resultado_atual}</div>
                  </div>
                </a>))}
              </div>
            ) : <Nota>Nenhum teste mudou entre as rodadas {a} e {b}.</Nota>}
          </>
        ) : (
          <div className="cartao p-4 md:p-6">
            <div className="grid gap-2 grid-cols-[repeat(auto-fill,minmax(150px,1fr))]">
              {naRodada(ultima?.rodada).map(({ t, h }) => (
                <a key={t.id} href={`#/testes/${t.id}`} title={`${t.id}: ${t.pergunta}`} className="flex items-center gap-2.5 min-h-11 px-3 py-2 rounded-lg border border-border hover:border-border-strong transition-colors">
                  <span className="w-2.5 h-8 rounded-full shrink-0" style={{ background: CLASSE_COR[h!.classe_evidencia] }} />
                  <span className="min-w-0"><span className="block font-mono text-[13px] font-semibold">{t.id}</span><span className="block text-xs text-muted truncate">{t.pergunta}</span></span>
                </a>
              ))}
            </div>
            <div className="mt-4 flex flex-wrap gap-x-4 gap-y-1.5 text-[13px]">{'ABCDEFG'.split('').filter((k) => ultima?.placar.classes[k]).map((k) => <span key={k} className="inline-flex items-center gap-1.5"><i className="w-2.5 h-2.5 rounded-sm" style={{ background: CLASSE_COR[k] }} />{k}: {reg.classes[k]}</span>)}</div>
          </div>
        )}
      </Sec>

      {/* provas */}
      <Sec id="provas" eyebrow="Provas" titulo="Cada teste posto à prova" lead="Revisão de método, replicação, dado independente, sensibilidade ou contestação externa. O resultado fica no próprio teste e não apaga o que ele dizia antes.">
        {provas.length ? (
          <div className="grid gap-3">{provas.map((p, i) => (
            <a key={i} href={`#/testes/${p.id}`} className="cartao p-4 flex flex-wrap items-center gap-3 hover:border-border-strong"><SeloProva r={p.resultado} /><span className="font-mono text-sm font-semibold">{p.id}</span><span className="font-medium">{p.tipo}</span><span className="text-[14px] text-muted flex-1 min-w-[14rem]">{p.descricao}</span><span className="text-[13px] text-subtle">rodada {p.rodada} · {dataBR(p.data)}</span></a>))}
          </div>
        ) : (
          <div className="cartao p-5 md:p-6 grid gap-4 md:grid-cols-[1fr_auto] md:items-center">
            <p className="text-[15px] text-muted">Nenhum teste foi posto à prova ainda: isso começa na fase 2 (double check da metodologia). Cada prova registrada aparecerá aqui e na gaveta do teste.</p>
            <div className="flex flex-wrap gap-2"><SeloProva r="resistiu" /><SeloProva r="ajustado" /><SeloProva r="caiu" /><SeloProva r="em_andamento" /></div>
          </div>
        )}
      </Sec>

      {/* marcos */}
      <Sec id="marcos" eyebrow="Marcos" titulo="O que aconteceu, em ordem" lead="Os principais momentos da rodada 1, incluindo os erros do próprio estudo que foram achados e corrigidos. O registro completo, hora a hora, está no Catálogo.">
        <ol className="relative grid gap-5 pl-7 before:absolute before:left-[9px] before:top-2 before:bottom-2 before:w-px before:bg-border max-w-[52rem]">
          {lt.marcos.map((m, i) => {
            const erro = /erro/i.test(m.titulo);
            return (
              <li key={i} className="relative">
                <span className="absolute -left-7 top-1 w-[19px] h-[19px] rounded-full border-[3px] border-bg" style={{ background: erro ? 'var(--warn)' : i === lt.marcos.length - 1 ? 'var(--ok)' : 'var(--accent)' }} />
                <div className="text-[13px] font-mono text-subtle">{dataBR(m.data)}{m.hora ? ` · ${m.hora}` : ''}</div>
                <div className="text-[16px] font-medium text-text mt-0.5">{m.titulo}</div>
                <p className="text-[14.5px] text-muted mt-0.5 leading-relaxed">{m.texto}</p>
              </li>
            );
          })}
        </ol>
        <div className="mt-6"><a className="inline-flex items-center gap-1.5 h-10 px-4 rounded-full border border-border text-sm font-medium hover:border-border-strong" href="#/docs/catalogo">Catálogo completo, hora a hora</a> <a className="inline-flex items-center gap-1.5 h-10 px-4 rounded-full border border-border text-sm font-medium hover:border-border-strong" href="#/docs/rodadas">Como funcionam as rodadas</a></div>
      </Sec>
    </div>
  );
}
