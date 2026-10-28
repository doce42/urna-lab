import { useEffect, useState } from 'react';
export type Tema = 'auto' | 'light' | 'dark';
const CHAVE = 'urnalab-tema';
export function lerTema(): Tema {
  try { const t = localStorage.getItem(CHAVE); if (t === 'light' || t === 'dark') return t; } catch { /* sem armazenamento */ }
  return 'auto';
}
export function aplicarTema(t: Tema) {
  if (t === 'auto') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.setAttribute('data-theme', t);
  try { if (t === 'auto') localStorage.removeItem(CHAVE); else localStorage.setItem(CHAVE, t); } catch { /* ignora */ }
}
export function temaEfetivo(t: Tema): 'light' | 'dark' {
  if (t !== 'auto') return t;
  return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}
export function useTema() {
  const [tema, setTemaEstado] = useState<Tema>(lerTema);
  const [efetivo, setEfetivo] = useState<'light' | 'dark'>(() => temaEfetivo(lerTema()));
  useEffect(() => {
    const mq = matchMedia('(prefers-color-scheme: dark)');
    const f = () => setEfetivo(temaEfetivo(tema));
    mq.addEventListener('change', f);
    return () => mq.removeEventListener('change', f);
  }, [tema]);
  const setTema = (t: Tema) => { aplicarTema(t); setTemaEstado(t); setEfetivo(temaEfetivo(t)); };
  const alternar = () => setTema(efetivo === 'dark' ? 'light' : 'dark');
  return { tema, efetivo, setTema, alternar };
}
