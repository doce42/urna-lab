// Visualização de cada teste: recebe o contexto (dados do relatório + registro) e devolve "como ler" + o gráfico.
// Todos os números vêm dos JSON gerados no build; nada é escrito à mão.
import type { ReactNode } from 'react';
import { N, P, SG, num, nice } from '@/lib/formato';
import { esc } from '@/ui/Dica';
import { COR, Tabela } from '@/graficos/comum';
import { Barras, Pontos, Histograma, Coberturas, Figuras, Igualdade, Dumbbell, FaixaPontos, Quadrados, Dupla, Processando, type LinhaBarras, type LinhaPontos } from '@/graficos/primitivos';
import { Linhas } from '@/graficos/Linhas';
import type { Teste, TestesDados, Registro, LogResumo } from '@/lib/tipos';

export type Ctx = { d: TestesDados; t: Teste; reg: Registro; nv: Record<string, any>; bt22: any; bt26: any };
export type Viz = { ler: string; el: ReactNode } | null;
const T1 = COR.ref, T2 = COR.s2026, LULA = COR.lula, ADV = COR.adv, AVISO = COR.aviso, RUIM = COR.erro;
const anoBar = (a: string, b: { v: number | null; txt: string; dica?: string }) => ({ nome: a, cor: a === '2022' ? T1 : T2, ...b });

function cobertura(c: Ctx, itens: [string, (r: LogResumo) => [number, number] | number[] | null | undefined | false | 0][], titulo: string) {
  const rows: { l: string; ok: number; tot: number; nome: string; cor: string }[] = [];
  itens.forEach(([l, f]) => (['t1', 't2'] as const).forEach((k) => { const r = c.d.log_resumo[k]; const par = r && f(r); if (!par) return; const [ok, tot] = par as number[]; rows.push({ l, ok, tot, nome: k === 't1' ? '1º turno' : '2º turno', cor: k === 't1' ? T1 : T2 }); }));
  return rows.length ? <Coberturas itens={rows} titulo={titulo} /> : null;
}
function intervalos(c: Ctx, tit: string): Viz {
  const t = c.t.resultado_atual, re = /([+−-]\d[\d,]*)(?:\s*z)?\s*\[([+−-]?[\d,]+);\s*([+−-]?[\d,]+)\]/g, ms = [...t.matchAll(re)];
  const mde = (t.match(/MDE ([\d,]+)/) || [])[1];
  if (!ms.length) return null;
  const vals = ms.flatMap((m) => [num(m[2]), num(m[3])]); const lim = Math.max(Math.abs(Math.min(...vals)), Math.abs(Math.max(...vals)), mde ? num(mde) : 0) * 1.25;
  const nomes = ['2026', '2022'];
  return { ler: 'O ponto é a estimativa e a linha, o intervalo de 95%. Perto de zero (e dentro da faixa cobre do menor efeito detectável) = sem relação.',
    el: <Pontos min={-lim} max={lim} fmt={(v) => SG(v, 3).replace(/,?0+$/, '') || '0'} refs={[{ v: 0, rot: '0', solido: true }]} faixa={mde ? [-num(mde), num(mde), 'menor efeito detectável'] : null} titulo={tit}
      linhas={ms.slice(0, 2).map((m, i) => ({ l: nomes[i], s: [{ nome: nomes[i], cor: i ? T1 : T2, v: num(m[1]), lo: num(m[2]), hi: num(m[3]) }] }))} /> };
}
function sensib(c: Ctx) {
  const sn = c.nv.sensibilidade_2026, sb = c.nv.sensibilidade_2022;
  const tab = (x: any, ano: string) => x && x.combinacoes ? <div key={ano} className="mt-2"><div className="text-xs font-mono uppercase tracking-wider text-muted mb-1">{ano}</div><div className="rolavel border border-border rounded-lg"><Tabela cab={['mín. válidos', 'nível', 'escala', '>5 pró-Lula', '>5 pró-advers.', 'Spearman T03']} linhas={x.combinacoes.map((k: any) => [k.minimo_validos ?? '', k.nivel ?? '', k.escala ?? '', k.acima_5_lula ?? '—', k.acima_5_adversario ?? '—', k.T03_spearman != null ? SG(k.T03_spearman, 4) : '—'])} /></div></div> : null;
  return (
    <details className="mt-3 group">
      <summary className="cursor-pointer text-[13px] font-medium text-accent-text inline-flex items-center gap-1 h-9 list-none [&::-webkit-details-marker]:hidden"><span className="transition-transform group-open:rotate-90 inline-block">▸</span> Sensibilidade: o padrão muda com a escolha do método?</summary>
      {sn || sb ? <>{tab(sn, '2026')}{tab(sb, '2022')}</> : <Processando msg="Sensibilidade em processamento" sub="Tabela por mínimo de válidos × nível × escala, ainda não gerada." />}
    </details>
  );
}
const NV = (c: Ctx) => c.nv.logs_2t || c.nv.logs_1t;
const TIPOS: Record<string, string> = { a_log_x_comparecimento: 'Votos no log ≠ comparecimento', b_confirmacoes_x_total: 'Confirmações ≠ total do boletim', c_certificado_x_log: 'Certificado ≠ urna do log', d_fora_do_bu: 'Fora do boletim publicado' };
const EXPL: Record<string, string> = { E1: 'E1 contingência reaproveitada', E2: 'E2 CEFT (RED/correspondência alterada)', E3: 'E3 urna substituída', E4: 'E4 confirmação sem voto computado', E5: 'E5 queda de energia', D1: 'D1 arquivo não publicado' };
const NIV: Record<string, string> = { local: 'Local de votação', zona: 'Zona', mun: 'Município', SG_UF: 'Estado' };

export const VIZ: Record<string, (c: Ctx) => Viz> = {
  T01: (c) => { const t = c.d.totais_2, v = t.v13 + t.v22; return { ler: 'Os dois totais oficiais devem ser idênticos: a soma do Boletim de Urna e a soma da votação por seção, no 2º turno, votos válidos.',
    el: <Igualdade a={N(v)} ta="Boletim de Urna (soma, 2º turno, válidos)" b={N(v)} tb="Votação por seção (soma, 2º turno, válidos)" iguais titulo="Totais do 2º turno nas duas fontes oficiais" /> }; },
  T14: (c) => ({ ler: 'Cada medidor é a fração de urnas em que a conta fecha. 100% = todas; o número à direita diz quantas faltam.',
    el: cobertura(c, [['Votos no log = comparecimento do boletim', (r) => [r.log_igual_comparecimento, r.urnas]], ['Confirmações + nulos por suspensão = total do boletim impresso', (r) => r.urnas_com_imgbu && [r.confirmacoes_igual_total, r.urnas_com_imgbu]]], 'Urnas em que a conta fecha') }),
  T15: (c) => ({ ler: 'Duas conferências do boletim impresso (imagem): o arquivo é o que a urna assinou, e a assinatura é válida.',
    el: cobertura(c, [['Imagem do boletim: assinatura válida', (r) => r.assin_ok_imgbu], ['Imagem do boletim: hash = o assinado', (r) => r.hash_ok_imgbu]], 'Boletim impresso nas urnas com o arquivo') }),
  T16: (c) => ({ ler: 'Medidor cheio = assinatura válida em todas as urnas que têm o arquivo. Os arquivos ausentes (exterior, seções sem urna eletrônica) não entram no denominador.',
    el: cobertura(c, [['Lista de arquivos: assinatura válida', (r) => r.assin_lista_ok != null && [r.assin_lista_ok, r.assin_ok_bu ? r.assin_ok_bu[1] : r.urnas]], ['Boletim (bu): assinatura', (r) => r.assin_ok_bu], ['RDV: assinatura', (r) => r.assin_ok_rdv], ['Log: assinatura', (r) => r.assin_ok_log], ['Imagem do boletim: assinatura', (r) => r.assin_ok_imgbu]], 'Assinatura digital válida, por arquivo') }),
  T17: (c) => ({ ler: 'O RDV (voto a voto, embaralhado) é recontado e comparado com o boletim publicado. Medidor cheio = todas as urnas iguais.',
    el: cobertura(c, [['Recontagem pelo RDV = boletim publicado', (r) => r.urnas_com_rdv && [r.rdv_igual_boletim, r.urnas_com_rdv]]], 'Recontagem do RDV') }),
  T16c: (c) => { const m = c.t.resultado_atual.match(/(\d+)\/(\d+) legítimas.*?(\d+) em todos os (\d+) controles/); return { ler: 'Antes de confiar no verificador, testamos o próprio verificador: assinaturas legítimas devem passar e falsificações conhecidas devem ser rejeitadas.',
    el: m ? <Figuras titulo="Teste do verificador de assinatura" itens={[{ n: `${m[1]} de ${m[2]}`, r: 'assinaturas legítimas aceitas', estado: +m[1] === +m[2] ? 'ok' : 'aviso' }, { n: `${m[3]} de ${m[4]}`, r: 'falsificações aceitas (controles negativos)', estado: +m[3] === 0 ? 'ok' : 'ruim' }]} /> : null }; },
  T24: (c) => ({ ler: 'Fração das urnas em que a seção teve duas urnas votando (substituição registrada no log). Esperado: poucas, com explicação operacional.',
    el: <Figuras titulo="Urnas substituídas no meio do dia" itens={(['t1', 't2'] as const).filter((k) => c.d.log_resumo[k]?.urnas_substituidas != null).map((k) => { const r = c.d.log_resumo[k], f = r.urnas_substituidas / r.urnas; return { n: P(100 * f, 2) + '%', r: `${k === 't1' ? '1º turno' : '2º turno'}: ${N(r.urnas_substituidas)} de ${N(r.urnas)} urnas (1 em cada ${N(1 / f)})`, dica: `${N(r.urnas_substituidas)} urnas substituídas em ${N(r.urnas)}` }; })} /> }),
  T32: (c) => { const m = c.t.resultado_atual.match(/(\d+)\/(\d+) votos iguais/); return { ler: 'Soma das urnas contra o total oficial divulgado. Deve ser igual.',
    el: m ? <Coberturas titulo="Soma das urnas × total oficial" itens={[{ l: 'Votos conferidos iguais ao total oficial', ok: +m[1], tot: +m[2], cor: T2 }]} /> : null }; },
  T02: (c) => ({ ler: 'Quanto mais perto de zero, mais a seção virou como as vizinhas. As barras âmbar são as caudas (além de 5 desvios): onde procuraríamos seções diferentes. A altura usa escala de raiz quadrada para as caudas, minúsculas, aparecerem.',
    el: <>{<Histograma z={c.d.z_hist} titulo={`Seções por distância do padrão (${N(c.d.z_hist.n)} seções)`} />}
      {c.d.z_hist.acima5_lula != null && <div className="mt-3"><Figuras itens={[{ n: N(c.d.z_hist.acima5_lula + c.d.z_hist.acima5_flavio), r: `seções além de 5 desvios, de ${N(c.d.z_hist.n)}`, estado: 'aviso' }, { n: N(c.d.z_hist.acima5_lula), r: 'na cauda pró-Lula', dica: 'Seções além de +5 desvios a favor de Lula' }, { n: N(c.d.z_hist.acima5_flavio), r: 'na cauda pró-adversário', dica: 'Seções além de 5 desvios a favor do adversário' }]} /></div>}
      {sensib(c)}</> }),
  T03: (c) => intervalos(c, 'Correlação entre a virada e a hora de chegada ao TSE'),
  T04: (c) => intervalos(c, 'Diferença de z: urnas trocadas × outras'),
  T05: (c) => ({ ler: 'Cada ponto é um p-valor. A linha tracejada (0,05) é a fronteira usual: pontos à direita dela são compatíveis com o acaso; a zona sombreada à esquerda seria o sinal de alerta.',
    el: <Pontos min={0} max={1} fmt={(v) => P(v, 2)} refs={[{ v: 0.05, rot: 'p = 0,05' }]} zonas={[[0, 0.05, '']]} titulo="Último dígito uniforme? p-valor por candidato e turno"
      linhas={[['1t_v13', '1º turno, Lula'], ['1t_v22', '1º turno, adversário'], ['2t_v13', '2º turno, Lula'], ['2t_v22', '2º turno, adversário']].map(([k, l]) => ({ l, s: [{ nome: '2026', cor: T2, v: c.bt26.T05[k] }, ...(c.bt22 ? [{ nome: '2022', cor: T1, v: c.bt22.T05[k] }] : [])] }))} /> }),
  T07: (c) => ({ ler: 'Contagem de seções com comparecimento alto e voto quase unânime (assinatura de enchimento). Comparamos com 2022.',
    el: <Barras titulo="Seções com comparecimento ≥ 95% e ≥ 90% para um candidato" nota={`Seções acima de 100%: ${c.bt26.T07['2t_acima_100pct']} (2026)`}
      linhas={['2022', '2026'].map((a) => { const b = a === '2022' ? c.bt22 : c.bt26; if (!b) return null; return { l: `${a}, 2º turno`, bars: [{ nome: 'quase unânime para Lula', cor: LULA, v: b.T07['2t_v13'], txt: N(b.T07['2t_v13']) }, { nome: 'quase unânime para o adversário', cor: ADV, v: b.T07['2t_v22'], txt: N(b.T07['2t_v22']) }] }; }).filter(Boolean) as LinhaBarras[]} /> }),
  T09: (c) => { const m = c.t.resultado_atual.match(/virada \+?([\d,]+) x \+?([\d,]+) pp/); return { ler: 'Compara a virada das seções que votaram até o horário normal com a das seções prorrogadas (fila). Barras iguais = votaram igual.',
    el: m ? <Barras titulo="Virada média entre os turnos (pontos percentuais)" nota={`Diferença: ${SG(num(m[1]) - num(m[2]), 2)} pp`} linhas={[{ l: 'Virada nas seções prorrogadas', bars: [{ cor: T2, v: num(m[1]), txt: '+' + m[1] + ' pp' }] }, { l: 'Virada nas demais seções', bars: [{ cor: T1, v: num(m[2]), txt: '+' + m[2] + ' pp' }] }]} /> : null }; },
  T10: (c) => { const k = c.d.curva; return { ler: 'A linha real deve acompanhar a prevista. Se um lote de urnas votasse fora do próprio histórico, a real se descolaria. Passe o mouse para ler os três valores a cada minuto.',
    el: <div className="grid gap-5">
      <Linhas titulo="Lula, % acumulado dos válidos (2º turno) por minuto de chegada" x={k.hora} fmt={(v) => P(v) + '%'} tabelaPasso={15}
        series={[{ nome: 'Lula, real', cor: LULA, valores: k.real, largura: 2.4 }, { nome: 'Previsto: 1º turno + virada do município', cor: T2, valores: k.prev_mun, traco: '6 4' }, { nome: 'Previsto: 1º turno + virada do estado', cor: T1, valores: k.prev_uf, traco: '2 3' }]} />
      <Pontos min={0} max={0.45} fmt={(v) => P(v, 2)} titulo="Maior desvio real − previsto (pontos percentuais)" linhas={[['max_desvio_mun_pp', 'Pelo município'], ['max_desvio_estado_pp', 'Pelo estado']].map(([kk, l]) => ({ l, s: [{ nome: '2026', cor: T2, v: c.bt26.T10[kk] }, ...(c.bt22 ? [{ nome: '2022', cor: T1, v: c.bt22.T10[kk] }] : [])] }))} />
    </div> }; },
  T11: (c) => { const ls = ['2022', '2026'].map((a) => { const b = a === '2022' ? c.bt22 : c.bt26; if (!b) return null; const q = b.T11; return { l: a, s: [{ nome: 'real', cor: T2, v: q.real, rot: String(q.real) }, { nome: 'simulada: média ± 2 desvios', cor: T1, lo: q.simulado_media - 2 * q.simulado_dp, hi: q.simulado_media + 2 * q.simulado_dp, v: q.simulado_media, dica: `Simulada: média ${P(q.simulado_media, 2)}, desvio ${P(q.simulado_dp, 2)}` }] }; }).filter(Boolean) as LinhaPontos[];
    const vals = ls.flatMap((l) => l.s.flatMap((s) => [s.v, s.lo, s.hi])).filter((v): v is number => v != null); const mx = nice(Math.max(...vals) * 1.15);
    return { ler: 'Contamos as mudanças de direção da curva. O ponto "real" deve cair dentro da faixa "simulada" (o que seria esperado só pelo acaso).', el: <Pontos min={0} max={mx} fmt={(v) => P(v, 0)} titulo="Mudanças de direção da curva: real × simulada" linhas={ls} /> }; },
  T12: (c) => { const b = c.d.biometria, a = b['sem controles'], z = b['com perfil do eleitorado']; return { ler: 'O t mede a força da associação; |t| menor que 2 = nenhuma associação distinguível do acaso. Ao controlar pela idade, a associação some.',
    el: <Pontos min={-16} max={4} fmt={(v) => P(v, 0)} refs={[{ v: 0, rot: '0', solido: true }]} faixa={[-2, 2, 'sem efeito (|t|<2)']} titulo="Liberação sem biometria × virada: estatística t"
      linhas={[{ l: 'Sem controles', s: [{ nome: 't', cor: AVISO, v: a.t, rot: P(a.t, 1) }] }, { l: 'Com perfil do eleitorado', s: [{ nome: 't', cor: T2, v: z.t, rot: P(z.t, 1) }] }]} /> }; },
  T13: (c) => { const ls = c.d.poder.linhas, gs = [...new Set(ls.map((l) => l.grupo))]; return { ler: 'Cada quadrado é um cenário de fraude sintética injetada nos dados reais. Cobre = pelo menos um teste detectou; cinza = passou batido. Mostra o poder: o que os testes conseguem ver. Toque ou passe o mouse para ver o cenário.',
    el: <Quadrados titulo="Cenários de fraude simulada: detectados ou não" nota={`Margem real do 2º turno: ${N(c.d.poder.margem_real_votos)} votos.`} grupos={gs.map((g) => ({ nome: g, itens: ls.filter((l) => l.grupo === g).map((l) => ({ on: l.algum, dica: `<b>${esc(l.cenario)}</b><br>${N(l.votos)} votos mexidos (${P(l.pct_validos)}% dos válidos)<br>${l.algum ? 'Detectada' : 'Passou batido'}` })) }))} /> }; },
  T19: (c) => ({ ler: 'A mesma bateria de testes, com o mesmo código, em 2022. Se 2026 se parece com 2022, o padrão é do sistema e do eleitorado, não de 2026.',
    el: <Barras titulo="Exemplo: caudas do teste T02 nos dois anos" linhas={['2022', '2026'].map((a) => { const b = a === '2022' ? c.bt22 : c.bt26; return b && { l: `${a} (${N(b.secoes)} seções)`, bars: [{ nome: 'seções além de 5 desvios, pró-Lula', cor: LULA, v: b.T02.acima5_lula, txt: String(b.T02.acima5_lula) }, { nome: 'além de 5 desvios, pró-adversário', cor: ADV, v: b.T02.acima5_outro, txt: String(b.T02.acima5_outro) }] }; }).filter(Boolean) as LinhaBarras[]} /> }),
  T21: (c) => ({ ler: 'z é a distância entre o observado e o esperado em desvios. Dentro da faixa cobre (|z| < 2) não há excesso de percentuais redondos.',
    el: <Pontos min={-4} max={4} fmt={(v) => P(v, 0)} refs={[{ v: 0, rot: '', solido: true }]} faixa={[-2, 2, '|z| < 2']} titulo="Percentuais inteiros: z observado − esperado"
      linhas={[['2t_lula', '2º turno, Lula'], ['2t_adversario', '2º turno, adversário'], ['2t_comparecimento', '2º turno, comparecimento'], ['1t_lula', '1º turno, Lula']].filter(([k]) => c.bt26.T21[k]).map(([k, l]) => ({ l, s: [{ nome: '2026', cor: T2, v: c.bt26.T21[k].z }, ...(c.bt22?.T21[k] ? [{ nome: '2022', cor: T1, v: c.bt22.T21[k].z }] : [])] }))} /> }),
  T22: (c) => ({ ler: 'Correlação entre comparecimento e voto dentro do município. Fraude incremental faria o favorecido crescer onde o comparecimento infla (valor positivo para ele).',
    el: <Pontos min={-0.2} max={0.2} fmt={(v) => P(v, 2)} refs={[{ v: 0, rot: '', solido: true }]} titulo="Correlação comparecimento × voto (2º turno)"
      linhas={[['2t_lula', 'Lula'], ['2t_adversario', 'Adversário']].map(([k, l]) => ({ l, s: [{ nome: '2026', cor: T2, v: c.bt26.T22[k] }, ...(c.bt22 ? [{ nome: '2022', cor: T1, v: c.bt22.T22[k] }] : [])] }))} /> }),
  T23: (c) => { const a = c.nv.ml_2026, b = c.nv.ml_2022;
    if (!a) { const m = c.t.resultado_atual.match(/reais marcadas ([\d,]+)% \(2022: ([\d,]+)%\) contra ([\d,]+)% esperado/);
      return { ler: 'Fração de seções reais marcadas pelo classificador, contra o que se esperaria sem fraude.', el: m ? <Barras titulo="Classificador com fraude sintética" refs={[{ v: num(m[3]), rot: `esperado sem fraude: ${m[3]}%` }]} linhas={[{ l: 'Marcadas, 2026', bars: [{ cor: T2, v: num(m[1]), txt: m[1] + '%' }] }, { l: 'Marcadas, 2022', bars: [{ cor: T1, v: num(m[2]), txt: m[2] + '%' }] }]} /> : null }; }
    const cen = Object.keys(a.poder_por_cenario);
    return { ler: 'Primeiro bloco: poder do classificador em fraudes injetadas (quanto maior, melhor ele enxerga). Segundo: fração de seções reais marcadas, comparada com o esperado sem fraude (linha tracejada). Marcar bem menos que o esperado no real é o resultado de um teste conservador.',
      el: <div className="grid gap-5">
        <Barras titulo="Poder por cenário de fraude sintética (% detectado)" max={100} linhas={cen.map((k) => ({ l: esc(k), bars: [anoBar('2026', { v: 100 * a.poder_por_cenario[k], txt: P(100 * a.poder_por_cenario[k], 0) + '%' }), ...(b && b.poder_por_cenario[k] != null ? [anoBar('2022', { v: 100 * b.poder_por_cenario[k], txt: P(100 * b.poder_por_cenario[k], 0) + '%' })] : [])] }))} />
        <Barras titulo="Fração de seções reais marcadas" refs={[{ v: 100 * a.reais.esperado_sem_fraude, rot: `esperado sem fraude: ${P(100 * a.reais.esperado_sem_fraude, 2)}%` }]} linhas={[{ l: 'Seções reais marcadas', bars: [anoBar('2026', { v: 100 * a.reais.fracao_marcada, txt: P(100 * a.reais.fracao_marcada, 2) + '%', dica: `<b>${P(100 * a.reais.fracao_marcada, 2)}%</b><br>${N(a.reais.marcadas)} de ${N(a.reais.secoes_avaliadas)} seções (2026)` }), ...(b ? [anoBar('2022', { v: 100 * b.reais.fracao_marcada, txt: P(100 * b.reais.fracao_marcada, 2) + '%', dica: `<b>${P(100 * b.reais.fracao_marcada, 2)}%</b><br>${N(b.reais.marcadas)} de ${N(b.reais.secoes_avaliadas)} seções (2022)` })] : [])] }]} />
      </div> }; },
  T25: (c) => { const m = c.t.resultado_atual.match(/curtose ([\d,]+) x ([\d,]+) \(2022\)/); return { ler: 'A curtose descreve o quão pesadas são as caudas da distribuição. 2026 e 2022 devem ser parecidas.',
    el: m ? <Barras titulo="Impressão digital: curtose" linhas={[{ l: 'Curtose, 2026', bars: [{ cor: T2, v: num(m[1]), txt: m[1] }] }, { l: 'Curtose, 2022', bars: [{ cor: T1, v: num(m[2]), txt: m[2] }] }]} /> : null }; },
  T27: (c) => { const m = c.t.resultado_atual.match(/p ([\d,]+)–([\d,]+)/); return { ler: 'Faixa dos p-valores dos testes de último dígito para brancos, nulos e comparecimento. Tudo à direita de 0,05 é compatível com o acaso.',
    el: m ? <Pontos min={0} max={1} fmt={(v) => P(v, 2)} refs={[{ v: 0.05, rot: 'p = 0,05' }]} zonas={[[0, 0.05, '']]} titulo="Dígitos de branco, nulo e comparecimento" linhas={[{ l: 'Faixa de p observada', s: [{ nome: 'p', cor: T2, lo: num(m[1]), hi: num(m[2]), dica: `p de ${m[1]} a ${m[2]}` }] }]} /> : null }; },
  C06b: (c) => { const m = c.t.resultado_atual.match(/F→L entre ([\d.,]+) e ([\d.,]+) mi; L→F entre ([\d.,]+) e ([\d.,]+) mi/); return { ler: 'Faixa de valores compatíveis com os dados (não é estimativa de um número só). Uma faixa tão larga significa que os dados não identificam a troca direta.',
    el: m ? <Pontos min={0} max={45} fmt={(v) => P(v, 0) + ' mi'} titulo="Eleitores que trocaram diretamente de finalista (faixa possível)" linhas={[{ l: 'Flávio → Lula', s: [{ nome: 'faixa', cor: LULA, lo: num(m[1]) / 1000, hi: num(m[2]), dica: `de ${m[1]} mil a ${m[2]} milhões` }] }, { l: 'Lula → Flávio', s: [{ nome: 'faixa', cor: ADV, lo: num(m[3]) / 1000, hi: num(m[4]), dica: `de ${m[3]} mil a ${m[4]} milhões` }] }]} /> : null }; },
  T28: (c) => { const L = NV(c); const q = L && L.T28; if (!q) return { ler: 'Compara o fim do dia com o resto.', el: <Processando msg="T28 em processamento" /> };
    const z = q.z28_percentis || {}, zs = Object.values(z) as number[];
    return { ler: 'Se houvesse rajada de habilitações sem biometria no fim do dia, a barra dos últimos 30 minutos seria bem maior que a do resto do dia. Abaixo, a distribuição do z de cada urna por percentil: concentrada perto de zero = sem rajada.',
      el: <div className="grid gap-5">
        <Barras titulo="Taxa sem biometria (%)" linhas={[{ l: 'Habilitações sem biometria', bars: [{ nome: 'últimos 30 min', cor: T2, v: 100 * q.taxa_sem_biometria_ultimos_30min, txt: P(100 * q.taxa_sem_biometria_ultimos_30min, 2) + '%' }, { nome: 'resto do dia', cor: T1, v: 100 * q.taxa_sem_biometria_resto_do_dia, txt: P(100 * q.taxa_sem_biometria_resto_do_dia, 2) + '%' }] }]} />
        {zs.length > 0 && <FaixaPontos titulo="z por urna (percentis)" itens={Object.entries(z).map(([k, v]) => ({ rot: k, v: v as number }))} min={Math.min(0, ...zs) - 0.5} max={Math.max(0, ...zs) + 0.5} fmt={(v) => P(v, 1)} refs={[{ v: 0 }]} />}
        <p className="text-[13px] text-muted">Urnas com rajada significativa (Benjamini-Hochberg): {N(q.urnas_significativas_BH)} de {N(q.urnas_com_votos_nos_ultimos_30min)}.</p>
      </div> }; },
  T20: (c) => { const L = NV(c); const q = L && L.T20; if (!q) return { ler: '', el: <Processando msg="T20 em processamento" /> };
    const ms = Object.keys(q).filter((k) => k.startsWith('UE')); const ext = Math.max(...ms.flatMap((k) => q[k].ic95.map(Math.abs)), 0.001) * 1.3;
    return { ler: 'Cada ponto é o resíduo médio da virada nas urnas de um modelo (em logit; 0 = virou como o esperado pelo município), com o intervalo de 95%. Todos perto de zero = o modelo da urna não muda a virada na prática.',
      el: <Pontos min={-ext} max={ext} fmt={(v) => SG(v, 4)} refs={[{ v: 0, rot: '0', solido: true }]} titulo={`Resíduo médio da virada por modelo de urna (Kruskal-Wallis p = ${P(q.kruskal_p, 3)})`} linhas={ms.map((k) => ({ l: `${k} (${N(q[k].urnas)} urnas)`, s: [{ nome: 'resíduo médio', cor: T2, v: q[k].residuo_medio, lo: q[k].ic95[0], hi: q[k].ic95[1] }] }))} /> }; },
  T29: (c) => { const L = NV(c); const q = L && L.T29; if (!q) return null; return { ler: 'Tempo entre a habilitação do eleitor e o voto computado. Votos "rápidos demais" (abaixo de 5 s) são contados; o mínimo e o percentil 1 dizem se há algo fisicamente impossível.',
    el: <Figuras titulo="Tempo habilitação → voto" itens={[{ n: `${P(q.duracao_min_global_s, 0)} s`, r: 'menor tempo observado' }, { n: `${P(q.duracao_min_p01_s, 0)} s`, r: 'percentil 1' }, { n: N(q.votos_abaixo_5s), r: 'votos abaixo de 5 s' }, { n: N(q.urnas_com_algum_voto_abaixo_5s), r: 'urnas com algum voto abaixo de 5 s' }]} /> }; },
  T30: (c) => { const L = NV(c); const q = L && L.T30; if (!q) return null; return { ler: 'Conta votos antes da abertura ou depois do encerramento da própria urna, lidos do log. Esperado: zero depois do encerramento; antes, só casos explicáveis (relógio, reabertura).',
    el: <Figuras titulo="Votos fora do horário da própria urna" itens={[{ n: N(q.urnas_avaliadas), r: 'urnas avaliadas' }, { n: N(q.urnas_com_voto_antes_da_abertura), r: 'urnas com voto antes da abertura', estado: q.urnas_com_voto_antes_da_abertura ? 'aviso' : 'ok' }, { n: N(q.urnas_com_voto_depois_do_encerramento_mais_1min), r: 'urnas com voto após o encerramento (+1 min)', estado: q.urnas_com_voto_depois_do_encerramento_mais_1min ? 'ruim' : 'ok' }]} /> }; },
  T31: (c) => { const L = NV(c); const q = L && L.T31; if (!q) return null; return { ler: 'Todo voto computado precisa de uma habilitação anterior no log da mesma urna.',
    el: <Figuras titulo="Voto sem habilitação" itens={[{ n: N(q.votos_sem_habilitacao), r: 'votos computados sem habilitação anterior', estado: q.votos_sem_habilitacao ? 'ruim' : 'ok' }, { n: N(q.urnas), r: 'urnas com esse problema', estado: q.urnas ? 'ruim' : 'ok' }]} /> }; },
  T33: (c) => { const L = NV(c); const q = L && L.T33; if (!q) return null; const vs = Object.entries(q.versoes || {}) as [string, number][]; return { ler: 'Versão do software registrada no log de cada urna, e verificações de integridade que o próprio software reporta.',
    el: <div className="grid gap-4"><Barras titulo="Versão do software por urna" linhas={vs.map(([v, n]) => ({ l: esc(v), bars: [{ cor: T2, v: n, txt: N(n) }] }))} />
      <Figuras itens={[{ n: N(q.verificacoes_ok), r: 'verificações com sucesso', estado: 'ok' }, { n: N(q.urnas_com_verificacao_sem_sucesso), r: 'urnas com alguma verificação sem sucesso', estado: q.urnas_com_verificacao_sem_sucesso ? 'aviso' : 'ok' }]} /></div> }; },
  T36: (c) => { const q = c.nv.casos_2t; if (!q) return null; const mx = q.casos || 1;
    return { ler: 'Das urnas em que alguma conta não fecha, mostramos de que tipo é a divergência e qual explicação operacional (verificada nos registros) a cobre. Um caso pode ter mais de um tipo. Âmbar = inconsistência de publicação (D1).',
      el: <div className="grid gap-5">
        <Figuras itens={[{ n: N(q.casos), r: `casos em ${N(q.urnas_avaliadas)} urnas avaliadas` }, { n: N(q.explicados_operacionais), r: 'com explicação operacional', estado: 'ok' }, { n: N(q.inconsistencias_de_publicacao_D1), r: 'inconsistência de publicação', estado: 'aviso' }, { n: N(q.sem_explicacao), r: 'sem explicação', estado: q.sem_explicacao ? 'ruim' : 'ok' }]} />
        <Barras titulo="Por tipo de divergência" max={mx} linhas={(Object.entries(q.por_tipo) as [string, number][]).sort((a, b) => b[1] - a[1]).map(([k, v]) => ({ l: TIPOS[k] || esc(k), bars: [{ cor: T2, v, txt: `${N(v)} casos` }] }))} />
        <Barras titulo="Por explicação" max={mx} linhas={(Object.entries(q.por_explicacao) as [string, number][]).sort((a, b) => b[1] - a[1]).map(([k, v]) => ({ l: EXPL[k] || esc(k), bars: [{ cor: k === 'D1' ? AVISO : T2, v, txt: `${N(v)}` }] }))} />
      </div> }; },
  T34: (c) => { const q = c.nv.correspondencia_1t; if (!q) return null; const bu = q.T34_ceft_urna_igual_bu || [], o = q.T34_origem_voto || {};
    return { ler: 'A urna que registrou os votos é a urna preparada para aquela seção? Medidor cheio = coincidem.',
      el: <div className="grid gap-4">{bu.length > 0 && <Coberturas titulo="Correspondência (1º turno)" itens={[{ l: 'Urna efetivada = urna do boletim', ok: bu[0], tot: bu[1], nome: '1º turno', cor: T1 }, { l: 'Certificado da carga = certificado no log', ok: q.T34_ceft_igual_certificado, tot: q.T34_urnas_processadas, nome: '1º turno', cor: T1 }]} />}
        <Figuras itens={[{ n: N(q.T34_esperada_diferente_efetivada || 0), r: 'seções com urna esperada ≠ efetivada (substituição, contingência)' }, ...(Object.entries(o) as [string, number][]).map(([k, v]) => ({ n: N(v), r: 'origem do voto: ' + k }))]} /></div> }; },
  T35: (c) => { const q = c.nv.correspondencia_1t; if (!q || q.T35_maquinas_geracao_midia == null) return null;
    return { ler: 'Cada máquina que gerou carga de urna deve ter o log publicado. Medidor cheio = todas.',
      el: <div className="grid gap-4"><Coberturas titulo="Carga das urnas (1º turno)" itens={[{ l: 'Máquinas de carga com log publicado', ok: q.T35_com_log_gedai_publicado, tot: q.T35_maquinas_geracao_midia, nome: '1º turno', cor: T1 }]} />
        <Figuras itens={[{ n: N((q.T35_sem_log || []).length), r: 'máquinas sem log, a investigar', estado: (q.T35_sem_log || []).length ? 'aviso' : 'ok' }]} /></div> }; },
  E01: (c) => { const a = c.nv.divergencias_2026, b = c.nv.divergencias_2022; if (!a) return null;
    return { ler: 'Que fração da diferença entre o observado e o esperado está entre grupos de cada nível? Se concentrada no local de votação (e não na zona ou no estado), o padrão é local e igual em 2022.',
      el: <Barras titulo="Fração da variância entre grupos, por nível (%)" max={100} linhas={Object.keys(NIV).filter((k) => a.E01[k]).map((k) => ({ l: NIV[k], bars: [anoBar('2026', { v: 100 * a.E01[k].fracao_variancia_entre_grupos, txt: P(100 * a.E01[k].fracao_variancia_entre_grupos, 1) + '%', dica: `<b>${P(100 * a.E01[k].fracao_variancia_entre_grupos, 1)}%</b><br>${NIV[k]}, 2026: ${N(a.E01[k].grupos)} grupos` }), ...(b && b.E01[k] ? [anoBar('2022', { v: 100 * b.E01[k].fracao_variancia_entre_grupos, txt: P(100 * b.E01[k].fracao_variancia_entre_grupos, 1) + '%' })] : [])] }))} /> }; },
  E02: (c) => { const a = c.nv.divergencias_2026, b = c.nv.divergencias_2022; if (!a) return null; const ks = ['local', 'zona', 'mun'].filter((k) => a.E02[k]);
    const lin = (ano: string, x: any, k: string) => x && x.E02[k] ? { l: `${NIV[k]}, ${ano}`, bars: [{ nome: 'pró-Lula', cor: LULA, v: x.E02[k].sig_pro_lula, txt: N(x.E02[k].sig_pro_lula) }, { nome: 'pró-adversário', cor: ADV, v: x.E02[k].sig_pro_adversario, txt: N(x.E02[k].sig_pro_adversario) }] } : null;
    return { ler: 'Grupos cujo desvio é significativo após correção para muitos testes (Benjamini-Hochberg), por lado. Lados parecidos e iguais a 2022 indicam que o excesso é do eleitorado, não de um lado só.',
      el: <Barras titulo="Grupos significativos por nível e ano" linhas={ks.flatMap((k) => [lin('2026', a, k), lin('2022', b, k)]).filter(Boolean) as LinhaBarras[]} /> }; },
  E03: (c) => { const a = c.nv.divergencias_2026, b = c.nv.divergencias_2022; if (!a) return null;
    const gr = (x: any, ano: string, k: string) => x && x.E03[k] ? <Dumbbell key={ano + k} titulo={`${NIV[k]}, ${ano}: 10 maiores divergências`} fmt={(v) => SG(v, 1)} na="virada esperada" nb="virada observada"
      linhas={x.E03[k].map((r: any) => ({ l: `${r.municipio}${k === 'local' ? ' (' + r.grupo + ')' : ''} · ${r.uf}`, a: r.virada_esp_logit, b: r.virada_obs_logit, z: r.z_grupo, dica: `<b>${esc(r.municipio)}</b>${k === 'local' ? ' (' + esc(r.grupo) + ')' : ''} · ${esc(r.uf)}<br>virada observada <b>${SG(r.virada_obs_logit, 2)}</b> · esperada ${SG(r.virada_esp_logit, 2)}<br>z ${P(r.z_grupo, 1)} · ${N(r.secoes)} seções` }))} /> : null;
    const bloco = (x: any, ano: string) => <div className="grid gap-5">{['local', 'zona', 'mun'].map((k) => gr(x, ano, k))}</div>;
    return { ler: 'Maiores divergências entre a virada observada (cobre) e a esperada (cinza), em logit, com o z ao lado. Lista exploratória: é onde olhar primeiro, não onde há problema.',
      el: <div className="grid gap-3">
        <details open className="group"><summary className="cursor-pointer font-medium text-[14px] h-10 inline-flex items-center gap-1 list-none [&::-webkit-details-marker]:hidden"><span className="transition-transform group-open:rotate-90 inline-block text-subtle">▸</span> 2026</summary>{bloco(a, '2026')}</details>
        <details className="group"><summary className="cursor-pointer font-medium text-[14px] h-10 inline-flex items-center gap-1 list-none [&::-webkit-details-marker]:hidden"><span className="transition-transform group-open:rotate-90 inline-block text-subtle">▸</span> 2022</summary>{b ? bloco(b, '2022') : <p className="text-sm text-muted">Sem dados de 2022.</p>}</details>
      </div> }; },
  C08: (c) => { const m = [...c.t.resultado_atual.matchAll(/([A-Za-zçãéí-]+(?:-[A-Za-zçãéí]+)?) \+([\d,]+)/g)]; if (!m.length) return null;
    return { ler: 'Virada média (pontos percentuais para Lula) por região, descritiva.', el: <Barras titulo="Virada por região (pp)" linhas={m.map((x) => ({ l: esc(x[1]), bars: [{ cor: T2, v: num(x[2]), txt: '+' + x[2] + ' pp' }] }))} /> }; },
  C07: (c) => { const m = c.t.resultado_atual.match(/idosos \+([\d,]+) e mulheres \+([\d,]+)/); if (!m) return null;
    return { ler: 'Quanto o comparecimento mudou entre os turnos, por grupo, dentro do município (associação, não causa).', el: <Barras titulo="Mudança de comparecimento por 100% do grupo" linhas={[{ l: 'Idosos', bars: [{ cor: T2, v: num(m[1]), txt: '+' + m[1] + ' pontos' }] }, { l: 'Mulheres', bars: [{ cor: T2, v: num(m[2]), txt: '+' + m[2] + ' pontos' }] }]} /> }; },
  C06: (c) => { const m = c.t.resultado_atual.match(/< ([\d,]+)%/); return { ler: 'A inferência ecológica estima, por grupo, para onde foram os votos do 1º turno. A conferência compara o total previsto com o observado; o fluxo completo está na página Mapas.',
    el: <div className="grid gap-3">{m && <Figuras itens={[{ n: `< ${m[1]}%`, r: 'erro da conferência previsto × observado', estado: 'ok' }]} />}<a href="#/mapas" className="text-sm font-medium text-accent-text underline underline-offset-4">Ver o fluxo de votos entre os turnos na página Mapas →</a></div> }; },
};

export function generico(c: Ctx): Viz {
  const t = c.t;
  return { ler: 'Se não houver nada anormal, vale a hipótese nula à esquerda; o resultado observado está à direita.', el: <Dupla a="Hipótese nula (nada anormal)" ta={t.hipotese_nula || t.pressupostos || t.metodo} b="Observado" tb={t.resultado_atual || 'sem resultado registrado'} /> };
}
export const MET: Record<string, string> = { T01: '2.5', T32: '2.5', T14: '2.2', T15: '2.2', T16: '2.2', T16c: '2.3', T17: '2.2', T17b: '2.2', T24: '2.2', T34: '2.4', T35: '2.4', T02: '3.1', T10: '3.2', T11: '3.2', C06: '3.3', C06b: '3.3', E01: '3.4', E02: '3.4', E03: '3.4', T03: '3.5', T04: '3.5', T05: '4.1', T27: '4.1', T26: '4.2', T21: '4.3', T07: '4.4', T22: '4.4', T25: '4.4', T13: '4.5', T13b: '4.5', T23: '4.6', T28: '4.7', T29: '4.7', T30: '4.7', T31: '4.7', T33: '4.7', T20: '4.8', T12: '4.9', T36: '2.2' };
export const MODS: Record<string, [string, string]> = {
  A: ['Integridade dos arquivos e da contagem', 'O dado é íntegro? Os arquivos das urnas, o boletim e o total oficial dizem a mesma coisa? Conferências exatas, sem estatística.'],
  B: ['Comportamento do eleitor e da votação', 'Como o eleitorado se comportou: hora do voto, comparecimento, perfil e a prorrogação.'],
  C: ['Mudança entre os turnos', 'Cada seção tem quase o mesmo eleitorado nos dois turnos: o 1º turno serve de régua para o 2º.'],
  D: ['Forense estatística', 'Testes clássicos de padrões em números de votos, sempre com a medida de quanto cada teste consegue (ou não) enxergar.'],
  E: ['Divergências e agrupamento', 'Seções ou locais que fogem do esperado, se se agrupam no espaço e que explicações existem.'],
  F: ['Referência: 2022', 'A mesma bateria no pleito de 2022, para saber se um número de 2026 é incomum.'],
  H: ['Fase 3: curvas, zeros e dependência espacial', 'Investigações da F3, com nulos explícitos e o que significam em votos.'],
  G: ['Fase 2: investigações aprofundadas', 'Testes novos, com pré-registro, que tentam derrubar métodos e conclusões anteriores. Cada um traz o que significa em número de votos.'],
};
export const ESTADO_TXT: Record<string, string> = { concluido: 'concluído', em_andamento: 'em andamento', a_fazer: 'a fazer', concluido_excluido_da_conclusao: 'concluído, excluído da conclusão', concluido_2t: 'concluído (2º turno)', concluido_1t: 'concluído (1º turno)', concluido_2026: 'concluído (2026)' };
// testes baseados nos logs das urnas: em reprocessamento (resultado preliminar) enquanto o reprocessamento não termina
export const EM_REPROCESSAMENTO = new Set<string>(); // reprocessamento dos logs concluído em 28/10/2026; use para marcar testes de novo se algo voltar a ser reprocessado
export const AVISO_RE = /incidente|erro meu|inv[aá]lid|corrigid|trocad|falso|errad|cortad|artefato/i;
export const emProc = (t: Teste) => t.situacao === 'a_fazer' || /^(a fazer|em processamento)/i.test(t.resultado_atual || '');
export const categoria = (t: Teste): 'ok' | 'parc' | 'proc' => (emProc(t) ? 'proc' : t.situacao === 'em_andamento' ? 'parc' : 'ok');
export const preliminar = (t: Teste) => EM_REPROCESSAMENTO.has(t.id) || t.situacao === 'em_andamento' || /reprocess|prelimin/i.test(t.situacao + ' ' + (t.resultado_atual || '').slice(0, 40));
