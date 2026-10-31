# Edge Pulse UI kit: icon buttons, mode tiles, HUD, map nodes, badges, stamps. Run: python3 tools/make_ui.py
# 2026 soft-clay language: no outlines, tinted blurred shadows, inner light rim, subtle gloss, large radii.
import os
from layout import folder_for

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
INK = "none"  # outlines removed (2016-era look)
METAL = ("#7a8294", "#3a4050")  # graphite face
TINTS = {"graphite": METAL, "green": ("#9dff6a", "#2f9a12"), "cyan": ("#7ff3ff", "#1478d4"),
         "magenta": ("#ff9ee8", "#b8268f"), "amber": ("#ffe08a", "#e07a00"), "violet": ("#c9a0ff", "#5a2fd6"),
         "red": ("#ff9a9a", "#d42a3a"), "gold": ("#fff3b0", "#c98a00")}

# 128-grid glyphs. Stroke glyphs use round caps; fill glyphs marked with "F:".
ICONS = {
    "home": "M34 64 L64 36 L94 64 M44 56 V92 H84 V56",
    "pause": "M52 42 V86 M76 42 V86",
    "play": "F:M52 38 L92 64 L52 90 Z",
    "settings": "GEAR",
    "sound": "F:M38 54 H52 L70 38 V90 L52 74 H38 Z|M80 50 Q90 64 80 78 M90 42 Q106 64 90 86",
    "sound_off": "F:M38 54 H52 L70 38 V90 L52 74 H38 Z|M80 52 L98 76 M98 52 L80 76",
    "music": "M58 84 V42 L90 36 V78|F:M42 84 a10 9 0 1 0 20 0 a10 9 0 1 0 -20 0 M74 78 a10 9 0 1 0 20 0 a10 9 0 1 0 -20 0",
    "haptics": "M52 38 H76 Q80 38 80 42 V86 Q80 90 76 90 H52 Q48 90 48 86 V42 Q48 38 52 38 Z M36 52 V76 M92 52 V76",
    "share": "M48 64 L82 44 M48 64 L82 84|F:M38 64 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0 M74 44 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0 M74 84 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0",
    "trophy": "M64 76 V88 M48 92 H80 M46 46 H36 Q36 62 50 64 M82 46 H92 Q92 62 78 64|F:M44 36 H84 V54 A20 20 0 0 1 44 54 Z",
    "lock": "M52 58 V48 A12 12 0 0 1 76 48 V58|F:M42 58 H86 Q90 58 90 62 V88 Q90 92 86 92 H42 Q38 92 38 88 V62 Q38 58 42 58 Z",
    "check": "M40 66 L58 84 L90 46",
    "close": "M44 44 L84 84 M84 44 L44 84",
    "back": "M74 38 L48 64 L74 90",
    "swap": "M40 52 H86 L74 40 M88 76 H42 L54 88",
    "calendar": "M40 44 H88 V90 H40 Z M40 58 H88 M52 34 V48 M76 34 V48",
    "flag": "M46 92 V36 M46 40 H86 L76 54 L86 68 H46",
    "infinity": "M64 64 C52 46 34 46 34 64 C34 82 52 82 64 64 C76 46 94 46 94 64 C94 82 76 82 64 64 Z",
    "drops": "F:M50 36 C58 48 62 54 62 61 A12 12 0 0 1 38 61 C38 54 42 48 50 36 Z M78 58 C86 70 90 76 90 83 A12 12 0 0 1 66 83 C66 76 70 70 78 58 Z",
    "bolt": "F:M72 30 L44 70 H62 L54 98 L86 56 H67 Z",
    "clock": "M64 46 V64 L78 72|C:64,64,30",
    "constellation": "M36 84 L54 50 L74 68 L92 38|F:M30 84 a6 6 0 1 0 12 0 a6 6 0 1 0 -12 0 M48 50 a6 6 0 1 0 12 0 a6 6 0 1 0 -12 0 M68 68 a6 6 0 1 0 12 0 a6 6 0 1 0 -12 0 M86 38 a6 6 0 1 0 12 0 a6 6 0 1 0 -12 0",
    "cross": "M64 34 V94 M34 64 H94",
    "star": "F:M64 32 L73 53 L96 55 L79 70 L84 93 L64 81 L44 93 L49 70 L32 55 L55 53 Z",
    "fire": "F:M54 64 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0|C:64,64,22|C:64,64,34",
    "shop": "M38 50 H90 L84 90 H44 Z M52 50 V44 A12 12 0 0 1 76 44 V50",
}


def svg(body, w, h, pad=8):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w + 2 * pad} {h + 2 * pad}" '
            f'width="{w + 2 * pad}" height="{h + 2 * pad}">{body}</svg>')


def glyph(name, color="#fff", sw=9):
    out = []
    for part in ICONS[name].split("|"):
        if part == "GEAR":
            out.append(f'<circle cx="64" cy="64" r="26" fill="none" stroke="{color}" stroke-width="14" stroke-dasharray="10.2 10.2"/>'
                       f'<circle cx="64" cy="64" r="19" fill="none" stroke="{color}" stroke-width="{sw}"/>')
        elif part.startswith("F:"):
            out.append(f'<path d="{part[2:]}" fill="{color}"/>')
        elif part.startswith("C:"):
            x, y, r = part[2:].split(",")
            out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw * .8}"/>')
        else:
            out.append(f'<path d="{part}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(out)


def embossed(name, cx=64, cy=64, scale=1.0, shade="#000"):
    """Glyph with soft blurred shadow."""
    t = f"translate({cx - 64 * scale} {cy - 64 * scale}) scale({scale})"
    return (f'<g transform="{t} translate(0 3)" opacity=".3" filter="url(#gs)">{glyph(name, shade, 10)}</g>'
            f'<g transform="{t}">{glyph(name)}</g>')


def defs(l, d):
    return (f'<defs><linearGradient id="f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{l}"/>'
            f'<stop offset="1" stop-color="{d}"/></linearGradient>'
            '<linearGradient id="gl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".35"/>'
            '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<filter id="sh" x="-40%" y="-40%" width="180%" height="190%"><feGaussianBlur stdDeviation="7"/></filter>'
            '<filter id="gs" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.5"/></filter></defs>')


def icon_button(name, tint="graphite", under=""):
    """Round chunky icon button: drop shadow, dark base, face, rim, gloss, embossed glyph."""
    l, d = TINTS[tint]
    return svg(defs(l, d) + under +
               f'<circle cx="64" cy="72" r="54" fill="{d}" opacity=".55" filter="url(#sh)"/>'
               f'<circle cx="64" cy="65" r="58" fill="{d}"/>'
               f'<circle cx="64" cy="62" r="58" fill="url(#f)" stroke="{INK}" stroke-width="4"/>'
               f'<circle cx="64" cy="62" r="56" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>'
               '<ellipse cx="64" cy="30" rx="40" ry="20" fill="url(#gl)"/>' + embossed(name, 64, 62, .8, d), 128, 128)


def tile(name, tint, w=180):
    """Mode tile: glossy rounded square with big glyph (used on mode select & Pulse Club)."""
    l, d = TINTS[tint]
    r = w * .3
    return svg(defs(l, d) +
               f'<rect x="10" y="22" width="{w - 20}" height="{w - 20}" rx="{r}" fill="{d}" opacity=".6" filter="url(#sh)"/>'
               f'<rect x="0" y="5" width="{w}" height="{w - 8}" rx="{r}" fill="{d}"/>'
               f'<rect x="0" y="0" width="{w}" height="{w - 8}" rx="{r}" fill="url(#f)" stroke="{INK}" stroke-width="4"/>'
               f'<rect x="6" y="6" width="{w - 12}" height="{w - 20}" rx="{r - 6}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>'
               f'<rect x="14" y="8" width="{w - 28}" height="{w * .32}" rx="{w * .16}" fill="url(#gl)"/>'
               + embossed(name, w / 2, w / 2 - 4, w / 128 * .85, d), w, w)


def pill(w=280, h=72):
    """Glass HUD pill for score / timer / moves (text drawn by the game)."""
    return svg('<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2f3a" stop-opacity=".9"/>'
               '<stop offset="1" stop-color="#0d0f14" stop-opacity=".9"/></linearGradient></defs>'
               f'<rect x="0" y="4" width="{w}" height="{h}" rx="{h / 2}" fill="#000" opacity=".35"/>'
               f'<rect x="0" y="0" width="{w}" height="{h}" rx="{h / 2}" fill="url(#g)" stroke="#c2c7d1" stroke-opacity=".6" stroke-width="3"/>'
               f'<rect x="{h / 2}" y="4" width="{w - h}" height="{h * .3}" rx="{h * .15}" fill="#fff" opacity=".1"/>', w, h)


def slot(label_color):
    """NOW / NEXT slot: inset glass well with colored top lip."""
    return svg('<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0f14"/>'
               '<stop offset="1" stop-color="#2a2f3a"/></linearGradient></defs>'
               '<rect x="0" y="0" width="128" height="128" rx="30" fill="#c2c7d1" stroke="#1a1020" stroke-width="4"/>'
               '<rect x="8" y="8" width="112" height="112" rx="24" fill="url(#g)"/>'
               f'<rect x="30" y="2" width="68" height="8" rx="4" fill="{label_color}"/>', 128, 128)


def progress(fill_pct, tint="green", w=320, h=32):
    l, d = TINTS[tint]
    fw = max(h, (w - 8) * fill_pct)
    return svg(defs(l, d) +
               f'<rect x="0" y="0" width="{w}" height="{h}" rx="{h / 2}" fill="#0d0f14" stroke="{INK}" stroke-width="4"/>'
               f'<rect x="4" y="4" width="{fw}" height="{h - 8}" rx="{(h - 8) / 2}" fill="url(#f)"/>'
               f'<rect x="12" y="7" width="{fw - 16}" height="{(h - 8) * .35}" rx="3" fill="#fff" opacity=".45"/>', w, h)


def toggle(on):
    l, d = TINTS["green" if on else "graphite"]
    x = 74 if on else 30
    return svg(defs(l, d) +
               f'<rect x="0" y="0" width="104" height="60" rx="30" fill="url(#f)" stroke="{INK}" stroke-width="4"/>'
               f'<circle cx="{x}" cy="34" r="24" fill="#000" opacity=".3"/>'
               f'<circle cx="{x}" cy="30" r="24" fill="#f4f6fa" stroke="{INK}" stroke-width="4"/>'
               f'<ellipse cx="{x - 4}" cy="22" rx="12" ry="7" fill="#fff"/>', 104, 64)


def node(state):
    """Campaign map node: done (green + check), current (cyan + halo), locked (graphite + lock)."""
    tint, g = {"done": ("green", "check"), "current": ("cyan", "play"), "locked": ("graphite", "lock")}[state]
    halo = ('<circle cx="64" cy="64" r="62" fill="none" stroke="#7ff3ff" stroke-width="5" stroke-dasharray="12 8" opacity=".9"/>'
            if state == "current" else "")
    return icon_button(g, tint, halo)


def badge(name, earned=True):
    """Mastery badge: hex medal, gold when earned, graphite when locked."""
    l, d = TINTS["gold" if earned else "graphite"]
    hexp = "M64 4 L116 34 V94 L64 124 L12 94 V34 Z"
    inner = "M64 18 L104 41 V87 L64 110 L24 87 V41 Z"
    return svg(defs(l, d) +
               f'<path d="{hexp}" fill="{d}" opacity=".55" filter="url(#sh)" transform="translate(0 8)"/>'
               f'<path d="{hexp}" fill="{d}" transform="translate(0 4)"/>'
               f'<path d="{hexp}" fill="url(#f)" stroke="{INK}" stroke-width="4"/>'
               f'<path d="{inner}" fill="{d}" opacity=".45"/>'
               f'<path d="M64 18 L104 41 V60 Q64 48 24 60 V41 Z" fill="#fff" opacity=".25"/>'
               + embossed(name, 64, 64, .6, d) + ("" if earned else '<path d="' + hexp + '" fill="#16181e" opacity=".35"/>'), 128, 128)


def stamp(earned=True):
    """Daily Pulse stamp: scalloped seal."""
    import math
    pts = " ".join(f"{64 + (58 if i % 2 else 50) * math.cos(i * math.pi / 16):.1f},{64 + (58 if i % 2 else 50) * math.sin(i * math.pi / 16):.1f}"
                   for i in range(32))
    l, d = TINTS["magenta" if earned else "graphite"]
    return svg(defs(l, d) +
               f'<polygon points="{pts}" fill="url(#f)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
               '<circle cx="64" cy="64" r="38" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="3" stroke-dasharray="4 6"/>'
               + embossed("check" if earned else "calendar", 64, 64, .6), 128, 128)


def ribbon(w=420, h=110):
    """'NEW RECORD' / 'STAGE CLEAR' banner; text drawn by the game in Poppins 900."""
    l, d = TINTS["amber"]
    return svg(defs(l, d) +
               f'<path d="M0 40 H60 V100 H0 L20 70 Z M{w} 40 H{w - 60} V100 H{w} L{w - 20} 70 Z" fill="{d}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
               f'<path d="M40 10 Q{w / 2} -6 {w - 40} 10 V80 Q{w / 2} 64 40 80 Z" fill="url(#f)" stroke="{INK}" stroke-width="4"/>'
               f'<path d="M50 18 Q{w / 2} 4 {w - 50} 18 V34 Q{w / 2} 22 50 34 Z" fill="#fff" opacity=".4"/>', w, h)


def combo_burst():
    """Starburst behind combo shoutouts."""
    import math
    pts = " ".join(f"{64 + (60 if i % 2 == 0 else 40) * math.cos(i * math.pi / 10 - math.pi / 2):.1f},"
                   f"{64 + (60 if i % 2 == 0 else 40) * math.sin(i * math.pi / 10 - math.pi / 2):.1f}" for i in range(20))
    l, d = TINTS["amber"]
    return svg(defs(l, d) + f'<polygon points="{pts}" fill="url(#f)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
               '<circle cx="64" cy="64" r="30" fill="#fff" opacity=".25"/>', 128, 128)


files = {f"icon_{n}.svg": icon_button(n) for n in
         ("home", "pause", "settings", "sound", "sound_off", "music", "haptics", "share", "back", "close", "swap", "shop", "trophy")}
files |= {"icon_play_green.svg": icon_button("play", "green"), "icon_check_green.svg": icon_button("check", "green"),
          "icon_close_red.svg": icon_button("close", "red"), "btn_fire.svg": icon_button("fire", "cyan")}
MODES = {"endless": ("infinity", "violet"), "color_match": ("drops", "magenta"), "blast": ("bolt", "amber"),
         "time_rush": ("clock", "cyan"), "campaign": ("flag", "green"), "daily": ("calendar", "magenta"),
         "weekly": ("constellation", "violet")}
files |= {f"mode_{k}.svg": tile(g, t) for k, (g, t) in MODES.items()}
files |= {"hud_pill.svg": pill(), "slot_now.svg": slot("#7ff3ff"), "slot_next.svg": slot("#8c94a3"),
          "progress_track_60.svg": progress(.6), "progress_time.svg": progress(.35, "amber"),
          "toggle_on.svg": toggle(True), "toggle_off.svg": toggle(False),
          "node_done.svg": node("done"), "node_current.svg": node("current"), "node_locked.svg": node("locked"),
          "stamp_on.svg": stamp(True), "stamp_off.svg": stamp(False), "ribbon.svg": ribbon(), "combo_burst.svg": combo_burst()}
BADGES = {"streak": "bolt", "campaign": "flag", "stamps": "calendar", "row_col": "cross",
          "endless": "infinity", "blaster": "star", "rush": "clock", "collector": "trophy"}
files |= {f"badge_{k}.svg": badge(g) for k, g in BADGES.items()}
files |= {"badge_locked.svg": badge("lock", False)}

os.makedirs(OUT, exist_ok=True)
for n, data in files.items():
    os.makedirs(os.path.join(OUT, folder_for(n)), exist_ok=True)
    open(os.path.join(OUT, folder_for(n), n), "w").write(data)
print(f"wrote {len(files)} UI assets to {os.path.abspath(OUT)}")
