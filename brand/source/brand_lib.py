"""wortlaut brand geometry: symbol (highlighted w), wordmark (outlined type), lockups, tiles.

All drawing is pure vector math so the whole kit can be rebuilt with `python build_kit.py`.
Requires: fonttools, cairosvg, pillow and the @fontsource/space-grotesk npm package.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

NODE = os.environ.get("FONT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "node_modules", "@fontsource"))

# ---------------------------------------------------------------- colours
C = {
    "night": "#14213D", "night-900": "#0D1630", "night-700": "#1E2E52", "night-600": "#2C3F6A",
    "signal": "#FF6B2C", "signal-ink": "#BF3E0A",
    "paper": "#F4F1EA", "paper-200": "#EAE6DB", "line": "#DAD5C8",
    "slate": "#4A5470", "mist": "#AAB3C8", "white": "#FFFFFF", "black": "#000000",
    "hit-light": "#FFE0CC", "hit-dark": "#4A2A25",
    "error": "#B3261E", "success": "#1B7A4B",
}


def lum(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ---------------------------------------------------------------- symbol
# ---------------------------------------------------------------- type
_fonts = {}


def _font(wt):
    if wt not in _fonts:
        _fonts[wt] = TTFont(f"{NODE}/space-grotesk/files/space-grotesk-latin-{wt}-normal.woff")
    return _fonts[wt]


def outline(text, size, wt, x0=0.0, tracking=0.0, y0=0.0):
    f = _font(wt); gs = f.getGlyphSet(); cm = f.getBestCmap(); upm = f["head"].unitsPerEm
    sc = size / upm; x = x0; d = ""
    for ch in text:
        gn = cm[ord(ch)]; pen = SVGPathPen(gs)
        gs[gn].draw(TransformPen(pen, (sc, 0, 0, -sc, x, y0)))
        d += pen.getCommands(); x += gs[gn].width * sc + tracking * size
    return d, x


S = 100.0
TRACK = -0.03
JOIN = 0.02            # extra space between "wort" and "laut"
WT_BOLD, WT_LIGHT = 700, 400


def _metrics():
    f = _font(WT_BOLD); gs = f.getGlyphSet(); upm = f["head"].unitsPerEm
    bp = BoundsPen(gs); gs[f.getBestCmap()[ord("l")]].draw(bp)
    return bp.bounds[3] / upm * S


ASC = _metrics()


# ---------------------------------------------------------------- symbol: the highlighted "w"
def _rrect(x, y, w, h, r):
    return (f"M{x + r:g},{y:g}H{x + w - r:g}A{r:g},{r:g} 0 0 1 {x + w:g},{y + r:g}V{y + h - r:g}"
            f"A{r:g},{r:g} 0 0 1 {x + w - r:g},{y + h:g}H{x + r:g}A{r:g},{r:g} 0 0 1 {x:g},{y + h - r:g}"
            f"V{y + r:g}A{r:g},{r:g} 0 0 1 {x + r:g},{y:g}Z")


def _build_hit(pad_x=9.0, pad_y=9.0, r=12.0):
    """The first letter of the name as a search hit: a bold w on a marker-orange rounded box."""
    f = _font(WT_BOLD); gs = f.getGlyphSet(); upm = f["head"].unitsPerEm
    bp = BoundsPen(gs); gs[f.getBestCmap()[ord("w")]].draw(bp)
    gx0, gy0, gx1, gy1 = [v * S / upm for v in bp.bounds]
    gw, gh = gx1 - gx0, gy1 - gy0
    W, H = gw + 2 * pad_x, gh + 2 * pad_y
    glyph, _ = outline("w", S, WT_BOLD, pad_x - gx0, 0.0, pad_y + gh + gy0)
    return {"box": _rrect(0, 0, W, H, r), "quote": glyph, "wave": "", "x0": 0.0, "w": W, "h": H,
            "baseline": pad_y + gh + gy0}


_HIT = _build_hit()
SYMBOLS = {"full": _HIT, "compact": _HIT}   # one symbol for all sizes, 16 px and up
MARK_COLOR = (C["signal"], C["night"], C["night"])    # marker box, night-blue letter
MARK_REV = (C["signal"], C["night"], C["night"])      # same on dark: the orange box carries the letter


def sym_body(variant, fill):
    """fill: one colour (single-colour mark, letter knocked out) or (box, letter, unused) colours."""
    s = SYMBOLS[variant]
    if isinstance(fill, str):
        return f'<path fill-rule="evenodd" d="{s["box"]}{s["quote"]}" fill="{fill}"/>'
    return f'<path d="{s["box"]}" fill="{fill[0]}"/><path d="{s["quote"]}" fill="{fill[1]}"/>'


def sym_group(variant, fill, x, y, height):
    s = SYMBOLS[variant]; k = height / s["h"]
    return f'<g transform="translate({x:g},{y:g}) scale({k:.5f})">{sym_body(variant, fill)}</g>'


def sym_width(variant, height):
    s = SYMBOLS[variant]; return s["w"] * height / s["h"]


def sym_svg(variant, fill, title="wortlaut symbol"):
    s = SYMBOLS[variant]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s["w"]:.3f} {s["h"]:.3f}" '
            f'width="{s["w"]:.1f}" height="{s["h"]:.1f}" role="img" aria-label="{title}"><title>{title}</title>'
            f'{sym_body(variant, fill)}</svg>')


def wordmark_paths():
    d1, x = outline("wort", S, WT_BOLD, 0, TRACK)
    d2, x2 = outline("laut", S, WT_LIGHT, x + JOIN * S, TRACK)
    return d1, d2, x2 - TRACK * S


D_BOLD, D_LIGHT, WW = wordmark_paths()
PAD = 6.0


def wordmark_g(c1, c2, ox, baseline):
    return (f'<g transform="translate({ox:g},{baseline:g})"><path d="{D_BOLD}" fill="{c1}"/>'
            f'<path d="{D_LIGHT}" fill="{c2}"/></g>')


def svg(w, h, body, bg=None, title="wortlaut"):
    rect = f'<rect width="{w:g}" height="{h:g}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.1f}" height="{h:.1f}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{rect}{body}</svg>')


# ---------------------------------------------------------------- lockups
GAP_H = 0.26 * S


def wordmark_svg(c1, c2):
    return svg(WW + 2 * PAD, ASC + 2 * PAD, wordmark_g(c1, c2, PAD, ASC + PAD))


MH_H = ASC                                    # mark height in the horizontal lockup: ascender height, sitting on the baseline


def lockup_h_size():
    return sym_width("full", MH_H) + GAP_H + WW + 2 * PAD, MH_H + 2 * PAD


def lockup_h_body(mark, c1, c2):
    mw = sym_width("full", MH_H)
    return sym_group("full", mark, PAD, PAD, MH_H) + wordmark_g(c1, c2, PAD + mw + GAP_H, MH_H + PAD)


def lockup_h_svg(mark, c1, c2):
    w, h = lockup_h_size(); return svg(w, h, lockup_h_body(mark, c1, c2))


def lockup_s_size():
    mh = 0.36 * WW * SYMBOLS["full"]["h"] / SYMBOLS["full"]["w"]
    return WW + 2 * PAD, mh + 0.30 * S + ASC + 2 * PAD, mh


def lockup_s_svg(mark, c1, c2):
    w, h, mh = lockup_s_size(); mw = sym_width("full", mh)
    body = sym_group("full", mark, (w - mw) / 2, PAD, mh) + wordmark_g(c1, c2, PAD, PAD + mh + 0.30 * S + ASC)
    return svg(w, h, body)


# ---------------------------------------------------------------- tiles
def tile_svg(size, variant, mark, bg, radius_frac=0.225, mark_frac=0.56, bleed=False, title="wortlaut"):
    mw = size * mark_frac; mh = mw * SYMBOLS[variant]["h"] / SYMBOLS[variant]["w"]
    if mh > size * 0.78:
        mh = size * 0.78
    mw = sym_width(variant, mh)
    r = 0 if bleed else size * radius_frac
    body = f'<rect width="{size}" height="{size}" rx="{r:g}" fill="{bg}"/>' + sym_group(variant, mark, (size - mw) / 2, (size - mh) / 2, mh)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>')


def text_path(text, size, wt, fill, tracking=0.0):
    d, w = outline(text, size, wt, 0, tracking)
    return f'<path d="{d}" fill="{fill}"/>', w
