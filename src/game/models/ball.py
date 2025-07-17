# src/game/models/ball.py
from src.game.config import *
import math

class Ball(arcade.Sprite):
    """Класс мяча в игре Batty"""

    def __init__(self):
        super().__init__("assets/images/ball.png", scale=1.0)
        self.change_x = 0
        self.change_y = 0
        self.previous_y = 0
        self.rotation_speed = 180  # градусов в секунду
        self.is_attached = True
        self.parent = None
        self.sound_bounce = arcade.load_sound(SOUND_BOUNCE)
        self.life_timer = None
        self.visible_timer = 0

    def clone(self, angle_offset_degrees=0):
        clone = Ball()
        clone.center_x = self.center_x
        clone.center_y = self.center_y
        clone.parent = self.parent
        clone.is_attached = False
        clone.life_timer = 10

        speed = math.hypot(self.change_x, self.change_y)
        current_angle = math.atan2(self.change_y, self.change_x)
        new_angle = current_angle + math.radians(angle_offset_degrees)

        clone.change_x = speed * math.cos(new_angle)
        clone.change_y = speed * math.sin(new_angle)

        return clone

    def attach_to_paddle(self, paddle):
        """Привязать мяч к платформе"""
        self.center_x = paddle.center_x
        self.center_y = paddle.top + self.height / 2
        self.previous_y = self.center_y
        self.is_attached = True

    def launch(self):
        """Запустить мяч вверх"""
        self.is_attached = False
        self.change_x = BALL_NORMAL_SPEED
        self.change_y = BALL_NORMAL_SPEED

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        """Обновление положения мяча"""
        # Прикреплен к платформе
        if self.is_attached and self.parent and hasattr(self.parent, "paddle"):
            paddle = self.parent.paddle
            self.center_x = paddle.center_x
            self.center_y = paddle.top + self.height / 2
            return

        # Таймер жизни бонусного мяча
        if self.life_timer is not None:
            self.life_timer -= delta_time

            # ✨ Мигание за 3 секунды до исчезновения
            if self.life_timer <= 3:
                self.visible_timer += delta_time
                if self.visible_timer >= 0.2:
                    self.visible = not self.visible
                    self.visible_timer = 0

            if self.life_timer <= 0:
                self.remove_from_sprite_lists()
                return

        # Стандартное движение
        self.previous_y = self.center_y
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        self.angle = (self.angle + self.rotation_speed * delta_time) % 360

        # Стенки
        if self.left <= 0:
            self.left = 0
            self.change_x *= -1
        elif self.right >= SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
            self.change_x *= -1

        if self.top >= SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
            self.change_y *= -1

    def check_collision(self, paddle):
        """Проверка и отскок от платформы"""
        if arcade.check_for_collision(self, paddle):
            if self.change_y < 0:
                arcade.play_sound(self.sound_bounce, volume=SOUND_VOLUME)
                self.bounce_from_paddle(paddle)

    def bounce_from_paddle(self, paddle):
        """Физический отскок от платформы"""
        offset = (self.center_x - paddle.center_x) / (paddle.width / 2)
        offset = max(-1.0, min(1.0, offset))

        max_bounce_angle = math.radians(75)
        bounce_angle = offset * max_bounce_angle

        speed = math.hypot(self.change_x, self.change_y)
        self.change_x = speed * math.sin(bounce_angle)
        self.change_y = speed * math.cos(bounce_angle)

        self.center_y = paddle.top + self.height / 2 + 1

    def bounce_off_brick(self, brick):
        """Отскок от кирпича"""
        dx = self.center_x - brick.center_x
        dy = self.center_y - brick.center_y

        overlap_x = (self.width + brick.width) / 2 - abs(dx)
        overlap_y = (self.height + brick.height) / 2 - abs(dy)

        if overlap_x < overlap_y:
            if dx > 0:
                self.left = brick.right + 1
            else:
                self.right = brick.left - 1
            self.change_x *= -1
        else:
            if dy > 0:
                self.bottom = brick.top + 1
            else:
                self.top = brick.bottom - 1
            self.change_y *= -1

    def reset(self):
        """Сброс мяча на платформу"""
        self.is_attached = True
        self.change_x = 0
        self.change_y = 0