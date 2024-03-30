from constants import *
from actors.player import Player
from nodes.camera import Camera
from nodes.room import Room


class PlayerTest:
    def __init__(self, game):
        # region Font for debug
        self.font = font.Font(
            TTFS_DATA["cg_pixel_3x5_mono.ttf"]["path"],
            TTFS_DATA["cg_pixel_3x5_mono.ttf"]["h"]
        )
        self.font_h = TTFS_DATA["cg_pixel_3x5_mono.ttf"]["h"]
        self.font_w = TTFS_DATA["cg_pixel_3x5_mono.ttf"]["w"]
        # endregion Font for debug

        # Game
        self.game = game

        # region Camera
        self.camera = Camera(self)
        # endregion Camera

        # region Prepare testing room
        self.room = Room(self, self.game, "stage1_wide_empty_game.json")
        # endregion Prepare testing room

        # region Instance player to be tested
        self.player = Player(self, self.game)
        # endregion Instance player to be tested

        self.camera.set_target(self.player.camera_anchor)

    def on_player_hit_door(self, door):
        pass

    def event(self, event):
        self.player.event(event)

    def draw(self):
        # Fill native surface color to have good contrast for player
        NATIVE_SURF.fill("black")

        # Draw bg
        self.room.draw_bg()

        # region Draw grid in debug
        if self.game.is_debug:
            for i in range(20):
                offset = TILE_S * i
                xd = (offset - self.camera.rect.x) % NATIVE_W
                yd = (offset - self.camera.rect.y) % NATIVE_H
                pg.draw.line(NATIVE_SURF, "grey4", (xd, 0), (xd, NATIVE_H))
                pg.draw.line(NATIVE_SURF, "grey4", (0, yd), (NATIVE_W, yd))
            xd = -self.camera.rect.x % NATIVE_W
            yd = -self.camera.rect.y % NATIVE_H
            pg.draw.line(NATIVE_SURF, "grey8", (xd, 0), (xd, NATIVE_H))
            pg.draw.line(NATIVE_SURF, "grey8", (0, yd), (NATIVE_W, yd))
            self.font.render_to(
                NATIVE_SURF, (xd + self.font_w, yd + self.font_h), f"{
                    int(self.camera.rect.x - 1) // NATIVE_W + 1}{
                    int(self.camera.rect.y - 1) // NATIVE_H + 1}", "white"
            )
            # endregion

        # Draw player
        self.player.draw()

        # Draw fg
        self.room.draw_fg()

    def update(self, dt):
        # region Update player
        self.player.update(dt)
        # endregion Update player

        # region Update camera
        self.camera.update(dt)
        # endregion Update camera

        # region Update all bg sprites actors
        self.room.update(dt)
        # endregion Update all bg sprites actors
