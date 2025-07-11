import arcade
import arcade.gui

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Batty"

# Paddle
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 25
PADDLE_UP_Y = 30
PADDLE_SPEED = 300
PADDLE_COLOR = (0, 0, 255)

# Ball
BALL_WIDTH = 30
BALL_HEIGHT = 30
BALL_NORMAL_SPEED = -200
BALL_FAST_SPEED = 300
BALL_SLOW_SPEED = 100
BALL_COLOR = (0, 255, 0)

# for fonts
DEFAULT_FONT_SIZE = 20
TITLE_FONT_SIZE = 48

# for font score
SCORE_FONT = 24

# for lives
MAX_LIVES = 3
X = 20
Y = 580
SPACING = 30
SCALE = 1.0

# Text for game over
GAME_OVER_TEXT = 48

# For blinking
BLINKING_INTERVAL = 0.1
MAX_BLINKING_COUNT = 30

# for sounds
SOUND_VOLUME = 0.5
SOUND_BOUNCE = "assets/sounds/ball_bounce.mp3"
SOUND_BALL_BRICK = "assets/sounds/ball_brick_bounce.mp3"