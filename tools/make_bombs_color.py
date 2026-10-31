# Colour bombs (soft-clay, match the piece colours): 5 designs × 4 colours = 20, nested:
#   assets/bombs/colored/<design>/bombc_<design>_<i>.svg   + bombs/bombs_color.json   Run: python3 make_bombs_color.py
import json, math, os
from make_assets import layered, GLYPHS
from make_collection import COLS, SLOTS, sym, polar
from make_sweets import circ
from layout import folder_for

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
SPARK = '<path d="M96 22 l3 8 8 3 -8 3 -3 8 -3 -8 -8 -3 8 -3 z" fill="#fff"/>'  # layered()'s sparkle; removed (fuse lives there)
METAL = ('<linearGradient id="mt" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f6fa"/>'
         '<stop offset=".5" stop-color="#8c94a3"/><stop offset="1" stop-color="#3b414d"/></linearGradient>')


def cap_and_fuse(cx, cy, ang, w, h, fuse):
    return (f'<g transform="rotate({ang} {cx} {cy})"><rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{h * .3}" fill="url(#mt)"/>'
            f'<rect x="{cx - w / 2 + 2}" y="{cy - h / 2 + 2}" width="{w - 4}" height="{h * .3}" rx="2" fill="#fff" opacity=".6"/></g>'
            f'<path d="{fuse}" stroke="#3a2614" stroke-width="5.5" fill="none" stroke-linecap="round"/>'
            f'<path d="{fuse}" stroke="#b08a5a" stroke-width="2" stroke-dasharray="3 4" fill="none" stroke-linecap="round"/>')


def body(shape, c, glyph, extra):
    return layered(shape, c, glyph, extra).replace(SPARK, "").replace("<defs>", "<defs>" + METAL, 1)


def window(cx, cy, r, c):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c[2]}" opacity=".15"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-width="3" opacity=".45"/>')


def mini(c, g):
    return body(circ(58, 84, 34), c, sym(g, .42, 58, 86), cap_and_fuse(80, 56, 40, 20, 14, "M84 50 Q94 38 90 26"))


def classic(c, g):
    return body(circ(58, 74, 46), c, sym(g, .5, 54, 80), window(54, 80, 22, c) + cap_and_fuse(90, 36, 40, 26, 18, "M94 28 Q108 18 102 6"))


def mega(c, g):
    bands = ('<path d="M6 66 Q58 84 112 66" stroke="url(#mt)" stroke-width="9" fill="none"/>'
             '<path d="M14 102 Q58 118 104 102" stroke="url(#mt)" stroke-width="7" fill="none"/>'
             + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#3b414d"/>' for x, y in ((22, 71), (58, 75), (94, 71), (30, 106), (58, 110), (86, 106))))
    return body(circ(58, 72, 54), c, sym(g, .42, 58, 50), bands + cap_and_fuse(96, 26, 40, 30, 20, "M100 18 Q118 6 112 -4"))


LINE = "M30 46 H90 C108 46 118 60 118 76 C118 92 108 106 90 106 H30 C12 106 2 92 2 76 C2 60 12 46 30 46 Z"


def line(c, g):
    chev = ('<path d="M24 64 L12 76 L24 88 M34 64 L22 76 L34 88 M96 64 L108 76 L96 88 M86 64 L98 76 L86 88" '
            'stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>')
    return body(LINE, c, sym(g, .4, 60, 76), chev + cap_and_fuse(60, 40, 0, 26, 14, "M60 34 Q64 20 76 14"))


SPIKE = polar(lambda t: 40 + 9 * max(0.0, math.cos(8 * t)) ** 6, 240, cy=76)


def spike(c, g):
    return body(SPIKE, c, sym(g, .42, 64, 76), window(64, 76, 20, c) + cap_and_fuse(64, 30, 0, 22, 12, "M64 25 Q60 12 70 4"))


BOMBS = {  # id: (name, size, blast, fuse tip, renderer)
    "mini": ("Mini Pop", "small", "tight cross", (90, 26), mini),
    "classic": ("Pulse Bomb", "medium", "3×3 blast", (102, 6), classic),
    "mega": ("Mega Boomer", "large", "5×5 blast", (112, -4), mega),
    "line": ("Line Blaster", "medium", "clears a full row", (76, 14), line),
    "spike": ("Spike Mine", "medium", "clears all around", (70, 4), spike),
}

if __name__ == "__main__":
    meta = []
    for bid, (name, size, blast, tip, fn) in BOMBS.items():
        files = []
        for i, cols in enumerate(COLS):
            f = f"bombc_{bid}_{i}.svg"
            d = os.path.join(OUT, folder_for(f)); os.makedirs(d, exist_ok=True)
            open(os.path.join(d, f), "w").write(fn(cols, GLYPHS[SLOTS[i]]))
            files.append({"file": f"{folder_for(f)}/{f}", "tierName": ["Cyan", "Magenta", "Lime", "Amber"][i], "light": cols[0], "color": cols[1]})
        meta.append({"id": bid, "name": name, "size": size, "blast": blast, "tip": [(tip[0] + 8) / 144, (tip[1] + 8) / 144], "pieces": files})
    json.dump(meta, open(os.path.join(OUT, "bombs", "bombs_color.json"), "w"), indent=1)
    print(f"wrote {len(meta) * 4} colour bombs + bombs_color.json")
