module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  purge: {
    enabled: false, //true for production build
    content: ["../**/templates/*.html", "../**/templates/**/*.html"],
  },
  theme: {
    extend: {
      colors: {
        primary: "#222221",
        primary2: "#242424",
        primary3: "#1e1e1e",
        primary4: "#202020",
        primary5: "#2f2f2f",
        primary6: "#1f1f1f",
        primary7: "#151516",
        secondary: "#dededf",
        secondary2: "#7a7a7a",
        secondary3: "#a5a5a6",
        golden: "#ab6e36",
      },
      fontFamily: {
        jura: ['"Jura"', "sans-serif"],
      },
      rotate: {
        "30": "30deg"
      }
    },
  },
  variants: {},
  plugins: [],
};
