// Cabeçalho, navegação e rodapé.
import { useEffect, useState } from 'react';
import { clsx } from 'clsx';
import { Github, Menu, Moon, Sun, X, FileDown } from 'lucide-react';
import { Logo, Urna } from './Marca';
import { Botao, BotaoLink } from './base';
import { useTema } from '@/lib/tema';
import { href, type Rota } from '@/lib/rotas';
import type { Meta } from '@/lib/tipos';

const ITENS: { rota: Rota['pagina']; rotulo: string; h: string }[] = [
  { rota: 'home', rotulo: 'Início', h: '/' }, { rota: 'testes', rotulo: 'Testes', h: '/testes' }, { rota: 'mapas', rotulo: 'Mapas', h: '/mapas' }, { rota: 'linha', rotulo: 'Linha do tempo', h: '/linha-do-tempo' }, { rota: 'docs', rotulo: 'Docs e ajuda', h: '/docs' },
];
export function Cabecalho({ rota, meta }: { rota: Rota; meta: Meta | null }) {
  const { efetivo, alternar } = useTema();
  const [aberto, setAberto] = useState(false);
  const [rolou, setRolou] = useState(false);
  useEffect(() => { const f = () => setRolou(scrollY > 8); f(); addEventListener('scroll', f, { passive: true }); return () => removeEventListener('scroll', f); }, []);
  useEffect(() => { setAberto(false); }, [rota.hash]);
  useEffect(() => { document.body.style.overflow = aberto ? 'hidden' : ''; return () => { document.body.style.overflow = ''; }; }, [aberto]);
  const github = meta?.github || 'https://github.com/doce42/urna-lab';
  return (
    <header className={clsx('sticky top-0 z-40 transition-[background,box-shadow,border-color] duration-300 border-b', rolou ? 'bg-bg/85 backdrop-blur-md border-border' : 'bg-bg/0 border-transparent')} style={{ height: 'var(--topo)' }}>
      <div className="container h-full flex items-center gap-3">
        <a href="#/" className="shrink-0 rounded-md" aria-label="urna lab, início"><Logo tamanho={26} /></a>
        <nav className="hidden lg:flex items-center gap-1 ml-6" aria-label="Principal">
          {ITENS.map((i) => (
            <a key={i.rota} href={href(i.h)} aria-current={rota.pagina === i.rota ? 'page' : undefined}
              className={clsx('h-10 px-3.5 inline-flex items-center rounded-full text-[15px] font-medium transition-colors', rota.pagina === i.rota ? 'text-text bg-surface-2' : 'text-muted hover:text-text hover:bg-surface-2/70')}>
              {i.rotulo}
            </a>
          ))}
        </nav>
        <div className="ml-auto flex items-center gap-2">
          {meta?.pdf && <BotaoLink href="/relatorio.pdf" tamanho="sm" className="hidden lg:inline-flex" download><FileDown size={16} />Relatório em PDF</BotaoLink>}
          <BotaoLink href={github} target="_blank" rel="noopener" tamanho="sm" variante="secundario" className="hidden sm:inline-flex"><Github size={16} />GitHub</BotaoLink>
          <Botao icone tamanho="sm" variante="secundario" onClick={alternar} aria-label={efetivo === 'dark' ? 'Usar tema claro' : 'Usar tema escuro'} title="Alternar tema">
            {efetivo === 'dark' ? <Sun size={17} /> : <Moon size={17} />}
          </Botao>
          <Botao icone tamanho="sm" variante="secundario" className="lg:hidden" onClick={() => setAberto((a) => !a)} aria-expanded={aberto} aria-controls="menu-movel" aria-label="Abrir menu">
            {aberto ? <X size={18} /> : <Menu size={18} />}
          </Botao>
        </div>
      </div>
      {aberto && (
        <div id="menu-movel" className="lg:hidden fixed inset-x-0 bottom-0 bg-bg border-t border-border overflow-y-auto" style={{ top: 'var(--topo)' }}>
          <nav className="container py-4 flex flex-col gap-1" aria-label="Principal (móvel)">
            {ITENS.map((i) => (
              <a key={i.rota} href={href(i.h)} aria-current={rota.pagina === i.rota ? 'page' : undefined}
                className={clsx('h-12 px-4 flex items-center rounded-lg text-lg font-medium', rota.pagina === i.rota ? 'bg-surface-2 text-text' : 'text-muted')}>{i.rotulo}</a>
            ))}
            <div className="mt-3 flex flex-wrap gap-2">
              <BotaoLink href={github} target="_blank" rel="noopener"><Github size={16} />Repositório no GitHub</BotaoLink>
              {meta?.pdf && <BotaoLink href="/relatorio.pdf" download><FileDown size={16} />Relatório em PDF</BotaoLink>}
            </div>
          </nav>
        </div>
      )}
    </header>
  );
}

export function Rodape({ meta }: { meta: Meta | null }) {
  const github = meta?.github || 'https://github.com/doce42/urna-lab';
  return (
    <footer className="mt-24 border-t border-border bg-surface/60">
      <div className="container py-12 grid gap-10 md:grid-cols-[1.4fr_1fr_1fr]">
        <div className="max-w-md">
          <Logo tamanho={22} />
          <p className="mt-4 text-sm text-muted leading-relaxed">
            Estudo independente, imparcial e reproduzível da apuração presidencial brasileira de 2026, com 2022 como referência.
            Só dados oficiais do TSE (dados abertos e arquivos gravados por cada urna). Não é órgão oficial e não tem vínculo com candidatos ou partidos.
          </p>
          <p className="mt-4 inline-flex items-center gap-2 text-[13px] text-muted"><i className="w-2 h-2 rounded-full bg-warn shrink-0" />Estudo em andamento: parte dos testes ainda será feita · dados de {meta?.gerado_em ? meta.gerado_em.split('-').reverse().join('/') : '—'}</p>
          <p className="mt-2 text-xs text-subtle">Código MIT · documentação e resultados CC BY 4.0</p>
        </div>
        <div>
          <div className="t-eyebrow mb-3">Navegar</div>
          <ul className="grid gap-2 text-sm">
            {ITENS.map((i) => <li key={i.rota}><a className="text-muted hover:text-text" href={href(i.h)}>{i.rotulo}</a></li>)}
            {meta?.pdf && <li><a className="text-muted hover:text-text" href="/relatorio.pdf" download>Relatório completo em PDF</a></li>}
          </ul>
        </div>
        <div>
          <div className="t-eyebrow mb-3">Reproduzir e contestar</div>
          <ul className="grid gap-2 text-sm">
            <li><a className="text-muted hover:text-text" href={github} target="_blank" rel="noopener">Repositório no GitHub</a></li>
            <li><a className="text-muted hover:text-text" href="#/docs/pipeline">Como reproduzir</a></li>
            <li><a className="text-muted hover:text-text" href="#/docs/contribuir">Como contribuir e discordar</a></li>
            <li><a className="text-muted hover:text-text" href="#/docs/consumo">Consumo de IA do estudo</a></li>
          </ul>
        </div>
      </div>
      <div className="container pb-10 flex flex-wrap items-center gap-3 text-xs text-subtle">
        <Urna tamanho={14} />
        <span>Nada aqui afirma ou nega fraude além do que os números sustentam. Significância estatística não é prova de manipulação, e ausência de achado não é prova de inexistência.</span>
      </div>
    </footer>
  );
}
