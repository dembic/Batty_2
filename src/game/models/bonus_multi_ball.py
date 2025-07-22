# src/game/models/bonus_multi_ball.py
from src.game.config import *
from .bonus import Bonus
from ..hud.floating_text import FloatingText


class BonusMultiBall(Bonus):
    def __init__(self, x, y):
        super().__init__(BONUS_BALL_PNG, x, y)

    @staticmethod
    def apply(game_view):

        if len(game_view.extra_balls) > 0:
            print("MultiBall bonus ignored - already active")
            return
        print("MultiBall bonus active")

        original_ball = game_view.ball
        angles = [-30, 30]
        for angle in angles:
            new_ball = game_view.ball.clone(angle_offset_degrees=angle)
            game_view.extra_balls.append(new_ball)
            game_view.sprite_list.append(new_ball)

        # Floating text
        x = game_view.paddle.center_x
        y = game_view.paddle.top + 20
        game_view.floating_texts.append(
            FloatingText("MULTI BALL", x, y, color=arcade.color.ORANGE)
        )