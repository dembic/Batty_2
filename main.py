from src.game.config import *
from src.game import *

def main():
    """Main function to start the game."""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    menu_view = MenuView()  # Start with MenuView without arguments
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()