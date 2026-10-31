# Single source of truth for where each asset lives under assets/ (by filename prefix).
CATEGORIES = {  # folder: (title, prefixes) — order = order in assets/index.html
    "pieces": ("Pieces", ("piece_",)),
    "collection": ("Piece collection", ("col_",)),
    "events": ("Event pieces", ("evt_",)),
    "seasons": ("Seasonal pieces", ("sea_",)),
    "sweets": ("Sweet Shop", ("sw_",)),
    "bombs": ("Bombs", ("bomb_", "bombc_")),  # nested: bombs/<design>/ (metal tiers), bombs/colored/<design>/  # nested: sweets/<category>/<design>/
    "board": ("Board & objects", ("board_", "cell_", "crate", "launcher")),
    "hud": ("HUD & currency", ("hud_", "slot_", "progress_", "life_", "shard", "star_", "combo_")),
    "buttons": ("Buttons & controls", ("btn_", "icon_", "toggle_")),
    "panels": ("Panels & banners", ("panel_", "ribbon")),
    "modes": ("Mode tiles", ("mode_",)),
    "map": ("Campaign map", ("node_",)),
    "rewards": ("Rewards & badges", ("badge_", "stamp_")),
}


def folder_for(name):
    if name.startswith("sw_"):  # sw_<category>_<design>_<i>.svg → sweets/<category>/<design>
        _, cat, design, _ = name.split("_", 3)
        return f"sweets/{cat}/{design}"
    if name.startswith("bombc_"):  # bombc_<design>_<i>.svg → bombs/colored/<design>
        return f"bombs/colored/{name.split('_')[1]}"
    if name.startswith("bomb_"):  # bomb_<design>_<i>.svg → bombs/<design>
        return f"bombs/{name.split('_')[1]}"
    for folder, (_, prefixes) in CATEGORIES.items():
        if name.startswith(prefixes):
            return folder
    raise ValueError(f"no category for {name}: add its prefix to tools/layout.py")
