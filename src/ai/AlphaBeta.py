from utils.constants import *
from ai.tools import *
from game import Game
from ai.AI import AI
from sprites.pacman import Pacman
from sprites.ghost import Ghost
from sprites.wall import Wall
from sprites.dot import Dot
import os
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor  # Utiliser ThreadPoolExecutor au lieu de ProcessPoolExecutor


# Current score : 1228

class AlphaBeta(AI):
    def __init__(self, game:Game, depth=3):
        super().__init__(game)
        self.depth=depth
        self.pacman = game.pacman
        self.ghosts = game.ghosts
        self.walls = game.walls
        self.dots = game.dots
        self.last_positions = []
        self.back_countdown = PACMAN_IA_BACKCOUNTDOWN

    
    def alpha_beta(self, game:Game, depth, alpha, beta, is_pacman_turn):
        """Perform the Alpha-Beta pruning algorithm to find the best move"""

        # Base case: if depth is 0 or game over, evaluates the state
        if depth==0 or game.lives<=0 or not game.dots:
            return self.evaluate(game)
        
        moves = get_possible_directions(game)

        if is_pacman_turn:
            max_val = -float('inf')
            for move in moves:
                newgame = game.clone()
                newgame.update(update_ghosts=False)
                newgame.pacman.set_direction(move)
                val = self.alpha_beta(newgame, depth-1, alpha, beta, False)
                max_val = max(max_val, val)
                alpha = max(alpha, max_val)
                if beta <= alpha:
                    break     
                del newgame
            return max_val
        else:
            min_val = float('inf')
            for move in moves:
                newgame = game.clone()
                newgame.update(update_pacman=False)
                newgame.pacman.set_direction(move)
                val = self.alpha_beta(newgame, depth-1, alpha, beta, True)
                min_val = min(min_val, val)
                beta = min(beta, min_val)
                if beta <= alpha:
                    break
                del newgame
            return min_val
        
    def evaluate_move(self, move):
        """Évalue un mouvement pour la parallélisation"""
        new_game = self.game.clone()
        new_game.pacman.set_direction(move)
        new_game.update(update_ghosts=False)
        
        current_pos = (new_game.pacman.rect.x, new_game.pacman.rect.y)
        if current_pos in self.last_positions:
            score = -float('inf')  # Penalize if Pacman is in the same position as before
        else:
            score = self.alpha_beta(new_game, self.depth-1, -float('inf'), float('inf'), True)
        
        del new_game
        return (move, score)
    
    def get_best_direction(self):
        """Get the best direction for Pacman to move using Alpha-Beta pruning with threading"""
        best_move = self.pacman.direction
        best_evaluation = -float('inf')

        for ghost in self.ghosts:
            ghost_distance = self.distance(self.pacman.rect.x, ghost.rect.x, self.pacman.rect.y, ghost.rect.y, type='manhattan')
            if ghost_distance < 4*TILE_SIZE:
                self.last_positions.clear()  # Clear the last positions if Pacman is too close to a ghost
                break

        moves = get_possible_directions(self.game)
        
        # Use ThreadPoolExecutor to evaluate moves in parallel
        max_workers = os.cpu_count()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_move = {executor.submit(self.evaluate_move, move): move for move in moves}
            
            # Wait for all futures to complete and get the results
            for future in concurrent.futures.as_completed(future_to_move):
                move_result = future.result()
                move, score = move_result
                if score > best_evaluation:
                    best_evaluation = score
                    best_move = move

        if (PACMAN_IA_MEMORY > 0):
            self.last_positions.append((self.pacman.rect.x, self.pacman.rect.y))
            if len(self.last_positions) > PACMAN_IA_MEMORY:
                self.last_positions.pop(0)

        return best_move
    
    def update(self):
        """Update the AI's decision-making process"""
        best_direction = self.get_best_direction()
        self.pacman.set_direction(best_direction)