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
        """Evaluates the current state of the game with improved dot collection and ghost avoidance"""
        if game.lives < self.game.lives:
            return float('-inf')
        
        if len(game.dots) == 0:
            return float('inf')

        evaluation = 0
        pacman_x = game.pacman.rect.x
        pacman_y = game.pacman.rect.y
        
        # Track the minimum distance to any ghost and count nearby ghosts
        min_ghost_distance = float('inf')
        nearby_ghosts = 0
        ghost_danger = 0
        
        # Calculate ghost distances and danger levels
        for ghost in game.ghosts:
            if game.pacman.rect.colliderect(ghost.rect) and ghost.state == 'normal':
                return float('-inf')
                
            ghost_distance = self.distance(pacman_x, ghost.rect.x, pacman_y, ghost.rect.y, type='manhattan')
            min_ghost_distance = min(min_ghost_distance, ghost_distance)
            
            if ghost.state == 'frightened':
                # Reward for chasing frightened ghosts, but don't get too distracted
                chase_reward = 200 / max(1, ghost_distance)
                evaluation += min(chase_reward, 300)
            elif ghost.state == 'normal':
                # Calculate danger based on distance and position with progressive scaling
                if ghost_distance < 8 * TILE_SIZE:
                    nearby_ghosts += 1
                    # Exponential danger increase as distance decreases
                    danger = 600 * math.pow(2, (8 * TILE_SIZE - ghost_distance) / (2 * TILE_SIZE))
                    
                    # Check if ghost is blocking path to nearest dot
                    if len(game.dots) > 0:
                        nearest_dot = min(game.dots, key=lambda d: self.distance(pacman_x, d.rect.x, pacman_y, d.rect.y))
                        ghost_to_dot = self.distance(ghost.rect.x, nearest_dot.rect.x, ghost.rect.y, nearest_dot.rect.y)
                        
                        # More sophisticated path blocking detection
                        if ghost_to_dot < ghost_distance:
                            # Calculate if the ghost is between Pacman and the dot
                            pacman_to_dot = self.distance(pacman_x, nearest_dot.rect.x, pacman_y, nearest_dot.rect.y)
                            if ghost_to_dot < pacman_to_dot:
                                danger *= 2.0  # Doubled danger if ghost blocks direct path
                    
                    ghost_danger += danger
        
        # Apply ghost danger penalties
        evaluation -= ghost_danger
        
        # Get possible moves for escape route analysis
        possible_moves = get_possible_directions(game)
        escape_routes = len(possible_moves)
        
        # Evaluate dots with more dynamic weighting based on safety
        safety_factor = min(1.0, max(0.3, min_ghost_distance / (6 * TILE_SIZE)))
        base_dot_value = 500  # Increased base value for dots
        dot_value = base_dot_value * safety_factor  # Scale with safety
        
        # Find nearest dot and evaluate dot clusters
        if len(game.dots) > 0:
            min_dot_distance = float('inf')
            dots_in_area = 0
            
            for dot in game.dots:
                dot_distance = self.distance(pacman_x, dot.rect.x, pacman_y, dot.rect.y, type='manhattan')
                min_dot_distance = min(min_dot_distance, dot_distance)
                
                # Count dots in nearby area
                if dot_distance < 6 * TILE_SIZE:
                    dots_in_area += 1
            
            # Enhanced reward system for dots
            dot_reward = (dot_value / max(1, min_dot_distance)) * safety_factor
            cluster_bonus = 1 + (0.3 * dots_in_area)  # Increased cluster bonus
            path_safety = 1.0 if escape_routes > 2 else 0.7  # Reduced reward in constrained areas
            dot_reward *= cluster_bonus * path_safety
            evaluation += dot_reward
        
        # Penalties for dangerous positions
        if nearby_ghosts > 0:
            if escape_routes == 1:
                evaluation -= 1000 * nearby_ghosts  # Severe penalty for dead ends
            elif escape_routes == 2:
                evaluation -= 500 * nearby_ghosts   # Significant penalty for corridors
            
            # Extra penalty when multiple ghosts are nearby
            if nearby_ghosts > 1:
                evaluation -= 300 * (nearby_ghosts - 1) * (4 - escape_routes)
        
        # Base reward for having more escape routes
        evaluation += 50 * escape_routes
        
        # Bonus for eating dots
        evaluation += (len(self.game.dots) - len(game.dots)) * 300
        
        return evaluation
