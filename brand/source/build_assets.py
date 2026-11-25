"""Builds logos, icons, social images, tokens and font files into ../wortlaut-brand."""
import json, os, shutil, io
import cairosvg
from PIL import Image
import brand_lib as B
from brand_lib import C

_HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.abspath(os.path.join(_HERE, ".."))
ROOT = os.environ.get("BRAND_OUT") or (_PARENT if os.path.basename(_PARENT) == "wortlaut-brand" else os.path.join(_PARENT, "wortlaut-brand"))
FONT_SRC = B.NODE


def out(path):
    p = os.path.join(ROOT, path); os.makedirs(os.path.dirname(p), exist_ok=True); return p


def write(path, text):
    open(out(path), "w", encoding="utf-8").write(text)


def png(svg_text, path, width=None, height=None, bg=None):
    kw = {}
    if width: kw["output_width"] = width
    if height: kw["output_height"] = height
    if bg: kw["background_color"] = bg
    cairosvg.svg2png(bytestring=svg_text.encode(), write_to=out(path), **kw)


MONO = {"color": (B.MARK_COLOR, C["night"], C["night"]), "reversed": (B.MARK_REV, C["paper"], C["paper"]),
        "black": (C["black"], C["black"], C["black"]), "white": (C["white"], C["white"], C["white"])}
SYM_FILL = {"color": B.MARK_COLOR, "reversed": B.MARK_REV, "black": C["black"], "white": C["white"]}

CONTRAST_PAIRS = [
    ("night on paper", C["night"], C["paper"], 4.5), ("night on white", C["night"], C["white"], 4.5),
    ("slate on paper", C["slate"], C["paper"], 4.5), ("slate on white", C["slate"], C["white"], 4.5),
    ("signal-ink on paper", C["signal-ink"], C["paper"], 4.5), ("signal-ink on white", C["signal-ink"], C["white"], 4.5),
    ("error on paper", C["error"], C["paper"], 4.5), ("success on paper", C["success"], C["paper"], 4.5),
    ("night on hit-light", C["night"], C["hit-light"], 4.5),
    ("paper on night", C["paper"], C["night"], 4.5), ("paper on night-900", C["paper"], C["night-900"], 4.5),
    ("mist on night", C["mist"], C["night"], 4.5), ("mist on night-700", C["mist"], C["night-700"], 4.5),
    ("paper on hit-dark", C["paper"], C["hit-dark"], 4.5),
    ("night on signal (w on marker)", C["night"], C["signal"], 4.5),
    ("signal on night (graphics, large text)", C["signal"], C["night"], 3.0),
    ("signal on night-900 (graphics, large text)", C["signal"], C["night-900"], 3.0),
]
CHART = ["#14213D", "#BF3E0A", "#1F7A8C", "#8A6A00"]


def contrast_table():
    rows = []
    for name, a, b, need in CONTRAST_PAIRS:
        v = B.contrast(a, b)
        assert v >= need, f"contrast fail {name}: {v:.2f} < {need}"
        rows.append((name, round(v, 1), need))
    for c in CHART:
        for bg in (C["paper"], C["white"]):
            assert B.contrast(c, bg) >= 3.0, f"chart colour {c} on {bg}"
    return rows


def build():
    for d in ("logo", "icon", "social", "fonts", "tokens"):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)
    # ---------------- logos
    for name, (m, c1, c2) in MONO.items():
        write(f"logo/svg/lockup-horizontal-{name}.svg", B.lockup_h_svg(m, c1, c2))
        write(f"logo/svg/lockup-stacked-{name}.svg", B.lockup_s_svg(m, c1, c2))
        write(f"logo/svg/wordmark-{name}.svg", B.wordmark_svg(c1, c2))
        bg = None
        png(B.lockup_h_svg(m, c1, c2), f"logo/png/lockup-horizontal-{name}.png", width=2000)
        png(B.lockup_s_svg(m, c1, c2), f"logo/png/lockup-stacked-{name}.png", width=1600)
        png(B.wordmark_svg(c1, c2), f"logo/png/wordmark-{name}.png", width=2000)
    for name, fill in SYM_FILL.items():
        write(f"logo/svg/symbol-{name}.svg", B.sym_svg("full", fill))
        png(B.sym_svg("full", fill), f"logo/png/symbol-{name}.png", width=1200)

    # ---------------- icons
    fav = B.tile_svg(64, "compact", B.MARK_REV, C["night"], radius_frac=0.2, mark_frac=0.72)
    write("icon/favicon.svg", fav)
    for s in (16, 32, 48):
        png(fav, f"icon/favicon-{s}.png", width=s)
    ims = [Image.open(out(f"icon/favicon-{s}.png")).convert("RGBA") for s in (48, 32, 16)]
    ims[0].save(out("icon/favicon.ico"), sizes=[(48, 48), (32, 32), (16, 16)], append_images=ims[1:])
    rounded = B.tile_svg(512, "full", B.MARK_REV, C["night"], radius_frac=0.225, mark_frac=0.58)
    write("icon/app-icon.svg", rounded)
    png(rounded, "icon/icon-512.png", width=512)
    png(rounded, "icon/icon-192.png", width=192)
    bleed = B.tile_svg(1024, "full", B.MARK_REV, C["night"], bleed=True, mark_frac=0.56)
    write("icon/app-icon-fullbleed.svg", bleed)
    png(bleed, "icon/app-icon-1024.png", width=1024)
    png(bleed, "icon/apple-touch-icon.png", width=180)
    mask = B.tile_svg(512, "full", B.MARK_REV, C["night"], bleed=True, mark_frac=0.46)
    png(mask, "icon/icon-maskable-512.png", width=512)
    write("icon/safari-pinned-tab.svg", B.sym_svg("compact", C["black"]))
    write("icon/site.webmanifest", json.dumps({
        "name": "Wortlaut", "short_name": "Wortlaut", "lang": "de",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
        "theme_color": C["night"], "background_color": C["paper"], "display": "standalone"}, indent=2) + "\n")

    # ---------------- social
    def banner(w, h, tagline, scale_w, path, sub_wt=400):
        lw, lh = B.lockup_h_size(); k = scale_w / lw
        lock = f'<g transform="translate({(w - lw * k) / 2:g},{(h - lh * k) / 2 - h * 0.06:g}) scale({k:.5f})">{B.lockup_h_body(B.MARK_REV, C["paper"], C["paper"])}</g>'
        size = h * 0.058
        tp, tw = B.text_path(tagline, size, sub_wt, C["mist"], 0.01)
        tag = f'<g transform="translate({(w - tw) / 2:g},{(h + lh * k) / 2 - h * 0.06 + h * 0.15:g})">{tp}</g>'
        s = B.svg(w, h, lock + tag, bg=C["night"])
        write(path + ".svg", s); png(s, path + ".png", width=w)
    banner(1200, 630, "suche in reden des deutschen bundestags", 800, "social/og-image-de")
    banner(1280, 640, "search German Bundestag speeches by word or phrase", 820, "social/github-social-preview-en")
    banner(1500, 500, "suche in reden des deutschen bundestags", 780, "social/banner-1500x500")
    av = B.tile_svg(1000, "full", B.MARK_REV, C["night"], bleed=True, mark_frac=0.56)
    png(av, "social/avatar-1000.png", width=1000)
    png(av, "social/github-org-avatar-500.png", width=500)

    # ---------------- fonts
    for fam, pkg, ws in (("Space Grotesk", "space-grotesk", (400, 500, 700)), ("Inter", "inter", (400, 500, 600))):
        for w in ws:
            src = f"{FONT_SRC}/{pkg}/files/{pkg}-latin-{w}-normal.woff2"
            shutil.copy(src, out(f"fonts/{pkg}-{w}.woff2"))
        shutil.copy(f"{FONT_SRC}/{pkg}/LICENSE", out(f"fonts/LICENSE-{pkg}.txt"))
    css = ""
    for fam, pkg, ws in (("Space Grotesk", "space-grotesk", (400, 500, 700)), ("Inter", "inter", (400, 500, 600))):
        for w in ws:
            css += (f"@font-face {{\n  font-family: '{fam}';\n  font-style: normal;\n  font-weight: {w};\n  font-display: swap;\n"
                    f"  src: url('./{pkg}-{w}.woff2') format('woff2');\n}}\n")
    write("fonts/fonts.css", css)

    # ---------------- tokens
    rows = contrast_table()
    light = {"bg": C["paper"], "surface": C["white"], "surface-sunken": C["paper-200"], "text": C["night"],
             "text-muted": C["slate"], "border": C["line"], "accent": C["signal-ink"], "accent-graphic": C["signal-ink"],
             "primary": C["night"], "on-primary": C["paper"], "hit-bg": C["hit-light"], "hit-text": C["night"],
             "focus": C["signal-ink"], "error": C["error"], "success": C["success"]}
    dark = {"bg": C["night-900"], "surface": C["night"], "surface-sunken": C["night-900"], "text": C["paper"],
            "text-muted": C["mist"], "border": C["night-600"], "accent": C["signal"], "accent-graphic": C["signal"],
            "primary": C["signal"], "on-primary": C["night"], "hit-bg": C["hit-dark"], "hit-text": C["paper"],
            "focus": C["signal"], "error": "#FF8A80", "success": "#6FD3A0"}
    assert B.contrast(dark["error"], C["night-900"]) >= 4.5 and B.contrast(dark["success"], C["night-900"]) >= 4.5
    tokens = {
        "name": "wortlaut", "version": "1.0.0",
        "color": {"palette": {k: v for k, v in C.items() if k not in ("black",)}, "light": light, "dark": dark,
                  "chart": CHART},
        "font": {"display": {"family": "Space Grotesk", "weights": [400, 500, 700], "fallback": "system-ui, sans-serif"},
                 "text": {"family": "Inter", "weights": [400, 500, 600], "fallback": "system-ui, sans-serif"}},
        "radius": {"sm": "6px", "md": "10px", "lg": "16px", "pill": "999px"},
        "space": {"1": "4px", "2": "8px", "3": "12px", "4": "16px", "6": "24px", "8": "32px", "12": "48px", "16": "64px"},
        "type-scale": {"display": "clamp(2.5rem, 6vw, 4.5rem)", "h1": "2.25rem", "h2": "1.5rem", "h3": "1.125rem",
                       "body": "1rem", "small": "0.875rem"},
        "contrast": {n: v for n, v, _ in rows},
    }
    write("tokens/tokens.json", json.dumps(tokens, indent=2, ensure_ascii=False) + "\n")

    def vars_(d, indent="  "):
        return "".join(f"{indent}--wl-{k}: {v};\n" for k, v in d.items())
    css = ("/* wortlaut design tokens. Light is the default; dark follows the system or data-theme=\"dark\". */\n"
           ":root {\n" + vars_(light) +
           "  --wl-signal: #FF6B2C;\n  --wl-font-display: 'Space Grotesk', system-ui, sans-serif;\n"
           "  --wl-font-text: 'Inter', system-ui, sans-serif;\n  --wl-radius-sm: 6px;\n  --wl-radius-md: 10px;\n"
           "  --wl-radius-lg: 16px;\n  --wl-radius-pill: 999px;\n}\n"
           "@media (prefers-color-scheme: dark) {\n  :root:not([data-theme=\"light\"]) {\n" + vars_(dark, "    ") + "  }\n}\n"
           ":root[data-theme=\"dark\"] {\n" + vars_(dark) + "}\n"
           "mark { background: var(--wl-hit-bg); color: var(--wl-hit-text); border-radius: 3px; padding: 0 .15em; }\n")
    write("tokens/brand.css", css)
    pal = {k: v for k, v in C.items() if k not in ("black", "white")}
    write("tokens/tailwind.preset.cjs",
          "/** Tailwind preset for wortlaut. Add to tailwind.config: presets: [require('./tailwind.preset.cjs')] */\n"
          "module.exports = {\n  theme: {\n    extend: {\n      colors: { wl: " + json.dumps(pal, indent=8).replace("\n    }", "\n      }") + " },\n"
          "      fontFamily: {\n        display: ['Space Grotesk', 'system-ui', 'sans-serif'],\n"
          "        sans: ['Inter', 'system-ui', 'sans-serif'],\n      },\n"
          "      borderRadius: { sm: '6px', md: '10px', lg: '16px' },\n    },\n  },\n};\n")
    return rows


if __name__ == "__main__":
    for r in build():
        print(r)
