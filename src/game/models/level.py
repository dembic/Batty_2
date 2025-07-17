# src/game/models/level.py
import json

from src.game.config import *
from .brick import Brick


class Level:
    def __init__(self, width, height, grid=None):
        self.bricks = arcade.SpriteList()
        self.width = width
        self.height = height
        self.sound_ball_brick_bounce = arcade.load_sound(SOUND_BALL_BRICK)
        self.on_brick_destroyed = None

    def load_from_json(self, path):
        with open(path, "r") as f:
            data = json.load(f)

        for entry in data:
            x = entry.get("x")
            y = entry.get("y")
            color = entry.get("color")
            health = entry.get("health", 1)
            points = health * 10

            brick = Brick(x, y, health=health, points=points, color=color)
            self.bricks.append(brick)

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
        colors = ["blue", "green", "orange", "pink", "purple", "red", "yellow"]
        rows = 6
        cols = len(colors)
        brick_width = 54
        brick_height = 23

        for row in range(rows):
            for col in range(cols):
                color = colors[col % len(colors)]
                x = col * brick_width + brick_width // 2 + 180
                y = self.height - (row * brick_height + brick_height // 2 + 100)
                brick = Brick(x, y, color=color)
                self.bricks.append(brick)

    def update(self, delta_time):
        self.bricks.update(delta_time)

    def draw(self):
        self.bricks.draw()

    def bounce_off_brick_directional(self, ball, brick):
        dx = ball.center_x - brick.center_x
        dy = ball.center_y - brick.center_y

        overlap_x = (ball.width + brick.width) / 2 - abs(dx)
        overlap_y = (ball.height + brick.height) / 2 - abs(dy)

        if overlap_x < overlap_y:
            # Горизонтальный отскок (слева/справа)
            if dx > 0:
                ball.left = brick.right + 1
            else:
                ball.right = brick.left - 1
            ball.change_x *= -1
        else:
            # Вертикальный отскок (сверху/снизу)
            if dy > 0:
                ball.bottom = brick.top + 1
            else:
                ball.top = brick.bottom - 1
            ball.change_y *= -1

    def check_collision(self, balls):
        total_points = 0

        for ball in balls:
            hit_list = arcade.check_for_collision_with_list(ball, self.bricks)

            if not hit_list:
                continue

            # Отскок только от ближайшего кирпича
            closest_brick = min(
                hit_list,
                key=lambda brick: (brick.center_x - ball.center_x) ** 2 + (brick.center_y - ball.center_y) ** 2
            )

            self.bounce_off_brick_directional(ball, closest_brick)

            arcade.play_sound(self.sound_ball_brick_bounce, volume=SOUND_VOLUME)
            total_points += closest_brick.hit()

            if closest_brick.is_destroyed and self.on_brick_destroyed:
                self.on_brick_destroyed(closest_brick)

        return total_points