# src/game/models/bonus_lives.py

from src.game.config import *
from .bonus import Bonus

class BonusLives(Bonus):
    def __init__(self, x, y):
        super().__init__(LIVES_PNG, x, y)

    @staticmethod
    def apply(game_view):
        game_view.lives_display.gain_life()
        print("Bonus Lives: +1 life")