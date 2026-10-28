// Roteamento por hash: #/ , #/testes , #/testes/T02 , #/mapas , #/docs/metodologia/secao
import { useEffect, useState } from 'react';

export type Rota = { pagina: 'home' | 'testes' | 'mapas' | 'docs'; partes: string[]; hash: string; query: string };

export function lerRota(): Rota {
  const h = location.hash.replace(/^#\/?/, '');
  const [caminho, query = ''] = h.split('?');
  const partes = caminho.split('/').filter(Boolean).map(decodeURIComponent);
  const p = partes[0] || '';
  const pagina: Rota['pagina'] = p === 'testes' ? 'testes' : p === 'mapas' ? 'mapas' : p === 'docs' ? 'docs' : 'home';
  return { pagina, partes: partes.slice(1), hash: h, query };
}
export function useRota() {
  const [rota, setRota] = useState(lerRota);
  useEffect(() => {
    const f = () => setRota(lerRota());
    window.addEventListener('hashchange', f);
    return () => window.removeEventListener('hashchange', f);
  }, []);
  return rota;
}
export const irPara = (h: string) => { location.hash = h.startsWith('#') ? h : '#/' + h.replace(/^\/+/, ''); };
export const href = (h: string) => (h.startsWith('#') ? h : '#/' + h.replace(/^\/+/, ''));
