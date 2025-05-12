import pygame
import sys
from utils.constants import *
from game import Game
from ai.LookAhead import LookAhead
from ai.AlphaBeta import AlphaBeta

def train_ai(game):
    print("Training AI...")
    actions = []  # List to store AI actions
    for i in range(PACMAN_IA_ITERATIONS):
        game.update()
        actions.append(game.pacman.direction)  # Record the AI's chosen direction
        if game.state == GAME_WON:
            game.reset()
        if game.state == GAME_OVER:
            break
        if i % 10 == 0:  # Show progress every 10 iterations
            print(f"Training progress: {i}/{PACMAN_IA_ITERATIONS}")
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
    
    # Wait a moment after replay
    pygame.time.wait(1000)

def play_game(screen, clock, ai_mode=False):
    # Initialize game
    game = Game(screen)
    game.state = PLAYING
    
    if ai_mode:
        game.ai = AlphaBeta(game, depth=PACMAN_IA_DEPTH)
    
    # Main game loop
    while game.state != GAME_OVER and game.state != GAME_WON:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not ai_mode:  # Only handle player input in player mode
                game.handle_input(event)
        
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)
    
    # Display final score
    final_score = game.score
    font = pygame.font.Font(None, 36)
    if game.state == GAME_WON:
        result_text = f"YOU WON! Score: {final_score}"
    else:
        result_text = f"GAME OVER. Final Score: {final_score}"
    
    text = font.render(result_text, True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    # Wait for a moment before exiting
    pygame.time.wait(3000)

def main():
    pygame.init()
    
    # Initialize display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()
    
    # Selection screen
    font = pygame.font.Font(None, 36)
    title = font.render("Select Mode:", True, WHITE)
    player_text = font.render("Press P for Player Mode", True, WHITE)
    ai_text = font.render("Press A for AI Mode", True, WHITE)
    
    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    player_rect = player_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    ai_rect = ai_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
    
    # Mode selection loop
    waiting_for_input = True
    while waiting_for_input:
        screen.fill(BLACK)
        screen.blit(title, title_rect)
        screen.blit(player_text, player_rect)
        screen.blit(ai_text, ai_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Player mode
                    play_game(screen, clock, ai_mode=False)
                    waiting_for_input = False
                elif event.key == pygame.K_a:  # AI mode
                    # Train AI first
                    training_game = Game(None)
                    training_game.state = TRAINING
                    training_game.ai = AlphaBeta(training_game, depth=PACMAN_IA_DEPTH)
                    actions = train_ai(training_game)
                    
                    # Create game for replay
                    game = Game(screen)
                    game.state = PLAYING
                    replay_actions(game, actions, clock)
                    
                    # Clear screen and continue waiting for input
                    screen.fill(BLACK)
                    pygame.display.flip()
        
        clock.tick(FPS)

if __name__ == "__main__":
    main()
