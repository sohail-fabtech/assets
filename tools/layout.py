# Single source of truth for where every asset lives under assets/.
# All pieces sit under assets/pieces/<collection>/<sub>/...; everything else is UI grouped by purpose.
CATEGORIES = {  # top-level folder: title — order = order in assets/index.html
    "pieces": "Pieces",
    "board": "Board & objects",
    "hud": "HUD & currency",
    "buttons": "Buttons & controls",
    "panels": "Panels & banners",
    "modes": "Mode tiles",
    "map": "Campaign map",
    "rewards": "Rewards & badges",
    "ui": "Chrome: frames, ribbons, headers, tags, badges",
    "scenes": "World scenes",
}
UI = {  # flat UI folders by filename prefix
    "board": ("board_", "cell_", "crate", "launcher"),
    "hud": ("hud_", "slot_", "progress_", "life_", "shard", "star_", "combo_"),
    "buttons": ("btn_", "icon_", "toggle_"),
    "panels": ("panel_", "ribbon"),
    "modes": ("mode_",),
    "map": ("node_",),
    "rewards": ("badge_", "stamp_"),
}


def folder_for(name):
    p = name[:-4].split("_")  # drop .svg
    if name.startswith("piece_"):   return f"pieces/core/{p[1]}"                      # piece_box_cyan
    if name.startswith("col_"):     return f"pieces/collection/{p[1]}"                # col_jelly_0
    if name.startswith("evt_"):     return f"pieces/events/{p[1]}"                    # evt_pumpkin_0
    if name.startswith("sw_"):      return f"pieces/sweets/{p[1]}/{p[2]}"             # sw_bakery_donut_0
    if name.startswith("bombc_"):   return f"pieces/bombs/colored/{p[1]}"             # bombc_mini_0
    if name.startswith("bomb_"):    return f"pieces/bombs/metal/{p[1]}"               # bomb_mini_iron
    if name.startswith("blk_"):     return f"pieces/blockers/{p[1]}"                  # blk_crate_3
    if name.startswith("ui_"):      return f"buttons/{p[1]}"                          # ui_volcano_pill-primary_normal
    if name.startswith("lv_"):      return f"pieces/levels/{p[1]}/{p[2]}"             # lv_volcano_obstacles_lava_2
    if name.startswith("lvb_"):     return f"board/levels/{p[1]}"                     # lvb_volcano_board
    if name.startswith("chr_"):     return f"ui/chrome/{p[1]}"                        # chr_brand_close, chr_shared_chest
    if name.startswith("scn_"):     return f"scenes/{p[1]}"                           # scn_volcano_card
    if name.startswith("th_"):      return f"pieces/themes/{'_'.join(p[1:-2])}/{p[-2]}"  # th_orchid_dusk_gem_0
    if name.startswith("thb_"):     return f"board/themes/{'_'.join(p[1:-1])}"        # thb_lagoon_board
    if name.startswith("sea_"):                                                        # sea_autumn_acorn_0 / _board / _emblem
        if p[2] == "board":  return "board/seasons"
        if p[2] == "emblem": return "rewards/seasons"
        return f"pieces/seasons/{p[1]}/{p[2]}"
    for folder, prefixes in UI.items():
        if name.startswith(prefixes):
            return folder
    raise ValueError(f"no folder for {name}: add its prefix to tools/layout.py")


if __name__ == "__main__":  # self-check
    assert folder_for("piece_box_cyan.svg") == "pieces/core/box"
    assert folder_for("th_orchid_dusk_gem_0.svg") == "pieces/themes/orchid_dusk/gem"
    assert folder_for("thb_ember_glow_cell.svg") == "board/themes/ember_glow"
    assert folder_for("sea_winter_board.svg") == "board/seasons"
    assert folder_for("sea_spring_tulip_2.svg") == "pieces/seasons/spring/tulip"
    assert folder_for("sw_bakery_donut_1.svg") == "pieces/sweets/bakery/donut"
    assert folder_for("bomb_mega_gold.svg") == "pieces/bombs/metal/mega"
    assert folder_for("blk_ice_2.svg") == "pieces/blockers/ice"
    assert folder_for("ui_volcano_pill-primary_pressed.svg") == "buttons/volcano"
    assert folder_for("lv_reef_collectibles_pearl_0.svg") == "pieces/levels/reef/collectibles"
    assert folder_for("lvb_nebula_board.svg") == "board/levels/nebula"
    assert folder_for("chr_brand_ribbon.svg") == "ui/chrome/brand"
    assert folder_for("scn_reef_card.svg") == "scenes/reef"
    assert folder_for("icon_home.svg") == "buttons"
    print("layout ok")
