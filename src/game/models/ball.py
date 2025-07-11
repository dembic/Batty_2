# src/game/models/ball.py
from src.game.config import *

import math

class Ball(arcade.Sprite):
    """Class representing the ball in the Batty game"""

    def __init__(self):
        texture = arcade.load_texture("assets/images/ball.png")
        super().__init__(texture, scale=1)
        self.change_x = 0
        self.change_y = 0
        self.previous_y = 0
        self.rotation_speed = 180 # Градусов в секунду
        self.is_attached = True
        self.parent = None
        self.sound_bounce = arcade.load_sound(SOUND_BOUNCE)

    def attach_to_paddle(self, paddle):
        """Привязать мяч к платформе"""
        self.center_x = paddle.center_x
        self.center_y = paddle.top + self.height / 2
        self.previous_y = self.center_y

    def launch(self):
        """Запустить мяч в полет"""
        self.is_attached = False
        self.change_x = BALL_NORMAL_SPEED
        self.change_y = BALL_NORMAL_SPEED

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        """Update ball position and handle screen boundaries"""
        if self.is_attached:
            # Мяч следует за платформой
            paddle = kwargs.get("paddle")
            if paddle:
                self.attach_to_paddle(paddle)
            return

        self.previous_y = self.center_y
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        # Врашение мяча
        self.angle += self.rotation_speed * delta_time
        self.angle %= 360

        # Отражение от левой/правой стены
        if self.left <= 0:
            self.left = 0
            self.change_x *= -1

        if self.right >= SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
            self.change_x *= -1

        # Отражение от верхней границы
        if self.top >= SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
            self.change_y *= -1

    # Проверка коллизий
    def check_collision(self, paddle):
        """Check and handle collision with paddle using physics-based angle"""
        if arcade.check_for_collision(self, paddle):
            if self.change_y < 0: # Если мяч падал вниз
                """self.change_y *= -1 """# No physics
                arcade.play_sound(sound=self.sound_bounce, volume=SOUND_VOLUME)
                self.bounce_from_paddle(paddle)

        # Проверка столкновений с кирпичами через Level
        if self.parent and hasattr(self.parent, 'level'):
            self.parent.level.check_collision(self)

    def bounce_from_paddle(self, paddle):
        """Pysics-based bounce depending on were the ball hits the paddle"""
        offset = (self.center_x - paddle.center_x) / (paddle.width / 2)
        offset = max(-1.0, min(1.0, offset))

        max_bounce_angle = math.radians(75)
        bounce_angle = offset * max_bounce_angle

        speed = math.hypot(self.change_x, self.change_y)
        self.change_x = speed * math.sin(bounce_angle)
        self.change_y = speed * math.cos(bounce_angle)

        # Устанавливаем чуть выше платформы чтобы не залипнуть
        self.center_y = paddle.top + self.height / 2 + 1

    def bounce_off_brick(self, brick):
        # Расстояния между центрами
        dx = self.center_x - brick.center_x
        dy = self.center_y - brick.center_y

        overlap_x = (self.width + brick.width) / 2 - abs(dx)
        overlap_y = (self.height + brick.height) / 2 - abs(dy)

        if overlap_x < overlap_y:
            # Горизонтальный отскок
            if dx > 0:
                self.left = brick.right
            else:
                self.right = brick.left
            self.change_x *= -1
        else:
            # Вертикальный отскок
            if dy > 0:
                self.bottom = brick.top
            else:
                self.top = brick.bottom
            self.change_y *= -1

    def reset(self):
        """Reset ball to initial position and speed"""
        self.is_attached = True
        self.change_x = 0
        self.change_y = 0