# Realistic bomb collection: 5 designs × 5 level tiers = 25 bombs, nested by design:
#   assets/bombs/<design>/bomb_<design>_<tier>.svg   + bombs.json (fuse-tip coords for the live spark, FX tints)
# Tiers read as materials (black iron → bronze → steel → gold → inferno). Fuse tips are unlit on purpose:
# the spark, fire and smoke are drawn live by assets/motion/blast.js.
import json, math, os
from layout import folder_for

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")

# tier: (name, level, body hi/mid/dark/deep, rim light, cap hi/mid/dark, fx light/color)
TIERS = {
    "iron": ("Black Iron", 1, ("#70757f", "#1c1e23", "#0b0c0e", "#020203"), "#6a7f96", ("#c4cad4", "#4a505c", "#15181d"), ("#ffd27a", "#ff7a1a")),
    "bronze": ("Bronze", 2, ("#ffdcac", "#b8742e", "#5a3110", "#1e0e04"), "#ffc28a", ("#ffe9b0", "#a8782a", "#3a2408"), ("#ffd9a0", "#ff8a2a")),
    "steel": ("Steel", 3, ("#ffffff", "#aeb6c2", "#555d6a", "#1a1e24"), "#d8ecff", ("#ffffff", "#9aa2ae", "#2a3038"), ("#e8f4ff", "#7fd0ff")),
    "gold": ("Gold", 4, ("#fff8c8", "#f2ba2c", "#8a5806", "#382000"), "#fff2a8", ("#fffbe0", "#e8b83a", "#6a4400"), ("#fff3b0", "#ffc21f")),
    "inferno": ("Inferno", 5, ("#ff9a5a", "#7a1a0c", "#2a0604", "#0a0101"), "#ff6a2a", ("#9aa2ae", "#3b414d", "#111316"), ("#ffd05a", "#ff3a1a")),
}


def doc(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-8 -8 144 144" width="144" height="144">{body}</svg>'


def defs(tier):
    _, _, (hi, mid, dk, deep), rim, (chi, cmid, cdk), _ = TIERS[tier]
    return (f'<defs><radialGradient id="body" cx="36%" cy="30%" r="78%"><stop offset="0" stop-color="{hi}"/>'
            f'<stop offset=".28" stop-color="{mid}"/><stop offset=".72" stop-color="{dk}"/><stop offset="1" stop-color="{deep}"/></radialGradient>'
            f'<radialGradient id="rim" cx="62%" cy="80%" r="60%"><stop offset=".55" stop-color="{rim}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{rim}" stop-opacity=".75"/></radialGradient>'
            f'<linearGradient id="cap" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{cdk}"/><stop offset=".35" stop-color="{chi}"/>'
            f'<stop offset=".6" stop-color="{cmid}"/><stop offset="1" stop-color="{cdk}"/></linearGradient>'
            '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="3"/>'
            '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .9 0"/></filter>'
            '<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>'
            '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.5"/></filter>'
            '</defs>')


def shell(clip_d, tier, highlight):
    """Shade any closed body shape like cast metal: gradient, grain, rim light, sharp + soft specular."""
    return (f'<clipPath id="k"><path d="{clip_d}"/></clipPath>'
            f'<path d="{clip_d}" fill="url(#body)"/>'
            f'<g clip-path="url(#k)"><rect x="-8" y="-8" width="144" height="144" filter="url(#grain)" opacity=".16"/>'
            f'<path d="{clip_d}" fill="url(#rim)"/>{highlight}</g>'
            f'<path d="{clip_d}" fill="none" stroke="#000" stroke-opacity=".55" stroke-width="1.5"/>')


def spec(x, y, rx, ry, ang=-30):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx * 1.9}" ry="{ry * 1.9}" fill="#fff" opacity=".22" filter="url(#soft)" transform="rotate({ang} {x} {y})"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#fff" opacity=".9" transform="rotate({ang} {x} {y})"/>')


def circle_d(cx, cy, r):
    return f"M{cx} {cy - r} A{r} {r} 0 1 1 {cx} {cy + r} A{r} {r} 0 1 1 {cx} {cy - r} Z"


def cap(cx, cy, ang, w, h):
    """Bolted cylindrical neck."""
    return (f'<g transform="rotate({ang} {cx} {cy})">'
            f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="3" fill="url(#cap)" stroke="#000" stroke-opacity=".6" stroke-width="1.2"/>'
            f'<rect x="{cx - w / 2 - 2}" y="{cy + h / 2 - 5}" width="{w + 4}" height="6" rx="2.5" fill="url(#cap)" stroke="#000" stroke-opacity=".6" stroke-width="1.2"/>'
            f'<circle cx="{cx - w / 2 + 4}" cy="{cy + h / 2 - 2}" r="1.6" fill="#000" opacity=".55"/><circle cx="{cx + w / 2 - 4}" cy="{cy + h / 2 - 2}" r="1.6" fill="#000" opacity=".55"/>'
            f'<rect x="{cx - w / 2 + 3}" y="{cy - h / 2 + 2}" width="3" height="{h - 6}" rx="1.5" fill="#fff" opacity=".55"/></g>')


def fuse(d):
    """Braided rope fuse with a charred tip."""
    return (f'<path d="{d}" stroke="#2a1a0c" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#8a6234" stroke-width="5" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#c9a06a" stroke-width="2" stroke-dasharray="2.5 3.5" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#3a2410" stroke-width="2" stroke-dasharray="2.5 3.5" stroke-dashoffset="3" fill="none" stroke-linecap="round" opacity=".7"/>')


def tip(x, y):
    return f'<circle cx="{x}" cy="{y}" r="3.4" fill="#151008"/>'


def contact(cx, cy, rx):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx * .16}" fill="#000" opacity=".45" filter="url(#soft)"/>'


def cracks(tier, paths):
    if tier != "inferno":
        return ""
    lines = "".join(f'<path d="{p}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' for p in paths)
    return (f'<g stroke="#ff5a1a" stroke-width="5" filter="url(#glow)" opacity=".9">{lines}</g>'
            f'<g stroke="#ffd27a" stroke-width="1.8">{lines}</g>')


def crack_paths(x, y, r):
    """Irregular fissures branching from one point, like heat-split metal."""
    out = []
    for a, L, kink in ((-2.6, .62, .35), (-1.2, .5, -.4), (.2, .58, .3), (1.5, .55, -.3), (2.6, .4, .45)):
        mx, my = x + r * L * .5 * math.cos(a + kink), y + r * L * .5 * math.sin(a + kink)
        ex, ey = x + r * L * math.cos(a), y + r * L * math.sin(a)
        bx, by = mx + r * .18 * math.cos(a - 1.1), my + r * .18 * math.sin(a - 1.1)
        out.append(f"M{x:.1f} {y:.1f} L{mx:.1f} {my:.1f} L{ex:.1f} {ey:.1f} M{mx:.1f} {my:.1f} L{bx:.1f} {by:.1f}")
    return out


def seam(cx, cy, r):
    return (f'<path d="M{cx - r} {cy} A{r} {r * .28} 0 0 0 {cx + r} {cy}" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="2"/>'
            f'<path d="M{cx - r} {cy + 1.6} A{r} {r * .28} 0 0 0 {cx + r} {cy + 1.6}" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="1.2"/>')


# ---- designs ---------------------------------------------------------------------------------------
def sphere_bomb(tier, cx, cy, r, cap_xy, cap_wh, fuse_d, tip_xy, extra_in="", extra_out=""):
    d = circle_d(cx, cy, r)
    return doc(defs(tier) + contact(cx, cy + r + 4, r * .8) + fuse(fuse_d) + tip(*tip_xy) +
               cap(*cap_xy, 40, *cap_wh) +
               shell(d, tier, seam(cx, cy + r * .15, r) + extra_in + spec(cx - r * .38, cy - r * .42, r * .2, r * .11)) +
               cracks(tier, crack_paths(cx + r * .15, cy + r * .1, r)) + extra_out)


def mini(t):
    return sphere_bomb(t, 58, 82, 34, (82, 50), (16, 14), "M84 44 Q96 34 92 22", (92, 22))


def classic(t):
    return sphere_bomb(t, 58, 74, 46, (90, 32), (22, 18), "M93 24 Q110 14 104 2", (104, 2))


def mega(t):
    cx, cy, r = 58, 72, 54
    band = lambda y, a: (f'<path d="M{cx - r} {y} A{r} {r * a} 0 0 0 {cx + r} {y}" stroke="url(#cap)" stroke-width="9" fill="none"/>'
                         f'<path d="M{cx - r} {y - 4} A{r} {r * a} 0 0 0 {cx + r} {y - 4}" stroke="#fff" stroke-opacity=".35" stroke-width="1.2" fill="none"/>')
    rivets = "".join(f'<circle cx="{x}" cy="{y}" r="2.8" fill="url(#cap)" stroke="#000" stroke-opacity=".6"/>'
                     for x, y in ((18, 82), (40, 91), (58, 93), (76, 91), (98, 82)))
    return sphere_bomb(t, cx, cy, r, (98, 24), (26, 20), "M102 15 Q120 4 112 -6", (112, -6), band(78, .3) + rivets)


def line(t):
    """Iron canister lying sideways with riveted end caps (row clear)."""
    body = "M26 52 H94 Q110 52 110 78 Q110 104 94 104 H26 Q10 104 10 78 Q10 52 26 52 Z"
    ends = "".join(f'<rect x="{x}" y="50" width="12" height="56" rx="5" fill="url(#cap)" stroke="#000" stroke-opacity=".6" stroke-width="1.2"/>'
                   f'<circle cx="{x + 6}" cy="60" r="1.8" fill="#000" opacity=".5"/><circle cx="{x + 6}" cy="96" r="1.8" fill="#000" opacity=".5"/>' for x in (8, 100))
    hl = ('<rect x="20" y="59" width="80" height="4" rx="2" fill="#fff" opacity=".7"/>'
          '<rect x="20" y="56" width="80" height="14" rx="7" fill="#fff" opacity=".18" filter="url(#soft)"/>')
    _, _, (hi, mid, dk, deep), *_ = TIERS[t]
    cyl = (f'<linearGradient id="body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{dk}"/><stop offset=".18" stop-color="{hi}"/>'
           f'<stop offset=".42" stop-color="{mid}"/><stop offset=".85" stop-color="{deep}"/><stop offset="1" stop-color="{dk}"/></linearGradient>')
    return doc(defs(t).replace('<radialGradient id="body"', '<radialGradient id="unused"').replace('<defs>', '<defs>' + cyl) +
               contact(60, 112, 50) + fuse("M60 42 Q64 26 78 18") + tip(78, 18) + cap(60, 46, 0, 18, 12) +
               shell(body, t, hl) + ends +
               cracks(t, crack_paths(62, 80, 34)))


def spike(t):
    """Naval-mine style sphere with capped horns all round (area clear)."""
    cx, cy, r = 64, 76, 38
    horns = ""
    for i in range(8):
        a = i * math.pi / 4 + math.pi / 8
        if abs(a - math.pi * 1.5) < .3: continue  # leave the top for the fuse cap
        x, y = cx + (r + 6) * math.cos(a), cy + (r + 6) * math.sin(a)
        deg = math.degrees(a) + 90
        horns += (f'<g transform="rotate({deg:.0f} {x:.1f} {y:.1f})"><rect x="{x - 4:.1f}" y="{y - 6:.1f}" width="8" height="14" rx="2" fill="url(#cap)" stroke="#000" stroke-opacity=".6"/>'
                  f'<rect x="{x - 6:.1f}" y="{y - 9:.1f}" width="12" height="5" rx="2.5" fill="url(#cap)" stroke="#000" stroke-opacity=".6"/></g>')
    return doc(defs(t) + contact(cx, cy + r + 10, r * .9) + fuse("M64 30 Q60 16 70 6") + tip(70, 6) + horns + cap(64, 36, 0, 18, 12) +
               shell(circle_d(cx, cy, r), t, seam(cx, cy + 6, r) + spec(cx - 15, cy - 16, 8, 4.5)) +
               cracks(t, crack_paths(70, 82, 34)))


BOMBS = {  # id: (name, size, blast, fuse tip in 128-grid, renderer)
    "mini": ("Mini Pop", "small", "tight cross", (92, 22), mini),
    "classic": ("Pulse Bomb", "medium", "3×3 blast", (104, 2), classic),
    "mega": ("Mega Boomer", "large", "5×5 blast", (112, -6), mega),
    "line": ("Line Blaster", "medium", "clears a full row", (78, 18), line),
    "spike": ("Spike Mine", "medium", "clears all around", (70, 6), spike),
}

if __name__ == "__main__":
    meta = []
    for bid, (name, size, blast, tp, fn) in BOMBS.items():
        files = []
        for tid, (tname, lvl, *_, fxc) in TIERS.items():
            f = f"bomb_{bid}_{tid}.svg"
            d = os.path.join(OUT, folder_for(f)); os.makedirs(d, exist_ok=True)
            open(os.path.join(d, f), "w").write(fn(tid))
            files.append({"file": f"{folder_for(f)}/{f}", "tier": tid, "tierName": tname, "level": lvl, "light": fxc[0], "color": fxc[1]})
        meta.append({"id": bid, "name": name, "size": size, "blast": blast, "tip": [(tp[0] + 8) / 144, (tp[1] + 8) / 144], "pieces": files})
    json.dump(meta, open(os.path.join(OUT, "bombs", "bombs.json"), "w"), indent=1)
    print(f"wrote {len(meta) * len(TIERS)} bombs + bombs.json")
