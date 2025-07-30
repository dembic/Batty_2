# src/game/models/laser_beam.py
from arcade import SpriteSheet

from src.game.config import *

class LaserBeam(arcade.Sprite):
    def __init__(self, x, y, scale=1.0):
        super().__init__(scale=scale)
        self.center_x = x
        self.center_y = y
        self.change_y = SPEED_LASER_UP # Скорость лазера вверх

        # Загружаем спрайтшит и нарезаем
        self.sprite_sheet = SpriteSheet(LASER_BEAM_SPRITESHEET)
        self.textures = self.sprite_sheet.get_texture_grid(
            size=(41, 41),
            columns=3,
            count=9
        )

        self.frame_index =0
        self.frame_time = 0.1
        self.timer = 0

        self.texture = self.textures[0]

    def update(self, delta_time: float = 1/60, *args, **kwargs) -> None:
        self.center_y += self.change_y * delta_time
        if self.top > SCREEN_HEIGHT:
            self.remove_from_sprite_lists()

    def update_animation(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.timer += delta_time
        if self.timer >= self.frame_time:
            self.timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.textures)
            self.texture = self.textures[self.frame_index]