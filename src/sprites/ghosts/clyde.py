from ..ghost import Ghost
from utils.constants import *
import math

class Clyde(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, CLYDE_SPRITE)
        self.scatter_tile = (0, GRID_HEIGHT - 1)  # Bottom-left corner
        
    def update(self, wall_group, pacman):
        """Clyde targets Pacman directly when far, but runs away when close"""
        if self.state == 'normal':
            pacman_tile = (pacman.rect.x // TILE_SIZE, pacman.rect.y // TILE_SIZE)
            current_tile = self.get_tile_pos()
            
            # Calculate distance to Pacman
            distance = math.sqrt(
                (current_tile[0] - pacman_tile[0]) ** 2 +
                (current_tile[1] - pacman_tile[1]) ** 2
            )
            
            # If distance is greater than 8 tiles, target Pacman
            # Otherwise, go to scatter position
            if distance > 8:
                self.set_target(*pacman_tile)
            else:
                self.set_target(*self.scatter_tile)
                
        elif self.state == 'frightened':
            # When frightened, move randomly (implemented in base class)
            pass
        elif self.state == 'eaten':
            # Return to ghost house
            self.set_target(14, 14)  # Center of ghost house
            
        super().update(wall_group)
