# src/game/views/high_scores_view.py

from src.game.config import *
from src.game import *

# Экран для отображения рекордов очков
class HighScoresView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        # Text
        start_x = SCREEN_WIDTH // 2 - 80
        start_y = SCREEN_HEIGHT // 2 + 200
        self.font_high_scores = arcade.Text(
            "High Scores",
            start_x,
            start_y,
            arcade.color.FRENCH_WINE,
            DEFAULT_FONT_SIZE, bold=True
        )
        self.high_scores = self.load_high_scores()
        self.score_texts = [
            arcade.Text(f"{i+1}.     {score}", start_x, start_y - 50 - i * 30, arcade.color.AQUA,
                        DEFAULT_FONT_SIZE, bold=True)
            for i, score in enumerate(self.high_scores)
        ]

    def load_high_scores(self):
        path = "assets/high_scores.txt"
        try:
            with open(path, "r") as f:
                scores = [int(line.strip()) for line in f.readlines()]
                return sorted(scores, reverse=True)[:10]
        except FileNotFoundError:
            print("No high scores file")
            return []

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.manager.enable()

    def on_draw(self):
        self.clear()
        self.font_high_scores.draw()
        for score in self.score_texts:
            score.draw()

    def on_key_press(self, key, modifiers):
        """Handle keyboard input to return menu."""
        if key == arcade.key.ESCAPE:
            from .menu_view import MenuView  # Ленивый импорт
            menu_view = MenuView()
            self.window.show_view(menu_view)

    def on_hide_view(self):
        self.manager.disable()