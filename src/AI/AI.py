import math
from utils.constants import *
from AI.tools import *
from game import Game
from sprites.pacman import Pacman
from sprites.ghosts import Ghost
from sprites.wall import Wall
from sprites.dot import Dot

class AI:
    def __init__(self,game, depth=3):
        self.game=game
        self.depth=depth
        self.pacamn = game.pacman
        self.ghosts = game.ghosts
        self.walls = game.walls
        self.dots = game.dots

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
            evaluation += 50/max(1,dot_distance)
        
        if count_adjacent_walls(self.pacman,self.walls) >= 2:
            evaluation -= 100  # Penalize if Pacman is surrounded by walls

        return evaluation
    
    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        """Perform the Alpha-Beta pruning algorithm to find the best move"""

        # Base case: if depth is 0 or game over, evaluate the state
        if depth==0 or self.game.lives<=0 or not self.dots:
            return self.evaluate()
        return
    
    def get_best_direction(self):
        pass

    def update(self):
        """Update the AI's decision-making process"""
        best_direction = self.get_best_direction()
        self.pacman.set_direction(best_direction)