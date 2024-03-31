from constants import *


class Camera:
    def __init__(self, owner):
        self.rect = pg.FRect(0, 0, NATIVE_W, NATIVE_H)
        self.lerp_weight = 0.1
        self.target = [0, 0]
        self.owner = owner
        self.target_x = 0
        self.target_y = 0

    def set_target(self, value):
        self.target = value

    def update(self, dt):
        # Prevent target to be in a pos where cam is outside of room x
        self.target_x = self.target[0]
        left = self.owner.room.rect[0]
        right = self.owner.room.rect[0] + self.owner.room.rect[2]
        left += NATIVE_W // 2
        right -= NATIVE_W // 2
        self.target_x = max(min(self.target_x, right), left)

        # Prevent target to be in a pos where cam is outside of room y
        self.target_y = self.target[1]
        top = self.owner.room.rect[1]
        bottom = self.owner.room.rect[1] + self.owner.room.rect[3]
        top += NATIVE_H // 2
        bottom -= NATIVE_H // 2
        self.target_y = max(min(self.target_y, bottom), top)

        # Update horizontal position
        self.rect.x = pg.math.lerp(
            self.rect.x,
            self.target_x - (NATIVE_W // 2),
            self.lerp_weight
        )
        if abs(self.rect.x) < 0.001:
            self.rect.x = 0

        # Update vertical position
        self.rect.y = pg.math.lerp(
            self.rect.y,
            self.target_y - (NATIVE_H // 2),
            self.lerp_weight
        )
        if abs(self.rect.y) < 0.001:
            self.rect.y = 0

    def draw(self):
        # Debug draw target
        if self.owner.game.is_debug:
            x = self.target_x - self.rect.x
            y = self.target_y - self.rect.y
            pg.draw.circle(DEBUG_SURF, "yellow", (x, y), 2)
