# assets/level_editor/editor.py

import glob
import json
import os

import arcade.gui

from src.game.config import *
from grid_overlay import GridOverlay

class Brick:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        arcade.draw_lbwh_rectangle_filled(
            self.x - BRICK_WIDTH // 2,
            self.y - BRICK_HEIGHT // 2,
            BRICK_WIDTH,
            BRICK_HEIGHT,
            COLOR_PALETTE[self.color]
        )
        arcade.draw_lbwh_rectangle_outline(
            self.x - BRICK_WIDTH // 2,
            self.y - BRICK_HEIGHT // 2,
            BRICK_WIDTH,
            BRICK_HEIGHT,
            arcade.color.BLACK, 1
        )

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "color": self.color,
            "health": self.get_health()
        }

    def get_health(self):
        if self.color == "red":
            return 5
        elif self.color in ("blue", "green"):
            return 1
        else:
            return 2


class LevelEditor(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Batty Level Editor")
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.grid = GridOverlay(SCREEN_WIDTH, SCREEN_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT, GRID_MARGIN)

        self.bricks = []
        self.current_color_index = 0
        self.loaded_level_path = None
        self.awaiting_overwrite_confirm = False
        self.pending_save_path = None
        self.show_grid = True

        self.level_list_open = False
        self.level_files = []
        self.scroll_offset = 0
        self.entry_height = 30

    def on_draw(self):
        self.clear(arcade.color.ASH_GREY)

        for brick in self.bricks:
            brick.draw()

        if self.show_grid:
            self.grid.draw()

        # Показываем редактируемый файл
        if self.loaded_level_path:
            filename = os.path.basename(self.loaded_level_path)
            arcade.Text(
                f"Editing: {filename}",
                10,
                self.height - 50,
                arcade.color.DARK_GREEN,
                14
            ).draw()

        arcade.Text(
            f"1–7: Color | L: Load | S: Save | C: Clear | G: Toggle Grid | Left Click = Add | Right Click = Remove",
            10, 10, arcade.color.BLACK, 12).draw()

        arcade.Text(
            f"Current color: {COLOR_LIST[self.current_color_index]}",
            10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 14).draw()

        if self.awaiting_overwrite_confirm:
            arcade.Text("File exists! Press Y to overwrite or N to cancel.", 10, 50, arcade.color.RED, 14).draw()

        if self.level_list_open:
            self.draw_level_list()

        self.manager.draw()

    def draw_level_list(self):
        x = SCREEN_WIDTH // 2 + 280
        y = SCREEN_HEIGHT - 80
        width = 300
        height = SCREEN_HEIGHT - 70

        arcade.draw_lbwh_rectangle_filled(SCREEN_WIDTH // 2 + 270, SCREEN_HEIGHT // 2 - 260, width, height, arcade.color.GRAY)
        arcade.Text("Select level", x + 10, y + 50, arcade.color.BLACK, 16, bold=True).draw()

        start_y = y - 40 + self.scroll_offset
        for i, file_path in enumerate(self.level_files):
            filename = os.path.basename(file_path)
            entry_y = start_y - i * self.entry_height
            if 50 < entry_y < SCREEN_HEIGHT - 30:
                arcade.Text(filename, x + 20, entry_y, arcade.color.WHITE, 14).draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.level_list_open:
            list_x = SCREEN_WIDTH // 2 + 290
            list_y = SCREEN_HEIGHT - 80
            start_y = list_y - 40 + self.scroll_offset

            for i, file_path in enumerate(self.level_files):
                entry_y = start_y - i * self.entry_height
                if (list_x + 20 < x < list_x + 280) and (entry_y < y < entry_y + self.entry_height):
                    self.load_level_from_file(file_path)
                    self.level_list_open = False
                    return
            return

        grid_x = (x // (BRICK_WIDTH + GRID_MARGIN)) * (BRICK_WIDTH + GRID_MARGIN) + BRICK_WIDTH // 2
        grid_y = (y // (BRICK_HEIGHT + GRID_MARGIN)) * (BRICK_HEIGHT + GRID_MARGIN) + BRICK_HEIGHT // 2

        if grid_y < 100:
            return

        if button == arcade.MOUSE_BUTTON_RIGHT:
            for brick in self.bricks:
                if abs(brick.x - grid_x) < BRICK_WIDTH // 2 and abs(brick.y - grid_y) < BRICK_HEIGHT // 2:
                    self.bricks.remove(brick)
                    return

        if button == arcade.MOUSE_BUTTON_LEFT:
            for brick in self.bricks:
                if abs(brick.x - grid_x) < 2 and abs(brick.y - grid_y) < 2:
                    return
            color = COLOR_LIST[self.current_color_index]
            self.bricks.append(Brick(grid_x, grid_y, color))

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.level_list_open:
            visible_height = SCREEN_HEIGHT - 120
            full_height = len(self.level_files) * self.entry_height
            max_scroll = max(0, full_height - visible_height + self.entry_height)
            self.scroll_offset -= scroll_y * 15
            self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))


    def on_key_press(self, key, modifiers):
        if self.awaiting_overwrite_confirm:
            if key == arcade.key.Y:
                self.save_json_to_file(self.pending_save_path)
                self.awaiting_overwrite_confirm = False
                self.pending_save_path = None
            elif key == arcade.key.N:
                self.awaiting_overwrite_confirm = False
                self.pending_save_path = None
            return

        if arcade.key.KEY_1 <= key <= arcade.key.KEY_7:
            self.current_color_index = key - arcade.key.KEY_1
        elif key == arcade.key.S:
            self.save_json_to_file()
        elif key == arcade.key.C:
            self.bricks.clear()
        elif key == arcade.key.G:
            self.show_grid = not self.show_grid
        elif key == arcade.key.L:
            self.level_files = sorted(glob.glob(os.path.join(LEVELS_DIR, "level*.json")))
            self.level_list_open = True
            self.scroll_offset = 0

    def load_level_from_file(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        self.bricks = [Brick(b["x"], b["y"], b["color"]) for b in data]
        self.loaded_level_path = path
        print(f"Loaded {path}")

    def save_json_to_file(self, path=None):
        if not path:
            path = self.loaded_level_path or self.get_next_available_path()
            if os.path.exists(path):
                self.awaiting_overwrite_confirm = True
                self.pending_save_path = path
                return

        data = [b.to_dict() for b in self.bricks]
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Saved to {path}")
        self.loaded_level_path = path

    @staticmethod
    def get_next_available_path():
        os.makedirs(LEVELS_DIR, exist_ok=True)
        index = 1
        while True:
            path = os.path.join(LEVELS_DIR, f"level{index:02}.json")
            if not os.path.exists(path):
                return path
            index += 1


if __name__ == "__main__":
    editor = LevelEditor()
    arcade.run()
