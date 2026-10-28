import { useEffect, useState } from 'react';
import { useRota } from '@/lib/rotas';
import { carregar, onAtividade, useDados, type Progresso } from '@/lib/dados';
import type { Registro, Home as HomeDados, Meta } from '@/lib/tipos';
import { Carregando, BarraTopo } from '@/ui/Carregando';
import { Cabecalho, Rodape } from '@/ui/Casca';
import { DicaGlobal } from '@/ui/Dica';
import { Erro, SkeletonBloco } from '@/ui/base';
import { Home } from '@/paginas/Home';
import { Testes } from '@/paginas/Testes';
import { Mapas } from '@/paginas/Mapas';
import { Docs } from '@/paginas/Docs';
import { LinhaDoTempo } from '@/paginas/LinhaDoTempo';
import { Respostas } from '@/paginas/Respostas';

export default function App() {
  const rota = useRota();
  // primeira carga: registro de testes + dados da página inicial (tela cheia com progresso)
  const [etapa, setEtapa] = useState('Lendo o registro de testes…');
  const [progresso, setProgresso] = useState<Progresso | null>(null);
  const [erro, setErro] = useState<Error | null>(null);
  const [reg, setReg] = useState<Registro | null>(null);
  const [meta, setMeta] = useState<Meta | null>(null);
  const [tentativa, setTentativa] = useState(0);
  const [ativos, setAtivos] = useState(0);
  useEffect(() => onAtividade(setAtivos), []);
  useEffect(() => {
    let vivo = true; setErro(null);
    (async () => {
      try {
        setEtapa('Lendo o registro de testes…');
        const [r, m] = await Promise.all([carregar<Registro>('registro'), carregar<Meta>('meta').catch(() => null)]);
        if (!vivo) return; setReg(r); setMeta(m);
        if (rota.pagina === 'home') { setEtapa('Baixando os resultados da apuração…'); await carregar<HomeDados>('home', (p) => vivo && setProgresso(p)); }
        setEtapa('Montando os gráficos…'); setProgresso({ lido: 1, total: 1, etapa: 'Montando' });
        await new Promise((f) => setTimeout(f, 120));
      } catch (e) { if (vivo) setErro(e as Error); }
    })();
    return () => { vivo = false; };
  }, [tentativa]);
  useEffect(() => { if (!rota.hash.includes('/')) scrollTo({ top: 0 }); }, [rota.pagina]);
  useEffect(() => { document.title = { home: 'urna lab · apuração presidencial 2026, verificada com dados oficiais', testes: 'Testes · urna lab', mapas: 'Mapas · urna lab', linha: 'Evolução da pesquisa · urna lab', respostas: 'Perguntas e respostas científicas · urna lab', docs: 'Docs e ajuda · urna lab' }[rota.pagina]; }, [rota.pagina]);
  const pronto = !!reg && !erro && (rota.pagina !== 'home' || progresso?.etapa === 'Montando');
  return (
    <>
      <Carregando etapa={etapa} progresso={progresso} erro={erro} aoTentar={() => setTentativa((t) => t + 1)} pronto={pronto} />
      <BarraTopo ativos={pronto ? ativos : 0} />
      <Cabecalho rota={rota} meta={meta} />
      <main id="conteudo" className="min-h-[70vh]">
        {reg && (
          rota.pagina === 'home' ? <HomeCarregada reg={reg} meta={meta} /> :
          rota.pagina === 'testes' ? <Testes reg={reg} meta={meta} partes={rota.partes} /> :
          rota.pagina === 'mapas' ? <Mapas /> : rota.pagina === 'linha' ? <LinhaDoTempo reg={reg} /> : rota.pagina === 'respostas' ? <Respostas reg={reg} /> : <Docs partes={rota.partes} meta={meta} />
        )}
      </main>
      <Rodape meta={meta} />
      <DicaGlobal />
    </>
  );
}
function HomeCarregada({ reg, meta }: { reg: Registro; meta: Meta | null }) {
  const { dados, erro, recarregar } = useDados<HomeDados>('home');
  if (erro) return <div className="container pt-16"><Erro erro={erro} aoTentar={recarregar} /></div>;
  if (!dados) return <div className="container pt-16 grid gap-4"><SkeletonBloco altura={120} className="max-w-xl" /><SkeletonBloco altura={360} /></div>;
  return <Home h={dados} reg={reg} meta={meta} />;
}
