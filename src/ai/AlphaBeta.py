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


    def evaluate(self, game:Game):
        """Evaluates the current state of the game"""
        # This function evaluates the current state of the game based on Pacman's position, ghost positions, and dot positions.
        if game.lives < self.game.lives:
            return float('-inf')
        evaluation = 0
        evaluation += game.score # Pacman's score is a positive factor

        # Count nearby ghosts and track their distances
        nearby_ghosts = 0
        close_ghosts_penalty = 0

        possible_moves = get_possible_directions(game)
        
        for ghost in game.ghosts:
            if game.pacman.rect.colliderect(ghost.rect) and ghost.state == 'normal':
                return float('-inf')  # Extremely negative score for colliding with a ghost
            ghost_distance = self.distance(game.pacman.rect.x, ghost.rect.x, game.pacman.rect.y, ghost.rect.y, type='custom', coef=0.1)

            # If the ghost is frightened, we want to get closer to it
            # If the ghost is normal, we want to get away from it
            if ghost.state == 'frightened':
                evaluation += (100 / max(1, ghost_distance))
            elif ghost.state == 'normal':
                if ghost_distance < 4*TILE_SIZE:
                    nearby_ghosts += 1
                    
                if ghost_distance < 2*TILE_SIZE:
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
            dot_distance = self.distance(game.pacman.rect.x, dot.rect.x, game.pacman.rect.y, dot.rect.y, type='euclidean', coef=2)
            evaluation += 1 / (len(game.dots) * dot_distance)  # Closer to the dot is better

        return evaluation


    
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