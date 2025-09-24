"""
Block module for the Automotive ASIL Game.
Contains the FunctionalityBlock class representing functionality blocks.
"""

import pygame
import random
from constants import (
    BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_SPEED,
    FUNCTIONALITIES, ASIL_COLORS, BLACK
)


class FunctionalityBlock:
    """Represents a functionality block that moves toward the car."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BLOCK_WIDTH
        self.height = BLOCK_HEIGHT
        self.functionality, self.asil_level = random.choice(list(FUNCTIONALITIES.items()))
        self.color = ASIL_COLORS[self.asil_level]
        self.font = pygame.font.Font(None, 24)
        
    def update(self):
        """Move the block to the left."""
        self.x -= BLOCK_SPEED
        
    def draw(self, screen):
        """Draw the functionality block with text."""
        # Draw main block
        block_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, block_rect)
        pygame.draw.rect(screen, BLACK, block_rect, 2)
        
        # Draw functionality name (split into multiple lines if needed)
        words = self.functionality.split()
        if len(words) > 2:
            # Split into two lines
            line1 = " ".join(words[:len(words)//2])
            line2 = " ".join(words[len(words)//2:])
            text1 = self.font.render(line1, True, BLACK)
            text2 = self.font.render(line2, True, BLACK)
            
            text1_rect = text1.get_rect(center=(self.x + self.width//2, self.y + self.height//2 - 10))
            text2_rect = text2.get_rect(center=(self.x + self.width//2, self.y + self.height//2 + 10))
            
            screen.blit(text1, text1_rect)
            screen.blit(text2, text2_rect)
        else:
            # Single line
            text = self.font.render(self.functionality, True, BLACK)
            text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
            screen.blit(text, text_rect)
            
        # No longer showing ASIL level - users must guess!
        
    def get_rect(self):
        """Get collision rectangle for the block."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def is_off_screen(self):
        """Check if block has moved off the left side of screen."""
        return self.x + self.width < 0
