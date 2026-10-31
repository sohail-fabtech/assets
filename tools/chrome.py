# Polished UI chrome: thick-bevel frames, ribbons, title pills, plates, progress bars, close button, chest.
#   assets/ui/chrome/<tone>/chr_<tone>_<part>.svg      tone = "brand" (global purple UI) or a theme id
# Stretchable parts are authored for CSS border-image (9-slice / 3-slice) — corners never distort:
#   frame: slice 44 · ribbon: slice 0 92 · pill / plate / track / fill: slice 0 50%   (see SLICE below)
# Layer recipe (from the reference crops): dark outline → deep base → gradient body → bottom inner shade
#   → top inner highlight band → thin rim light → soft outer glow.
import json, math, os
from level_themes import THEMES
from layout import folder_for
from make_ui_kit import mix

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
BRAND = ("#b48cff", "#7a3ad8", "#3a1080")  # light, mid, dark — global UI purple
SLICE = {"header": "0 60 fill", "bubble": "34 fill", "frame": "44 fill", "ribbon": "0 92 fill", "pill": "0 48 fill", "plate-cream": "0 40 fill", "plate-dark": "0 34 fill",
         "track": "0 18 fill", "fill": "0 18 fill"}


def tone(tid):
    if tid == "brand": return BRAND
    p = THEMES[tid]["palette"]
    return mix(p["primary"], "#fff", .45), p["primary"], mix(p["primaryDark"], "#000", .25)


def doc(w, h, body, pad=0):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w + 2 * pad} {h + 2 * pad}" width="{w + 2 * pad}" height="{h + 2 * pad}">'
            '<defs><filter id="blur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4"/></filter>'
            '<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter></defs>'
            f'{body}</svg>')


def vgrad(k, *stops):
    return f'<linearGradient id="{k}" x1="0" y1="0" x2="0" y2="1">' + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + "</linearGradient>"


def rrect(x, y, w, h, r):
    return f"M{x + r} {y} H{x + w - r} A{r} {r} 0 0 1 {x + w} {y + r} V{y + h - r} A{r} {r} 0 0 1 {x + w - r} {y + h} H{x + r} A{r} {r} 0 0 1 {x} {y + h - r} V{y + r} A{r} {r} 0 0 1 {x + r} {y} Z"


def glossy(x, y, w, h, r, c, outline=3.5, depth=6, k="b"):
    """The core chunky-glossy body every chrome part is built from."""
    l, m, d = c
    body = rrect(x, y, w, h - depth, r)
    return (vgrad(f"{k}g", (0, l), (.48, m), (1, mix(m, d, .55)))
            .join(["<defs>", "</defs>"])
            + f'<path d="{rrect(x, y + depth, w, h - depth, r)}" fill="{d}"/>'                                   # deep base (3D lip)
            + f'<path d="{body}" fill="url(#{k}g)"/>'
            + f'<path d="{rrect(x + 4, y + (h - depth) * .52, w - 8, (h - depth) * .44, max(4, r - 4))}" fill="{d}" opacity=".18"/>'  # bottom inner shade
            + f'<path d="{rrect(x + 6, y + 4, w - 12, (h - depth) * .4, max(4, r - 5))}" fill="#fff" opacity=".32"/>'               # top highlight band
            + f'<path d="{rrect(x + 1.5, y + 1.5, w - 3, h - depth - 3, r - 1)}" fill="none" stroke="#fff" stroke-opacity=".45" stroke-width="1.6"/>'  # rim light
            + f'<path d="{rrect(x, y, w, h, r)}" fill="none" stroke="{mix(d, "#000", .45)}" stroke-width="{outline}"/>')            # dark outline


# ---- parts -----------------------------------------------------------------------------------------
def close_btn(c):
    l, m, d = c
    x = ('<path d="M38 36 L66 64 M66 36 L38 64" stroke-width="13" stroke-linecap="round"/>')
    return doc(104, 104, glossy(2, 2, 100, 100, 26, c, k="cl")
               + f'<g stroke="{mix(d, "#000", .3)}" opacity=".55" transform="translate(0 4)">{x}</g><g stroke="#fff">{x}</g>'
               + '<path d="M40 34 L48 42" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".6"/>')


def pill(c, w=360, h=96):
    return doc(w, h, glossy(2, 2, w - 4, h - 4, (h - 4) / 2 - 2, c, k="pl"))


def frame(c, s=160):
    """9-slice card frame: dark outline, thick bevelled ring, inner rim, transparent-ish centre for the scene."""
    l, m, d = c
    ring = 18
    return doc(s, s,
               vgrad("fr", (0, l), (.35, m), (1, d)).join(["<defs>", "</defs>"]) +
               f'<path d="{rrect(1.5, 1.5, s - 3, s - 3, 34)}" fill="url(#fr)" stroke="{mix(d, "#000", .5)}" stroke-width="3"/>'
               f'<path d="{rrect(5, 5, s - 10, s - 10, 30)}" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="2"/>'      # outer rim light
               f'<path d="{rrect(ring, ring, s - 2 * ring, s - 2 * ring, 20)}" fill="{mix(d, "#000", .55)}"/>'                       # inner well (scene sits here)
               f'<path d="{rrect(ring, ring, s - 2 * ring, s - 2 * ring, 20)}" fill="none" stroke="{mix(d, "#000", .6)}" stroke-width="3"/>'
               f'<path d="{rrect(ring - 3, ring - 3, s - 2 * ring + 6, s - 2 * ring + 6, 23)}" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="1.5"/>')


def ribbon(c, w=520, h=140, crown=False):
    """Banner with arched top, folded tails behind, highlight band. 3-slice horizontally (tails fixed)."""
    l, m, d = c
    dk = mix(d, "#000", .45)
    tails = (f'<path d="M4 54 H96 V116 H4 L30 85 Z" fill="{mix(m, d, .6)}" stroke="{dk}" stroke-width="3" stroke-linejoin="round"/>'
             f'<path d="M{w - 4} 54 H{w - 96} V116 H{w - 4} L{w - 30} 85 Z" fill="{mix(m, d, .6)}" stroke="{dk}" stroke-width="3" stroke-linejoin="round"/>'
             f'<path d="M70 104 L96 116 V100 Z M{w - 70} 104 L{w - 96} 116 V100 Z" fill="{dk}"/>')  # folds
    body = f"M64 30 Q{w / 2} 14 {w - 64} 30 V104 Q{w / 2} 90 64 104 Z"
    hl = f"M74 38 Q{w / 2} 24 {w - 74} 38 V58 Q{w / 2} 46 74 58 Z"
    return doc(w, h, vgrad("rb", (0, l), (.5, m), (1, mix(m, d, .6))).join(["<defs>", "</defs>"]) + tails
               + f'<path d="{body}" fill="{d}" transform="translate(0 5)"/><path d="{body}" fill="url(#rb)"/>'
               + f'<path d="{hl}" fill="#fff" opacity=".3"/>'
               + f'<path d="M70 36 Q{w / 2} 21 {w - 70} 36" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="2"/>'
               + f'<path d="{body}" fill="none" stroke="{dk}" stroke-width="3.5" stroke-linejoin="round"/>')


def plate_cream(w=300, h=96):
    return doc(w, h, vgrad("pc", (0, "#fff8ec"), (.6, "#f6e2c2"), (1, "#e2c08e")).join(["<defs>", "</defs>"])
               + f'<path d="{rrect(2, 8, w - 4, h - 10, 26)}" fill="#a87a44"/>'
               + f'<path d="{rrect(2, 2, w - 4, h - 10, 26)}" fill="url(#pc)" stroke="#8a5a24" stroke-width="3"/>'
               + f'<path d="{rrect(8, 6, w - 16, (h - 10) * .36, 18)}" fill="#fff" opacity=".6"/>'
               + f'<path d="{rrect(6, 6, w - 12, h - 18, 22)}" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="1.6"/>')


def plate_dark(w=240, h=68):
    return doc(w, h, f'<path d="{rrect(2, 2, w - 4, h - 4, (h - 4) / 2)}" fill="#120a24" fill-opacity=".82" stroke="#000" stroke-opacity=".6" stroke-width="2.5"/>'
               + f'<path d="{rrect(4, 4, w - 8, h - 8, (h - 8) / 2)}" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="1.5"/>'
               + f'<path d="M{h / 2} {h - 6} H{w - h / 2}" stroke="#fff" stroke-opacity=".12" stroke-width="2" stroke-linecap="round"/>')


def track(w=400, h=40):
    return doc(w, h, f'<path d="{rrect(1.5, 1.5, w - 3, h - 3, (h - 3) / 2)}" fill="#160c2a" stroke="#05020c" stroke-width="3"/>'
               + f'<path d="{rrect(5, 5, w - 10, h * .3, h * .15)}" fill="#000" opacity=".45"/>'           # inner top shadow
               + f'<path d="M{h / 2} {h - 4} H{w - h / 2}" stroke="#fff" stroke-opacity=".14" stroke-width="2" stroke-linecap="round"/>')


def fill(c, w=400, h=40):
    l, m, d = c
    return doc(w, h, vgrad("fl", (0, l), (.5, m), (1, d)).join(["<defs>", "</defs>"])
               + f'<path d="{rrect(5, 5, w - 10, h - 10, (h - 10) / 2)}" fill="url(#fl)"/>'
               + f'<path d="{rrect(12, 8, w - 24, (h - 10) * .34, 5)}" fill="#fff" opacity=".55"/>'
               + f'<path d="{rrect(5, 5, w - 10, h - 10, (h - 10) / 2)}" fill="none" stroke="{mix(d, "#000", .3)}" stroke-width="1.5"/>')


ORANGE = ("#ffe08a", "#ffa51f", "#d4600a")  # progress fill default (matches the reference crop)


def crown():
    return doc(120, 90, vgrad("cr", (0, "#fff4b0"), (.5, "#ffc21f"), (1, "#c07000")).join(["<defs>", "</defs>"])
               + '<path d="M14 78 L8 26 L36 50 L60 10 L84 50 L112 26 L106 78 Z" fill="url(#cr)" stroke="#7a4400" stroke-width="3.5" stroke-linejoin="round"/>'
               + '<rect x="12" y="70" width="96" height="14" rx="5" fill="#ffd23a" stroke="#7a4400" stroke-width="3"/>'
               + '<path d="M60 44 L68 54 L60 64 L52 54 Z" fill="#ff3a5a" stroke="#7a0010" stroke-width="2"/>'
               + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff6c0" stroke="#7a4400" stroke-width="2"/>' for x, y in ((8, 24), (60, 8), (112, 24)))
               + '<path d="M22 62 L28 32" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".6"/>')


def sparkle(col="#ffd65a"):
    return doc(48, 48, f'<path d="M24 2 C26 18 30 22 46 24 C30 26 26 30 24 46 C22 30 18 26 2 24 C18 22 22 18 24 2 Z" fill="{col}" filter="url(#glow)" opacity=".7"/>'
               f'<path d="M24 2 C26 18 30 22 46 24 C30 26 26 30 24 46 C22 30 18 26 2 24 C18 22 22 18 24 2 Z" fill="#fff8d0"/>')


def arrow():
    return doc(70, 90, vgrad("ar", (0, "#ffe680"), (1, "#ff9a1a")).join(["<defs>", "</defs>"])
               + '<path d="M12 8 L58 45 L12 82 L26 45 Z" fill="url(#ar)" stroke="#8a4a00" stroke-width="4" stroke-linejoin="round"/>'
               + '<path d="M18 16 L48 42" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".6"/>')


def chest():
    """Reward chest: purple lacquered wood, gold bands, star lock, light burst + pedestal."""
    rays = "".join(f'<path d="M150 150 L{150 + 150 * math.cos(a / 10 * 6.283):.0f} {150 + 150 * math.sin(a / 10 * 6.283):.0f} '
                   f'L{150 + 150 * math.cos((a + .45) / 10 * 6.283):.0f} {150 + 150 * math.sin((a + .45) / 10 * 6.283):.0f} Z" fill="#ffe680" opacity=".22"/>'
                   for a in range(10))
    gold = '<linearGradient id="gd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2a0"/><stop offset=".5" stop-color="#f2b81f"/><stop offset="1" stop-color="#a06000"/></linearGradient>'
    wood = '<linearGradient id="wd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b07aff"/><stop offset=".55" stop-color="#6a2ad0"/><stop offset="1" stop-color="#3a0a8a"/></linearGradient>'
    return doc(300, 300, f'<defs>{gold}{wood}<radialGradient id="hl"><stop offset="0" stop-color="#fff6c0"/><stop offset="1" stop-color="#ffb000" stop-opacity="0"/></radialGradient></defs>'
               + f'<g>{rays}</g><circle cx="150" cy="150" r="130" fill="url(#hl)" opacity=".7"/>'
               + '<ellipse cx="150" cy="262" rx="110" ry="24" fill="#2a1060"/><ellipse cx="150" cy="254" rx="104" ry="20" fill="#9a6aff"/><ellipse cx="150" cy="252" rx="86" ry="13" fill="#d8c0ff" opacity=".5"/>'
               # body
               + '<path d="M58 150 H242 V232 Q242 244 230 244 H70 Q58 244 58 232 Z" fill="url(#wd)" stroke="#1e0650" stroke-width="4"/>'
               # lid (arched)
               + '<path d="M54 150 V118 Q54 70 150 66 Q246 70 246 118 V150 Z" fill="url(#wd)" stroke="#1e0650" stroke-width="4"/>'
               + '<path d="M72 96 Q150 74 228 96" stroke="#fff" stroke-width="6" fill="none" opacity=".35" stroke-linecap="round"/>'
               # gold bands + rim
               + '<rect x="48" y="142" width="204" height="20" rx="6" fill="url(#gd)" stroke="#6a3a00" stroke-width="3"/>'
               + ''.join(f'<path d="M{x} 70 Q{x - 4 if x < 150 else x + 4} 110 {x} 150 V244" stroke="#6a3a00" stroke-width="22" fill="none" opacity=".45"/>'  # band edge
                         f'<path d="M{x} 70 Q{x - 4 if x < 150 else x + 4} 110 {x} 150 V244" stroke="url(#gd)" stroke-width="16" fill="none"/>' for x in (92, 208))
               # star lock plate
               + '<path d="M118 132 H182 V190 Q182 202 170 202 H130 Q118 202 118 190 Z" fill="url(#gd)" stroke="#6a3a00" stroke-width="3.5"/>'
               + '<path d="M150 140 L157 156 L174 157 L161 168 L165 185 L150 176 L135 185 L139 168 L126 157 L143 156 Z" fill="#ffe680" stroke="#8a4a00" stroke-width="2.5" stroke-linejoin="round"/>'
               + '<path d="M146 148 L150 156" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".8"/>'
               + '<path d="M64 228 H236" stroke="#000" stroke-opacity=".25" stroke-width="4"/>', 0)


def reward(kind):
    if kind == "coin":
        return doc(96, 96, vgrad("cn", (0, "#fff4a0"), (.5, "#ffc21f"), (1, "#b06a00")).join(["<defs>", "</defs>"])
                   + '<circle cx="48" cy="48" r="42" fill="url(#cn)" stroke="#7a4400" stroke-width="4"/><circle cx="48" cy="48" r="32" fill="none" stroke="#fff6c0" stroke-width="3" opacity=".8"/>'
                   + '<path d="M56 34 Q48 28 40 34 Q36 42 48 48 Q60 54 56 62 Q48 68 40 62 M48 26 V70" stroke="#8a4a00" stroke-width="5" fill="none" stroke-linecap="round"/>'
                   + '<ellipse cx="34" cy="30" rx="10" ry="6" fill="#fff" opacity=".6" transform="rotate(-30 34 30)"/>')
    if kind == "orb":
        return doc(96, 96, '<defs><radialGradient id="ob" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="#7ff3ff"/>'
                   '<stop offset=".65" stop-color="#b04aff"/><stop offset="1" stop-color="#3a0a8a"/></radialGradient></defs>'
                   '<circle cx="48" cy="48" r="42" fill="url(#ob)" stroke="#2a0a6a" stroke-width="3"/><path d="M14 56 Q48 36 82 58" stroke="#5fff9a" stroke-width="6" fill="none" opacity=".5"/>'
                   '<ellipse cx="34" cy="30" rx="11" ry="6" fill="#fff" opacity=".8" transform="rotate(-30 34 30)"/>')
    return doc(110, 90, '<g transform="rotate(-14 55 45)"><path d="M10 20 H100 V36 A9 9 0 0 0 100 54 V70 H10 V54 A9 9 0 0 0 10 36 Z" fill="#a070ff" stroke="#2a0a6a" stroke-width="3.5"/>'
                   '<path d="M32 20 V70" stroke="#2a0a6a" stroke-width="2" stroke-dasharray="4 4"/>'
                   '<path d="M64 32 L68 41 L78 42 L70 48 L73 58 L64 52 L55 58 L58 48 L50 42 L60 41 Z" fill="#fff"/><rect x="16" y="24" width="80" height="8" rx="4" fill="#fff" opacity=".35"/></g>')


# ---- panels & banners parts ------------------------------------------------------------------------
def header(c, w=480, h=88):
    """Panel title bar: big top radius, flat bottom edge, glossy. 3-slice horizontally (slice 0 60)."""
    l, m, d = c
    bar = f"M2 {h - 2} V34 A32 32 0 0 1 34 2 H{w - 34} A32 32 0 0 1 {w - 2} 34 V{h - 2} Z"
    return doc(w, h, vgrad("hd", (0, l), (.5, m), (1, mix(m, d, .5))).join(["<defs>", "</defs>"])
               + f'<path d="{bar}" fill="url(#hd)" stroke="{mix(d, "#000", .45)}" stroke-width="3"/>'
               + f'<path d="M14 {h * .42} V34 A22 22 0 0 1 36 12 H{w - 36} A22 22 0 0 1 {w - 14} 34 V{h * .42} Z" fill="#fff" opacity=".28"/>'
               + f'<path d="M4 {h - 6} H{w - 4}" stroke="{d}" stroke-width="5" opacity=".6"/>')


def tag(c):
    """Vertical bookmark ribbon with a notched tail (NEW / HOT / LV 5)."""
    l, m, d = c
    shape = "M6 4 H74 V120 L40 100 L6 120 Z"
    return doc(80, 126, vgrad("tg", (0, l), (.5, m), (1, d)).join(["<defs>", "</defs>"])
               + f'<path d="{shape}" fill="url(#tg)" stroke="{mix(d, "#000", .45)}" stroke-width="3" stroke-linejoin="round"/>'
               + '<path d="M14 10 H32 V96 L14 108 Z" fill="#fff" opacity=".22"/><path d="M10 8 H70" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>')


def corner(c):
    """Diagonal corner ribbon for the top-right of cards (BEST VALUE). Text is rotated 45° in HTML."""
    l, m, d = c
    return doc(170, 170, vgrad("cr2", (0, l), (.5, m), (1, d)).join(["<defs>", "</defs>"])
               + f'<path d="M150 170 L170 150 V170 Z M0 20 L20 0 H0 Z" fill="{mix(d, "#000", .35)}"/>'
               + f'<path d="M20 0 H78 L170 92 V150 Z" fill="url(#cr2)" stroke="{mix(d, "#000", .45)}" stroke-width="3" stroke-linejoin="round"/>'
               + '<path d="M34 6 H70 L164 100 V112 Z" fill="#fff" opacity=".25"/>')


def burst(c):
    """Starburst badge (‑50%, x2, SALE)."""
    l, m, d = c
    pts = " ".join(f"{70 + (64 if i % 2 == 0 else 54) * math.cos(i * math.pi / 14):.1f},{70 + (64 if i % 2 == 0 else 54) * math.sin(i * math.pi / 14):.1f}" for i in range(28))
    return doc(140, 140, '<defs><radialGradient id="bs" cx="40%" cy="35%" r="70%">' + f'<stop offset="0" stop-color="{l}"/><stop offset=".6" stop-color="{m}"/><stop offset="1" stop-color="{d}"/></radialGradient></defs>'
               + f'<polygon points="{pts}" fill="{mix(d, "#000", .4)}" transform="translate(0 4)"/>'
               + f'<polygon points="{pts}" fill="url(#bs)" stroke="{mix(d, "#000", .45)}" stroke-width="3" stroke-linejoin="round"/>'
               + '<circle cx="70" cy="70" r="44" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2" stroke-dasharray="3 5"/>'
               + '<ellipse cx="52" cy="44" rx="20" ry="10" fill="#fff" opacity=".35" transform="rotate(-25 52 44)"/>')


def bubble():
    """Callout body (cream, 9-slice 34) — pair with chr_shared_tail.svg for the pointer."""
    return doc(120, 120, vgrad("bb", (0, "#fffdf6"), (1, "#f2e0c2")).join(["<defs>", "</defs>"])
               + f'<path d="{rrect(2, 2, 116, 112, 28)}" fill="#a87a44"/><path d="{rrect(2, 2, 116, 108, 28)}" fill="url(#bb)" stroke="#8a5a24" stroke-width="3"/>'
               + f'<path d="{rrect(8, 6, 104, 34, 20)}" fill="#fff" opacity=".7"/>')


def tail():
    return doc(60, 44, '<path d="M4 0 H56 L14 42 Z" fill="#f2e0c2" stroke="#8a5a24" stroke-width="3" stroke-linejoin="round"/><path d="M2 2 H58" stroke="#f2e0c2" stroke-width="5"/>')


def rays(col="#ffe680"):
    """Rotating light rays behind reward icons."""
    r = "".join(f'<path d="M200 200 L{200 + 200 * math.cos(a / 16 * 6.283):.0f} {200 + 200 * math.sin(a / 16 * 6.283):.0f} '
                f'L{200 + 200 * math.cos((a + .5) / 16 * 6.283):.0f} {200 + 200 * math.sin((a + .5) / 16 * 6.283):.0f} Z"/>' for a in range(16))
    return doc(400, 400, f'<defs><radialGradient id="rf"><stop offset="0" stop-color="{col}" stop-opacity=".9"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>'
               f'<g fill="url(#rf)">{r}</g><circle cx="200" cy="200" r="90" fill="url(#rf)"/>')


def divider():
    return doc(300, 24, '<path d="M10 12 H120 M180 12 H290" stroke="#fff" stroke-opacity=".35" stroke-width="2" stroke-linecap="round"/>'
               '<path d="M150 2 L160 12 L150 22 L140 12 Z" fill="#ffd65a" stroke="#7a4400" stroke-width="2"/><circle cx="128" cy="12" r="3" fill="#ffd65a"/><circle cx="172" cy="12" r="3" fill="#ffd65a"/>')


def socket(c):
    """Round icon socket that sits above a panel (icon overlaps the top edge)."""
    l, m, d = c
    return doc(130, 130, '<defs><radialGradient id="sk" cx="40%" cy="35%" r="70%">' + f'<stop offset="0" stop-color="{l}"/><stop offset=".6" stop-color="{m}"/><stop offset="1" stop-color="{d}"/></radialGradient></defs>'
               + f'<circle cx="65" cy="69" r="60" fill="{mix(d, "#000", .4)}"/><circle cx="65" cy="65" r="60" fill="url(#sk)" stroke="{mix(d, "#000", .45)}" stroke-width="3"/>'
               + f'<circle cx="65" cy="65" r="47" fill="{mix(d, "#000", .35)}"/><circle cx="65" cy="65" r="47" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="2"/>'
               + '<path d="M22 44 A48 48 0 0 1 70 12" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".55"/>')


# ---- ribbon collection: curved / wave / bow (per tone) + laurels, stars, plaque, wings, trophy ------
# Each curved ribbon exposes its text arc (ARCS) so pages can lay labels along the curve with <textPath>.
# centre line of each band (midway between its top and bottom edges); labels sit on it with dy=.36em
ARCS = {"curved": "M90 115 Q300 51 510 115", "wave": "M80 117 C210 57 390 167 520 107"}


def _tails(c, y, flip=False):
    """Folded ribbon tail + the darker fold triangle that sells the 3D twist."""
    l, m, d = c
    dk, back = mix(d, "#000", .45), mix(m, d, .7)
    t = (f'<path d="M110 {y - 8} L18 {y + 6} L46 {y + 44} L14 {y + 84} L112 {y + 76} Z" fill="{back}" stroke="{dk}" stroke-width="3.5" stroke-linejoin="round"/>'
         f'<path d="M30 {y + 12} L100 {y + 4}" stroke="#fff" stroke-opacity=".25" stroke-width="3"/>'
         f'<path d="M92 {y + 58} L112 {y + 76} L112 {y + 46} Z" fill="{mix(d, "#000", .3)}" stroke="{dk}" stroke-width="3" stroke-linejoin="round"/>')
    return f'<g transform="translate(600 0) scale(-1 1)">{t}</g>' if flip else t


def curved(c):
    l, m, d = c
    dk = mix(d, "#000", .45)
    band = "M90 70 Q300 6 510 70 L510 160 Q300 96 90 160 Z"
    return doc(600, 230, vgrad("cv", (0, l), (.5, m), (1, mix(m, d, .55))).join(["<defs>", "</defs>"])
               + _tails(c, 96) + _tails(c, 96, True)
               + f'<path d="{band}" fill="{d}" transform="translate(0 7)"/><path d="{band}" fill="url(#cv)"/>'
               + '<path d="M104 84 Q300 24 496 84 L496 104 Q300 46 104 104 Z" fill="#fff" opacity=".28"/>'
               + '<path d="M100 76 Q300 14 500 76" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="2.5"/>'
               + f'<path d="M96 150 Q300 88 504 150" fill="none" stroke="{dk}" stroke-opacity=".35" stroke-width="4"/>'
               + f'<path d="{band}" fill="none" stroke="{dk}" stroke-width="4" stroke-linejoin="round"/>')


def wave(c):
    l, m, d = c
    dk = mix(d, "#000", .45)
    band = "M80 74 C210 14 390 124 520 64 L520 150 C390 210 210 100 80 160 Z"
    return doc(600, 240, vgrad("wv", (0, l), (.5, m), (1, mix(m, d, .55))).join(["<defs>", "</defs>"])
               + _tails(c, 100) + _tails(c, 70, True)
               + f'<path d="{band}" fill="{d}" transform="translate(0 7)"/><path d="{band}" fill="url(#wv)"/>'
               + '<path d="M92 84 C220 28 384 136 508 76 L508 96 C384 156 220 48 92 104 Z" fill="#fff" opacity=".26"/>'
               + f'<path d="{band}" fill="none" stroke="{dk}" stroke-width="4" stroke-linejoin="round"/>')


def bow(c):
    l, m, d = c
    dk = mix(d, "#000", .45)
    g = vgrad("bw", (0, l), (.5, m), (1, mix(m, d, .6))).join(["<defs>", "</defs>"])
    loop = lambda sx: (f'<g transform="translate(150 0) scale({sx} 1) translate(-150 0)">'
                       f'<path d="M140 92 C110 40 40 30 34 70 C28 110 96 118 140 104 Z" fill="url(#bw)" stroke="{dk}" stroke-width="4" stroke-linejoin="round"/>'
                       f'<path d="M126 92 C104 64 70 60 60 78 C78 74 104 84 124 98 Z" fill="{mix(d, "#000", .2)}" opacity=".6"/>'
                       '<path d="M52 62 C64 50 90 50 104 60" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" opacity=".5"/></g>')
    tail = lambda sx: (f'<g transform="translate(150 0) scale({sx} 1) translate(-150 0)">'
                       f'<path d="M138 108 L94 196 L112 188 L118 210 L156 112 Z" fill="{mix(m, d, .45)}" stroke="{dk}" stroke-width="4" stroke-linejoin="round"/></g>')
    return doc(300, 220, g + tail(1) + tail(-1) + loop(1) + loop(-1)
               + f'<rect x="126" y="78" width="48" height="40" rx="14" fill="url(#bw)" stroke="{dk}" stroke-width="4"/>'
               + '<rect x="134" y="84" width="32" height="10" rx="5" fill="#fff" opacity=".45"/>')


def laurel(col=("#fff2a0", "#f2b81f", "#9a5a00")):
    """One laurel branch (left side); mirror it for the right. Paired leaves along a sweeping stem."""
    l, m, d = col
    stem = lambda t: (96 - 70 * math.sin(t * 1.75), 208 - 186 * t)   # sweeping curve bottom-right → top-left
    leaves = ""
    for i in range(9):
        t = .08 + i / 9.4
        x, y = stem(t)
        x2, y2 = stem(t + .01)
        ang = math.degrees(math.atan2(y2 - y, x2 - x))
        size = 1.15 - t * .45
        for side in (-1, 1):
            a = math.radians(ang + side * 52)
            cx, cy = x + math.cos(a) * 15 * size, y + math.sin(a) * 15 * size
            leaves += (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{20 * size:.1f}" ry="{8.5 * size:.1f}" fill="url(#lf)" stroke="{d}" stroke-width="2.4" '
                       f'transform="rotate({ang + side * 52:.0f} {cx:.1f} {cy:.1f})"/>'
                       f'<path d="M{x:.1f} {y:.1f} L{cx:.1f} {cy:.1f}" stroke="{d}" stroke-width="1.4" opacity=".6"/>')
    tip_x, tip_y = stem(1)
    path = "M" + " L".join(f"{stem(i / 30)[0]:.1f} {stem(i / 30)[1]:.1f}" for i in range(31))
    return doc(140, 224, f'<defs><linearGradient id="lf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{l}"/><stop offset=".55" stop-color="{m}"/><stop offset="1" stop-color="{d}"/></linearGradient></defs>'
               + f'<path d="{path}" stroke="{d}" stroke-width="6" fill="none" stroke-linecap="round"/>' + leaves
               + f'<ellipse cx="{tip_x:.1f}" cy="{tip_y:.1f}" rx="9" ry="16" fill="url(#lf)" stroke="{d}" stroke-width="2.4" transform="rotate(-20 {tip_x:.1f} {tip_y:.1f})"/>')


STAR5 = " ".join(f"{100 + (92 if i % 2 == 0 else 42) * math.cos(i * math.pi / 5 - math.pi / 2):.1f},{104 + (92 if i % 2 == 0 else 42) * math.sin(i * math.pi / 5 - math.pi / 2):.1f}" for i in range(10))


def big_star(face=False):
    """Chunky glossy gold star with a 3D lip; optional original cute face."""
    f = ('<ellipse cx="80" cy="108" rx="7" ry="10" fill="#3a1a00"/><ellipse cx="120" cy="108" rx="7" ry="10" fill="#3a1a00"/>'
         '<circle cx="82" cy="104" r="3" fill="#fff"/><circle cx="122" cy="104" r="3" fill="#fff"/>'
         '<path d="M88 126 Q100 138 112 126" stroke="#3a1a00" stroke-width="5" fill="none" stroke-linecap="round"/>'
         '<ellipse cx="66" cy="124" rx="9" ry="5" fill="#ff7a5a" opacity=".5"/><ellipse cx="134" cy="124" rx="9" ry="5" fill="#ff7a5a" opacity=".5"/>') if face else ""
    return doc(200, 210, '<defs><radialGradient id="sg" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#fff8c0"/><stop offset=".45" stop-color="#ffcc2a"/><stop offset="1" stop-color="#e07a00"/></radialGradient></defs>'
               + f'<polygon points="{STAR5}" fill="#a85200" stroke="#a85200" stroke-width="14" stroke-linejoin="round" transform="translate(0 8)"/>'
               + f'<polygon points="{STAR5}" fill="url(#sg)" stroke="#8a4000" stroke-width="12" stroke-linejoin="round"/>'
               + f'<polygon points="{STAR5}" fill="url(#sg)"/>'
               + '<path d="M100 30 L116 72 L160 74 M100 30 L84 72" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".55"/>' + f)


def plaque():
    """Carved stone plaque with cracks, moss and bolts (VICTORY slab)."""
    return doc(420, 170, vgrad("st", (0, "#c8ccd6"), (.5, "#8a909c"), (1, "#5a606c")).join(["<defs>", "</defs>"])
               + '<path d="M30 30 Q60 12 210 16 Q370 10 394 34 Q414 84 398 130 Q360 156 210 152 Q50 158 24 132 Q8 84 30 30 Z" fill="#3a3e46" transform="translate(0 8)"/>'
               + '<path d="M30 30 Q60 12 210 16 Q370 10 394 34 Q414 84 398 130 Q360 156 210 152 Q50 158 24 132 Q8 84 30 30 Z" fill="url(#st)" stroke="#2a2d33" stroke-width="4"/>'
               + '<path d="M44 34 Q210 22 380 38 L376 56 Q210 40 46 54 Z" fill="#fff" opacity=".25"/>'
               + '<path d="M70 120 L88 100 L84 86 M330 40 L340 60 L358 66" stroke="#2a2d33" stroke-width="3" fill="none" stroke-linecap="round"/>'
               + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#5fa83a"/>' for x, y, r in ((30, 60, 9), (40, 50, 6), (390, 120, 8), (380, 132, 6), (24, 110, 5)))
               + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="url(#mt2)" stroke="#2a2d33" stroke-width="2"/>' for x, y in ((52, 84), (368, 84))).replace("url(#mt2)", "#a8aeb8"))


def plus_btn():
    return doc(64, 64, '<defs><radialGradient id="pb" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#9ff8ff"/><stop offset=".6" stop-color="#1fb8d8"/><stop offset="1" stop-color="#0a5a7a"/></radialGradient></defs>'
               '<circle cx="32" cy="35" r="28" fill="#063a50"/><circle cx="32" cy="32" r="28" fill="url(#pb)" stroke="#063a50" stroke-width="3"/>'
               '<path d="M32 18 V46 M18 32 H46" stroke="#fff" stroke-width="7" stroke-linecap="round"/><ellipse cx="24" cy="20" rx="9" ry="5" fill="#fff" opacity=".5"/>')


def wing():
    """One gold wing (left; mirror for the right): five layered feathers fanning up from the root."""
    feathers = ""
    for i, (ang, ln) in enumerate(((198, 96), (214, 118), (232, 132), (252, 128), (272, 104))):
        a = math.radians(ang); tx, ty = 150 + ln * math.cos(a), 170 + ln * math.sin(a)
        n = math.radians(ang + 90); w = 17
        feathers += (f'<path d="M150 170 Q{150 + w * math.cos(n) + ln * .5 * math.cos(a):.0f} {170 + w * math.sin(n) + ln * .5 * math.sin(a):.0f} {tx:.0f} {ty:.0f} '
                     f'Q{150 - w * math.cos(n) + ln * .55 * math.cos(a):.0f} {170 - w * math.sin(n) + ln * .55 * math.sin(a):.0f} 150 170 Z" fill="url(#wg)" stroke="#8a4a00" stroke-width="3" stroke-linejoin="round"/>'
                     f'<path d="M150 170 L{150 + ln * .8 * math.cos(a):.0f} {170 + ln * .8 * math.sin(a):.0f}" stroke="#fff6c0" stroke-width="2" opacity=".6"/>')
    return doc(170, 190, '<defs><linearGradient id="wg" x1="1" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#c06a00"/><stop offset=".45" stop-color="#ffb81f"/><stop offset="1" stop-color="#fff2a0"/></linearGradient></defs>'
               + feathers + '<circle cx="150" cy="170" r="12" fill="#f2b81f" stroke="#8a4a00" stroke-width="3"/>')


def trophy():
    return doc(160, 170, vgrad("tp", (0, "#fff4a0"), (.5, "#f2b81f"), (1, "#a05a00")).join(["<defs>", "</defs>"])
               + '<path d="M44 22 H116 V60 A36 36 0 0 1 44 60 Z" fill="url(#tp)" stroke="#6a3a00" stroke-width="4"/>'
               + '<path d="M44 34 H22 Q14 70 50 84 M116 34 H138 Q146 70 110 84" stroke="url(#tp)" stroke-width="10" fill="none" stroke-linecap="round"/>'
               + '<path d="M44 34 H22 Q14 70 50 84 M116 34 H138 Q146 70 110 84" stroke="#6a3a00" stroke-width="3" fill="none" opacity=".5"/>'
               + '<rect x="70" y="96" width="20" height="28" fill="url(#tp)" stroke="#6a3a00" stroke-width="3"/><rect x="46" y="122" width="68" height="24" rx="6" fill="url(#tp)" stroke="#6a3a00" stroke-width="4"/>'
               + '<path d="M58 30 V58" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".6"/>')


def write(f, data):
    d = os.path.join(OUT, folder_for(f)); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f), "w").write(data)
    return f"{folder_for(f)}/{f}"


if __name__ == "__main__":
    out = {"slice": SLICE, "arcs": ARCS, "tones": {}}
    for tid in ["brand", *THEMES]:
        c = tone(tid)
        parts = {"close": close_btn(c), "pill": pill(c), "frame": frame(c), "ribbon": ribbon(c), "fill": fill(c),
                 "header": header(c), "tag": tag(c), "corner": corner(c), "burst": burst(c), "socket": socket(c),
                 "curved": curved(c), "wave": wave(c), "bow": bow(c)}
        out["tones"][tid] = {k: write(f"chr_{tid}_{k}.svg", v) for k, v in parts.items()}
    shared = {"plate-cream": plate_cream(), "plate-dark": plate_dark(), "track": track(), "fill-orange": fill(ORANGE), "crown": crown(),
              "sparkle": sparkle(), "arrow": arrow(), "chest": chest(), "reward-coin": reward("coin"), "reward-orb": reward("orb"), "reward-ticket": reward("ticket"),
              "bubble": bubble(), "tail": tail(), "rays": rays(), "divider": divider(),
              "laurel-gold": laurel(), "laurel-green": laurel(("#d8ffa0", "#4fc23a", "#1f6a12")), "star-gold": big_star(), "star-face": big_star(True),
              "plaque": plaque(), "plus": plus_btn(), "wing": wing(), "trophy": trophy()}
    out["shared"] = {k: write(f"chr_shared_{k}.svg", v) for k, v in shared.items()}
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "data", "chrome.json"), "w"), indent=1)
    print(f"wrote {sum(len(v) for v in out['tones'].values()) + len(shared)} chrome parts + data/chrome.json")
