import pygame as pg
from os.path import join
import pygame.freetype as font
from json import load

pg.init()

# Pngs dir and file paths
PNGS_DIR_PATH = "pngs"
PNGS_PATHS = {
    "player_sprite_sheet.png": join(PNGS_DIR_PATH, "player_sprite_sheet.png"),
    "player_flip_sprite_sheet.png": join(PNGS_DIR_PATH, "player_flip_sprite_sheet.png"),
    "stage_1_sprite_sheet.png": join(PNGS_DIR_PATH, "stage_1_sprite_sheet.png")
}

# Ttfs dir and data
TTFS_DIR_PATH = "ttfs"
TTFS_DATA = {
    "cg_pixel_3x5_mono.ttf": {
        "path": join(TTFS_DIR_PATH, "cg_pixel_3x5_mono.ttf"),
        "h": 5,
        "w": 3,
    },
}

# Jsons dir and file paths
JSONS_DIR_PATH = "jsons"
JSONS_PATHS = {
    "player_animation.json": join(JSONS_DIR_PATH, "player_animation.json"),
    "fire_animation.json": join(JSONS_DIR_PATH, "fire_animation.json"),
    "stage1_empty_game.json": join(JSONS_DIR_PATH, "stage1_empty_game.json"),
    "stage1_wide_empty_game.json": join(JSONS_DIR_PATH, "stage1_wide_empty_game.json"),
}

# Constants
TILE_S = 16
# FPS = 1
FPS = 60
NATIVE_W = 320
NATIVE_H = 176

# Pg constants
NATIVE_SURF = pg.Surface((NATIVE_W, NATIVE_H))
NATIVE_RECT = NATIVE_SURF.get_rect()
DEBUG_SURF = pg.Surface((NATIVE_W, NATIVE_H))
DEBUG_SURF.set_colorkey("red")
DEBUG_RECT = DEBUG_SURF.get_rect()
CLOCK = pg.time.Clock()
EVENTS = [pg.KEYDOWN, pg.KEYUP, pg.QUIT]
