from constants import *
from scenes.player_test import PlayerTest
from actors.fire import Fire


class Game:
    def __init__(self, initial_scene):
        # Global debug flag
        self.is_debug = False

        # All game actors (enemies, animated bg, chest, items, ...)
        self.actors = {
            "Fire": Fire
        }

        # Resolution setting, window size and surf
        self.resolution = 4
        self.window_w = NATIVE_W * self.resolution
        self.window_h = NATIVE_H * self.resolution
        self.window_surf = pg.display.set_mode((self.window_w, self.window_h))

        # All game scenes, starting scene and current scene
        self.scenes = {
            "PlayerTest": PlayerTest
        }
        self.initial_scene = initial_scene
        self.current_scene = self.scenes[self.initial_scene](self)

        # Keybinds
        self.key_bindings = {
            "up": pg.K_UP,
            "down": pg.K_DOWN,
            "left": pg.K_LEFT,
            "right": pg.K_RIGHT,
            "enter": pg.K_RETURN,
            "pause": pg.K_ESCAPE,
            "jump": pg.K_c,
        }

    def set_scene(self, value):
        # Takes scene class name and update current scene
        self.current_scene = self.scenes[value](self)


# Instance game
game = Game("PlayerTest")

# Main loop
while 1:
    # region Get dt
    dt = CLOCK.tick(FPS)
    # TODO: slow down time
    # dt /= 4
    # endregion Get dt

    # Get event
    for event in pg.event.get(EVENTS):
        # region Window quit
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        # endregion Window quit

        # region Debug toggle
        if event.type == pg.KEYUP:
            if event.key == pg.K_0:
                game.is_debug = not game.is_debug
        # endregion Debug toggle

        # region Current scene event
        game.current_scene.event(event)
        # endregion Current scene event

    # region Clear native and debug surface
    NATIVE_SURF.fill("red")
    DEBUG_SURF.fill("red")
    # endregion Clear native and debug surface

    # region Current scene draw
    game.current_scene.draw()
    # endregion Current scene draw

    # region Current scene update
    game.current_scene.update(dt)
    # endregion Current scene update

    # region Draw debug surface on native
    NATIVE_SURF.blit(DEBUG_SURF, (0, 0))
    # endregion Draw debug surface on native

    # region Native to window and update window
    pg.transform.scale(NATIVE_SURF, (game.window_w,
                       game.window_h), game.window_surf)
    pg.display.update()
    # endregion Native to window and update window
