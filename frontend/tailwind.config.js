/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        danger: '#ff0066',
        darkbg: '#0a0e27',
        darkcard: '#1a1f3a',
      },
      animation: {
        'pulse-danger': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1)',
        'glow': 'glow 2s ease-in-out infinite',
      },
      keyframes: {
        glow: {
          '0%, 100%': { textShadow: '0 0 10px #ff0066' },
          '50%': { textShadow: '0 0 20px #ff0066, 0 0 30px #ff0066' },
        }
      }
    },
  },
  plugins: [],
}
