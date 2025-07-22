# src/game/hud/floating_text.py

from src.game.config import *

class FloatingText:
    def __init__(self, text, x, y, color=arcade.color.WHITE, duration=1.0):
        self.text = arcade.Text(text, x, y, color=color, font_size=16, anchor_x="center")
        self.total_time = 0.0
        self.duration = duration
        self.velocity_y = 30  # поднимается вверх

    def update(self, delta_time):
        self.total_time += delta_time
        self.text.y += self.velocity_y * delta_time

    def draw(self):
        self.text.draw()

    def is_done(self):
        return self.total_time > self.duration