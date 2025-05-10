import math
from utils.constants import *
from AI.tools import *
from game import Game
from sprites.pacman import Pacman
from sprites.ghost import Ghost
from sprites.wall import Wall
from sprites.dot import Dot

class AI:
    def __init__(self,game, depth=3):
        self.game=game
        self.depth=depth
        self.pacman = game.pacman
        self.ghosts = game.ghosts
        self.walls = game.walls
        self.dots = game.dots
        self.last_positions = []

    def evaluate(self):
        """Evaluate the current state of the game"""
        # This function evaluates the current state of the game based on Pacman's position, ghost positions, and dot positions.

        evaluation=0
        evaluation+=self.game.score*10 # Pacman's score is a positive factor

        for ghost in self.ghosts:
            ghost_distance = math.sqrt((self.pacman.rect.x - ghost.rect.x)**2 + (self.pacman.rect.y - ghost.rect.y)**2)
            
            # If the gohst is frightened, we want to get closer to it
            # If the ghost is normal, we want to get away from it
            if ghost.state == 'frightened':
                evaluation += (200 / max(1, ghost_distance))
            elif ghost.state == 'normal':
                evaluation -= (300 / max(1, ghost_distance))

        for dot in self.dots:
            dot_distance = math.sqrt((self.pacman.rect.x - dot.rect.x)**2 + (self.pacman.rect.y - dot.rect.y)**2)
            evaluation += 30/max(1,dot_distance)
        
        wall_count = count_adjacent_walls(self.pacman, self.walls)
        if wall_count >= 2:
            evaluation -= 100*wall_count  # Penalize if Pacman is surrounded by walls

        return evaluation
    
    def alpha_beta(self, depth, alpha, beta, is_pacman_turn):
        """Perform the Alpha-Beta pruning algorithm to find the best move"""

        # Base case: if depth is 0 or game over, evaluate the state
        if depth==0 or self.game.lives<=0 or not self.dots:
            return self.evaluate()
        
        if is_pacman_turn:
            max_val = -float('inf')
            moves = get_possible_directions(self.pacman,self.walls)
            for move in moves:
                old_x, old_y = self.pacman.rect.x, self.pacman.rect.y

                # Simulate Pacman's movement
                self.game.pacman.rect.x += move[0] * PACMAN_SPEED
                self.game.pacman.rect.y += move[1] * PACMAN_SPEED

                val = self.alpha_beta(depth-1, alpha, beta, False)

                # Revert Pacman's position
                self.game.pacman.rect.x = old_x
                self.game.pacman.rect.y = old_y

                max_val = max(max_val, val)
                alpha = max(alpha, max_val)
                if beta <= alpha:
                    break
            return max_val

        else:
            min_val = float('inf')
            moves = [UP, DOWN, LEFT, RIGHT]
            for ghost in self.ghosts:
                for move in moves:
                    old_x, old_y = ghost.rect.x, ghost.rect.y

                    #Simulate ghost movement
                    ghost.rect.x += move[0] * GHOST_SPEED
                    ghost.rect.y += move[1] * GHOST_SPEED

                    val = self.alpha_beta(depth-1, alpha, beta, True)

                    # Revert ghost's position
                    ghost.rect.x = old_x
                    ghost.rect.y = old_y

                    min_val = min(min_val, val)
                    beta = min(beta, min_val)
                    if beta <= alpha:
                        break

                
            return min_val

    
    def get_best_direction(self):
        """Get the best direction for Pacman to move using Alpha-Beta pruning"""
        best_move = self.pacman.direction
        best_evaluation = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        moves = get_possible_directions(self.pacman,self.walls)
        for move in moves:
            old_x, old_y = self.game.pacman.rect.x, self.game.pacman.rect.y
            
            # Simulate Pacman's movement
            self.game.pacman.rect.x += move[0] * PACMAN_SPEED
            self.game.pacman.rect.y += move[1] * PACMAN_SPEED
            
            current_pos = (self.game.pacman.rect.x, self.game.pacman.rect.y)
            if current_pos in self.last_positions:
                score = -float('inf') # Penalize if Pacman is in the same position as before
            else:
                score = self.alpha_beta(self.depth-1, alpha, beta, False)
            
            # Revert Pacman's position
            self.game.pacman.rect.x, self.game.pacman.rect.y = old_x, old_y
            
            if score > best_evaluation:
                best_evaluation = score
                best_move = move
        
        self.last_positions.append((self.pacman.rect.x, self.pacman.rect.y))
        if len(self.last_positions) > 5:  #Keep the last 5 positions
            self.last_positions.pop(0)

        return best_move

    def update(self):
        """Update the AI's decision-making process"""
        best_direction = self.get_best_direction()
        self.pacman.set_direction(best_direction)