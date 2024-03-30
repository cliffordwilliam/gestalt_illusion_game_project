from constants import *
from nodes.animator import Animator
from nodes.kinematic import Kinematic


class Player:
    def __init__(self, world, game):
        # region Debug stuff
        self.frame_counter = 0
        self.collided_cell_name = ""
        # endregion Debug stuff

        # region Font for debug
        self.font = font.Font(
            TTFS_DATA["cg_pixel_3x5_mono.ttf"]["path"],
            TTFS_DATA["cg_pixel_3x5_mono.ttf"]["h"]
        )
        self.font_h = TTFS_DATA["cg_pixel_3x5_mono.ttf"]["h"]
        self.font_w = TTFS_DATA["cg_pixel_3x5_mono.ttf"]["w"]
        # endregion Font for debug

        # region world
        self.world = world
        # endregion world

        # region Game
        self.game = game
        # endregion Game

        # region Name
        self.name = "Player"
        # endregion Name

        # region Inputs
        self.is_left_pressed = 0
        self.is_right_pressed = 0
        self.is_down_pressed = False
        # endregion Inputs

        # region Player sprite sheets
        self.sprite_sheet = pg.image.load(
            PNGS_PATHS["player_sprite_sheet.png"])
        self.sprite_sheet_flip = pg.image.load(
            PNGS_PATHS["player_flip_sprite_sheet.png"])
        self.current_sprite_sheet = self.sprite_sheet
        # endregion Player sprite sheets

        # region Surface offset
        self.surface_offset_x = 21
        self.surface_offset_y = 14
        # endregion Surface offset

        # region Read json animation data
        self.aniamtion_data = {}
        with open(JSONS_PATHS["player_animation.json"], "r") as data:
            self.aniamtion_data = load(data)
        # endregion Read json animation data

        # region init starting region
        self.region = self.aniamtion_data["idle"]["frames_list"][0]["region"]
        # endregion init starting region

        # region Player state
        self.state = "idle"
        # endregion Player state

        # region Player facing direction
        self.facing_direction = 1
        self.old_facing_direction = self.facing_direction
        # endregion Player facing direction

        # region Player direction input
        self.direction = 0
        # endregion Player direction

        # region Animator node
        self.animator = Animator(self, self.aniamtion_data, "idle")
        # endregion Animator node

        # region Rect
        self.rect = pg.FRect(TILE_S, 0, 6, 31)
        # endregion Rect

        # region movement
        self.max_run = 0.09
        self.run_lerp_weight = 0.2
        self.max_fall = 0.270
        self.normal_gravity = 0.000533
        self.heavy_gravity = 0.001066
        self.gravity = self.normal_gravity
        self.jump_vel = -0.240
        self.velocity = pg.math.Vector2()
        self.remainder_x = 0
        self.remainder_y = 0
        # endregion movement

        # region Kinematic
        self.kinematic = Kinematic(game, self, world)
        # endregion Kinematic

        self.camera_anchor = [
            self.rect.x + (self.facing_direction * (2 * TILE_S)),
            self.rect.y
        ]

    # Called by kinematic
    def on_collide(self, cell):
        # Found door?
        self.collided_cell_name = cell["name"]
        if cell["name"] == "Door":
            self.world.on_player_hit_door(cell)
            self.velocity.y = 0
            self.kinematic.remainder_y = 0

    def event(self, event):
        if event.type == pg.KEYDOWN:
            # Just pressed left
            if event.key == self.game.key_bindings["left"]:
                # Set is pressed left 1
                self.is_left_pressed = 1

            # Just pressed right
            if event.key == self.game.key_bindings["right"]:
                # Set is pressed right 1
                self.is_right_pressed = 1

            # Just pressed down
            if event.key == self.game.key_bindings["down"]:
                # Set is pressed down true
                self.is_down_pressed = True

            # Just pressed jump
            elif event.key == self.game.key_bindings["jump"]:
                # Idle, run crouch can jump
                if self.state in [
                    "idle",
                    "run",
                    "crouch"
                ]:
                    # Exit up
                    self.set_state("up")

        elif event.type == pg.KEYUP:
            # Just released left
            if event.key == self.game.key_bindings["left"]:
                # Set is released left 0
                self.is_left_pressed = 0

            # Just released right
            if event.key == self.game.key_bindings["right"]:
                # Set is released right 0
                self.is_right_pressed = 0

            # Just released down
            if event.key == self.game.key_bindings["down"]:
                # Set is released down false
                self.is_down_pressed = False

            # Just released jump
            elif event.key == self.game.key_bindings["jump"]:
                # Idle, run crouch can jump
                if self.state == "up":
                    self.gravity = self.heavy_gravity

    def draw(self):
        # region Draw player to native surface
        xds = (self.rect.x - self.surface_offset_x) - self.world.camera.rect.x
        yds = (self.rect.y - self.surface_offset_y) - self.world.camera.rect.y
        NATIVE_SURF.blit(
            self.current_sprite_sheet, (xds, yds), self.region
        )
        # endregion Draw player to native surface

        # region Debug draw
        if self.game.is_debug == True:
            # region Draw fps
            self.font.render_to(
                DEBUG_SURF,
                (self.font_w, self.font_h),
                f'fps: {int(CLOCK.get_fps())}',
                "white",
                "black"
            )
            # endregion Draw fps

            # region Draw frame counter
            self.font.render_to(
                DEBUG_SURF,
                (self.font_w, self.font_h * 3),
                f'frame: {self.frame_counter}',
                "white",
                "black"
            )
            # endregion Draw frame counter

            # region Draw current animation
            self.font.render_to(
                DEBUG_SURF,
                (self.font_w, self.font_h * 5),
                f'current animation: {self.animator.current_animation}',
                "white",
                "black"
            )
            # endregion Draw current animation

            # region Draw collision
            self.font.render_to(
                DEBUG_SURF,
                (self.font_w, self.font_h * 7),
                f'collision: {self.collided_cell_name}',
                "white",
                "black"
            )
            # endregion Draw collision

            # region Draw is on floor
            self.font.render_to(
                DEBUG_SURF,
                (self.font_w, self.font_h * 9),
                f'is on floor: {self.kinematic.is_on_floor}',
                "white",
                "black"
            )
            # endregion Draw is on floor

            # region Draw is on wall
            self.font.render_to(
                DEBUG_SURF,
                (self.font_w, self.font_h * 11),
                f'is on wall: {self.kinematic.is_on_wall}',
                "white",
                "black"
            )
            # endregion Draw is on wall

            # region Draw is on wall
            self.font.render_to(
                DEBUG_SURF,
                (self.font_w, self.font_h * 13),
                f'state: {self.state}',
                "white",
                "black"
            )
            # endregion Draw is on wall

            # region Draw my rect in tu tile
            # pos -> tu
            x_tu = (self.rect.centerx // TILE_S) - self.world.room.x_tu
            y_tu = (self.rect.centery // TILE_S) - self.world.room.y_tu
            # tu -> xds
            xds = ((x_tu + self.world.room.x_tu) * TILE_S) - \
                self.world.camera.rect.x
            yds = ((y_tu + self.world.room.y_tu) * TILE_S) - \
                self.world.camera.rect.y
            pg.draw.lines(
                DEBUG_SURF,
                "aqua",
                True,
                [
                    (xds, yds),
                    (xds + TILE_S, yds),
                    (xds + TILE_S, yds + TILE_S),
                    (xds, yds + TILE_S),
                ]
            )
            # endregion Draw my rect in tu tile
        # endregion Debug draw

    def update(self, dt):
        # Update debug stuff
        self.collided_cell_name = ""

        # region Update animation node
        self.animator.update(dt)
        # endregion Update animation node

        # region Debug update
        if self.game.is_debug == True:
            self.frame_counter += 1
            if self.frame_counter == 61:
                self.frame_counter = 0
        # endregion Debug update

        # region Update velocity with gravity
        self.velocity.y += self.gravity * dt
        self.velocity.y = min(self.velocity.y, self.max_fall)
        # endregion Update velocity with gravity

        # region Update x velocity with direction
        self.velocity.x = pg.math.smoothstep(
            self.velocity.x,
            self.direction * self.max_run,
            self.run_lerp_weight
        )
        if abs(self.velocity.x) < 0.001:
            self.velocity.x = 0
        # endregion Update x velocity with direction

        # region Move
        self.kinematic.move(dt)
        # endregion Move

        # region Update camera anchor
        self.camera_anchor[0] = self.rect.x + \
            (self.facing_direction * (2 * TILE_S))
        self.camera_anchor[1] = self.rect.y
        # endregion Update camera anchor

        # region Get horizontal input direction
        self.direction = self.is_right_pressed - self.is_left_pressed
        # endregion Get horizontal input direction

        # region Update facing direction and old facing direction
        if self.direction != 0:
            self.old_facing_direction = self.facing_direction
            self.facing_direction = self.direction
        # endregion Update facing direction and old facing direction

        # Idle
        if self.state == "idle":
            # region Exit to run
            if self.direction != 0 and not self.kinematic.is_on_wall:
                self.set_state("run")
            # endregion Exit to run

            # region Exit to crouch
            elif self.is_down_pressed:
                self.set_state("crouch")
            # endregion Exit to crouch

            # region Exit to down
            elif not self.kinematic.is_on_floor:
                self.set_state("down")
            # endregion Exit to down

            # Exit jump in just pressed event input

        # Run
        elif self.state == "run":
            # region Exit to idle
            if self.direction == 0 or self.kinematic.is_on_wall:
                self.set_state("idle")
            # endregion Exit to idle

            # region Exit to crouch
            elif self.is_down_pressed:
                self.set_state("crouch")
            # endregion Exit to crouch

            # region Exit to down
            elif not self.kinematic.is_on_floor:
                self.set_state("down")
            # endregion Exit to down

            # Exit jump in just pressed event input

            # region Handle turning - frame perfect
            if self.facing_direction == 1:
                self.current_sprite_sheet = self.sprite_sheet
            elif self.facing_direction == -1:
                self.current_sprite_sheet = self.sprite_sheet_flip
            if self.old_facing_direction != self.facing_direction:
                self.animator.set_current_animation("turn")
            # endregion Handle turning - frame perfect

        # Crouch
        elif self.state == "crouch":
            # region Exit to run
            if not self.is_down_pressed and self.direction != 0:
                self.set_state("run")
            # endregion Exit to run

            # region Exit to idle
            elif not self.is_down_pressed and self.direction == 0:
                self.set_state("idle")
            # endregion Exit to idle

            # Exit jump in just pressed event input

            # region Cannot move direction 0
            self.direction = 0
            # endregion Cannot move direction 0

        # Up
        elif self.state == "up":
            # region Exit to down
            if self.velocity.y > 0:
                self.set_state("down")
            # endregion Exit to down

        # Down
        elif self.state == "down":
            # region Exit to run
            if self.kinematic.is_on_floor and self.direction != 0:
                self.set_state("run")
            # endregion Exit to run

            # region Exit to idle
            if self.kinematic.is_on_floor and self.direction == 0:
                self.set_state("idle")
            # endregion Exit to idle

            # region Exit to crouch
            if self.kinematic.is_on_floor and self.is_down_pressed:
                self.set_state("crouch")
            # endregion Exit to crouch

    # Set state
    def set_state(self, value):
        old_state = self.state
        self.state = value

        # From idle
        if old_state == "idle":
            # To run
            if self.state == "run":
                # region Handle turning
                if self.facing_direction == 1:
                    self.current_sprite_sheet = self.sprite_sheet
                elif self.facing_direction == -1:
                    self.current_sprite_sheet = self.sprite_sheet_flip
                if self.old_facing_direction == self.facing_direction:
                    # Play run transition animation
                    self.animator.set_current_animation("idle_to_run")
                elif self.old_facing_direction != self.facing_direction:
                    # Play turn to run transition animation
                    self.animator.set_current_animation("turn")
                # endregion Handle turning

            # To crouch
            elif self.state == "crouch":
                # region Play crouch animation
                self.animator.set_current_animation("crouch")
                # endregion Play crouch animation

            # To up
            elif self.state == "up":
                # region Set jump vel
                self.velocity.y = self.jump_vel
                # endregion Set jump vel

                # region Play up animation
                self.animator.set_current_animation("up")
                # endregion Play up animation

            # To down
            elif self.state == "down":
                # Remove grav build up
                self.velocity.y = 0

                # region set Heavy gravity
                self.gravity = self.heavy_gravity
                # endregion set Heavy gravity

                # region Play up down transition animation
                self.animator.set_current_animation("up_to_down")
                # endregion Play up down transition animation

        # From run
        elif old_state == "run":
            # To idle
            if self.state == "idle":
                # region Play run_to_idle animation
                self.animator.set_current_animation("run_to_idle")
                # endregion Play run_to_idle animation

            # To crouch
            elif self.state == "crouch":
                # region Play crouch animation
                self.animator.set_current_animation("crouch")
                # endregion Play crouch animation

            # To up
            elif self.state == "up":
                # region Set jump vel
                self.velocity.y = self.jump_vel
                # endregion Set jump vel

                # region Play up animation
                self.animator.set_current_animation("up")
                # endregion Play up animation

            # To down
            elif self.state == "down":
                # Remove grav build up
                self.velocity.y = 0

                # region set Heavy gravity
                self.gravity = self.heavy_gravity
                # endregion set Heavy gravity

                # region Play up down transition animation
                self.animator.set_current_animation("up_to_down")
                # endregion Play up down transition animation

        # From crouch
        elif old_state == "crouch":
            # To idle
            if self.state == "idle":
                # region Play idle animation
                self.animator.set_current_animation("crouch_to_idle")
                # endregion Play idle animation

            # To run
            elif self.state == "run":
                # region Handle turning
                if self.facing_direction == 1:
                    self.current_sprite_sheet = self.sprite_sheet
                elif self.facing_direction == -1:
                    self.current_sprite_sheet = self.sprite_sheet_flip
                if self.old_facing_direction == self.facing_direction:
                    # Play run transition animation
                    self.animator.set_current_animation("idle_to_run")
                elif self.old_facing_direction != self.facing_direction:
                    # Play turn to run transition animation
                    self.animator.set_current_animation("turn")
                # endregion Handle turning

            # To up
            elif self.state == "up":
                # region Set jump vel
                self.velocity.y = self.jump_vel
                # endregion Set jump vel

                # region Play up animation
                self.animator.set_current_animation("up")
                # endregion Play up animation

        # From up
        elif old_state == "up":
            # To down
            if self.state == "down":
                # region set Heavy gravity
                self.gravity = self.heavy_gravity
                # endregion set Heavy gravity

                # region Play up down transition animation
                self.animator.set_current_animation("up_to_down")
                # endregion Play up down transition animation

        # From down
        elif old_state == "down":
            # region Reset gravity
            self.gravity = self.normal_gravity
            # endregion Reset gravity

            # To idle
            if self.state == "idle":
                # region Play land animation
                self.animator.set_current_animation("land")
                # endregion Play land animation

            # To run
            if self.state == "run":
                # region Handle turning
                if self.facing_direction == 1:
                    self.current_sprite_sheet = self.sprite_sheet
                elif self.facing_direction == -1:
                    self.current_sprite_sheet = self.sprite_sheet_flip
                if self.old_facing_direction == self.facing_direction:
                    # Play run transition animation
                    self.animator.set_current_animation("idle_to_run")
                elif self.old_facing_direction != self.facing_direction:
                    # Play turn to run transition animation
                    self.animator.set_current_animation("turn")
                # endregion Handle turning

            # To crouch
            elif self.state == "crouch":
                # region Play crouch animation
                self.animator.set_current_animation("crouch")
                # endregion Play crouch animation
