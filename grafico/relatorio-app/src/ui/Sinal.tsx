// Nível de sinal (suspeita) de cada teste e veredito de 2026, separados de "passou/não passou". Fonte: fase3/veredito_2026.json.
import { useDados } from '@/lib/dados';

export type Nivel = { id: string; nome: string; cor: string; o_que_e: string };
export type Hipotese = { id: string; mecanismo: string; o_que_deixaria: string; escala_necessaria: string; testes: string[]; resultado: string; status: string; em_votos: string };
export type Veredito = {
  margem_2026: number; votos_para_inverter: number; niveis: Nivel[]; sinal_por_teste: Record<string, { nivel: string; motivo: string }>; hipoteses: Hipotese[];
  resposta_central: { aviso?: { titulo: string; itens: string[]; nota_autor?: string }; pergunta: string; resposta: string; deducao: string[]; o_que_seria_preciso: string; anomalias_2026: { o_que: string; votos: string; sinal: string; teste: string }[];
    avisos?: string[]; nota_anomalias?: string; operacao?: Operacao; alegacoes?: Alegacoes };
};
export type Alegacoes = { titulo: string; frase: string; situacao: string; itens: { alegacao: string; resposta: string; perguntas: string[]; testes: string[] }[] };
export type Operacao = { titulo: string; data: string; versao: string; pergunta: string; resposta: string; achados: { titulo: string; texto: string; teste: string }[]; pontos_cegos: string[]; perguntas: string[]; capitulo: string; documentos: { slug: string; titulo: string }[] };

// Avisos que acompanham os resultados (Operação Veracidade Geral, RECOMENDACOES_SITE.md seção 3)
export function AvisosAlcance({ avisos }: { avisos: string[] }) {
  return (
    <div className="cartao p-5 md:p-6 border-l-[3px]" style={{ borderLeftColor: 'var(--warn)' }}>
      <div className="text-[12px] font-mono uppercase tracking-wider" style={{ color: 'var(--warn)' }}>Leia junto com os resultados</div>
      <ul className="mt-2 grid gap-1.5 text-[15px] leading-relaxed text-muted list-disc pl-5">{avisos.map((a) => <li key={a}>{a}</li>)}</ul>
    </div>
  );
}

export const COR_SINAL: Record<string, string> = {
  S0: 'var(--ok)', S1: 'color-mix(in srgb, var(--ok) 70%, var(--text-subtle))', S2: 'var(--warn)',
  S3: 'color-mix(in srgb, var(--warn) 45%, var(--erro))', S4: 'var(--erro)', S5: 'var(--erro)', PC: 'var(--text-subtle)', M: 'var(--text-subtle)',
};
export const COR_STATUS = (s: string) => s.startsWith('Contrariada') ? 'var(--ok)' : s.startsWith('Sem sinal') ? 'color-mix(in srgb, var(--ok) 70%, var(--text-subtle))' : s.startsWith('Sinal') ? COR_SINAL.S3 : 'var(--text-subtle)';

export function useVeredito() { return useDados<Veredito>('veredito').dados; }

export function SeloSinal({ nivel, nome, titulo }: { nivel: string; nome?: string; titulo?: string }) {
  const c = COR_SINAL[nivel] || 'var(--text-subtle)';
  return (
    <span title={titulo} className="inline-flex items-center gap-1.5 min-h-7 px-2.5 rounded-full text-xs font-medium border shrink-0" style={{ color: c, borderColor: c, borderStyle: nivel === 'M' ? 'dashed' : 'solid' }}>
      <i className="w-2 h-2 rounded-full" style={{ background: c }} />{nome || nivel}
    </span>
  );
}

export function SeloStatus({ s }: { s: string }) {
  const c = COR_STATUS(s);
  return <span className="inline-flex items-center gap-1.5 min-h-6 px-2 rounded-full text-xs font-medium border shrink-0" style={{ color: c, borderColor: c }}><i className="w-1.5 h-1.5 rounded-full" style={{ background: c }} />{s}</span>;
}

// Aviso antes da pergunta: o estudo é auditoria metodológica dos dados; a pergunta sobre fraude é testada, não é a premissa.
export function AvisoEstudo({ aviso }: { aviso: { titulo: string; itens: string[]; nota_autor?: string } }) {
  return (
    <div className="cartao p-5 md:p-6 border-l-[3px]" style={{ borderLeftColor: 'var(--accent)' }}>
      <div className="text-[12px] font-mono uppercase tracking-wider text-accent-text">Aviso</div>
      <h2 className="t-h3 mt-1">{aviso.titulo}</h2>
      <ul className="mt-3 grid gap-2 text-[15px] leading-relaxed text-muted list-disc pl-5">{aviso.itens.map((a) => <li key={a}>{a}</li>)}</ul>
      {aviso.nota_autor && <div className="mt-4 pt-4 border-t border-border"><div className="text-[12px] font-mono uppercase tracking-wider text-muted">Nota do autor</div><p className="mt-1.5 text-[15px] leading-relaxed text-text italic">“{aviso.nota_autor}”</p></div>}
    </div>
  );
}

// Bloco da resposta central: pergunta, resposta, dedução, hipóteses e anomalias reais. Usado na Home e em Respostas.
// recolher: hipóteses e anomalias ficam em <details> (Home), para a resposta e os avisos virem primeiro
export function RespostaCentral({ v, compacto, recolher }: { v: Veredito; compacto?: boolean; recolher?: boolean }) {
  const r = v.resposta_central; const nivel = (id: string) => v.niveis.find((n) => n.id === id)?.nome || id;
  return (
    <div className="grid gap-6">
      {r.aviso && <AvisoEstudo aviso={r.aviso} />}
      <div className="cartao p-5 md:p-7">
        <div className="text-[12px] font-mono uppercase tracking-wider text-muted">Pergunta testada</div>
        <h2 className="t-h2 mt-1">{r.pergunta}</h2>
        <p className="mt-3 text-[17px] leading-relaxed text-text">{r.resposta}</p>
        {!compacto && <ol className="mt-4 grid gap-1.5 text-[15px] text-muted list-decimal pl-5">{r.deducao.map((d) => <li key={d}>{d}</li>)}</ol>}
        <p className="mt-4 text-[14px] text-muted"><b className="font-medium text-text">O que fecharia o que resta: </b>{r.o_que_seria_preciso}</p>
        {r.alegacoes && <p className="mt-3 text-[14px] text-muted"><b className="font-medium text-text">Alegações públicas: </b>{r.alegacoes.frase} <a href="#/respostas/alegacoes" className="text-accent-text underline underline-offset-2">Ver as respostas</a></p>}
      </div>
      {r.avisos && r.avisos.length > 0 && <AvisosAlcance avisos={r.avisos} />}
      <Recolhivel recolher={recolher} titulo={`As ${v.hipoteses.length} hipóteses de fraude examinadas e as anomalias reais de 2026`}>
      <div>
        <h3 className="t-h3">As hipóteses de fraude examinadas</h3>
        <p className="text-muted text-[14.5px] mt-1">Cada mecanismo concreto, o que ele deixaria nos dados e o que encontramos. Inverter 2026 exigiria trocar ~{(v.votos_para_inverter / 1e6).toFixed(2).replace('.', ',')} mi votos de lado.</p>
        <ul className="mt-3 grid gap-2">{v.hipoteses.map((h) => (
          <li key={h.id} className="cartao p-4">
            <div className="flex flex-wrap items-start gap-x-3 gap-y-2"><span className="font-mono text-sm font-semibold w-9 shrink-0 pt-0.5">{h.id}</span><span className="text-[15px] text-text font-medium leading-snug flex-1 min-w-[14rem]">{h.mecanismo}</span><SeloStatus s={h.status} /></div>
            <p className="mt-1.5 text-[14.5px] text-muted leading-relaxed">{h.resultado}</p>
            <p className="mt-1 text-[13.5px]"><b className="font-medium text-text">Em votos: </b><span className="text-muted">{h.em_votos}</span></p>
            {!compacto && <details className="mt-1 group/h"><summary className="cursor-pointer list-none text-[12.5px] text-subtle hover:text-text"><span className="group-open/h:hidden">o que deixaria e testes</span><span className="hidden group-open/h:inline">recolher</span></summary>
              <div className="mt-1.5 grid gap-1 text-[13.5px] text-muted"><div><b className="font-medium text-text">O que deixaria: </b>{h.o_que_deixaria}</div><div><b className="font-medium text-text">Escala: </b>{h.escala_necessaria}</div>
                <div><b className="font-medium text-text">Testes: </b>{h.testes.map((t, k) => <span key={t}>{k ? ', ' : ''}{/^[TCE]\d/.test(t) ? <a className="text-accent-text underline underline-offset-2" href={`#/testes/${t}`}>{t}</a> : t}</span>)}</div></div></details>}
          </li>
        ))}</ul>
      </div>
      <div>
        <h3 className="t-h3">Anomalias reais em 2026</h3>
        <p className="text-muted text-[14.5px] mt-1">O que encontramos fora do esperado, com o tamanho em votos. {r.nota_anomalias || 'Nenhuma tem causa demonstrada.'}</p>
        <ul className="mt-3 grid gap-1.5">{r.anomalias_2026.map((a) => (
          <li key={a.o_que} className="flex flex-wrap items-center gap-x-3 gap-y-1 text-[14.5px] border-b border-border py-2">
            <SeloSinal nivel={a.sinal} nome={nivel(a.sinal)} /><span className="flex-1 min-w-[12rem] text-text">{a.o_que}</span><span className="font-mono text-[13.5px] text-muted">{/^[~\d]/.test(a.votos) && !/votos/.test(a.votos) ? `${a.votos} votos` : a.votos}</span>
            <a href={`#/testes/${a.teste}`} className="text-accent-text underline underline-offset-2 text-[13px]">{a.teste}</a>
          </li>
        ))}</ul>
      </div>
      </Recolhivel>
    </div>
  );
}

function Recolhivel({ recolher, titulo, children }: { recolher?: boolean; titulo: string; children: React.ReactNode }) {
  if (!recolher) return <>{children}</>;
  return (
    <details className="cartao group/r">
      <summary className="cursor-pointer list-none p-4 md:p-5 flex items-center gap-3 [&::-webkit-details-marker]:hidden"><span className="w-6 h-6 grid place-items-center rounded-full bg-surface-2 text-subtle text-xs transition-transform group-open/r:rotate-90" aria-hidden="true">▸</span><span className="t-h3">{titulo}</span><span className="ml-auto text-xs text-subtle group-open/r:hidden">abrir</span><span className="ml-auto text-xs text-subtle hidden group-open/r:inline">fechar</span></summary>
      <div className="px-4 md:px-5 pb-5 grid gap-6">{children}</div>
    </details>
  );
}

// Alegações públicas mais comuns e a resposta curta de cada uma (fase3/veredito_2026.json → resposta_central.alegacoes)
export function AlegacoesResumo({ a, titulo = true, max }: { a: Alegacoes; titulo?: boolean; max?: number }) {
  const cartao = (x: Alegacoes['itens'][number]) => (
        <li key={x.alegacao} className="cartao p-4 md:p-5 flex flex-col gap-2">
          <div className="text-[12px] font-mono uppercase tracking-wider text-muted">Alegação</div>
          <h3 className="text-[15.5px] font-medium text-text leading-snug">{x.alegacao}</h3>
          <p className="text-[14.5px] text-muted leading-relaxed"><b className="font-medium text-text">Resposta curta: </b>{x.resposta}</p>
          <div className="mt-auto pt-1 flex flex-wrap gap-1.5">
            {x.perguntas.map((q) => <a key={q} href={`#/respostas/${q}`} className="font-mono text-xs h-7 px-2.5 inline-flex items-center rounded-md border border-border hover:border-border-strong">{q}</a>)}
            {x.testes.map((t) => <a key={t} href={`#/testes/${t}`} className="font-mono text-xs h-7 px-2.5 inline-flex items-center rounded-md border border-border bg-surface-2 hover:border-border-strong">{t}</a>)}
          </div>
        </li>
      );
  const vis = max ? a.itens.slice(0, max) : a.itens, resto = max ? a.itens.slice(max) : [];
  return (
    <div className="grid gap-3">
      {titulo && <div className="max-w-[46rem]"><h2 className="t-h2">{a.titulo}</h2><p className="t-lead mt-3 text-[17px]">{a.frase}</p></div>}
      <ul className="grid gap-3 md:grid-cols-2">{vis.map(cartao)}</ul>
      {resto.length > 0 && <details className="group/al">
        <summary className="cursor-pointer list-none inline-flex items-center gap-2 min-h-10 text-[14px] font-medium text-accent-text [&::-webkit-details-marker]:hidden"><span className="transition-transform group-open/al:rotate-90" aria-hidden="true">▸</span><span className="group-open/al:hidden">Mais {resto.length} alegações com resposta curta</span><span className="hidden group-open/al:inline">Recolher</span></summary>
        <ul className="mt-2 grid gap-3 md:grid-cols-2">{resto.map(cartao)}</ul>
      </details>}
      <p className="text-[13px] text-muted">{a.situacao}</p>
    </div>
  );
}
