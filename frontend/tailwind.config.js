/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      animation: {
        fadeInOut: "fadeInOut 5s ease-out",
        wiggle: "wiggle 0.5s ease-in-out infinite",
      },
      keyframes: {
        fadeInOut: {
          "0%": { opacity: "0", transform: "translateX(-50%) translateY(5px)" },
          "10%": { opacity: "1", transform: "translateX(-50%) translateY(0)" },
          "90%": { opacity: "1", transform: "translateX(-50%) translateY(0)" },
          "100%": { opacity: "0", transform: "translateX(-50%) translateY(-5px)" },
        },
        wiggle: {
          "0%": { transform: "rotate(0deg)" },
          "25%": { transform: "rotate(3deg)" },
          "75%": { transform: "rotate(-3deg)" },
          "100%": { transform: "rotate(0deg)" },
        },
      },
    },
  },
  plugins: [],
};
