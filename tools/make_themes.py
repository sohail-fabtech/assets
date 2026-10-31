# Edge Pulse color worlds × piece styles. Run: python3 tools/make_themes.py
# Slot i always carries the same symbol (drop, heart, leaf, star) so colorblind players keep their cues in every world.
import json, os
from layout import folder_for
from make_assets import svg, layered, BOX, BALL, GLYPHS

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
SYMBOLS = [GLYPHS[k] for k in ("cyan", "magenta", "lime", "amber")]

# world: 4 piece colours (light, mid, dark) + board (top, bottom, rim light, rim dark) + UI accent
WORLDS = {
    "graphite": {"pieces": [("#7ff3ff", "#14b8d4", "#06576b"), ("#ff9ee8", "#e83fb8", "#6e0f55"),
                            ("#d6ff8a", "#7fd420", "#2f5a07"), ("#ffe08a", "#ffa51f", "#7a3d00")],
                 "board": ("#3a3f4b", "#16181e", "#d9dde5", "#5b616e"), "accent": "#7ff3ff"},
    "aurora": {"pieces": [("#7dffc8", "#19c98f", "#065c44"), ("#9fd8ff", "#3a8cff", "#123c8a"),
                          ("#d6b3ff", "#8e4dff", "#3a1680"), ("#ffb3e6", "#ff4fb8", "#7a0f55")],
               "board": ("#1d3a4a", "#0a1420", "#9ff5d8", "#2a5a6a"), "accent": "#7dffc8"},
    "orchid_dusk": {"pieces": [("#f0b3ff", "#b84dff", "#4f1673"), ("#ffb8c8", "#ff5c86", "#7a1430"),
                               ("#ffd2b0", "#ff8a4d", "#7a3010"), ("#c8c8ff", "#6f6fff", "#25256e")],
                    "board": ("#3a2448", "#140a1e", "#f0c8ff", "#5a3a6e"), "accent": "#f0b3ff"},
    "lagoon": {"pieces": [("#a8fff4", "#1fd1c1", "#05605a"), ("#ffc0a8", "#ff6b4a", "#7a200e"),
                          ("#fff0b0", "#f2c230", "#7a5a00"), ("#a8c8ff", "#2f6bff", "#0e2a7a")],
               "board": ("#0f4a58", "#06202a", "#b8fff0", "#1a6a70"), "accent": "#a8fff4"},
    "ember_glow": {"pieces": [("#ffc4a0", "#ff5a1f", "#7a1600"), ("#ffe9a0", "#ffb300", "#7a4a00"),
                              ("#ff9ab0", "#e0204f", "#6e0020"), ("#b8ffd8", "#2fd47f", "#0b5a30")],
                   "board": ("#4a2418", "#1a0a06", "#ffd0a0", "#7a3a20"), "accent": "#ffb300"},
    "sapphire": {"pieces": [("#a8c4ff", "#2a5cff", "#0c1f7a"), ("#d8fbff", "#5fd8f0", "#0f5c70"),
                            ("#dcb0ff", "#9a3dff", "#3c0f7a"), ("#f8ffa0", "#d4e020", "#5a6000")],
                 "board": ("#1a2a5a", "#080e24", "#c8d8ff", "#2a3a7a"), "accent": "#a8c4ff"},
}

PILLOW = "M64 12 C98 4 124 30 116 64 C124 98 98 124 64 116 C30 124 4 98 12 64 C4 30 30 4 64 12 Z"


def sym(g, scale=1.0, cx=64, cy=64):
    return f'<g transform="translate({cx - 64 * scale} {cy - 64 * scale}) scale({scale})">{g}</g>'


def gem(cols, g):
    """Faceted hexagon: outer facets lit top→bottom, flat table on top, symbol engraved."""
    l, m, d = cols
    o = [(64, 6), (116, 35), (116, 93), (64, 122), (12, 93), (12, 35)]
    t = [(64 + (x - 64) * .52, 62 + (y - 64) * .52) for x, y in o]
    shades = [l, l, m, d, d, m]  # top-right, right, bottom-right, bottom-left, left, top-left facets
    facets = "".join(
        f'<polygon points="{o[i][0]},{o[i][1]} {o[(i + 1) % 6][0]},{o[(i + 1) % 6][1]} '
        f'{t[(i + 1) % 6][0]:.1f},{t[(i + 1) % 6][1]:.1f} {t[i][0]:.1f},{t[i][1]:.1f}" fill="{shades[i]}"/>' for i in range(6))
    P = lambda pts: " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return svg(
        f'<defs><filter id="sh" x="-40%" y="-40%" width="180%" height="190%"><feGaussianBlur stdDeviation="6"/></filter>'
        f'<linearGradient id="tb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{l}"/><stop offset="1" stop-color="{m}"/></linearGradient></defs>'
        f'<polygon points="{P(o)}" fill="{d}" opacity=".55" filter="url(#sh)" transform="translate(0 8)"/>'
        f'{facets}<polygon points="{P(t)}" fill="url(#tb)"/>'
        f'<polygon points="{P(o)}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="2" stroke-linejoin="round"/>'
        f'<polygon points="{P(t[:3] + [(64, 62)])}" fill="#fff" opacity=".22"/>'
        f'<g fill="{d}" opacity=".35" transform="translate(0 2)">{sym(g, .62, 64, 62)}</g>'
        f'<g fill="#fff" opacity=".85">{sym(g, .62, 64, 62)}</g>'
        '<path d="M92 24 l2.5 7 7 2.5 -7 2.5 -2.5 7 -2.5 -7 -7 -2.5 7 -2.5 z" fill="#fff"/>')


def bubble(cols, g):
    """Glass bubble: see-through core, coloured rim, big window highlight, tinted symbol inside."""
    l, m, d = cols
    return svg(
        f'<defs><filter id="sh" x="-40%" y="-40%" width="180%" height="190%"><feGaussianBlur stdDeviation="6"/></filter>'
        f'<radialGradient id="b" cx="45%" cy="40%" r="62%"><stop offset="0" stop-color="{l}" stop-opacity=".25"/>'
        f'<stop offset=".7" stop-color="{m}" stop-opacity=".6"/><stop offset="1" stop-color="{d}" stop-opacity=".95"/></radialGradient></defs>'
        f'<circle cx="64" cy="72" r="50" fill="{m}" opacity=".4" filter="url(#sh)"/>'
        f'<circle cx="64" cy="64" r="56" fill="url(#b)"/>'
        f'<circle cx="64" cy="64" r="54.5" fill="none" stroke="{l}" stroke-width="3" opacity=".8"/>'
        f'<g fill="{m}">{sym(g, .8)}</g><g fill="#fff" opacity=".35">{sym(g, .8, 63, 62)}</g>'
        '<path d="M30 46 A38 38 0 0 1 62 20" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".85"/>'
        '<circle cx="28" cy="60" r="4.5" fill="#fff" opacity=".8"/>'
        f'<path d="M40 104 A44 44 0 0 0 98 96" fill="none" stroke="{l}" stroke-width="4" stroke-linecap="round" opacity=".6"/>')


STYLES = {"box": lambda c, g: layered(BOX, c, g), "ball": lambda c, g: layered(BALL, c, g),
          "pillow": lambda c, g: layered(PILLOW, c, g), "gem": gem, "bubble": bubble}


def board(top, bottom, rl, rd):
    return svg(f'<defs><linearGradient id="r" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{rl}"/>'
               f'<stop offset=".5" stop-color="{rd}"/><stop offset="1" stop-color="{rl}"/></linearGradient>'
               f'<radialGradient id="f" cx="50%" cy="35%" r="75%"><stop offset="0" stop-color="{top}"/>'
               f'<stop offset="1" stop-color="{bottom}"/></radialGradient></defs>'
               '<rect width="1024" height="1024" rx="88" fill="url(#r)"/>'
               '<rect x="14" y="14" width="996" height="996" rx="76" fill="url(#f)"/>'
               '<rect x="15" y="15" width="994" height="994" rx="75" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="2"/>',
               1024, 1024, 0)


def cell(bottom):
    return svg(f'<rect x="4" y="4" width="120" height="120" rx="28" fill="#000" opacity=".28"/>'
               f'<rect x="4" y="6" width="120" height="118" rx="28" fill="none" stroke="#fff" stroke-opacity=".07" stroke-width="2"/>', 128, 128, 0)


def write(f, data):
    d = os.path.join(OUT, folder_for(f)); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f), "w").write(data)
    return f"{folder_for(f)}/{f}"


if __name__ == "__main__":
    out, n = {}, 0
    for w, t in WORLDS.items():
        files = {st: [write(f"th_{w}_{st}_{i}.svg", fn(cols, SYMBOLS[i])) for i, cols in enumerate(t["pieces"])] for st, fn in STYLES.items()}
        n += 4 * len(STYLES)
        out[w] = {"pieces": [c[1] for c in t["pieces"]], "light": [c[0] for c in t["pieces"]], "board": t["board"], "accent": t["accent"],
                  "boardFile": write(f"thb_{w}_board.svg", board(*t["board"])), "cellFile": write(f"thb_{w}_cell.svg", cell(t["board"][1])),
                  "files": files}
        n += 2
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "data", "themes.json"), "w"), indent=1)
    print(f"wrote {n} theme assets + data/themes.json")
