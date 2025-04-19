from utils.constants import *

def count_adjacent_walls(pacman,walls):
        """Count the number of walls adjacent to Pacman"""
        count = 0
        x, y = pacman.rect.x, pacman.rect.y
        for dx, dy in [(0, TILE_SIZE), (0, -TILE_SIZE), 
                      (TILE_SIZE, 0), (-TILE_SIZE, 0)]:
            if is_wall(walls,x + dx, y + dy):
                count += 1
        return count
    
def is_wall(walls, x, y):
    """Check if there is a wall at the given coordinates"""
    for wall in walls:
        if wall.rect.x == x and wall.rect.y == y:
             return True
    return False

def get_possible_directions(game):
    """Get possible directions for Pacman to move"""
    possible_directions = []

    for direction in [UP, DOWN, LEFT, RIGHT]:
         if game.pacman.can_move(direction, game):
            possible_directions.append(direction)
    
    return possible_directions