# Release gate for the asset library. Exits non-zero on any failure. Run: python3 check_assets.py (also last step of build_all.sh)
import glob, json, os, re, sys, xml.dom.minidom
from level_themes import THEMES, FONTS
from level_themes import contrast

A = os.path.join(os.path.dirname(__file__), "..", "assets")
os.chdir(A)
errors = []

# 1. every referenced file exists (data manifests + literal paths in pages)
def walk(o, where):
    if isinstance(o, dict): [walk(v, where) for v in o.values()]
    elif isinstance(o, list): [walk(v, where) for v in o]
    elif isinstance(o, str) and o.endswith((".svg", ".ttf")) and "{" not in o and not os.path.exists(o):
        errors.append(f"missing {o} (from {where})")
for f in glob.glob("data/*.json"):
    walk(json.load(open(f)), f)
for f in glob.glob("pages/*.html"):
    for m in re.findall(r'"\.\./([^"$]+\.(?:svg|json|css|js))"', open(f).read()):
        if not os.path.exists(m): errors.append(f"missing {m} (from {f})")

# 2. every SVG is well-formed XML
svgs = glob.glob("**/*.svg", recursive=True)
for f in svgs:
    try: xml.dom.minidom.parse(f)
    except Exception as e: errors.append(f"bad svg {f}: {e}")

# 3. label contrast on coloured buttons (labels are 22px/800 = WCAG "large text" → 3:1 minimum)
for tid, t in THEMES.items():
    p = t["palette"]
    for role, fg, bg in (("primary", p["onPrimary"], p["primary"]), ("secondary", p["onSecondary"], p["secondary"]), ("danger", p["onDanger"], p["danger"])):
        r = contrast(fg, p["labelBg"] or bg)  # neon labels sit on dark glass, not on the tube colour
        if r < 3: errors.append(f"contrast {tid} {role}: {r:.2f}:1 (< 3:1) — adjust palette in level_themes.py")
    for what, fg, bg in (("ghost on background", p["ghost"], p["bg"]), ("label on surface", p["onSurface"], p["surface"]), ("text on background", p["text"], p["bg"])):
        if contrast(fg, bg) < 3: errors.append(f"contrast {tid} {what}: {contrast(fg, bg):.2f}:1 (< 3:1)")

# 4. every theme is complete
kit = json.load(open("data/ui-kit.json"))
for tid in THEMES:
    for c, states in kit["controls"].items():
        for s in states:
            f = kit["pattern"].replace("{theme}", tid).replace("{control}", c).replace("{state}", s)
            if not os.path.exists(f): errors.append(f"incomplete theme {tid}: {f}")
levels = json.load(open("data/levels.json"))
for tid, t in THEMES.items():
    lv = levels.get(tid)
    if not lv: errors.append(f"incomplete theme {tid}: no level data"); continue
    if len(lv["pieces"]) != 4: errors.append(f"{tid}: needs 4 pieces")
    for o in lv["obstacles"]:
        if len(o["states"]) != o["hits"]: errors.append(f"{tid}: obstacle {o['id']} has {len(o['states'])} states for {o['hits']} hits")

# 4b. every world has its scene, hero collectible and chrome tone set
chrome = json.load(open("data/chrome.json"))
for tid, lv in levels.items():
    if tid != "graphite" and not lv.get("scene"): errors.append(f"{tid}: no world scene")
    goal = lv.get("goal", {}).get("item")
    if not any(c["id"] == goal and c.get("hero") for c in lv["collectibles"]): errors.append(f"{tid}: goal item {goal} has no hero render")
    for part in ("close", "pill", "frame", "ribbon", "fill", "header", "tag", "corner", "burst", "socket", "curved", "wave", "bow"):
        if part not in chrome["tones"].get(tid, {}): errors.append(f"{tid}: chrome part {part} missing")

# 5. every bundled font has its licence beside it
for fam, (path, _) in FONTS.items():
    if not os.path.exists(f"fonts/{path}"): errors.append(f"font file missing: {path}")
    if not os.path.exists(f"fonts/{path.split('/')[0]}/OFL.txt"): errors.append(f"licence missing for {fam}")

print(f"checked {len(svgs)} svgs, {len(THEMES)} themes, {len(FONTS)} fonts")
if errors:
    print("\n".join("✗ " + e for e in errors[:60])); print(f"{len(errors)} problem(s)"); sys.exit(1)
print("✓ all checks passed")
