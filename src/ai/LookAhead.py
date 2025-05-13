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
        self.game=game
        self.depth=depth
        self.pacman = game.pacman
        self.ghosts = game.ghosts
        self.walls = game.walls
        self.dots = game.dots
        self.last_positions = []
        self.max_workers = os.cpu_count()  # Number of CPU cores available

    def look_ahead(self, game:Game, depth):
        """Perform the look-ahead algorithm to find the best move"""

        # Base case: if depth is 0 or game over, evaluates the state
        if depth==0 or game.lives<=0 or not game.dots:
            return self.evaluate(game)
        
        min_val = float('inf')
        moves = get_possible_directions(game)
        for move in moves:
            # Simulate Pacman's movement

            newgame = game.clone()       
            newgame.pacman.set_direction(move)
            newgame.update()

            val = self.look_ahead(newgame, depth-1)

            min_val = min(min_val, val)
        
            del newgame

        return min_val

    def evaluate_move(self, move, game, depth):
        """Evaluate a single move for parallel execution"""
        new_game = game.clone()
        new_game.pacman.set_direction(move)
        new_game.update()
        
        current_pos = (new_game.pacman.rect.x, new_game.pacman.rect.y)
        if current_pos in self.last_positions:             
            score = -float('inf')  # Penalize if Pacman is in the same position as before
        else:
            score = self.look_ahead(new_game, depth-1)
            
        del new_game
        return (move, score)
    
    def get_best_direction(self):
        """Get the best direction for Pacman to move using Alpha-Beta pruning"""
        best_move = self.pacman.direction
        best_evaluation = -float('inf')

        for ghost in self.ghosts:
            ghost_distance = self.distance(self.pacman.rect.x, ghost.rect.x, self.pacman.rect.y, ghost.rect.y, type='manhattan')
            if ghost_distance < PACMAN_IA_AVOID_AREA:
                self.last_positions.clear()  # Clear the last positions if Pacman is too close to a ghost
                break

        moves = get_possible_directions(self.game)
        

        # with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
        #     futures = {executor.submit(self.evaluate_move, move, self.game, self.depth): move for move in moves}
            
            
        #     for future in concurrent.futures.as_completed(futures):
        #         move, score = future.result()
        #         if score > best_evaluation:
        #             best_evaluation = score
        #             best_move = move

        for move in moves:
            move, score = self.evaluate_move(move, self.game, self.depth)
            if score > best_evaluation:
                best_evaluation = score
                best_move = move

        if (PACMAN_IA_MEMORY > 0):
            self.last_positions.append((self.pacman.rect.x, self.pacman.rect.y))
            if len(self.last_positions) > PACMAN_IA_MEMORY:  #Keep the lasts positions
                self.last_positions.pop(0)

        return best_move

    def update(self):
        """Update the AI's decision-making process"""
        best_direction = self.get_best_direction()
        self.pacman.set_direction(best_direction)