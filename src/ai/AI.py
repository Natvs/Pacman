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
    
        # Base evaluation starting point (small positive value to encourage movement)
        evaluation = 10
        
        # Strongly reward dot eating
        dots_eaten = len(self.game.dots) - len(game.dots)
        evaluation += dots_eaten * 500

        # Count nearby ghosts and track their distances
        nearby_ghosts = 0
        close_ghosts_penalty = 0
        min_ghost_distance = float('inf')

        possible_moves = get_possible_directions(game)
        
        # Add bonus for being at intersections and turning
        if len(possible_moves) > 2:  # At an intersection
            evaluation += 50  # Bonus for being at intersection
            if game.pacman.direction != game.pacman.next_direction:
                evaluation += 30  # Additional bonus for turning at intersection
        
        for ghost in game.ghosts:
            if game.pacman.rect.colliderect(ghost.rect) and ghost.state == 'normal':
                return float('-inf')
            ghost_distance = self.distance(game.pacman.rect.x, ghost.rect.x, game.pacman.rect.y, ghost.rect.y, type='manhattan', coef=0.1)
            min_ghost_distance = min(min_ghost_distance, ghost_distance)

            # Simplified path safety check
            path_safety = self.distance(game.pacman.rect.x, ghost.rect.x, 
                                     game.pacman.rect.y, ghost.rect.y, 
                                     type='custom', coef=0.8)  # Less sensitive wall detection
            
            # Check if we're moving towards or away from the ghost
            next_pos_x = game.pacman.rect.x + game.pacman.direction[0] * PACMAN_SPEED
            next_pos_y = game.pacman.rect.y + game.pacman.direction[1] * PACMAN_SPEED
            next_distance = self.distance(next_pos_x, ghost.rect.x, next_pos_y, ghost.rect.y, type='manhattan')
            moving_towards_ghost = next_distance < ghost_distance

            if ghost.state == 'frightened':
                evaluation += (300 / max(1, ghost_distance))  # Higher reward for chasing frightened ghosts
            elif ghost.state == 'normal':
                if ghost_distance < 8*TILE_SIZE:
                    nearby_ghosts += 1
                    # Apply smaller penalty if moving away from ghost
                    penalty_multiplier = 1.5 if moving_towards_ghost else 0.5
                    
                    if ghost_distance < 6*TILE_SIZE:
                        evaluation -= (20 * penalty_multiplier) / ghost_distance
                        close_ghosts_penalty += 10
                    elif ghost_distance < 4*TILE_SIZE:
                        evaluation -= (40 * penalty_multiplier) / ghost_distance
                        close_ghosts_penalty += 20
                    elif ghost_distance < 2*TILE_SIZE:
                        evaluation -= (80 * penalty_multiplier) / ghost_distance
                        close_ghosts_penalty += 40
                
                # Simpler path safety penalty
                if path_safety > ghost_distance:
                    evaluation -= (path_safety - ghost_distance) * 10

        # Simplified ghost penalties
        if nearby_ghosts > 0:
            escape_routes = len(possible_moves)
            ghost_penalty = nearby_ghosts * 30
            
            if escape_routes == 1:
                ghost_penalty *= 1.5
            
            evaluation -= ghost_penalty
        
        # Apply accumulated penalty for close ghosts
        evaluation -= close_ghosts_penalty

        # Strongly encourage dot pursuit when ghosts are far
        min_dot_distance = float('inf')
        for dot in game.dots:
            dot_distance = self.distance(game.pacman.rect.x, dot.rect.x, game.pacman.rect.y, dot.rect.y, type='manhattan', coef=1)
            min_dot_distance = min(min_dot_distance, dot_distance)
            # Scale dot reward based on ghost distance
            dot_reward = 200 if min_ghost_distance > 6*TILE_SIZE else 100
            evaluation += dot_reward / dot_distance

        # Extra reward for nearest dot
        if min_dot_distance != float('inf'):
            evaluation += 2000 / min_dot_distance
            
        return evaluation
