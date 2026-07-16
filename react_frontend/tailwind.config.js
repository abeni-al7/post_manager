/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        fortune: {
          maroon: '#800000',
          'dark-maroon': '#420909',
          green: '#008000',
          'light-blue': '#b3c7e3',
          'light-gray': '#e4ebf5',
          border: '#cccccc',
        }
      },
      fontFamily: {
        'headline': ['Verdana', 'Geneva', 'sans-serif'],
        'body': ['Verdana', 'Geneva', 'sans-serif'],
      }
    },
  },
  plugins: [],
}