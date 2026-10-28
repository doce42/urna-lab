// Dica (tooltip) global: qualquer elemento com data-dica mostra o conteúdo ao passar o ponteiro ou tocar.
import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

export function DicaGlobal() {
  const [html, setHtml] = useState<string | null>(null);
  const [pos, setPos] = useState({ x: 0, y: 0 });
  const fixa = useRef(false);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const mover = (e: PointerEvent) => {
      if (e.pointerType === 'touch') return;
      const t = (e.target as Element).closest?.('[data-dica]') as HTMLElement | null;
      if (!t) { if (!fixa.current) setHtml(null); return; }
      fixa.current = false; setHtml(t.getAttribute('data-dica')); setPos({ x: e.clientX, y: e.clientY });
    };
    const clicar = (e: MouseEvent) => {
      const t = (e.target as Element).closest?.('[data-dica]') as HTMLElement | null;
      if (t && matchMedia('(pointer: coarse)').matches) { fixa.current = true; setHtml(t.getAttribute('data-dica')); setPos({ x: e.clientX, y: e.clientY }); }
      else if (!t) { fixa.current = false; setHtml(null); }
    };
    const sair = () => { if (!fixa.current) setHtml(null); };
    document.addEventListener('pointermove', mover, { passive: true });
    document.addEventListener('click', clicar);
    document.addEventListener('scroll', sair, { passive: true, capture: true });
    return () => { document.removeEventListener('pointermove', mover); document.removeEventListener('click', clicar); document.removeEventListener('scroll', sair, { capture: true } as EventListenerOptions); };
  }, []);
  useEffect(() => {
    const el = ref.current; if (!el || !html) return;
    const w = el.offsetWidth, h = el.offsetHeight, vw = innerWidth, vh = innerHeight;
    let left = pos.x + 14, top = pos.y + 14;
    if (left + w > vw - 8) left = Math.max(8, pos.x - w - 14);
    if (top + h > vh - 8) top = Math.max(8, pos.y - h - 12);
    el.style.left = left + 'px'; el.style.top = top + 'px';
  }, [html, pos]);
  if (!html) return null;
  return createPortal(<div ref={ref} className="dica" role="tooltip" dangerouslySetInnerHTML={{ __html: html }} />, document.body);
}
export const esc = (s: unknown) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] as string));
export const dica = (html: string) => ({ 'data-dica': html });
