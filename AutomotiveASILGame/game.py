"""
Game module for the Automotive ASIL Game.
Contains the main Game class with game logic and UI handling.
"""

import pygame
import sys
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK, RED, GREEN,
    CAR_X, CAR_Y, CAR_WIDTH, CAR_HEIGHT, BLOCK_SPAWN_RATE,
    GAME_START, GAME_PLAYING, GAME_OVER
)
from car import Car
from block import FunctionalityBlock


class Game:
    """Main game class handling the game loop and logic."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ASIL Highway DASH or CRASH...!")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.game_state = GAME_START
        self.score = 0
        
        # Game objects
        self.car = Car(CAR_X, CAR_Y)
        self.blocks = []
        self.spawn_timer = 0
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
        
        # Input handling
        self.last_key_time = 0
        self.key_cooldown = 200  # milliseconds
        
    def handle_events(self):
        """Handle user input and events."""
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == GAME_START:
                        self.start_game()
                    elif self.game_state == GAME_OVER:
                        self.restart_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.game_state == GAME_PLAYING:
                    # Handle ASIL/QM key presses with cooldown (case-insensitive)
                    if current_time - self.last_key_time > self.key_cooldown:
                        pressed_key = None
                        if event.key == pygame.K_a:
                            pressed_key = "A"
                        elif event.key == pygame.K_b:
                            pressed_key = "B"
                        elif event.key == pygame.K_c:
                            pressed_key = "C"
                        elif event.key == pygame.K_d:
                            pressed_key = "D"
                        elif event.key == pygame.K_q:
                            pressed_key = "Q"
                            
                        if pressed_key:
                            self.handle_asil_input(pressed_key)
                            self.last_key_time = current_time
    
    def handle_asil_input(self, pressed_key):
        """Handle ASIL/QM key input and check for correct matches."""
        # Check if any block is close enough to the car (within detection range)
        detection_range = 200  # pixels from car
        
        for block in self.blocks[:]:  # Use slice to avoid modification during iteration
            if block.x <= CAR_X + detection_range and block.x >= CAR_X - 50:
                if block.asil_level == pressed_key:
                    # Correct answer - remove block and increase score
                    self.blocks.remove(block)
                    self.score += 1
                    return
                else:
                    # Wrong answer - game over
                    self.game_state = GAME_OVER
                    return
    
    def update(self):
        """Update game logic."""
        if self.game_state == GAME_PLAYING:
            # Spawn new blocks
            self.spawn_timer += 1
            if self.spawn_timer >= BLOCK_SPAWN_RATE:
                new_block = FunctionalityBlock(SCREEN_WIDTH, CAR_Y - 20)
                self.blocks.append(new_block)
                self.spawn_timer = 0
                
            # Update blocks
            for block in self.blocks[:]:
                block.update()
                
                # Remove blocks that are off screen
                if block.is_off_screen():
                    self.blocks.remove(block)
                    
                # Check collision with car
                if block.get_rect().colliderect(self.car.get_rect()):
                    self.game_state = GAME_OVER
    
    def draw(self):
        """Draw all game elements."""
        self.screen.fill(WHITE)
        
        if self.game_state == GAME_START:
            self.draw_start_screen()
        elif self.game_state == GAME_PLAYING:
            self.draw_game_screen()
        elif self.game_state == GAME_OVER:
            self.draw_game_over_screen()
            
        pygame.display.flip()
    
    def draw_start_screen(self):
        """Draw the start screen with instructions."""
        title_text = self.big_font.render("ASIL Highway DASH or CRASH...!", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        instructions = [
            "Learn automotive safety integrity levels (ASIL) and quality management (QM)!",
            "",
            "HOW TO PLAY:",
            "• Functionality blocks will approach your car from the right",
            "• Each block shows a car functionality - guess its ASIL/QM level!", 
            "• Press the correct key (A, B, C, D, or Q) before the block reaches your car",
            "• Wrong key or collision --> Game Over!",
            "",
            "ASIL LEVELS:",
            "• D (Red) - Highest safety risk (Airbags, ABS)",
            "• C (Orange) - High safety risk (Power Steering)",
            "• B (Gold) - Medium safety risk (Lane Assist)",
            "• A (Green) - Low safety risk (Traffic Signs)",
            "• Q (Blue) - Quality Managed (Parking Sensors)",
            "",
            "Press SPACE to start!"
        ]
        
        y_offset = 180
        for line in instructions:
            if line.startswith("•"):
                text = self.small_font.render(line, True, BLACK)
            elif line.startswith("ASIL LEVELS:") or line.startswith("HOW TO PLAY:"):
                text = self.font.render(line, True, BLACK)
            elif line == "Press SPACE to start!":
                text = self.font.render(line, True, RED)
            else:
                text = self.small_font.render(line, True, BLACK)
                
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25
    
    def draw_game_screen(self):
        """Draw the main game screen."""
        # Draw ground line
        pygame.draw.line(self.screen, BLACK, (0, CAR_Y + CAR_HEIGHT + 10), 
                        (SCREEN_WIDTH, CAR_Y + CAR_HEIGHT + 10), 3)
        
        # Draw car
        self.car.draw(self.screen)
        
        # Draw blocks
        for block in self.blocks:
            block.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Draw controls reminder
        controls_text = self.small_font.render("Press A, B, C, D, or Q for correct ASIL level", True, BLACK)
        self.screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))
        
        # Draw detection zone indicator
        detection_zone = pygame.Rect(CAR_X - 50, CAR_Y - 50, 200, CAR_HEIGHT + 100)
        pygame.draw.rect(self.screen, (200, 255, 200), detection_zone, 2)
        zone_text = self.small_font.render("Detection Zone", True, GREEN)
        self.screen.blit(zone_text, (CAR_X - 30, CAR_Y - 70))
    
    def draw_game_over_screen(self):
        """Draw the game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(score_text, score_rect)
        
        # Restart instruction
        restart_text = self.font.render("Press SPACE to restart or ESC to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(restart_text, restart_rect)
        
        # Show some ASIL info
        info_text = self.small_font.render("Remember: D=Highest Risk, C=High, B=Medium, A=Low, Q=Quality Managed", True, WHITE)
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(info_text, info_rect)
    
    def start_game(self):
        """Start the game."""
        self.game_state = GAME_PLAYING
        self.score = 0
        self.blocks = []
        self.spawn_timer = 0
        
    def restart_game(self):
        """Restart the game after game over."""
        self.start_game()
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
