# src/game/views/high_scores_view.py

from src.game.config import *
from src.game import *
from src.game.utils.high_score_manager import HighScoreManager

# Экран для отображения рекордов очков
class HighScoresView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.score = HighScoreManager().load_scores()

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


    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.manager.enable()

    def on_draw(self):
        self.clear()
        self.font_high_scores.draw()
        for i, entry in enumerate(self.score[:10]):
            text = f"{i + 1}. {entry['name']} - {entry['score']}"
            arcade.draw_text(text, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 150 - i * 40, arcade.color.YELLOW, 24)


    def on_key_press(self, key, modifiers):
        """Handle keyboard input to return menu."""
        if key == arcade.key.ESCAPE:
            from .menu_view import MenuView  # Ленивый импорт
            menu_view = MenuView()
            self.window.show_view(menu_view)

    def on_hide_view(self):
        self.manager.disable()