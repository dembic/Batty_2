# src/game/views/game_view.py
import os.path

from src.game.config import *
from ..models import Paddle, Ball, Level
from ..hud import LivesDisplay, ScoreDisplay, LevelDisplay
from ..models.bonus_manager import BonusManager
from ..models.laser_beam import LaserBeam


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.sound_pause = arcade.load_sound(SOUND_PAUSE)
        self.level_index = 1
        self.level_complete_text_timer = 0
        self.show_level_text_timer = 2
        self.level_text = None

        self.bonus_manager = BonusManager()
        self.extra_balls = arcade.SpriteList()  # для дополнительных мячей

        self.laser_active = False
        self.lasers = arcade.SpriteList()
        self.laser_timer = 0
        self._laser_shot_timer = 0

        self.floating_texts = []

        # Текст завершения уровня
        self.level_complete_view = arcade.Text(
            "Level complete",
            SCREEN_WIDTH // 2 - 170,
            SCREEN_HEIGHT // 2,
            arcade.color.FRENCH_WINE,
            36,
            bold=True
        )

        self.level_display = LevelDisplay()
        self.score_display = ScoreDisplay()
        self.lives_display = LivesDisplay(x=X, y=Y, spacing=SPACING, scale=SCALE)

        self.paddle = Paddle()
        self.ball = Ball()
        self.ball.parent = self

        self.level = Level(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.load_level(self.level_index)

        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.paddle)
        self.sprite_list.append(self.ball)
        self.sprite_list.extend(self.level.bricks)

        self.level_display.update_level(self.level_index)

    def load_level(self, index):
        # Очистка бонусов и мячей перед загрузкой нового уровня
        self.extra_balls = arcade.SpriteList()
        self.bonus_manager.bonuses = arcade.SpriteList()

        self.level_display.update_level(self.level_index)

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
            print(f"No more level")
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
            36, bold=True
        )

        self.level.on_brick_destroyed = self.handle_brick_destroyed

    def handle_brick_destroyed(self, brick):
        if self.ball not in self.sprite_list:
            return # Главный мяч упал бонусы не появятся
        self.bonus_manager.maybe_drop_bonus(brick.center_x, brick.center_y)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.manager.enable()
        self.ball.parent = self

    def on_draw(self):
        self.clear()

        if self.show_level_text_timer > 0:
            self.level_text.draw()
            return

        if self.level_complete_text_timer <= 0:
            self.sprite_list.draw()
        else:
            self.level.bricks.draw()

        self.lives_display.draw()
        self.score_display.draw()

        if self.level_complete_text_timer > 0:
            self.level_complete_view.draw()

        self.bonus_manager.bonuses.draw()
        self.extra_balls.draw()
        self.level_display.draw()
        self.lasers.draw()

        # floating text
        for ft in self.floating_texts:
            ft.draw()


    def on_update(self, delta_time: float):
        # Начало уровня — ждём, не обновляем ничего
        if self.show_level_text_timer > 0:
            self.show_level_text_timer -= delta_time
            return

        # === Движение ===
        if self.level_complete_text_timer <= 0:
            self.paddle.update(delta_time)
            self.ball.update(delta_time)
            self.ball.check_collision(self.paddle)

            self.extra_balls.update()
            for ball in self.extra_balls:
                ball.check_collision(self.paddle)

        # Обновление бонусов
        self.bonus_manager.update(delta_time, self)


        # Удаление упавших бонусных мячей
        to_remove = [ball for ball in self.extra_balls if ball.bottom <= 0]
        for ball in to_remove:
            ball.remove_from_sprite_lists()

        # Проверка падения основного мяча
        main_ball_lost = False
        if self.ball.bottom <= 0:
            self.ball.remove_from_sprite_lists()
            main_ball_lost = True

        # === Потеря жизни только если вообще нет мячей ===
        if main_ball_lost:
            if len(self.extra_balls) > 0:
                new_main_ball = self.extra_balls.pop()
                new_main_ball.life_timer = None
                new_main_ball.visible = True
                self.ball = new_main_ball
                self.ball.parent = self
            else:
                # Нет ни одного мяча - теряем жизнь
                self.lives_display.lose_life()
                self.paddle.start_blinking(use_scale=False)
                self.ball = Ball()
                self.ball.parent = self
                self.ball.reset()
                self.ball.attach_to_paddle(self.paddle)
                self.sprite_list.append(self.ball)

        # === Обновление мигания жизни и платформы ===
        self.lives_display.update(delta_time)

        # === Коллизии с кирпичами (все мячи) ===
        all_balls = [self.ball] + list(self.extra_balls)
        points = self.level.check_collision(all_balls)
        # add score
        if points > 0:
            self.score_display.add(points)

        # Лазеры обновляются
        self.lasers.update()

        # Если лазеры активны
        if self.laser_active:
            self.laser_timer -= delta_time
            self._laser_shot_timer -= delta_time

            if self.laser_timer <= 0:
                self.laser_active = False
                self.lasers = arcade.SpriteList()
            elif self._laser_shot_timer <= 0:
                beam1 = LaserBeam(self.paddle.left + 10, self.paddle.top)
                beam2 = LaserBeam(self.paddle.right - 10, self.paddle.top)
                self.lasers.append(beam1)
                self.lasers.append(beam2)
                self._laser_shot_timer = 0.3

        # Коллизии лазеров с кирпичами
        for laser_beam in self.lasers:
            hit_list = arcade.check_for_collision_with_list(laser_beam, self.level.bricks)
            if hit_list:
                laser_beam.remove_from_sprite_lists()
                for brick in hit_list:
                    points = brick.hit()
                    self.score_display.add(points)
                    if brick.is_destroyed and hasattr(self.level, "on_brick_destroyed"):
                        self.level.on_brick_destroyed(brick)

        # Обновление всплывающих текстов
        for ft in self.floating_texts:
            ft.update(delta_time)

        # Удаление изчезнувших текстов
        self.floating_texts = [ft for ft in self.floating_texts if not ft.is_done()]

        # === Конец уровня ===
        if self.level_complete_text_timer <= 0 and all(
                getattr(brick, "is_indestructible", False) or brick.is_destroyed
                for brick in self.level.bricks
        ):
            self.level_complete_text_timer = 2.0

        if self.level_complete_text_timer > 0:
            self.level_complete_text_timer -= delta_time
            if self.level_complete_text_timer <= 0:
                self.level_index += 1
                self.load_level(self.level_index)

        # === Конец игры ===
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
        if key == arcade.key.ESCAPE:
            from .menu_view import MenuView
            self.window.show_view(MenuView())
        if key == arcade.key.P:
            from .pause_view import PauseView
            self.window.show_view(PauseView(self))
            arcade.play_sound(self.sound_pause)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.paddle.stop_left()
        elif key == arcade.key.RIGHT:
            self.paddle.stop_right()

    def on_hide_view(self):
        self.manager.disable()