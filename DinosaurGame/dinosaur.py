"""
Dinosaur module containing the Dinosaur class.
Handles the main character's movement, jumping, and rendering.
"""

import pygame
from constants import (
    BLACK, WHITE, GRAVITY, JUMP_STRENGTH, 
    DINOSAUR_WIDTH, DINOSAUR_HEIGHT
)


class Dinosaur:
    """
    Dinosaur class representing the main character.
    Handles movement, jumping, and collision detection.
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = DINOSAUR_WIDTH
        self.height = DINOSAUR_HEIGHT
        self.vel_y = 0  # Vertical velocity
        self.jump_strength = JUMP_STRENGTH  # Negative because y decreases upward
        self.gravity = GRAVITY
        self.is_jumping = False
        self.ground_y = y  # Remember the ground position
        
    def jump(self):
        """Make the dinosaur jump if it's on the ground."""
        if not self.is_jumping:
            self.vel_y = self.jump_strength
            self.is_jumping = True
    
    def update(self):
        """Update dinosaur position and handle gravity."""
        # Apply gravity
        if self.is_jumping:
            self.vel_y += self.gravity
            self.y += self.vel_y
            
            # Check if dinosaur has landed
            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.vel_y = 0
                self.is_jumping = False
    
    def draw(self, screen):
        """Draw the dinosaur on the screen."""
        # Draw dinosaur as a black rectangle (can be replaced with an image)
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))
        
        # Add some details to make it look more like a dinosaur
        # Eye
        pygame.draw.circle(screen, WHITE, (self.x + 30, self.y + 15), 5)
        pygame.draw.circle(screen, BLACK, (self.x + 32, self.y + 15), 2)
        
        # Legs
        pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + self.height, 8, 10))
        pygame.draw.rect(screen, BLACK, (self.x + 25, self.y + self.height, 8, 10))
    
    def get_rect(self):
        """Return the dinosaur's rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
