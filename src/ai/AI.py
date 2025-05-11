import math
from utils.constants import *
from game import Game
from ai.tools import *

class AI:

    def __init__(self, game):
        self.game = game

    def distance(self, x1, x2, y1, y2, type = 'manhattan', coef=1):
        if type == 'manhattan':
            return abs(x1 - x2) + abs(y1 - y2)
        elif type == 'euclidean':
            return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        elif type == 'exponential':
            return math.pow(coef * (abs(x1 - x2) + abs(y1 - y2)), 2)
        elif type == 'custom':
            dist = self.distance(x1, x2, y1, y2, type='exponential', coef=coef)
            min_x = min(x1, x2)
            min_y = min(y1, y2)
            max_x = max(x1, x2)
            max_y = max(y1, y2)
            for x in range(min_x, max_x, TILE_SIZE):
                for y in range(min_y, max_y, TILE_SIZE):
                    if not self.game.get_access(x, y):
                        return 2*dist
            return dist

    def evaluate(self, game:Game):
        """Evaluates the current state of the game"""
        # This function evaluates the current state of the game based on Pacman's position, ghost positions, and dot positions.

        if game.lives < self.game.lives:
            return float('-inf')
    
        evaluation = 0
        evaluation +=(len(self.game.dots) - len(game.dots))*10

        # Count nearby ghosts and track their distances
        nearby_ghosts = 0
        close_ghosts_penalty = 0

        possible_moves = get_possible_directions(game)
        
        for ghost in game.ghosts:
            if game.pacman.rect.colliderect(ghost.rect) and ghost.state == 'normal':
                return float('-inf')
            ghost_distance = self.distance(game.pacman.rect.x, ghost.rect.x, game.pacman.rect.y, ghost.rect.y, type='euclidean', coef=0.1)

            # If the ghost is frightened, we want to get closer to it
            # If the ghost is normal, we want to get away from it
            if ghost.state == 'frightened':
                evaluation += (100 / max(1, ghost_distance))
            elif ghost.state == 'normal':
                if ghost_distance < 4*TILE_SIZE:
                    nearby_ghosts += 1
                if ghost_distance < 4*TILE_SIZE:
                    evaluation -= 50 / ghost_distance
                elif ghost_distance < 3*TILE_SIZE:
                    evaluation -= 100 / ghost_distance  
                elif ghost_distance < 2*TILE_SIZE:
                    evaluation -= 150 / ghost_distance  # Increased penalty for very close ghosts
                    close_ghosts_penalty += 50  # Add penalty for each close ghost
                else:
                    evaluation -= 2 / ghost_distance  # Slightly increased penalty for all ghosts

        # Add extra penalty when multiple ghosts are nearby (dangerous situation)
        if nearby_ghosts > 1:
            # Higher penalty when few escape routes
            if len(possible_moves) <= 2:
                evaluation -= 200 * (nearby_ghosts - 1)  # Very dangerous situation
            else:
                evaluation -= 100 * (nearby_ghosts - 1)
        
        # Apply accumulated penalty for close ghosts
        evaluation -= close_ghosts_penalty

        # General penalty for being in an area with few escape routes
        if len(possible_moves) == 1:
            evaluation -= 50  # Dead end penalty
        elif len(possible_moves) == 2:
            evaluation -= 20  # Corridor penalty

        for dot in game.dots:
            if game.pacman.rect.colliderect(dot.rect):
                evaluation+= 500
            dot_distance = self.distance(game.pacman.rect.x, dot.rect.x, game.pacman.rect.y, dot.rect.y, type='euclidean', coef=2)
            evaluation += 1 / (len(game.dots) * dot_distance)  # Closer to the dot is better

        return evaluation