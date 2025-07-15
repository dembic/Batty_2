# src/game/views/game_view.py
import os.path

from src.game.config import *
from ..models import Paddle, Ball, Level
from ..hud import LivesDisplay, ScoreDisplay

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.sound_pause = arcade.load_sound(SOUND_PAUSE)
        self.level_index = 1
        self.level_complete_text_timer = 0
        self.level_complete_text = None
        self.show_level_text_timer = 2
        self.level_text = None

        # Текс для завершения уровня
        start_x = SCREEN_WIDTH // 2 - 170
        start_y = SCREEN_HEIGHT // 2
        self.level_complete_view = arcade.Text(
            "Level complete",
            start_x,
            start_y,
            arcade.color.FRENCH_WINE,
            36, bold=True
        )

        # Game objects экземпляры классов
        self.score_display = ScoreDisplay()
        self.lives_display = LivesDisplay(x=X, y=Y, spacing=SPACING, scale=SCALE)
        self.paddle = Paddle()
        self.ball = Ball()
        self.ball.parent = self
        self.level = Level(SCREEN_WIDTH, SCREEN_HEIGHT)
        #self.level.generate_procedural() # Generate bricks
        #self.level.load_from_json(LEVEL_PATH)
        self.load_level(self.level_index)
        self.ball.attach_to_paddle(self.paddle)

        # Создаем SpriteList для управления спрайтами
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.paddle)
        self.sprite_list.append(self.ball)
        self.sprite_list.extend(self.level.bricks)

    def load_level(self, index):
        file_level = f"level{index:02}.json"
        path = os.path.join(f"assets/level_editor/{LEVELS_DIR}", file_level)
        if os.path.exists(path):
            self.level = Level(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.level.load_from_json(path)

            # Обновить спрайты
            self.sprite_list = arcade.SpriteList()
            self.sprite_list.append(self.paddle)
            self.sprite_list.append(self.ball)
            self.sprite_list.extend(self.level.bricks)

            # Прекрепить мяч
            self.ball.reset()
            self.ball.attach_to_paddle(self.paddle)

            print(f"Loaded {file_level}")
        else:
            print(f"No  more level")
            from .game_over_view import GameOverView
            self.window.show_view(GameOverView())

        # Текст для начала уровня
        self.show_level_text_timer = 2
        level_str = f"Level {index:02}"
        self.level_text = arcade.Text(
            level_str,
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT // 2 + 40,
            arcade.color.LIGHT_GREEN,
            36,bold=True
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.manager.enable()
        self.ball.parent = self

    def on_draw(self):
        self.clear() # Очистка экрана
        # Отображаем текс уровня
        if self.show_level_text_timer > 0:
            self.level_text.draw()
            return

        if self.level_complete_text_timer <= 0: # Если уровень не завершен
            self.sprite_list.draw() # Рисуем спрайты включая кирпичи
        else:
            self.level.bricks.draw()
        self.lives_display.draw()
        self.score_display.draw()

        # Рисуем надпись Level Complete
        if self.level_complete_text_timer > 0:
            self.level_complete_view.draw()

    def on_update(self, delta_time: float):
        # Начало уровня
        if self.show_level_text_timer > 0:
            self.show_level_text_timer -= delta_time
            return # Ничего не двигаем до завершения

        # Конец уровня
        if self.level_complete_text_timer <= 0:
            self.paddle.update(delta_time)
            self.ball.update(delta_time)
            self.ball.check_collision(self.paddle)

        # Обработка потери жизни если мяч упал
        if self.ball.bottom <= 0:
            self.lives_display.lose_life()
            self.paddle.start_blinking(use_scale=False)
            self.ball.reset()

        # Обновление мигания для жизней и платформы
        self.lives_display.update(delta_time)

        # Обновление и добавление очков
        points = self.level.check_collision(self.ball)
        if points > 0:
            self.score_display.add(points)

        # Условия для показа надписи при завершении уровня
        if self.level_complete_text_timer <= 0 and all(
            getattr(brick, "is_indestructible", False) or brick.is_destroyed
            for brick in self.level.bricks
        ):
            self.level_complete_text_timer = 2.0

        # Таймер показа Level Complete
        if self.level_complete_text_timer > 0:
            self.level_complete_text_timer -= delta_time
            if self.level_complete_text_timer <= 0:
                self.level_index += 1
                self.load_level(self.level_index)

        # Обработка конца игры
        if self.lives_display.current_lives == 0:
            from .game_over_view import GameOverView
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.paddle.move_left()
        elif key == arcade.key.RIGHT:
            self.paddle.move_right()
        elif key == arcade.key.SPACE and self.ball.is_attached:
            self.ball.launch()

        # return the main menu
        if key == arcade.key.ESCAPE:
            from .menu_view import MenuView # Ленивый импорт
            menu_view = MenuView()
            self.window.show_view(menu_view)

        # Game pause
        if key == arcade.key.P:
            from .pause_view import PauseView
            pause = PauseView(self)
            self.window.show_view(pause)
            arcade.play_sound(sound=self.sound_pause)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.paddle.stop_left()
        elif key == arcade.key.RIGHT:
            self.paddle.stop_right()

    def on_hide_view(self):
        self.manager.disable()