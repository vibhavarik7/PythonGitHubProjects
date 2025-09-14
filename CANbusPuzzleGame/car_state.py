"""
Car state management for the CAN Bus Puzzle Game
"""

from enums import SubsystemState, WindowState, DoorState

class CarState:
    """Manages the state of all car subsystems"""
    
    def __init__(self):
        self.headlights = SubsystemState.OFF
        self.driver_window = WindowState.OPEN  # Start with windows open
        self.passenger_window = WindowState.OPEN  # Start passenger closed
        self.doors = DoorState.UNLOCKED
        self.engine_rpm = 0
        
    def update_subsystem(self, subsystem: str, value: int) -> bool:
        """Update a subsystem state. Returns True if successful."""
        try:
            if subsystem == "headlights":
                self.headlights = SubsystemState(value)
                return True
            elif subsystem == "windows":
                # For windows, value determines which window: 0=driver, 1=passenger
                # The second parameter would be open/close (this is simplified)
                if value == 0:
                    self.driver_window = WindowState.CLOSED
                elif value == 1:
                    self.driver_window = WindowState.OPEN
                elif value == 2:
                    self.passenger_window = WindowState.CLOSED
                elif value == 3:
                    self.passenger_window = WindowState.OPEN
                else:
                    return False  # Invalid window command
                return True
            elif subsystem == "doors":
                self.doors = DoorState(value)
                return True
            elif subsystem == "engine":
                self.engine_rpm = max(0, min(8000, value * 1000))  # Scale and limit RPM
                return True
        except (ValueError, TypeError):
            pass
        return False
