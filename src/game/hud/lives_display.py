# src/game/hud/lives_display.py
from src.game.config import *
from ..models.blinking import Blinking

class LivesDisplay:
    def __init__(self, x=X, y=Y, spacing=SPACING, scale=SCALE):
        self.max_lives = MAX_LIVES
        self.current_lives = self.max_lives
        self.x = x
        self.y = y
        self.spacing = spacing
        self.scale = scale

        # Create for lives
        self.lives_sprites = arcade.SpriteList()

        # Инициализируем спрайты жизней
        for i in range(self.max_lives):
            sprite = Blinking("assets/images/lives.png", scale=scale)
            sprite.center_x = self.x + i * self.spacing
            sprite.center_y = self.y
            self.lives_sprites.append(sprite)

    def draw(self):
        self.lives_sprites.draw()

    def lose_life(self):
        if self.current_lives > 0:
            self.current_lives -= 1
            # blinking last sprite
            if self.current_lives < self.max_lives:
                self.lives_sprites[self.current_lives].start_blinking(use_scale=True)

    def gain_life(self):
        if self.current_lives < self.max_lives:
            self.current_lives += 1
            # Show last sprite
            if self.current_lives - 1 < self.max_lives:
                self.lives_sprites[self.current_lives - 1].alpha = 255

    def reset(self):
        self.current_lives = self.max_lives
        for sprite in self.lives_sprites:
            sprite.alpha = 255
            sprite.is_blinking = False
            sprite.scale = sprite.base_scale # Сброс масштаба

    def update(self, delta_time):
        for sprite in self.lives_sprites:
            if sprite.is_blinking:
                sprite.update_blinking(delta_time)


