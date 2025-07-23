# src/game/models/enemy_manager.py

from src.game.config import *
from src.game.models.enemy import Enemy, EnemyState


class EnemyManager:
    def __init__(self):
        self.enemies = arcade.SpriteList()

    def spawn_enemy(self, x, y, kind="default"):
        enemy = Enemy(x, y)
        if kind == "default":
            enemy.start_idle()
        # Можно расширить типы: flying, boss, etc.
        self.enemies.append(enemy)

    def update(self, delta_time, game_view):
        self.enemies.update()
        self.enemies.update_animation(delta_time)

    def draw(self):
        self.enemies.draw()

    def clear(self):
        self.enemies = arcade.SpriteList()

    def remove_dead(self):
        for enemy in self.enemies:
            if  enemy.state == EnemyState.DEATH:
                enemy.remove_from_sprite_lists()