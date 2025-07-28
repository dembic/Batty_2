# src/game/models/enemy_manager.py

from src.game.config import *
from src.game.models.enemy import Enemy, EnemyState
from src.game.models.bomb import Bomb



class EnemyManager:
    def __init__(self, paddle):
        self.sound = arcade.load_sound(BOMB_TO_PADDLE_SOUND)
        self.ball = None
        self.enemies = arcade.SpriteList()
        self.bombs = arcade.SpriteList()
        self.paddle = paddle
        
        
    def set_ball(self, ball):
        self.ball = ball
        
    def spawn_enemy(self, x, y):
        enemy = Enemy(x, y)
        enemy.target = self.paddle
        enemy.start_idle()
        enemy.throw_bomb_callback = self.throw_bomb
        self.enemies.append(enemy)

    def throw_bomb(self, x, y, enemy):
        if enemy.active_bomb is None:
            bomb = Bomb(x, y + 15)
            bomb.owner = enemy
            enemy.active_bomb = bomb
            self.bombs.append(bomb)

    def update(self, delta_time):
        for enemy in self.enemies:
            enemy.reduce_cooldowns(delta_time)
        self.enemies.update()
        self.enemies.update_animation(delta_time)
        self.bombs.update()
        for bomb in self.bombs:
            bomb.update_animation(delta_time)

        self.remove_dead()

    def update_bombs(self, lives_display=None):
        for bomb in self.bombs:
            bomb.update()

            if bomb.bottom < 0:
                bomb.remove_from_sprite_lists()
                if bomb.owner:
                    bomb.owner.active_bomb = None
                continue

            if lives_display and bomb.collides_with_sprite(self.paddle) and not self.paddle.is_blinking:
                bomb.remove_from_sprite_lists()
                if bomb.owner:
                    bomb.owner.active_bomb = None
                arcade.play_sound(self.sound, volume=SOUND_VOLUME)
                self.paddle.start_blinking(use_scale=False)
                lives_display.lose_life()
                self.ball.attach_to_paddle(self.paddle)

    def draw(self):
        self.enemies.draw()
        self.bombs.draw()

    def on_brick_destroyed(self):
        for enemy in self.enemies:
            enemy.on_brick_destroyed()



    def clear(self):
        self.enemies = arcade.SpriteList()
        self.bombs = arcade.SpriteList()

    def remove_dead(self):
        for enemy in self.enemies:
            if  enemy.state == EnemyState.DEATH:
                enemy.remove_from_sprite_lists()