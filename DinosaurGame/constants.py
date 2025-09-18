"""
Game constants and configuration values.
Contains all the constant values used throughout the dinosaur game.
"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
FPS = 60

# Colors (RGB tuples)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (34, 139, 34)
BLUE = (135, 206, 235)
RED = (255, 0, 0)

# Game physics
GRAVITY = 0.8
JUMP_STRENGTH = -15


# Dinosaur settings
DINOSAUR_WIDTH = 40
DINOSAUR_HEIGHT = 60
DINOSAUR_X_POSITION = 100

# Obstacle settings
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 60
OBSTACLE_SPEED = 5
INITIAL_SPAWN_DELAY = 120  # frames (2 seconds at 60 FPS)
MIN_SPAWN_DELAY = 60  # frames (1 second at 60 FPS)

# Game states
GAME_STATE_START = "START"
GAME_STATE_PLAYING = "PLAYING"  
GAME_STATE_GAME_OVER = "GAME_OVER"
