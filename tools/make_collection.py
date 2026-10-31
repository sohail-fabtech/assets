# Piece collection: 10 sets × 4 colours = 40 unlockable pieces with rarity. Run: python3 make_collection.py
# Unlock design (ethical): fixed Shard prices, no random drops, set progress always visible, cosmetic only.
import json, math, os
from make_assets import svg, layered, BALL, GLYPHS
from layout import folder_for

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
SLOTS = ["cyan", "magenta", "lime", "amber"]
COLS = [("#7ff3ff", "#14b8d4", "#06576b"), ("#ff9ee8", "#e83fb8", "#6e0f55"),
        ("#d6ff8a", "#7fd420", "#2f5a07"), ("#ffe08a", "#ffa51f", "#7a3d00")]
SPARK = '<path d="M96 22 l3 8 8 3 -8 3 -3 8 -3 -8 -8 -3 8 -3 z" fill="#fff"/>'


def polar(r, n=120, cy=64, sy=1.0):
    """Closed smooth path from a radius function r(theta)."""
    pts = [(64 + r(t) * math.cos(t), cy + r(t) * math.sin(t) * sy) for t in (i / n * 2 * math.pi - math.pi / 2 for i in range(n))]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def rounded_poly(pts, k=.22):
    """Polygon with rounded corners (quadratic at each vertex)."""
    out = []
    for i, (x, y) in enumerate(pts):
        px, py = pts[i - 1]; nx, ny = pts[(i + 1) % len(pts)]
        a = (x + (px - x) * k, y + (py - y) * k); b = (x + (nx - x) * k, y + (ny - y) * k)
        out.append(f"{'M' if i == 0 else 'L'}{a[0]:.1f} {a[1]:.1f} Q{x} {y} {b[0]:.1f} {b[1]:.1f}")
    return " ".join(out) + " Z"


def sym(g, s, cx=64, cy=64):
    return f'<g transform="translate({cx - 64 * s} {cy - 64 * s}) scale({s})">{g}</g>'


def shadow_defs(extra=""):
    return f'<defs><filter id="sh" x="-40%" y="-40%" width="180%" height="190%"><feGaussianBlur stdDeviation="6"/></filter>{extra}</defs>'


# ---- path-based sets reuse the soft-clay renderer -------------------------------------------------
JELLY = ("M64 12 C96 12 116 40 116 72 C116 100 98 116 84 111 C76 108 72 118 64 118 C56 118 52 108 44 111 "
         "C30 116 12 100 12 72 C12 40 32 12 64 12 Z")
BLOOM = polar(lambda t: 30 + 26 * abs(math.cos(3 * t)) ** .6)
STARLET = polar(lambda t: 40 + 18 * ((math.cos(5 * t) + 1) / 2) ** 1.5)
PEBBLE = polar(lambda t: 52 + 4 * math.sin(2 * t) + 3 * math.cos(3 * t), sy=.88, cy=66)
HIVE = rounded_poly([(64 + 58 * math.cos(a), 64 + 58 * math.sin(a)) for a in (i * math.pi / 3 for i in range(6))])


def jelly(c, g):
    l, m, d = c  # extra inner wobble highlight
    return layered(JELLY, c, sym(g, .8, 64, 70), f'<ellipse cx="44" cy="44" rx="10" ry="16" fill="#fff" opacity=".5" transform="rotate(30 44 44)"/>')


def token(c, g):
    l, m, d = c
    edge = (f'<circle cx="64" cy="64" r="44" fill="none" stroke="{d}" stroke-width="3" opacity=".45"/>'
            f'<circle cx="64" cy="64" r="51" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="3 6" opacity=".45"/>')
    return layered(BALL, c, sym(g, .7), edge)


def bloom(c, g):
    l, m, d = c
    return layered(BLOOM, c, sym(g, .6), f'<circle cx="64" cy="64" r="22" fill="{l}" opacity=".35"/>')


def starlet(c, g):
    return layered(STARLET, c, sym(g, .5, 64, 68))


def pebble(c, g):
    l, m, d = c
    specks = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{d}" opacity=".35"/>' for x, y, r in
                     ((36, 80, 3), (90, 86, 2.5), (82, 40, 2), (46, 96, 2), (98, 64, 3), (30, 56, 2)))
    return layered(PEBBLE, c, sym(g, .7, 64, 66), specks)


def hive(c, g):
    l, m, d = c
    inner = rounded_poly([(64 + 34 * math.cos(a), 64 + 34 * math.sin(a)) for a in (i * math.pi / 3 for i in range(6))])
    return layered(HIVE, c, sym(g, .55), f'<path d="{inner}" fill="none" stroke="#fff" stroke-width="3" opacity=".35"/>')


# ---- custom-rendered sets -------------------------------------------------------------------------
def crystal(c, g):
    l, m, d = c
    T, R, B, L, C = (64, 4), (104, 50), (64, 124), (24, 50), (64, 50)
    poly = lambda *p: " ".join(f"{x},{y}" for x, y in p)
    return svg(shadow_defs() +
               f'<polygon points="{poly(T, R, B, L)}" fill="{d}" opacity=".55" filter="url(#sh)" transform="translate(0 8)"/>'
               f'<polygon points="{poly(T, C, L)}" fill="{l}"/><polygon points="{poly(T, R, C)}" fill="{m}"/>'
               f'<polygon points="{poly(L, C, B)}" fill="{m}"/><polygon points="{poly(C, R, B)}" fill="{d}"/>'
               f'<polygon points="{poly(T, R, B, L)}" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width="2" stroke-linejoin="round"/>'
               f'<polygon points="{poly(T, (54, 50), (64, 50))}" fill="#fff" opacity=".45"/>'
               f'<g fill="#fff" opacity=".85">{sym(g, .45, 64, 74)}</g>' + SPARK)


def planet(c, g):
    l, m, d = c
    ring = 'transform="rotate(-18 64 64)"'
    return svg(shadow_defs(f'<radialGradient id="p" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="{l}"/>'
                           f'<stop offset=".55" stop-color="{m}"/><stop offset="1" stop-color="{d}"/></radialGradient>') +
               f'<circle cx="64" cy="74" r="40" fill="{d}" opacity=".5" filter="url(#sh)"/>'
               f'<ellipse cx="64" cy="64" rx="62" ry="16" fill="none" stroke="{l}" stroke-width="7" opacity=".55" {ring}/>'
               f'<circle cx="64" cy="64" r="42" fill="url(#p)"/>'
               f'<path d="M30 70 Q64 60 98 70" stroke="{l}" stroke-width="5" fill="none" opacity=".35"/>'
               f'<g fill="#fff" opacity=".85">{sym(g, .5, 64, 60)}</g>'
               f'<path d="M2 64 A62 16 0 0 0 126 64" fill="none" stroke="{l}" stroke-width="7" stroke-linecap="round" {ring}/>'
               f'<path d="M14 70 A62 16 0 0 0 60 80" fill="none" stroke="#fff" stroke-width="2.5" opacity=".6" {ring}/>'
               '<ellipse cx="48" cy="40" rx="14" ry="7" fill="#fff" opacity=".45" transform="rotate(-30 48 40)"/>')


def critter(c, g):
    l, m, d = c
    face = ('<ellipse cx="46" cy="66" rx="10" ry="12" fill="#fff"/><ellipse cx="82" cy="66" rx="10" ry="12" fill="#fff"/>'
            f'<circle cx="48" cy="69" r="6.5" fill="{d}"/><circle cx="84" cy="69" r="6.5" fill="{d}"/>'
            '<circle cx="45" cy="65" r="2.6" fill="#fff"/><circle cx="81" cy="65" r="2.6" fill="#fff"/>'
            '<ellipse cx="32" cy="84" rx="8" ry="5" fill="#ff6b9a" opacity=".45"/><ellipse cx="96" cy="84" rx="8" ry="5" fill="#ff6b9a" opacity=".45"/>'
            f'<path d="M56 86 Q64 94 72 86" fill="none" stroke="{d}" stroke-width="4" stroke-linecap="round"/>')
    ears = f'<path d="M26 34 Q22 4 52 16 Q36 20 26 34 Z M102 34 Q106 4 76 16 Q92 20 102 34 Z" fill="{l}"/>'
    return layered(BALL, c, sym(g, .3, 64, 36), ears + face)


def nebula(c, g):
    l, m, d = c
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity="{o}"/>' for x, y, r, o in
                    ((40, 44, 1.6, .9), (86, 36, 1.2, .8), (94, 80, 1.8, .9), (34, 84, 1.1, .7), (70, 98, 1.4, .8), (58, 30, 1, .7), (100, 56, 1, .6)))
    return svg(shadow_defs(f'<filter id="n"><feGaussianBlur stdDeviation="9"/></filter>'
                           f'<radialGradient id="s" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#2a2450"/>'
                           f'<stop offset="1" stop-color="#07061a"/></radialGradient><clipPath id="k"><circle cx="64" cy="64" r="56"/></clipPath>') +
               f'<circle cx="64" cy="72" r="52" fill="{m}" opacity=".55" filter="url(#sh)"/>'
               f'<circle cx="64" cy="64" r="56" fill="url(#s)"/>'
               f'<g clip-path="url(#k)" filter="url(#n)"><ellipse cx="50" cy="56" rx="34" ry="18" fill="{m}" opacity=".85" transform="rotate(-25 50 56)"/>'
               f'<ellipse cx="82" cy="80" rx="26" ry="14" fill="{l}" opacity=".7" transform="rotate(-25 82 80)"/></g>'
               f'{stars}<circle cx="64" cy="64" r="55" fill="none" stroke="{l}" stroke-width="2.5" opacity=".8"/>'
               f'<g fill="#fff" opacity=".95" style="filter:drop-shadow(0 0 6px {l})">{sym(g, .6)}</g>'
               '<path d="M34 42 A36 36 0 0 1 58 22" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".5"/>' + SPARK)


# id: (name, rarity, tagline, renderer)
SETS = {
    "jelly": ("Jelly Drops", "common", "Wobbly, glossy, squishy", jelly),
    "token": ("Pulse Tokens", "common", "Minted coins with ridged rims", token),
    "pebble": ("River Pebbles", "common", "Smooth stones with speckles", pebble),
    "bloom": ("Blooms", "rare", "Six-petal glass flowers", bloom),
    "hive": ("Hive Cells", "rare", "Honeycomb hexes with inner frame", hive),
    "starlet": ("Starlets", "rare", "Soft rounded stars", starlet),
    "crystal": ("Crystal Shards", "epic", "Four-facet cut crystals", crystal),
    "planet": ("Tiny Planets", "epic", "Ringed worlds", planet),
    "critter": ("Pulse Critters", "legendary", "Little friends who cheer your clears", critter),
    "nebula": ("Nebula Orbs", "legendary", "A galaxy in every piece", nebula),
}
PRICE = {"common": 40, "rare": 80, "epic": 140, "legendary": 220}

if __name__ == "__main__":
    meta = []
    for sid, (name, rarity, tag, fn) in SETS.items():
        pieces = []
        for i, cols in enumerate(COLS):
            f = f"col_{sid}_{i}.svg"
            os.makedirs(os.path.join(OUT, folder_for(f)), exist_ok=True)
            open(os.path.join(OUT, folder_for(f), f), "w").write(fn(cols, GLYPHS[SLOTS[i]]))
            pieces.append({"file": f, "color": cols[1], "light": cols[0], "price": PRICE[rarity]})
        meta.append({"id": sid, "name": name, "rarity": rarity, "tagline": tag, "pieces": pieces})
    json.dump(meta, open(os.path.join(OUT, "collection", "collection.json"), "w"), indent=1)
    print(f"wrote {len(meta) * 4} collection pieces + collection.json")
