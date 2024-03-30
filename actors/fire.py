from constants import *
from nodes.animator import Animator


class Fire:
    def __init__(self, game, camera, sprite_sheet_surface, x, y):
        # region Position
        self.x = x
        self.y = y
        # endregion Position

        # region Game
        self.game = game
        # endregion Game

        # region Camera
        self.camera = camera
        # endregion Camera

        # region Name
        self.name = "Fire"
        # endregion Name

        # region Fire sprite sheets
        self.sprite_sheet = sprite_sheet_surface
        # endregion Fire sprite sheets

        # region Read json animation data
        self.aniamtion_data = {}
        with open(JSONS_PATHS["fire_animation.json"], "r") as data:
            self.aniamtion_data = load(data)
        # endregion Read json animation data

        # region init starting region
        self.region = self.aniamtion_data["burn"]["frames_list"][0]["region"]
        self.w = self.region[2]
        self.h = self.region[2]
        # endregion init starting region

        # region Animator node
        self.animator = Animator(self, self.aniamtion_data, "burn")
        # endregion Animator node

    def draw(self):
        # region Draw player to native surface
        # Only update sprites that are in view
        if not (self.camera.rect.x - self.w <= self.x < self.camera.rect.right) and not (self.camera.rect.y - self.h <= self.y < self.camera.rect.bottom):
            return

        # Draw in camera offset position
        xds = self.x - self.camera.rect.x
        yds = self.y - self.camera.rect.y
        NATIVE_SURF.blit(self.sprite_sheet, (xds, yds), self.region)
        # endregion Draw player to native surface

    def update(self, dt):
        # region Update animation node
        self.animator.update(dt)
        # endregion Update animation node
