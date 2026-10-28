// Símbolo da urna isométrica (identidade final) e logo completo. Cores por variável CSS: troca com o tema.
export function Urna({ tamanho = 28, animado = false, className = '' }: { tamanho?: number; animado?: boolean; className?: string }) {
  return (
    <svg width={tamanho} height={tamanho * (43 / 40)} viewBox="4 3 40 43" aria-hidden="true" className={`urna ${className}`} style={{ overflow: 'visible' }}>
      <path fill="var(--accent)" d="M24 5 L42 14.5 L24 24 L6 14.5Z" />
      <path fill="var(--brand)" d="M6 14.5 L24 24 V44 L6 34.5Z" />
      <path fill="var(--brand)" opacity=".72" d="M42 14.5 L24 24 V44 L42 34.5Z" />
      {animado && <rect className="voto" x="21.5" y="2" width="5" height="9" rx="1.2" fill="var(--brand)" opacity="0" transform="rotate(27 24 10)" />}
      <path className="fenda" d="M18.5 12.2 L29.5 17.8" stroke="#1B1D21" strokeWidth="3.4" strokeLinecap="round" />
    </svg>
  );
}
export function Logo({ tamanho = 26, className = '' }: { tamanho?: number; className?: string }) {
  return (
    <span className={`inline-flex items-center gap-2.5 ${className}`} aria-label="urna lab">
      <Urna tamanho={tamanho} />
      <span className="font-sans font-semibold text-text" style={{ fontSize: tamanho * 0.86, letterSpacing: '-.04em', lineHeight: 1 }}>urna lab</span>
    </span>
  );
}
