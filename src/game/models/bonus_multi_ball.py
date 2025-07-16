# src/game/models/bonus_multi_ball.py
from .bonus import Bonus
from src.game.config import *

class BonusMultiBall(Bonus):
    def __init__(self, x, y):
        super().__init__("assets/images/ball.png", x, y)


    def apply(self, game_view):
        """Создать два дополнительных мяча"""
        print("MultiBall bonus activated!")

        if not game_view.ball:
            print("No base ball to clone from.")
            return

        for _ in range(2):
            new_ball = game_view.ball.clone()
            new_ball.center_x = game_view.center_x
            new_ball.center_y = game_view.center_y
            game_view.extra_balls.append(new_ball)
            game_view.sprite_list.append(new_ball)