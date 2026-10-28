// Carregamento dos arquivos de dados sob demanda, com progresso (ReadableStream) e cache em memória.
import { useEffect, useState, useCallback } from 'react';

export type Progresso = { lido: number; total: number; etapa: string };
const cache = new Map<string, unknown>();
const emCurso = new Map<string, Promise<unknown>>();
const ouvintes = new Set<(ativos: number) => void>();
let ativos = 0;
const avisar = () => ouvintes.forEach((f) => f(ativos));
export const onAtividade = (f: (ativos: number) => void) => { ouvintes.add(f); return () => { ouvintes.delete(f); }; };

async function baixar(url: string, aoProgredir?: (p: Progresso) => void): Promise<string> {
  const r = await fetch(url, { cache: 'default' });
  if (!r.ok) throw new Error(`Não foi possível baixar ${url.split('/').pop()} (HTTP ${r.status}).`);
  const total = +(r.headers.get('Content-Length') || 0);
  if (!r.body) return r.text();
  const leitor = r.body.getReader(), partes: Uint8Array[] = [];
  let lido = 0;
  for (;;) {
    const { done, value } = await leitor.read();
    if (done) break;
    partes.push(value); lido += value.length;
    aoProgredir?.({ lido, total, etapa: 'Baixando' });
  }
  return new Blob(partes as BlobPart[]).text();
}

export function carregar<T>(nome: string, aoProgredir?: (p: Progresso) => void): Promise<T> {
  if (cache.has(nome)) return Promise.resolve(cache.get(nome) as T);
  if (emCurso.has(nome)) return emCurso.get(nome) as Promise<T>;
  ativos++; avisar();
  const p = baixar(`/dados/${nome}.json`, aoProgredir)
    .then((t) => { aoProgredir?.({ lido: 1, total: 1, etapa: 'Montando' }); const d = JSON.parse(t) as T; cache.set(nome, d); return d; })
    .finally(() => { emCurso.delete(nome); ativos--; avisar(); });
  emCurso.set(nome, p);
  return p;
}
export const jaCarregado = (nome: string) => cache.has(nome);

export function useDados<T>(nome: string | null) {
  const [estado, setEstado] = useState<{ dados: T | null; erro: Error | null; progresso: Progresso | null }>(() => ({
    dados: nome && cache.has(nome) ? (cache.get(nome) as T) : null, erro: null, progresso: null,
  }));
  const [tentativa, setTentativa] = useState(0);
  useEffect(() => {
    if (!nome) return;
    let vivo = true;
    if (cache.has(nome)) { setEstado({ dados: cache.get(nome) as T, erro: null, progresso: null }); return; }
    setEstado((e) => ({ ...e, erro: null }));
    carregar<T>(nome, (p) => vivo && setEstado((e) => ({ ...e, progresso: p })))
      .then((d) => vivo && setEstado({ dados: d, erro: null, progresso: null }))
      .catch((erro) => vivo && setEstado({ dados: null, erro, progresso: null }));
    return () => { vivo = false; };
  }, [nome, tentativa]);
  const recarregar = useCallback(() => setTentativa((t) => t + 1), []);
  return { ...estado, recarregar };
}
