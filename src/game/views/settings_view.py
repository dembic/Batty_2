from src.game.config import *
from src.game import *

# Экран для настроек игры
class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        # Text
        start_x = SCREEN_WIDTH // 2 - 180
        start_y = SCREEN_HEIGHT // 2
        self.fonts = arcade.Text(
            "Settings View (Placeholder)",
            start_x,
            start_y,
            arcade.color.FRENCH_WINE,
            DEFAULT_FONT_SIZE, bold=True
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_GRAY)
        self.manager.enable()

    def on_draw(self):
        self.clear()
        self.fonts.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from .menu_view import MenuView  # Ленивый импорт
            menu_view = MenuView()
            self.window.show_view(menu_view)

    def on_hide_view(self):
        self.manager.disable()