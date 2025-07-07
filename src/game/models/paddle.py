from src.game.config import *

class Paddle(arcade.Sprite):
    """Class representing the paddle in the Batty game."""
    def __init__(self):
        texture = arcade.load_texture("assets/images/paddle.png")
        super().__init__(texture, scale=1.0)
        self.center_x = SCREEN_WIDTH // 2 # Starting paddle position
        self.center_y = PADDLE_UP_Y
        self.change_x = 0 # speed

        self.velocity_x = 0
        self.acceleration = 1200 # pixel/second ^2
        self.max_speed = 500 # pixel/sec
        self.friction = 1000 # Затухание после отпускания клавиши

        self.moving_left = False
        self.moving_right = False

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        # Обновляем ускорение в зависимости от направления
        if self.moving_left and not self.moving_right:
            self.velocity_x -= self.acceleration * delta_time
        elif self.moving_right and not self.moving_left:
            self.velocity_x += self.acceleration * delta_time
        else:
            # Применяем инерцию трение
            if self.velocity_x > 0:
                self.velocity_x -= self.friction * delta_time
                if self.velocity_x < 0:
                    self.velocity_x = 0
            elif self.velocity_x < 0:
                self.velocity_x += self.friction * delta_time
                if self.velocity_x > 0:
                    self.velocity_x = 0
        # Ограничение мексимальной скорости
        self.velocity_x = max(-self.max_speed, min(self.velocity_x, self.max_speed))

        # Обновляем позицию
        self.center_x += self.velocity_x * delta_time

        # Ограничение движение чтобы не выходить за пределы экрана
        if self.left < 0:
            self.left = 0
            self.velocity_x = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
            self.velocity_x = 0

    def move_left(self):
        """Move the paddle left"""
        self.moving_left = True

    def move_right(self):
        """Move the paddle right"""
        self.moving_right = True

    def stop_left(self):
        """Stop the paddle movement"""
        self.moving_left = False

    def stop_right(self):
        self.moving_right = False