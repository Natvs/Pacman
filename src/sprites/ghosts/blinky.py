from ..ghost import Ghost
from utils.constants import *

class Blinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, BLINKY_SPRITE)
        
    def update(self, wall_group, pacman):
        """Blinky directly targets Pacman's current position"""
        if self.state == 'normal':
            pacman_tile = (pacman.rect.x // TILE_SIZE, pacman.rect.y // TILE_SIZE)
            self.set_target(*pacman_tile)
        elif self.state == 'frightened':
            # When frightened, move randomly (implemented in base class)
            pass
        elif self.state == 'eaten':
            # Return to ghost house
            self.set_target(14, 14)  # Center of ghost house
            
        super().update(wall_group)
