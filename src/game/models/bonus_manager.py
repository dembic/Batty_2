# src/game/models/bonus_manager.py

import random
from arcade import SpriteList
from src.game.config import *
from .bonus_multi_ball import BonusMultiBall

class BonusManager:
    def __init__(self):
        self.bonuses = SpriteList()
        self.bonus_cooldown = 0

    def maybe_drop_bonus(self, x, y):
        if self.bonus_cooldown <= 0:
            if random.random() < 0.2: # 20% Шанс
                self.bonuses.append(BonusMultiBall(x, y))
                self.bonus_cooldown = 15

    def update(self, delta_time, game_view):

        if self.bonus_cooldown > 0:
            self.bonus_cooldown -= delta_time

        self.bonuses.update()
        for bonus in self.bonuses:
            if arcade.check_for_collision(bonus, game_view.paddle):
                bonus.apply(game_view)
                bonus.remove_from_sprite_lists()
