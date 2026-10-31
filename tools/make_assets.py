# Generates Edge Pulse SVG assets into ../assets. Run: python3 tools/make_assets.py
import os
from layout import folder_for

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
COLORS = {"cyan": ("#7ff3ff", "#14b8d4", "#06576b"),
          "magenta": ("#ff9ee8", "#e83fb8", "#6e0f55"),
          "lime": ("#d6ff8a", "#7fd420", "#2f5a07"),
          "amber": ("#ffe08a", "#ffa51f", "#7a3d00")}


def svg(body, w=128, h=128, pad=8):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w+2*pad} {h+2*pad}" '
            f'width="{w+2*pad}" height="{h+2*pad}">{body}</svg>')


def grad(id, light, mid, dark):
    return (f'<radialGradient id="{id}" cx="35%" cy="30%" r="75%">'
            f'<stop offset="0" stop-color="{light}"/><stop offset=".55" stop-color="{mid}"/>'
            f'<stop offset="1" stop-color="{dark}"/></radialGradient>')


SHADOW = '<ellipse cx="64" cy="122" rx="40" ry="6" fill="#000" opacity=".3"/>'
BOX = "M64 8 C110 8 120 18 120 64 C120 110 110 120 64 120 C18 120 8 110 8 64 C8 18 18 8 64 8 Z"  # squircle
BALL = "M64 8 A56 56 0 1 1 63.9 8 Z"
GLYPHS = {  # embossed symbol per color = colorblind friendly
    "cyan": '<path d="M64 42 C75 57 81 66 81 75 A17 17 0 0 1 47 75 C47 66 53 57 64 42 Z"/>',
    "magenta": '<path d="M64 88 C45 75 42 62 49 55 C56 48 62 52 64 57 C66 52 72 48 79 55 C86 62 83 75 64 88 Z"/>',
    "lime": '<path d="M46 84 C46 60 61 47 84 44 C84 68 71 84 46 84 Z"/>',
    "amber": '<polygon points="64,42 71,57 87,58 74,68 79,85 64,76 49,85 54,68 41,58 57,57"/>',
}


def layered(shape, cols, glyph, extra=""):
    """Soft-clay recipe: tinted blur shadow > depth > base gradient > bevel shade > rim light > gloss > glyph > sparkle."""
    l, m, d = cols
    return svg(
        f'<defs><linearGradient id="base" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{l}"/>'
        f'<stop offset=".45" stop-color="{m}"/><stop offset="1" stop-color="{d}"/></linearGradient>'
        f'<radialGradient id="bevel" cx="50%" cy="35%" r="70%"><stop offset=".6" stop-color="#000" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="#000" stop-opacity=".25"/></radialGradient>'
        f'<linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".6"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="clip"><path d="{shape}"/></clipPath>'
        f'<filter id="sh" x="-40%" y="-40%" width="180%" height="190%"><feGaussianBlur stdDeviation="6"/></filter></defs>'
        f'<path d="{shape}" fill="{d}" opacity=".6" filter="url(#sh)" transform="translate(0 8) scale(.94) translate(4 4)"/>'
        f'<path d="{shape}" fill="{d}" transform="translate(0 4)"/>'
        f'<path d="{shape}" fill="url(#base)"/>'
        f'<g clip-path="url(#clip)"><path d="{shape}" fill="url(#bevel)"/>'
        f'<path d="{shape}" fill="none" stroke="#fff" stroke-width="3" opacity=".45" transform="translate(0 -4)"/>'
        f'<ellipse cx="64" cy="30" rx="44" ry="22" fill="url(#gloss)"/></g>'
        f'<g fill="{d}" opacity=".35" transform="translate(0 2)">{glyph}</g>'
        f'<g fill="#fff" opacity=".9">{glyph}</g>{extra}'
        '<path d="M96 22 l3 8 8 3 -8 3 -3 8 -3 -8 -8 -3 8 -3 z" fill="#fff"/>')


def box(c):
    return layered(BOX, COLORS[c], GLYPHS[c])


def ball(c):
    return layered(BALL, COLORS[c], GLYPHS[c])


def charged(c):  # Blast piece: ball + outer energy glow
    l = COLORS[c][0]
    glow = (f'<circle cx="64" cy="64" r="60" fill="none" stroke="{l}" stroke-width="5" opacity=".9" '
            f'stroke-dasharray="14 8"/>')
    return layered(BALL, COLORS[c], GLYPHS[c], glow).replace("<defs>", '<defs><filter id="b"><feGaussianBlur stdDeviation="3"/></filter>', 1)


def button(fill_l, fill_d, label, w=360, h=120):
    """Glossy chunky game button: dark base for 3D depth, face gradient, top gloss band."""
    return svg(
        f'<defs><linearGradient id="f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{fill_l}"/>'
        f'<stop offset="1" stop-color="{fill_d}"/></linearGradient></defs>'
        f'<filter id="sh" x="-20%" y="-40%" width="140%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>'
        f'<rect x="16" y="20" width="{w-32}" height="{h-24}" rx="36" fill="{fill_d}" opacity=".6" filter="url(#sh)"/>'
        f'<rect x="0" y="5" width="{w}" height="{h-14}" rx="36" fill="{fill_d}"/>'
        f'<rect x="0" y="0" width="{w}" height="{h-16}" rx="36" fill="url(#f)"/>'
        f'<rect x="1" y="1" width="{w-2}" height="{h-18}" rx="35" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width="2"/>'
        f'<rect x="20" y="6" width="{w-40}" height="30" rx="15" fill="#fff" opacity=".22"/>'
        f'<text x="{w/2}" y="{h/2+8}" text-anchor="middle" font-family="Poppins, sans-serif" font-weight="800" letter-spacing="-0.5" '
        f'font-size="48" fill="#1a1020" opacity=".5" dy="4">{label}</text>'
        f'<text x="{w/2}" y="{h/2+8}" text-anchor="middle" font-family="Poppins, sans-serif" font-weight="800" letter-spacing="-0.5" '
        f'font-size="48" fill="#fff" stroke="#1a1020" stroke-width="2">{label}</text>', w, h)


def panel(w=600, h=400):
    """Glass modal panel over graphite."""
    return svg(
        '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a5060" stop-opacity=".95"/>'
        '<stop offset="1" stop-color="#1b1e26" stop-opacity=".95"/></linearGradient></defs>'
        f'<rect x="0" y="10" width="{w}" height="{h-10}" rx="40" fill="#000" opacity=".35"/>'
        f'<rect x="0" y="0" width="{w}" height="{h-10}" rx="40" fill="url(#g)" stroke="#fff" stroke-opacity=".18" stroke-width="2"/>'
        f'<rect x="6" y="6" width="{w-12}" height="{h-22}" rx="34" fill="none" stroke="#fff" stroke-opacity=".15" stroke-width="2"/>'
        f'<path d="M40 6 H{w-40} Q{w-6} 6 {w-6} 40 V90 Q{w/2} 60 6 110 V40 Q6 6 40 6 Z" fill="#fff" opacity=".07"/>', w, h)


def crate():
    planks = "".join(f'<rect x="14" y="{y}" width="100" height="22" fill="#b97a3c" stroke="#6b3f17" stroke-width="2"/>'
                     for y in (14, 38, 62, 86))
    return svg(f'{SHADOW}<rect x="10" y="10" width="108" height="102" rx="10" fill="#8a5424"/>{planks}'
               '<path d="M18 18 L110 104 M110 18 L18 104" stroke="#6b3f17" stroke-width="10" stroke-linecap="round"/>'
               '<path d="M18 18 L110 104 M110 18 L18 104" stroke="#d29a5a" stroke-width="5" stroke-linecap="round"/>'
               + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#3a2410"/>' for x in (20, 108) for y in (20, 102)))


def potion():
    return svg('<defs><linearGradient id="p" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7ad9"/>'
               '<stop offset="1" stop-color="#8a1fd6"/></linearGradient></defs>'
               '<rect x="50" y="8" width="28" height="14" rx="4" fill="#c28a4a"/>'
               '<path d="M54 22 H74 V40 Q104 52 104 82 A40 40 0 0 1 24 82 Q24 52 54 40 Z" fill="#ffffff22" stroke="#fff" stroke-opacity=".7" stroke-width="3"/>'
               '<path d="M30 76 Q64 64 98 76 A34 34 0 0 1 30 76 Z" fill="url(#p)"/>'
               '<path d="M30 76 Q64 64 98 76 A34 36 0 0 1 30 76" fill="url(#p)" transform="translate(0 2)"/>'
               '<ellipse cx="46" cy="60" rx="7" ry="14" fill="#fff" opacity=".6"/>'
               '<circle cx="74" cy="90" r="4" fill="#fff" opacity=".7"/><circle cx="62" cy="98" r="2.5" fill="#fff" opacity=".7"/>')


def heart():
    return svg(f'<defs>{grad("g", "#ffb3c7", "#ff3b6b", "#8a0026")}</defs>'
               '<path d="M64 112 C20 80 8 56 14 38 C22 14 52 12 64 34 C76 12 106 14 114 38 C120 56 108 80 64 112 Z" fill="url(#g)" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>'
               '<ellipse cx="38" cy="38" rx="12" ry="7" fill="#fff" opacity=".6" transform="rotate(-30 38 38)"/>')


def launcher():
    return svg('<defs><linearGradient id="m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f6fa"/>'
               '<stop offset=".5" stop-color="#8c94a3"/><stop offset="1" stop-color="#3b414d"/></linearGradient></defs>'
               '<path d="M64 10 L108 70 Q112 92 92 100 H36 Q16 92 20 70 Z" fill="url(#m)" stroke="#1d2129" stroke-width="3"/>'
               '<circle cx="64" cy="70" r="16" fill="#1d2129"/><circle cx="64" cy="70" r="10" fill="#7ff3ff"/>'
               '<circle cx="60" cy="66" r="3" fill="#fff"/>')


def cell():  # inset grid cell
    return svg('<defs><linearGradient id="c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0f14"/>'
               '<stop offset="1" stop-color="#2a2f3a"/></linearGradient></defs>'
               '<rect x="4" y="4" width="120" height="120" rx="20" fill="url(#c)"/>'
               '<rect x="5" y="5" width="118" height="118" rx="19" fill="none" stroke="#fff" stroke-opacity=".08" stroke-width="2"/>')


def board():  # graphite board with soft metallic rim
    return svg('<defs><linearGradient id="r" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d9dde5"/>'
               '<stop offset=".5" stop-color="#5b616e"/><stop offset="1" stop-color="#c2c7d1"/></linearGradient>'
               '<radialGradient id="f" cx="50%" cy="40%" r="70%"><stop offset="0" stop-color="#3a3f4b"/>'
               '<stop offset="1" stop-color="#16181e"/></radialGradient></defs>'
               '<rect x="0" y="0" width="1024" height="1024" rx="72" fill="url(#r)"/>'
               '<rect x="16" y="16" width="992" height="992" rx="60" fill="url(#f)"/>', 1024, 1024)


def shard():  # Pulse Shard currency
    return svg(f'<defs>{grad("g", "#e0fbff", "#7f9bff", "#3a1fa8")}</defs>'
               '<path d="M64 6 L104 48 L64 122 L24 48 Z" fill="url(#g)" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>'
               '<path d="M64 6 L64 122 M24 48 H104" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>'
               '<path d="M64 6 L44 48 L64 30 Z" fill="#fff" opacity=".5"/>')


def star(on=True):
    fill = ('url(#g)', '#3b414d')[not on]
    pts = "64,8 80,46 120,48 88,74 100,114 64,92 28,114 40,74 8,48 48,46"
    return svg(f'<defs>{grad("g", "#fff6b0", "#ffc21f", "#a35a00")}</defs>'
               f'<polygon points="{pts}" fill="{fill}" stroke="#fff" stroke-opacity=".5" stroke-width="3" stroke-linejoin="round"/>')


if __name__ == "__main__":
    files = {f"piece_box_{c}.svg": box(c) for c in COLORS}
    files |= {f"piece_ball_{c}.svg": ball(c) for c in COLORS}
    files |= {f"piece_charged_{c}.svg": charged(c) for c in COLORS}
    files |= {"crate.svg": crate(), "life_potion.svg": potion(), "life_heart.svg": heart(),
              "launcher.svg": launcher(), "cell_inset.svg": cell(), "board_graphite.svg": board(),
              "shard.svg": shard(), "star_on.svg": star(True), "star_off.svg": star(False),
              "btn_play.svg": button("#9dff6a", "#2f9a12", ""),
              "btn_secondary.svg": button("#7fd8ff", "#1d6fd4", ""), "panel_glass.svg": panel()}

    os.makedirs(OUT, exist_ok=True)
    for name, data in files.items():
        os.makedirs(os.path.join(OUT, folder_for(name)), exist_ok=True)
        open(os.path.join(OUT, folder_for(name), name), "w").write(data)

    print(f"wrote {len(files)} assets to {os.path.abspath(OUT)}")
