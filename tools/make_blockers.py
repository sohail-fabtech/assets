# Blockers (board obstacles) with damage states: crate, ice, stone (3 hits) and chain lock (2 hits, overlays a piece).
#   assets/pieces/blockers/<design>/blk_<design>_<hp>.svg  + data/blockers.json      Run: python3 make_blockers.py
import json, os
from layout import folder_for

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")


def doc(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-8 -8 144 144" width="144" height="144">{body}</svg>'


FILTERS = ('<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>'
           '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="3"/>'
           '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .8 0"/></filter>')
SHADOW = '<rect x="12" y="20" width="104" height="104" rx="16" fill="#000" opacity=".4" filter="url(#soft)"/>'


def crack(d, w=3, light="#fff", lo=.35):
    """Crack = dark split with a thin lit edge so it reads as depth, not a drawn line."""
    return (f'<path d="{d}" fill="none" stroke="#000" stroke-opacity=".7" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{light}" stroke-opacity="{lo}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" transform="translate(1 1.5)"/>')


# ---- wooden crate ---------------------------------------------------------------------------------
def crate(hp):
    plank = lambda y, broken=False: (
        f'<rect x="14" y="{y}" width="100" height="30" rx="3" fill="url(#wood)"/>'
        f'<rect x="14" y="{y}" width="100" height="30" rx="3" filter="url(#grain)" opacity=".18"/>'
        f'<path d="M18 {y + 9} Q50 {y + 5} 78 {y + 10} T112 {y + 8} M18 {y + 21} Q46 {y + 25} 80 {y + 19} T112 {y + 22}" stroke="#6b3a14" stroke-width="1.4" fill="none" opacity=".55"/>'
        f'<rect x="14" y="{y}" width="100" height="3" fill="#fff" opacity=".25"/><rect x="14" y="{y + 27}" width="100" height="3" fill="#000" opacity=".25"/>')
    planks = plank(16) + plank(49) + plank(82)
    brace = ('<path d="M20 22 L108 106" stroke="#5a3010" stroke-width="15" stroke-linecap="round"/>'
             '<path d="M20 22 L108 106" stroke="url(#wood2)" stroke-width="11" stroke-linecap="round"/>'
             '<path d="M22 20 L110 104" stroke="#fff" stroke-opacity=".25" stroke-width="2" stroke-linecap="round"/>')
    bracket = lambda x, y, sx, sy: (f'<path d="M{x} {y} h{22 * sx} v{8 * sy} h{-14 * sx} v{14 * sy} h{-8 * sx} Z" fill="url(#iron)" stroke="#1d2129" stroke-width="1.2"/>'
                                    f'<circle cx="{x + 5 * sx}" cy="{y + 5 * sy}" r="2.2" fill="#d8dde5"/><circle cx="{x + 16 * sx}" cy="{y + 4 * sy}" r="1.8" fill="#d8dde5"/>')
    brackets = bracket(10, 10, 1, 1) + bracket(118, 10, -1, 1) + bracket(10, 118, 1, -1) + bracket(118, 118, -1, -1)
    dmg = ""
    if hp <= 2:
        dmg += crack("M30 52 L42 60 L38 68 L52 76") + crack("M80 86 L90 94 L86 104", 2.5)
    if hp == 1:  # middle plank snapped: dark gap with jagged splintered ends, loose splinters
        dmg += ('<path d="M38 49 L48 56 L42 62 L52 70 L44 79 L78 79 L70 72 L80 64 L72 57 L84 49 Z" fill="#2a1608"/>'
                '<path d="M38 49 L48 56 L42 62 L52 70 L44 79" fill="none" stroke="#e8b070" stroke-width="2"/>'
                '<path d="M84 49 L72 57 L80 64 L70 72 L78 79" fill="none" stroke="#e8b070" stroke-width="2"/>'
                '<path d="M96 108 l10 -4 l-8 7 Z M24 100 l-9 2 l7 -6 Z" fill="#c98a4a" stroke="#6b3a14"/>') + crack("M88 22 L96 34 L92 44", 2.5)
    return doc('<defs>' + FILTERS +
               '<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e0a060"/><stop offset=".5" stop-color="#c07a3a"/><stop offset="1" stop-color="#8a5020"/></linearGradient>'
               '<linearGradient id="wood2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8aa66"/><stop offset="1" stop-color="#9a5a24"/></linearGradient>'
               '<linearGradient id="iron" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#aab2be"/><stop offset="1" stop-color="#3b414d"/></linearGradient></defs>'
               + SHADOW + '<rect x="6" y="6" width="116" height="116" rx="12" fill="#5a3010"/>'
               '<rect x="8" y="8" width="112" height="112" rx="10" fill="#7a4418"/>' + planks + brace + dmg + brackets +
               '<rect x="6" y="6" width="116" height="116" rx="12" fill="none" stroke="#2a1608" stroke-width="2"/>')


# ---- ice block ------------------------------------------------------------------------------------
def ice(hp):
    body = "M22 6 H106 Q122 6 122 22 V106 Q122 122 106 122 H22 Q6 122 6 106 V22 Q6 6 22 6 Z"
    if hp == 1:  # chipped corner
        body = "M22 6 H84 L96 16 L106 10 L122 30 V106 Q122 122 106 122 H22 Q6 122 6 106 V22 Q6 6 22 6 Z"
    bubbles = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".55"/><circle cx="{x - r * .3}" cy="{y - r * .3}" r="{r * .35}" fill="#fff"/>'
                      for x, y, r in ((36, 84, 4), (46, 96, 2.5), (88, 70, 3), (72, 100, 2), (98, 92, 3.5)))
    frost = "".join(f'<path d="M{x} {y} l6 6 M{x + 6} {y} l-6 6" stroke="#fff" stroke-width="1.4" opacity=".55"/>' for x, y in ((24, 30), (96, 104), (104, 40), (20, 104)))
    dmg = ""
    if hp <= 2:
        dmg += crack("M64 34 L56 52 L66 60 L54 80 L60 96", 3, "#fff", .9) + crack("M66 60 L86 66 L98 58", 2.5, "#fff", .9)
    if hp == 1:
        dmg += (crack("M56 52 L36 46 L24 54", 2.5, "#fff", .9) + crack("M54 80 L34 88 L22 84", 2.5, "#fff", .9)
                + crack("M86 66 L94 84 L110 92", 2.5, "#fff", .9)
                + '<path d="M104 2 l8 -4 l2 8 Z M116 18 l8 0 l-3 6 Z" fill="#bfeeff" stroke="#fff" stroke-opacity=".8"/>')
    return doc('<defs>' + FILTERS +
               '<linearGradient id="ice" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f2fdff"/><stop offset=".45" stop-color="#9fe4ff"/><stop offset="1" stop-color="#3aa8e0"/></linearGradient>'
               f'<clipPath id="k"><path d="{body}"/></clipPath></defs>'
               + SHADOW + f'<path d="{body}" fill="url(#ice)" opacity=".92"/>'
               '<g clip-path="url(#k)">'
               '<path d="M6 6 H122 L100 28 H28 Z" fill="#fff" opacity=".45"/><path d="M6 6 L28 28 V100 L6 122 Z" fill="#fff" opacity=".25"/>'
               '<path d="M122 6 L100 28 V100 L122 122 Z" fill="#0a5a8a" opacity=".18"/><path d="M6 122 L28 100 H100 L122 122 Z" fill="#0a5a8a" opacity=".28"/>'
               '<rect x="28" y="28" width="72" height="72" rx="6" fill="#fff" opacity=".12"/>'
               f'{bubbles}{frost}<path d="M18 40 L40 18 M18 56 L56 18" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".55"/>{dmg}</g>'
               f'<path d="{body}" fill="none" stroke="#fff" stroke-opacity=".85" stroke-width="2.5"/>')


# ---- stone block ----------------------------------------------------------------------------------
STONES = [  # (polygon points, highlight side)
    "14,14 58,12 62,44 16,48", "64,12 114,14 112,40 66,44", "14,54 44,52 48,84 14,86",
    "52,50 112,46 114,82 54,86", "14,92 66,92 64,116 16,114", "72,92 114,90 114,114 70,116",
]


def stone(hp):
    gone = {3: (), 2: (), 1: (2, 5)}[hp]  # stones knocked out at last stage
    def rock(i, pts):
        if i in gone:
            return f'<polygon points="{pts}" fill="#2a2d33"/><polygon points="{pts}" fill="none" stroke="#000" stroke-opacity=".5" stroke-width="2"/>'
        return (f'<polygon points="{pts}" fill="url(#rock)" stroke="#3a3e46" stroke-width="2.5" stroke-linejoin="round"/>'
                f'<polygon points="{pts}" filter="url(#grain)" opacity=".22"/>'
                f'<polyline points="{" ".join(pts.split()[:2])}" fill="none" stroke="#fff" stroke-opacity=".45" stroke-width="2" stroke-linecap="round"/>')
    rocks = "".join(rock(i, p) for i, p in enumerate(STONES))
    moss = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#6fa83a" opacity=".85"/>' for x, y, r in ((18, 50, 3), (24, 52, 2), (62, 88, 2.5), (110, 44, 2.5)))
    dmg = ""
    if hp <= 2:
        dmg += crack("M30 18 L38 30 L34 40") + crack("M80 56 L88 66 L84 78 L94 82", 2.5)
    if hp == 1:
        dmg += crack("M84 18 L92 30 L100 34", 2.5) + crack("M30 96 L40 106 L36 112", 2.5)
        dmg += '<path d="M24 120 l6 -4 l5 4 Z M104 120 l7 -5 l4 5 Z M40 122 l4 -3 l3 3 Z" fill="#8a8f99" stroke="#3a3e46"/>'
    return doc('<defs>' + FILTERS +
               '<linearGradient id="rock" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c4c8d0"/><stop offset=".55" stop-color="#8a8f99"/><stop offset="1" stop-color="#5a5f69"/></linearGradient></defs>'
               + SHADOW + '<rect x="6" y="6" width="116" height="116" rx="14" fill="#3a3e46"/>' + rocks + moss + dmg +
               '<rect x="6" y="6" width="116" height="116" rx="14" fill="none" stroke="#22252b" stroke-width="2"/>')


# ---- chain lock (overlay; transparent so the locked piece shows through) --------------------------
def chain_links(x0, y0, x1, y1, n, skip=()):
    """Interlocking links along a line: face-on and edge-on links alternate like a real chain."""
    out, ang = "", 45 if (x1 - x0) * (y1 - y0) > 0 else -45
    for i in range(n):
        if i in skip: continue
        t = (i + .5) / n; x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        ry = 5.5 if i % 2 == 0 else 2.2
        out += (f'<g transform="rotate({ang} {x:.1f} {y:.1f})"><ellipse cx="{x:.1f}" cy="{y:.1f}" rx="9" ry="{ry}" fill="none" stroke="#1d2129" stroke-width="6"/>'
                f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="9" ry="{ry}" fill="none" stroke="url(#steel)" stroke-width="3.6"/>'
                + (f'<path d="M{x - 6:.1f} {y - 3.5:.1f} Q{x:.1f} {y - 6.5:.1f} {x + 6:.1f} {y - 3.5:.1f}" stroke="#fff" stroke-width="1.2" fill="none" opacity=".75"/>' if i % 2 == 0 else "")
                + '</g>')
    return out


def chain(hp):
    a = chain_links(4, 4, 124, 124, 13)
    b = chain_links(124, 4, 4, 124, 13, skip=(3, 4) if hp == 1 else ())
    shackle_y = 40 if hp == 2 else 30
    lock = (f'<path d="M50 {shackle_y + 26} V{shackle_y + 12} A14 14 0 0 1 78 {shackle_y + 12} V{shackle_y + 26 if hp == 2 else shackle_y + 16}" '
            'fill="none" stroke="#1d2129" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M50 {shackle_y + 26} V{shackle_y + 12} A14 14 0 0 1 78 {shackle_y + 12} V{shackle_y + 26 if hp == 2 else shackle_y + 16}" '
            'fill="none" stroke="url(#steel)" stroke-width="6" stroke-linecap="round"/>'
            '<rect x="40" y="62" width="48" height="40" rx="9" fill="url(#gold)" stroke="#5a3a00" stroke-width="2"/>'
            '<rect x="44" y="65" width="40" height="7" rx="3.5" fill="#fff" opacity=".45"/>'
            '<circle cx="64" cy="80" r="5" fill="#3a2400"/><path d="M62 82 h4 l1.5 10 h-7 Z" fill="#3a2400"/>')
    if hp == 2:  # chains pass behind the lock
        return doc('<defs>' + FILTERS + STEEL_GOLD + '</defs>' + a + b + lock)
    return doc('<defs>' + FILTERS + STEEL_GOLD + '</defs>' + a + b +
               # snapped link ends + lock popped open and tilted
               '<path d="M92 34 l5 -7 M82 46 l-5 5" stroke="url(#steel)" stroke-width="3.6" stroke-linecap="round"/>'
               f'<g transform="rotate(-12 64 82)">{lock}</g>')


STEEL_GOLD = ('<linearGradient id="steel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f6fa"/><stop offset=".5" stop-color="#9aa2ae"/><stop offset="1" stop-color="#4a505c"/></linearGradient>'
              '<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe9a0"/><stop offset=".5" stop-color="#e8b030"/><stop offset="1" stop-color="#9a6a08"/></linearGradient>')

BLOCKERS = {  # id: (name, hits, overlay?, rule, renderer)
    "crate": ("Wooden Crate", 3, False, "Breaks into splinters after 3 adjacent clears", crate),
    "ice": ("Ice Block", 3, False, "Cracks, chips, then shatters after 3 adjacent clears", ice),
    "stone": ("Stone Block", 3, False, "Crumbles stone by stone after 3 adjacent clears", stone),
    "chain": ("Chain Lock", 2, True, "Locks the piece under it; clear it twice to free", chain),
}

if __name__ == "__main__":
    meta = []
    for bid, (name, hits, overlay, rule, fn) in BLOCKERS.items():
        states = []
        for hp in range(hits, 0, -1):
            f = f"blk_{bid}_{hp}.svg"
            d = os.path.join(OUT, folder_for(f)); os.makedirs(d, exist_ok=True)
            open(os.path.join(d, f), "w").write(fn(hp))
            states.append({"hp": hp, "file": f"{folder_for(f)}/{f}"})
        meta.append({"id": bid, "name": name, "hits": hits, "overlay": overlay, "rule": rule, "states": states})
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    json.dump(meta, open(os.path.join(OUT, "data", "blockers.json"), "w"), indent=1)
    print(f"wrote {sum(len(m['states']) for m in meta)} blocker states + data/blockers.json")
