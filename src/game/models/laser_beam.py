# src/game/models/laser_beam.py

from src.game.config import *

class LaserBeam(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(LASER_BEAM_PNG, scale=1.0)
        self.center_x = x
        self.center_y = y
        self.change_y = SPEED_LASER_UP # Скорость лазера вверх

    def update(self, delta_time: float = 1/60, *args, **kwargs) -> None:
        self.center_y += self.change_y * delta_time
        if self.top > SCREEN_HEIGHT:
            self.remove_from_sprite_lists()
