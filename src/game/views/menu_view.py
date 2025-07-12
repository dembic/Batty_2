# src/game/views/menu_view.py

from src.game.config import *
from .game_view import GameView
from .high_scores_view import HighScoresView
from .settings_view import SettingsView

class MenuView(arcade.View):
    """Main menu view for Batty game."""

    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.main_view = None  # Инициализируем позже при переходе

        # Create buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=250)
        high_scores_button = arcade.gui.UIFlatButton(text="High Scores", width=250)
        settings_button = arcade.gui.UIFlatButton(text="Settings", width=250)
        quit_button = arcade.gui.UIFlatButton(text="Quit", width=250)

        # Define styles for all states including 'press'
        button_style = {
            "normal": {"bg_color": (50, 50, 50), "font_color": arcade.color.WHITE_SMOKE},
            "hover": {"bg_color": (70, 70, 70), "font_color": arcade.color.LIGHT_GRAY},
            "press": {"bg_color": (30, 30, 30), "font_color": arcade.color.WHITE}
        }
        start_button.style = button_style
        high_scores_button.style = button_style
        settings_button.style = button_style
        quit_button.style = button_style

        @start_button.event("on_click")
        def on_click_start_button(_):
            game_view = GameView()
            self.window.show_view(game_view)

        @high_scores_button.event("on_click")
        def on_click_high_scores_button(_):
            high_scores_view = HighScoresView()
            self.window.show_view(high_scores_view)

        @settings_button.event("on_click")
        def on_click_settings_button(_):
            settings_view = SettingsView()
            self.window.show_view(settings_view)

        @quit_button.event("on_click")
        def on_click_quit_button(_):
            arcade.exit()

        # Создаем якорный Layout
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        # Elements Layout with Batty title
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            align_x=50,
            align_y=150,
            child=arcade.gui.UITextArea(text="Batty", width=200, height=50, font_size=36)
        )
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            align_y=50,
            child=start_button
        )
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            align_y=-10,
            child=high_scores_button
        )
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            align_y=-70,
            child=settings_button
        )
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            align_y=-130,
            child=quit_button
        )

    def on_show_view(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.BLACK)
        self.manager.enable()

    def on_hide_view(self):
        """Called when hiding this view."""
        self.manager.disable()

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        """Handle keyboard input."""
        if key == arcade.key.ESCAPE:
            pass # Нет необходимости возврата это начальный вид

    def on_resize(self, width, height):
        """Handle window resize to keep elements centered."""
        super().on_resize(width, height)