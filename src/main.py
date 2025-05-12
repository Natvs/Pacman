import pygame
import sys
from utils.constants import *
from game import Game
from ai.LookAhead import LookAhead
from ai.AlphaBeta import AlphaBeta

def train_ai(game):
    print("Training AI...")
    actions = []  # List to store AI actions
    for i in range(TRAINING_ITERATIONS):
        game.update()
        actions.append(game.pacman.direction)  # Record the AI's chosen direction
        if game.state == GAME_WON or game.state == GAME_OVER:
            game.reset()
        if i % 10 == 0:  # Show progress every 10 iterations
            print(f"Training progress: {i}/{TRAINING_ITERATIONS}")
    print("Training complete!")
    return actions

def replay_actions(game, actions, clock):
    print("Replaying AI actions...")
    for action in actions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        game.pacman.set_direction(action)
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)  # Slower speed for visualization

def main():
    pygame.init()
    
    # Initialize game without display for training
    training_game = Game(None)  # Pass None as screen to skip rendering
    training_game.state = TRAINING
    training_game.ai = AlphaBeta(training_game, depth=7)
    
    # Train the AI and get actions
    actions = train_ai(training_game)
    
    # Initialize display for replay
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pacman - AI Training Replay")
    clock = pygame.time.Clock()
    
    # Create new game instance for replay
    game = Game(screen)
    game.state = PLAYING
    
    # Replay the training actions
    replay_actions(game, actions, clock)

if __name__ == "__main__":
    main()
