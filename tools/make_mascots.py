# Animated SVG mascots (self-contained SMIL — they animate anywhere an <img> shows them):
#   body morph (same-structure paths), eye blink, wandering pupils, mouth squish.
#   assets/ui/mascots/masc_<colour>.svg + masc_splat_<colour>.svg (paint splat used by the Play transition)
# Run: python3 make_mascots.py
import math, os, random
from layout import folder_for

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
COLS = {"cyan": ("#14b8d4", "#0a7a96"), "magenta": ("#e83fb8", "#a01a7a"), "lime": ("#7fd420", "#4a9a0a"), "amber": ("#ffa51f", "#c06a00")}
INK = "#160a3a"


def blob(seed, n=10, r=88, wob=11, cx=100, cy=104):
    """Smooth closed blob with exactly n cubic segments (so SMIL can morph between seeds)."""
    rnd = random.Random(seed)
    pts = [(cx + (r + rnd.uniform(-wob, wob)) * math.cos(a), cy + (r + rnd.uniform(-wob, wob)) * math.sin(a))
           for a in (i / n * 2 * math.pi for i in range(n))]
    d = f"M{(pts[0][0] + pts[-1][0]) / 2:.1f} {(pts[0][1] + pts[-1][1]) / 2:.1f}"
    for i in range(n):  # quadratic-through-midpoints as cubic → smooth, same command count
        p, q = pts[i], pts[(i + 1) % n]
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        d += f" C{p[0]:.1f} {p[1]:.1f} {p[0]:.1f} {p[1]:.1f} {mx:.1f} {my:.1f}"
    return d + " Z"


def mascot(name, seed, mouth="smile"):
    col, dk = COLS[name]
    shapes = [blob(seed + k) for k in range(3)] + [blob(seed)]
    dur = 5 + seed % 3
    eye = lambda x, delay: (f'<g transform="translate({x} 86)"><ellipse rx="17" ry="20" fill="#fff">'
                            f'<animate attributeName="ry" values="20;20;1.5;20" keyTimes="0;.94;.97;1" dur="4.2s" begin="{delay}s" repeatCount="indefinite"/></ellipse>'
                            '<g><animateTransform attributeName="transform" type="translate" values="0 0;5 2;-4 3;-5 -2;3 -3;0 0" dur="5.6s" repeatCount="indefinite"/>'
                            f'<circle r="8.5" fill="{INK}"/><circle cx="-3" cy="-3" r="3" fill="#fff"/></g></g>')
    m = (f'<ellipse cx="100" cy="128" rx="9" ry="11" fill="{INK}"><animate attributeName="ry" values="11;7;11" dur="1.8s" repeatCount="indefinite"/></ellipse>' if mouth == "o"
         else f'<path d="M84 122 Q100 138 116 122" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round">'
              '<animate attributeName="d" values="M84 122 Q100 138 116 122;M84 124 Q100 134 116 124;M84 122 Q100 138 116 122" dur="2.6s" repeatCount="indefinite"/></path>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 210" width="200" height="210">'
            f'<path fill="{dk}" transform="translate(0 8)" d="{shapes[0]}"><animate attributeName="d" values="{";".join(shapes)}" dur="{dur}s" repeatCount="indefinite"/></path>'
            f'<path fill="{col}" d="{shapes[0]}"><animate attributeName="d" values="{";".join(shapes)}" dur="{dur}s" repeatCount="indefinite"/></path>'
            f'<path fill="#fff" opacity=".22" d="M52 60 Q70 34 104 32" stroke="#fff" stroke-width="10" stroke-linecap="round"/>'
            f'<g>{eye(80, seed % 3 * .6)}{eye(120, seed % 3 * .6)}</g>{m}'
            '<animateTransform attributeName="transform" type="scale" values="1 1;1.02 .98;1 1" dur="2.2s" repeatCount="indefinite" additive="sum"/>'
            '</svg>')


def splat(name):
    """Paint splat: wobbly core + drips, used scaled up to cover the screen."""
    col, _ = COLS[name]
    rnd = random.Random(name)
    core = blob(hash(name) % 1000, n=14, r=70, wob=16, cx=100, cy=100)
    drops = "".join(f'<circle cx="{100 + d * math.cos(a):.0f}" cy="{100 + d * math.sin(a):.0f}" r="{rnd.uniform(4, 11):.0f}" fill="{col}"/>'
                    for a, d in ((rnd.uniform(0, 6.28), rnd.uniform(82, 98)) for _ in range(9)))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200"><path fill="{col}" d="{core}"/>{drops}</svg>'


if __name__ == "__main__":
    for i, (name, mouth) in enumerate((("cyan", "smile"), ("magenta", "o"), ("lime", "smile"), ("amber", "o"))):
        for f, data in ((f"masc_{name}.svg", mascot(name, i * 7 + 3, mouth)), (f"masc_splat_{name}.svg", splat(name))):
            d = os.path.join(OUT, folder_for(f)); os.makedirs(d, exist_ok=True)
            open(os.path.join(d, f), "w").write(data)
    print("wrote 4 animated mascots + 4 splats")
