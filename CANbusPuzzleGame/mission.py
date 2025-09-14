"""
Mission system for the CAN Bus Puzzle Game
"""

from typing import Dict
from car_state import CarState

class Mission:
    """Represents a game mission"""
    
    def __init__(self, description: str, target_state: Dict, can_command: str):
        self.description = description
        self.target_state = target_state
        self.can_command = can_command
        self.completed = False
    
    def check_completion(self, car_state: CarState) -> bool:
        """Check if mission is completed based on car state"""
        for attr, expected_value in self.target_state.items():
            if getattr(car_state, attr) != expected_value:
                return False
        self.completed = True
        return True
