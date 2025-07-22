# src/game/views/__init__.py

from .menu_view import MenuView
from .game_view import GameView
from .high_scores_view import HighScoresView
from .settings_view import SettingsView


__all__ = [
    'MenuView', 'GameView', 'HighScoresView', 'SettingsView'
]