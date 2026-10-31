# Seasonal collection (soft-clay, matches all other sets): 4 seasons × 2 phenomenon sets × 4 colours = 32 pieces,
# plus a mesh-aura board and a glass emblem per season. Run: python3 make_seasons.py
import json, math, os
from make_assets import GLYPHS
from make_collection import SLOTS, polar, rounded_poly, sym
from layout import folder_for

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")


def doc(body, w=128, h=128, pad=10):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w + 2 * pad} {h + 2 * pad}" '
            f'width="{w + 2 * pad}" height="{h + 2 * pad}">{body}</svg>')


def capsule(cx, cy, length, w, ang):
    """Rounded bar (for snowflake arms) as a path; same winding so subpaths union."""
    a = math.radians(ang); dx, dy = math.cos(a) * length / 2, math.sin(a) * length / 2
    nx, ny = -math.sin(a) * w / 2, math.cos(a) * w / 2
    p = [(cx - dx + nx, cy - dy + ny), (cx + dx + nx, cy + dy + ny), (cx + dx - nx, cy + dy - ny), (cx - dx - nx, cy - dy - ny)]
    r = w / 2
    return (f"M{p[0][0]:.1f} {p[0][1]:.1f} L{p[1][0]:.1f} {p[1][1]:.1f} A{r} {r} 0 0 0 {p[2][0]:.1f} {p[2][1]:.1f} "
            f"L{p[3][0]:.1f} {p[3][1]:.1f} A{r} {r} 0 0 0 {p[0][0]:.1f} {p[0][1]:.1f} Z")


# ---- shapes: same soft-clay renderer as every other collection ------------------------------------
from make_assets import layered, BALL

TULIP = "M18 50 L40 64 L64 24 L88 64 L110 50 C114 92 96 120 64 120 C32 120 14 92 18 50 Z"
DROP = "M64 6 C84 36 108 60 108 84 A44 38 0 0 1 20 84 C20 60 44 36 64 6 Z"
SUN = polar(lambda t: 46 + 13 * max(0.0, math.cos(8 * t)) ** 2)
SHELL = ("M64 118 L52 106 C20 96 8 68 14 44 C24 20 46 10 64 10 C82 10 104 20 114 44 "
         "C120 68 108 96 76 106 Z")
GINKGO = "M64 98 C26 98 4 70 8 34 Q36 20 58 30 L64 42 L70 30 Q92 20 120 34 C124 70 102 98 64 98 Z"
ACORN = "M28 56 H100 C100 94 86 116 64 122 C42 116 28 94 28 56 Z"
FLAKE = polar(lambda t: 32 + 28 * ((math.cos(6 * t + math.pi) + 1) / 2) ** 4, 240)  # 6 arms, one pointing up
MITTEN = ("M44 122 H94 Q102 122 102 114 V56 C102 30 88 14 68 14 C50 14 40 28 40 44 V60 L30 50 "
          "C20 40 6 50 12 64 L40 94 V114 Q40 122 44 122 Z")


def tulip(c, g):
    l, m, d = c
    extra = (f'<path d="M40 64 Q64 86 88 64" stroke="{d}" stroke-width="3" fill="none" opacity=".35"/>'
             '<path d="M20 112 Q30 92 50 100 Q36 104 28 118 Z M108 112 Q98 92 78 100 Q92 104 100 118 Z" fill="#4fc23a"/>')
    return layered(TULIP, c, sym(g, .5, 64, 86), extra)


def raindrop(c, g):
    extra = ('<path d="M42 102 A22 18 0 0 1 86 102" stroke="#ff5a8a" stroke-width="4" fill="none" stroke-linecap="round"/>'
             '<path d="M48 104 A16 12 0 0 1 80 104" stroke="#ffd21f" stroke-width="4" fill="none" stroke-linecap="round"/>'
             '<path d="M54 106 A10 7 0 0 1 74 106" stroke="#2fd4ff" stroke-width="4" fill="none" stroke-linecap="round"/>'
             '<path d="M50 34 Q42 52 40 66" stroke="#fff" stroke-width="6" stroke-linecap="round" fill="none" opacity=".6"/>')
    return layered(DROP, c, sym(g, .55, 64, 72), extra)


def sun(c, g):
    l, m, d = c
    return layered(SUN, c, sym(g, .55), f'<circle cx="64" cy="64" r="38" fill="{l}" opacity=".45"/>'
                                         '<circle cx="64" cy="64" r="38" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>')


def shell(c, g):
    l, m, d = c
    ridges = "".join(f'<path d="M64 110 L{64 + 58 * math.cos(math.radians(a)):.0f} {110 - 96 * math.sin(math.radians(a)):.0f}" '
                     f'stroke="{d}" stroke-width="3" opacity=".3"/>' for a in (40, 60, 80, 100, 120, 140))
    hinge = f'<rect x="48" y="104" width="32" height="16" rx="7" fill="{m}"/><rect x="52" y="106" width="24" height="4" rx="2" fill="#fff" opacity=".4"/>'
    return layered(SHELL, c, sym(g, .45, 64, 58), ridges + hinge)


def ginkgo(c, g):
    l, m, d = c
    veins = "".join(f'<path d="M64 96 L{64 + 60 * math.cos(math.radians(a)):.0f} {96 - 60 * math.sin(math.radians(a)):.0f}" '
                    f'stroke="{d}" stroke-width="2" opacity=".3"/>' for a in range(24, 170, 14))
    stem = f'<path d="M64 98 Q62 112 70 124" stroke="#8a5a2a" stroke-width="6" stroke-linecap="round" fill="none"/>'
    return layered(GINKGO, c, sym(g, .45, 64, 62), veins + stem)


def acorn(c, g):
    cap = ('<path d="M18 60 C18 34 40 22 64 22 C88 22 110 34 110 60 Q64 70 18 60 Z" fill="#8a5a2a"/>'
           '<path d="M22 56 C24 36 42 28 64 28 C86 28 104 36 106 56" fill="none" stroke="#b07a3e" stroke-width="3"/>'
           + "".join(f'<path d="M{x} 34 L{x + 10} 58 M{x + 10} 34 L{x} 58" stroke="#6b4018" stroke-width="2" opacity=".6"/>' for x in (32, 50, 68, 86)) +
           '<path d="M62 22 Q60 8 72 4" stroke="#6b4018" stroke-width="6" stroke-linecap="round" fill="none"/>'
           '<ellipse cx="44" cy="36" rx="12" ry="5" fill="#fff" opacity=".25" transform="rotate(-15 44 36)"/>')
    return layered(ACORN, c, sym(g, .45, 64, 90), cap).replace('<path d="M96 22 l3 8', '<path d="M96 70 l3 8', 1)


def snowstar(c, g):
    l, m, d = c
    tips = "".join(f'<circle cx="{64 + 50 * math.cos(a):.1f}" cy="{64 + 50 * math.sin(a):.1f}" r="4.5" fill="#fff" opacity=".7"/>'
                   for a in (i * math.pi / 3 - math.pi / 2 for i in range(6)))
    return layered(FLAKE, c, sym(g, .4), f'<circle cx="64" cy="64" r="20" fill="{l}" opacity=".5"/>' + tips)


def mitten(c, g):
    l, m, d = c
    cuff = ('<rect x="36" y="100" width="70" height="24" rx="12" fill="#fff"/>'
            + "".join(f'<circle cx="{x}" cy="112" r="3" fill="{l}"/>' for x in (50, 62, 74, 86)) +
            f'<path d="M42 74 L52 66 L62 74 L72 66 L82 74 L92 66 L100 74" fill="none" stroke="{l}" stroke-width="5" stroke-linejoin="round"/>')
    return layered(MITTEN, c, sym(g, .42, 72, 46), cuff)


# season: months, saturated palette (slot order = drop, heart, leaf, star families), accent, two sets
SEASONS = {
    "spring": {"months": [3, 4, 5], "accent": "#ff4fa8", "bg": ("#ffb0dc", "#9ff0ff", "#c8ff9a", "#2a2440"),
               "cols": [("#9ff0ff", "#22b8e8", "#0b5a85"), ("#ffb0dc", "#ff4fa8", "#8a0f52"),
                        ("#c8ff9a", "#5cd636", "#1f6a12"), ("#fff09a", "#ffcc1f", "#8a5a00")],
               "sets": [("tulip", "Tulip Buds", "First blooms of the year", tulip),
                        ("raindrop", "Rainbow Drops", "Spring showers, rainbow inside", raindrop)]},
    "summer": {"months": [6, 7, 8], "accent": "#ffb000", "bg": ("#ffb59a", "#8ffff0", "#ffe680", "#10283a"),
               "cols": [("#8ffff0", "#00d0c0", "#005a5a"), ("#ffb59a", "#ff5a3a", "#8a1a05"),
                        ("#e0ff7a", "#9ae000", "#3a5a00"), ("#ffe680", "#ffb000", "#8a4000")],
               "sets": [("sun", "Sunny Days", "Bright suns with soft rays", sun),
                        ("shell", "Seashells", "Ridged shells from the shore", shell)]},
    "autumn": {"months": [9, 10, 11], "accent": "#ff9500", "bg": ("#ff9a8a", "#ffd27a", "#a8d0ff", "#1e1626"),
               "cols": [("#a8d0ff", "#3a7ae8", "#123a8a"), ("#ff9a8a", "#e83a2a", "#7a0e05"),
                        ("#d8f07a", "#8ac020", "#3a5a05"), ("#ffd27a", "#ff9500", "#7a3a00")],
               "sets": [("ginkgo", "Ginkgo Leaves", "Fan leaves on the wind", ginkgo),
                        ("acorn", "Acorns", "Little nuts in woolly caps", acorn)]},
    "winter": {"months": [12, 1, 2], "accent": "#5cc8ff", "bg": ("#d8f8ff", "#ffb0d0", "#a8ffd8", "#0b1030"),
               "cols": [("#d8f8ff", "#5cc8ff", "#0f4a8a"), ("#ffb0d0", "#ff3d8a", "#7a0a3a"),
                        ("#a8ffd8", "#20c890", "#05603e"), ("#fff0a0", "#ffc83a", "#8a5a00")],
               "sets": [("snowstar", "Snow Stars", "Six-point flakes", snowstar),
                        ("mitten", "Cozy Mittens", "Knitted, with fluffy cuffs", mitten)]},
}


def board(bg):
    """Mesh aura via soft radial gradients (huge blurs are unreliable at full-screen sizes)."""
    a, b, c, base = bg
    g = "".join(f'<radialGradient id="g{i}"><stop offset="0" stop-color="{col}" stop-opacity=".8"/>'
                f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>' for i, col in enumerate((a, b, c)))
    return doc(f'<defs>{g}<filter id="gr"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2"/>'
               '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .5 0"/></filter>'
               '<clipPath id="k"><rect width="1024" height="1024" rx="88"/></clipPath></defs>'
               f'<g clip-path="url(#k)"><rect width="1024" height="1024" fill="{base}"/>'
               '<circle cx="200" cy="180" r="620" fill="url(#g0)"/><circle cx="900" cy="300" r="560" fill="url(#g1)"/>'
               '<circle cx="520" cy="980" r="640" fill="url(#g2)"/>'
               f'<rect width="1024" height="1024" fill="{base}" opacity=".4"/>'
               '<rect width="1024" height="1024" filter="url(#gr)" opacity=".06"/></g>'
               '<rect x="1.5" y="1.5" width="1021" height="1021" rx="87" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="3"/>',
               1024, 1024, 0)


def emblem(season, cols, accent):
    icons = {
        "spring": "".join(f'<circle cx="{64 + 18 * math.cos(a):.1f}" cy="{64 + 18 * math.sin(a):.1f}" r="13"/>'
                          for a in (i * 2 * math.pi / 5 - math.pi / 2 for i in range(5))) + '<circle cx="64" cy="64" r="10" fill-opacity=".6"/>',
        "summer": '<circle cx="64" cy="64" r="20"/>' + "".join(
            f'<path d="{capsule(64 + 34 * math.cos(math.radians(a)), 64 + 34 * math.sin(math.radians(a)), 16, 7, a)}"/>' for a in range(0, 360, 45)),
        "autumn": GLYPHS["lime"],
        "winter": "".join(f'<path d="{capsule(64, 64, 72, 9, a)}"/>' for a in (90, 30, -30)),
    }
    return layered(BALL, cols, icons[season])


if __name__ == "__main__":
    meta, n = [], 0
    for sid, S in SEASONS.items():
        sets = []
        for key, name, tag, fn in S["sets"]:
            pieces = []
            for i, cols in enumerate(S["cols"]):
                f = f"sea_{sid}_{key}_{i}.svg"
                os.makedirs(os.path.join(OUT, folder_for(f)), exist_ok=True)
                open(os.path.join(OUT, folder_for(f), f), "w").write(fn(cols, GLYPHS[SLOTS[i]])); n += 1
                pieces.append({"file": f, "color": cols[1], "light": cols[0]})
            sets.append({"id": key, "name": name, "tagline": tag, "pieces": pieces})
        for f, data in ((f"sea_{sid}_board.svg", board(S["bg"])), (f"sea_{sid}_emblem.svg", emblem(sid, S["cols"][3 if sid in ("summer", "autumn") else 1], S["accent"]))):
            open(os.path.join(OUT, folder_for(f), f), "w").write(data); n += 1
        meta.append({"id": sid, "months": S["months"], "accent": S["accent"], "bg": S["bg"],
                     "board": f"sea_{sid}_board.svg", "emblem": f"sea_{sid}_emblem.svg", "sets": sets})
    json.dump(meta, open(os.path.join(OUT, "seasons", "seasons.json"), "w"), indent=1)
    print(f"wrote {n} season assets + seasons.json")
