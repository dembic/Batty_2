from src.game.config import *
from ..models import Paddle, Ball

# Placeholder classes with manager initialized in __init__
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        # Text
        start_x = SCREEN_WIDTH // 2 - 60
        start_y = SCREEN_HEIGHT // 2
        self.game_view = arcade.Text(
            "Batty",
            start_x,
            start_y,
            arcade.color.FRENCH_WINE,
            DEFAULT_FONT_SIZE, bold=True
        )

        # Game objects экземпляры классов
        self.paddle = Paddle()
        self.ball = Ball()
        self.ball.attach_to_paddle(self.paddle)

        # Создаем SpriteList для управления спрайтами
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.paddle)
        self.sprite_list.append(self.ball)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.manager.enable()

    def on_draw(self):
        self.clear()
        self.game_view.draw()
        self.sprite_list.draw()

    def on_update(self, delta_time: float):
        self.paddle.update(delta_time)
        self.ball.update(delta_time, paddle=self.paddle)
        self.ball.check_collision(self.paddle)

        if self.ball.is_attached:
            self.ball.attach_to_paddle(self.paddle)

    def on_key_press(self, key, modifiers):
        """Handle keyboard input to return menu."""
        if key == arcade.key.LEFT:
            self.paddle.move_left()
        elif key == arcade.key.RIGHT:
            self.paddle.move_right()
        elif key == arcade.key.SPACE and self.ball.is_attached:
            self.ball.launch()

        # return main menu
        if key == arcade.key.ESCAPE:
            from .menu_view import MenuView # Ленивый импорт
            menu_view = MenuView()
            self.window.show_view(menu_view)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.paddle.stop_left()
        elif key == arcade.key.RIGHT:
            self.paddle.stop_right()

    def on_hide_view(self):
        self.manager.disable()