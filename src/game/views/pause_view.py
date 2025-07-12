# src/game/views/pause_view.py
import arcade

from src.game.config import *

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view # Сохраняем ссылку на текущую игру
        self.text = arcade.Text(
            "GAME PAUSE",
            SCREEN_WIDTH // 2 - 160,
            SCREEN_HEIGHT // 2,
            arcade.color.YELLOW,
            36, bold=True
        )
        self.sound_pause = arcade.load_sound(SOUND_PAUSE)

    def on_draw(self):
        self.clear()
        self.game_view.on_draw() # Рисуем текущую игру как фон
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, (0,0,0,180)) # Затемнение
        self.text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            self.window.show_view(self.game_view)
            arcade.play_sound(sound=self.sound_pause)