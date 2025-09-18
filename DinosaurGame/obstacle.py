"""
Obstacle module containing the Obstacle class.
Handles the cactus obstacles that the dinosaur must avoid.
"""

import pygame
from constants import GREEN, OBSTACLE_SPEED, OBSTACLE_WIDTH, OBSTACLE_HEIGHT


class Obstacle:
    """
    Obstacle class representing the blocks the dinosaur must avoid.
    Handles movement and collision detection.
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.speed = OBSTACLE_SPEED
    
    def update(self):
        """Move the obstacle from right to left."""
        self.x -= self.speed
    
    def draw(self, screen):
        """Draw the obstacle on the screen."""
        # Draw obstacle as a green cactus-like block
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        
        # Add some spikes to make it look more like a cactus
        for i in range(0, self.height, 15):
            pygame.draw.polygon(screen, GREEN, [
                (self.x - 5, self.y + i + 5),
                (self.x, self.y + i),
                (self.x - 5, self.y + i - 5)
            ])
            pygame.draw.polygon(screen, GREEN, [
                (self.x + self.width + 5, self.y + i + 5),
                (self.x + self.width, self.y + i),
                (self.x + self.width + 5, self.y + i - 5)
            ])
    
    def get_rect(self):
        """Return the obstacle's rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        """Check if the obstacle has moved off the left side of the screen."""
        return self.x + self.width < 0
