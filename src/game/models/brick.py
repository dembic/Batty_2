# src/game/models/brick.py
import random

from src.game.config import *

class Brick(arcade.Sprite):
    def __init__(self, x, y, health=None, points=10, color=None, scale=SCALE):
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

        if color is None:
            color = random.choice(list(COLOR_TO_COLUMN.keys()))

        self.brick_color = color
        self.color_column = COLOR_TO_COLUMN.get(color, 0)

        self.is_indestructible = (color == "gray")

        if self.is_indestructible:
            self.health = None
            self.max_health = None
            self.points = 0
        else:
            self.health = health if health is not None else COLOR_TO_HEALTH[color]
            self.max_health = self.health
            self.points = points

        self.is_destroyed = False

        # Назначаем первая текстура здоровая
        self.update_texture()

    def update_texture(self):
        if self.is_indestructible:
            row = 0
        else:
            row = 5 - (self.health - 1)
            row = max(1, min(row, 5))

        index = self.color_column + row * 7
        self.texture = self.textures[index]

    def hit(self):
        if self.is_indestructible:
            return 0

        if not self.is_destroyed and self.health > 0:
            self.health -= 1
            if self.health > 0:
                self.update_texture()
            else:
                self.is_destroyed = True
                self.remove_from_sprite_lists()
                return self.points
        return 0



