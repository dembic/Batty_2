# src/game/models/ball.py
from src.game.config import *
import math

class Ball(arcade.Sprite):
    """Class representing the ball in the Batty game"""

    def __init__(self):
        texture = arcade.load_texture("assets/images/ball.png")
        super().__init__(texture, scale=1.0)
        self.change_x = 0
        self.change_y = 0
        self.previous_y = 0

        self.is_attached = True

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

        # Если мяч упал вниз
        if self.bottom <= 0:
            self.bottom = 0
            """self.change_y *= -1"""
            self.reset()

    # Проверка коллизий
    def check_collision(self, paddle):
        """Check and handle collision with paddle using physics-based angle"""
        if arcade.check_for_collision(self, paddle):
            if self.change_y < 0: # Если мяч падал вниз
                """self.change_y *= -1 """# No physics
                self.bounce_from_paddle(paddle)

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

    def reset(self):
        """Reset ball to initial position and speed"""
        self.is_attached = True
        self.change_x = 0
        self.change_y = 0