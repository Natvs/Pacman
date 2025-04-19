import pygame
import sys
from utils.constants import *
from game import Game
from ai.LookAhead import LookAhead
from ai.AlphaBeta import AlphaBeta

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()
    
    game = Game(screen)
    game.ai = LookAhead(game, depth=PACMAN_IA_LOOKAHEAD)
    
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_input(event)
        
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)
        if game.state == GAME_WON or game.state == GAME_OVER:
            play = False
    
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_input(event)
            
        clock.tick(FPS)
        pass

if __name__ == "__main__":
    main()
