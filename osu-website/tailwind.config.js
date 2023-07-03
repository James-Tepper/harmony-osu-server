const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  mode: "jit",
  content: [
    ['./dist/*.{html,js,jsx,ts,tsx}'],
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter var", ...defaultTheme.fontFamily.sans],
    },
  },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
