import math
from utils.constants import *
from AI.tools import *
from game import Game
from sprites.pacman import Pacman
from sprites.ghost import Ghost
from sprites.wall import Wall
from sprites.dot import Dot

class AI:
    def __init__(self, game:Game, depth=3):
        self.game=game
        self.depth=depth
        self.pacman = game.pacman
        self.ghosts = game.ghosts
        self.walls = game.walls
        self.dots = game.dots
        self.last_positions = []
        self.back_countdown = PACMAN_IA_BACKCOUNTDOWN

    def distance(self, x1, x2, y1, y2, type = 'manhattan', coef=1):
        if type == 'manhattan':
            return abs(x1 - x2) + abs(y1 - y2)
        elif type == 'euclidean':
            return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        elif type == 'exponential':
            return math.pow(coef * (abs(x1 - x2) + abs(y1 - y2)), 2)
            
    def evaluate(self, game:Game):
        """Evaluates the current state of the game"""
        # This function evaluates the current state of the game based on Pacman's position, ghost positions, and dot positions.

        evaluation=0
        evaluation+=game.score # Pacman's score is a positive factor

        for ghost in game.ghosts:
            ghost_distance = self.distance(game.pacman.rect.x, ghost.rect.x, game.pacman.rect.y, ghost.rect.y, type='exponential', coef=0.1)

            # If the ghost is frightened, we want to get closer to it
            # If the ghost is normal, we want to get away from it
            if ghost.state == 'frightened':
                evaluation += (100 / max(1, ghost_distance))
                pass
            elif ghost.state == 'normal':
                if ghost_distance < 2*TILE_SIZE:
                    evaluation -= 5000 / ghost_distance  # If Pacman is too close to a ghost, it's game over
                else:
                    evaluation -= 1 / ghost_distance
                pass

        for dot in game.dots:
            dot_distance = self.distance(game.pacman.rect.x, dot.rect.x, game.pacman.rect.y, dot.rect.y, type='euclidean', coef=2)
            evaluation += 1 / (len(game.dots) * dot_distance)  # Closer to the dot is better

        '''wall_count = count_adjacent_walls(game.pacman, game.walls)
        if wall_count >= 2:
            evaluation -= 100*wall_count  # Penalize if Pacman is surrounded by walls'''

        return evaluation
    
    def alpha_beta(self, game:Game, depth, alpha, beta, is_pacman_turn):
        """Perform the Alpha-Beta pruning algorithm to find the best move"""

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

            val = self.alpha_beta(newgame, depth-1, alpha, beta, False)

            max_val = max(max_val, val)
            alpha = max(alpha, max_val)
            if beta <= alpha:
                break
        
            del newgame

        return max_val

    
    def get_best_direction(self):
        """Get the best direction for Pacman to move using Alpha-Beta pruning"""
        best_move = self.pacman.direction
        best_evaluation = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        for ghost in self.ghosts:
            ghost_distance = self.distance(self.pacman.rect.x, ghost.rect.x, self.pacman.rect.y, ghost.rect.y, type='manhattan')
            if ghost_distance < 4*TILE_SIZE:
                self.last_positions.clear()  # Clear the last positions if Pacman is too close to a ghost
                break

        moves = get_possible_directions(self.game)
        for move in moves:
            # Simulate Pacman's movement
            new_game = self.game.clone()
            new_game.pacman.set_direction(move)
            new_game.update()

            current_pos = (new_game.pacman.rect.x, new_game.pacman.rect.y)
            if current_pos in self.last_positions:             
                score = -float('inf') # Penalize if Pacman is in the same position as before
            else:
                score = self.alpha_beta(new_game, self.depth-1, alpha, beta, False)
            if score > best_evaluation:
                best_evaluation = score
                best_move = move

            del new_game

        if (PACMAN_IA_MEMORY > 0):
            self.last_positions.append((self.pacman.rect.x, self.pacman.rect.y))
            if len(self.last_positions) > PACMAN_IA_MEMORY:  #Keep the lasts positions
                self.last_positions.pop(0)

        return best_move

    def update(self):
        """Update the AI's decision-making process"""
        best_direction = self.get_best_direction()
        self.pacman.set_direction(best_direction)