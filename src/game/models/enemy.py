# src/game/models/enemy.py

from enum import Enum, auto
import math, random

import arcade.math

from src.game.config import *

class EnemyState(Enum):
    IDLE = auto()
    FLYING = auto()
    ATTACK = auto()
    ATTACK_RECOVER = auto()
    DEATH = auto()

class Enemy(arcade.Sprite):
    def __init__(self, x, y, scale=1.0):
        super().__init__(scale=float(scale))
        self.center_x = x
        self.center_y = y

        self.state = EnemyState.IDLE
        self.frame_index = 0
        self.frame_time = 0.1
        self.timer = 0
        self.attack_cooldown = 0
        self.attack_finished = False
        self.active_bomb = None  # Ссылка на бомбу
        self.patrol_direction = 1
        self.patrol_timer = 0.0
        self.base_y = y
        self.flight_timer = 0.0
        self.flight_amplitude_current = random.uniform(10,40)
        self.flight_amplitude_target = self.flight_amplitude_current
        self.flight_period_timer = 0.0
        self.flight_period_duration = 3.0
        self.flight_frequency = random.uniform(0.3,0.6)
        self.brick_destroyed_recently = True
        self.attack_start_y = y
        self.attack_target_y = y - 80 # На сколько пикселей нырять при атаке
        self.attack_move_timer = 0.0
        self.attack_move_duration = 0.5 # Время за которое он переместится вниз


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
        self.reduce_cooldowns(delta_time)

        if self.state == EnemyState.DEATH:
            return

        if self.brick_destroyed_recently:

            if self.target:
                # Следует за ракеткой
                dx = self.target.center_x - self.center_x
                self.mirror_towards(dx)
                self.center_x += dx * delta_time * 0.6
                self.state = EnemyState.ATTACK


            self.patrol_timer += delta_time
            if self.patrol_timer > 2.0:
                self.brick_destroyed_recently = False
                self.patrol_timer = 0.0
        else:
            # Патрулирует влево-вправо
            self.center_x += self.patrol_direction * 50 * delta_time
            if self.left < 0 or self.right > SCREEN_WIDTH:
                self.patrol_direction *= -1

            # Отзеркаливание спрайта
            self.mirror_towards(self.patrol_direction)

            # Шанс сбросить бомбу при патруле
            if self.state in (EnemyState.IDLE, EnemyState.FLYING) and self.attack_cooldown <= 0 and self.active_bomb is None:
                if random.random() < 0.005: # 0.5% процента каждую итерацию
                    self.start_attack()
                    self.attack_cooldown = 3.0

            # Плавно вниз при атаке
            if self.state == EnemyState.ATTACK:
                self.attack_move_timer += delta_time
                t = min(self.attack_move_timer / self.attack_move_duration, 1.0)
                self.center_y = arcade.math.lerp(self.attack_start_y, self.attack_target_y, t)
                return
            elif self.state == EnemyState.ATTACK_RECOVER:
                self.attack_move_timer += delta_time
                t = min(self.attack_move_timer / self.attack_move_duration, 1.0)
                self.center_y = arcade.math.lerp(self.attack_target_y, self.base_y, t)
                if t >= 1.0:
                    self.start_idle()
                return

            # Плавное вертикальное движение по синусойде
            self.flight_period_timer += delta_time
            if self.flight_period_timer >= self.flight_period_duration:
                self.flight_period_timer = 0.0
                self.flight_amplitude_current = self.flight_amplitude_target
                self.flight_amplitude_target = random.uniform(10,40)

            t = self.flight_period_timer / self.flight_period_duration
            amplitude = arcade.math.lerp(self.flight_amplitude_current, self.flight_amplitude_target, t)

            self.flight_timer += delta_time
            self.center_y = self.base_y + math.sin(self.flight_timer * self.flight_frequency * 2 * math.pi) * amplitude

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
                    self.start_attack_recover()

            self.texture = frames[self.frame_index]

    def mirror_towards(self, dx: float):
        if dx > 0:
            self.scale = -abs(self.scale) if isinstance(self.scale, (int, float)) else (-abs(self.scale[0]),
                                                                                       self.scale[1])
        elif dx < 0:
            self.scale = abs(self.scale) if isinstance(self.scale, (int, float)) else (abs(self.scale[0]),
                                                                                        self.scale[1])
    def on_brick_destroyed(self):
        self.brick_destroyed_recently = True
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
        self.attack_start_y = self.center_y
        self.attack_target_y = self.center_y - 80
        self.attack_move_timer = 0.0

    def start_attack_recover(self):
        self.state = EnemyState.ATTACK_RECOVER
        self.attack_move_timer = 0.0

    def start_death(self):
        self.state = EnemyState.DEATH
        self.frame_index = 0
        self.timer = 0
