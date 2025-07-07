# src/game/__init__.py

from .config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from .views import MenuView, GameView, HighScoresView, SettingsView


__all__ = [
    'SCREEN_WIDTH', 'SCREEN_HEIGHT', 'SCREEN_TITLE',
    'MenuView', 'GameView', 'HighScoresView', 'SettingsView'
]