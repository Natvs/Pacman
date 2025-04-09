from ..ghost import Ghost
from utils.constants import *

class Inky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, INKY_SPRITE)
        
    def clone(self):
        new_ghost = Inky(self.rect.x, self.rect.y)
        new_ghost.direction = self.direction
        new_ghost.speed = self.speed
        new_ghost.state = self.state
        new_ghost.target_tile = self.target_tile
        return new_ghost

    def update(self, wall_group, pacman, blinky):
        """Inky uses both Pacman and Blinky's position for targeting"""
        if self.state == 'normal':
            # First, get the position 2 tiles ahead of Pacman
            pacman_tile = (pacman.rect.x // TILE_SIZE, pacman.rect.y // TILE_SIZE)
            intermediate_x = pacman_tile[0] + (2 * pacman.direction[0])
            intermediate_y = pacman_tile[1] + (2 * pacman.direction[1])
            
            # Get Blinky's position
            blinky_tile = (blinky.rect.x // TILE_SIZE, blinky.rect.y // TILE_SIZE)
            
            # Calculate the vector from Blinky to the intermediate point
            vector_x = intermediate_x - blinky_tile[0]
            vector_y = intermediate_y - blinky_tile[1]
            
            # Double the vector to get Inky's target
            target_x = intermediate_x + vector_x
            target_y = intermediate_y + vector_y
            
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
            
        super().update(wall_group)
