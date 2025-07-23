# src/game/models/enemy.py
import arcade
from enum import Enum, auto
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

        self.sprite_sheet = arcade.SpriteSheet(ENEMY_TEXTURE)
        self.textures_all = self.sprite_sheet.get_texture_grid(
            size=(81, 64),
            columns=22,
            count=22,  # максимум 22
            margin=(0, 0, 0, 0)
        )

        self.texture_idle = self.textures_all[0:4]
        self.texture_flying = self.textures_all[4:8]
        self.texture_attack = self.textures_all[8:16]
        self.texture_death = self.textures_all[16:22]

        self.texture = self.texture_idle[0]

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

        if not frames:
            return

        self.frame_index = (self.frame_index + 1) % len(frames)
        self.texture = frames[self.frame_index]

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

    def start_death(self):
        self.state = EnemyState.DEATH
        self.frame_index = 0
        self.timer = 0

