"""
UI components for the CAN Bus Puzzle Game
"""

import pygame
import time
from typing import List
from constants import *
from enums import SubsystemState, WindowState, DoorState
from can_message import CANBusMessage
from car_state import CarState
from mission import Mission

class UIRenderer:
    """Handles all UI rendering for the game"""
    
    def __init__(self, screen, fonts):
        self.screen = screen
        self.font = fonts['font']
        self.large_font = fonts['large_font']
        self.title_font = fonts['title_font']
        self.small_font = fonts['small_font']
    
    def draw_car(self, car_state: CarState):
        """Draw the car representation with better visibility and labeling"""
        # Car positioned in left area
        car_x = 200
        car_y = 350
        car_width = 280
        car_height = 160
        
        # Main car body with shadow effect
        shadow_rect = pygame.Rect(car_x - car_width//2 + 3, car_y - car_height//2 + 3, car_width, car_height)
        pygame.draw.rect(self.screen, DARK_GRAY, shadow_rect)
        
        car_rect = pygame.Rect(car_x - car_width//2, car_y - car_height//2, car_width, car_height)
        pygame.draw.rect(self.screen, LIGHT_GRAY, car_rect)
        pygame.draw.rect(self.screen, BLACK, car_rect, 4)
        
        # Car title - positioned higher above the car, slightly to the left
        title_text = self.title_font.render("Here is a CAR to control", True, BLACK)
        self.screen.blit(title_text, (car_x - 120, car_y - car_height//2 - 80))
        
        # Headlights (front of car)
        light_color = YELLOW if car_state.headlights == SubsystemState.ON else GRAY
        light_size = 20
        
        # Left headlight
        pygame.draw.circle(self.screen, light_color, (car_x - car_width//2 - 15, car_y - 30), light_size)
        pygame.draw.circle(self.screen, BLACK, (car_x - car_width//2 - 15, car_y - 30), light_size, 3)
        
        # Right headlight  
        pygame.draw.circle(self.screen, light_color, (car_x - car_width//2 - 15, car_y + 30), light_size)
        pygame.draw.circle(self.screen, BLACK, (car_x - car_width//2 - 15, car_y + 30), light_size, 3)
        
        # Windows
        window_width = 80
        window_height = 50
        
        # Driver window (top)
        driver_window_rect = pygame.Rect(car_x - 60, car_y - 60, window_width, window_height)
        if car_state.driver_window == WindowState.OPEN:
            pygame.draw.rect(self.screen, WHITE, driver_window_rect)
            pygame.draw.lines(self.screen, BLACK, False, [
                (driver_window_rect.left, driver_window_rect.top + 10),
                (driver_window_rect.right, driver_window_rect.top + 10),
                (driver_window_rect.right, driver_window_rect.bottom),
                (driver_window_rect.left, driver_window_rect.bottom)
            ], 3)
        else:
            pygame.draw.rect(self.screen, LIGHT_BLUE, driver_window_rect)
        pygame.draw.rect(self.screen, BLACK, driver_window_rect, 3)
        
        # Driver window status - positioned above the window, more to the left
        driver_status = "OPEN" if car_state.driver_window == WindowState.OPEN else "CLOSED"
        driver_text = self.font.render(f"Driver: {driver_status}", True, BLACK)
        self.screen.blit(driver_text, (car_x - 100, car_y - 95))
        
        # Passenger window (bottom)
        passenger_window_rect = pygame.Rect(car_x - 60, car_y + 10, window_width, window_height)
        if car_state.passenger_window == WindowState.OPEN:
            pygame.draw.rect(self.screen, WHITE, passenger_window_rect)
            pygame.draw.lines(self.screen, BLACK, False, [
                (passenger_window_rect.left, passenger_window_rect.top + 10),
                (passenger_window_rect.right, passenger_window_rect.top + 10),
                (passenger_window_rect.right, passenger_window_rect.bottom),
                (passenger_window_rect.left, passenger_window_rect.bottom)
            ], 3)
        else:
            pygame.draw.rect(self.screen, LIGHT_BLUE, passenger_window_rect)
        pygame.draw.rect(self.screen, BLACK, passenger_window_rect, 3)
        
        # Passenger window status - positioned below the window, more to the left
        passenger_status = "OPEN" if car_state.passenger_window == WindowState.OPEN else "CLOSED"
        passenger_text = self.font.render(f"Passenger: {passenger_status}", True, BLACK)
        self.screen.blit(passenger_text, (car_x - 100, car_y + 85))
        
        # Door locks (right side of car)
        lock_color = RED if car_state.doors == DoorState.LOCKED else GREEN
        lock_size = 12
        
        # Door lock indicators
        pygame.draw.circle(self.screen, lock_color, (car_x + 100, car_y - 30), lock_size)
        pygame.draw.circle(self.screen, BLACK, (car_x + 100, car_y - 30), lock_size, 3)
        pygame.draw.circle(self.screen, lock_color, (car_x + 100, car_y + 30), lock_size)
        pygame.draw.circle(self.screen, BLACK, (car_x + 100, car_y + 30), lock_size, 3)
        
        # Engine RPM display - positioned below car center, more visible
        rpm_color = GREEN if car_state.engine_rpm > 1000 else BLACK
        rpm_text = self.font.render(f"Engine RPM: {car_state.engine_rpm}", True, rpm_color)
        self.screen.blit(rpm_text, (car_x - 80, car_y + 110))
        
        # Headlight status text - positioned below engine RPM
        light_status = "ON" if car_state.headlights == SubsystemState.ON else "OFF"
        light_text = self.font.render(f"Headlights: {light_status}", True, BLACK)
        self.screen.blit(light_text, (car_x - 80, car_y + 135))
        
        # Door status - positioned below headlights
        door_status = "LOCKED" if car_state.doors == DoorState.LOCKED else "UNLOCKED"
        door_text = self.font.render(f"Doors: {door_status}", True, BLACK)
        self.screen.blit(door_text, (car_x - 80, car_y + 160))
    
    def draw_can_messages(self, can_messages: List[CANBusMessage]):
        """Draw the CAN bus message area"""
        # Message area background
        msg_x = WINDOW_WIDTH * 2 // 3
        msg_y = 100
        msg_width = WINDOW_WIDTH // 3 - 20
        msg_height = WINDOW_HEIGHT - 200
        
        msg_rect = pygame.Rect(msg_x, msg_y, msg_width, msg_height)
        pygame.draw.rect(self.screen, WHITE, msg_rect)
        pygame.draw.rect(self.screen, BLACK, msg_rect, 2)
        
        # Title
        title = self.font.render("CAN Bus Messages", True, BLACK)
        self.screen.blit(title, (msg_x + 10, msg_y - 30))
        
        # Messages
        y_offset = msg_y + 10
        for message in can_messages[-12:]:  # Show last 12 messages
            if hasattr(message, 'system_text'):
                text = f"SYS: {message.system_text}"
                color = BLUE
            else:
                text = str(message)
                color = BLACK
            
            msg_surface = self.font.render(text, True, color)
            if msg_surface.get_width() > msg_width - 20:
                # Wrap long messages
                text = text[:40] + "..."
                msg_surface = self.font.render(text, True, color)
            
            self.screen.blit(msg_surface, (msg_x + 10, y_offset))
            y_offset += 25
    
    def draw_subsystem_mapping(self):
        """Draw the CAN ID to subsystem mapping"""
        mapping_x = 450
        mapping_y = 120
        mapping_width = 320
        mapping_height = 220
        
        # Background
        mapping_rect = pygame.Rect(mapping_x, mapping_y, mapping_width, mapping_height)
        pygame.draw.rect(self.screen, WHITE, mapping_rect)
        pygame.draw.rect(self.screen, BLACK, mapping_rect, 3)
        
        # Title
        title_text = self.title_font.render("CAN BUS MAPPINGS", True, BLACK)
        self.screen.blit(title_text, (mapping_x + 10, mapping_y + 10))
        
        # Mappings
        mappings = [
            ("0x101 → Windows Control", "Data: 0=Driver Close, 1=Driver Open"),
            ("", "      2=Passenger Close, 3=Passenger Open"),
            ("0x201 → Headlights", "Data: 0=OFF, 1=ON"),
            ("0x301 → Door Locks", "Data: 0=UNLOCK, 1=LOCK"),
            ("0x401 → Engine", "Data: RPM value (0-8)")
        ]
        
        y_offset = mapping_y + 50
        for main_text, sub_text in mappings:
            if main_text:
                text_surface = self.font.render(main_text, True, BLACK)
                self.screen.blit(text_surface, (mapping_x + 15, y_offset))
                y_offset += 25
            if sub_text:
                sub_surface = self.small_font.render(sub_text, True, DARK_GRAY)
                self.screen.blit(sub_surface, (mapping_x + 15, y_offset))
                y_offset += 20
        
        # Command format
        format_text = self.font.render("Command format: send <CAN_ID> <DATA>", True, BLUE)
        self.screen.blit(format_text, (mapping_x + 15, y_offset + 10))
        
        # Dismiss instruction
        dismiss_text = self.small_font.render("Press SPACE to start playing", True, RED)
        self.screen.blit(dismiss_text, (mapping_x + 15, y_offset + 35))

    def draw_mission(self, current_mission_index: int, missions: List[Mission]):
        """Draw the current mission"""
        if current_mission_index < len(missions):
            mission = missions[current_mission_index]
            mission_text = f"Mission {current_mission_index + 1}: {mission.description}"
            progress_text = f"Progress: {current_mission_index}/{len(missions)} missions completed"
        else:
            mission_text = "🎉 ALL MISSIONS COMPLETED! YOU WON! 🎉"
            progress_text = "Congratulations! You've mastered CAN bus communication!"
        
        # Mission background
        mission_rect = pygame.Rect(10, 10, WINDOW_WIDTH - 20, 80)
        pygame.draw.rect(self.screen, LIGHT_BLUE, mission_rect)
        pygame.draw.rect(self.screen, BLACK, mission_rect, 2)
        
        # Mission text
        mission_surface = self.title_font.render(mission_text, True, BLACK)
        self.screen.blit(mission_surface, (20, 25))
        
        progress_surface = self.font.render(progress_text, True, DARK_GRAY)
        self.screen.blit(progress_surface, (20, 55))
    
    def draw_input_box(self, input_text: str, input_active: bool, show_mapping: bool):
        """Draw the command input box with better instructions"""
        input_y = WINDOW_HEIGHT - 100
        input_rect = pygame.Rect(10, input_y, WINDOW_WIDTH - 20, 50)
        
        # Input box background
        color = LIGHT_BLUE if show_mapping else WHITE
        pygame.draw.rect(self.screen, color, input_rect)
        pygame.draw.rect(self.screen, BLACK, input_rect, 3)
        
        if show_mapping:
            # Show mapping instructions
            instruction = self.font.render("Study the CAN Bus mappings above, then press SPACE to start!", True, BLACK)
            self.screen.blit(instruction, (20, input_y + 15))
        else:
            # Normal input mode
            # Label with example
            label = self.font.render("Enter CAN Bus Command (example: send 0x201 01):", True, BLACK)
            self.screen.blit(label, (15, input_y - 25))
            
            # Input text
            display_text = input_text
            if input_active and int(time.time() * 2) % 2:  # Blinking cursor
                display_text += "|"
            
            text_surface = self.font.render(display_text, True, BLACK)
            self.screen.blit(text_surface, (20, input_y + 15))
            
            # Help text
            help_text = self.small_font.render("Press ENTER to send command | Press M to show mappings again", True, DARK_GRAY)
            self.screen.blit(help_text, (20, input_y + 60))
    
    def draw_error_animation(self, show_error: bool, error_scale: float):
        """Draw the error animation"""
        if show_error and error_scale > 0:
            # Large red X in center of screen
            center_x = WINDOW_WIDTH // 2
            center_y = WINDOW_HEIGHT // 2
            
            # Scale the X
            size = int(100 * error_scale)
            thickness = max(8, int(12 * error_scale))
            
            # Draw X
            pygame.draw.line(self.screen, RED, 
                           (center_x - size, center_y - size), 
                           (center_x + size, center_y + size), thickness)
            pygame.draw.line(self.screen, RED, 
                           (center_x + size, center_y - size), 
                           (center_x - size, center_y + size), thickness)
            
            # Draw error text
            error_text = self.large_font.render("WRONG COMMAND!", True, RED)
            text_rect = error_text.get_rect(center=(center_x, center_y + size + 50))
            self.screen.blit(error_text, text_rect)
