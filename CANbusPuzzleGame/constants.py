"""
Constants for the CAN Bus Puzzle Game
"""

# Window dimensions
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)
LIGHT_BLUE = (173, 216, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# CAN Bus ID mappings
CAN_IDS = {
    0x101: "windows",
    0x201: "headlights", 
    0x301: "doors",
    0x401: "engine"
}
