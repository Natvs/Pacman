import pygame
import sys
from utils.constants import *
from game import Game
from ai.LookAhead import LookAhead
from ai.AlphaBeta import AlphaBeta

def train_ai(game):
    print("Training AI...")
    for i in range(TRAINING_ITERATIONS):
        game.update()
        if game.state == GAME_WON or game.state == GAME_OVER:
            game.reset()
        if i % 10 == 0:  # Show progress every 10 iterations
            print(f"Training progress: {i}/{TRAINING_ITERATIONS}")
    print("Training complete!")

def main():
    pygame.init()
    
    # Initialize game without display for training
    game = Game(None)  # Pass None as screen to skip rendering
    game.state = TRAINING
    game.ai = AlphaBeta(game, depth=7)
    
    # Train the AI
    train_ai(game)
    
    # Initialize display for actual game
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()
    
    # Create new game instance with trained AI settings
    game = Game(screen)
    game.ai = AlphaBeta(game, depth=7)
    game.state = PLAYING
    
    # Main game loop
    while game.state != GAME_OVER and game.state != GAME_WON:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_input(event)
        
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)
    
    # Keep window open after game ends
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
