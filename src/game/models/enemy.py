# src/game/models/enemy.py

from enum import Enum, auto
import arcade
from src.game.config import *

class EnemyState(Enum):
    IDLE = auto()
    FLYING = auto()
    ATTACK = auto()
    DEATH = auto()

class Enemy(arcade.Sprite):
    def __init__(self, x, y, scale=1.0):
        super().__init__(scale=scale)
        self.center_x = x
        self.center_y = y

        self.state = EnemyState.IDLE
        self.frame_index = 0
        self.frame_time = 0.1
        self.timer = 0
        self.attack_cooldown = 0
        self.attack_finished = False
        self.active_bomb = None  # Ссылка на бомбу

        self.sprite_sheet = arcade.SpriteSheet(ENEMY_TEXTURE)
        self.textures_all = self.sprite_sheet.get_texture_grid(
            size=(81, 64),
            columns=22,
            count=22,
            margin=(0, 0, 0, 0)
        )

        self.texture_idle = self.textures_all[0:4]
        self.texture_flying = self.textures_all[4:8]
        self.texture_attack = self.textures_all[8:16]
        self.texture_death = self.textures_all[16:22]

        self.texture = self.texture_idle[0]

        self.target = None  # Paddle
        self.throw_bomb_callback = None  # Колбэк для спавна бомбы

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        if self.state != EnemyState.DEATH and self.target:
            # Движение с задержкой к ракетке
            self.center_x += (self.target.center_x - self.center_x) * delta_time * 0.1

        self.reduce_cooldowns(delta_time)

    def update_animation(self, delta_time: float = 1 / 60, *args, **kwargs):
        self.timer += delta_time
        if self.timer < self.frame_time:
            return

        self.timer = 0

        if self.state == EnemyState.IDLE:
            frames = self.texture_idle
        elif self.state == EnemyState.FLYING:
            frames = self.texture_flying
        elif self.state == EnemyState.ATTACK:
            frames = self.texture_attack
        elif self.state == EnemyState.DEATH:
            frames = self.texture_death
        else:
            frames = [self.texture]

        if frames:
            self.frame_index += 1
            if self.frame_index >= len(frames):
                self.frame_index = 0

                if self.state == EnemyState.ATTACK:
                    self.attack_finished = True
                    if self.throw_bomb_callback:
                        self.throw_bomb_callback(self.center_x, self.bottom, self)
                        # После атаки можно вернуть в idle или flying
                    self.start_idle()

            self.texture = frames[self.frame_index]

    def on_brick_destroyed(self):
        if self.state != EnemyState.DEATH and self.attack_cooldown <= 0 and self.active_bomb is None:
            self.start_attack()
            self.attack_cooldown = 2.0  # задержка перед следующей атакой

    def reduce_cooldowns(self, delta_time):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time

    def start_idle(self):
        self.state = EnemyState.IDLE
        self.frame_index = 0
        self.timer = 0

    def start_flying(self):
        self.state = EnemyState.FLYING
        self.frame_index = 0
        self.timer = 0

    def start_attack(self):
        self.state = EnemyState.ATTACK
        self.frame_index = 0
        self.timer = 0
        self.attack_finished = False

    def start_death(self):
        self.state = EnemyState.DEATH
        self.frame_index = 0
        self.timer = 0
