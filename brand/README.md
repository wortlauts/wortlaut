# Wortlaut brand kit

Version 1.0, 2026-11-24. Everything needed to use the Wortlaut brand: logos, icons, social images, colour and type tokens, fonts and the rules.
A visual overview in German is in `OVERVIEW.html` (open in a browser) and `OVERVIEW.pdf`.

## Idea

- **Symbol:** the first letter of the name as a search hit: a bold lowercase `w` in night blue on an orange marker box. It stands next to the wordmark in the logo; the name itself is always set normally, so the `w` in "wortlaut" is a plain letter. One symbol for every size, down to 16 px.
- **Wordmark:** `wortlaut` in Space Grotesk, "wort" bold and "laut" regular, always lowercase, tight tracking.
- **Colour:** night blue on paper for light surfaces, orange as the marker. Orange is a fill behind night blue, never text or a line on a light surface. On light surfaces a darker orange ink (`signal-ink`) is used for links and highlights.

## What is in the box

| Path | Content |
| --- | --- |
| `logo/svg/` | lockups, symbol, wordmark as SVG (outlined type, no font needed) |
| `logo/png/` | the same as transparent PNG |
| `icon/` | favicon (svg, ico, png), app icons, maskable icon, apple-touch-icon, web manifest |
| `social/` | Open Graph image, GitHub social preview, banner, avatars |
| `tokens/` | tokens.json, brand.css, tailwind.preset.cjs |
| `fonts/` | Space Grotesk and Inter (woff2) with OFL licence texts and fonts.css |
| `source/` | scripts that rebuild everything in this folder |
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
<meta name="theme-color" content="#14213D">
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
| night | `#14213D` |
| signal | `#FF6B2C` |
| signal-ink | `#BF3E0A` |
| paper | `#F4F1EA` |
| slate | `#4A5470` |
| night-900 | `#0D1630` |
| night-700 | `#1E2E52` |
| night-600 | `#2C3F6A` |
| mist | `#AAB3C8` |
| line | `#DAD5C8` |
| paper-200 | `#EAE6DB` |
| hit-light | `#FFE0CC` |
| hit-dark | `#4A2A25` |
| error | `#B3261E` |
| success | `#1B7A4B` |

Rules: `signal` (marker orange) is a fill behind `night` blue, on light and dark surfaces. It is never used for text or thin lines on `paper` or white, use `signal-ink` there. Chart series: `#14213D`, `#BF3E0A`, `#1F7A8C`, `#8A6A00`. Never use party colours.

The build checks these contrast ratios and fails if one drops below its target:

| Pair | Ratio | Use |
| --- | --- | --- |
| night on paper | 14.2 : 1 | text |
| night on white | 16 : 1 | text |
| slate on paper | 6.7 : 1 | text |
| slate on white | 7.5 : 1 | text |
| signal-ink on paper | 4.8 : 1 | text |
| signal-ink on white | 5.4 : 1 | text |
| error on paper | 5.8 : 1 | text |
| success on paper | 4.7 : 1 | text |
| night on hit-light | 12.8 : 1 | text |
| paper on night | 14.2 : 1 | text |
| paper on night-900 | 15.9 : 1 | text |
| mist on night | 7.6 : 1 | text |
| mist on night-700 | 6.4 : 1 | text |
| paper on hit-dark | 11.3 : 1 | text |
| night on signal (w on marker) | 5.6 : 1 | text |
| signal on night (graphics, large text) | 5.6 : 1 | graphics, large text |
| signal on night-900 (graphics, large text) | 6.3 : 1 | graphics, large text |

Not allowed: `signal` (`#FF6B2C`) as text or line colour on paper or white. It only reaches 2.5 : 1 there.

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
