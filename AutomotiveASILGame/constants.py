"""
Constants and configurations for the Automotive ASIL Game.
Contains all game settings, colors, dimensions, and automotive functionalities.
"""

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
BLUE = (100, 150, 255)
GREEN = (50, 200, 50)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Car properties
CAR_WIDTH = 80
CAR_HEIGHT = 40
CAR_WINDOW_WIDTH = 60
CAR_WINDOW_HEIGHT = 20
CAR_X = 100
CAR_Y = SCREEN_HEIGHT - 150

# Block properties
BLOCK_WIDTH = 200
BLOCK_HEIGHT = 60
BLOCK_SPEED = 3
BLOCK_SPAWN_RATE = 120  # frames between spawns

# Game states
GAME_START = 0
GAME_PLAYING = 1
GAME_OVER = 2

# Automotive functionalities mapped to ASIL/QM levels
FUNCTIONALITIES = {
    "Airbags": "D",
    "ABS": "D", 
    "Electronic Stability Control": "D",
    "Power Steering": "C",
    "Brake Assist": "D",
    "Lane Departure Warning": "B",
    "Blind Spot Monitoring": "B",
    "Adaptive Cruise Control": "B",
    "Automatic Emergency Braking": "C",
    "Lane Keep Assist": "B",
    "Traffic Sign Recognition": "A",
    "Parking Sensors": "Q",
    "Backup Camera": "Q",
    "Tire Pressure Monitoring": "A",
    "Engine Control Unit": "D",
    "Transmission Control": "C",
    "Anti-lock Braking System": "D",
    "Electronic Brake Distribution": "C",
    "Hill Start Assist": "B",
    "Traction Control": "C",
    "Forward Collision Warning": "B",
    "Driver Drowsiness Detection": "A",
    "Night Vision Assist": "A",
    "Park Assist": "Q",
    "Keyless Entry": "Q"
}

# ASIL level colors for visual feedback
ASIL_COLORS = {
    "D": (220, 50, 50),    # Dark Red - Highest risk
    "C": (255, 140, 0),    # Orange - High risk  
    "B": (255, 215, 0),    # Gold - Medium risk
    "A": (144, 238, 144),  # Light Green - Low risk
    "Q": (173, 216, 230)   # Light Blue - Quality managed
}
