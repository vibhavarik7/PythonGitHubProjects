"""
Enums for the CAN Bus Puzzle Game
"""

from enum import Enum

class SubsystemState(Enum):
    OFF = 0
    ON = 1

class WindowState(Enum):
    CLOSED = 0
    OPEN = 1

class DoorState(Enum):
    UNLOCKED = 0
    LOCKED = 1
