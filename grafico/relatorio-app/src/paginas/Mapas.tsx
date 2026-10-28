import { useMemo, useState } from 'react';
import { sum } from 'd3-array';
import type { Topology } from 'topojson-specification';
import type { Mapas as MapasDados, Mapas2022 } from '@/lib/tipos';
import { useDados } from '@/lib/dados';
import { N, P, PP, votosMil, UF, capitalizar } from '@/lib/formato';
import { Botao, Eyebrow, SkeletonBloco, Erro, Nota } from '@/ui/base';
import { Mapa } from '@/graficos/Mapa';
import { Sankey, Bolhas, Klimek, BarrasUF } from '@/graficos/especiais';
import { COR, Tabela } from '@/graficos/comum';

const Sec = ({ id, eyebrow, titulo, lead, children }: { id: string; eyebrow: string; titulo: string; lead?: string; children: React.ReactNode }) => (
  <section id={id} className="mt-16 md:mt-20 scroll-mt-20"><div className="max-w-[46rem]"><Eyebrow>{eyebrow}</Eyebrow><h2 className="t-h2 mt-2">{titulo}</h2>{lead && <p className="t-lead mt-3 text-[17px]">{lead}</p>}</div><div className="mt-6">{children}</div></section>
);
const Toggle = ({ opcoes, valor, setValor, rotulo }: { opcoes: [string, string][]; valor: string; setValor: (v: string) => void; rotulo: string }) => (
  <div className="inline-flex items-center gap-1.5 flex-wrap" role="group" aria-label={rotulo}><span className="text-[13px] text-muted mr-1">{rotulo}</span>{opcoes.map(([k, r]) => <Botao key={k} tamanho="sm" variante={valor === k ? 'primario' : 'secundario'} aria-pressed={valor === k} onClick={() => setValor(k)}>{r}</Botao>)}</div>
);

export function Mapas() {
  const { dados: m, erro, recarregar } = useDados<MapasDados>('mapas');
  const { dados: topo } = useDados<Topology>('geo');
  const [ano, setAno] = useState('2026');
  const [med, setMed] = useState<'lula2' | 'virada'>('lula2');
  const { dados: m22 } = useDados<Mapas2022>(ano === '2022' || true ? 'mapas-2022' : null);
  const [anoB, setAnoB] = useState('2026');
  const [uf, setUf] = useState('BR');
  const [turno4, setTurno4] = useState('2t');
  const [cand4, setCand4] = useState('lula');

  const idx = useMemo(() => { const o = new Map<number, number>(); m?.codigos.forEach((c, i) => o.set(+c, i)); return o; }, [m]);
  const valor = useMemo(() => (cod: number) => { if (!m) return null; const i = idx.get(cod); if (i == null) return null; if (ano === '2026') return m.municipios[i][med === 'lula2' ? 1 : 2]; const r = m22?.municipios[i]; return r ? r[med === 'lula2' ? 1 : 2] : null; }, [m, m22, idx, ano, med]);
  const dadosUf = useMemo(() => (cod: number) => { if (!m) return null; const i = idx.get(cod); if (i == null) return null; if (ano === '2026') { const r = m.municipios[i]; return { lula1: r[0], lula2: r[1], virada: r[2], eleitores: r[5] }; } const r = m22?.municipios[i]; return r ? { lula1: r[0], lula2: r[1], virada: r[2], eleitores: r[3] } : null; }, [m, m22, idx, ano]);
  const nome = (cod: number) => { const i = idx.get(cod); return i == null ? String(cod) : `${capitalizar(m!.nomes[i])} (${m!.uf[i]})`; };

  const pts = useMemo(() => { if (!m) return []; if (anoB === '2026') return m.municipios.map((r, i) => ({ nome: capitalizar(m.nomes[i]), uf: m.uf[i], lula1: r[0], lula2: r[1], virada: r[2], eleitores: r[5] })).filter((p) => p.virada != null);
    return (m22?.municipios || []).map((r, i) => r ? { nome: capitalizar(m.nomes[i]), uf: m.uf[i], lula1: r[0], lula2: r[1], virada: r[2], eleitores: r[3] } : null).filter((p): p is NonNullable<typeof p> => !!p && p.virada != null); }, [m, m22, anoB]);
  const ufLinhas = useMemo(() => m ? Object.keys(m.ufs['2026']).map((k) => ({ k, v: m.ufs['2026'][k].virada, ref: m.ufs['2022']?.[k]?.virada ?? null, dica: `<b>${UF[k] || k}</b><br>Lula ${P(m.ufs['2026'][k].lula1, 1)}% → ${P(m.ufs['2026'][k].lula2, 1)}% (${PP(m.ufs['2026'][k].virada)})<br>2022: ${m.ufs['2022']?.[k] ? PP(m.ufs['2022'][k].virada) : '—'}` })).sort((a, b) => b.v - a.v) : [], [m]);
  const contrib = useMemo(() => m ? Object.entries(m.ufs['2026']).map(([k, u]) => ({ k, v: u.ganho_lula - u.ganho_adv, ref: null, dica: `<b>${UF[k] || k}</b><br>mudança na diferença Lula − Flávio: ${votosMil(u.ganho_lula - u.ganho_adv)} votos` })).sort((a, b) => b.v - a.v) : [], [m]);
  const cidades = useMemo(() => m ? m.municipios.map((r, i) => ({ nome: capitalizar(m.nomes[i]), uf: m.uf[i], d: r[6] - r[7], virada: r[2] })).sort((a, b) => b.d - a.d).slice(0, 20) : [], [m]);
  const top3 = contrib.slice(0, 3), tot = sum(contrib, (e) => e.v), soma3 = sum(top3, (e) => e.v);
  const fluxo = m?.fluxo['2026'];
  const V = fluxo ? (uf === 'BR' ? fluxo.votos : fluxo.por_uf[uf]) : null;
  const k26 = m?.klimek20['2026']?.[`${turno4}_${cand4}`], k22 = m?.klimek20['2022']?.[`${turno4}_${cand4}`];
  const canto = (G: number[][]) => G[18][18] + G[18][19] + G[19][18] + G[19][19];
  const totG = (G: number[][]) => sum(G.flat());
  const nomeC = (a: string) => (cand4 === 'lula' ? 'Lula' : a === '2026' ? 'Flávio Bolsonaro' : 'Bolsonaro');

  return (
    <div className="container pt-10 md:pt-16 pb-8">
      <div className="max-w-[52rem]"><Eyebrow>Mapas · o que mudou entre os turnos</Eyebrow><h1 className="t-h1 mt-2">O resultado e a virada, município por município.</h1><p className="t-lead mt-4">Cada bloco responde a uma pergunta no próprio título. Dados oficiais do TSE; a malha do IBGE serve só para desenhar. 2022 aparece como referência.</p></div>
      {erro && <div className="mt-8"><Erro erro={erro} aoTentar={recarregar} /></div>}

      <Sec id="mapa" eyebrow="Pergunta 1" titulo="Como fica no mapa?" lead="Verde-azulado = mais para Lula; violeta = mais para Flávio Bolsonaro; cinza = equilíbrio (50% no resultado, zero na virada). As cores dos candidatos vêm da legenda, não da marca de nenhum lado.">
        <div className="cartao p-4 md:p-6">
          <div className="flex flex-wrap gap-4 mb-4">
            <Toggle rotulo="Mostrar" valor={med} setValor={(v) => setMed(v as 'lula2' | 'virada')} opcoes={[['lula2', 'Resultado do 2º turno'], ['virada', 'Quanto Lula cresceu']]} />
            <Toggle rotulo="Eleição" valor={ano} setValor={setAno} opcoes={[['2026', '2026'], ['2022', '2022']]} />
          </div>
          {m && topo ? <div className="max-w-[720px] mx-auto"><Mapa topo={topo} valor={valor} nome={nome} medida={med} uf={dadosUf} titulo={med === 'lula2' ? `Lula no 2º turno de ${ano}, % dos válidos por município` : `Quanto Lula cresceu do 1º para o 2º turno de ${ano}, por município`} /></div> : <SkeletonBloco altura={520} />}
        </div>
      </Sec>

      <Sec id="estados" eyebrow="Pergunta 2" titulo={m ? `Lula cresceu nos ${ufLinhas.filter((l) => l.v > 0).length} estados; mais em ${UF[ufLinhas[0]?.k]} (${PP(ufLinhas[0]?.v)}) e menos em ${UF[ufLinhas[ufLinhas.length - 1]?.k]} (${PP(ufLinhas[ufLinhas.length - 1]?.v)})` : 'Onde Lula cresceu em percentual?'} lead="Cada barra é um estado: quantos pontos percentuais Lula ganhou do 1º para o 2º turno (votos válidos). O ponto cinza é o mesmo número em 2022.">
        <div className="grid gap-4 lg:grid-cols-2 items-start">
          <div className="cartao p-4 md:p-6">{m ? <BarrasUF linhas={ufLinhas} titulo="Quanto Lula cresceu por estado (pp dos válidos)" fmt={(v) => PP(v, 0).replace(' pp', '')} /> : <SkeletonBloco altura={600} />}</div>
          <div className="grid gap-4">
            <div className="cartao p-4 md:p-6">{m ? <BarrasUF linhas={contrib} titulo={`${top3.map((e) => UF[e.k]).join(', ')} responderam por ${P((100 * soma3) / tot, 0)}% da mudança na diferença`} sub="Quanto cada estado mudou a diferença Lula − Flávio, em votos. Estados grandes pesam mais mesmo com virada menor." fmt={(v) => votosMil(v)} nomeBar="2026" nomeRef="" /> : <SkeletonBloco altura={600} />}</div>
            <div className="cartao p-4 md:p-6"><div className="text-[14px] font-semibold mb-2">20 cidades que mais mudaram a diferença</div>{m ? <div className="rolavel"><Tabela cab={['#', 'cidade', 'votos', 'virada']} linhas={cidades.map((c, i) => [String(i + 1), `${c.nome} (${c.uf})`, votosMil(c.d), PP(c.virada)])} /></div> : <SkeletonBloco altura={300} />}<Nota className="mt-2">Última coluna: quanto Lula cresceu em percentual na cidade.</Nota></div>
          </div>
        </div>
      </Sec>

      <Sec id="bolhas" eyebrow="Pergunta 3" titulo="A mudança foi parecida no país todo?" lead="Cada bolinha é um município, numa faixa por região. Quanto mais à direita, mais Lula cresceu ali. O tamanho é o número de eleitores; a linha tracejada é a média do país.">
        <div className="cartao p-4 md:p-6">
          <div className="mb-4"><Toggle rotulo="Eleição" valor={anoB} setValor={setAnoB} opcoes={[['2026', '2026'], ['2022', '2022']]} /></div>
          {m && pts.length ? <Bolhas pts={pts} nac={m.nacional[anoB].virada_nacional} titulo={`Virada por município em ${anoB}, por região`} /> : <SkeletonBloco altura={520} />}
        </div>
      </Sec>

      <Sec id="fluxo" eyebrow="Pergunta 4" titulo="De onde vieram os votos do 2º turno?" lead="À esquerda, em quem a pessoa votou no 1º turno (ou se não votou). À direita, o que fez no 2º. A espessura é o número de eleitores estimado por inferência ecológica (teste C06); não é o voto de cada pessoa.">
        <div className="cartao p-4 md:p-6">
          <div className="mb-4 flex items-center gap-2 flex-wrap"><label className="text-[13px] text-muted" htmlFor="sel-uf">Recorte</label>
            <select id="sel-uf" value={uf} onChange={(e) => setUf(e.target.value)} className="h-10 px-3 rounded-full border border-border bg-surface text-sm font-medium">
              <option value="BR">Brasil</option>{Object.keys(UF).filter((k) => k !== 'ZZ').sort((a, b) => UF[a].localeCompare(UF[b])).map((k) => <option key={k} value={k}>{UF[k]}</option>)}
            </select></div>
          {fluxo && V ? <Sankey f={fluxo} V={V} titulo={`Fluxo de eleitores, ${uf === 'BR' ? 'Brasil' : UF[uf]}`} /> : <SkeletonBloco altura={480} />}
          <details className="mt-3 text-[14px] text-muted"><summary className="cursor-pointer font-medium text-text">Houve gente que trocou de Flávio para Lula?</summary><p className="mt-2 leading-relaxed">Os números oficiais não permitem saber. O voto é secreto e só existem totais por seção: se numa seção 300 pessoas trocaram de Flávio para Lula e outras 300 de Lula para Flávio, o resultado é o mesmo de ninguém ter trocado. A estimativa acima (troca pequena) depende de supor que, dentro de cada estado, quem votou igual no 1º turno se comportou parecido. Ver o teste <a className="underline" href="#/testes/C06b">C06b</a>.</p></details>
        </div>
      </Sec>

      <Sec id="klimek" eyebrow="Pergunta 5" titulo={k26 && k22 ? `Não há um grupo separado do resto, mas a zona de alerta tem ${N(canto(k26))} seções em 2026 (${P((100 * canto(k26)) / totG(k26), 2)}%) contra ${N(canto(k22))} em 2022 (${P((100 * canto(k22)) / totG(k22), 2)}%)` : 'Há sinal de urna “enchida”?'} lead="Cada bolinha agrupa as seções com a mesma faixa de comparecimento (de baixo para cima) e de votos no candidato (da esquerda para a direita). Enchimento clássico apareceria como um grupo separado no canto de cima à direita. A diferença entre os anos está em investigação nos logs das urnas (T07, T25).">
        <div className="cartao p-4 md:p-6">
          <div className="flex flex-wrap gap-4 mb-4">
            <Toggle rotulo="Turno" valor={turno4} setValor={setTurno4} opcoes={[['2t', '2º turno'], ['1t', '1º turno']]} />
            <Toggle rotulo="Candidato" valor={cand4} setValor={setCand4} opcoes={[['lula', 'Lula'], ['adversario', 'Adversário']]} />
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            {k22 ? <Klimek G={k22} nomeC={nomeC('2022')} titulo={`2022 · ${turno4 === '2t' ? '2º' : '1º'} turno · ${nomeC('2022')}`} cor={COR.ref} /> : <SkeletonBloco altura={420} />}
            {k26 ? <Klimek G={k26} nomeC={nomeC('2026')} titulo={`2026 · ${turno4 === '2t' ? '2º' : '1º'} turno · ${nomeC('2026')}`} /> : <SkeletonBloco altura={420} />}
          </div>
        </div>
      </Sec>
    </div>
  );
}
