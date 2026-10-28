/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  darkMode: ['selector', '[data-theme="dark"]'],
  theme: {
    container: { center: true, padding: { DEFAULT: '16px', sm: '24px', lg: '32px' }, screens: { '2xl': '1280px' } },
    extend: {
      colors: {
        bg: 'var(--bg)', surface: 'var(--surface)', 'surface-2': 'var(--surface-2)',
        border: 'var(--border)', 'border-strong': 'var(--border-strong)',
        text: 'var(--text)', muted: 'var(--text-muted)', subtle: 'var(--text-subtle)',
        brand: 'var(--brand)', 'brand-contrast': 'var(--brand-contrast)',
        accent: 'var(--accent)', 'accent-text': 'var(--accent-text)', 'accent-soft': 'var(--accent-soft)',
        ok: 'var(--ok)', warn: 'var(--warn)', erro: 'var(--erro)',
      },
      fontFamily: { sans: 'var(--font-sans)', mono: 'var(--font-mono)' },
      borderRadius: { sm: 'var(--radius-sm)', DEFAULT: 'var(--radius)', lg: 'var(--radius-lg)', xl: '20px', '2xl': '28px' },
      boxShadow: { sm: 'var(--shadow-sm)', DEFAULT: 'var(--shadow)', lg: 'var(--shadow-lg)' },
      transitionTimingFunction: { out: 'cubic-bezier(.2,.8,.2,1)' },
    },
  },
  plugins: [],
};
