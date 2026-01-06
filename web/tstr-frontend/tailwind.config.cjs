/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}',
    './public/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'navy-blue': '#000080',
        'navy-blue-dark': '#000066',
        'lime-green': '#32CD32',
        'lime-green-light': '#7FFF00',
      }
    },
  },
  plugins: [],
}
