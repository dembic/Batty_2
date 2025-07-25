# src/game/views/game_over_view.py
import arcade.shape_list

from src.game.config import *
from src.game.utils.high_score_manager import HighScoreManager

class GameOverView(arcade.View, arcade.gui.UIAnchorLayout):
    def __init__(self, score):
        super().__init__()
        self.score = score
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.text_input = None

        # Окно с UI
        layout = arcade.gui.UIAnchorLayout()

        panel = arcade.gui.UIAnchorLayout(width=350, height=450, size_hint=None)
        panel.with_padding(all=20)
        panel.with_background(
            texture=arcade.gui.NinePatchTexture(
                left=7, right=7, bottom=7, top=7,
                texture=arcade.load_texture("assets/images/game_over_panel.png")
            )
        )

        vbox = arcade.gui.UIBoxLayout(vertical=True, space_between=10)
        vbox.add(arcade.gui.UILabel(text="Game Over", font_size=24, align="center", text_color=arcade.color.BROWN))
        vbox.add(arcade.gui.UILabel(text=f"Your Score: {score}", font_size=16, text_color=arcade.color.RED_BROWN))

        self.text_input = arcade.gui.UIInputText(width=100, text_color=arcade.color.BLACK).with_border()
        vbox.add(self.text_input)

        submit = arcade.gui.UIFlatButton(text="Submit", width=100)
        submit.on_click = self.on_submit
        vbox.add(submit)

        panel.add(child=vbox, anchor_x="center_x", anchor_y="center_y")
        layout.add(child=panel)
        self.manager.add(layout)

    def on_submit(self, event):
        name = self.text_input.text.strip() or "Anonymous"
        HighScoreManager().add_score(name, self.score)
        from .menu_view import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self) -> None:
        self.manager.disable()