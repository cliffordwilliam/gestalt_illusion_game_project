from constants import *


class Room:
    def __init__(self, owner, game, name):
        # Get owner
        self.owner = owner

        # Get game
        self.game = game

        # Get room name
        self.name = name

        # Use room name to read json
        self.room_data = {}
        with open(JSONS_PATHS[self.name], 'r') as data:
            self.room_data = load(data)

        # Room bg layers, no 0, not a coordinate list
        self.bg_layers = self.room_data["BG_LAYERS"]

        # Room collision layer, this one layer has 0, 0 = air, it is a coordinate list
        self.collision_layer = self.room_data["COLLISION_LAYER"]

        # The collision draw layer removed all 0, it is used for drawing only
        self.collision_draw_layer = [x for x in self.collision_layer if x != 0]

        # Room fg layer, no 0, not a coordinate list
        self.fg_layers = self.room_data["FG_LAYERS"]

        # Room rect, room camera limit
        self.rect = self.room_data["ROOM_RECT"]
        self.x_tu = self.rect[0] // TILE_S
        self.y_tu = self.rect[1] // TILE_S
        self.w_tu = self.rect[2] // TILE_S
        self.h_tu = self.rect[3] // TILE_S

        # Room background names that it needs to draw
        self.bg1 = self.room_data["BG1"]
        self.bg2 = self.room_data["BG2"]
        self.bg3 = self.room_data["BG3"]
        self.bg4 = self.room_data["BG4"]

        # Load this room sprite sheet
        self.sprite_sheet_png_name = self.room_data["SPRITE_SHEET_PNG_NAME"]
        self.sprite_sheet_path = PNGS_PATHS[self.sprite_sheet_png_name]
        self.sprite_sheet_surf = pg.image.load(
            self.sprite_sheet_path).convert_alpha()

        # Check if there are any actors in bg layers
        for i in range(len(self.bg_layers)):
            room = self.bg_layers[i]
            for j in range(len(room)):
                sprite = room[j]
                if sprite != 0:
                    name = sprite["name"]
                    x = sprite["xds"]
                    y = sprite["yds"]
                    if name in self.game.actors:
                        actor = self.game.actors[name](
                            self.game, self.owner.camera, self.sprite_sheet_surf, x, y)
                        self.bg_layers[i][j] = {"name": "actor", "obj": actor}

    def change_room_to(self, name):
        # Get new room name
        self.name = name

        # Use room name to read json
        self.room_data = {}
        with open(JSONS_PATHS[self.name], 'r') as data:
            self.room_data = load(data)

        # Room bg layers, no 0, not a coordinate list
        self.bg_layers = self.room_data["BG_LAYERS"]

        # Room collision layer, this one layer has 0, 0 = air, it is a coordinate list
        self.collision_layer = self.room_data["COLLISION_LAYER"]

        # The collision draw layer removed all 0, it is used for drawing only
        self.collision_draw_layer = [x for x in self.collision_layer if x != 0]

        # Room fg layer, no 0, not a coordinate list
        self.fg_layers = self.room_data["FG_LAYERS"]

        # Room rect, room camera limit
        self.rect = self.room_data["ROOM_RECT"]
        self.x_tu = self.rect[0] // TILE_S
        self.y_tu = self.rect[1] // TILE_S
        self.w_tu = self.rect[2] // TILE_S
        self.h_tu = self.rect[3] // TILE_S

        # Room background names that it needs to draw
        self.bg1 = self.room_data["BG1"]
        self.bg2 = self.room_data["BG2"]
        self.bg3 = self.room_data["BG3"]
        self.bg4 = self.room_data["BG4"]

        # Load this room sprite sheet
        self.sprite_sheet_png_name = self.room_data["SPRITE_SHEET_PNG_NAME"]
        self.sprite_sheet_path = PNGS_PATHS[self.sprite_sheet_png_name]
        self.sprite_sheet_surf = pg.image.load(
            self.sprite_sheet_path).convert_alpha()

        # Check if there are any actors in bg layers
        for i in range(len(self.bg_layers)):
            room = self.bg_layers[i]
            for j in range(len(room)):
                sprite = room[j]
                if sprite != 0:
                    name = sprite["name"]
                    x = sprite["xds"]
                    y = sprite["yds"]
                    if name in self.game.actors:
                        actor = self.game.actors[name](
                            self.game, self.owner.camera, self.sprite_sheet_surf, x, y)
                        self.bg_layers[i][j] = {"name": "actor", "obj": actor}

    def draw_bg(self):
        # Each names are unique ids
        if self.bg1 == "sky":
            x = (-self.owner.camera.rect.x * 0.05) % NATIVE_W
            NATIVE_SURF.blit(self.sprite_sheet_surf, (x, 0), (0, 0, 320, 179))
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x - NATIVE_W, 0), (0, 0, 320, 179))

        if self.bg2 == "clouds":
            x = (-self.owner.camera.rect.x * 0.1) % NATIVE_W
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x, 0), (0, 176, 320, 160))
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x - NATIVE_W, 0), (0, 176, 320, 160))

        if self.bg3 == "trees":
            x = (-self.owner.camera.rect.x * 0.5) % NATIVE_W
            # 1
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x, 32), (320, 448, 80, 160))
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x - NATIVE_W, 32), (320, 448, 80, 160))
            # 2
            NATIVE_SURF.blit(self.sprite_sheet_surf, (x + 96, 64),
                             (320, 448, 80, 160))
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x + 96 - NATIVE_W, 64), (320, 448, 80, 160))
            # 3
            NATIVE_SURF.blit(self.sprite_sheet_surf, (x + 160, 32),
                             (320, 448, 80, 160))
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x + 160 - NATIVE_W, 32), (320, 448, 80, 160))
            # 4
            NATIVE_SURF.blit(self.sprite_sheet_surf, (x + 224, 16),
                             (320, 448, 80, 160))
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x + 224 - NATIVE_W, 16), (320, 448, 80, 160))

        if self.bg4 == "blue_glow":
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (0, 48), (0, 512, 320, 128))
        # endregion

        # region Draw all bg sprites
        for room in self.bg_layers:
            for item in room:
                if item["name"] == "actor":
                    item["obj"].draw()
                    continue
                # Only update sprites that are in view
                if (self.owner.camera.rect.x - item["region"][2] <= item["xds"] < self.owner.camera.rect.right) and (self.owner.camera.rect.y - item["region"][3] <= item["yds"] < self.owner.camera.rect.bottom):
                    xd = item["xds"] - self.owner.camera.rect.x
                    yd = item["yds"] - self.owner.camera.rect.y
                    NATIVE_SURF.blit(self.sprite_sheet_surf,
                                     (xd, yd), item["region"])
        # endregion Draw all bg sprites

    def draw_fg(self):
        # region Draw all collision sprites
        for item in self.collision_draw_layer:
            # Only update sprites that are in view
            if (self.owner.camera.rect.x - item["region"][2] <= item["xds"] < self.owner.camera.rect.right) and (self.owner.camera.rect.y - item["region"][3] <= item["yds"] < self.owner.camera.rect.bottom):
                xd = item["xds"] - self.owner.camera.rect.x
                yd = item["yds"] - self.owner.camera.rect.y
                NATIVE_SURF.blit(self.sprite_sheet_surf,
                                 (xd, yd), item["region"])
        # endregion Draw all collision sprites

        # region Draw all fg sprites
        for room in self.fg_layers:
            for item in room:
                # Only update sprites that are in view
                if (self.owner.camera.rect.x - item["region"][2] <= item["xds"] < self.owner.camera.rect.right) and (self.owner.camera.rect.y - item["region"][3] <= item["yds"] < self.owner.camera.rect.bottom):
                    xd = item["xds"] - self.owner.camera.rect.x
                    yd = item["yds"] - self.owner.camera.rect.y
                    NATIVE_SURF.blit(self.sprite_sheet_surf,
                                     (xd, yd), item["region"])
        # endregion all fg sprites

    def update(self, dt):
        # region Update all bg sprites actors
        for room in self.bg_layers:
            for item in room:
                if item["name"] == "actor":
                    item["obj"].update(dt)
        # endregion Update all bg sprites actors
