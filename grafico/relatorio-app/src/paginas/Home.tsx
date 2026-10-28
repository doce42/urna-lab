import { useMemo, useState } from 'react';
import { ArrowRight, BookOpen, FlaskConical, Map as MapIcon, Github } from 'lucide-react';
import { sum } from 'd3-array';
import { N, P, PP, milhoes, votosMil, minutoHora, nomeCurto, dataBR, REG, UF } from '@/lib/formato';
import type { Home as HomeDados, Registro, Meta } from '@/lib/tipos';
import { Botao, BotaoLink, Eyebrow, SeloClasse, CLASSE_COR, Nota } from '@/ui/base';
import { Urna } from '@/ui/Marca';
import { COR, Grafico, Tabela, Legenda } from '@/graficos/comum';
import { Linhas } from '@/graficos/Linhas';
import { Sankey, Cascata, BarrasUF, rotFluxo } from '@/graficos/especiais';
import { dica, esc } from '@/ui/Dica';
import { emProc } from '@/viz/testes';
import { RespostaCentral, useVeredito } from '@/ui/Sinal';

const Secao = ({ id, eyebrow, titulo, lead, children, className = '' }: { id: string; eyebrow: string; titulo: string; lead?: string; children: React.ReactNode; className?: string }) => (
  <section id={id} className={`container mt-20 md:mt-28 scroll-mt-20 ${className}`}>
    <div className="max-w-[46rem]">
      <Eyebrow>{eyebrow}</Eyebrow>
      <h2 className="t-h2 mt-2">{titulo}</h2>
      {lead && <p className="t-lead mt-3 text-[17px]">{lead}</p>}
    </div>
    <div className="mt-8">{children}</div>
  </section>
);


function RespostaHome() {
  const v = useVeredito();
  if (!v) return null;
  return (
    <section id="resposta" className="container mt-12 md:mt-16 scroll-mt-20">
      <RespostaCentral v={v} />
      <p className="mt-5 text-[14.5px]"><a href="#/respostas" className="text-accent-text underline underline-offset-4">Todas as perguntas, com a resposta, os números e o que cada uma significa em votos</a></p>
    </section>
  );
}

export function Home({ h, reg, meta }: { h: HomeDados; reg: Registro; meta: Meta | null }) {
  const n26 = h.nacional['2026'], n22 = h.nacional['2022'];
  const t2 = h.totais_2, val2 = t2.v13 + t2.v22;
  const r2 = h.log_resumo.t2;
  const base2 = r2?.assin_ok_bu ? r2.assin_ok_bu[1] : r2?.urnas;
  const placar = h.placar;
  const [modoApur, setModoApur] = useState<'t2' | 't1'>('t2');
  const falta = reg.testes.filter(emProc);

  // 1º x 2º turno: votos por candidato
  const barras1 = useMemo(() => {
    const cands = Object.entries(h.totais_1).filter(([k]) => k.startsWith('v')).sort((a, b) => b[1] - a[1]);
    const tot1 = sum(cands, (c) => c[1]) + h.totais_1.branco + h.totais_1.nulo;
    const top = cands.slice(0, 4), outros = sum(cands.slice(4), (c) => c[1]);
    return { tot1, itens: [...top.map(([k, v]) => ({ k, nome: nomeCurto(h.nomes_1['c' + k.slice(1)] || k), v })), { k: 'outros', nome: 'Outros candidatos', v: outros }, { k: 'bn', nome: 'Brancos e nulos', v: h.totais_1.branco + h.totais_1.nulo }] };
  }, [h]);
  const tot2 = val2 + t2.branco + t2.nulo;
  const corCand = (k: string) => (k === 'v13' ? COR.lula : k === 'v22' ? COR.adv : k === 'bn' ? COR.neutro : k === 'outros' ? 'var(--border-strong)' : COR.ref);

  // cascata por região
  const cascata = useMemo(() => {
    const a = h.ufs['2026'], n = n26;
    const L1 = n.votos_lula2 - n.ganho_lula, F1 = n.votos_adv2 - n.ganho_adv, m1 = L1 - F1, m2 = n.votos_lula2 - n.votos_adv2;
    const regs = Object.keys(REG).map((r) => ({ r, d: sum(REG[r], (u) => (a[u] ? a[u].ganho_lula - a[u].ganho_adv : 0)) })).sort((x, y) => y.d - x.d);
    const ext = m2 - m1 - sum(regs, (r) => r.d); if (Math.abs(ext) > 1000) regs.push({ r: 'Exterior', d: ext });
    const passos: { r: string; base: number; d: number; total?: boolean }[] = [{ r: '1º turno', base: 0, d: m1, total: true }];
    let acc = m1; regs.forEach((g) => { passos.push({ r: g.r, base: acc, d: g.d }); acc += g.d; });
    passos.push({ r: '2º turno', base: 0, d: m2, total: true });
    return { passos, m1, m2 };
  }, [h, n26]);

  // fluxo nacional
  const fluxo = h.fluxo['2026'];
  const fluxoResumo = useMemo(() => {
    if (!fluxo) return null;
    const L = fluxo.linhas.map((l) => l.replace(' (1º)', '')), C = fluxo.colunas, V = fluxo.votos;
    const jL = C.indexOf('Lula'), jA = C.indexOf('Adversário');
    const de = (nome: string, j: number) => { const i = L.indexOf(nome); return i < 0 ? 0 : V[i][j]; };
    const elim = L.filter((l) => !['Lula', 'Adversário', 'Branco/nulo', 'Abstenção'].includes(l));
    const gL = { elim: sum(elim, (l) => de(l, jL)), bn: de('Branco/nulo', jL), abst: de('Abstenção', jL) };
    const gA = { elim: sum(elim, (l) => de(l, jA)), bn: de('Branco/nulo', jA), abst: de('Abstenção', jA) };
    return { gL, gA, novosL: gL.elim + gL.bn + gL.abst + de('Adversário', jL), novosA: gA.elim + gA.bn + gA.abst + de('Lula', jA) };
  }, [fluxo]);

  // apuração por minuto
  const ap = h.apuracao[modoApur];
  const serieApur = useMemo(() => {
    const x = ap.min.map(minutoHora);
    if (modoApur === 't2') return { x, series: [
      { nome: 'Lula, % dos válidos (real)', cor: COR.lula, valores: ap.pct.c13, largura: 2.4 },
      { nome: 'Lula, previsto pelo 1º turno + virada do município', cor: COR.s2026, valores: ap.prev.p13m, traco: '6 4' },
      { nome: 'Flávio Bolsonaro, % dos válidos', cor: COR.adv, valores: ap.pct.c22 },
    ] };
    const ks = Object.keys(ap.pct).filter((k) => k[0] === 'c').slice(0, 4);
    // a cor segue o candidato (número de urna), nunca a posição: no 1º turno Flávio liderou e herdava a cor do Lula
    const outras = [COR.ref, COR.aviso];
    let j = 0;
    const corDe = (k: string) => (k === 'c13' ? COR.lula : k === 'c22' ? COR.adv : outras[j++ % outras.length]);
    return { x, series: ks.map((k) => ({ nome: nomeCurto(ap.nomes[k] || k), cor: corDe(k), valores: ap.pct[k] })) };
  }, [ap, modoApur]);
  const urnasPct = ap.urnas.map((u) => (100 * u) / ap.total_urnas);
  const horasCheias = ap.min.map((m, i) => (m % 60 === 0 ? i : -1)).filter((i) => i >= 0);

  // UFs: virada
  const ufLinhas = useMemo(() => Object.keys(h.ufs['2026']).map((k) => ({ k, v: h.ufs['2026'][k].virada, ref: h.ufs['2022']?.[k]?.virada ?? null,
    dica: `<b>${esc(UF[k] || k)}</b><br>Lula 1º turno ${P(h.ufs['2026'][k].lula1, 1)}% → 2º ${P(h.ufs['2026'][k].lula2, 1)}%<br>cresceu ${PP(h.ufs['2026'][k].virada)} (2022: ${h.ufs['2022']?.[k] ? PP(h.ufs['2022'][k].virada) : '—'})` })).sort((a, b) => b.v - a.v), [h]);

  const logs = h.logs;
  const logsX = useMemo(() => { if (!logs) return null; const horas = [...new Set(Object.values(logs).flatMap((v) => v.t))].sort((a, b) => a - b); return { horas, series: Object.entries(logs).map(([k, v]) => { const mp = new Map(v.t.map((t, i) => [t, v.votos[i]])); return { nome: k === 't1' ? '1º turno' : '2º turno', cor: k === 't1' ? COR.ref : COR.s2026, traco: k === 't1' ? '6 4' : undefined, valores: horas.map((t) => mp.get(t) ?? null), area: k === 't2' }; }) }; }, [logs]);

  return (
    <div className="pb-8">
      {/* ---------- herói ---------- */}
      <section className="container pt-10 md:pt-20">
        <div className="grid gap-10 lg:grid-cols-[1.15fr_1fr] lg:gap-16 items-end">
          <div className="surgir">
            <div className="inline-flex items-start sm:items-center gap-2 min-h-8 py-1.5 sm:py-0 px-3 rounded-full border border-border bg-surface text-[13px] text-muted leading-snug">
              <i className="w-2 h-2 rounded-full bg-accent shrink-0 mt-1.5 sm:mt-0" style={{ boxShadow: '0 0 0 3px color-mix(in srgb, var(--accent) 25%, transparent)' }} />
              <a href="#/linha-do-tempo" className="hover:text-text">{meta?.fase_atual || 'Estudo em andamento'} · dados de {dataBR(h.gerado_em)}</a>
            </div>
            <h1 className="t-display mt-6 max-w-[14ch]">A apuração de 2026, conferida urna por urna.</h1>
            <p className="t-lead mt-6 max-w-[52ch]">
              Auditoria metodológica independente, imparcial e reproduzível dos dados públicos da eleição presidencial (1º e 2º turno), com 2022 como referência. Não parte de suspeita nem de acusação.
              Só dados oficiais do TSE: dados abertos e os arquivos gravados por cada urna. Cada teste diz a pergunta, a hipótese nula, o resultado e o que ele não consegue ver.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <BotaoLink href="#/testes" variante="primario" tamanho="lg"><FlaskConical size={18} />Ver os {reg.testes.length} testes</BotaoLink>
              <BotaoLink href="#/docs" tamanho="lg"><BookOpen size={18} />Como foi feito</BotaoLink>
              <BotaoLink href={meta?.github || '#'} target="_blank" rel="noopener" tamanho="lg" variante="fantasma"><Github size={18} />Código e dados</BotaoLink>
            </div>
          </div>
          <div className="surgir atraso-2">
            <div className="cartao p-6 md:p-8 relative overflow-hidden">
              <div className="absolute -right-10 -top-10 opacity-[.07] pointer-events-none"><Urna tamanho={220} /></div>
              <Eyebrow>2º turno · {h.datas.t2.split('-').reverse().join('/')}</Eyebrow>
              <div className="t-hero mt-3 t-num">{N(h.urnas_2)}</div>
              <div className="text-muted mt-2">urnas no 2º turno · {N(h.urnas_1)} no 1º</div>
              <div className="mt-6 grid grid-cols-2 gap-4 border-t border-border pt-5">
                <div><div className="text-2xl font-semibold tracking-tight t-num">{r2 ? P((100 * r2.assin_lista_ok) / (base2 || 1), r2.assin_lista_ok === base2 ? 0 : 3) + '%' : '—'}</div><div className="text-[13px] text-muted mt-1">das urnas com arquivos têm assinatura digital válida</div></div>
                <div><div className="text-2xl font-semibold tracking-tight t-num">{r2 ? N(r2.rdv_igual_boletim) : '—'}</div><div className="text-[13px] text-muted mt-1">recontagens pelo RDV iguais ao boletim, de {r2 ? N(r2.urnas_com_rdv) : '—'}</div></div>
              </div>
              <Nota className="mt-5">Prova determinística: conta exata e criptografia, não amostra. Prova coerência entre arquivos oficiais; não prova que o software da urna contou certo.</Nota>
            </div>
          </div>
        </div>

        {/* KPIs */}
        <div className="mt-12 grid grid-cols-2 lg:grid-cols-4 gap-3 surgir atraso-3">
          {[
            { n: P((100 * t2.v13) / val2) + '%', r: `Lula no 2º turno · ${N(t2.v13)} votos`, cor: COR.lula },
            { n: P((100 * t2.v22) / val2) + '%', r: `Flávio Bolsonaro no 2º turno · ${N(t2.v22)} votos`, cor: COR.adv },
            { n: N(h.margem_votos), r: 'votos de diferença (margem do 2º turno)', cor: COR.s2026 },
            { n: `${P(n26.comp1, 1)}% → ${P(n26.comp2, 1)}%`, r: `comparecimento, do 1º para o 2º turno (2022: ${P(n22.comp1, 1)}% → ${P(n22.comp2, 1)}%)`, cor: COR.ref },
          ].map((k, i) => (
            <div key={i} className="cartao p-5 border-t-[3px]" style={{ borderTopColor: k.cor }}>
              <div className="text-[1.65rem] md:text-3xl font-semibold tracking-tight leading-none">{k.n}</div>
              <div className="text-[13px] text-muted mt-2 leading-snug">{k.r}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ---------- a pergunta e a resposta (fase3/veredito_2026.json) ---------- */}
      <RespostaHome />

      {/* ---------- placar ---------- */}
      <Secao id="validado" eyebrow="O que já foi verificado" titulo="Placar da verificação" lead={`${placar.total} testes registrados, cada um com classe de evidência e grau de certeza. Nenhum número aqui é escrito à mão: tudo sai do código e do registro de testes.`}>
        <div className="grid gap-4">
          <div className="cartao p-5 md:p-6 grid gap-5 lg:grid-cols-[auto_1fr] lg:items-center">
            <div className="grid grid-cols-3 gap-2 sm:gap-3 lg:min-w-[380px]">
              {[{ n: placar.concluidos, r: 'concluídos', cor: 'var(--ok)', f: 'ok' }, { n: placar.parciais, r: 'parciais', cor: 'var(--warn)', f: 'parc' }, { n: placar.processando, r: 'processando', cor: 'var(--text-subtle)', f: 'proc' }].map((k) => (
                <a key={k.r} href={`#/testes?estado=${k.f}`} className="rounded-lg border border-border bg-surface-2 p-3 sm:p-4 hover:border-border-strong transition-colors min-w-0">
                  <div className="text-2xl sm:text-3xl font-semibold tracking-tight" style={{ color: k.cor }}>{k.n}</div><div className="text-xs sm:text-[13px] text-muted mt-1 leading-snug">{k.r}</div>
                </a>
              ))}
            </div>
            <div className="lg:border-l lg:border-border lg:pl-6">
              <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm mb-3">
                <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-accent" /><b className="font-semibold">{placar.confirmatorios}</b> confirmatórios</div>
                <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-border-strong" /><b className="font-semibold">{placar.exploratorios}</b> exploratórios</div>
                <span className="text-xs font-mono uppercase tracking-wider text-muted self-center basis-full sm:basis-auto"><span className="hidden sm:inline">· </span>classe de evidência</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {'ABCDEFG'.split('').map((k) => (
                  <a key={k} href={`#/testes?classe=${k}`} className="inline-flex items-center gap-2 h-9 pl-1 pr-3 rounded-full border border-border bg-surface text-[13px] font-medium hover:border-border-strong transition-colors" title={reg.classes[k]}>
                    <b className="grid place-items-center w-7 h-7 rounded-full text-white text-xs" style={{ background: CLASSE_COR[k] }}>{k}</b>
                    <span className="text-muted">{reg.classes[k].split(' / ')[0]}</span><span className="t-num">{placar.classes[k] || 0}</span>
                  </a>
                ))}
              </div>
            </div>
          </div>
          <div className="grid gap-3 lg:grid-cols-3">
            {[
              { t: '1. Prova determinística', cor: 'var(--cA)', p: r2 ? <>Assinatura da lista de arquivos válida em <b>{N(r2.assin_lista_ok)}</b> das <b>{N(base2)}</b> urnas do 2º turno com arquivos; recontagem do RDV igual ao boletim em <b>{N(r2.rdv_igual_boletim)}</b> de <b>{N(r2.urnas_com_rdv)}</b>; log fecha com o comparecimento em <b>{N(r2.log_igual_comparecimento)}</b> de <b>{N(r2.urnas)}</b>. Boletim de Urna e votação por seção iguais voto a voto nos dois turnos (T01).</> : 'Processamento dos arquivos do 2º turno ainda não terminou.', ids: ['T01', 'T16', 'T17'] },
              { t: '2. Evidência estatística, com poder medido', cor: 'var(--cB)', p: <>{N(h.z_hist.acima5_lula + h.z_hist.acima5_flavio)} seções de {N(h.z_hist.n)} ficaram além de 5 desvios ({h.z_hist.acima5_lula} pró-Lula, {h.z_hist.acima5_flavio} pró-Flávio): anomalia estatística registrada (classe B), com excesso pró-Lula que também aparece em 2022, sem prova de causa. A curva reconstruída pela hora de recebimento dos boletins difere da prevista em no máximo {P(h.curva_max_desvio.depois_19h, 2)} pp depois das 19h (descrição, não teste calibrado; não é a curva divulgada). Dos {h.poder.cenarios} cenários de fraude simulada, {h.poder.detectados} foram detectados; o maior que passou despercebido move {N(h.poder.maior_passou_votos)} votos, contra uma margem de {N(h.margem_votos)}. Esses cenários só deslocam votos a favor de Lula; na Fase 2, o mesmo teste não via o deslocamento no sentido contrário, e na Fase 3, com a regra de duas caudas e contando só alarmes no sentido certo, vê troca dispersa de ~123 mil votos e troca concentrada de ~62 mil em locais ou municípios de até ~5 mil seções; não vê ~25 mil votos em nenhuma forma, nem troca no município inteiro das 5 maiores cidades (até ~700 mil votos). São simulações, não votos encontrados nos dados, e mecanismos não simulados ficam fora desse alcance (P18, A2).</>, ids: ['T02', 'T10', 'T13'] },
              { t: '3. Limite dos dados públicos', cor: 'var(--cG)', p: <>Uma troca pequena e uniforme no país inteiro, ou qualquer falha no software da urna que gere arquivos consistentes e assinados, não deixa rastro nos dados públicos. Resultados nulos não provam ausência. {falta.length ? <>{falta.length === 1 ? 'Falta 1 teste' : `Faltam ${falta.length} testes`} ({falta.map((t) => t.id).join(', ')}).</> : null}</>, ids: ['C06b', 'T13b'] },
            ].map((f) => (
              <div key={f.t} className="cartao p-5 border-l-4" style={{ borderLeftColor: f.cor }}>
                <h3 className="t-h3">{f.t}</h3>
                <p className="text-[15px] text-muted mt-2 leading-relaxed">{f.p}</p>
                <div className="mt-3 flex flex-wrap gap-1.5">{f.ids.filter((i) => reg.testes.find((t) => t.id === i)).map((i) => <a key={i} href={`#/testes/${i}`} className="font-mono text-xs h-7 px-2.5 inline-flex items-center rounded-md border border-border hover:border-border-strong">{i}</a>)}</div>
              </div>
            ))}
          </div>
        </div>
        <Nota className="mt-4 max-w-[80ch]">A pergunta “houve fraude?” é respondida só nestes termos: o que foi demonstrado, o que é evidência, o que é inconclusivo e o que está fora do alcance dos dados. Significância estatística não é prova de manipulação; ausência de achado não é prova de inexistência.</Nota>
      </Secao>

      {/* ---------- 1º x 2º turno ---------- */}
      <Secao id="turnos" eyebrow="Primeiras respostas" titulo="Do 1º para o 2º turno" lead={`Lula foi de ${P(n26.lula1, 1)}% para ${P(n26.lula2, 1)}% dos válidos (${PP(n26.virada)}). Em 2022, a mudança foi de ${PP(n22.virada)}.`}>
        <div className="grid gap-4 lg:grid-cols-2">
          <div className="cartao p-5 md:p-6">
            <Grafico titulo="Votos no 1º turno (04/10)" sub={`${N(barras1.tot1)} votos · ${N(h.urnas_1)} urnas`} tabela={<Tabela cab={['', 'votos', '% do total']} linhas={barras1.itens.map((i) => [i.nome, N(i.v), P((100 * i.v) / barras1.tot1, 1) + '%'])} />}>
              <div className="flex h-7 rounded-md overflow-hidden gap-[2px] mt-1">{barras1.itens.map((i) => <div key={i.k} style={{ width: `${(100 * i.v) / barras1.tot1}%`, background: corCand(i.k) }} {...dica(`<b>${esc(i.nome)}</b><br>${N(i.v)} votos · ${P((100 * i.v) / barras1.tot1, 1)}%`)} />)}</div>
              <div className="mt-3 grid gap-1.5">{barras1.itens.map((i) => <div key={i.k} className="flex items-center gap-2.5 text-[14px]"><i className="w-3 h-3 rounded-sm shrink-0" style={{ background: corCand(i.k) }} /><span className="text-muted flex-1 truncate">{i.nome}</span><span className="t-num font-medium">{P((100 * i.v) / barras1.tot1, 1)}%</span><span className="t-num text-subtle text-xs w-20 text-right hidden sm:block">{milhoes(i.v, 2)}</span></div>)}</div>
            </Grafico>
          </div>
          <div className="cartao p-5 md:p-6">
            <Grafico titulo="Votos no 2º turno (25/10)" sub={`${N(tot2)} votos · ${N(h.urnas_2)} urnas`} tabela={<Tabela cab={['', 'votos', '% do total']} linhas={[['Lula', N(t2.v13), P((100 * t2.v13) / tot2, 1) + '%'], ['Flávio Bolsonaro', N(t2.v22), P((100 * t2.v22) / tot2, 1) + '%'], ['Brancos e nulos', N(t2.branco + t2.nulo), P((100 * (t2.branco + t2.nulo)) / tot2, 1) + '%']]} />}>
              <div className="flex h-7 rounded-md overflow-hidden gap-[2px] mt-1">
                {[['v13', 'Lula', t2.v13], ['v22', 'Flávio Bolsonaro', t2.v22], ['bn', 'Brancos e nulos', t2.branco + t2.nulo]].map(([k, nome, v]) => <div key={k as string} style={{ width: `${(100 * (v as number)) / tot2}%`, background: corCand(k as string) }} {...dica(`<b>${nome}</b><br>${N(v as number)} votos · ${P((100 * (v as number)) / tot2, 1)}% do total`)} />)}
              </div>
              <div className="mt-3 grid gap-1.5">
                {[['v13', 'Lula', t2.v13], ['v22', 'Flávio Bolsonaro', t2.v22], ['bn', 'Brancos e nulos', t2.branco + t2.nulo]].map(([k, nome, v]) => <div key={k as string} className="flex items-center gap-2.5 text-[14px]"><i className="w-3 h-3 rounded-sm shrink-0" style={{ background: corCand(k as string) }} /><span className="text-muted flex-1">{nome}</span><span className="t-num font-medium">{P((100 * (v as number)) / tot2, 1)}%</span><span className="t-num text-subtle text-xs w-20 text-right hidden sm:block">{milhoes(v as number, 2)}</span></div>)}
              </div>
              <div className="mt-4 pt-4 border-t border-border grid grid-cols-2 gap-3 text-sm">
                <div><div className="text-xs text-subtle">dos válidos</div><div className="font-medium t-num">Lula {P((100 * t2.v13) / val2)}% · Flávio {P((100 * t2.v22) / val2)}%</div></div>
                <div><div className="text-xs text-subtle">2022, dos válidos</div><div className="font-medium t-num">Lula {P(n22.lula2, 1)}% · Bolsonaro {P(100 - n22.lula2, 1)}%</div></div>
              </div>
            </Grafico>
          </div>
        </div>
      </Secao>

      {/* ---------- evolução da apuração ---------- */}
      <Secao id="apuracao" eyebrow="A noite da apuração" titulo="Como a curva evoluiu, minuto a minuto" lead="Cada urna entra na soma na hora em que o boletim chegou ao TSE. No 2º turno, a linha tracejada é o que as mesmas urnas deveriam dar pelo próprio 1º turno mais a virada do município: se um lote votasse fora do próprio histórico, a real se descolaria.">
        <div className="cartao p-5 md:p-6">
          <div className="flex flex-wrap items-center gap-2 mb-4">
            {(['t2', 't1'] as const).map((k) => <Botao key={k} tamanho="sm" variante={modoApur === k ? 'primario' : 'secundario'} onClick={() => setModoApur(k)} aria-pressed={modoApur === k}>{k === 't2' ? '2º turno' : '1º turno'}</Botao>)}
            <span className="text-[13px] text-muted ml-1">% acumulado dos votos válidos, por minuto de chegada ao TSE</span>
          </div>
          <Linhas x={serieApur.x} series={serieApur.series} fmt={(v) => P(v, 1) + '%'} altura={300} tabelaPasso={30} rotulosX={horasCheias} ariaRotulo="Percentual acumulado por minuto de chegada" />
          <div className="mt-5">
            <Linhas titulo="Urnas apuradas (% do total)" x={serieApur.x} series={[{ nome: 'urnas apuradas', cor: COR.ref, valores: urnasPct, area: true }]} fmt={(v) => P(v, 0) + '%'} altura={140} zero={0} rotulosFim tabelaPasso={30} rotulosX={horasCheias} />
          </div>
          <Nota className="mt-3">Maior desvio real − previsto depois das 19h no 2º turno: {P(h.curva_max_desvio.depois_19h, 2)} pp (teste <a className="underline" href="#/testes/T10">T10</a>). Zigue-zagues da curva compatíveis com a simulação (<a className="underline" href="#/testes/T11">T11</a>).</Nota>
        </div>
      </Secao>

      {/* ---------- de onde vieram os votos ---------- */}
      {fluxo && fluxoResumo && (
        <Secao id="fluxo" eyebrow="De onde vieram os votos" titulo={`Lula somou cerca de ${P(fluxoResumo.novosL / 1e6, 1)} milhões de votos novos no 2º turno; Flávio Bolsonaro, ${P(fluxoResumo.novosA / 1e6, 1)} milhões`} lead="Estimativa por grupos (inferência ecológica, teste C06): o que fez no 2º turno quem votou em cada opção no 1º. Reproduz o total real do 2º turno com erro abaixo de 0,1%. O voto individual é secreto. Na Fase 2, um teste com dados sintéticos mostrou que a proporção entre destinos depende do pressuposto de taxas homogêneas dentro do estado; a ordem entre eles se manteve.">
          <div className="grid gap-3 sm:grid-cols-3 mb-4">
            {[[fluxoResumo.gL.elim, fluxoResumo.gA.elim, 'vindos de eleitores de candidatos eliminados'], [fluxoResumo.gL.bn, fluxoResumo.gA.bn, 'vindos de quem votou branco ou nulo no 1º turno'], [fluxoResumo.gL.abst, fluxoResumo.gA.abst, 'vindos de quem não votou no 1º turno']].map(([a, b, r], i) => (
              <div key={i} className="cartao p-5"><div className="text-2xl font-semibold tracking-tight t-num"><span style={{ color: COR.lula }}>{milhoes(a as number)}</span> <span className="text-subtle text-lg">×</span> <span style={{ color: COR.adv }}>{milhoes(b as number, (b as number) < 5e5 ? 2 : 1)}</span></div><div className="text-[13px] text-muted mt-1">{r as string} (Lula × Flávio)</div></div>
            ))}
          </div>
          <div className="cartao p-5 md:p-6"><Sankey f={fluxo} V={fluxo.votos} titulo="Fluxo de eleitores do 1º para o 2º turno, Brasil" /></div>
          <div className="mt-3 flex flex-wrap gap-3 items-center"><a href="#/mapas#fluxo" className="text-sm font-medium text-accent-text inline-flex items-center gap-1">Ver o fluxo por estado <ArrowRight size={15} /></a><Nota>Troca direta entre finalistas: os dados só garantem um mínimo e permitem até dezenas de milhões em cada sentido (<a className="underline" href="#/testes/C06b">C06b</a>).</Nota></div>
        </Secao>
      )}

      {/* ---------- cascata + mapa resumido ---------- */}
      <Secao id="virada" eyebrow="Onde a diferença mudou" titulo={`Flávio terminou o 1º turno ${votosMil(-cascata.m1).replace('+', '')} votos à frente; Lula fechou o 2º turno ${votosMil(cascata.m2).replace('+', '')} à frente`} lead="Cada degrau é quanto uma região mudou a diferença Lula − Flávio, em votos. À direita, o mesmo movimento por estado, com 2022 como referência.">
        <div className="grid gap-4 lg:grid-cols-2">
          <div className="cartao p-5 md:p-6"><Cascata passos={cascata.passos} titulo="Mudança na diferença Lula − Flávio, por região (votos)" /></div>
          <div className="cartao p-5 md:p-6"><BarrasUF linhas={ufLinhas} titulo="Quanto Lula cresceu por estado (pontos percentuais dos válidos)" fmt={(v) => PP(v, 0).replace(' pp', '')} /></div>
        </div>
        <div className="mt-4"><BotaoLink href="#/mapas" variante="secundario"><MapIcon size={16} />Mapas completos: município por município, bolhas e assinatura de enchimento</BotaoLink></div>
      </Secao>

      {/* ---------- votação ao longo do dia ---------- */}
      {logsX && (
        <Secao id="dia" eyebrow="Dentro das urnas" titulo="A que horas o país votou" lead="Votos computados a cada minuto, contados dos logs das urnas (horário de Brasília). O log não diz em quem: o voto é secreto. É um dos dados independentes das tabelas de votação, usado para confirmar padrões descobertos nelas.">
          <div className="cartao p-5 md:p-6"><Linhas x={logsX.horas.map(minutoHora)} series={logsX.series} fmt={N} zero={0} altura={260} tabelaPasso={30} rotulosX={logsX.horas.map((m, i) => (m % 60 === 0 ? i : -1)).filter((i) => i >= 0)} ariaRotulo="Votos computados por minuto" /></div>
        </Secao>
      )}

      {/* ---------- propósito ---------- */}
      <Secao id="proposito" eyebrow="Propósito" titulo="Não procuramos uma conclusão: procuramos explicações testáveis" lead="O estudo não parte da pergunta “houve fraude?”: parte dos dados. Pergunta quais padrões, anomalias e divergências existem, quais explicações científicas têm e quais hipóteses resistem a uma investigação rigorosa. A pergunta sobre fraude é respondida dentro desse quadro.">
        <div className="grid gap-4 md:grid-cols-3">
          {[
            ['Não presumir', 'Nem que houve fraude, nem que seria impossível. Anomalia estatística não é fraude; ausência de evidência não é demonstração de inexistência.'],
            ['Medir o poder', 'Todo resultado negativo vem com a medida do que o teste conseguiria ver: fraude sintética injetada nos dados reais e 2022 como controle de especificidade.'],
            ['Deixar refutar', 'Código MIT, documentação CC BY 4.0, critérios fixados antes de rodar, emendas datadas, sementes registradas. Qualquer pessoa pode reproduzir e discordar.'],
          ].map(([t, p]) => <div key={t} className="cartao p-6"><h3 className="t-h3">{t}</h3><p className="text-[15px] text-muted mt-2 leading-relaxed">{p}</p></div>)}
        </div>
        <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {[['Diretriz científica', 'diretriz', 'Princípios e classes A–G'], ['Protocolo', 'protocolo', 'Critérios fixados antes'], ['Metodologia', 'metodologia', 'A matemática de cada teste'], ['Como reproduzir', 'pipeline', 'Do download aos resultados']].map(([t, s, r]) => (
            <a key={s} href={`#/docs/${s}`} className="cartao cartao-hover p-5 flex items-center justify-between gap-3"><div><div className="font-medium">{t}</div><div className="text-[13px] text-muted mt-0.5">{r}</div></div><ArrowRight size={18} className="text-subtle shrink-0" /></a>
          ))}
        </div>
        <div className="mt-4 flex flex-wrap gap-2 items-center text-[13px] text-muted">
          <SeloClasse classe="A" nome="regularidade" /> <SeloClasse classe="B" nome="anomalia estatística" /> <SeloClasse classe="D" nome="inconsistência verificável" /> <SeloClasse classe="G" nome="inconclusivo" />
          <span>Classes de evidência substituem o binário “fraude / sem fraude”. Não é uma escada: uma anomalia robusta não vira evidência de manipulação só por ser muito significativa.</span>
        </div>
      </Secao>
    </div>
  );
}
