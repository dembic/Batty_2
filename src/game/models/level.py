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

    def check_collision(self, balls):
        total_points = 0

        for ball in balls:
            hit_list = arcade.check_for_collision_with_list(ball, self.bricks)
            for brick in hit_list:
                ball.bounce_off_brick(brick)
                total_points += brick.hit()
                arcade.play_sound(sound=self.sound_ball_brick_bounce, volume=SOUND_VOLUME)

                if brick.is_destroyed and hasattr(self, "on_brick_destroyed"):
                    self.on_brick_destroyed(brick)
        return total_points
        #return 0