# src/game/models/bonus_multi_ball.py
from .bonus import Bonus

class BonusMultiBall(Bonus):
    def __init__(self, x, y):
        super().__init__("assets/images/ball.png", x, y)

    @staticmethod
    def apply(game_view):
        """Создать два дополнительных мяча"""
        angles = [-30, 30]
        for angle in angles:
            new_ball = game_view.ball.clone(angle_offset_degrees=angle)
            game_view.extra_balls.append(new_ball)
            game_view.sprite_list.append(new_ball)