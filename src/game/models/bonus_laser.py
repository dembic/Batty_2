# src/game/models/bonus_laser.py

from src.game.config import *
from .bonus import Bonus
from ..hud.floating_text import FloatingText


class BonusLaser(Bonus):
    def __init__(self, x, y):
        super().__init__(BONUS_LASER_PNG, x, y)

    @staticmethod
    def apply(game_view):
        if game_view.laser_active:
            print("Bonus laser ignored - already active")
            return
        print("Bonus laser active")
        game_view.laser_active = True
        game_view.laser_timer = 10.0

        # Floating text
        x = game_view.paddle.center_x
        y = game_view.paddle.top + 20
        game_view.floating_texts.append(
            FloatingText("LASERS!", x, y, color=arcade.color.RED)
        )
