from ..ghost import Ghost
#from game import Game
from utils.constants import *

class Blinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, BLINKY_SPRITE)
    
    def clone(self):
        new_ghost = Blinky(self.rect.x, self.rect.y)
        new_ghost.direction = self.direction
        new_ghost.speed = self.speed
        new_ghost.state = self.state
        new_ghost.target_tile = self.target_tile
        return new_ghost

    def update(self, game):
        """Blinky directly targets Pacman's current position"""
        if self.state == 'normal':
            pacman_tile = (game.pacman.rect.x // TILE_SIZE, game.pacman.rect.y // TILE_SIZE)
            self.set_target(*pacman_tile)
        elif self.state == 'frightened':
            # When frightened, move randomly (implemented in base class)
            pass
        elif self.state == 'eaten':
            # Return to ghost house
            self.set_target(14, 14)  # Center of ghost house
            
        super().update(game)
