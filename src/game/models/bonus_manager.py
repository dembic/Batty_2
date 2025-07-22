# src/game/models/bonus_manager.py

import random
from src.game.config import *
from .bonus_laser import BonusLaser
from .bonus_lives import BonusLives

class BonusManager:
    def __init__(self):
        self.bonuses = arcade.SpriteList()
        self.timer_bonus = 0
        self.game_view = None

    def maybe_drop_bonus(self, x, y):
        if self.timer_bonus > 0:
            return
        bonus_type = []

        # Только если лазер не активен — можно дропать лазер
        if not self.game_view.laser_active:
            bonus_type.append(BonusLaser)

        # Только если нет мультибола — можно дропать мультибол
        if len(self.game_view.extra_balls) == 0:
            from .bonus_multi_ball import BonusMultiBall
            bonus_type.append(BonusMultiBall)

        # Всегда можно дропать бонус жизни
        bonus_type.append(BonusLives)

        # Шанс для дропа
        if bonus_type and random.random() < 0.2:
            bonus_type = random.choice(bonus_type)
            bonus = bonus_type(x, y)
            self.bonuses.append(bonus)
            self.timer_bonus = 10


    def update(self, delta_time, game_view):
        self.bonuses.update()
        self.timer_bonus -= delta_time
        self.game_view = game_view

        for bonus in self.bonuses:
            if arcade.check_for_collision(bonus, game_view.paddle):
                bonus.apply(game_view)
                bonus.remove_from_sprite_lists()
