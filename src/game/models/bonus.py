# src/game/models/bonus.py

from src.game.config import *

class Bonus(arcade.Sprite):
    def __init__(self,image, x, y):
        super().__init__(image, scale=1.0)
        self.center_x = x
        self.center_y = y
        self.change_y = BONUS_SPEED

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.center_y += self.change_y * delta_time