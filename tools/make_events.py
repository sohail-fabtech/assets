# Event piece sets: 8 dated events × 4 colours = 32 pieces + events.json. Run: python3 make_events.py
# Live-ops model: dated window, play-to-earn prize path (no random drops), every event returns yearly.
import json, math, os
from make_assets import svg, layered, GLYPHS
from make_collection import COLS, SLOTS, SPARK, polar, sym, shadow_defs
from layout import folder_for

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
CANDLE = "#fff3c4"


def grad(id, l, m, d, cx="35%", cy="30%"):
    return (f'<radialGradient id="{id}" cx="{cx}" cy="{cy}" r="75%"><stop offset="0" stop-color="{l}"/>'
            f'<stop offset=".55" stop-color="{m}"/><stop offset="1" stop-color="{d}"/></radialGradient>')


def pumpkin(c, g):
    """Glowkin: three-lobe pumpkin, carved eyes + symbol nose + zigzag grin lit by a candle."""
    l, m, d = c
    return svg(shadow_defs(grad("b", l, m, d) + grad("s", m, d, d) + '<filter id="gl"><feGaussianBlur stdDeviation="3"/></filter>') +
               f'<ellipse cx="64" cy="112" rx="46" ry="8" fill="{d}" opacity=".5" filter="url(#sh)"/>'
               f'<ellipse cx="38" cy="74" rx="30" ry="40" fill="url(#s)"/><ellipse cx="90" cy="74" rx="30" ry="40" fill="url(#s)"/>'
               f'<ellipse cx="64" cy="72" rx="34" ry="44" fill="url(#b)"/>'
               f'<path d="M64 30 Q52 72 64 116 M64 30 Q76 72 64 116" stroke="{d}" stroke-width="2.5" fill="none" opacity=".35"/>'
               '<path d="M60 32 Q56 16 66 8 L74 12 Q66 20 68 32 Z" fill="#4f7a2a"/>'
               '<path d="M68 18 Q86 8 92 22 Q80 18 72 26" fill="#7fb83a"/>'
               f'<g fill="{CANDLE}" filter="url(#gl)" opacity=".8"><path d="M40 70 L52 56 L56 72 Z M88 70 L76 56 L72 72 Z"/></g>'
               f'<g fill="{CANDLE}"><path d="M40 70 L52 56 L56 72 Z M88 70 L76 56 L72 72 Z"/>'
               '<path d="M38 92 L47 99 L55 92 L64 99 L73 92 L81 99 L90 92 Q64 116 38 92 Z"/></g>'
               f'<g fill="{CANDLE}">{sym(g, .26, 64, 82)}</g>'
               '<ellipse cx="50" cy="44" rx="10" ry="5" fill="#fff" opacity=".45" transform="rotate(-25 50 44)"/>')


def snowglobe(c, g):
    """Frost Globe: glass dome with snow drift, symbol figurine, coloured base."""
    l, m, d = c
    return svg(shadow_defs(grad("bs", l, m, d, "50%", "10%") + '<clipPath id="k"><circle cx="64" cy="54" r="44"/></clipPath>') +
               f'<ellipse cx="64" cy="120" rx="40" ry="6" fill="{d}" opacity=".5" filter="url(#sh)"/>'
               f'<path d="M30 96 H98 L108 118 Q108 122 104 122 H24 Q20 122 20 118 Z" fill="url(#bs)"/>'
               f'<rect x="26" y="94" width="76" height="8" rx="4" fill="{l}"/>'
               f'<circle cx="64" cy="54" r="44" fill="{l}" opacity=".22"/>'
               f'<g clip-path="url(#k)"><ellipse cx="64" cy="100" rx="56" ry="20" fill="#fff"/>'
               f'<g fill="{m}">{sym(g, .55, 64, 58)}</g>'
               + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".9"/>' for x, y, r in
                         ((36, 30, 2.5), (52, 22, 2), (80, 28, 2.5), (92, 50, 2), (40, 56, 1.8), (86, 70, 2.2), (60, 38, 1.5), (30, 74, 2))) +
               '</g><circle cx="64" cy="54" r="44" fill="none" stroke="#fff" stroke-width="2.5" opacity=".7"/>'
               '<path d="M32 40 A36 36 0 0 1 58 16" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".75"/>' + SPARK)


def lantern(c, g):
    """Lucky Lantern: ribbed paper lantern, gold caps, tassel, warm inner glow."""
    l, m, d = c
    ribs = "".join(f'<ellipse cx="64" cy="64" rx="{rx}" ry="40" fill="none" stroke="{d}" stroke-width="2" opacity=".35"/>' for rx in (14, 30))
    return svg(shadow_defs(grad("b", CANDLE, m, d, "50%", "50%")) +
               f'<ellipse cx="64" cy="72" rx="44" ry="38" fill="{m}" opacity=".5" filter="url(#sh)"/>'
               '<path d="M64 0 V14" stroke="#c99a2a" stroke-width="3"/>'
               f'<ellipse cx="64" cy="64" rx="48" ry="40" fill="url(#b)"/>{ribs}'
               '<rect x="40" y="16" width="48" height="12" rx="5" fill="#ffd36a"/><rect x="40" y="100" width="48" height="12" rx="5" fill="#ffd36a"/>'
               '<rect x="42" y="18" width="44" height="4" rx="2" fill="#fff" opacity=".5"/>'
               '<path d="M64 112 V122 M58 114 V126 M70 114 V126" stroke="#ffd36a" stroke-width="3" stroke-linecap="round"/>'
               f'<g fill="#fff" opacity=".9">{sym(g, .5)}</g>'
               '<ellipse cx="40" cy="48" rx="8" ry="14" fill="#fff" opacity=".3"/>')


def letter(c, g):
    """Sealed With Love: tinted envelope closed by a wax seal stamped with the symbol."""
    l, m, d = c
    seal = polar(lambda t: 20 + 2.2 * math.cos(9 * t))
    return svg(shadow_defs(f'<linearGradient id="e" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{l}"/></linearGradient>') +
               f'<rect x="14" y="34" width="100" height="72" rx="12" fill="{d}" opacity=".5" filter="url(#sh)" transform="translate(0 8)"/>'
               '<rect x="10" y="28" width="108" height="76" rx="12" fill="url(#e)"/>'
               f'<path d="M12 98 L52 66 M116 98 L76 66" stroke="{m}" stroke-width="2.5" opacity=".35" fill="none"/>'
               f'<path d="M12 32 Q12 28 18 30 L64 70 L110 30 Q116 28 116 32 L72 76 Q64 82 56 76 Z" fill="{l}"/>'
               f'<path d="M12 32 L64 74 L116 32" fill="none" stroke="#fff" stroke-width="2" opacity=".7"/>'
               f'<g transform="translate(0 6)"><path d="{seal}" fill="{d}" transform="translate(0 3)"/><path d="{seal}" fill="{m}"/>'
               f'<circle cx="64" cy="64" r="13" fill="none" stroke="{d}" stroke-width="2" opacity=".5"/>'
               f'<g fill="#fff" opacity=".85">{sym(g, .32)}</g></g>' + SPARK)


EGG = "M64 8 C96 8 114 56 114 80 C114 106 92 122 64 122 C36 122 14 106 14 80 C14 56 32 8 64 8 Z"


def egg(c, g):
    """Spring Speckles: painted egg with zigzag band and dots."""
    l, m, d = c
    band = ('<path d="M16 66 L28 56 L40 66 L52 56 L64 66 L76 56 L88 66 L100 56 L112 66" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round" opacity=".7"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".6"/>' for x, y, r in ((40, 34, 3.5), (64, 24, 3), (88, 34, 3.5), (34, 104, 3), (94, 104, 3))))
    return layered(EGG, c, sym(g, .5, 64, 90), band)


ICEPOP = "M64 4 C88 4 100 18 100 40 V84 Q100 94 90 94 H38 Q28 94 28 84 V40 C28 18 40 4 64 4 Z"


def icepop(c, g):
    """Ice Pop: frosty bar with drip, glossy stripe and wooden stick."""
    l, m, d = c
    extra = ('<rect x="54" y="92" width="20" height="32" rx="9" fill="#e8c48a"/><rect x="58" y="94" width="5" height="24" rx="2.5" fill="#fff" opacity=".45"/>'
             f'<path d="M36 94 Q40 108 46 94" fill="{m}"/><circle cx="42" cy="106" r="2.5" fill="{m}"/>'
             '<rect x="38" y="16" width="9" height="64" rx="4.5" fill="#fff" opacity=".35"/>'
             '<path d="M48 22 L52 18 M80 28 L84 24 M76 70 L80 66" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".6"/>')
    return layered(ICEPOP, c, sym(g, .5, 64, 54), extra)


CAPY = "M64 24 C100 24 120 42 120 72 C120 102 98 118 64 118 C30 118 8 102 8 72 C8 42 28 24 64 24 Z"


def capy(c, g):
    """Chill Capy (original): sleepy calm face, big snout, fruit balanced on its head."""
    l, m, d = c
    face = (f'<ellipse cx="26" cy="38" rx="8" ry="6" fill="{d}"/><ellipse cx="102" cy="38" rx="8" ry="6" fill="{d}"/>'
            f'<path d="M34 64 Q42 70 50 64 M78 64 Q86 70 94 64" stroke="{d}" stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="64" cy="92" rx="32" ry="20" fill="{l}" opacity=".7"/>'
            f'<ellipse cx="55" cy="86" rx="4" ry="3" fill="{d}"/><ellipse cx="73" cy="86" rx="4" ry="3" fill="{d}"/>'
            f'<path d="M58 100 Q64 104 70 100" stroke="{d}" stroke-width="3" fill="none" stroke-linecap="round"/>'
            '<ellipse cx="30" cy="80" rx="7" ry="4" fill="#ff8aa8" opacity=".4"/><ellipse cx="98" cy="80" rx="7" ry="4" fill="#ff8aa8" opacity=".4"/>'
            f'<circle cx="64" cy="18" r="15" fill="{l}"/><circle cx="64" cy="18" r="15" fill="none" stroke="{d}" stroke-width="2" opacity=".3"/>'
            '<path d="M64 4 Q74 -2 80 6 Q72 6 66 8 Z" fill="#7fb83a"/>'
            f'<g fill="{d}" opacity=".8">{sym(g, .28, 64, 19)}</g>'
            '<ellipse cx="58" cy="12" rx="5" ry="3" fill="#fff" opacity=".7"/>')
    return layered(CAPY, c, "", face).replace('<path d="M96 22 l3 8', '<path d="M104 40 l3 8', 1)


FUZZ = polar(lambda t: 50 + 3.5 * math.sin(16 * t), cy=68)


def grump(c, g):
    """Grumpling (original ugly-cute): fuzzy blob, one half-lidded eye, lopsided toothy grin, nub horns."""
    l, m, d = c
    face = (f'<path d="M36 26 L42 6 L52 22 Z M92 26 L86 6 L76 22 Z" fill="{l}"/>'
            '<ellipse cx="64" cy="58" rx="22" ry="20" fill="#fff"/>'
            f'<circle cx="68" cy="62" r="10" fill="{d}"/><circle cx="64" cy="58" r="3.5" fill="#fff"/>'
            f'<path d="M40 52 Q64 34 88 52 L88 46 Q64 30 40 46 Z" fill="{m}"/>'
            f'<path d="M40 50 Q64 38 88 50" stroke="{d}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
            f'<path d="M38 88 Q64 104 92 84" stroke="{d}" stroke-width="4" fill="none" stroke-linecap="round"/>'
            '<path d="M50 92 L54 100 L58 94 Z M74 93 L77 101 L81 91 Z" fill="#fff"/>')
    return layered(FUZZ, c, sym(g, .24, 64, 108), face)


# id: set name, event, window (MM-DD start/end; end may wrap the year), story line, renderer
EVENTS = {
    "pumpkin": ("Glowkin Patch", "Spooky Pulse", "10-20", "11-03", "Carved by candlelight", pumpkin),
    "snowglobe": ("Frost Globes", "Winter Glow Festival", "12-10", "01-05", "A tiny snowfall in every piece", snowglobe),
    "lantern": ("Lucky Lanterns", "Lantern Festival", "01-20", "02-20", "Warm paper light for a new year", lantern),
    "letter": ("Sealed With Love", "Heart Week", "02-07", "02-21", "Wax-sealed notes", letter),
    "egg": ("Spring Speckles", "Spring Fest", "03-20", "04-20", "Hand-painted eggs", egg),
    "capy": ("Chill Capys", "Chill Week · trend drop", "05-01", "05-31", "Unbothered. Always.", capy),
    "icepop": ("Ice Pops", "Summer Splash", "07-01", "08-31", "Frosty, drippy, sweet", icepop),
    "grump": ("Grumplings", "Ugly-Cute Week · trend drop", "09-01", "09-30", "Grumpy outside, soft inside", grump),
}
PATH = [100, 250, 450, 700]  # prize path: event points needed for piece 1..4

if __name__ == "__main__":
    meta = []
    for eid, (name, event, start, end, story, fn) in EVENTS.items():
        pieces = []
        for i, cols in enumerate(COLS):
            f = f"evt_{eid}_{i}.svg"
            os.makedirs(os.path.join(OUT, folder_for(f)), exist_ok=True)
            open(os.path.join(OUT, folder_for(f), f), "w").write(fn(cols, GLYPHS[SLOTS[i]]))
            pieces.append({"file": f"{folder_for(f)}/{f}", "color": cols[1], "light": cols[0], "points": PATH[i]})
        meta.append({"id": eid, "name": name, "event": event, "start": start, "end": end, "story": story,
                     "returns": "yearly", "pieces": pieces})
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    json.dump(meta, open(os.path.join(OUT, "data", "events.json"), "w"), indent=1)
    print(f"wrote {len(meta) * 4} event pieces + events.json")
