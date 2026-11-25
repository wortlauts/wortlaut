"""Builds README.md (English, for repos) and OVERVIEW.html / OVERVIEW.pdf (German, visual) in ../wortlaut-brand."""
import os, re, base64, subprocess, datetime, json
import brand_lib as B
from brand_lib import C
import build_assets as A

ROOT = A.ROOT
TODAY = "2026-11-24"
ROWS = A.contrast_table()


def sized(svg, width):
    return re.sub(r'width="[^"]+" height="[^"]+"', f'width="{width}"', svg, count=1).replace("<svg ", '<svg style="display:block;max-width:100%;height:auto" ', 1)


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()


# ------------------------------------------------------------------ fonts embedded
fonts_css = ""
for fam, pkg, ws in (("Space Grotesk", "space-grotesk", (400, 500, 700)), ("Inter", "inter", (400, 500, 600))):
    for w in ws:
        fonts_css += (f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;"
                      f"src:url(data:font/woff2;base64,{b64(f'{ROOT}/fonts/{pkg}-{w}.woff2')}) format('woff2');}}")

# ------------------------------------------------------------------ svg snippets
LH = B.lockup_h_svg
LS = B.lockup_s_svg
M = A.MONO
lock_navy = LH(*M["color"]); lock_rev = LH(*M["reversed"]); lock_black = LH(*M["black"]); lock_white = LH(*M["white"])
stack_navy = LS(*M["color"]); stack_rev = LS(*M["reversed"])
sym_navy = B.sym_svg("full", B.MARK_COLOR); sym_orange = B.sym_svg("full", B.MARK_REV)
symc_orange = sym_orange; symc_navy = sym_navy


def ghost_symbol(fill):
    s = B.SYMBOLS["full"]; W = s["w"]; H = s["h"]; g = C["signal-ink"]; bl = s["baseline"]
    guides = (f'<line x1="-6" y1="{bl:.1f}" x2="{W+6:.1f}" y2="{bl:.1f}" stroke="{g}" stroke-width="0.5" stroke-dasharray="2 1.6"/>'
              f'<line x1="-6" y1="{bl-49.6:.1f}" x2="{W+6:.1f}" y2="{bl-49.6:.1f}" stroke="{g}" stroke-width="0.5" stroke-dasharray="2 1.6"/>'
              f'<line x1="{W/2:.1f}" y1="-6" x2="{W/2:.1f}" y2="{H+6:.1f}" stroke="{g}" stroke-width="0.5" stroke-dasharray="2 1.6"/>')
    return (f'<svg viewBox="-10 -10 {W+20:.1f} {H+20:.1f}" width="100%" aria-hidden="true">'
            f'{B.sym_body("full", B.MARK_COLOR)}{guides}</svg>')


def clear_space():
    w, h = B.lockup_h_size(); u = B.ASC / 2
    body = B.lockup_h_body(B.MARK_COLOR, C["night"], C["night"])
    return (f'<svg viewBox="{-u} {-u} {w+2*u:.1f} {h+2*u:.1f}" width="100%" aria-hidden="true" style="display:block">'
            f'<rect x="{-u}" y="{-u}" width="{w+2*u:.1f}" height="{h+2*u:.1f}" fill="{C["hit-light"]}"/>'
            f'<rect x="0" y="0" width="{w:.1f}" height="{h:.1f}" fill="{C["paper"]}"/>'
            f'<rect x="{B.PAD}" y="{B.PAD}" width="{w-2*B.PAD:.1f}" height="{h-2*B.PAD:.1f}" fill="none" stroke="{C["signal-ink"]}" stroke-width="0.8" stroke-dasharray="3 2"/>'
            f'{body}</svg>')


def tile(size_px, variant, bg, mark, radius, frac, bleed=False):
    svg = B.tile_svg(512, variant, mark, bg, radius_frac=radius, mark_frac=frac, bleed=bleed)
    return re.sub(r'width="512" height="512"', f'width="{size_px}" height="{size_px}"', svg, count=1)


def bars_chart(color):
    hs = [22, 30, 28, 44, 58, 52, 72, 66]
    r = "".join(f'<rect x="{i*26}" y="{80-h}" width="16" height="{h}" rx="3" fill="{color}"/>' for i, h in enumerate(hs))
    return f'<svg viewBox="0 0 208 84" width="100%" aria-hidden="true">{r}</svg>'


# ------------------------------------------------------------------ html
CSS = """
*{box-sizing:border-box}
html{background:#EAE6DB}
body{margin:0;font-family:Inter,system-ui,sans-serif;color:#14213D;font-size:14px;line-height:1.5}
.page{width:1123px;height:794px;margin:24px auto;background:#F4F1EA;position:relative;overflow:hidden;padding:48px 56px;display:flex;flex-direction:column;gap:22px;border:1px solid #DAD5C8}
.page.dark{background:#14213D;color:#F4F1EA;border-color:#14213D}
.head{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1.5px solid currentColor;padding-bottom:10px}
.head .no{font-family:'Space Grotesk',sans-serif;font-weight:500;font-size:13px;letter-spacing:.04em}
.head h2{margin:0;font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:30px;letter-spacing:-.02em;line-height:1}
.head .meta{font-size:12px;color:#4A5470}
.dark .head .meta{color:#AAB3C8}
.grid{display:grid;gap:20px}
.box{border:1px solid #DAD5C8;background:#fff;padding:20px;display:flex;flex-direction:column;gap:12px;border-radius:14px;min-height:0}
.box.night{background:#14213D;border-color:#14213D;color:#F4F1EA}
.box.paper{background:#F4F1EA}
.lab{font-size:12px;color:#4A5470;letter-spacing:.02em}
.night .lab{color:#AAB3C8}
.mid{display:flex;align-items:center;justify-content:center;flex:1}
p{margin:0}
.sw{display:flex;flex-direction:column;gap:6px;font-size:12px;line-height:1.35}
.sw i{display:block;height:54px;border-radius:8px;border:1px solid rgba(20,33,61,.12)}
.sw b{font-weight:600}
table{border-collapse:collapse;width:100%;font-size:12px}
td,th{text-align:left;padding:4px 8px 4px 0;border-bottom:1px solid #DAD5C8;font-weight:400}
th{color:#4A5470;font-weight:500}
.tag{display:inline-block;font-size:11px;font-weight:600;padding:2px 9px;border-radius:999px;color:#F4F1EA;background:#14213D}
.tag.bad{background:#BF3E0A;color:#fff}
.theme-light{--bg:#F4F1EA;--surface:#fff;--text:#14213D;--muted:#4A5470;--border:#DAD5C8;--accent:#BF3E0A;--primary:#14213D;--on-primary:#F4F1EA;--hit:#FFE0CC;--hit-t:#14213D}
.theme-dark{--bg:#0D1630;--surface:#14213D;--text:#F4F1EA;--muted:#AAB3C8;--border:#2C3F6A;--accent:#FF6B2C;--primary:#FF6B2C;--on-primary:#14213D;--hit:#4A2A25;--hit-t:#F4F1EA}
.ui{background:var(--bg);color:var(--text);border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:12px;border:1px solid var(--border)}
.ui .bar{display:flex;align-items:center;gap:10px;background:var(--surface);border:1.5px solid var(--text);border-radius:999px;padding:6px 6px 6px 18px}
.ui .bar span{flex:1;font-size:15px}
.ui .btn{background:var(--primary);color:var(--on-primary);font-weight:600;font-size:13px;padding:9px 18px;border-radius:999px}
.ui .chips{display:flex;gap:8px;flex-wrap:wrap}
.ui .chip{border:1px solid var(--border);background:var(--surface);color:var(--muted);border-radius:999px;padding:3px 12px;font-size:12px}
.ui .chip.on{background:var(--text);color:var(--bg);border-color:var(--text)}
.ui .card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px;display:flex;flex-direction:column;gap:6px}
.ui .card .who{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:15px}
.ui .card .sub{font-size:12px;color:var(--muted)}
.ui mark{background:var(--hit);color:var(--hit-t);border-radius:3px;padding:0 .15em}
.ui a{color:var(--accent);font-size:13px;font-weight:500}
@page{size:1123px 794px;margin:0}
@media print{html{background:none}.page{margin:0;border:none;page-break-after:always}}
"""


def page(no, title, meta, body, dark=False):
    return (f'<section class="page{" dark" if dark else ""}"><div class="head"><div><span class="no">{no}</span></div>'
            f'<h2>{title}</h2><div class="meta">{meta}</div></div>{body}</section>')


def swatch(name, hexv, note=""):
    border = ' style="background:%s"' % hexv
    return f'<div class="sw"><i{border}></i><b>{name}</b><span>{hexv}</span><span style="color:#4A5470">{note}</span></div>'


pages = []

# 1 cover
pages.append(f'''<section class="page dark" style="justify-content:center;align-items:center;gap:28px">
<div style="width:520px">{sized(stack_rev, 520)}</div>
<div style="font-family:'Space Grotesk',sans-serif;font-weight:400;font-size:22px;color:#AAB3C8">suche in reden des deutschen bundestags</div>
<div style="position:absolute;left:56px;bottom:40px;font-size:12px;color:#AAB3C8">marken-übersicht · version 1.0 · {TODAY}</div>
<div style="position:absolute;right:56px;bottom:40px;font-size:12px;color:#AAB3C8">logo, farben, schrift, icons, social, tokens</div></section>''')

# 2 concept
pages.append(page("01", "das zeichen", "der anfangsbuchstabe wird zum treffer", f'''
<div class="grid" style="grid-template-columns:420px 1fr;flex:1;gap:36px">
<div class="box paper" style="justify-content:center"><div class="mid" style="padding:10px"><div style="width:100%">{ghost_symbol(C["night"])}</div></div><div class="lab">konstruktion: kleines w in space grotesk bold, 9 einheiten rand rundum, ecken 12. die gestrichelten linien zeigen grundlinie und x-höhe des w.</div></div>
<div style="display:flex;flex-direction:column;gap:22px;justify-content:center">
<div><div class="tag">1</div><h3 style="margin:8px 0 4px;font-family:'Space Grotesk',sans-serif;font-size:22px">ein treffer, der einen namen trägt</h3><p>wer sucht, sieht treffer: ein markierter begriff im text. das orange feld ist dieser textmarker, darin steht das w. so wird der anfangsbuchstabe zum zeichen, und das zeichen liest sich als „w“ und als „hier steht dein wort“. im logo steht das zeichen neben dem wort, im namen selbst bleibt das w ein ganz normaler buchstabe.</p></div>
<div><div class="tag">2</div><h3 style="margin:8px 0 4px;font-family:'Space Grotesk',sans-serif;font-size:22px">wort in fett, laut in regular</h3><p>der name besteht aus zwei wörtern. das fette „wort“ ist das, was gesagt wird, das ruhigere „laut“ der klang dazu. beide teile stehen eng zusammen und werden immer klein geschrieben.</p></div>
<div><div class="tag">3</div><h3 style="margin:8px 0 4px;font-family:'Space Grotesk',sans-serif;font-size:22px">orange nur als marker, nachtblau trägt den text</h3><p>hell bleibt die oberfläche ruhig: nachtblau auf papier. orange ist der marker und steht als fläche hinter nachtblau, nie als schrift oder linie auf hell. für links und markierungen auf hell gibt es ein dunkleres orange.</p></div>
</div></div>'''))

# 3 logo family
pages.append(page("02", "logo-familie", "alle varianten liegen als svg und png im paket", f'''
<div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr 150px;flex:1">
<div class="box"><div class="lab">horizontal · farbig auf hell (standard)</div><div class="mid">{sized(lock_navy, 380)}</div></div>
<div class="box night"><div class="lab">horizontal · reversed auf dunkel</div><div class="mid">{sized(lock_rev, 380)}</div></div>
<div class="box"><div class="lab">gestapelt · farbig auf hell</div><div class="mid">{sized(stack_navy, 230)}</div></div>
<div class="box night"><div class="lab">gestapelt · reversed</div><div class="mid">{sized(stack_rev, 230)}</div></div>
<div class="box"><div class="lab">einfarbig schwarz (druck, stempel, fax)</div><div class="mid">{sized(lock_black, 300)}</div></div>
<div class="box" style="background:#000;border-color:#000"><div class="lab" style="color:#bbb">einfarbig weiß</div><div class="mid">{sized(lock_white, 300)}</div></div>
</div>'''))

# 4 clear space + sizes
pages.append(page("03", "schutzraum und größen", "vermeiden, dass das logo zu eng sitzt", f'''
<div class="grid" style="grid-template-columns:1.15fr 1fr;flex:1">
<div class="box"><div class="lab">schutzraum: mindestens die halbe symbolhöhe rundherum</div><div class="mid" style="padding:10px"><div style="width:100%">{clear_space()}</div></div><p class="lab">die getönte fläche bleibt frei von text, bildern und kanten.</p></div>
<div class="box"><div class="lab">mindestgrößen</div>
<div style="display:flex;align-items:flex-end;gap:30px;padding:10px 0">
<div>{sized(lock_navy, 140)}<div class="lab" style="margin-top:6px">logo ab 140 px breite</div></div>
<div>{sized(sym_navy, 48)}<div class="lab" style="margin-top:6px">symbol ab 24 px</div></div>
<div>{sized(symc_navy, 16)}<div class="lab" style="margin-top:6px">symbol ab 16 px</div></div>
</div>
<p>das zeichen funktioniert ab 16 px (favicon). es gibt nur eine version, ohne umschalten für kleine größen.</p>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:12px;flex:1">
<div class="box paper" style="align-items:center;justify-content:center">{sized(sym_navy, 150)}<div class="lab">auf hell</div></div>
<div class="box night" style="align-items:center;justify-content:center">{sized(sym_orange, 150)}<div class="lab">auf dunkel</div></div></div>
</div></div>'''))

# 5 icons
pages.append(page("04", "icons und avatare", "gleiche gestalt, passend zu jeder plattform", f'''
<div class="grid" style="grid-template-columns:repeat(4,1fr);flex:1;grid-template-rows:1fr 150px">
<div class="box paper" style="align-items:center;justify-content:center">{tile(180,"full",C["night"],B.MARK_REV,.225,.58)}<div class="lab">app-icon · 512 px, abgerundet</div></div>
<div class="box paper" style="align-items:center;justify-content:center">{tile(180,"full",C["night"],B.MARK_REV,0,.46,True)}<div class="lab">maskable (pwa) · symbol in der sicherheitszone</div></div>
<div class="box paper" style="align-items:center;justify-content:center"><div style="border-radius:50%;overflow:hidden;width:180px;height:180px;background:#14213D">{tile(180,"full",C["night"],B.MARK_REV,0,.56,True)}</div><div class="lab">github-org-avatar · rund beschnitten</div></div>
<div class="box paper" style="align-items:center;justify-content:center">{tile(180,"full",C["night"],B.MARK_REV,0,.56,True)}<div class="lab">apple-touch-icon · vollflächig, ios rundet selbst</div></div>
<div class="box paper" style="grid-column:span 2;flex-direction:row;align-items:center;gap:26px"><div class="lab" style="width:90px">favicon</div>
<div style="display:flex;align-items:flex-end;gap:22px"><div>{tile(48,"full",C["night"],B.MARK_REV,.2,.72)}</div><div>{tile(32,"full",C["night"],B.MARK_REV,.2,.72)}</div><div>{tile(16,"full",C["night"],B.MARK_REV,.2,.72)}</div></div><p class="lab">48, 32 und 16 px in echter größe</p></div>
<div class="box paper" style="grid-column:span 2;justify-content:center"><p>dateien: <b>icon/</b> (favicon.svg, favicon.ico, app-icon.svg, icon-192/512.png, icon-maskable-512.png, apple-touch-icon.png, app-icon-1024.png, site.webmanifest) und <b>social/</b> (avatare).</p></div>
</div>'''))

# 6 colours
brand = [("nacht", C["night"], "text, flächen, dunkle oberfläche"), ("signal", C["signal"], "marker: feld hinter nachtblau, treffer"),
         ("signal-tinte", C["signal-ink"], "orange auf hell: links, markierungen"), ("papier", C["paper"], "seitenhintergrund")]
neutral = [("nacht-900", C["night-900"], "dunkelmodus hintergrund"), ("nacht-700", C["night-700"], "erhöhte fläche dunkel"), ("nacht-600", C["night-600"], "linien dunkel"),
           ("schiefer", C["slate"], "zweittext hell"), ("nebel", C["mist"], "zweittext dunkel"), ("linie", C["line"], "linien hell"),
           ("papier-200", C["paper-200"], "vertiefte fläche"), ("weiß", C["white"], "karten")]
state = [("treffer hell", C["hit-light"], "markierung im text"), ("treffer dunkel", C["hit-dark"], "markierung im dunkelmodus"), ("fehler", C["error"], "meldungen"), ("erfolg", C["success"], "meldungen")]
sel = [r for r in ROWS if r[0] in ("night on paper", "slate on paper", "signal-ink on paper", "signal-ink on white", "paper on night", "mist on night", "night on signal", "night on hit-light", "paper on hit-dark")]
DE = [("signal-ink", "signal-tinte"), ("hit-light", "treffer hell"), ("hit-dark", "treffer dunkel"), ("night", "nacht"), ("paper", "papier"), ("slate", "schiefer"), ("mist", "nebel"), ("signal", "signal")]
def de(n):
    n = n.replace(" on ", " auf ")
    for a, b in DE:
        n = n.replace(a, b)
    return n
trows = "".join(f"<tr><td>{de(n)}</td><td><b>{v:g} : 1</b></td></tr>" for n, v, _ in sel)
chart_sw = "".join(f'<i style="display:block;width:44px;height:30px;border-radius:6px;background:{c}"></i>' for c in A.CHART)
pages.append(page("05", "farbe", "jede textkombination erfüllt wcag aa (4,5 : 1)", f'''
<div class="grid" style="grid-template-columns:1.5fr 1fr;flex:1">
<div style="display:flex;flex-direction:column;gap:16px">
<div class="lab">marke</div><div class="grid" style="grid-template-columns:repeat(4,1fr)">{"".join(swatch(*s) for s in brand)}</div>
<div class="lab">neutrale töne</div><div class="grid" style="grid-template-columns:repeat(8,1fr);gap:10px">{"".join(swatch(*s[:2]) for s in neutral)}</div>
<div class="lab">zustände und treffer</div><div class="grid" style="grid-template-columns:repeat(4,1fr)">{"".join(swatch(*s) for s in state)}</div>
<div class="lab">diagramme (mindestens 3 : 1 auf hell), niemals parteifarben</div><div style="display:flex;gap:10px">{chart_sw}</div>
</div>
<div class="box"><div class="lab">kontrast (auszug)</div><table>{trows}</table>
<p style="color:#BF3E0A;font-weight:600;margin-top:6px">signal (#FF6B2C) auf papier erreicht nur {B.contrast(C["signal"], C["paper"]):.1f} : 1 und wird dort nie als schrift oder linie verwendet, nur als fläche hinter nachtblau.</p></div>
</div>'''))

# 7 typography
pages.append(page("06", "schrift", "space grotesk für marke und überschriften, inter für die oberfläche", f'''
<div class="grid" style="grid-template-columns:1fr 1fr;flex:1">
<div class="box" style="gap:10px"><div class="lab">space grotesk · 400 / 500 / 700</div>
<div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:64px;line-height:1;letter-spacing:-.03em">wer sagte das zuerst?</div>
<div style="font-family:'Space Grotesk',sans-serif;font-weight:500;font-size:30px;line-height:1.15;letter-spacing:-.015em">treffer, trends und redner</div>
<div style="font-family:'Space Grotesk',sans-serif;font-weight:400;font-size:20px;color:#4A5470">abcdefghijklmnopqrstuvwxyz äöüß 0123456789</div>
<div style="display:flex;gap:26px;align-items:baseline;font-family:'Space Grotesk',sans-serif;font-size:34px;letter-spacing:-.02em;margin-top:6px"><span style="font-weight:400">regular</span><span style="font-weight:500">medium</span><span style="font-weight:700">bold</span></div>
<div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:26px;letter-spacing:-.02em;margin-top:6px">wort<span style="font-weight:400">laut</span></div><p style="font-size:13px;color:#4A5470;margin-top:-4px">als schriftzug immer klein: „wort“ bold, „laut“ regular</p>
<p class="lab" style="margin-top:auto">frei nutzbar (sil open font license), im paket unter fonts/ mit lizenztext. selbst hosten, nicht von einem drittanbieter laden.</p></div>
<div class="box" style="gap:10px"><div class="lab">inter · 400 / 500 / 600</div>
<div style="font-weight:600;font-size:22px">überschrift in der oberfläche</div>
<p style="font-size:16px;line-height:1.55">fließtext in 16 px mit 1,55 zeilenabstand. inter bleibt in kleinen größen und in tabellen gut lesbar und hat tabellenziffern für die trend-zahlen.</p>
<p style="font-size:14px;color:#4A5470">zweittext in 14 px, schiefer #4A5470 auf papier, 6,7 : 1</p>
<table style="margin-top:6px"><tr><th>größe</th><th>verwendung</th></tr><tr><td>display · clamp 2,5 bis 4,5 rem</td><td>startseite</td></tr><tr><td>h1 · 2,25 rem</td><td>seitentitel</td></tr><tr><td>h2 · 1,5 rem</td><td>abschnitte</td></tr><tr><td>body · 1 rem</td><td>text</td></tr><tr><td>small · 0,875 rem</td><td>meta, quellen</td></tr></table></div>
</div>'''))

# 8 UI
ui_card = lambda theme: f'''<div class="ui {theme}">
<div style="display:flex;align-items:center;gap:10px">{sized(B.sym_svg("full", B.MARK_COLOR if theme=="theme-light" else B.MARK_REV), 28)}<b style="font-family:'Space Grotesk',sans-serif;font-size:18px;letter-spacing:-.02em">wort<span style="font-weight:400">laut</span></b></div>
<div class="bar"><span>digitalisierung</span><div class="btn">suchen</div></div>
<div class="chips"><div class="chip on">alle jahre</div><div class="chip">fraktion</div><div class="chip">redner</div><div class="chip">zwischenrufe</div></div>
<div class="card"><div class="who">beispiel-redner</div><div class="sub">21. wahlperiode · beispiel-datum · beispieltext</div><p>… eine <mark>digitalisierung</mark>, die bei den menschen ankommt, ist keine frage der technik …</p><a href="#">zur ganzen rede</a></div>
<div class="card"><div class="sub">trend · treffer pro jahr</div>{bars_chart("#14213D" if theme=="theme-light" else "#FF6B2C")}</div></div>'''
pages.append(page("07", "oberfläche", "dieselben tokens in hell und dunkel", f'''
<div class="grid" style="grid-template-columns:1fr 1fr;flex:1;gap:24px">{ui_card("theme-light")}{ui_card("theme-dark")}</div>'''))

# 9 social + files
tree = []
for dp, dn, fn in os.walk(ROOT):
    dn.sort()
    rel = os.path.relpath(dp, ROOT)
    if rel == "." or rel.count(os.sep) > 0:
        continue
    tree.append((rel, len(fn)))
FILEROWS = {"logo": "lockups, symbol, wordmark als svg (svg/) und png (png/)", "icon": "favicon, app-icons, manifest", "social": "og-bild, github-vorschau, banner, avatare",
            "tokens": "tokens.json, brand.css, tailwind.preset.cjs", "fonts": "woff2 und lizenz (ofl)"}
trows2 = "".join(f"<tr><td><b>{k}/</b></td><td>{v}</td></tr>" for k, v in FILEROWS.items())
pages.append(page("08", "social und dateien", "was im paket liegt", f'''
<div class="grid" style="grid-template-columns:1.2fr 1fr;flex:1">
<div style="display:flex;flex-direction:column;gap:14px">
<div class="box" style="padding:12px"><div class="lab">og-bild 1200 × 630</div>{sized(open(f"{ROOT}/social/og-image-de.svg").read(), 520)}</div>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:14px">
<div class="box" style="padding:12px"><div class="lab">github-vorschau 1280 × 640</div>{sized(open(f"{ROOT}/social/github-social-preview-en.svg").read(), 250)}</div>
<div class="box" style="padding:12px"><div class="lab">banner 1500 × 500</div>{sized(open(f"{ROOT}/social/banner-1500x500.svg").read(), 250)}</div></div></div>
<div class="box"><div class="lab">inhalt des pakets</div><table>{trows2}</table>
<p style="margin-top:8px">zusätzlich: <b>README.md</b> (regeln auf englisch für die repos), <b>OVERVIEW.html / .pdf</b> (diese seite) und <b>source/</b> mit dem skript, das alles neu erzeugt.</p>
<p class="lab" style="margin-top:auto">in html: &lt;link rel="icon" href="/favicon.svg" type="image/svg+xml"&gt; und &lt;link rel="icon" href="/favicon.ico" sizes="48x48"&gt;. weitere hinweise in README.md.</p></div>
</div>'''))

# 10 do/dont + legal
badstretch = f'<div style="transform:scale(.7,1.5);transform-origin:center">{sized(lock_navy, 190)}</div>'
badshadow = f'<div style="filter:drop-shadow(4px 5px 3px rgba(0,0,0,.45))">{sized(lock_navy, 190)}</div>'
badfont = "<div style=\"font-family:Georgia,serif;font-weight:700;font-size:34px;color:#14213D\">wortlaut</div>"
badtight = f'<div style="width:100%;padding:0">{sized(lock_navy, 270)}</div>'
def demo(ok, inner, cap, dark=False, pad=10):
    cls = "night" if dark else "paper"
    return (f'<div style="display:flex;flex-direction:column;gap:8px"><span class="tag{"" if ok else " bad"}">{"richtig" if ok else "falsch"}</span>'
            f'<div class="box {cls}" style="height:118px;overflow:hidden;padding:{pad}px"><div class="mid">{inner}</div></div><p class="lab">{cap}</p></div>')
pages.append(page("09", "richtig und falsch", "kleine regeln, großer unterschied", f'''
<div class="grid" style="grid-template-columns:repeat(4,1fr);gap:16px 16px;flex:0 0 auto">
{demo(True, sized(lock_navy, 190), "farbig auf hellem grund")}
{demo(True, sized(lock_rev, 190), "reversed auf dunklem grund", True)}
{demo(False, sized(LH(C["signal"], C["signal"], C["signal"]), 190), "orange als schrift auf papier: kaum lesbar")}
{demo(False, badstretch, "verzerren oder drehen")}
{demo(False, badshadow, "schatten, verläufe, konturen")}
{demo(False, badfont, "wortmarke neu setzen oder andere schrift")}
{demo(False, sized(lock_navy, 262), "kein schutzraum, zu eng am rand", False, 0)}
{demo(False, sized(lock_navy, 190).replace('#14213D', '#BF3E0A'), "umfärben außerhalb der palette")}
</div>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:16px;flex:1">
<div class="box"><div class="lab">außerdem</div><p>• das orange feld nicht drehen, verschieben oder anders einfärben<br>• name im logo immer klein, im fließtext „Wortlaut“<br>• keine bundesadler, bundestagslogos oder parteifarben verwenden<br>• orange nie als schrift oder linie auf hell, nur als fläche hinter nachtblau</p></div>
<div class="box paper"><div class="lab">hinweis für die seite (vorschlag, vor dem start rechtlich prüfen)</div><p>„Wortlaut ist ein unabhängiges Projekt und steht in keiner Verbindung zum Deutschen Bundestag. Die Texte stammen aus den Plenarprotokollen des Deutschen Bundestages (amtliche Werke, § 5 UrhG).“</p></div>
</div>'''))

html = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><title>wortlaut marken-übersicht</title>'
        f'<style>{fonts_css}{CSS}</style></head><body>' + "".join(pages) + '</body></html>')
open(f"{ROOT}/OVERVIEW.html", "w", encoding="utf-8").write(html)

# pdf via headless chrome
subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={ROOT}/OVERVIEW.pdf", f"file://{ROOT}/OVERVIEW.html"], check=True, capture_output=True)
print("overview ok", len(html))


# ------------------------------------------------------------------ README.md (English, for the repos)
def tree_md():
    notes = {"logo/svg": "lockups, symbol, wordmark as SVG (outlined type, no font needed)", "logo/png": "the same as transparent PNG",
             "icon": "favicon (svg, ico, png), app icons, maskable icon, apple-touch-icon, web manifest",
             "social": "Open Graph image, GitHub social preview, banner, avatars",
             "tokens": "tokens.json, brand.css, tailwind.preset.cjs", "fonts": "Space Grotesk and Inter (woff2) with OFL licence texts and fonts.css",
             "source": "scripts that rebuild everything in this folder"}
    lines = []
    for k, v in notes.items():
        lines.append(f"| `{k}/` | {v} |")
    return "\n".join(lines)


ct = "\n".join(f"| {n} | {v:g} : 1 | {'text' if need >= 4.5 else 'graphics, large text'} |" for n, v, need in ROWS)
pal = lambda keys: "\n".join(f"| {k} | `{C[k]}` |" for k in keys)

README = f"""# Wortlaut brand kit

Version 1.0, {TODAY}. Everything needed to use the Wortlaut brand: logos, icons, social images, colour and type tokens, fonts and the rules.
A visual overview in German is in `OVERVIEW.html` (open in a browser) and `OVERVIEW.pdf`.

## Idea

- **Symbol:** the first letter of the name as a search hit: a bold lowercase `w` in night blue on an orange marker box. It stands next to the wordmark in the logo; the name itself is always set normally, so the `w` in "wortlaut" is a plain letter. One symbol for every size, down to 16 px.
- **Wordmark:** `wortlaut` in Space Grotesk, "wort" bold and "laut" regular, always lowercase, tight tracking.
- **Colour:** night blue on paper for light surfaces, orange as the marker. Orange is a fill behind night blue, never text or a line on a light surface. On light surfaces a darker orange ink (`signal-ink`) is used for links and highlights.

## What is in the box

| Path | Content |
| --- | --- |
{tree_md()}
Top level: `README.md` (this file), `OVERVIEW.html`, `OVERVIEW.pdf`.

Pick a logo file:

| Need | File |
| --- | --- |
| default logo on light backgrounds | `logo/svg/lockup-horizontal-color.svg` |
| default logo on dark backgrounds | `logo/svg/lockup-horizontal-reversed.svg` |
| square space (cover, poster) | `logo/svg/lockup-stacked-color.svg` or `-reversed.svg` |
| one colour print, stamp | `-black.svg` or `-white.svg` |
| symbol alone (name already visible nearby) | `logo/svg/symbol-color.svg` (light backgrounds), `symbol-reversed.svg` (dark backgrounds) |
| wordmark only (name already next to the symbol) | `logo/svg/wordmark-color.svg` |

## Using it in the web app

```html
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="{C['night']}">
<meta property="og:image" content="/og-image-de.png">
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="stylesheet" href="/brand.css">
```

Copy `icon/*` to the site root (or `public/` in Next.js), `fonts/` to `public/fonts/`, `social/og-image-de.png` next to it and `tokens/brand.css` where your global styles live.
The CSS variables are prefixed `--wl-`. Light is the default; dark follows the system setting or `data-theme="dark"` on `<html>`.
For Tailwind, add `presets: [require('./tailwind.preset.cjs')]` to the config. `tokens.json` holds the same values as data for other tools.

## Colours

| Token | Value |
| --- | --- |
{pal(['night', 'signal', 'signal-ink', 'paper', 'slate', 'night-900', 'night-700', 'night-600', 'mist', 'line', 'paper-200', 'hit-light', 'hit-dark', 'error', 'success'])}

Rules: `signal` (marker orange) is a fill behind `night` blue, on light and dark surfaces. It is never used for text or thin lines on `paper` or white, use `signal-ink` there. Chart series: `#14213D`, `#BF3E0A`, `#1F7A8C`, `#8A6A00`. Never use party colours.

The build checks these contrast ratios and fails if one drops below its target:

| Pair | Ratio | Use |
| --- | --- | --- |
{ct}

Not allowed: `signal` (`#FF6B2C`) as text or line colour on paper or white. It only reaches {B.contrast(C['signal'], C['paper']):.1f} : 1 there.

## Typography

- Brand name and headings: **Space Grotesk** (400, 500, 700).
- Interface and body: **Inter** (400, 500, 600). Use tabular numbers for trend data (`font-variant-numeric: tabular-nums`).
- Both are licensed under the SIL Open Font License 1.1 (texts in `fonts/`). Self-host them, do not load them from a third party.
- Scale: display `clamp(2.5rem, 6vw, 4.5rem)`, h1 2.25rem, h2 1.5rem, h3 1.125rem, body 1rem, small 0.875rem.

## Rules

- **Clear space:** at least half the symbol height on every side.
- **Minimum size:** horizontal logo 140 px wide, symbol 16 px.
- **Backgrounds:** colour logo on light, reversed logo on dark. Do not place the logo on busy photos, and never use orange alone as the colour of text.
- **Do not** stretch, rotate, outline, add shadows or gradients, recolour outside the palette, move or redraw the marker box, rotate the letter, or set the wordmark in another font.
- **Name:** the logo is always lowercase. In running text write "Wortlaut".
- **No official symbols:** do not use the federal eagle, Bundestag logos or party colours.
- **Notice for the site (suggestion, check legally before launch):** "Wortlaut ist ein unabhängiges Projekt und steht in keiner Verbindung zum Deutschen Bundestag. Die Texte stammen aus den Plenarprotokollen des Deutschen Bundestages (amtliche Werke, § 5 UrhG)."

Taglines: German "suche in reden des deutschen bundestags", English "Search German Bundestag speeches by word or phrase".

## Licence

Fonts: SIL Open Font License 1.1 (see `fonts/`). Code in `source/`: same licence as the rest of the repository once chosen.
Logo and symbol: decide before the repository goes public. Suggestion: keep the logo files outside the code licence (all rights reserved by the project owner, use allowed to refer to Wortlaut) so forks cannot present themselves as the original project.

## Rebuilding

Everything is generated from code in `source/`:

```bash
cd source
npm install @fontsource/space-grotesk @fontsource/inter
pip install -r requirements.txt
python build_kit.py          # needs Google Chrome for OVERVIEW.pdf
```

`brand_lib.py` holds the geometry (symbol, wordmark, lockups). Change the colours in its `C` table or the bar parameters in `SYMBOLS` and rebuild.
"""
open(f"{ROOT}/README.md", "w", encoding="utf-8").write(README)
print("readme ok")
