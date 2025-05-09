import math
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
    def __init__(self, game:Game, depth=3,max_workers=4):
        super().__init__(game)
        self.game=game
        self.depth=depth
        self.pacman = game.pacman
        self.ghosts = game.ghosts
        self.walls = game.walls
        self.dots = game.dots
        self.last_positions = []
        self.max_workers = max_workers

    def evaluate(self, game:Game):
        """Evaluates the current state of the game"""
        
        # This function evaluates the current state of the game based on Pacman's position, ghost positions, and dot positions.

        evaluation=0
        evaluation+=game.score # Pacman's score is a positive factor
        evaluate_dots = True

        min_ghost_distance = float('inf')
        for ghost in game.ghosts:
            ghost_distance = self.distance(game.pacman.rect.x, ghost.rect.x, game.pacman.rect.y, ghost.rect.y, type='manhattan', coef=0.1)
            min_ghost_distance = min(min_ghost_distance, ghost_distance) 
            # If the ghost is frightened, we want to get closer to it
            # If the ghost is normal, we want to get away from it
            if ghost.state == 'frightened':
                evaluation += (100 / max(1, ghost_distance))
                pass
            elif ghost.state == 'normal':
                if ghost_distance < PACMAN_IA_AVOID_AREA:
                    evaluation -= 100 / ghost_distance  # If Pacman is too close to a ghost, it's game over
                    #evaluate_dots = False
                else:
                    evaluation -= 0.5 / ghost_distance
                pass
        
        dots_remaining_factor = len(game.dots)/len(self.dots) if len(self.dots) > 0 else 0

        if evaluate_dots:
            closest_dot_distance = float('inf')
            is_heading_to_dot =  False
            for dot in game.dots:
                dot_distance = self.distance(game.pacman.rect.x, dot.rect.x, game.pacman.rect.y, dot.rect.y, type='manhattan', coef=2)
                closest_dot_distance = min(closest_dot_distance, dot_distance)

                pacman_dir = game.pacman.direction
                if pacman_dir == 'up' and abs(game.pacman.rect.x - dot.rect.x) < 20 and dot.rect.y < game.pacman.rect.y:
                    is_heading_to_dot = True
                elif pacman_dir == 'down' and abs(game.pacman.rect.x - dot.rect.x) < 20 and dot.rect.y > game.pacman.rect.y:
                    is_heading_to_dot = True
                elif pacman_dir == 'left' and abs(game.pacman.rect.y - dot.rect.y) < 20 and dot.rect.x < game.pacman.rect.x:
                    is_heading_to_dot = True
                elif pacman_dir == 'right' and abs(game.pacman.rect.y - dot.rect.y) < 20 and dot.rect.x > game.pacman.rect.x:
                    is_heading_to_dot = True
        
        if closest_dot_distance != float('inf'):
            dot_weight = 400 * (1.5 - dots_remaining_factor) 
            evaluation += dot_weight / closest_dot_distance

            if is_heading_to_dot and min_ghost_distance > PACMAN_IA_AVOID_AREA * 2:
                evaluation += 150  # Significant bonus for heading straight to dots when safe
        
        # Encourage direction changes that lead to dots when safe
        current_real_direction = self.pacman.direction
        if game.pacman.direction != current_real_direction and is_heading_to_dot and min_ghost_distance > PACMAN_IA_AVOID_AREA:
            evaluation += 100  # Bonus for changing direction to collect dots when safe

        '''wall_count = count_adjacent_walls(game.pacman, game.walls)
        if wall_count >= 2:
            evaluation -= 100*wall_count  # Penalize if Pacman is surrounded by walls'''

        return evaluation
    
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
        

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.evaluate_move, move, self.game, self.depth): move for move in moves}
            
            
            for future in concurrent.futures.as_completed(futures):
                move, score = future.result()
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