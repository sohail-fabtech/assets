# Level content per theme: 4 pieces, 3 obstacles (with damage states), 2 collectibles, board + cell.
#   assets/pieces/levels/<theme>/{pieces,obstacles,collectibles}/lv_<theme>_<kind>_<name>_<n>.svg
#   assets/board/levels/<theme>/lvb_<theme>_board|cell.svg      + data/levels.json      Run: python3 make_levels.py
# All designs are original. Obstacles get one file per remaining hit (n = hits left).
import itertools, json, math, os
from level_themes import THEMES
from layout import folder_for
from make_assets import layered, BALL, GLYPHS
from make_collection import SLOTS, polar, rounded_poly, sym, crystal as c_crystal, pebble as c_pebble, nebula as c_nebula
from make_themes import gem as t_gem, bubble as t_bubble, PILLOW
from make_blockers import crack, chain_links, STEEL_GOLD, crate as b_crate, ice as b_ice, chain as b_chain
from make_ui_kit import mix, lum

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
_id = itertools.count()
BOX = "M64 8 C110 8 120 18 120 64 C120 110 110 120 64 120 C18 120 8 110 8 64 C8 18 18 8 64 8 Z"
HEX = rounded_poly([(64 + 58 * math.cos(a), 64 + 58 * math.sin(a)) for a in (i * math.pi / 3 + math.pi / 6 for i in range(6))])
STAR = polar(lambda t: 26 + 32 * ((math.cos(5 * t) + 1) / 2) ** 2.6, 240)  # crisp rounded 5-point star
FX = ('<filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="4"/></filter>'
      '<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3"/></filter>'
      '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="2"/>'
      '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .7 0"/></filter>')


def doc(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-8 -8 144 144" width="144" height="144"><defs>{FX}{STEEL_GOLD}</defs>{body}</svg>'


def rg(l, m, d, cx="36%", cy="30%"):
    """Radial gradient defined inline; returns (defs, url)."""
    k = f"g{next(_id)}"
    return (f'<radialGradient id="{k}" cx="{cx}" cy="{cy}" r="75%"><stop offset="0" stop-color="{l}"/><stop offset=".55" stop-color="{m}"/>'
            f'<stop offset="1" stop-color="{d}"/></radialGradient>'), f"url(#{k})"


def lg(stops, x2=0, y2=1):
    k = f"g{next(_id)}"
    return (f'<linearGradient id="{k}" x1="0" y1="0" x2="{x2}" y2="{y2}">' + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
            + '</linearGradient>'), f"url(#{k})"


def shadow(cx=64, cy=118, rx=42):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx * .15}" fill="#000" opacity=".4" filter="url(#soft)"/>'


def spec(x, y, rx, ry, a=-30):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#fff" opacity=".75" transform="rotate({a} {x} {y})"/>'


# ---- pieces: one material language per theme --------------------------------------------------------
def p_lava(c, g):
    cr = '<path d="M30 80 L48 70 L60 86 L80 72 L98 84" stroke="#ffd27a" stroke-width="4" fill="none" filter="url(#glow)"/><path d="M30 80 L48 70 L60 86 L80 72 L98 84" stroke="#fff3c4" stroke-width="1.4" fill="none"/>'
    return layered(HEX, c, sym(g, .5, 64, 56), cr)


def p_wood(c, g):
    grain = "".join(f'<path d="M14 {y} Q40 {y - 6} 64 {y} T114 {y}" stroke="{c[2]}" stroke-width="1.6" fill="none" opacity=".3"/>' for y in (44, 64, 84))
    return layered(PILLOW, c, sym(g, .5), grain)


def p_pearl(c, g):
    sheen = ('<path d="M14 70 Q64 40 114 70 V120 H14 Z" fill="#7ff3ff" opacity=".16"/><path d="M14 40 Q64 10 114 40 V60 Q64 30 14 60 Z" fill="#ff9ee8" opacity=".14"/>')
    return layered(BALL, c, sym(g, .5), sheen)


def p_neon(c, g):
    l, m, d = c
    ring = f'<path d="{BOX}" fill="none" stroke="{l}" stroke-width="6" filter="url(#glow)"/><path d="{BOX}" fill="none" stroke="#fff" stroke-width="2" opacity=".8"/>'
    return layered(BOX, c, sym(g, .5), ring).replace("<defs>", "<defs>" + FX, 1)


def p_brass(c, g):
    rivets = "".join(f'<circle cx="{64 + 46 * math.cos(a):.1f}" cy="{64 + 46 * math.sin(a):.1f}" r="3.2" fill="url(#gold)"/>' for a in (i * math.pi / 3 + math.pi / 6 for i in range(6)))
    return layered(HEX, c, sym(g, .5), rivets).replace("<defs>", "<defs>" + STEEL_GOLD, 1)


PIECE = {"glossy": lambda c, g: layered(BOX, c, sym(g, 1.0)), "lava": p_lava, "frosted": t_bubble, "wood": p_wood, "ice": t_gem,
         "pearl": p_pearl, "neon": p_neon, "crystal": c_crystal, "sand": c_pebble, "brass": p_brass, "cosmic": c_nebula}


# ---- obstacles ----------------------------------------------------------------------------------------
def slab(t, hp, maxhp, top, mid, low, motif=""):
    """Tile-filling block (lava tile, sand, coral wall, crystal barrier, machine …) with progressive cracks."""
    gd, gu = lg([(0, top), (.5, mid), (1, low)], 1, 1)
    body = (f'<rect x="10" y="18" width="108" height="106" rx="16" fill="#000" opacity=".4" filter="url(#soft)"/>'
            f'<defs>{gd}</defs><rect x="6" y="10" width="116" height="112" rx="16" fill="{low}"/>'
            f'<rect x="6" y="6" width="116" height="110" rx="16" fill="{gu}"/>'
            f'<rect x="6" y="6" width="116" height="110" rx="16" filter="url(#grain)" opacity=".14"/>{motif}'
            f'<rect x="12" y="10" width="104" height="26" rx="12" fill="#fff" opacity=".16"/>'
            f'<rect x="6" y="6" width="116" height="110" rx="16" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="2"/>')
    return doc(body + damage(hp, maxhp))


def damage(hp, maxhp):
    hits = maxhp - hp
    paths = ["M34 30 L46 44 L40 56 L54 66", "M84 70 L94 82 L88 96 L100 104", "M80 24 L88 36 L100 40", "M26 84 L38 92 L34 104"]
    return "".join(crack(p, 3) for p in paths[:hits * 2])


def ball(t, hp, maxhp, l, m, d, extra="", r=44, cy=64):
    gd, gu = rg(l, m, d)
    return doc(f'<defs>{gd}</defs>' + shadow(64, cy + r + 6, r * .85) + f'<circle cx="64" cy="{cy}" r="{r}" fill="{gu}"/>'
               + extra + spec(64 - r * .38, cy - r * .42, r * .22, r * .12) + damage(hp, maxhp))


def obstacle(tid, oid, hp, maxhp):
    t = THEMES[tid]; p = t["palette"]
    S = lambda *a: slab(t, hp, maxhp, *a)
    if oid in ("crate", "ice", "chain"):  # graphite reuses the shipped blocker art
        return {"crate": b_crate, "ice": b_ice, "chain": b_chain}[oid](hp)
    if oid == "lava":
        return S("#ffb04a", "#e04a10", "#5a1004", '<path d="M20 50 Q44 36 64 54 T112 48 M18 86 Q50 72 72 90 T112 84" stroke="#fff3a0" stroke-width="5" fill="none" filter="url(#glow)" opacity=".9"/>'
                 '<path d="M20 50 Q44 36 64 54 T112 48 M18 86 Q50 72 72 90 T112 84" stroke="#fff6d0" stroke-width="1.6" fill="none"/>')
    if oid in ("rock", "asteroid"):
        craters = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#000" opacity=".25"/><circle cx="{x - 1}" cy="{y - 1}" r="{r}" fill="none" stroke="#fff" stroke-opacity=".25"/>'
                          for x, y, r in ((50, 52, 8), (80, 76, 6), (56, 86, 5), (84, 44, 4)))
        body = polar(lambda a: 46 + 4 * math.sin(3 * a) + 3 * math.cos(5 * a))
        gd, gu = rg("#b8a8a0" if oid == "rock" else "#a8a8c0", "#6a5a54" if oid == "rock" else "#54546a", "#2a2220")
        return doc(f'<defs>{gd}</defs>' + shadow() + f'<path d="{body}" fill="{gu}"/>{craters}' + spec(44, 38, 9, 5)
                   + ('<path d="M98 30 Q114 12 124 6 M100 40 Q118 30 126 26" stroke="#ff9a3a" stroke-width="4" stroke-linecap="round" opacity=".7"/>' if oid == "asteroid" else "") + damage(hp, maxhp))
    if oid == "fire":
        fl = "M64 8 C78 30 100 44 100 76 C100 102 84 120 64 120 C44 120 28 102 28 76 C28 58 40 50 44 34 C52 46 56 52 58 60 C62 44 58 26 64 8 Z"
        gd, gu = lg([(0, "#fff3a0"), (.45, "#ffa51f"), (1, "#e02a04")])
        return doc(f'<defs>{gd}</defs><path d="{fl}" fill="#ff6a1a" filter="url(#glow)" opacity=".8"/><path d="{fl}" fill="{gu}"/>'
                   '<path d="M64 60 C72 74 82 82 82 96 C82 108 74 116 64 116 C54 116 46 108 46 96 C46 86 56 80 64 60 Z" fill="#fff6c8" opacity=".85"/>' + damage(hp, maxhp))
    if oid == "balloon":
        gd, gu = rg(mix(p["secondary"], "#fff", .5), p["secondary"], p["secondaryDark"])
        return doc(f'<defs>{gd}</defs>' + shadow(64, 124, 22) + '<path d="M64 98 Q58 112 66 124" stroke="#fff" stroke-width="2" fill="none"/>'
                   f'<ellipse cx="64" cy="54" rx="38" ry="44" fill="{gu}"/><path d="M58 96 L70 96 L64 104 Z" fill="{p["secondaryDark"]}"/>' + spec(48, 32, 10, 6) + damage(hp, maxhp))
    if oid == "cloud":
        puffs = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/>' for x, y, r in ((40, 70, 26), (64, 56, 32), (90, 70, 26), (64, 82, 28)))
        return doc(shadow() + f'<g opacity=".96">{puffs}</g><g fill="#cfe4ff" opacity=".6"><circle cx="64" cy="92" r="22"/></g>' + damage(hp, maxhp))
    if oid == "platform":
        return doc(shadow(64, 124, 34) + '<path d="M14 60 H114 L98 92 L80 104 L64 120 L48 104 L30 92 Z" fill="#8a6a4a"/><path d="M14 60 H114 L104 74 H24 Z" fill="#6a4a2a"/>'
                   '<rect x="10" y="48" width="108" height="16" rx="8" fill="#5fd23a"/><rect x="16" y="50" width="96" height="5" rx="2.5" fill="#d6ff8a" opacity=".7"/>' + damage(hp, maxhp))
    if oid in ("vine", "seaweed"):
        col, dk = ("#3ad48a", "#127a46") if oid == "vine" else ("#2ad8a0", "#0a6a4a")
        stems = "".join(f'<path d="M{x} 124 C{x - 20} 90 {x + 20} 60 {x} 4" stroke="{dk}" stroke-width="7" fill="none" stroke-linecap="round"/>'
                        f'<path d="M{x} 124 C{x - 20} 90 {x + 20} 60 {x} 4" stroke="{col}" stroke-width="4" fill="none" stroke-linecap="round"/>' for x in (30, 64, 98)[:hp + 1])
        leaves = "".join(f'<path d="M{x} {y} q{10 * s} -12 {20 * s} -4 q-10 10 -{20 * s} 4 Z" fill="{col}" stroke="{dk}" stroke-width="1.5"/>'
                         for x, y, s in ((30, 40, 1), (64, 70, -1), (98, 30, -1), (64, 24, 1), (30, 96, 1), (98, 90, -1)))
        return doc(stems + leaves)
    if oid in ("mushroom", "glowshroom"):
        cap = "M18 66 C18 30 40 14 64 14 C88 14 110 30 110 66 Q64 78 18 66 Z"
        gd, gu = rg("#ff9a8a", "#e03a3a", "#7a0a0a") if oid == "mushroom" else rg("#c8fff0", "#3ad8c8", "#0a5a6a")
        dots = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".9"/>' for x, y, r in ((40, 40, 7), (66, 28, 6), (88, 46, 8), (60, 54, 4)))
        return doc(f'<defs>{gd}</defs>' + shadow() + '<path d="M48 64 Q44 104 52 118 H76 Q84 104 80 64 Z" fill="#f2e6d0"/><path d="M50 70 Q48 100 54 116" stroke="#d4c4a8" stroke-width="3" fill="none"/>'
                   + (f'<path d="{cap}" fill="#3ad8c8" filter="url(#glow)" opacity=".7"/>' if oid == "glowshroom" else "") + f'<path d="{cap}" fill="{gu}"/>{dots}' + damage(hp, maxhp))
    if oid == "stump":
        rings = "".join(f'<ellipse cx="64" cy="44" rx="{r}" ry="{r * .4}" fill="none" stroke="#8a5a2a" stroke-width="2" opacity=".6"/>' for r in (12, 24, 36))
        return doc(shadow() + '<path d="M18 44 V100 Q18 118 64 118 Q110 118 110 100 V44 Z" fill="#7a4a20"/><path d="M28 50 V104 M48 54 V112 M80 54 V112 M100 50 V104" stroke="#5a3010" stroke-width="3" opacity=".6"/>'
                   '<ellipse cx="64" cy="44" rx="46" ry="18" fill="#e0b070"/>' + rings + '<path d="M50 66 Q56 72 62 66 M66 66 Q72 72 78 66" stroke="#2a1608" stroke-width="3" fill="none" stroke-linecap="round"/>' + damage(hp, maxhp))
    if oid in ("iceblock", "barrier", "geode"):
        top, mid, low = {"iceblock": ("#f2fdff", "#8fdcff", "#2a8ac8"), "barrier": ("#f0e0ff", "#b06aff", "#4a1a8a"), "geode": ("#d8c8e0", "#7a6a80", "#2a2030")}[oid]
        motif = ('<polygon points="40,40 64,26 88,40 88,80 64,96 40,80" fill="#c06aff" opacity=".8"/><polygon points="40,40 64,26 64,60" fill="#fff" opacity=".4"/>' if oid == "geode"
                 else '<polygon points="6,6 50,6 24,116 6,116" fill="#fff" opacity=".18"/><polygon points="70,6 96,6 76,116 52,116" fill="#fff" opacity=".1"/>')
        return S(top, mid, low, motif)
    if oid in ("frostlock", "echochain"):
        tint = "#bfeeff" if oid == "frostlock" else "#c8a0ff"
        lock = ('<rect x="40" y="62" width="48" height="40" rx="9" fill="url(#gold)" stroke="#5a3a00" stroke-width="2"/>'
                '<path d="M50 64 V52 A14 14 0 0 1 78 52 V64" fill="none" stroke="url(#steel)" stroke-width="6"/><circle cx="64" cy="80" r="5" fill="#3a2400"/>') if hp > 1 else ""
        return doc(f'<g style="filter:drop-shadow(0 0 4px {tint})">' + chain_links(4, 4, 124, 124, 13) + chain_links(124, 4, 4, 124, 13, (3, 4) if hp == 1 else ()) + f'</g>{lock}')
    if oid == "slide":
        return S("#f2fdff", "#8fdcff", "#2a8ac8", '<path d="M30 64 H90 M74 44 L96 64 L74 84" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    if oid == "bubble":
        return t_bubble(("#d8fbff", "#7fe0ff", "#2a7aa8"), "")  # 1 hit: pops
    if oid == "coral":
        branch = "".join(f'<path d="M{x} 116 C{x} 90 {x + d} 70 {x + d * 1.4} 40" stroke="#ff7a8a" stroke-width="9" fill="none" stroke-linecap="round"/>' for x, d in ((34, -8), (54, 6), (74, -6), (94, 8)))
        return S("#ffd0c0", "#2a6a8a", "#0a2a4a", branch)
    if oid == "ghost":
        sheet = "M28 116 V56 C28 30 44 14 64 14 C84 14 100 30 100 56 V116 L90 106 L80 116 L70 106 L64 116 L58 106 L48 116 L38 106 Z"
        return doc(shadow(64, 124, 30) + f'<path d="{sheet}" fill="#f4f0ff" opacity=".95"/><path d="{sheet}" fill="none" stroke="#b04aff" stroke-width="2" opacity=".6"/>'
                   '<ellipse cx="52" cy="56" rx="7" ry="10" fill="#1a1030"/><ellipse cx="78" cy="56" rx="7" ry="10" fill="#1a1030"/><circle cx="54" cy="52" r="2.5" fill="#fff"/><circle cx="80" cy="52" r="2.5" fill="#fff"/>'
                   '<path d="M56 78 Q64 86 72 78" stroke="#1a1030" stroke-width="3.5" fill="none" stroke-linecap="round"/>' + damage(hp, maxhp))
    if oid == "bulb":
        return doc(shadow() + '<path d="M40 56 A26 26 0 1 1 88 56 C88 70 78 76 76 90 H52 C50 76 40 70 40 56 Z" fill="#fff8d0" opacity=".35" stroke="#fff" stroke-width="2.5"/>'
                   '<path d="M54 84 L58 60 L64 70 L70 60 L74 84" stroke="#ffd27a" stroke-width="2.5" fill="none"/>'
                   '<rect x="50" y="90" width="28" height="22" rx="4" fill="url(#steel)"/><path d="M50 96 H78 M50 104 H78" stroke="#4a505c" stroke-width="2"/>' + damage(hp, maxhp))
    if oid in ("wheel", "gear"):
        n, col = (12, p["secondary"]) if oid == "wheel" else (10, "#c89040")
        teeth = polar(lambda a: 52 + (6 if oid == "gear" else 0) * (1 if math.cos(n * a) > 0 else 0))
        spokes = "".join(f'<path d="M64 64 L{64 + 40 * math.cos(a):.1f} {64 + 40 * math.sin(a):.1f}" stroke="#fff" stroke-width="5" opacity=".7"/>' for a in (i * math.pi / 3 for i in range(6)))
        gd, gu = rg(mix(col, "#fff", .4), col, mix(col, "#000", .5))
        return doc(f'<defs>{gd}</defs>' + shadow() + f'<path d="{teeth}" fill="{gu}"/><circle cx="64" cy="64" r="40" fill="#000" opacity=".2"/>{spokes}'
                   '<circle cx="64" cy="64" r="12" fill="url(#steel)" stroke="#2a2f3a" stroke-width="2"/>' + damage(hp, maxhp))
    if oid == "sand":
        return S("#ffe8b0", "#e0b060", "#8a5a20", '<path d="M10 70 Q40 54 70 70 T120 66 M10 96 Q44 82 76 98 T120 92" stroke="#fff4d0" stroke-width="4" fill="none" opacity=".7"/>')
    if oid == "cactus":
        return doc(shadow() + '<path d="M50 120 V30 A14 14 0 0 1 78 30 V120 Z M50 76 H30 V50 A8 8 0 0 1 46 50 V64 H50 Z M78 66 H98 V40 A8 8 0 0 1 114 40 V74 Q114 82 106 82 H78 Z" fill="#3aa84a"/>'
                   '<path d="M64 26 V118 M40 56 V70 M106 46 V76" stroke="#1f6a2a" stroke-width="2" opacity=".6"/><circle cx="64" cy="16" r="7" fill="#ff6a9a"/>'
                   + "".join(f'<path d="M{x} {y} l-4 -3 M{x} {y} l4 -3" stroke="#fff" stroke-width="1.4"/>' for x, y in ((56, 50), (72, 70), (58, 94), (36, 60), (106, 56))) + damage(hp, maxhp))
    if oid == "mirage":
        return doc('<rect x="6" y="6" width="116" height="116" rx="16" fill="#ffe8b0" opacity=".25" stroke="#fff" stroke-opacity=".5" stroke-dasharray="6 6" stroke-width="2"/>'
                   + "".join(f'<path d="M18 {y} Q40 {y - 8} 64 {y} T110 {y}" stroke="#fff" stroke-width="3" fill="none" opacity=".55"/>' for y in (40, 64, 88)))
    if oid == "vent":
        return S("#c8c0b0", "#6a5a48", "#2a2016", '<rect x="24" y="30" width="80" height="60" rx="8" fill="#1a1410"/>' + "".join(f'<rect x="28" y="{y}" width="72" height="6" rx="3" fill="url(#steel)"/>' for y in (36, 50, 64, 78))
                 + '<g fill="#fff" opacity=".7" filter="url(#soft)"><circle cx="50" cy="20" r="10"/><circle cx="70" cy="12" r="12"/><circle cx="86" cy="22" r="8"/></g>')
    if oid == "machine":
        return S("#e8c080", "#a07030", "#4a3010", '<circle cx="64" cy="60" r="26" fill="#2a2016"/><circle cx="64" cy="60" r="20" fill="url(#gold)"/><path d="M64 46 V60 L74 66" stroke="#2a2016" stroke-width="4" stroke-linecap="round"/>'
                 + "".join(f'<circle cx="{x}" cy="{y}" r="3.2" fill="url(#steel)"/>' for x, y in ((18, 18), (110, 18), (18, 104), (110, 104))))
    if oid == "blackhole":
        swirl = "".join(f'<ellipse cx="64" cy="64" rx="{r}" ry="{r * .42}" fill="none" stroke="{c}" stroke-width="{w}" opacity=".85" transform="rotate(-20 64 64)"/>'
                        for r, c, w in ((56, "#ff4ab8", 4), (44, "#b06aff", 5), (32, "#ffd65a", 3)))
        return doc(f'{swirl}<circle cx="64" cy="64" r="24" fill="#000"/><circle cx="64" cy="64" r="24" fill="none" stroke="#fff" stroke-width="2" opacity=".7"/>' + damage(hp, maxhp))
    if oid == "satellite":
        return doc(shadow() + '<rect x="4" y="50" width="38" height="26" rx="3" fill="#2a4a8a" stroke="#c8d8ff" stroke-width="2"/><rect x="86" y="50" width="38" height="26" rx="3" fill="#2a4a8a" stroke="#c8d8ff" stroke-width="2"/>'
                   '<path d="M8 63 H38 M90 63 H120 M23 50 V76 M105 50 V76" stroke="#c8d8ff" stroke-width="1.2" opacity=".6"/><rect x="44" y="40" width="40" height="46" rx="8" fill="url(#steel)"/>'
                   '<path d="M64 40 V20" stroke="#c8d8ff" stroke-width="3"/><circle cx="64" cy="18" r="5" fill="#ff4a5a"/>' + damage(hp, maxhp))
    raise ValueError(f"no obstacle drawer for {oid}")


# ---- collectibles -------------------------------------------------------------------------------------
def collectible(tid, cid):
    t = THEMES[tid]; p = t["palette"]; a, b = p["primary"], p["secondary"]
    gem = lambda col, shape: t_gem((mix(col, "#fff", .5), col, mix(col, "#000", .55)), "") if shape == "hex" else c_crystal((mix(col, "#fff", .5), col, mix(col, "#000", .55)), "")
    if cid in ("firecrystal", "skycrystal", "rarecrystal", "prism"): return gem({"firecrystal": "#ff6a1a", "skycrystal": "#7fd0ff", "rarecrystal": b, "prism": "#e04ad0"}[cid], "diamond")
    if cid in ("magmagem", "icediamond", "jewel"): return gem({"magmagem": "#e8203a", "icediamond": "#8fdcff", "jewel": "#1fc8c0"}[cid], "hex")
    if cid in ("pearl", "planetcore", "steamcore", "shard"):
        col = {"pearl": "#f6eef0", "planetcore": "#ff7a3a", "steamcore": "#ffd27a", "shard": "#7f9bff"}[cid]
        gd, gu = rg("#fff", col, mix(col, "#000", .45))
        glow = f'<circle cx="64" cy="64" r="52" fill="{col}" opacity=".5" filter="url(#glow)"/>' if cid != "pearl" else ""
        return doc(f'<defs>{gd}</defs>{shadow(64, 116, 34)}{glow}<circle cx="64" cy="64" r="40" fill="{gu}"/>'
                   + ('<path d="M30 72 Q64 54 98 72" stroke="#fff" stroke-width="3" fill="none" opacity=".5"/>' if cid == "planetcore" else "") + spec(50, 48, 10, 6))
    if cid in ("starfrag", "star"):
        gd, gu = rg("#fff8c8", "#ffd23a", "#a06400")
        return doc(f'<defs>{gd}</defs><path d="{STAR}" fill="#ffd23a" filter="url(#glow)" opacity=".7"/><path d="{STAR}" fill="{gu}"/>' + spec(52, 46, 8, 4))
    if cid == "feather":
        return doc('<path d="M100 14 C60 20 30 60 26 112 C60 100 96 66 100 14 Z" fill="#fff" stroke="#bcd8ff" stroke-width="2"/><path d="M26 112 Q60 60 100 14" stroke="#8ab8ff" stroke-width="3" fill="none"/>'
                   + "".join(f'<path d="M{x} {y} l12 -6" stroke="#bcd8ff" stroke-width="2"/>' for x, y in ((40, 92), (52, 76), (64, 60), (76, 44))))
    if cid == "glowshroom": return obstacle(tid, "glowshroom", 1, 1)
    if cid == "fairydust":
        sp = "".join(f'<path d="M{x} {y - s} L{x + s * .3} {y - s * .3} L{x + s} {y} L{x + s * .3} {y + s * .3} L{x} {y + s} L{x - s * .3} {y + s * .3} L{x - s} {y} L{x - s * .3} {y - s * .3} Z" fill="{c}"/>'
                     for x, y, s, c in ((64, 60, 30, "#fff6b0"), (32, 36, 12, "#7fe8ff"), (98, 40, 14, "#ffb8e8"), (40, 98, 10, "#c8ffa8"), (94, 94, 12, "#fff")))
        return doc(f'<g filter="url(#glow)" opacity=".8">{sp}</g>{sp}')
    if cid == "snowflake":
        arms = "".join(f'<path d="M64 64 L{64 + 54 * math.cos(r):.1f} {64 + 54 * math.sin(r):.1f} M{64 + 32 * math.cos(r):.1f} {64 + 32 * math.sin(r):.1f} l{12 * math.cos(r + .8):.1f} {12 * math.sin(r + .8):.1f} M{64 + 32 * math.cos(r):.1f} {64 + 32 * math.sin(r):.1f} l{12 * math.cos(r - .8):.1f} {12 * math.sin(r - .8):.1f}"/>'
                       for r in (i * math.pi / 3 - math.pi / 2 for i in range(6)))
        return doc(f'<g stroke="#5cc8ff" stroke-width="11" stroke-linecap="round" fill="none">{arms}</g><g stroke="#f2fbff" stroke-width="6" stroke-linecap="round" fill="none">{arms}</g>')
    if cid == "shell":
        from make_seasons import shell
        return shell(("#ffd8c8", "#ff8a7a", "#8a2a1a"), "")
    if cid in ("ticket", "token", "waterdrop", "cog"):
        if cid == "ticket":
            return doc('<g transform="rotate(-12 64 64)"><path d="M14 36 H114 V54 A10 10 0 0 0 114 74 V92 H14 V74 A10 10 0 0 0 14 54 Z" fill="#7aff4a"/>'
                       '<path d="M40 36 V92" stroke="#1a1030" stroke-width="2" stroke-dasharray="4 4"/><circle cx="76" cy="64" r="14" fill="#1a1030"/><circle cx="72" cy="60" r="3" fill="#7aff4a"/><circle cx="82" cy="60" r="3" fill="#7aff4a"/></g>')
        if cid == "token":
            gd, gu = rg("#e8c8ff", "#9a4aff", "#3a0a8a")
            return doc(f'<defs>{gd}</defs>{shadow(64, 116, 34)}<circle cx="64" cy="64" r="44" fill="{gu}"/><circle cx="64" cy="64" r="34" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="4 5" opacity=".7"/>'
                       '<path d="M52 56 A12 14 0 0 1 76 56 V80 L70 74 L64 80 L58 74 L52 80 Z" fill="#fff" opacity=".9"/>' + spec(48, 42, 10, 5))
        if cid == "waterdrop":
            from make_seasons import raindrop
            return raindrop(("#a8f8ff", "#1fc8e0", "#05606a"), "")
        teeth = polar(lambda a: 46 + 10 * (1 if math.cos(8 * a) > 0 else 0))
        gd, gu = rg("#fff0b0", "#e0a040", "#6a4000")
        return doc(f'<defs>{gd}</defs>{shadow()}<path d="{teeth}" fill="{gu}"/><circle cx="64" cy="64" r="16" fill="#2a1a08"/>' + spec(48, 40, 8, 4))
    raise ValueError(f"no collectible drawer for {cid}")


GROUND = {  # theme-specific base the hero item sits on (rgb glow colour, base art)
    "volcano": ("#ff6a1a", '<path d="M30 220 L60 180 L100 196 L128 170 L160 192 L200 178 L228 220 Z" fill="#2a0e08"/><path d="M60 214 L96 200 L128 210 L170 198 L204 214" stroke="#ff8a1a" stroke-width="4" fill="none" filter="url(#glow)"/>'),
    "sky": ("#bfe4ff", '<g fill="#fff"><circle cx="70" cy="206" r="30"/><circle cx="110" cy="194" r="38"/><circle cx="156" cy="200" r="34"/><circle cx="192" cy="210" r="24"/><rect x="60" y="206" width="140" height="26" rx="13"/></g>'),
    "forest": ("#7fffb0", '<ellipse cx="128" cy="214" rx="96" ry="22" fill="#1f6a2a"/><ellipse cx="128" cy="208" rx="86" ry="14" fill="#3aa84a"/><path d="M60 206 l4 -14 l4 14 M180 206 l4 -12 l4 12 M100 210 l3 -10 l3 10" stroke="#7fe08a" stroke-width="3"/>'),
    "tundra": ("#bfeeff", '<ellipse cx="128" cy="214" rx="100" ry="24" fill="#a8d0f0"/><ellipse cx="128" cy="206" rx="90" ry="16" fill="#f4fbff"/>'),
    "reef": ("#a8fff4", '<path d="M40 214 Q128 120 216 214 Z" fill="#ffd8c8" stroke="#c87a5a" stroke-width="3"/><path d="M128 214 L80 150 M128 214 L104 136 M128 214 L152 136 M128 214 L176 150" stroke="#e8a890" stroke-width="3"/><ellipse cx="128" cy="218" rx="100" ry="14" fill="#e8c890"/>'),
    "carnival": ("#b04aff", '<ellipse cx="128" cy="214" rx="104" ry="22" fill="#c8b0ff" opacity=".35" filter="url(#soft)"/>'),
    "crystal": ("#c06aff", '<path d="M40 222 L70 196 L110 206 L150 190 L200 204 L220 222 Z" fill="#2a1450"/><path d="M70 196 L84 168 L98 202 Z M180 200 L190 176 L202 204 Z" fill="#7a4aff"/>'),
    "desert": ("#ffd27a", '<path d="M20 222 Q90 180 150 200 T236 222 Z" fill="#f0b860"/><path d="M40 216 Q100 196 150 206" stroke="#fff4d0" stroke-width="3" fill="none" opacity=".7"/>'),
    "steampunk": ("#ffc86a", '<rect x="44" y="196" width="168" height="26" rx="8" fill="url(#gold)" stroke="#3a2008" stroke-width="3"/>' + "".join(f'<circle cx="{x}" cy="209" r="4" fill="#3a2008"/>' for x in (60, 196))),
    "nebula": ("#ff4ab8", '<ellipse cx="128" cy="210" rx="104" ry="20" fill="none" stroke="#ffb0f0" stroke-width="5" opacity=".7" filter="url(#glow)"/><ellipse cx="128" cy="210" rx="104" ry="20" fill="none" stroke="#fff" stroke-width="1.5"/>'),
    "graphite": ("#7ff3ff", '<ellipse cx="128" cy="214" rx="90" ry="18" fill="#2a2f3a"/><ellipse cx="128" cy="208" rx="80" ry="12" fill="#5b616e"/>'),
}


def hero(tid, cid):
    """Showcase render (256²) for collection tiles: glow halo + rays + themed base + the item, large + sparkles."""
    col, base = GROUND[tid]
    inner = collectible(tid, cid)
    rays = "".join(f'<path d="M128 110 L{128 + 140 * math.cos(a / 8 * 6.283):.0f} {110 + 140 * math.sin(a / 8 * 6.283):.0f} L{128 + 140 * math.cos((a + .35) / 8 * 6.283):.0f} {110 + 140 * math.sin((a + .35) / 8 * 6.283):.0f} Z" fill="{col}" opacity=".14"/>' for a in range(8))
    sparks = "".join(f'<path d="M{x} {y - r} C{x + r * .15} {y - r * .15} {x + r * .15} {y - r * .15} {x + r} {y} C{x + r * .15} {y + r * .15} {x + r * .15} {y + r * .15} {x} {y + r} C{x - r * .15} {y + r * .15} {x - r * .15} {y + r * .15} {x - r} {y} C{x - r * .15} {y - r * .15} {x - r * .15} {y - r * .15} {x} {y - r} Z" fill="#fff"/>'
                     for x, y, r in ((44, 60, 10), (214, 84, 8), (196, 36, 6), (60, 150, 6)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256"><defs>{FX}{STEEL_GOLD}</defs>'
            f'{rays}<circle cx="128" cy="110" r="96" fill="{col}" opacity=".35" filter="url(#soft)"/>{base}'
            f'<svg x="38" y="18" width="180" height="180" viewBox="-8 -8 144 144">{inner[inner.index(">") + 1:inner.rindex("</svg>")]}</svg>{sparks}</svg>')


# world collection goal: (collectible id, how many, tile title) — drives the world cards + Collection screen
GOALS = {"graphite": ("shard", 20, "Pulse Shards"), "volcano": ("firecrystal", 20, "Volcano Gems"), "sky": ("feather", 20, "Sky Feathers"),
         "forest": ("glowshroom", 18, "Fairy Mushrooms"), "tundra": ("snowflake", 20, "Ice Flakes"), "reef": ("pearl", 18, "Pearls"),
         "carnival": ("ticket", 18, "Ghost Tickets"), "crystal": ("rarecrystal", 20, "Crystals"), "desert": ("waterdrop", 20, "Oasis Drops"),
         "steampunk": ("cog", 18, "Gears"), "nebula": ("starfrag", 20, "Star Fragments")}


def board(t):
    p = t["palette"]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024"><defs>'
            f'<radialGradient id="f" cx="50%" cy="35%" r="75%"><stop offset="0" stop-color="{p["surface"]}"/><stop offset="1" stop-color="{p["bg"]}"/></radialGradient>'
            f'<linearGradient id="r" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{mix(p["primary"], "#fff", .4)}"/><stop offset=".5" stop-color="{p["primaryDark"]}"/>'
            f'<stop offset="1" stop-color="{mix(p["secondary"], "#fff", .3)}"/></linearGradient></defs>'
            '<rect width="1024" height="1024" rx="88" fill="url(#r)"/><rect x="14" y="14" width="996" height="996" rx="76" fill="url(#f)"/>'
            '<rect x="15" y="15" width="994" height="994" rx="75" fill="none" stroke="#fff" stroke-opacity=".15" stroke-width="2"/></svg>')


def cell(t):
    dark = "#000" if lum(t["palette"]["bg"]) < .3 else "#1d2a4a"  # light themes get a navy inset
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">'
            f'<rect x="4" y="4" width="120" height="120" rx="28" fill="{dark}" opacity=".26"/>'
            '<rect x="4" y="6" width="120" height="118" rx="28" fill="none" stroke="#fff" stroke-opacity=".08" stroke-width="2"/></svg>')


def write(f, data):
    d = os.path.join(OUT, folder_for(f)); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f), "w").write(data)
    return f"{folder_for(f)}/{f}"


if __name__ == "__main__":
    levels, n = {}, 0
    for tid, t in THEMES.items():
        draw = PIECE[t["material"]]
        pieces = [write(f"lv_{tid}_pieces_p_{i}.svg", draw(c, GLYPHS[SLOTS[i]])) for i, c in enumerate(t["pieces"])]
        obstacles = [{"id": oid, "name": name, "hits": hits,
                      "states": [write(f"lv_{tid}_obstacles_{oid}_{hp}.svg", obstacle(tid, oid, hp, hits)) for hp in range(hits, 0, -1)]}
                     for oid, name, hits in t["obstacles"]]
        collectibles = [{"id": cid, "name": name, "file": write(f"lv_{tid}_collectibles_{cid}_0.svg", collectible(tid, cid)),
                         "hero": write(f"lv_{tid}_hero_{cid}_0.svg", hero(tid, cid))} for cid, name in t["collectibles"]]
        n += 4 + sum(len(o["states"]) for o in obstacles) + 2 * len(collectibles) + 2
        levels[tid] = {"name": t["name"], "mood": t["mood"], "material": t["material"], "pieces": pieces, "obstacles": obstacles,
                       "collectibles": collectibles, "mechanics": t["mechanics"],
                       "board": write(f"lvb_{tid}_board.svg", board(t)), "cell": write(f"lvb_{tid}_cell.svg", cell(t)),
                       "goal": dict(zip(("item", "count", "title"), GOALS[tid]))}
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    json.dump(levels, open(os.path.join(OUT, "data", "levels.json"), "w"), indent=1)
    print(f"wrote {n} level assets for {len(levels)} themes + data/levels.json")
