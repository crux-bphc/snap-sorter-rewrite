/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,svelte}"],
  theme: {
    extend: {
      colors: {
        primary: "#007BFF", // Blue
        accent: "#5BC0DE", // Light Blue
      },
    },
  },
  plugins: [],
};
