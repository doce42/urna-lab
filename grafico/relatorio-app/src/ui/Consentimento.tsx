import { useEffect, useState } from 'react';

const CHAVE = 'urnalab-privacidade';
const SDK = 'https://www.gstatic.com/firebasejs/13.1.0/';

type Escolha = 'aceito' | 'recusado' | null;
const ler = (): Escolha => { try { const v = localStorage.getItem(CHAVE); return v === 'aceito' || v === 'recusado' ? v : null; } catch { return null; } };
const gravar = (v: Escolha) => { try { if (v) localStorage.setItem(CHAVE, v); else localStorage.removeItem(CHAVE); } catch { /* sem armazenamento: vale só nesta visita */ } };
const naoRastrear = () => navigator.doNotTrack === '1' || (navigator as unknown as { globalPrivacyControl?: boolean }).globalPrivacyControl === true;

let carregado = false;
// o Analytics só entra depois do aceite; sem aceite nenhum script do Google é baixado
async function ligar() {
  if (carregado) return; carregado = true;
  try {
    // a configuração vem do próprio Hosting (não fica no repositório); fora do Hosting (dev) a medição simplesmente não liga
    const r = await fetch('/__/firebase/init.json', { cache: 'no-store' });
    if (!r.ok) throw new Error('sem configuração');
    const CONFIG = await r.json();
    if (!CONFIG.measurementId) throw new Error('sem measurementId');
    const app = await import(/* @vite-ignore */ SDK + 'firebase-app.js');
    const an = await import(/* @vite-ignore */ SDK + 'firebase-analytics.js');
    const a = app.initializeApp(CONFIG);
    (window as unknown as { __analytics?: unknown }).__analytics = { an: an.getAnalytics(a), log: an.logEvent };
  } catch { carregado = false; }
}
export function evento(nome: string, dados?: Record<string, string>) {
  const x = (window as unknown as { __analytics?: { an: unknown; log: (a: unknown, n: string, d?: unknown) => void } }).__analytics;
  if (x) try { x.log(x.an, nome, dados); } catch { /* medição nunca quebra a página */ }
}

export function Consentimento() {
  const [escolha, setEscolha] = useState<Escolha>(ler);
  const [aberta, setAberta] = useState(false);
  useEffect(() => { if (escolha === 'aceito' && !naoRastrear()) void ligar(); }, [escolha]);
  useEffect(() => {
    const abrir = () => setAberta(true);
    window.addEventListener('urnalab:privacidade', abrir);
    const clique = (e: MouseEvent) => { const a = (e.target as HTMLElement).closest('a'); const h = a?.getAttribute('href') || ''; if (/\.(pdf|csv|zip|parquet)(\?|$)/i.test(h)) evento('download', { arquivo: h.split('/').pop() || h }); };
    document.addEventListener('click', clique);
    return () => { window.removeEventListener('urnalab:privacidade', abrir); document.removeEventListener('click', clique); };
  }, []);
  if (naoRastrear() || (escolha && !aberta)) return null;
  const decidir = (v: Escolha) => { gravar(v); setEscolha(v); setAberta(false); };
  return (
    <div role="dialog" aria-label="Privacidade" className="fixed inset-x-0 bottom-0 z-50 border-t border-border bg-surface shadow-lg">
      <div className="container py-4 flex flex-wrap items-center gap-x-6 gap-y-3">
        <p className="text-sm text-muted leading-relaxed flex-1 min-w-[260px]">
          Posso medir os acessos com o Google Analytics para saber se o estudo está sendo lido? Só carrega se você aceitar, sem nome nem e-mail. <a className="underline hover:text-text" href="#/docs/privacidade">Detalhes</a>
        </p>
        <div className="flex gap-2">
          <button type="button" onClick={() => decidir('recusado')} className="px-4 py-2 rounded-md border border-border text-sm hover:bg-bg">Recusar</button>
          <button type="button" onClick={() => decidir('aceito')} className="px-4 py-2 rounded-md border border-border text-sm hover:bg-bg">Aceitar</button>
        </div>
      </div>
    </div>
  );
}
export const abrirPrivacidade = () => window.dispatchEvent(new Event('urnalab:privacidade'));
