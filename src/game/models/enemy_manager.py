# src/game/models/enemy_manager.py

from src.game.config import *
from src.game.models.enemy import Enemy, EnemyState
from src.game.models.bomb import Bomb


class EnemyManager:
    def __init__(self, paddle):
        self.enemies = arcade.SpriteList()
        self.bombs = arcade.SpriteList()
        self.paddle = paddle

    def spawn_enemy(self, x, y):
        enemy = Enemy(x, y)
        enemy.target = self.paddle
        enemy.start_idle()
        enemy.throw_bomb_callback = self.throw_bomb
        self.enemies.append(enemy)

    def throw_bomb(self, x, y, enemy):
        if enemy.active_bomb is None:
            bomb = Bomb(x, y)
            bomb.owner = enemy
            enemy.active_bomb = bomb
            self.bombs.append(bomb)

    def update(self, delta_time):
        for enemy in self.enemies:
            enemy.reduce_cooldowns(delta_time)
        self.enemies.update()
        self.enemies.update_animation(delta_time)
        self.bombs.update()
        self.remove_dead()

    def update_bombs(self):
        for bomb in self.bombs:
            bomb.update()

            # Бомба улетела вниз
            if bomb.bottom < 0:
                bomb.remove_from_sprite_lists()
                if hasattr(bomb, "owner") and bomb.owner:
                    bomb.owner.active_bomb = None

            # Столкновение с ракеткой
            if arcade.check_for_collision(bomb, self.paddle):
                bomb.remove_from_sprite_lists()
                if hasattr(bomb, "owner") and bomb.owner:
                    bomb.owner.active_bomb = None
                # Тут вызываем повреждения

    def draw(self):
        self.enemies.draw()
        self.bombs.draw()

    def on_brick_destroyed(self):
        for enemy in self.enemies:
            enemy.on_brick_destroyed()

    def check_bomb_collision(self, paddle):
        for bomb in self.bombs:
            if bomb.collides_with_sprite(paddle):
                if bomb.owner:
                    bomb.owner.active_bomb = None
                bomb.remove_from_sprite_lists()
                # Реакция попадания по ракетке
                if hasattr(paddle, "on_hit"):
                    paddle.on_hit()

    def clear(self):
        self.enemies = arcade.SpriteList()

    def remove_dead(self):
        for enemy in self.enemies:
            if  enemy.state == EnemyState.DEATH:
                enemy.remove_from_sprite_lists()