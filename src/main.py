import pygame
import sys
from utils.constants import *
from game import Game
from sprites.dot import Dot
from ai.LookAhead import LookAhead
from ai.AlphaBeta import AlphaBeta

# Store the last training session's actions
last_training_actions = None

def train_ai(game, screen):
    font = pygame.font.Font(None, 36)
    actions = []  # List to store AI actions
    
    def display_progress(current, total):
        screen.fill(BLACK)
        # Display title
        title_text = font.render("Training AI...", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)
        
        # Display progress count
        count_text = font.render(f"Progress: {current}/{total}", True, WHITE)
        count_rect = count_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(count_text, count_rect)
        
        # Display progress bar
        progress = current / total
        bar_width = 400
        bar_height = 20
        
        # Draw progress
        progress_width = int(bar_width * progress)
        progress_rect = pygame.Rect((WINDOW_WIDTH - bar_width) // 2,
                                  WINDOW_HEIGHT // 2 + 30,
                                  progress_width,
                                  bar_height)
        pygame.draw.rect(screen, WHITE, progress_rect)
        
        pygame.display.flip()
    
    # Initial progress display
    display_progress(0, PACMAN_IA_ITERATIONS)
    
    for i in range(PACMAN_IA_ITERATIONS):
        # Handle Pygame events to keep the window responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Training interrupted.")
                pygame.quit()
                sys.exit()
        
        start_life = game.lives
        start_level = game.level
        game.update()
        if game.lives < start_life:
            print("Pacman lost a life during training.", game.lives, "lives left")
        if start_level < game.level:
            print("Level up to level", game.level)
            
        # Record complete game state
        ghost_states = [{
            'direction': (ghost.direction[0], ghost.direction[1]),
            'position': (ghost.rect.x, ghost.rect.y),
            'state': ghost.state,
            'target': ghost.target if hasattr(ghost, 'target') else None
        } for ghost in game.ghosts]

        # Create a snapshot of dot positions
        dot_positions = [(dot.rect.x, dot.rect.y) for dot in game.dots]
        
        actions.append({
            'pacman': {
                'direction': (game.pacman.direction[0], game.pacman.direction[1]),
                'position': (game.pacman.rect.x, game.pacman.rect.y),
            },
            'ghosts': ghost_states,
            'dots': dot_positions,
            'score': game.score,
            'lives': game.lives,
            'level': game.level,
            'movement_count': game.movement_count
        })
        if game.state == GAME_WON:
            game.reset()
        if game.state == GAME_OVER:
            print("Game Over during training.")
            break
        
        # Update progress display more frequently
        if i % 50 == 0:
            display_progress(i, PACMAN_IA_ITERATIONS)
            #pygame.time.wait(1)  # Small delay to ensure display updates
    
    # Show completion
    display_progress(PACMAN_IA_ITERATIONS, PACMAN_IA_ITERATIONS)
    return actions

def replay_actions(game:Game, actions, clock):
    game.state = PLAYING
    total_actions = len(actions)
    font = pygame.font.Font(None, 24)
    
    def display_iteration(current):
        # Create background rectangle
        text = f"Action: {current}/{total_actions}"
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        
        # Position in top-right corner with padding
        padding = 10
        text_rect.topright = (WINDOW_WIDTH - padding, padding)
        
        # Draw background rectangle
        bg_rect = text_rect.inflate(20, 10)  # Make background slightly larger
        bg_rect.topright = (WINDOW_WIDTH - padding + 10, padding - 5)
        pygame.draw.rect(game.screen, BLACK, bg_rect)
        
        # Draw text
        game.screen.blit(text_surface, text_rect)
    
    for i in range(len(actions)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        action = actions[i]
        
        # Synchronize game state
        game.score = action['score']
        game.lives = action['lives']
        game.level = action['level']
        game.movement_count = action['movement_count']
        
        # Synchronize Pacman
        pacman_state = action['pacman']
        game.pacman.rect.x = pacman_state['position'][0]
        game.pacman.rect.y = pacman_state['position'][1]
        game.pacman.set_direction(pacman_state['direction'])
        
        # Synchronize ghosts
        for ghost, ghost_state in zip(game.ghosts, action['ghosts']):
            if not ghost in game.ghosts: game.ghosts.append(ghost)
            ghost.rect.x = ghost_state['position'][0]
            ghost.rect.y = ghost_state['position'][1]
            ghost.direction = ghost_state['direction']
            ghost.state = ghost_state['state']
            if ghost_state['target'] is not None:
                ghost.target = ghost_state['target']
        
        # Synchronize dots
        game.dots = []
        for x, y in action['dots']:
            dot = Dot(x, y)
            game.dots.append(dot)
        
        game.draw()
        display_iteration(i)  # Display current iteration
        pygame.display.flip()
        clock.tick(FPS)
    
    # Wait a moment after replay
    pygame.time.wait(1000)

def play_game(screen, clock, ai_mode=False):
    # Initialize game
    game = Game(screen)
    game.state = PLAYING
    
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
    train_text = font.render("Press T for AI Training Mode", True, WHITE)
    replay_text = font.render("Press R for AI Replay Mode", True, WHITE)
    
    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 75))
    player_rect = player_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 25))
    train_rect = train_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 25))
    replay_rect = replay_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 75))
    
    # Mode selection loop
    waiting_for_input = True
    while waiting_for_input:
        screen.fill(BLACK)
        screen.blit(title, title_rect)
        screen.blit(player_text, player_rect)
        screen.blit(train_text, train_rect)
        screen.blit(replay_text, replay_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Player mode
                    play_game(screen, clock, ai_mode=False)
                    waiting_for_input = False
                elif event.key == pygame.K_t:  # AI Training mode
                    global last_training_actions
                    # Train AI and save actions
                    training_game = Game(None)  # No display during game updates
                    training_game.state = TRAINING
                    training_game.ai = LookAhead(training_game, depth=PACMAN_IA_DEPTH)
                    last_training_actions = train_ai(training_game, screen)  # But pass screen for progress display
                    
                    # Show training completion message
                    completion_text = font.render("Training Complete!", True, WHITE)
                    completion_rect = completion_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                    screen.fill(BLACK)
                    screen.blit(completion_text, completion_rect)
                    pygame.display.flip()
                    pygame.time.wait(2000)  # Show message for 2 seconds
                    
                elif event.key == pygame.K_r:  # AI Replay mode
                    if last_training_actions is None:
                        # Show message that training is needed first
                        msg_text = font.render("Please run Training Mode first!", True, WHITE)
                        msg_rect = msg_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                        screen.fill(BLACK)
                        screen.blit(msg_text, msg_rect)
                        pygame.display.flip()
                        pygame.time.wait(2000)  # Show message for 2 seconds
                    else:
                        # Create new game for replay
                        game = Game(screen)
                        
                        # Replay the stored actions
                        replay_actions(game, last_training_actions, clock)
                    
                    # Clear screen and continue waiting for input
                    screen.fill(BLACK)
                    pygame.display.flip()
        
        clock.tick(FPS)

if __name__ == "__main__":
    main()
