from ..ghost import Ghost
#from game import Game
from utils.constants import *

class Pinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, PINKY_SPRITE)
        
    def clone(self):
        new_ghost = Pinky(self.rect.x, self.rect.y)
        new_ghost.direction = self.direction
        new_ghost.speed = self.speed
        new_ghost.state = self.state
        new_ghost.target_tile = self.target_tile
        return new_ghost

    def update(self, game):
        """Pinky targets 4 tiles ahead of Pacman's current direction"""
        if self.state == 'normal':
            # Calculate target position (4 tiles ahead of Pacman)
            pacman_tile = (game.pacman.rect.x // TILE_SIZE, game.pacman.rect.y // TILE_SIZE)
            target_x = pacman_tile[0] + (4 * game.pacman.direction[0])
            target_y = pacman_tile[1] + (4 * game.pacman.direction[1])
            
            # Keep target within bounds
            target_x = max(0, min(target_x, GRID_WIDTH - 1))
            target_y = max(0, min(target_y, GRID_HEIGHT - 1))
            
            self.set_target(target_x, target_y)
            
        elif self.state == 'frightened':
            # When frightened, move randomly (implemented in base class)
            pass
        elif self.state == 'eaten':
            # Return to ghost house
            self.set_target(14, 14)  # Center of ghost house
            
        super().update(game)
