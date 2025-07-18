# src/game/hud/level_display.py
from src.game.config import *

class LevelDisplay:
    def __init__(self, x=SCREEN_WIDTH - 500, y=SCREEN_HEIGHT - 30):
        self.position = (x, y)

        # Text
        self.level_text = arcade.Text(
            "", x, y,
            arcade.color.YELLOW_GREEN,
            LEVEL_FONT, bold=True
        )

    def update_level(self, level_index: int):
        self.level_text.text = f"Level {level_index}"

    def draw(self):
        self.level_text.draw()
