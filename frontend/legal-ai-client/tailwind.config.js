// tailwind.config.js
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        // Apple-like palette (light-first)
        ink: "#0b0b0b",
        muted: "#6b7280",
        glass: "rgba(255,255,255,0.65)",
        // keep your neon names if Dashboard still uses them (no harm)
        "neon-blue": "#00eaff",
        "neon-teal": "#2df4c8",
        "neon-magenta": "#ff46c7",
        "bg-deep": "#0b0f19",
        "bg-deeper": "#05070d"
      },
      fontFamily: {
        sans: ['-apple-system','BlinkMacSystemFont','"Segoe UI"', 'Roboto', 'Arial','system-ui','sans-serif']
      },
      boxShadow: {
        subtle: '0 6px 18px rgba(16,24,40,0.06)',
        soft: '0 8px 40px rgba(16,24,40,0.08)'
      }
    }
  },
  plugins: []
};
