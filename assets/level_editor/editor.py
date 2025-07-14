# assets/level_editor/editor.py
import glob
import json
import os


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
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Batty Level editor")
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = None
        self.bricks = []
        self.current_color_index = 0
        self.grid_offset_y = 100
        self.pending_save_path = None
        self.awaiting_overwrite_confirm = False
        self.loaded_level_path = None
        self.show_grid = True
        self.grid = GridOverlay(SCREEN_WIDTH, SCREEN_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT, GRID_MARGIN, self.grid_offset_y)

    def show_level_selector_gui(self):
        self.manager.clear()
        self.v_box = arcade.gui.UIBoxLayout()

        # Заголовок
        self.v_box.add(arcade.gui.UITextArea(text="Select Level to Load", font_size=18, height=40))

        # Получение списка уровней
        files = sorted(glob.glob(os.path.join(LEVELS_DIR, "level*.json")))
        for path in files:
            filename_level = os.path.basename(path)

            button = arcade.gui.UIFlatButton(text=filename_level, width=200)
            @button.event("on_click")
            def on_click(event, path=path):
                self.load_level_from_file(path)
                self.manager.clear() # Удаляем меню после выбора

            self.v_box.add(button)

        # Отмена
        cancel_btn = arcade.gui.UIFlatButton(text="Cancel", width=200)
        @cancel_btn.event("on_click")
        def on_click_cancel(event):
            self.manager.clear()

        self.v_box.add(cancel_btn)
        self.manager.add(arcade.gui.UIAnchorLayout(children=self.v_box, anchor_x="center_x", anchor_y="center_y"))

    def on_draw(self):
        self.clear(arcade.color.ASH_GREY)
        for brick in self.bricks:
            brick.draw()

        if self.pending_save_path:
            arcade.Text(
                f"Will save to: {self.pending_save_path}",
                10,
                40,
                arcade.color.DARK_RED if self.awaiting_overwrite_confirm else arcade.color.DARK_GREEN,
                12
            ).draw()
        if self.awaiting_overwrite_confirm:
            arcade.Text(
                f"File exists! Press Y to overwrite or N to cancel.",
                10,
                60,
                arcade.color.RED,
                12
            ).draw()

        # Подсказка
        arcade.Text(
            f"Current color: {COLOR_LIST[self.current_color_index]}",
            10,
            SCREEN_HEIGHT - 30,
            arcade.color.BLACK,
            14
        ).draw()

        arcade.Text(
            f"1-7: Сolor | S: = Save | C: = Clear | G: = Grid | Left Click: Add | Right Click: Remove",
            10,
            10,
            arcade.color.DARK_BLUE_GRAY,
            12
        ).draw()

        if self.show_grid:
            self.grid.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        grid_x = (x // (BRICK_WIDTH + GRID_MARGIN)) * (BRICK_WIDTH + GRID_MARGIN) + BRICK_WIDTH // 2
        grid_y = (y // (BRICK_HEIGHT + GRID_MARGIN)) * (BRICK_HEIGHT + GRID_MARGIN) + BRICK_HEIGHT // 2

        if grid_y < self.grid_offset_y:
            return
        # Удаление кирпича по правому клику
        if button == arcade.MOUSE_BUTTON_RIGHT:
            for brick in self.bricks:
                if abs(brick.x - grid_x) < BRICK_WIDTH // 2 and abs(brick.y - grid_y) < BRICK_HEIGHT // 2:
                    self.bricks.remove(brick)
                    return

        # Добавление кирпича по левому клику
        if button == arcade.MOUSE_BUTTON_LEFT:
            for brick in self.bricks:
                if abs(brick.x - grid_x) < 2 and abs(brick.y - grid_y) < 2:
                    return # Уже есть - не добавляем


            color = COLOR_LIST[self.current_color_index]
            self.bricks.append(Brick(grid_x, grid_y, color))

    def on_key_press(self, key, modifiers):
        if self.awaiting_overwrite_confirm:
            if key == arcade.key.Y:
                self.save_json_to_file(self.pending_save_path)
                self.awaiting_overwrite_confirm = False
                self.pending_save_path = None
            elif key == arcade.key.N:
                print("Save canceled")
                self.awaiting_overwrite_confirm = False
                self.pending_save_path = None
            return

        if arcade.key.KEY_1 <= key <= arcade.key.KEY_7:
            self.current_color_index = key - arcade.key.KEY_1
        elif key == arcade.key.S:
            self.save_json_to_file()
        elif key == arcade.key.C:
            self.bricks.clear()
        elif key == arcade.key.L:
            self.show_level_selector_gui()
        elif key == arcade.key.G:
            self.show_grid = not self.show_grid

    def load_level_from_file(self, path):
        with open(path, "r") as f:
            data = json.load(f)

            self.bricks.clear()
            for bricks_data in data:
                self.bricks.append(Brick(bricks_data["x"], bricks_data["y"], bricks_data["color"]))

            self.loaded_level_path = path
            print(f"Loaded level from {path}")

    def load_level_by_index(self, index):
        filename_level = f"level{index:02}.json"
        path = os.path.join(LEVELS_DIR, filename_level)

        if not os.path.exists(path):
            print(f"File {filename_level} not found in {LEVELS_DIR}")
            return
        with open(path, "r") as f:
            data = json.load(f)

        self.bricks.clear()
        for brick_data in data:
            brick = Brick(brick_data["x"], brick_data["y"], brick_data["color"])
            self.bricks.append(brick)

        self.loaded_level_path = path
        print(f"Loaded level from {path}")

    def prepare_save_to_json(self):
        levels_dir = LEVELS_DIR
        os.makedirs(levels_dir, exist_ok=True)

        index = 1
        while True:
            filename_level = f"level{index:02}.json"
            full_path = os.path.join(levels_dir, filename_level)
            if not os.path.exists(full_path):
                break
            index += 1

        # Проверка: если последний файл существует - предложить перезаписать
        full_path = os.path.join(levels_dir, f"level{index - 1:02}.json") if index > 1 else full_path

        if os.path.exists(full_path):
            print(f"File {full_path} exists. Press Y to overwrite or N to cancel.")
            self.awaiting_overwrite_confirm = True
            self.pending_save_path = full_path
        else:
            self.save_json_to_file(full_path)

    def save_json_to_file(self, path=None):
        data =[brick.to_dict() for brick in self.bricks]
        if not path:
            path = self.loaded_level_path or self.get_next_available_path()
            self.loaded_level_path = path

        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Save {len(data)} bricks to {path}")

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