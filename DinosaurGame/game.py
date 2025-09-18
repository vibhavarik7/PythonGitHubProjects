"""
Game module containing the main Game class.
Handles the game loop, events, rendering, and game state management.
"""

import pygame
import sys
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT, FPS,
    WHITE, BLACK, GRAY, BLUE, RED, GREEN,
    INITIAL_SPAWN_DELAY, MIN_SPAWN_DELAY, DINOSAUR_X_POSITION,
    GAME_STATE_START, GAME_STATE_PLAYING, GAME_STATE_GAME_OVER
)
from dinosaur import Dinosaur
from obstacle import Obstacle


class Game:
    """
    Main game class that handles the game loop, events, and game state.
    """
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dinosaur Game")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.game_state = GAME_STATE_START
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        
        # Game objects
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT - 60
        self.dinosaur = Dinosaur(DINOSAUR_X_POSITION, ground_y)
        self.obstacles = []
        self.obstacle_spawn_timer = 0
        self.obstacle_spawn_delay = INITIAL_SPAWN_DELAY
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.medium_font = pygame.font.Font(None, 56)
        self.big_font = pygame.font.Font(None, 72)
    
    def handle_events(self):
        """Handle user input and events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == GAME_STATE_START:
                        self.start_game()
                    elif self.game_state == GAME_STATE_GAME_OVER:
                        self.restart_game()
                    elif self.game_state == GAME_STATE_PLAYING:
                        self.dinosaur.jump()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Update game logic if the game is playing."""
        if self.game_state == GAME_STATE_PLAYING:
            # Update dinosaur
            self.dinosaur.update()
            
            # Spawn obstacles
            self.obstacle_spawn_timer += 1
            if self.obstacle_spawn_timer >= self.obstacle_spawn_delay:
                ground_y = SCREEN_HEIGHT - GROUND_HEIGHT - 60
                self.obstacles.append(Obstacle(SCREEN_WIDTH, ground_y))
                self.obstacle_spawn_timer = 0
                
                # Gradually increase difficulty by reducing spawn delay
                if self.obstacle_spawn_delay > MIN_SPAWN_DELAY:
                    self.obstacle_spawn_delay -= 1
            
            # Update obstacles
            for obstacle in self.obstacles[:]:  # Use slice to avoid modification during iteration
                obstacle.update()
                
                # Remove obstacles that are off screen
                if obstacle.is_off_screen():
                    self.obstacles.remove(obstacle)
            
            # Check collisions
            for obstacle in self.obstacles:
                if self.dinosaur.get_rect().colliderect(obstacle.get_rect()):
                    self.game_state = GAME_STATE_GAME_OVER
            
            # Update score (based on time survived)
            current_time = pygame.time.get_ticks()
            self.score = (current_time - self.start_time) // 100  # Score = seconds * 10
    
    def draw(self):
        """Draw all game elements on the screen."""
        # Clear screen with sky blue background
        self.screen.fill(BLUE)
        
        if self.game_state == GAME_STATE_START:
            self.draw_start_screen()
        elif self.game_state == GAME_STATE_PLAYING:
            self.draw_game_screen()
        elif self.game_state == GAME_STATE_GAME_OVER:
            self.draw_game_over_screen()
        
        pygame.display.flip()
    
    def draw_start_screen(self):
        """Draw the start screen."""
        # Draw ground
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, GRAY, ground_rect)
        pygame.draw.line(self.screen, BLACK, (0, SCREEN_HEIGHT - GROUND_HEIGHT), 
                        (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT), 3)
        
        # Draw dinosaur at starting position
        self.dinosaur.draw(self.screen)
        
        # Title
        title_text = self.medium_font.render("Run Dino Run, Jump Over Cactus", True, GREEN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80))
        self.screen.blit(title_text, title_rect)
        
        # Welcome messages
        welcome_text = self.font.render("Welcome to the classic endless runner!", True, BLACK)
        welcome_rect = welcome_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(welcome_text, welcome_rect)
        
        # Controls
        controls_title = self.font.render("CONTROLS:", True, BLACK)
        controls_rect = controls_title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(controls_title, controls_rect)
        
        space_text = self.font.render("SPACE - Jump over obstacles", True, BLACK)
        space_rect = space_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        self.screen.blit(space_text, space_rect)
        
        esc_text = self.font.render("ESC - Quit game", True, BLACK)
        esc_rect = esc_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        self.screen.blit(esc_text, esc_rect)
        
        # Start instruction
        start_text = self.medium_font.render("Press SPACE to Start!", True, RED)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120))
        self.screen.blit(start_text, start_rect)
    
    def draw_game_screen(self):
        """Draw the main game screen."""
        # Draw ground
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, GRAY, ground_rect)
        pygame.draw.line(self.screen, BLACK, (0, SCREEN_HEIGHT - GROUND_HEIGHT), 
                        (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT), 3)
        
        # Draw game objects
        self.dinosaur.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Draw instructions at the bottom
        instruction_text = self.font.render("Press SPACE to jump", True, BLACK)
        self.screen.blit(instruction_text, (10, SCREEN_HEIGHT - 40))
    
    def draw_game_over_screen(self):
        """Draw the game over screen."""
        # Draw ground
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, GRAY, ground_rect)
        pygame.draw.line(self.screen, BLACK, (0, SCREEN_HEIGHT - GROUND_HEIGHT), 
                        (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT), 3)
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(final_score_text, final_score_rect)
        
        # Restart instruction
        restart_text = self.font.render("Press SPACE to restart or ESC to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def start_game(self):
        """Start the game from the start screen."""
        self.game_state = GAME_STATE_PLAYING
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        
        # Reset dinosaur
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT - 60
        self.dinosaur = Dinosaur(DINOSAUR_X_POSITION, ground_y)
        
        # Clear obstacles
        self.obstacles = []
        self.obstacle_spawn_timer = 0
        self.obstacle_spawn_delay = INITIAL_SPAWN_DELAY
    
    def restart_game(self):
        """Reset the game to its initial state."""
        self.game_state = GAME_STATE_PLAYING
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        
        # Reset dinosaur
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT - 60
        self.dinosaur = Dinosaur(DINOSAUR_X_POSITION, ground_y)
        
        # Clear obstacles
        self.obstacles = []
        self.obstacle_spawn_timer = 0
        self.obstacle_spawn_delay = INITIAL_SPAWN_DELAY
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
