# src/game/models/brick.py
import random

from src.game.config import *

class Brick(arcade.Sprite):
    def __init__(self, x, y, health=None, points=10, scale=SCALE):
        super().__init__()
        sprite_sheet = arcade.SpriteSheet("assets/images/brick_spritesheet.png")
        self.textures = sprite_sheet.get_texture_grid(
            size=(54,22),
            columns=7,
            count=42,
            margin=(0,0,0,0)
        )

        self.position = (x, y)
        self.scale = scale
        self.center_x = x
        self.center_y = y
        self.health = health
        self.max_health = self.health
        self.points = points
        self.is_destroyed = False

        self.cur_texture_index = random.randint(7,14)
        self.texture = self.textures[self.cur_texture_index]

        #print(f"Loaded {len(self.textures)} textures, Brick at ({x}, {y}) with health {self.health}")

        self.width = 54 * scale
        self.height = 22 * scale

    def hit(self):
        if not self.is_destroyed and self.health > 0:
            self.health -= 1
            if self.health > 0:
                self.cur_texture_index = int(((self.health -1) / self.max_health) * (len(self.textures) -1))
                self.texture = self.textures[self.cur_texture_index]
            elif self.health <= 0:
                self.is_destroyed = True
                self.remove_from_sprite_lists()
                return self.points
        return 0

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        if self.is_destroyed:
            self.alpha = 0


