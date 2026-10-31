# Sweet Shop collection: 12 original sweet designs × 4 colours = 48 pieces, nested by category/design:
#   assets/sweets/<category>/<design>/sw_<category>_<design>_<i>.svg   Run: python3 make_sweets.py
import json, math, os
from make_assets import layered, BALL, GLYPHS
from make_collection import COLS, SLOTS, sym
from layout import folder_for

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
CHOC, CHOC_D, DOUGH = "#6b3a1f", "#3e1f0e", "#e8b070"


def circ(cx, cy, r, ccw=False):
    """Circle as a path; ccw=True cuts a hole when combined with a clockwise outer path."""
    s = 0 if ccw else 1
    return f"M{cx} {cy - r} A{r} {r} 0 1 {s} {cx} {cy + r} A{r} {r} 0 1 {s} {cx} {cy - r} Z"


def spiral(cx, cy, r, turns=2.6, n=90):
    pts = [(cx + r * t / n * math.cos(t / n * turns * 2 * math.pi), cy + r * t / n * math.sin(t / n * turns * 2 * math.pi)) for t in range(n + 1)]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def sprinkles(cols, spots):
    return "".join(f'<rect x="{x - 5}" y="{y - 1.8}" width="10" height="3.6" rx="1.8" fill="{cols[i % len(cols)]}" transform="rotate({a} {x} {y})"/>'
                   for i, (x, y, a) in enumerate(spots))


FUN = ["#fff", "#ffe08a", "#7ff3ff", "#ff9ee8", "#d6ff8a"]

# ---- candies --------------------------------------------------------------------------------------
def lollipop(c, g):
    stick = '<rect x="59" y="92" width="10" height="34" rx="5" fill="#f4f1ec"/><rect x="61" y="94" width="3" height="28" rx="1.5" fill="#fff"/>'
    swirl = f'<path d="{spiral(64, 52, 38)}" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".55"/>'
    return layered(circ(64, 52, 42), c, sym(g, .3, 64, 52), swirl + stick)


WRAPPED = (circ(64, 64, 30) + " M38 64 L6 40 Q2 64 6 88 Z M90 64 L122 40 Q126 64 122 88 Z")


def wrapped(c, g):
    l, m, d = c
    extra = (f'<path d="M44 40 L60 92 M64 36 L80 90" stroke="#fff" stroke-width="7" opacity=".35" stroke-linecap="round"/>'
             f'<path d="M12 50 L30 62 M10 64 H30 M12 78 L30 66 M116 50 L98 62 M118 64 H98 M116 78 L98 66" stroke="{d}" stroke-width="2.5" opacity=".4" stroke-linecap="round"/>')
    return layered(WRAPPED, c, sym(g, .4), extra)


def mint(c, g):
    wedges = "".join(f'<path d="M64 64 L{64 + 54 * math.cos(math.radians(a)):.1f} {64 + 54 * math.sin(math.radians(a)):.1f} '
                     f'A54 54 0 0 1 {64 + 54 * math.cos(math.radians(a + 22)):.1f} {64 + 54 * math.sin(math.radians(a + 22)):.1f} Z" fill="#fff" opacity=".6"/>'
                     for a in range(0, 360, 45))
    return layered(circ(64, 64, 56), c, sym(g, .42), wedges + '<circle cx="64" cy="64" r="22" fill="#fff" opacity=".35"/>')


JELLYBEAN = "M30 30 C50 10 98 14 112 44 C124 72 106 110 72 112 C52 114 54 90 36 92 C10 94 4 56 30 30 Z"


def jellybean(c, g):
    return layered(JELLYBEAN, c, sym(g, .45, 70, 62),
                   '<path d="M38 40 Q60 24 92 32" stroke="#fff" stroke-width="7" stroke-linecap="round" fill="none" opacity=".5"/>')


# ---- bakery ---------------------------------------------------------------------------------------
FROST = "M18 64 C10 46 28 32 40 38 C42 20 60 12 72 20 C86 12 106 24 100 40 C116 42 118 62 108 66 Z"
WRAP = "M24 64 H104 L94 118 Q93 122 88 122 H40 Q35 122 34 118 Z"


def cupcake(c, g):
    l, m, d = c
    pleats = "".join(f'<path d="M{x} 66 L{x + (64 - x) * .18:.0f} 120" stroke="{d}" stroke-width="3" opacity=".35"/>' for x in range(34, 100, 10))
    wrap = f'<path d="{WRAP}" fill="{d}" opacity=".35"/>' + pleats
    icing = ('<path d="M30 54 Q50 44 64 50 Q80 56 98 48" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".55"/>'
             + sprinkles(FUN, [(40, 44, 30), (58, 30, -20), (78, 34, 60), (90, 50, -40), (50, 58, 80)]) +
             '<circle cx="66" cy="12" r="10" fill="#e8203a"/><circle cx="62" cy="9" r="3" fill="#fff" opacity=".6"/>'
             '<path d="M66 4 Q70 -4 78 -2" stroke="#4f7a2a" stroke-width="3" fill="none" stroke-linecap="round"/>')
    return layered(FROST + " " + WRAP, c, sym(g, .36, 64, 92), wrap + icing)


def donut(c, g):
    l, m, d = c
    dough = f'<path d="M10 72 A54 54 0 0 0 118 72" stroke="{DOUGH}" stroke-width="10" fill="none" stroke-linecap="round"/>'
    hole = '<circle cx="64" cy="64" r="16" fill="none" stroke="#000" stroke-opacity=".18" stroke-width="6"/>'
    return layered(circ(64, 64, 56) + " " + circ(64, 64, 16, ccw=True), c, "",
                   dough + hole + sprinkles(FUN, [(36, 36, 20), (64, 22, -30), (92, 34, 50), (100, 62, -10), (30, 70, 70), (86, 92, 30), (48, 96, -50)]) +
                   f'<g fill="#fff" opacity=".85">{sym(g, .26, 64, 34)}</g>')


SHELL_TOP = "M14 50 Q14 18 64 18 Q114 18 114 50 Q114 58 106 58 H22 Q14 58 14 50 Z"
SHELL_BOT = "M14 82 Q14 74 22 74 H106 Q114 74 114 82 Q114 110 64 110 Q14 110 14 82 Z"


def macaron(c, g):
    l, m, d = c
    cream = '<rect x="20" y="54" width="88" height="24" rx="12" fill="#fff8f0"/><rect x="24" y="58" width="80" height="5" rx="2.5" fill="#fff"/>'
    feet = "".join(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{l}" opacity=".8"/>' for y in (57, 75) for x in range(22, 110, 7))
    return layered(SHELL_TOP + " " + SHELL_BOT, c, sym(g, .36, 64, 38), cream + feet)


# ---- chocolates -----------------------------------------------------------------------------------
DOME = "M14 94 C14 48 34 20 64 20 C94 20 114 48 114 94 Q114 104 104 104 H24 Q14 104 14 94 Z"


def bonbon(c, g):
    drizzle = (f'<path d="M20 58 L34 50 L48 60 L62 50 L76 60 L90 50 L104 60 L112 54" stroke="{CHOC}" stroke-width="6" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
               f'<rect x="10" y="94" width="108" height="20" rx="10" fill="{CHOC}"/><rect x="16" y="97" width="96" height="4" rx="2" fill="#a0603a"/>'
               f'<path d="M20 114 Q64 122 108 114" stroke="{CHOC_D}" stroke-width="3" fill="none"/>')
    return layered(DOME, c, sym(g, .4, 64, 76), drizzle)


# ---- gummies --------------------------------------------------------------------------------------
BEAR = " ".join([circ(64, 40, 26), circ(42, 20, 10), circ(86, 20, 10), "M34 76 C34 54 94 54 94 76 C98 100 90 118 64 118 C38 118 30 100 34 76 Z",
                 circ(30, 76, 11), circ(98, 76, 11), circ(42, 114, 12), circ(86, 114, 12)])


def gummybear(c, g):
    l, m, d = c
    face = (f'<circle cx="54" cy="36" r="4" fill="{d}"/><circle cx="74" cy="36" r="4" fill="{d}"/>'
            f'<ellipse cx="64" cy="48" rx="9" ry="6" fill="{l}" opacity=".7"/><circle cx="64" cy="46" r="3" fill="{d}"/>'
            f'<ellipse cx="64" cy="90" rx="18" ry="20" fill="{l}" opacity=".45"/>')
    return layered(BEAR, c, sym(g, .3, 64, 90), face)


GUMDROP = "M64 12 C92 12 112 60 114 96 Q114 112 98 112 H30 Q14 112 14 96 C16 60 36 12 64 12 Z"


def gumdrop(c, g):
    sugar = "".join(f'<rect x="{x}" y="{y}" width="4" height="4" fill="#fff" opacity=".7" transform="rotate(45 {x + 2} {y + 2})"/>'
                    for x, y in ((40, 40), (70, 30), (88, 58), (30, 74), (56, 90), (94, 92), (48, 60), (78, 76), (64, 50), (36, 100)))
    return layered(GUMDROP, c, sym(g, .42, 64, 72), sugar)


# ---- fruits ---------------------------------------------------------------------------------------
def citrus(c, g):
    l, m, d = c
    segs = "".join(f'<path d="M64 64 L{64 + 42 * math.cos(math.radians(a)):.1f} {64 + 42 * math.sin(math.radians(a)):.1f}" stroke="#fff" stroke-width="3.5" opacity=".8"/>'
                   for a in range(0, 360, 45))
    pulp = f'<circle cx="64" cy="64" r="44" fill="#fff" opacity=".85"/><circle cx="64" cy="64" r="41" fill="{l}"/>'
    return layered(circ(64, 64, 56), c, sym(g, .3), pulp + segs + '<circle cx="64" cy="64" r="7" fill="#fff" opacity=".8"/>')


CHERRY = circ(40, 86, 30) + " " + circ(90, 80, 30)


def cherry(c, g):
    stems = ('<path d="M42 58 Q50 26 78 10 M88 52 Q86 30 78 10" stroke="#4f7a2a" stroke-width="5" fill="none" stroke-linecap="round"/>'
             '<path d="M78 10 Q100 0 112 14 Q96 20 78 10 Z" fill="#6fbf3a"/>')
    return layered(CHERRY, c, sym(g, .3, 40, 88), stems).replace('<path d="M96 22 l3 8', '<path d="M96 62 l3 8', 1)


# category → design → (display name, renderer)
SWEETS = {
    "candies": {"lollipop": ("Swirl Pops", lollipop), "wrapped": ("Twist Wraps", wrapped),
                "mint": ("Pinwheel Mints", mint), "jellybean": ("Jelly Beans", jellybean)},
    "bakery": {"cupcake": ("Cherry Cupcakes", cupcake), "donut": ("Sprinkle Donuts", donut), "macaron": ("Macarons", macaron)},
    "chocolates": {"bonbon": ("Drizzle Bonbons", bonbon)},
    "gummies": {"gummybear": ("Gummy Bears", gummybear), "gumdrop": ("Sugar Gumdrops", gumdrop)},
    "fruits": {"citrus": ("Citrus Slices", citrus), "cherry": ("Twin Cherries", cherry)},
}

if __name__ == "__main__":
    meta, n = {}, 0
    for cat, designs in SWEETS.items():
        meta[cat] = []
        for did, (name, fn) in designs.items():
            files = []
            for i, cols in enumerate(COLS):
                f = f"sw_{cat}_{did}_{i}.svg"
                d = os.path.join(OUT, folder_for(f)); os.makedirs(d, exist_ok=True)
                open(os.path.join(d, f), "w").write(fn(cols, GLYPHS[SLOTS[i]])); n += 1
                files.append(f"{folder_for(f)}/{f}")
            meta[cat].append({"id": did, "name": name, "pieces": files})
    json.dump(meta, open(os.path.join(OUT, "sweets", "sweets.json"), "w"), indent=1)
    print(f"wrote {n} sweets in {sum(len(v) for v in SWEETS.values())} design folders + sweets.json")
