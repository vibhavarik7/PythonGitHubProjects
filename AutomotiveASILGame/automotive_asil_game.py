"""
Automotive ASIL/QM Learning Game
A Pygame-based educational game where players learn automotive safety integrity levels.

The player controls a car and must press the correct ASIL/QM key when functionality 
blocks approach to avoid collisions.
"""

import pygame
from game import Game


def main():
    """Main function to run the automotive ASIL game."""
    # Initialize Pygame
    pygame.init()
    
    print("Starting ASIL Highway Dash or Crash ...")
    print("Learn automotive safety integrity levels while playing!")
    print("\nControls:")
    print("- A, B, C, D, Q: ASIL/QM levels")
    print("- SPACE: Start/Restart")
    print("- ESC: Quit")
    
    game = Game()
    game.run()


if __name__ == "__main__":
    main()