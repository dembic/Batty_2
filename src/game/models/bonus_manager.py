# src/game/models/bonus_manager.py

import random
from arcade import SpriteList
from src.game.config import *
from .bonus_multi_ball import BonusMultiBall

#from .bonus_multi_ball import BonusMultiBall

class BonusManager:
    def __init__(self):
        self.bonuses = SpriteList()

    def maybe_drop_bonus(self, x, y):
        if random.random() < 0.8: # 20% Шанс
            self.bonuses.append(BonusMultiBall(x, y))

    def update(self, delta_time, game_view):
        self.bonuses.update()
        for bonus in self.bonuses:
            if arcade.check_for_collision(bonus, game_view.paddle):
                bonus.apply(game_view)
                bonus.remove_from_sprite_lists()
