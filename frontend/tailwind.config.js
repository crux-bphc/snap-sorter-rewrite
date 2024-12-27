/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        gfs: ["GFS Didot"], // Replace 'custom' with your alias
      },
      colors: {
        background: "#1E1E1E", // Custom background color
        foreground: "#FFFFFF", // Custom foreground color
      },
    },
  },
  plugins: [],
};
