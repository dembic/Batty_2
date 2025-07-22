# src/game/models/bonus_lives.py

from src.game.config import *
from .bonus import Bonus
from ..hud.floating_text import FloatingText


class BonusLives(Bonus):
    def __init__(self, x, y):
        super().__init__(LIVES_PNG, x, y)
        self.center_x = x
        self.center_y = y

    def update(self, delta_time: float = 1/60, *args, **kwargs):
        super().update()
        self.center_y += self.change_y * delta_time

    def apply(self, game_view):
        if game_view.lives_display.current_lives < MAX_LIVES:
            game_view.lives_display.gain_life()
            platform_x = game_view.paddle.center_x
            platform_y = game_view.paddle.top + 20
            game_view.floating_texts.append(
                FloatingText("+1 LIFE", platform_x, platform_y)
            )
