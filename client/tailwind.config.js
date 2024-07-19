/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial-light': 'radial-gradient(circle at top, hsl(213, 19%, 18%), rgb(15 23 42))',
      },
    },
  },
  plugins: [],
}
