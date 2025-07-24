# src/game/models/bomb.py

from src.game.config import *

class Bomb(arcade.Sprite):
    def __init__(self, x, y, texture=None, scale=0.8):
        super().__init__(texture or BOMB_TEXTURE, scale)
        self.center_x = x
        self.center_y = y
        self.change_y = SPEED_ENEMY_BOMB
        self.owner = None

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.center_y += self.change_y * delta_time * 0.7
        if self.bottom < 0:
            self.remove_from_sprite_lists()
            if self.owner:
                self.owner.active_bomb = None