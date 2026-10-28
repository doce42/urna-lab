// Formatação de números em pt-BR. Tudo o que aparece na tela passa por aqui.
export const N = (n: number | null | undefined) => (n == null || Number.isNaN(n) ? '—' : Math.round(n).toLocaleString('pt-BR'));
export const P = (n: number | null | undefined, d = 2) =>
  n == null || Number.isNaN(n) ? '—' : n.toLocaleString('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });
export const SG = (v: number | null | undefined, d = 3) => (v == null ? '—' : (v >= 0 ? '+' : '−') + P(Math.abs(v), d));
export const PP = (v: number | null | undefined, d = 1) => (v == null ? '—' : SG(v, d) + ' pp');
export const compacto = (n: number) =>
  Math.abs(n) >= 1e6 ? P(n / 1e6, n % 1e6 === 0 ? 0 : 1) + ' mi' : Math.abs(n) >= 1e4 ? P(n / 1e3, 0) + ' mil' : N(n);
export const milhoes = (n: number, d = 1) => P(n / 1e6, d) + ' mi';
export const votosMil = (v: number) =>
  (v >= 0 ? '+' : '−') + (Math.abs(v) >= 1e6 ? P(Math.abs(v) / 1e6, 2) + ' mi' : N(Math.abs(v) / 1e3) + ' mil');
export const num = (s: string) => parseFloat(String(s).replace(/\./g, '').replace(',', '.').replace('−', '-'));
export const pct = (a: number, b: number) => (b ? a / b : 0);
export const nice = (x: number) => {
  const p = Math.pow(10, Math.floor(Math.log10(x || 1))), f = x / p;
  return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * p;
};
export const minutoHora = (m: number) => {
  const h = Math.floor(m / 60), mi = m % 60;
  return `${String(h).padStart(2, '0')}:${String(mi).padStart(2, '0')}`;
};
export const segHora = (s: number) => minutoHora(Math.floor(s / 60));
export const UF: Record<string, string> = {
  RO: 'Rondônia', AC: 'Acre', AM: 'Amazonas', RR: 'Roraima', PA: 'Pará', AP: 'Amapá', TO: 'Tocantins', MA: 'Maranhão', PI: 'Piauí', CE: 'Ceará',
  RN: 'Rio Grande do Norte', PB: 'Paraíba', PE: 'Pernambuco', AL: 'Alagoas', SE: 'Sergipe', BA: 'Bahia', MG: 'Minas Gerais', ES: 'Espírito Santo',
  RJ: 'Rio de Janeiro', SP: 'São Paulo', PR: 'Paraná', SC: 'Santa Catarina', RS: 'Rio Grande do Sul', MS: 'Mato Grosso do Sul', MT: 'Mato Grosso',
  GO: 'Goiás', DF: 'Distrito Federal', ZZ: 'Exterior',
};
export const REG: Record<string, string[]> = {
  Norte: 'AC AM AP PA RO RR TO'.split(' '), Nordeste: 'AL BA CE MA PB PE PI RN SE'.split(' '), 'Centro-Oeste': 'DF GO MS MT'.split(' '),
  Sudeste: 'ES MG RJ SP'.split(' '), Sul: 'PR RS SC'.split(' '),
};
export const regiaoDe = (uf: string) => Object.keys(REG).find((r) => REG[r].includes(uf)) || 'Exterior';
export const dataBR = (iso: string) => (iso && /^\d{4}-\d{2}-\d{2}/.test(iso) ? iso.slice(0, 10).split('-').reverse().join('/') : iso);
const TITULOS = /^(ESCRITOR|VETERINÁRIO|VETERINARIO|DR|DRA|DOUTOR|PROFESSOR|PROFESSORA|DELEGADO|CORONEL|CAPITÃO|CAPITAO|SARGENTO|PASTOR|GENERAL|SENADOR|GOVERNADOR|DEPUTADO|PADRE|BISPO)$/i;
export const nomeCurto = (n: string) =>
  ({ 'LUIZ INÁCIO LULA DA SILVA': 'Lula', 'FLAVIO NANTES BOLSONARO': 'Flávio Bolsonaro', LULA: 'Lula', 'FLAVIO BOLSONARO': 'Flávio Bolsonaro' } as Record<string, string>)[n] ||
  n.split(' ').filter((p) => p.length > 2 && !TITULOS.test(p)).slice(0, 2).map((p) => p[0] + p.slice(1).toLowerCase()).join(' ');
export const capitalizar = (s: string) => s.toLowerCase().replace(/(^|\s|-)(\p{L})/gu, (m) => m.toUpperCase()).replace(/\bD[aeo]s?\b/g, (m) => m.toLowerCase());
