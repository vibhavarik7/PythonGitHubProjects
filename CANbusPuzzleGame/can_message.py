"""
CAN message handling for the CAN Bus Puzzle Game
"""

import time
from typing import Tuple, Optional

class CANBusMessage:
    """Represents a CAN bus message for display"""
    
    def __init__(self, can_id: int, data: int, timestamp: float):
        self.can_id = can_id
        self.data = data
        self.timestamp = timestamp
        
    def __str__(self):
        return f"ID: 0x{self.can_id:03X} Data: {self.data:02X} [{time.strftime('%H:%M:%S', time.localtime(self.timestamp))}]"

class CANMessageParser:
    """Handles parsing of CAN bus commands"""
    
    @staticmethod
    def parse_command(command: str) -> Tuple[bool, Optional[int], Optional[int]]:
        """Parse a CAN bus command. Returns (success, can_id, data)"""
        try:
            parts = command.strip().lower().split()
            if len(parts) != 3 or parts[0] != "send":
                return False, None, None
            
            can_id_str = parts[1]
            if can_id_str.startswith("0x"):
                can_id = int(can_id_str, 16)
            else:
                can_id = int(can_id_str)
            
            data = int(parts[2], 16) if parts[2].startswith("0x") else int(parts[2])
            
            return True, can_id, data
        except (ValueError, IndexError):
            return False, None, None
