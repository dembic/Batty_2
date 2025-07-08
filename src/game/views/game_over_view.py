# src/game/views/game_over_view.py
from src.game.config import *
from src.game import *

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        # Text
        start_x = SCREEN_WIDTH // 2 - 160
        start_y = SCREEN_HEIGHT // 2
        self.game_over_text = arcade.Text(
            "Game Over",
            start_x,
            start_y,
            arcade.color.ROSE,
            GAME_OVER_TEXT, bold=True
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.manager.enable()

    def on_draw(self):
        self.clear()
        self.game_over_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from .menu_view import MenuView
            menu_view = MenuView()
            self.window.show_view(menu_view)

    def on_hide_view(self):
        self.manager.disable()