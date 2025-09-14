#!/usr/bin/env python3
"""
CAN Bus Puzzle Game - Main Entry Point
A fun educational game where players control car subsystems using CAN bus commands.
"""

import pygame
import sys
import time
from typing import List

# Import our modules
from constants import *
from enums import SubsystemState, WindowState, DoorState
from car_state import CarState
from mission import Mission
from can_message import CANBusMessage, CANMessageParser
from ui_components import UIRenderer

class Game:
    """Main game class - simplified with modular components"""
    
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("CAN Bus Puzzle Game")
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        fonts = {
            'font': pygame.font.Font(None, 24),
            'large_font': pygame.font.Font(None, 48),
            'title_font': pygame.font.Font(None, 36),
            'small_font': pygame.font.Font(None, 20)
        }
        
        # Initialize components
        self.car_state = CarState()
        self.ui_renderer = UIRenderer(self.screen, fonts)
        self.can_parser = CANMessageParser()
        
        # Game state
        self.can_messages: List[CANBusMessage] = []
        self.current_mission_index = 0
        self.input_text = ""
        self.input_active = True
        self.running = True
        self.show_mapping = True
        
        # Error animation
        self.show_error = False
        self.error_start_time = 0
        self.error_scale = 0
        
        # Initialize missions
        self.missions = [
            Mission("Turn on headlights", {"headlights": SubsystemState.ON}, ""),
            Mission("Close the driver's window", {"driver_window": WindowState.CLOSED}, ""),
            Mission("Open the passenger window", {"passenger_window": WindowState.OPEN}, ""),
            Mission("Lock the doors", {"doors": DoorState.LOCKED}, ""),
            Mission("Start engine (RPM > 1000)", {"engine_rpm": 1000}, ""),
            Mission("Turn off headlights", {"headlights": SubsystemState.OFF}, ""),
        ]
        
        # Add initial system message
        self.add_system_message("System initialized")
    
    def add_can_message(self, can_id: int, data: int):
        """Add a CAN message to the display"""
        message = CANBusMessage(can_id, data, time.time())
        self.can_messages.append(message)
        # Keep only last 15 messages
        if len(self.can_messages) > 15:
            self.can_messages.pop(0)
    
    def add_system_message(self, text: str):
        """Add a system message (displayed as special CAN message)"""
        message = CANBusMessage(0x000, 0, time.time())
        message.system_text = text
        self.can_messages.append(message)
        if len(self.can_messages) > 15:
            self.can_messages.pop(0)
    
    def process_command(self, command: str):
        """Process a player command"""
        success, can_id, data = self.can_parser.parse_command(command)
        
        if not success:
            self.trigger_error()
            return
        
        # Add to CAN message log
        self.add_can_message(can_id, data)
        
        # Check if it's a valid CAN ID
        if can_id not in CAN_IDS:
            self.trigger_error()
            return
        
        # Update car state
        subsystem = CAN_IDS[can_id]
        if self.car_state.update_subsystem(subsystem, data):
            # Check if current mission is completed
            if self.current_mission_index < len(self.missions):
                current_mission = self.missions[self.current_mission_index]
                if current_mission.check_completion(self.car_state):
                    self.add_system_message(f"Mission completed: {current_mission.description}")
                    self.current_mission_index += 1
                    if self.current_mission_index >= len(self.missions):
                        self.add_system_message("All missions completed! You won!")
        else:
            self.trigger_error()
    
    def trigger_error(self):
        """Trigger the error animation"""
        self.show_error = True
        self.error_start_time = time.time()
        self.error_scale = 0
        self.input_text = ""
        self.add_system_message("Invalid command!")
    
    def update_error_animation(self):
        """Update the error animation"""
        if self.show_error:
            elapsed = time.time() - self.error_start_time
            if elapsed < 2.0:  # Show for 2 seconds
                # Pop-up animation: scale from 0 to 1 in first 0.3 seconds
                if elapsed < 0.3:
                    self.error_scale = (elapsed / 0.3) * 1.2  # Slight overshoot
                elif elapsed < 0.5:
                    self.error_scale = 1.2 - ((elapsed - 0.3) / 0.2) * 0.2  # Settle to 1.0
                else:
                    self.error_scale = 1.0
            else:
                self.show_error = False
                self.error_scale = 0
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.show_mapping:
                    # Dismiss mapping display and start game
                    self.show_mapping = False
                    self.add_system_message("Game started! Good luck with your missions!")
                
                elif event.key == pygame.K_m and not self.show_mapping:
                    # Show mapping again
                    self.show_mapping = True
                
                elif not self.show_mapping:  # Only process input when not showing mapping
                    if event.key == pygame.K_RETURN:
                        if self.input_text.strip():
                            self.process_command(self.input_text)
                            self.input_text = ""
                    
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    
                    elif event.unicode.isprintable():
                        self.input_text += event.unicode
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update_error_animation()
            
            # Clear screen
            self.screen.fill(WHITE)
            
            # Draw all game elements using UI renderer
            self.ui_renderer.draw_mission(self.current_mission_index, self.missions)
            self.ui_renderer.draw_car(self.car_state)
            self.ui_renderer.draw_can_messages(self.can_messages)
            
            # Show subsystem mapping if enabled
            if self.show_mapping:
                self.ui_renderer.draw_subsystem_mapping()
            
            self.ui_renderer.draw_input_box(self.input_text, self.input_active, self.show_mapping)
            self.ui_renderer.draw_error_animation(self.show_error, self.error_scale)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Main entry point"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
