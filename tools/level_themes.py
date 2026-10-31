# Single registry for level themes. Every themed asset, token and data file is generated from this.
# To add a theme: add one entry here, then run sh tools/build_all.sh (check_assets.py flags anything missing).
# Piece colours keep the drop/heart/leaf/star hue families (blue/pink/green/yellow) so gameplay reads the same everywhere.

FONTS = {  # family: (file under assets/fonts, CSS fallback). All SIL OFL 1.1 — free for commercial games, embeddable.
    "Poppins": ("poppins/Poppins-ExtraBold.ttf", "system-ui, sans-serif"),
    "Bungee": ("bungee/Bungee-Regular.ttf", "Impact, sans-serif"),
    "Fredoka": ("fredoka/Fredoka[wdth,wght].ttf", "system-ui, sans-serif"),
    "Cinzel Decorative": ("cinzel-decorative/CinzelDecorative-Bold.ttf", "Georgia, serif"),
    "Exo 2": ("exo2/Exo2[wght].ttf", "system-ui, sans-serif"),
    "Baloo 2": ("baloo2/Baloo2[wght].ttf", "system-ui, sans-serif"),
    "Creepster": ("creepster/Creepster-Regular.ttf", "fantasy"),
    "Righteous": ("righteous/Righteous-Regular.ttf", "system-ui, sans-serif"),
    "Lilita One": ("lilita-one/LilitaOne-Regular.ttf", "Impact, sans-serif"),
    "Rye": ("rye/Rye-Regular.ttf", "Georgia, serif"),
    "Audiowide": ("audiowide/Audiowide-Regular.ttf", "system-ui, sans-serif"),
}
FONT_SOURCE = "https://github.com/google/fonts/tree/main/ofl"


def T(name, mood, palette, pieces, material, font, title_only, motion, obstacles, collectibles, mechanics):
    return dict(name=name, mood=mood, palette=palette, pieces=pieces, material=material, font=font,
                fontTitleOnly=title_only, motion=motion, obstacles=obstacles, collectibles=collectibles, mechanics=mechanics)


# palette: bg, surface, primary, primaryDark, secondary, secondaryDark, accent, danger, text, onPrimary
# motion: (duration multiplier, easing, idle effect)
THEMES = {
    "graphite": T("Graphite", "Clean, shiny graphite and glass",
        dict(bg="#16181e", surface="#2a2f3a", primary="#5fd23a", primaryDark="#2f8a12", secondary="#4aa8ff", secondaryDark="#1d5fc4",
             accent="#7ff3ff", danger="#ff4a5a", text="#f2f4f8", onPrimary="#0e2a06"),
        [("#7ff3ff", "#14b8d4", "#06576b"), ("#ff9ee8", "#e83fb8", "#6e0f55"), ("#d6ff8a", "#7fd420", "#2f5a07"), ("#ffe08a", "#ffa51f", "#7a3d00")],
        "glossy", "Poppins", False, (1.0, "cubic-bezier(.34,1.4,.64,1)", "shine"),
        [("crate", "Wooden Crate", 3), ("ice", "Ice Block", 3), ("chain", "Chain Lock", 2)],
        [("shard", "Pulse Shard"), ("star", "Gold Star")], []),
    "volcano": T("Dangerous Volcano", "High pressure, lava everywhere",
        dict(bg="#1a0806", surface="#3a1410", primary="#ff6a1a", primaryDark="#a02a04", secondary="#ffc21f", secondaryDark="#a06400",
             accent="#ffd27a", danger="#ff2a2a", text="#fff1e6", onPrimary="#2a0800"),
        [("#ffd0a0", "#ff6a1a", "#8a2004"), ("#ff9aa0", "#e8203a", "#6a0410"), ("#e8f08a", "#a8c020", "#3a4a04"), ("#fff0a0", "#ffc21f", "#8a4a00")],
        "lava", "Bungee", False, (.9, "cubic-bezier(.2,1.5,.5,1)", "ember"),
        [("lava", "Lava Tile", 2), ("rock", "Falling Rock", 3), ("fire", "Fire Blocker", 2)],
        [("firecrystal", "Fire Crystal"), ("magmagem", "Volcanic Gem")], ["lava melts unmatched tiles", "rocks fall each 5 moves"]),
    "sky": T("Sky Islands", "Light, airy, always shifting",
        dict(bg="#cfe9ff", surface="#ffffff", primary="#4aa8ff", primaryDark="#1d5fc4", secondary="#b48cff", secondaryDark="#6a3fd0",
             accent="#ffffff", danger="#ff6a8a", text="#1d2a4a", onPrimary="#ffffff"),
        [("#d8f4ff", "#5fc8ff", "#1a5a9a"), ("#ffd8ee", "#ff8ac8", "#9a2a6a"), ("#dcffd8", "#7fe08a", "#2a7a3a"), ("#fff6c8", "#ffd65a", "#9a7010")],
        "frosted", "Fredoka", False, (1.25, "cubic-bezier(.3,1.25,.5,1)", "float"),
        [("balloon", "Balloon Blocker", 1), ("cloud", "Cloud Patch", 2), ("platform", "Floating Platform", 3)],
        [("feather", "Cloud Feather"), ("skycrystal", "Sky Crystal")], ["wind pushes pieces sideways", "platforms drift"]),
    "forest": T("Enchanted Forest", "Mysterious and glowing",
        dict(bg="#0a1a12", surface="#16301f", primary="#3ad48a", primaryDark="#127a46", secondary="#ffd65a", secondaryDark="#9a7010",
             accent="#7fe8ff", danger="#ff6a5a", text="#eafff2", onPrimary="#04200f"),
        [("#a8f4ff", "#2ab8e0", "#0a4a6a"), ("#ffb8e8", "#e04ab8", "#6a0a4a"), ("#c8ffa8", "#4fd43a", "#1a6010"), ("#fff0a0", "#ffc83a", "#8a5a00")],
        "wood", "Cinzel Decorative", True, (1.15, "cubic-bezier(.3,1.3,.5,1)", "firefly"),
        [("vine", "Creeping Vines", 2), ("mushroom", "Mushroom Blocker", 3), ("stump", "Sleeping Stump", 2)],
        [("glowshroom", "Glowing Mushroom"), ("fairydust", "Fairy Dust")], ["vines grow over a tile each turn"]),
    "tundra": T("Frozen Tundra", "Cold, slippery, precise",
        dict(bg="#0c1a2e", surface="#1c3250", primary="#5cc8ff", primaryDark="#1a6aa8", secondary="#ff9ad0", secondaryDark="#b03a7a",
             accent="#e0f8ff", danger="#ff5a7a", text="#f2fbff", onPrimary="#04203a"),
        [("#e8faff", "#6cd0ff", "#1a5a8a"), ("#ffe0f0", "#ff8ac4", "#8a2a5a"), ("#d8fff0", "#4fe0b0", "#0a6a4a"), ("#fff8d8", "#ffe07a", "#8a6a10")],
        "ice", "Exo 2", False, (1.0, "cubic-bezier(.25,1.2,.5,1)", "frost"),
        [("iceblock", "Ice Block", 3), ("frostlock", "Frozen Lock", 2), ("slide", "Sliding Ice", 1)],
        [("icediamond", "Ice Diamond"), ("snowflake", "Snowflake")], ["sliding ice moves pieces one tile"]),
    "reef": T("Coral Reef", "Fluid and dreamy",
        dict(bg="#04202e", surface="#0a3a4a", primary="#1fd8c8", primaryDark="#0a7a70", secondary="#ff7a8a", secondaryDark="#b02a40",
             accent="#a8fff4", danger="#ff4a5a", text="#e8fffb", onPrimary="#022a26"),
        [("#a8fff4", "#1fd8c8", "#05605a"), ("#ffc0c8", "#ff6a7a", "#8a1a2a"), ("#d8ff9a", "#8ad83a", "#2a5a0a"), ("#ffe8a0", "#ffb83a", "#8a5000")],
        "pearl", "Baloo 2", False, (1.2, "cubic-bezier(.3,1.25,.5,1)", "bubbles"),
        [("seaweed", "Seaweed", 2), ("bubble", "Air Bubble", 1), ("coral", "Coral Wall", 3)],
        [("pearl", "Pearl"), ("shell", "Sea Shell")], ["currents push pieces", "bubbles float upward"]),
    "carnival": T("Haunted Carnival", "Creepy but fun",
        dict(bg="#120a1e", surface="#26163a", primary="#7aff4a", primaryDark="#2a9a10", secondary="#b04aff", secondaryDark="#5a1aa0",
             accent="#ff4a6a", danger="#ff2a4a", text="#f4ecff", onPrimary="#0e2a04"),
        [("#a8f0ff", "#3ab8e8", "#0a4a6a"), ("#ffa8c0", "#ff3a6a", "#7a0a2a"), ("#c8ffa0", "#7aff4a", "#2a7a10"), ("#fff0a0", "#ffc21f", "#8a5a00")],
        "neon", "Creepster", True, (1.0, "cubic-bezier(.2,1.6,.4,1)", "flicker"),
        [("ghost", "Wandering Ghost", 2), ("bulb", "Broken Light", 1), ("wheel", "Spinning Wheel", 3)],
        [("ticket", "Ghost Ticket"), ("token", "Haunted Token")], ["ghosts swap two random pieces", "broken lights hide tiles"]),
    "crystal": T("Crystal Caves", "Sparkly and satisfying",
        dict(bg="#120a24", surface="#241640", primary="#b06aff", primaryDark="#5a20b0", secondary="#3ac8ff", secondaryDark="#0a6aa8",
             accent="#ffffff", danger="#ff4a7a", text="#f6f0ff", onPrimary="#ffffff"),
        [("#c8e8ff", "#3a9aff", "#0a3a8a"), ("#ffc8f0", "#e04ad0", "#6a0a5a"), ("#c8ffd8", "#2ad890", "#0a6a3a"), ("#fff4c8", "#ffd23a", "#8a6000")],
        "crystal", "Righteous", False, (.95, "cubic-bezier(.25,1.4,.5,1)", "sparkle"),
        [("barrier", "Crystal Barrier", 3), ("geode", "Geode", 2), ("echochain", "Echo Chain", 2)],
        [("rarecrystal", "Rare Crystal"), ("prism", "Prism Shard")], ["barriers break only to special matches"]),
    "desert": T("Desert Oasis", "Hot and dry until the water",
        dict(bg="#2a1606", surface="#4a2a10", primary="#1fc8c0", primaryDark="#0a7a74", secondary="#ffb83a", secondaryDark="#a0600a",
             accent="#ffe08a", danger="#e8402a", text="#fff6e0", onPrimary="#022a28"),
        [("#a8f8ff", "#1fc8e0", "#05606a"), ("#ffc0a8", "#e8603a", "#7a2008"), ("#e0f08a", "#9ab82a", "#3a4a08"), ("#fff0a0", "#ffc21f", "#8a5000")],
        "sand", "Lilita One", False, (1.05, "cubic-bezier(.3,1.3,.5,1)", "haze"),
        [("sand", "Sand Cover", 2), ("cactus", "Cactus Blocker", 3), ("mirage", "Mirage Tile", 1)],
        [("jewel", "Desert Jewel"), ("waterdrop", "Oasis Drop")], ["sand covers a tile every 3 moves", "mirages fake a match"]),
    "steampunk": T("Steampunk Factory", "Mechanical and rhythmic",
        dict(bg="#1a140e", surface="#33281c", primary="#e0a040", primaryDark="#8a5a10", secondary="#c86a3a", secondaryDark="#7a3410",
             accent="#ffe0a0", danger="#e83a2a", text="#fff2dc", onPrimary="#2a1600"),
        [("#c8e0f0", "#5a90c0", "#1a3a5a"), ("#ffb8a8", "#d04a3a", "#6a1408"), ("#d8e8a0", "#8aa83a", "#3a4a10"), ("#ffe0a0", "#e0a040", "#7a4a00")],
        "brass", "Rye", True, (1.3, "cubic-bezier(.4,1.15,.5,1)", "gears"),
        [("gear", "Moving Gear", 2), ("vent", "Steam Vent", 1), ("machine", "Locked Machine", 3)],
        [("cog", "Brass Cog"), ("steamcore", "Steam Core")], ["gears rotate a row each turn"]),
    "nebula": T("Cosmic Nebula", "Epic, vast and magical",
        dict(bg="#07061a", surface="#18143a", primary="#ff4ab8", primaryDark="#9a1a6a", secondary="#4a8aff", secondaryDark="#1a3ab0",
             accent="#ffd65a", danger="#ff4a5a", text="#f4f0ff", onPrimary="#ffffff"),
        [("#c8d8ff", "#4a7aff", "#122a8a"), ("#ffc0e8", "#ff4ab8", "#7a0a5a"), ("#c8ffe0", "#3ad8a0", "#0a6a4a"), ("#fff0b0", "#ffd65a", "#8a6a00")],
        "cosmic", "Audiowide", False, (1.1, "cubic-bezier(.3,1.35,.5,1)", "stars"),
        [("asteroid", "Asteroid", 3), ("blackhole", "Black Hole", 2), ("satellite", "Dead Satellite", 2)],
        [("starfrag", "Star Fragment"), ("planetcore", "Planet Core")], ["black holes pull pieces in", "gravity flips each 10 moves"]),
}


# ---- label colours: pick whichever ink reads best on each button colour (WCAG contrast) -------------
def _rgb(h):
    h = h.lstrip("#"); h = "".join(c * 2 for c in h) if len(h) == 3 else h
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def lum(h):
    c = [v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4 for v in _rgb(h)]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + .05) / (lb + .05)


INK = "#1a1020"
for _t in THEMES.values():
    _p = _t["palette"]
    for _role in ("primary", "secondary", "danger"):
        _p["on" + _role.capitalize()] = max(("#ffffff", INK), key=lambda ink: contrast(ink, _p[_role]))
    _p["onSurface"] = max(("#ffffff", INK), key=lambda ink: contrast(ink, _p["surface"]))
    _p["ghost"] = _p["accent"] if contrast(_p["accent"], _p["bg"]) >= 3 else _p["text"]  # outline/label colour for ghost buttons
