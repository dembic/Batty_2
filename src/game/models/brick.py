# src/game/models/brick.py
import random
from src.game.config import *

class Brick(arcade.Sprite):
    def __init__(self, x, y, health=1, points=10, scale=SCALE):
        super().__init__()
        sprite_sheet = arcade.SpriteSheet("assets/images/brick_spritesheet.png")
        self.textures = sprite_sheet.get_texture_grid(
            size=(54,23),
            columns=7,
            count=42,
            margin=(0,0,0,0)
        )

        self.position = (x, y)
        self.scale = scale
        self.center_x = x
        self.center_y = y
        self.health = health
        self.max_health = health
        self.points = points
        self.is_destroyed = False

        self.cur_texture_index = random.randint(7,10)
        self.texture = self.textures[self.cur_texture_index]

        self.width = 54 * scale
        self.height = 23 * scale

    def hit(self):
        if not self.is_destroyed and self.health > 0:
            self.health -= 1
            if self.health > 0:
                self.cur_texture_index = self.max_health - self.health
                if self.cur_texture_index < len(self.textures):
                    self.texture = self.textures[self.cur_texture_index]
            elif self.health <= 0:
                self.is_destroyed = True
                self.alpha = 0
                return self.points
        return 0

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        if self.is_destroyed:
            self.alpha = 0


