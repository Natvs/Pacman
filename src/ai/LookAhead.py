import math
import os
import concurrent.futures
from utils.constants import *
from ai.AI import AI
from ai.tools import *
from game import Game
from sprites.pacman import Pacman
from sprites.ghost import Ghost
from sprites.wall import Wall
from sprites.dot import Dot

# Current score : 1274

class LookAhead(AI):
    def __init__(self, game:Game, depth=3):
        super().__init__(game)
        self.game = game
        self.depth = depth
        self.pacman = game.pacman
        self.ghosts = game.ghosts
        self.walls = game.walls
        self.dots = game.dots
        self.grid_positions = {}  # Track positions by grid cells
        self.stagnation_threshold = 20  # Reduced threshold
        self.max_workers = os.cpu_count()
        self.last_dots_count = len(game.dots)
        self.last_directions = []  # Track recent directions
        self.direction_memory = 4  # Remember last 4 moves
        self.momentum_bonus = 0.3  # Increased bonus for maintaining direction
        self.reverse_penalty = 0.3  # Stronger penalty for reversing

    def look_ahead(self, game:Game, depth):
        """Perform the look-ahead algorithm to find the best move"""

        # Base case: if depth is 0 or game over, evaluates the state
        if depth==0 or game.lives<=0 or not game.dots:
            return self.evaluate(game)
        
        max_val = -float('inf')
        moves = get_possible_directions(game)
        for move in moves:
            # Simulate Pacman's movement
            newgame = game.clone()       
            newgame.pacman.set_direction(move)
            newgame.update()

            val = self.look_ahead(newgame, depth-1)

            max_val = max(max_val, val)
        
            del newgame

        return max_val

    def evaluate_move(self, move, game, depth):
        """Evaluate a single move for parallel execution"""
        new_game = game.clone()
        new_game.pacman.set_direction(move)
        new_game.update()
        
        # Convert pixel position to grid position
        grid_x = new_game.pacman.rect.x // TILE_SIZE
        grid_y = new_game.pacman.rect.y // TILE_SIZE
        grid_pos = (grid_x, grid_y)
        
        score = self.look_ahead(new_game, depth-1)
        
        # Apply increasing penalty based on grid position frequency
        freq = self.grid_positions.get(grid_pos, 0)
        if freq > 0:
            penalty = min((freq / self.stagnation_threshold) ** 2, 0.8)
            score *= (1.0 - penalty)
        
        # Add stronger momentum system
        if len(self.last_directions) > 0:
            last_dir = self.last_directions[-1]
            if move[0] == -last_dir[0] and move[1] == -last_dir[1]:
                # Stronger penalty for complete reversal
                score *= self.reverse_penalty
            elif len(self.last_directions) >= 2:
                # Check for oscillation pattern
                if move == self.last_directions[-2]:
                    score *= 0.4  # Heavy penalty for back-and-forth movement
        
        del new_game
        return (move, score)
    
    def get_best_direction(self):
        """Get the best direction for Pacman to move using look-ahead search"""
        best_move = self.pacman.direction
        best_evaluation = -float('inf')
        
        # Check if any dots were eaten
        current_dots = len(self.game.dots)
        if current_dots < self.last_dots_count:
            # Reset grid positions and direction history when a dot is eaten
            self.grid_positions = {}
            self.last_directions = []  # Reset movement history too
        self.last_dots_count = current_dots

        moves = get_possible_directions(self.game)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.evaluate_move, move, self.game.clone(), self.depth): move for move in moves}              
            for future in concurrent.futures.as_completed(futures):
                move, score = future.result()
                if score > best_evaluation:
                    best_evaluation = score
                    best_move = move

        # Update grid position frequency with increased penalty for revisits
        grid_x = self.pacman.rect.x // TILE_SIZE
        grid_y = self.pacman.rect.y // TILE_SIZE
        grid_pos = (grid_x, grid_y)
        # Increment counter more aggressively for revisits
        current_freq = self.grid_positions.get(grid_pos, 0)
        self.grid_positions[grid_pos] = current_freq + (2 if current_freq > 0 else 1)
        
        # Update direction history
        self.last_directions.append(best_move)
        if len(self.last_directions) > self.direction_memory:
            self.last_directions.pop(0)

        return best_move

    def update(self):
        """Update the AI's decision-making process"""
        best_direction = self.get_best_direction()
        self.pacman.set_direction(best_direction)
