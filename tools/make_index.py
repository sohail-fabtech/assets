# Builds assets/index.html: one preview of every asset, grouped by category. Run after the generators:
#   python3 make_assets.py && python3 make_ui.py && python3 make_themes.py && python3 make_index.py
import json, os
from layout import CATEGORIES

A = os.path.join(os.path.dirname(__file__), "..", "assets")
WIDE = ("board_", "sea_spring_board", "sea_summer_board", "sea_autumn_board", "sea_winter_board", "panel_", "ribbon", "btn_play", "btn_secondary", "progress_", "hud_pill")
nice = lambda n: n[:-4].replace("_", " ")

sections, nav = [], []
def cards(rel):
    files = sorted(f for f in os.listdir(os.path.join(A, rel)) if f.endswith(".svg"))
    return files, "".join(f'<figure class="{"wide" if f.startswith(WIDE) else ""}" data-path="{rel}/{f}" title="Click to copy path">'
                          f'<img src="{rel}/{f}" loading="lazy"><figcaption>{nice(f)}</figcaption></figure>' for f in files)


for folder, (title, _) in CATEGORIES.items():
    body, count = "", 0
    for root, dirs, _ in sorted(os.walk(os.path.join(A, folder))):  # nested folders get their own sub-heading
        dirs.sort()
        rel = os.path.relpath(root, A)
        files, html_cards = cards(rel)
        if not files: continue
        count += len(files)
        depth = rel.count("/")
        label = rel.split("/", 1)[1].replace("/", " › ") if depth else ""
        body += (f'<h3 class="d{depth}">{label} <span>{len(files)}</span></h3>' if label else "") + f'<div class="grid">{html_cards}</div>'
    nav.append(f'<a href="#{folder}">{title} <b>{count}</b></a>')
    sections.append(f'<section id="{folder}"><h2>{title} <span>{folder}/ · {count}</span></h2>{body}</section>')

themes = json.load(open(os.path.join(A, "themes", "themes.json")))
styles = ["box", "ball", "pillow", "gem", "bubble"]
rows, total = [], 0
for w, t in themes.items():
    pieces = "".join(f'<img src="themes/{w}/piece_{s}_{i}.svg" data-path="themes/{w}/piece_{s}_{i}.svg" title="{s} {i}" loading="lazy">'
                     for s in styles for i in range(4))
    dots = "".join(f'<i style="background:{c}"></i>' for c in t["pieces"])
    total += len(styles) * 4 + 2
    rows.append(f'<div class="world" style="--b0:{t["board"][0]};--b1:{t["board"][1]}"><div class="wh"><b>{w.replace("_", " ")}</b>{dots}</div>'
                f'<div class="wp"><img class="wb" src="themes/{w}/board.svg">{pieces}</div></div>')
nav.append(f'<a href="#themes">Color worlds <b>{total}</b></a>')
LIVE = [("bombs-live", "Bombs (live)", "bombs/index.html", "Lit fuses with live sparks · tap a bomb to detonate · Blast all", 900),
        ("seasons", "Seasons", "seasons/index.html", "Four aura seasons · current season is live · tap pieces", 1000),
        ("events", "Events", "events/index.html", "Live event prize path + yearly calendar · tap Play a run", 1000),
        ("vault", "Piece Vault", "collection/index.html", "Unlock pieces with Shards · tap a silhouette", 900),
        ("board", "Theme board", "themes/index.html", "Switch color worlds and piece styles on a live 7×7 board", 760),
        ("showcase", "Animated showcase", "motion/showcase.html", "Every asset with idle loops · tap anything", 900),
        ("demo", "Motion spec demo", "motion/demo.html", "Clear, fall, fire, life loss, score, combo, panel timings", 640)]
sections.append(f'<section id="themes"><h2>Color worlds <span>themes/ · {len(themes)} worlds × {len(styles)} styles</span></h2>{"".join(rows)}</section>')
for sid, title, src, sub, h in LIVE:  # interactive pages embedded so this one page shows everything
    nav.append(f'<a href="#{sid}">{title}</a>')
    sections.append(f'<section id="{sid}"><h2>{title} <span>{sub}</span></h2>'
                    f'<iframe src="{src}" loading="lazy" title="{title}" style="height:{h}px"></iframe></section>')

html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Edge Pulse · Asset library</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;800;900&display=swap" rel="stylesheet">
<style>
body{{margin:0;background:#12141a;color:#d6dae3;font:600 14px/1.45 Poppins,sans-serif}}
header{{position:sticky;top:0;z-index:2;background:#12141ae6;backdrop-filter:blur(14px);padding:16px 28px 12px;border-bottom:1px solid #ffffff10}}
h1{{font:900 26px/1.2 Poppins;letter-spacing:-.02em;margin:0 0 10px;display:flex;gap:16px;align-items:center}}
h1 input{{margin-left:auto;font:600 14px Poppins;color:#fff;background:#ffffff10;border:1px solid #ffffff20;border-radius:99px;padding:8px 16px;width:220px}}
nav{{display:flex;flex-wrap:wrap;gap:6px}}nav a{{color:#d6dae3;text-decoration:none;font-size:13px;padding:5px 12px;border-radius:99px;background:#ffffff0c}}
nav a:hover{{background:#ffffff1c}}nav b{{opacity:.5;font-weight:800}}
section{{padding:22px 28px 8px;scroll-margin-top:110px}}
h2{{font:800 20px/1.2 Poppins;letter-spacing:-.01em;margin:0 0 14px}}h2 span{{font-size:13px;font-weight:600;opacity:.5;margin-left:8px}}h2 a{{color:#7ff3ff}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:12px}}
figure{{margin:0;padding:14px 10px 8px;border-radius:18px;background:radial-gradient(120% 100% at 50% 0,#2e333f,#1b1e26);cursor:pointer;text-align:center;transition:transform .16s}}
figure:hover{{transform:translateY(-3px)}}figure.wide{{grid-column:span 2}}
figure img{{height:88px;max-width:100%;object-fit:contain}}figcaption{{font-size:12px;opacity:.65;margin-top:6px}}
.world{{border-radius:22px;padding:14px;margin-bottom:12px;background:radial-gradient(120% 120% at 20% 0,var(--b0),var(--b1))}}
.wh{{display:flex;gap:6px;align-items:center;margin-bottom:10px;text-transform:capitalize}}.wh b{{font:800 16px Poppins;margin-right:6px}}
.wh i{{width:14px;height:14px;border-radius:50%}}
.wp{{display:grid;grid-template-columns:120px repeat(20,minmax(36px,1fr));gap:4px;align-items:center}}.wp img{{width:100%;cursor:pointer}}
h3{{font:800 14px Poppins;margin:16px 0 8px;text-transform:capitalize;opacity:.8}}h3 span{{opacity:.5;font-weight:600}}h3.d1{{font-size:16px;opacity:1}}
iframe{{width:100%;border:0;border-radius:22px;background:#16181e;display:block;margin-bottom:12px}}
#toast{{position:fixed;bottom:24px;left:50%;translate:-50%;background:#fff;color:#12141a;padding:8px 16px;border-radius:99px;opacity:0;transition:opacity .2s}}
@media (max-width:900px){{.wp{{grid-template-columns:repeat(10,1fr)}}.wb{{grid-column:span 10;width:120px}}}}
</style></head><body>
<header><h1>Edge Pulse · Asset library <input id="q" placeholder="Filter by name…" aria-label="Filter assets"></h1><nav>{"".join(nav)}</nav></header>
{"".join(sections)}
<div id="toast"></div>
<script>
const toast = t => {{ const e = document.getElementById('toast'); e.textContent = t; e.style.opacity = 1; clearTimeout(e.t); e.t = setTimeout(() => e.style.opacity = 0, 1200); }};
document.addEventListener('click', e => {{ const p = e.target.closest('[data-path]'); if (p) navigator.clipboard?.writeText('assets/' + p.dataset.path).then(() => toast('Copied assets/' + p.dataset.path)); }});
document.getElementById('q').oninput = e => {{ const q = e.target.value.toLowerCase();
  document.querySelectorAll('figure').forEach(f => f.hidden = q && !f.dataset.path.includes(q.replace(/ /g, '_'))); }};
</script></body></html>'''
open(os.path.join(A, "index.html"), "w").write(html)
print(f"wrote assets/index.html")
