/** Tailwind preset for wortlaut. Add to tailwind.config: presets: [require('./tailwind.preset.cjs')] */
module.exports = {
  theme: {
    extend: {
      colors: { wl: {
        "night": "#14213D",
        "night-900": "#0D1630",
        "night-700": "#1E2E52",
        "night-600": "#2C3F6A",
        "signal": "#FF6B2C",
        "signal-ink": "#BF3E0A",
        "paper": "#F4F1EA",
        "paper-200": "#EAE6DB",
        "line": "#DAD5C8",
        "slate": "#4A5470",
        "mist": "#AAB3C8",
        "hit-light": "#FFE0CC",
        "hit-dark": "#4A2A25",
        "error": "#B3261E",
        "success": "#1B7A4B"
} },
      fontFamily: {
        display: ['Space Grotesk', 'system-ui', 'sans-serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: { sm: '6px', md: '10px', lg: '16px' },
    },
  },
};
