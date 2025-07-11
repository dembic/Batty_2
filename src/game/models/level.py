# src/game/models/level.py

import random
from src.game.config import *
from .brick import Brick

class Level:
    def __init__(self, width, height, grid=None):
        self.bricks = arcade.SpriteList()
        self.width = width
        self.height = height
        self.sound_ball_brick_bounce = arcade.load_sound(SOUND_BALL_BRICK)

    def load_from_grid(self, grid):
        brick_width = 54
        brick_height = 23
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] > 0:
                    x = col * brick_width + brick_width // 2
                    y = self.height - (row * brick_height + brick_height // 2 + 100)
                    health = grid[row][col]
                    points = health * 10
                    brick = Brick(x, y, health, points)
                    self.bricks.append(brick)

    def generate_procedural(self):
        rows, cols = 8, 12
        brick_width = 54
        brick_height = 23
        for row in range(rows):
            for col in range(cols):
                x = col * brick_width + brick_width // 2 + 90
                y = self.height - (row * brick_height + brick_height // 2 + 100)
                health = random.randint(1, 4)
                points = health * 10
                brick = Brick(x, y, health, points)
                self.bricks.append(brick)

    def update(self, delta_time):
        self.bricks.update(delta_time)

    def draw(self):
        self.bricks.draw()

    def check_collision(self, ball):
        hit_list = arcade.check_for_collision_with_list(ball, self.bricks)
        for brick in hit_list:
            ball.bounce_off_brick(brick)
            points = brick.hit()
            # Добавить логику начисления очков
            arcade.play_sound(sound=self.sound_ball_brick_bounce, volume=SOUND_VOLUME)
            break