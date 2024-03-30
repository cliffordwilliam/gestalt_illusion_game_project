from constants import *


class Camera:
    def __init__(self, owner):
        self.rect = pg.FRect(0, 0, NATIVE_W, NATIVE_H)
        self.lerp_weight = 0.1
        self.target = [0, 0]
        self.owner = owner

    def set_target(self, value):
        self.target = value

    def update(self, dt):
        # Update horizontal position
        self.rect.x = pg.math.lerp(
            self.rect.x,
            self.target[0] - (NATIVE_W // 2),
            self.lerp_weight
        )
        if abs(self.rect.x) < 0.001:
            self.rect.x = 0

        # Update vertical position
        self.rect.y = pg.math.lerp(
            self.rect.y,
            self.target[1] - (NATIVE_H // 2),
            self.lerp_weight
        )
        if abs(self.rect.y) < 0.001:
            self.rect.y = 0

        # # Limit cam to stay in room rect
        self.rect.clamp_ip(self.owner.room.rect)
