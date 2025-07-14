from src.game.config import *

class GridOverlay:
    def __init__(self, width, height, cell_width, cell_height, margin=0, offset_y=0):
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.margin = margin
        self.offset_y = offset_y

    def draw(self):
        color = arcade.color.LIGHT_GRAY

        # Vertical line
        x = 0
        while x <= self.width:
            arcade.draw_line(x, self.offset_y, x, self.height, color, 1)
            x += self.cell_width + self.margin

        # Horizontal line
        y = self.offset_y
        while y <= self.height:
            arcade.draw_line(0, y, self.width, y, color, 1)
            y += self.cell_height + self.margin

