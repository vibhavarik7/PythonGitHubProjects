"""
Car module for the Automotive ASIL Game.
Contains the Car class representing the player's car.
"""

import pygame
from constants import (
    CAR_WIDTH, CAR_HEIGHT, CAR_WINDOW_WIDTH, CAR_WINDOW_HEIGHT,
    RED, BLUE, BLACK
)


class Car:
    """Represents the player's car."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        
    def draw(self, screen):
        """Draw the car as a red rectangle with blue window."""
        # Car body (red rectangle)
        car_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, RED, car_rect)
        pygame.draw.rect(screen, BLACK, car_rect, 2)
        
        # Car window (blue square on top)
        window_x = self.x + (self.width - CAR_WINDOW_WIDTH) // 2
        window_y = self.y + 5
        window_rect = pygame.Rect(window_x, window_y, CAR_WINDOW_WIDTH, CAR_WINDOW_HEIGHT)
        pygame.draw.rect(screen, BLUE, window_rect)
        pygame.draw.rect(screen, BLACK, window_rect, 1)
        
    def get_rect(self):
        """Get collision rectangle for the car."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
