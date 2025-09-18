"""
Main entry point for the Dinosaur Game.
This file initializes pygame and starts the game using the modular components.
"""

import pygame
from game import Game

# Initialize Pygame
pygame.init()


def main():
    """Main function to run the dinosaur game."""
    print("Starting Dinosaur Game...")
    print("Controls:")
    print("- SPACE: Jump")
    print("- ESC: Quit")
    print("- SPACE (when game over): Restart")
    
    game = Game()
    game.run()


# Run the game
if __name__ == "__main__":
    main()
