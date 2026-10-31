# World scene backgrounds (768×1024 portrait), one per level theme. Layered vector illustration:
#   sky → far silhouettes → mid elements → foreground → light/particles → vignette.
#   assets/scenes/<theme>/scn_<theme>_card.svg      (path recorded in data/levels.json as "scene")
# These are the drop-in slot for painted art: replace the file with a same-size PNG/WebP/SVG and nothing else changes.
import json, math, os, random
from layout import folder_for

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
W, H = 768, 1024


def doc(body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs>'
            '<filter id="b8" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>'
            '<filter id="b20" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="20"/></filter>'
            '<filter id="b40" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>'
            '<radialGradient id="vig" cx="50%" cy="45%" r="75%"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>'
            f'{defs}</defs>{body}<rect width="{W}" height="{H}" fill="url(#vig)"/></svg>')


def sky(*stops, k="sky"):
    return (f'<linearGradient id="{k}" x1="0" y1="0" x2="0" y2="1">' + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + "</linearGradient>",
            f'<rect width="{W}" height="{H}" fill="url(#{k})"/>')


def glow(cx, cy, rx, ry, col, op=1, blur="b40"):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}" opacity="{op}" filter="url(#{blur})"/>'


def dots(seed, n, x0, y0, x1, y1, r0, r1, col, op=(.5, 1), glowing=False):
    rnd = random.Random(seed)
    out = ""
    for _ in range(n):
        x, y, r, o = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(r0, r1), rnd.uniform(*op)
        if glowing: out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r * 3:.1f}" fill="{col}" opacity="{o * .35:.2f}" filter="url(#b8)"/>'
        out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{col}" opacity="{o:.2f}"/>'
    return out


def ridge(seed, y, amp, col, n=9, op=1):
    """Jagged silhouette band across the scene (mountains, trees, rocks)."""
    rnd = random.Random(seed)
    pts = [(0, H)] + [(i * W / n, y + rnd.uniform(-amp, amp)) for i in range(n + 1)] + [(W, H)]
    return f'<polygon points="{" ".join(f"{x:.0f},{yy:.0f}" for x, yy in pts)}" fill="{col}" opacity="{op}"/>'


def hills(y, amp, col, waves=2.5, phase=0, op=1):
    d = f"M0 {H} L0 {y}" + "".join(f" L{x} {y + amp * math.sin(x / W * waves * 2 * math.pi + phase):.0f}" for x in range(0, W + 16, 16)) + f" L{W} {H} Z"
    return f'<path d="{d}" fill="{col}" opacity="{op}"/>'


# ---- scenes ------------------------------------------------------------------------------------------
def volcano():
    d, s = sky((0, "#1a0404"), (.45, "#6a140a"), (.72, "#e0501a"), (1, "#ffb04a"))
    cone = "M60 760 L300 330 Q384 300 468 330 L708 760 Z"
    lava = ["M372 340 Q350 460 300 560 T250 760", "M404 340 Q430 470 480 580 T540 760", "M388 342 Q392 500 380 760"]
    return doc(s + glow(384, 160, 330, 170, "#2a0a08", .9, "b40") + glow(160, 120, 200, 90, "#3a1210", .8) + glow(620, 180, 200, 100, "#3a1210", .8)
               + ridge(2, 640, 60, "#3a0e08", 7)
               + '<defs><linearGradient id="cn" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a1a10"/><stop offset=".55" stop-color="#2a0e08"/><stop offset="1" stop-color="#140604"/></linearGradient></defs>'
               + f'<path d="{cone}" fill="url(#cn)"/>' + glow(384, 320, 140, 60, "#ff8a1a", .95, "b20") + glow(384, 210, 120, 150, "#ff6a1a", .6, "b40")
               + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffd27a" filter="url(#b8)" opacity=".9"/>' for x, y, r in ((384, 270, 34), (350, 220, 22), (420, 200, 26), (384, 150, 18)))
               + "".join(f'<path d="{p}" stroke="#ff5a0a" stroke-width="22" fill="none" filter="url(#b8)" opacity=".9"/><path d="{p}" stroke="#ff8a1a" stroke-width="12" fill="none"/>'
                         f'<path d="{p}" stroke="#ffe8a0" stroke-width="4" fill="none"/>' for p in lava)
               + '<path d="M384 300 Q330 150 250 90 M384 300 Q440 140 520 70 M384 300 Q390 120 400 40" stroke="#ffb04a" stroke-width="5" fill="none" stroke-dasharray="2 26" stroke-linecap="round"/>'
               + ridge(5, 860, 40, "#1a0604", 10) + '<path d="M80 900 L200 880 L260 920 M520 910 L600 880 L700 900" stroke="#ff6a1a" stroke-width="5" fill="none" filter="url(#b8)"/>'
               + ridge(9, 960, 30, "#0c0302", 12) + dots(1, 70, 0, 0, W, 800, 1.5, 4, "#ffb04a", (.4, 1), True), d)


def island(x, y, s, tree=True):
    t = (f'<rect x="{x - 4 * s}" y="{y - 46 * s}" width="{8 * s}" height="{30 * s}" fill="#6a4020"/>'
         f'<circle cx="{x}" cy="{y - 56 * s}" r="{24 * s}" fill="#3aa84a"/><circle cx="{x - 8 * s}" cy="{y - 64 * s}" r="{12 * s}" fill="#6fd65a"/>') if tree else ""
    return (f'<path d="M{x - 90 * s} {y} Q{x - 60 * s} {y + 60 * s} {x - 10 * s} {y + 120 * s} Q{x + 10 * s} {y + 70 * s} {x + 90 * s} {y} Z" fill="#8a5a34"/>'
            f'<path d="M{x - 90 * s} {y} Q{x - 40 * s} {y + 40 * s} {x} {y + 50 * s} Q{x + 40 * s} {y + 30 * s} {x + 90 * s} {y} Z" fill="#6a4020"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{92 * s}" ry="{20 * s}" fill="#4fc23a"/><ellipse cx="{x - 10 * s}" cy="{y - 4 * s}" rx="{70 * s}" ry="{10 * s}" fill="#9aee6a"/>{t}')


def cloud(x, y, s, op=1, col="#fff"):
    return f'<g opacity="{op}" fill="{col}">' + "".join(f'<circle cx="{x + dx * s}" cy="{y + dy * s}" r="{r * s}"/>' for dx, dy, r in
                                                       ((-60, 10, 40), (-20, -10, 52), (30, 0, 46), (70, 14, 34), (0, 24, 44))) + "</g>"


def sky_islands():
    d, s = sky((0, "#5ab0ff"), (.6, "#a8dcff"), (1, "#e8f6ff"))
    balloon = ('<g transform="translate(590 230)"><path d="M0 -70 C46 -70 62 -30 50 10 C40 40 14 56 8 70 H-8 C-14 56 -40 40 -50 10 C-62 -30 -46 -70 0 -70 Z" fill="#ff5a4a"/>'
               '<path d="M0 -70 C18 -50 20 30 8 70 H-8 C-20 30 -18 -50 0 -70 Z" fill="#ffd23a"/><path d="M-50 10 Q0 24 50 10" stroke="#c02a1a" stroke-width="4" fill="none"/>'
               '<ellipse cx="-22" cy="-40" rx="10" ry="18" fill="#fff" opacity=".45"/><path d="M-8 70 L-10 90 M8 70 L10 90" stroke="#6a4020" stroke-width="2"/>'
               '<rect x="-14" y="88" width="28" height="20" rx="3" fill="#a06a34"/></g>')
    return doc(s + glow(640, 120, 160, 160, "#fff8d0", .9) + cloud(160, 200, 1.2, .55) + cloud(420, 120, .9, .5)
               + island(200, 420, .9) + island(560, 560, .7) + island(150, 700, .55, False) + balloon
               + cloud(120, 960, 2.2) + cloud(420, 990, 2.6) + cloud(700, 950, 2) + cloud(300, 900, 1.4, .9, "#f2f8ff")
               + dots(3, 18, 0, 0, W, 600, 1, 2.5, "#fff", (.5, .9)), d)


def mushroom(x, y, s, col, dk):
    return (glow(x, y - 40 * s, 70 * s, 50 * s, col, .6, "b20")
            + f'<path d="M{x - 12 * s} {y - 30 * s} Q{x - 16 * s} {y + 20 * s} {x - 10 * s} {y + 40 * s} H{x + 10 * s} Q{x + 16 * s} {y + 20 * s} {x + 12 * s} {y - 30 * s} Z" fill="#f2e6d0"/>'
            f'<path d="M{x - 60 * s} {y - 30 * s} C{x - 60 * s} {y - 90 * s} {x + 60 * s} {y - 90 * s} {x + 60 * s} {y - 30 * s} Q{x} {y - 16 * s} {x - 60 * s} {y - 30 * s} Z" fill="{col}"/>'
            f'<path d="M{x - 60 * s} {y - 30 * s} Q{x} {y - 16 * s} {x + 60 * s} {y - 30 * s}" stroke="{dk}" stroke-width="{4 * s}" fill="none"/>'
            + "".join(f'<circle cx="{x + dx * s}" cy="{y + dy * s}" r="{r * s}" fill="#fff" opacity=".9"/>' for dx, dy, r in ((-30, -50, 9), (0, -66, 8), (28, -48, 10), (12, -36, 5))))


def forest():
    d, s = sky((0, "#03140a"), (.5, "#0c3a20"), (.75, "#2a7a4a"), (1, "#0a2a14"))
    shafts = "".join(f'<polygon points="{x},0 {x + 60},0 {x + 220},700 {x + 120},700" fill="#e8ffd0" opacity=".07"/>' for x in (120, 300, 470))
    trees = lambda seed, y, col, n: "".join(f'<path d="M{x} {y} L{x - 50} {y + 160} H{x + 50} Z M{x} {y + 70} L{x - 70} {y + 260} H{x + 70} Z" fill="{col}"/>'
                                            for x in [random.Random(seed + i).uniform(0, W) for i in range(n)])
    return doc(s + glow(384, 420, 300, 160, "#5ad48a", .35) + shafts + trees(1, 260, "#0a3a1e", 9) + trees(7, 380, "#072a14", 7)
               + ridge(4, 720, 30, "#062010", 12) + mushroom(130, 860, 1.4, "#b04aff", "#5a1aa0") + mushroom(640, 820, 1.1, "#e04ab8", "#7a0a5a") + mushroom(520, 940, .7, "#7f5aff", "#3a1aa0")
               + hills(930, 20, "#041a0c", 4) + dots(5, 40, 0, 200, W, 900, 2, 4, "#d8ff7a", (.5, 1), True), d)


def tundra():
    d, s = sky((0, "#06102a"), (.55, "#1a3a7a"), (1, "#7ab8f0"))
    aurora = "".join(f'<path d="M-40 {y} C160 {y - 90} 330 {y + 60} 480 {y - 30} S700 {y - 60} 820 {y}" stroke="{c}" stroke-width="{w}" fill="none" opacity=".75" filter="url(#b20)"/>'
                     for y, c, w in ((180, "#3affb0", 60), (240, "#3ad8ff", 40), (150, "#ff7ad9", 26)))
    peaks = ("M-20 700 L140 420 L240 560 L380 330 L520 560 L620 440 L790 700 Z", "M140 420 L110 470 L160 480 L190 460 Z M380 330 L340 400 L390 420 L420 400 Z M620 440 L590 490 L640 500 L660 480 Z")
    return doc(s + dots(6, 80, 0, 0, W, 500, .8, 2, "#fff", (.4, 1)) + aurora
               + f'<path d="{peaks[0]}" fill="#c8dcf4"/><path d="M380 330 L520 560 L620 440 L790 700 H380 Z" fill="#8aaad8" opacity=".6"/><path d="{peaks[1]}" fill="#fff"/>'
               + '<ellipse cx="384" cy="780" rx="460" ry="80" fill="#5a9ad8"/><ellipse cx="384" cy="770" rx="420" ry="60" fill="#8ac8f4" opacity=".7"/>'
               + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .28}" fill="#eaf8ff"/><ellipse cx="{x}" cy="{y + 4}" rx="{rx}" ry="{rx * .2}" fill="#a8d0f0" opacity=".6"/>' for x, y, rx in ((180, 790, 70), (520, 810, 90), (650, 770, 40)))
               + hills(900, 30, "#f4fbff", 2) + hills(950, 24, "#dcebf8", 3, 1) + dots(8, 60, 0, 0, W, H, 1.5, 3.5, "#fff", (.5, .95)), d)


def fish(x, y, s, body, stripe, flip=1):
    return (f'<g transform="translate({x} {y}) scale({s * flip} {s})"><path d="M-40 0 C-20 -30 30 -30 46 0 C30 30 -20 30 -40 0 Z" fill="{body}"/>'
            f'<path d="M-36 0 L-66 -24 L-60 0 L-66 24 Z" fill="{body}"/><path d="M-6 -24 Q-14 0 -6 24 M14 -24 Q6 0 14 24" stroke="{stripe}" stroke-width="7" fill="none"/>'
            '<circle cx="28" cy="-6" r="6" fill="#fff"/><circle cx="30" cy="-6" r="3" fill="#102030"/><path d="M-10 -26 Q4 -44 20 -24" fill="' + body + '"/></g>')


def reef():
    d, s = sky((0, "#2ad0e8"), (.45, "#0a7aa8"), (1, "#03283e"))
    rays = "".join(f'<polygon points="{x},0 {x + 40},0 {x + 160},900 {x + 60},900" fill="#e8ffff" opacity=".08"/>' for x in (80, 260, 430, 600))
    kelp = "".join(f'<path d="M{x} 1024 C{x - 40} 840 {x + 40} 700 {x - 10} {h}" stroke="#1fa86a" stroke-width="16" fill="none" stroke-linecap="round"/>'
                   f'<path d="M{x} 1024 C{x - 40} 840 {x + 40} 700 {x - 10} {h}" stroke="#5fe08a" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/>' for x, h in ((60, 560), (130, 680), (680, 600), (730, 720)))
    coral = "".join(f'<path d="M{x} 1000 C{x} 940 {x + dx} 900 {x + dx * 1.6} 840" stroke="{c}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
                    for x, dx, c, w in ((240, -30, "#ff6a8a", 18), (260, 20, "#ff6a8a", 14), (300, 40, "#ff8aa0", 12), (470, -20, "#ffa040", 18), (500, 30, "#ffb860", 14), (560, -10, "#ff6aa8", 16)))
    fan = '<path d="M380 1000 C300 900 330 800 380 780 C430 800 460 900 380 1000 Z" fill="#c84ab8" opacity=".85"/><path d="M380 1000 L380 800 M380 960 L340 860 M380 960 L420 860" stroke="#ff9ae8" stroke-width="3"/>'
    bubbles = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#e8ffff" stroke-width="2" opacity=".7"/><circle cx="{x - r * .3}" cy="{y - r * .3}" r="{r * .25}" fill="#fff" opacity=".8"/>'
                      for x, y, r in [(random.Random(i).uniform(40, 740), random.Random(i + 50).uniform(80, 900), random.Random(i + 99).uniform(4, 14)) for i in range(26)])
    return doc(s + glow(384, 0, 400, 180, "#e8ffff", .6) + rays + hills(980, 26, "#e8c890", 2) + kelp + coral + fan
               + fish(560, 300, 1.2, "#ff8a1a", "#fff") + fish(210, 440, .8, "#3a8aff", "#ffd23a", -1) + fish(640, 520, .6, "#ffd23a", "#3a8aff") + bubbles, d)


def carnival():
    d, s = sky((0, "#0a0418"), (.6, "#2a0e4a"), (1, "#4a1a6a"))
    cx, cy, r = 190, 470, 160
    wheel = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#5a2a8a" stroke-width="10"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#b04aff" stroke-width="3" filter="url(#b8)"/>'
             + "".join(f'<path d="M{cx} {cy} L{cx + r * math.cos(a):.0f} {cy + r * math.sin(a):.0f}" stroke="#4a1a7a" stroke-width="5"/>'
                       f'<rect x="{cx + r * math.cos(a) - 14:.0f}" y="{cy + r * math.sin(a):.0f}" width="28" height="22" rx="5" fill="#3a1060"/>'
                       f'<circle cx="{cx + r * math.cos(a):.0f}" cy="{cy + r * math.sin(a):.0f}" r="5" fill="#7aff4a"/>' for a in (i * math.pi / 6 for i in range(12)))
             + f'<path d="M{cx - 90} 780 L{cx} {cy} L{cx + 90} 780" stroke="#3a1060" stroke-width="14" fill="none"/>')
    tent = lambda x, w, h, a, b: (f'<path d="M{x - w} 820 L{x} {820 - h} L{x + w} 820 Z" fill="{a}"/>'
                                  + "".join(f'<path d="M{x} {820 - h} L{x - w + i * w / 2} 820 L{x - w + (i + .5) * w / 2} 820 Z" fill="{b}"/>' for i in range(4))
                                  + f'<path d="M{x - w} 820 L{x} {820 - h} L{x + w} 820" stroke="#7aff4a" stroke-width="3" fill="none" filter="url(#b8)"/>')
    lights = "".join(f'<circle cx="{x}" cy="{560 + 40 * math.sin(x / 120)}" r="6" fill="{["#ff4a6a", "#ffd23a", "#7aff4a", "#3ad8ff"][i % 4]}"/>'
                     f'<circle cx="{x}" cy="{560 + 40 * math.sin(x / 120)}" r="14" fill="{["#ff4a6a", "#ffd23a", "#7aff4a", "#3ad8ff"][i % 4]}" opacity=".35" filter="url(#b8)"/>' for i, x in enumerate(range(330, 770, 36)))
    ghost = ('<g transform="translate(610 360)"><path d="M-50 70 V-10 C-50 -50 -24 -70 0 -70 C24 -70 50 -50 50 -10 V70 L36 56 L22 70 L8 56 L-6 70 L-20 56 L-34 70 Z" fill="#f4f0ff" opacity=".95"/>'
             '<ellipse cx="-16" cy="-14" rx="8" ry="12" fill="#1a1030"/><ellipse cx="16" cy="-14" rx="8" ry="12" fill="#1a1030"/><circle cx="-14" cy="-18" r="3" fill="#fff"/><circle cx="18" cy="-18" r="3" fill="#fff"/>'
             '<ellipse cx="-30" cy="8" rx="8" ry="5" fill="#ff8ac0" opacity=".6"/><ellipse cx="30" cy="8" rx="8" ry="5" fill="#ff8ac0" opacity=".6"/><path d="M-8 14 Q0 22 8 14" stroke="#1a1030" stroke-width="3" fill="none"/></g>')
    return doc(s + dots(9, 60, 0, 0, W, 500, .8, 2, "#fff", (.4, 1)) + '<circle cx="600" cy="140" r="56" fill="#f4ecc8"/>' + glow(600, 140, 120, 120, "#d8c8ff", .5)
               + ridge(3, 760, 40, "#1a0830", 8) + wheel + tent(470, 120, 190, "#4a1a6a", "#7a2a9a") + tent(660, 90, 150, "#3a1060", "#6a1a8a")
               + '<path d="M330 560 Q550 620 768 540" stroke="#2a1040" stroke-width="2" fill="none"/>' + lights + ghost
               + glow(384, 980, 500, 90, "#c8b0ff", .5) + hills(960, 16, "#0e0420", 3), d)


def crystal_cluster(x, y, s, col, lt):
    out = ""
    for dx, h, w, a in ((0, 220, 50, 0), (-50, 150, 40, -18), (50, 170, 42, 16), (-90, 90, 30, -30), (90, 110, 30, 28)):
        pts = f"{-w / 2},0 {w / 2},0 {w * .35},{-h} 0,{-h - w * .6} {-w * .35},{-h}"
        out += (f'<g transform="translate({x + dx * s} {y}) rotate({a}) scale({s})"><polygon points="{pts}" fill="{col}"/>'
                f'<polygon points="0,0 {w / 2},0 {w * .35},{-h} 0,{-h - w * .6}" fill="#000" opacity=".25"/>'
                f'<polygon points="{-w * .35},{-h} 0,{-h - w * .6} {-w * .1},{-h * .2}" fill="{lt}" opacity=".7"/></g>')
    return glow(x, y - 100 * s, 140 * s, 140 * s, col, .5, "b40") + out


def crystal():
    d, s = sky((0, "#06030f"), (.55, "#1e0e3a"), (1, "#3a1a6a"))
    walls = ('<path d="M0 0 H200 Q120 200 160 400 Q80 600 140 800 Q60 900 0 1024 Z" fill="#0c061a"/>'
             '<path d="M768 0 H560 Q650 220 600 420 Q700 620 630 820 Q720 920 768 1024 Z" fill="#0c061a"/>')
    return doc(s + glow(384, 420, 280, 260, "#7a3aff", .45) + walls + crystal_cluster(150, 520, .8, "#3a9aff", "#c8e8ff")
               + crystal_cluster(640, 600, .9, "#b04aff", "#f0d8ff") + crystal_cluster(384, 980, 1.3, "#7a5aff", "#e0d8ff")
               + crystal_cluster(80, 960, .9, "#3ac8ff", "#d8faff") + crystal_cluster(700, 990, .8, "#e04ad0", "#ffd8f4")
               + dots(11, 70, 0, 0, W, H, 1, 3, "#e8d8ff", (.4, 1), True), d)


def palm(x, y, s, lean=1):
    trunk = f'<path d="M{x} {y} Q{x + 20 * lean * s} {y - 120 * s} {x + 50 * lean * s} {y - 220 * s}" stroke="#8a5a2a" stroke-width="{16 * s}" fill="none" stroke-linecap="round"/>'
    tx, ty = x + 50 * lean * s, y - 220 * s
    fronds = "".join(f'<path d="M{tx} {ty} Q{tx + 70 * math.cos(a) * s} {ty + 70 * math.sin(a) * s - 30 * s} {tx + 120 * math.cos(a) * s} {ty + 120 * math.sin(a) * s + 20 * s}" stroke="#2a9a3a" stroke-width="{14 * s}" fill="none" stroke-linecap="round"/>'
                     for a in (-2.8, -2.2, -1.6, -1.0, -.4, .2))
    return trunk + fronds + f'<circle cx="{tx}" cy="{ty + 6 * s}" r="{8 * s}" fill="#6a4020"/>'


def desert():
    d, s = sky((0, "#ff9a3a"), (.4, "#ffc86a"), (1, "#ffe8b8"))
    dome = '<path d="M520 640 V560 Q560 500 600 560 V640 Z M600 640 V590 H680 V640 Z" fill="#c88a4a" opacity=".8"/><circle cx="560" cy="520" r="6" fill="#c88a4a" opacity=".8"/>'
    return doc(s + '<circle cx="384" cy="300" r="120" fill="#fff4c0"/>' + glow(384, 300, 260, 220, "#fff0a0", .8)
               + hills(600, 40, "#e8a050", 1.5, 0, .7) + dome + hills(680, 34, "#f0b860", 2) + '<ellipse cx="300" cy="760" rx="200" ry="50" fill="#1fc8c0"/><ellipse cx="300" cy="750" rx="170" ry="30" fill="#7ff0e8" opacity=".6"/>'
               + palm(150, 770, 1.1) + palm(450, 760, .9, -1) + hills(860, 30, "#f6c878", 2.5, 1)
               + "".join(f'<path d="M0 {y} Q192 {y - 14} 384 {y} T768 {y}" stroke="#e0a050" stroke-width="3" fill="none" opacity=".6"/>' for y in (910, 950, 990))
               + '<path d="M650 900 V820 A12 12 0 0 1 674 820 V900 Z M650 860 H634 V840 A7 7 0 0 1 648 840 Z" fill="#3aa84a"/>', d)


def gear_path(cx, cy, r, teeth):
    pts = []
    for i in range(teeth * 4):
        a = i / (teeth * 4) * 2 * math.pi
        rr = r + (r * .16 if i % 4 in (1, 2) else 0)
        pts.append(f"{cx + rr * math.cos(a):.0f},{cy + rr * math.sin(a):.0f}")
    return " ".join(pts)


def steampunk():
    d, s = sky((0, "#1a0e06"), (.55, "#4a2a12"), (1, "#8a5a2a"))
    defs = d + '<linearGradient id="br" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe0a0"/><stop offset=".5" stop-color="#c88a3a"/><stop offset="1" stop-color="#5a3410"/></linearGradient>'
    stacks = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{H}" fill="#2a1a0c"/>' for x, y, w in ((60, 260, 60), (180, 340, 40), (560, 220, 70), (680, 320, 44)))
    steam = "".join(glow(x + 25, y - 40, 60, 50, "#f0e0d0", .5, "b20") for x, y in ((60, 260), (560, 220)))
    gears = "".join(f'<polygon points="{gear_path(x, y, r, t)}" fill="url(#br)" stroke="#3a2008" stroke-width="4"/><circle cx="{x}" cy="{y}" r="{r * .55}" fill="none" stroke="#5a3410" stroke-width="{r * .12}"/>'
                    f'<circle cx="{x}" cy="{y}" r="{r * .2}" fill="#3a2008"/>' for x, y, r, t in ((120, 620, 120, 12), (300, 760, 70, 9), (650, 680, 140, 14), (520, 900, 60, 8)))
    pipes = ('<path d="M0 480 H260 Q300 480 300 520 V1024" stroke="#5a3410" stroke-width="40" fill="none"/><path d="M0 480 H260 Q300 480 300 520 V1024" stroke="url(#br)" stroke-width="30" fill="none"/>'
             '<path d="M768 420 H520 Q480 420 480 460 V560" stroke="url(#br)" stroke-width="26" fill="none"/>'
             + "".join(f'<rect x="{x - 22}" y="{y - 22}" width="44" height="44" rx="8" fill="#a06a2a" stroke="#3a2008" stroke-width="3"/>' for x, y in ((200, 480), (300, 640), (560, 420))))
    lamps = "".join(glow(x, y, 50, 50, "#ffc86a", .7, "b20") + f'<circle cx="{x}" cy="{y}" r="10" fill="#fff2c0"/>' for x, y in ((420, 380), (720, 520), (60, 760)))
    return doc(s + glow(384, 600, 400, 300, "#c86a2a", .35) + stacks + steam + pipes + gears + lamps + hills(990, 14, "#1a0e06", 3), defs)


def nebula():
    d, s = sky((0, "#05041a"), (1, "#120a30"))
    clouds = glow(250, 300, 300, 160, "#b04aff", .55) + glow(560, 520, 280, 200, "#ff4ab8", .45) + glow(300, 760, 300, 160, "#3a6aff", .45)
    arms = "".join(f'<path d="M520 520 ' + " ".join(f'L{520 + (6 + t * 2.2) * math.cos(t / 12 + k * math.pi):.0f} {520 + (6 + t * 2.2) * .55 * math.sin(t / 12 + k * math.pi):.0f}' for t in range(0, 90, 3))
                   + f'" stroke="{c}" stroke-width="{w}" fill="none" opacity=".8" filter="url(#b8)"/>' for k in (0, 1) for c, w in (("#ffb0f0", 18), ("#fff", 5)))
    planet = ('<circle cx="170" cy="190" r="90" fill="#ff8a3a"/><path d="M100 160 Q170 140 250 170 M90 210 Q170 190 258 220" stroke="#ffc88a" stroke-width="10" fill="none" opacity=".7"/>'
              '<circle cx="200" cy="215" r="90" fill="#000" opacity=".25" clip-path="url(#pc)"/><ellipse cx="170" cy="190" rx="150" ry="30" fill="none" stroke="#ffd8a0" stroke-width="8" transform="rotate(-15 170 190)"/>')
    return doc(s + clouds + dots(13, 160, 0, 0, W, H, .6, 2.2, "#fff", (.4, 1)) + dots(14, 14, 0, 0, W, H, 2, 3, "#fff6c0", (.7, 1), True) + arms
               + glow(520, 520, 40, 24, "#fff", .9, "b8") + planet + '<circle cx="660" cy="200" r="34" fill="#7a5aff"/><circle cx="650" cy="190" r="34" fill="#a88aff" opacity=".6"/>'
               + "".join(f'<path d="M{x} {y} m-{r} 0 a{r} {r * .85} 0 1 0 {2 * r} 0 a{r} {r * .85} 0 1 0 -{2 * r} 0" fill="#5a5470"/><circle cx="{x - r * .3}" cy="{y - r * .2}" r="{r * .25}" fill="#3a3450"/>'
                         for x, y, r in ((90, 900, 40), (680, 930, 52), (560, 980, 24))), d + '<clipPath id="pc"><circle cx="170" cy="190" r="90"/></clipPath>')


SCENES = {"volcano": volcano, "sky": sky_islands, "forest": forest, "tundra": tundra, "reef": reef, "carnival": carnival,
          "crystal": crystal, "desert": desert, "steampunk": steampunk, "nebula": nebula}

if __name__ == "__main__":
    paths = {}
    for tid, fn in SCENES.items():
        f = f"scn_{tid}_card.svg"
        dd = os.path.join(OUT, folder_for(f)); os.makedirs(dd, exist_ok=True)
        open(os.path.join(dd, f), "w").write(fn())
        paths[tid] = f"{folder_for(f)}/{f}"
    lv = os.path.join(OUT, "data", "levels.json")
    data = json.load(open(lv))
    for tid, p in paths.items(): data[tid]["scene"] = p   # the painted-art drop-in slot
    json.dump(data, open(lv, "w"), indent=1)
    print(f"wrote {len(paths)} world scenes, recorded in data/levels.json")
