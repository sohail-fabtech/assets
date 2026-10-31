# Single source of truth for where each asset lives under assets/ (by filename prefix).
CATEGORIES = {  # folder: (title, prefixes) — order = order in assets/index.html
    "pieces": ("Pieces", ("piece_",)),
    "collection": ("Piece collection", ("col_",)),
    "events": ("Event pieces", ("evt_",)),
    "seasons": ("Seasonal aura pieces", ("sea_",)),
    "board": ("Board & objects", ("board_", "cell_", "crate", "launcher")),
    "hud": ("HUD & currency", ("hud_", "slot_", "progress_", "life_", "shard", "star_", "combo_")),
    "buttons": ("Buttons & controls", ("btn_", "icon_", "toggle_")),
    "panels": ("Panels & banners", ("panel_", "ribbon")),
    "modes": ("Mode tiles", ("mode_",)),
    "map": ("Campaign map", ("node_",)),
    "rewards": ("Rewards & badges", ("badge_", "stamp_")),
}


def folder_for(name):
    for folder, (_, prefixes) in CATEGORIES.items():
        if name.startswith(prefixes):
            return folder
    raise ValueError(f"no category for {name}: add its prefix to tools/layout.py")
