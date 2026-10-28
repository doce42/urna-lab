// Tela de carregamento da primeira visita: símbolo animado, etapa real, barra com MB baixados e erro com "tentar de novo".
import { useEffect, useState } from 'react';
import { Urna } from './Marca';
import { Botao } from './base';
import { P } from '@/lib/formato';
import type { Progresso } from '@/lib/dados';

export function Carregando({ etapa, progresso, erro, aoTentar, pronto }: { etapa: string; progresso: Progresso | null; erro: Error | null; aoTentar: () => void; pronto: boolean }) {
  const [saindo, setSaindo] = useState(false);
  const [sumiu, setSumiu] = useState(false);
  useEffect(() => {
    if (!pronto) return;
    setSaindo(true);
    const t = setTimeout(() => setSumiu(true), 500);
    return () => clearTimeout(t);
  }, [pronto]);
  if (sumiu) return null;
  const total = progresso?.total || 0, lido = progresso?.lido || 0;
  const pctN = total ? Math.min(100, (100 * lido) / total) : 0;
  const indeterminada = !total || progresso?.etapa === 'Montando';
  const sub = erro ? '' : progresso && progresso.etapa === 'Baixando' ? (total ? `${P(lido / 1048576, 1)} de ${P(total / 1048576, 1)} MB` : `${P(lido / 1048576, 1)} MB`) : '';
  return (
    <div className="carregando" data-saindo={saindo ? '1' : '0'} role="status" aria-live="polite" aria-busy={!pronto}>
      <div className="w-[min(92vw,380px)] flex flex-col items-center text-center gap-5">
        <div className="flex items-center gap-3">
          <Urna tamanho={44} animado={!erro} />
          <span className="font-semibold text-[2rem] tracking-[-.04em] leading-none">urna lab</span>
        </div>
        {erro ? (
          <div className="w-full flex flex-col items-center gap-3 surgir">
            <div className="text-erro font-medium">Não foi possível carregar os dados.</div>
            <p className="text-sm text-muted">{erro.message}</p>
            <Botao variante="primario" onClick={aoTentar}>Tentar de novo</Botao>
          </div>
        ) : (
          <div className="w-full flex flex-col items-center gap-3">
            <div className="text-[15px] text-text font-medium" aria-live="polite">{etapa}</div>
            <div className="barra-prog w-full" data-indeterminada={indeterminada ? '1' : '0'} aria-hidden="true"><i style={{ width: `${pctN}%` }} /></div>
            <div className="h-5 font-mono text-xs text-subtle t-num">{sub}</div>
          </div>
        )}
        <p className="text-xs text-subtle max-w-[32ch]">Estudo independente com dados oficiais do TSE. Nada aqui é conclusão definitiva.</p>
      </div>
    </div>
  );
}

// barra fina no topo para carregamentos posteriores (sob demanda, por página ou teste)
export function BarraTopo({ ativos }: { ativos: number }) {
  const [largura, setLargura] = useState(0);
  const [visivel, setVisivel] = useState(false);
  useEffect(() => {
    let timer: number | undefined;
    if (ativos > 0) {
      setVisivel(true); setLargura(18);
      timer = window.setInterval(() => setLargura((l) => Math.min(88, l + (90 - l) * 0.12)), 220);
    } else {
      setLargura(100);
      timer = window.setTimeout(() => { setVisivel(false); setLargura(0); }, 450);
    }
    return () => { clearInterval(timer); clearTimeout(timer); };
  }, [ativos]);
  return <div className="barra-topo" aria-hidden="true"><i style={{ width: `${largura}%`, opacity: visivel ? 1 : 0 }} /></div>;
}
