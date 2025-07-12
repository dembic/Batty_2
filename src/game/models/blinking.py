# scr/game/models/blinking.py
import math

from src.game.config import *

class Blinking(arcade.Sprite):
    """Base class for objects that can blinking """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blinking_interval = BLINKING_INTERVAL
        self.blink_count = 0
        self.max_blink_count = MAX_BLINKING_COUNT
        self.is_blinking = False
        self.blink_timer = 0.0
        if isinstance(self.scale, (tuple, list)):
            self.base_scale = (float(self.scale[0]) + float(self.scale[1])) / 2 if len (self.scale) >= 2 else float(self.scale[0]) if self.scale else 1.0
        else:
            self.base_scale = float(self.scale) if self.scale is not None else 1.0
        self.target_scale = self.base_scale * 1.5
        self.use_scale_blink = True # Флаг для выбора типа мигания (scale or alpha)

    def start_blinking(self, use_scale=False):
        self.is_blinking = True
        self.blink_count = 0
        self.use_scale_blink = use_scale
        if self.use_scale_blink:
            self.scale = (self.base_scale, self.base_scale)
        else:
            self.alpha = 255

    def update_blinking(self, delta_time):
        if not self.is_blinking:
            return

        self.blink_timer += delta_time
        if self.blink_timer >= self.blinking_interval:
            self.blink_timer = 0.0
            self.blink_count += 1

            if self.use_scale_blink:
                progress = (self.blink_count % 2) / 2 # от 0 до 0.5
                current_scale = self.base_scale + (self.target_scale - self.base_scale) * math.sin(progress * math.pi)
                self.scale = (current_scale, current_scale)
                self.alpha = 255
            else:
                # Переключение видимости для платформы
                self.alpha = 0 if self.alpha == 255 else 255

            # Завершение мигания
            if self.blink_count >= self.max_blink_count:
                self.is_blinking = False
                if self.use_scale_blink:
                    self.alpha = 0 # Скрываем объект полностью для жизней
                    self.scale = (self.base_scale, self.base_scale)
                else:
                    self.alpha = 255