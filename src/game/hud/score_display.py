# src/game/hud/score_display.py

from src.game.config import *

class ScoreDisplay:
    def __init__(self):
        self.score = 0
        start_x = SCREEN_WIDTH - 280
        start_y = SCREEN_HEIGHT - 30

        # Text
        self.score_draw = arcade.Text(
            str(f"Score: {self.score}"),
            start_x,
            start_y,
            arcade.color.FRENCH_WINE,
            SCORE_FONT, bold=True
        )

    def add(self, points):
        self.score += points

    def reset(self):
        self.score = 0

    def draw(self):
        self.score_draw.text = f"Score: {self.score}"
        self.score_draw.draw()
