# Themed Buttons & Controls kit: 41 controls × every theme in level_themes.THEMES.
#   assets/buttons/<theme>/ui_<theme>_<control>_<state>.svg  + data/ui-kit.json + assets/motion/themes.css
# Labels are never baked in: the game draws them live in the theme's font (crisp, localisable).
import itertools, json, os
from level_themes import THEMES, FONTS, FONT_SOURCE, lum, contrast
from make_ui import glyph
from layout import folder_for

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
_ids = itertools.count()


# ---- colour helpers -------------------------------------------------------------------------------
def rgb(h):
    h = h.lstrip("#")
    if len(h) == 3: h = "".join(ch * 2 for ch in h)  # #fff → #ffffff
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]
def hexc(c): return "#" + "".join(f"{max(0, min(255, round(v))):02x}" for v in c)
def mix(a, b, t): return hexc([x + (y - x) * t for x, y in zip(rgb(a), rgb(b))])
def doc(w, h, body, pad=12):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w + 2 * pad} {h + 2 * pad}" '
            f'width="{w + 2 * pad}" height="{h + 2 * pad}">{body}</svg>')


FX = ('<filter id="sh" x="-30%" y="-40%" width="160%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'
      '<filter id="gs" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2"/></filter>'
      '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>'
      '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2"/>'
      '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .7 0"/></filter>')

RADIUS = {"brass": .28, "crystal": .22, "wood": .36, "neon": .4, "lava": .42}  # fraction of height; default = full pill


def rr(x, y, w, h, r):
    return f"M{x + r} {y} H{x + w - r} Q{x + w} {y} {x + w} {y + r} V{y + h - r} Q{x + w} {y + h} {x + w - r} {y + h} H{x + r} Q{x} {y + h} {x} {y + h - r} V{y + r} Q{x} {y} {x + r} {y} Z"


def material(mat, d, x, y, w, h, l, m, dk):
    """Surface detail clipped inside a face — this is what makes each theme feel physically different."""
    if mat == "lava":
        cr = f"M{x + w * .12} {y + h * .7} L{x + w * .3} {y + h * .55} L{x + w * .42} {y + h * .8} L{x + w * .6} {y + h * .6} L{x + w * .78} {y + h * .78} L{x + w * .9} {y + h * .62}"
        return (f'<path d="{cr}" stroke="#ffd27a" stroke-width="5" fill="none" filter="url(#glow)" opacity=".9"/>'
                f'<path d="{cr}" stroke="#fff3c4" stroke-width="1.6" fill="none"/>'
                f'<path d="{d}" fill="none" stroke="#1a0402" stroke-opacity=".55" stroke-width="6"/>')
    if mat == "wood":
        return "".join(f'<path d="M{x} {y + h * t} Q{x + w * .3} {y + h * (t - .06)} {x + w * .6} {y + h * t} T{x + w} {y + h * (t + .02)}" stroke="{dk}" stroke-width="1.6" fill="none" opacity=".4"/>'
                       for t in (.32, .52, .72))
    if mat == "ice":
        return (f'<path d="M{x} {y} L{x + w * .35} {y} L{x + w * .18} {y + h} L{x} {y + h} Z" fill="#fff" opacity=".18"/>'
                + "".join(f'<path d="M{x + w * a} {y + h * b} l5 5 m0 -5 l-5 5" stroke="#fff" stroke-width="1.3" opacity=".7"/>' for a, b in ((.82, .3), (.7, .7), (.9, .62))))
    if mat == "pearl":
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ff9ee8" opacity=".14"/>'  # iridescent sheen bands
                f'<path d="M{x} {y + h * .62} Q{x + w * .5} {y + h * .3} {x + w} {y + h * .6} V{y + h} H{x} Z" fill="#7ff3ff" opacity=".18"/>')
    if mat == "crystal":
        return (f'<polygon points="{x},{y} {x + w * .4},{y} {x + w * .25},{y + h}  {x},{y + h}" fill="#fff" opacity=".16"/>'
                f'<polygon points="{x + w * .55},{y} {x + w * .75},{y} {x + w * .6},{y + h} {x + w * .4},{y + h}" fill="#fff" opacity=".1"/>'
                f'<polygon points="{x + w * .75},{y} {x + w},{y} {x + w},{y + h} {x + w * .6},{y + h}" fill="{dk}" opacity=".2"/>')
    if mat == "sand":
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#grain)" opacity=".22"/>'
                + "".join(f'<circle cx="{x + w * a}" cy="{y + h * b}" r="1.6" fill="{dk}" opacity=".35"/>' for a, b in ((.2, .7), (.5, .8), (.8, .72), (.35, .6), (.66, .64))))
    if mat == "brass":
        return (f'<rect x="{x}" y="{y + h * .46}" width="{w}" height="{h * .08}" fill="#fff" opacity=".22"/>'
                + "".join(f'<circle cx="{cx}" cy="{y + h / 2}" r="{max(2.5, h * .05)}" fill="{dk}"/><circle cx="{cx - 1}" cy="{y + h / 2 - 1}" r="{max(1, h * .02)}" fill="#fff" opacity=".8"/>'
                          for cx in (x + h * .28, x + w - h * .28)))
    if mat == "cosmic":
        return ("".join(f'<circle cx="{x + w * a}" cy="{y + h * b}" r="{r}" fill="#fff" opacity=".85"/>' for a, b, r in ((.15, .3, 1.4), (.32, .7, 1), (.62, .25, 1.2), (.85, .66, 1.5), (.5, .55, .8)))
                + f'<ellipse cx="{x + w * .7}" cy="{y + h * .7}" rx="{w * .3}" ry="{h * .35}" fill="{l}" opacity=".18" filter="url(#glow)"/>')
    if mat == "frosted":
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h * .5}" fill="#fff" opacity=".25"/>'
    return ""


def face(x, y, w, h, l, m, dk, mat, depth=6, r=None, outline=False, state="normal"):
    """One chunky surface: soft tinted shadow, depth base, gradient face, material detail, rim light, gloss."""
    k = next(_ids)
    r = (h * RADIUS.get(mat, .5)) if r is None else r
    if state == "pressed": depth, y = 1.5, y + depth - 1.5
    if state == "disabled": l, m, dk = "#c4c8d0", "#8a8f99", "#5a5f69"
    d, dd = rr(x, y, w, h, r), rr(x, y + depth, w, h, r)
    if mat == "neon" and state != "disabled":  # neon: dark glass with glowing tube outline
        return (f'<path d="{dd}" fill="#000" opacity=".5" filter="url(#sh)"/>'
                f'<path d="{d}" fill="#140a22"/><path d="{d}" fill="none" stroke="{m}" stroke-width="8" filter="url(#glow)" opacity=".9"/>'
                f'<path d="{d}" fill="none" stroke="{l}" stroke-width="3"/>')
    grad = (f'<linearGradient id="f{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{l}"/>'
            f'<stop offset=".55" stop-color="{m}"/><stop offset="1" stop-color="{mix(m, dk, .5)}"/></linearGradient>'
            f'<clipPath id="c{k}"><path d="{d}"/></clipPath>')
    fill = "none" if outline else f"url(#f{k})"
    gloss = {"glossy": .32, "frosted": .5, "ice": .42, "pearl": .34, "brass": .45, "crystal": .3}.get(mat, .2)
    base = "" if outline else (f'<path d="{dd}" fill="{dk}" opacity=".5" filter="url(#sh)" transform="translate(0 4)"/>'
                               f'<path d="{dd}" fill="{dk}"/>')
    body = (f'<defs>{grad}</defs>{base}'
            f'<path d="{d}" fill="{fill}" {"stroke=" + chr(34) + m + chr(34) + " stroke-width=" + chr(34) + "4" + chr(34) if outline else ""}/>')
    if not outline:
        body += (f'<g clip-path="url(#c{k})">{material(mat, d, x, y, w, h, l, m, dk) if state != "disabled" and w >= 140 else ""}'
                 f'<rect x="{x + r * .4}" y="{y + 3}" width="{w - r * .8}" height="{h * .34}" rx="{h * .17}" fill="#fff" opacity="{gloss}"/></g>'
                 f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>')
    return body


# ---- controls -------------------------------------------------------------------------------------
def tone(t, role):
    p = t["palette"]
    if role == "primary":   return mix(p["primary"], "#fff", .35), p["primary"], p["primaryDark"]
    if role == "secondary": return mix(p["secondary"], "#fff", .35), p["secondary"], p["secondaryDark"]
    if role == "danger":    return mix(p["danger"], "#fff", .35), p["danger"], mix(p["danger"], "#000", .45)
    s = p["surface"]
    return mix(s, "#fff", .28), s, mix(s, "#000", .45)


def glyph_color(t, m):
    return "#ffffff" if contrast("#ffffff", m) >= contrast("#1a1020", m) else "#1a1020"


def icon(t, name, glyph_name, round_=False, role="surface"):
    l, m, dk = tone(t, role)
    if t["material"] == "neon":  # neon glyphs glow: tube colour for coloured buttons, theme neon for plain ones
        gc = t["palette"]["primary"] if role == "surface" else l
    else:
        gc = glyph_color(t, m)
    r = 64 if round_ else 34
    g = (f'<g transform="translate(64 64) scale(.78) translate(-64 -64) translate(0 3)" opacity=".3" filter="url(#gs)">{glyph(glyph_name, "#000", 10)}</g>'
         f'<g transform="translate(64 61) scale(.78) translate(-64 -64)">{glyph(glyph_name, gc, 10)}</g>')
    return doc(128, 128, f'<defs>{FX}</defs>' + face(0, 0, 128, 122, l, m, dk, t["material"], 6, r) + g)


def pill(t, role, state):
    if role == "ghost":
        p = t["palette"]
        return doc(360, 110, f'<defs>{FX}</defs>' + face(0, 0, 360, 104, p["ghost"], p["ghost"], mix(p["ghost"], "#000", .5), "glossy", 0,
                                                       104 * RADIUS.get(t["material"], .5), outline=True, state=state))
    l, m, dk = tone(t, role)
    return doc(360, 110, f'<defs>{FX}</defs>' + face(0, 0, 360, 100, l, m, dk, t["material"], 8, state=state))


def tab(t, active):
    l, m, dk = tone(t, "primary" if active else "surface")
    return doc(220, 80, f'<defs>{FX}</defs>' + face(0, 0, 220, 72, l, m, dk, t["material"], 6 if active else 3, 22)
               + (f'<rect x="70" y="58" width="80" height="6" rx="3" fill="#fff" opacity=".85"/>' if active else ""))


def segmented(t, left):
    sl, sm, sd = tone(t, "surface"); pl, pm, pd = tone(t, "primary")
    track = f'<path d="{rr(0, 0, 300, 70, 35)}" fill="{sd}"/><path d="{rr(3, 3, 294, 64, 32)}" fill="{sm}"/>'
    return doc(300, 76, f'<defs>{FX}</defs>' + track + face(6 if left else 150, 6, 144, 54, pl, pm, pd, t["material"], 4, 27))


def toggle(t, on):
    l, m, dk = tone(t, "primary" if on else "surface")
    x = 70 if on else 6
    return doc(124, 66, f'<defs>{FX}</defs>' + face(0, 0, 124, 62, l, m, dk, t["material"], 3, 31)
               + f'<circle cx="{x + 24}" cy="35" r="24" fill="#000" opacity=".3" filter="url(#gs)"/>'
               f'<circle cx="{x + 24}" cy="31" r="24" fill="#f6f7fa"/><ellipse cx="{x + 19}" cy="23" rx="11" ry="6" fill="#fff"/>'
               f'<circle cx="{x + 24}" cy="31" r="24" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="2"/>')


def check(t, on, radio=False):
    l, m, dk = tone(t, "primary" if on else "surface")
    if radio:
        return doc(72, 72, f'<defs>{FX}</defs>' + face(0, 0, 72, 68, l, m, dk, t["material"], 4, 34)
                   + (f'<circle cx="36" cy="34" r="14" fill="#fff"/><circle cx="36" cy="34" r="8" fill="{m}"/>' if on else '<circle cx="36" cy="34" r="16" fill="#000" opacity=".25"/>'))
    return doc(72, 72, f'<defs>{FX}</defs>' + face(0, 0, 72, 68, l, m, dk, t["material"], 4, 18)
               + ('<path d="M20 36 L31 47 L53 23" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' if on
                  else '<rect x="14" y="13" width="44" height="42" rx="10" fill="#000" opacity=".25"/>'))


def slider_track(t):
    sl, sm, sd = tone(t, "surface"); pl, pm, pd = tone(t, "primary")
    return doc(320, 30, f'<defs>{FX}</defs><path d="{rr(0, 2, 320, 26, 13)}" fill="{sd}"/><path d="{rr(3, 5, 314, 20, 10)}" fill="{mix(sm, "#000", .3)}"/>'
               + face(3, 5, 190, 20, pl, pm, pd, t["material"], 0, 10))


def slider_thumb(t):
    l, m, dk = tone(t, "secondary")
    return doc(56, 56, f'<defs>{FX}</defs>' + face(0, 0, 56, 52, l, m, dk, t["material"], 4, 26) + '<rect x="24" y="16" width="8" height="20" rx="4" fill="#fff" opacity=".7"/>')


def stepper(t):
    l, m, dk = tone(t, "surface"); pl, pm, pd = tone(t, "primary")
    return doc(210, 72, f'<defs>{FX}</defs><path d="{rr(0, 4, 210, 64, 32)}" fill="{dk}"/><path d="{rr(2, 6, 206, 58, 29)}" fill="{m}"/>'
               + face(4, 6, 58, 56, pl, pm, pd, t["material"], 4, 28) + face(148, 6, 58, 56, pl, pm, pd, t["material"], 4, 28)
               + '<path d="M22 34 H44 M166 34 H188 M177 23 V45" stroke="#fff" stroke-width="7" stroke-linecap="round"/>')


def badge(t):
    p = t["palette"]
    return doc(56, 56, f'<defs>{FX}</defs><circle cx="28" cy="31" r="26" fill="#000" opacity=".35" filter="url(#gs)"/>'
               f'<circle cx="28" cy="28" r="26" fill="#fff"/><circle cx="28" cy="28" r="22" fill="{p["danger"]}"/>'
               '<ellipse cx="22" cy="18" rx="9" ry="5" fill="#fff" opacity=".45"/>')


def price(t):
    l, m, dk = tone(t, "secondary")
    shard = ('<path d="M44 22 L64 44 L44 80 L24 44 Z" fill="#7f9bff" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/>'
             '<path d="M44 22 L34 44 L44 34 Z" fill="#fff" opacity=".6"/>')
    return doc(260, 96, f'<defs>{FX}</defs>' + face(0, 0, 260, 90, l, m, dk, t["material"], 7) + shard)


def booster(t, glyph_name="bolt"):
    l, m, dk = tone(t, "secondary")
    p = t["palette"]
    return doc(128, 128, f'<defs>{FX}</defs>' + face(0, 8, 120, 112, l, m, dk, t["material"], 6, 30)
               + f'<g transform="translate(60 62) scale(.72) translate(-64 -64)">{glyph(glyph_name, "#fff", 10)}</g>'
               f'<circle cx="112" cy="16" r="18" fill="#fff"/><circle cx="112" cy="16" r="14" fill="{p["danger"]}"/>')


ICON_SET = ["home", "pause", "play", "settings", "sound", "music", "share", "shop", "trophy", "swap", "back", "close"]


def controls(t):
    """control id → {state: svg}. The registry the JSON, preview and checks are built from."""
    c = {f"pill-{r}": {s: pill(t, r, s) for s in ("normal", "pressed", "disabled")} for r in ("primary", "secondary", "ghost", "danger")}
    c |= {f"icon-{n}": {"normal": icon(t, n, n)} for n in ICON_SET}
    c |= {"icon-fire": {"normal": icon(t, "fire", "fire", True, "primary")}, "booster": {"normal": booster(t)},
          "tab": {"active": tab(t, True), "inactive": tab(t, False)},
          "segmented": {"left": segmented(t, True), "right": segmented(t, False)},
          "toggle": {"on": toggle(t, True), "off": toggle(t, False)},
          "checkbox": {"on": check(t, True), "off": check(t, False)},
          "radio": {"on": check(t, True, True), "off": check(t, False, True)},
          "slider-track": {"normal": slider_track(t)}, "slider-thumb": {"normal": slider_thumb(t)},
          "stepper": {"normal": stepper(t)}, "badge": {"normal": badge(t)}, "price": {"normal": price(t)}}
    return c


def themes_css():
    faces = "".join(f'@font-face{{font-family:"{f}";src:url("../fonts/{path}") format("truetype");font-display:swap;font-weight:100 900}}\n'
                    for f, (path, _) in FONTS.items())
    faces += "".join(f'@font-face{{font-family:"Poppins";src:url("../fonts/poppins/Poppins-{w}.ttf") format("truetype");font-weight:{n}}}\n'
                     for w, n in (("SemiBold", 600), ("ExtraBold", 800), ("Black", 900)))
    rules = ""
    for tid, t in THEMES.items():
        p, (dur, eas, idle) = t["palette"], t["motion"]
        fam = f'"{t["font"]}", {FONTS[t["font"]][1]}'
        btn_font = '"Poppins", system-ui, sans-serif' if t["fontTitleOnly"] else fam
        rules += (f'[data-theme="{tid}"]{{' + "".join(f"--{k}:{v};" for k, v in p.items())
                  + f'--font-display:{fam};--font-button:{btn_font};--font-body:"Poppins", system-ui, sans-serif;'
                  f'--dur:{dur};--ease:{eas};--idle:{idle};--piece0:{t["pieces"][0][1]};--piece1:{t["pieces"][1][1]};--piece2:{t["pieces"][2][1]};--piece3:{t["pieces"][3][1]}}}\n')
    return "/* GENERATED by tools/make_ui_kit.py from tools/level_themes.py — do not edit by hand */\n" + faces + rules


if __name__ == "__main__":
    n, manifest = 0, {}
    for tid, t in THEMES.items():
        for cid, states in controls(t).items():
            for st, data in states.items():
                f = f"ui_{tid}_{cid}_{st}.svg"
                d = os.path.join(OUT, folder_for(f)); os.makedirs(d, exist_ok=True)
                open(os.path.join(d, f), "w").write(data); n += 1
                manifest.setdefault(cid, set()).add(st)
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    kit = {"themes": {tid: {"name": t["name"], "font": t["font"], "fontTitleOnly": t["fontTitleOnly"], "material": t["material"],
                            "palette": t["palette"], "motion": dict(zip(("dur", "ease", "idle"), t["motion"]))} for tid, t in THEMES.items()},
           "pattern": "buttons/{theme}/ui_{theme}_{control}_{state}.svg",
           "controls": {cid: sorted(s) for cid, s in manifest.items()}}
    json.dump(kit, open(os.path.join(OUT, "data", "ui-kit.json"), "w"), indent=1)
    fonts = [{"family": f, "file": f"fonts/{path}", "license": "SIL Open Font License 1.1", "licenseFile": f"fonts/{path.split('/')[0]}/OFL.txt",
              "source": f"{FONT_SOURCE}/{path.split('/')[0].replace('-', '')}"} for f, (path, _) in FONTS.items()]
    json.dump(fonts, open(os.path.join(OUT, "data", "fonts.json"), "w"), indent=1)
    open(os.path.join(OUT, "motion", "themes.css"), "w").write(themes_css())
    print(f"wrote {n} themed controls ({len(manifest)} controls × {len(THEMES)} themes) + ui-kit.json, fonts.json, themes.css")
