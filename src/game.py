import pygame
from utils.constants import *
from sprites.wall import Wall
from sprites.dot import Dot
from sprites.pacman import Pacman
from sprites.ghosts.blinky import Blinky
from sprites.ghosts.pinky import Pinky
from sprites.ghosts.inky import Inky
from sprites.ghosts.clyde import Clyde

class Game:

    def __init__(self, screen=None, init = True):
        if (init):
            self.level = 1
            self.screen = screen
            self.state = PLAYING
            self.score = 0
            self.lives = 3
            self.movement_count = 0
            
            self.home_walls = []
            self.walls = []
            self.access = []
            self.dots = []
            
            # Initialize game map only if we have a screen
            if screen is not None:
                self.map_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                self.load_map()
            
            # Create Pacman
            self.pacman = Pacman(13.5 * TILE_SIZE, 20*TILE_SIZE, None if screen is None else screen)
            
            # Create and initialize ghosts
            self.ghosts = []
            self.blinky = Blinky(12* TILE_SIZE, 16.5 * TILE_SIZE)
            self.pinky = Pinky(13.5 * TILE_SIZE, 16.5 * TILE_SIZE)
            self.inky = Inky(15 * TILE_SIZE, 16.5 * TILE_SIZE)
            self.clyde = Clyde(13.5 * TILE_SIZE, 16.5 * TILE_SIZE)
            
            # Initialize the game
            self.set_walls()
            self.set_access()
            self.reset_game()
            self.update_level()
    
    def clone(self) -> 'Game':
        new_game = Game(init=False)
        new_game.level = self.level
        new_game.state = self.state
        new_game.score = self.score
        new_game.movement_count = self.movement_count
        new_game.lives = self.lives
        new_game.dots = self.dots.copy()
        new_game.pacman = self.pacman.clone()

        new_game.blinky = self.blinky.clone()
        new_game.pinky = self.pinky.clone()
        new_game.inky = self.inky.clone()
        new_game.clyde = self.clyde.clone()

        #new_game.home_walls = [wall for wall in self.home_walls]
        #new_game.walls = [wall for wall in self.walls]
        new_game.access = self.access
        new_game.ghosts = [ghost.clone() for ghost in self.ghosts]
        return new_game


    def update_level(self):
        # Reset ghosts list
        self.ghosts = []
        
        # Add ghosts based on level
        if self.level >= 2:
            self.ghosts.append(self.blinky)
        if self.level >= 3:
            self.ghosts.append(self.pinky)
        if self.level >= 4:
            self.ghosts.append(self.inky)
        if self.level >= 5:
            self.ghosts.append(self.clyde)
            
        self.reset_game()
        self.set_dots()
    
    def load_map(self):
        # Only load map image if we're not in training mode
        if self.screen is not None:
            map_image = pygame.image.load(MAP_SPRITE).convert()
            self.map_surface = pygame.transform.scale(map_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
   
    def set_access(self):
        self.access = []
        for x in range(0, GRID_WIDTH*TILE_SIZE + 2*TILE_SIZE):
            self.access.append([True for _ in range(0, GRID_HEIGHT*TILE_SIZE + 2*TILE_SIZE)])
        
        for wall in self.walls:
            for x in range(wall.rect.x, wall.rect.x + wall.rect.width):
                for y in range(wall.rect.y, wall.rect.y + wall.rect.height):
                    self.access[TILE_SIZE + x][TILE_SIZE + y] = False
    
    def get_access(self, x, y):
        if (x > GRID_WIDTH*TILE_SIZE or y > GRID_HEIGHT*TILE_SIZE or x < 0 or y < 0):
            return False
        x += TILE_SIZE
        y += TILE_SIZE
        return self.access[x][y] and self.access[x+TILE_SIZE-1][y] and self.access[x][y+TILE_SIZE-1] and self.access[x+TILE_SIZE-1][y+TILE_SIZE-1]

    def add_home_walls(self):
        if hasattr(self, 'walls'):
            for y in range(14, 16):
                for x in range(13, 15):
                    wall = Wall(x*TILE_SIZE, y*TILE_SIZE)
                    self.home_walls.append(wall)
                    self.walls.append(wall)
            self.set_access()
    
    def remove_home_walls(self):
        if hasattr(self, 'walls'):
            for wall in self.home_walls:
                self.walls.remove(wall)
            self.home_walls = []
            self.set_access()

    def set_walls(self):
        """Create the walls of the map"""
        # Create wall sprites for the boundaries
        
        # Top and bottom walls
        for x in range(0, GRID_WIDTH*TILE_SIZE, TILE_SIZE):
            self.walls.append(Wall(x, 0))
            self.walls.append(Wall(x, (GRID_HEIGHT - 1)*TILE_SIZE))
        
        # Left and right walls
        for y in range(0, GRID_HEIGHT*TILE_SIZE, TILE_SIZE):
            if y < 16 * TILE_SIZE or y >= 17*TILE_SIZE:
                self.walls.append(Wall(0, y))
                self.walls.append(Wall((GRID_WIDTH - 1)*TILE_SIZE, y))

        # Square 1
        for x in range(2, 6):
            for y in range(2, 6):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        
        # Square 2
        for x in range(22, 26):
            for y in range(2, 6):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Square 3
        for x in range(1, 3):
            for y in range(28, 30):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Square 4
        for x in range(25, 27):
            for y in range(28, 30):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Rectangle 1
        for x in range(7, 12):
            for y in range(2, 6):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        
        # Rectangle 2
        for x in range(16, 21):
            for y in range(2, 6):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        
        # Rectangle 3
        for x in range(13, 15):
            for y in range(1, 6):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        
        # Rectangle 4
        for x in range(2, 6):
            for y in range(7, 9):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Rectangle 5
        for x in range(22, 26):
            for y in range(7, 9):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        
        # Rectangle 6
        for x in range(1, 6):
            for y in range(10, 16):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        
        # Rectangle 7
        for x in range(22, 27):
            for y in range(10, 16):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Rectangle 8
        for x in range(1, 6):
            for y in range(17, 23):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Rectangle 9
        for x in range(22, 27):
            for y in range(17, 23):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Rectangle 10
        for x in range(7, 9):
            for y in range(17, 23):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        
        # Rectangle 11
        for x in range(19, 21):
            for y in range(17, 23):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Rectangle 12
        for x in range(7, 12):
            for y in range(24, 27):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        
        # Rectangle 13
        for x in range(16, 21):
            for y in range(24, 27):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Shape 1
        for x in range(7, 9):
            for y in range(7, 16):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        for x in range(9, 12):
            for y in range(10, 13):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Shape 2
        for x in range(19, 21):
            for y in range(7, 16):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        for x in range(16, 19):
            for y in range(10, 13):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        
        # Shape 3
        for x in range(10, 18):
            for y in range(7, 9):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        for x in range(13, 15):
            for y in range(9, 13):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Shape 4
        for x in range(10, 18):
            for y in range(21, 23):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        for x in range(13, 15):
            for y in range(23, 27):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Shape 5
        for x in range(2, 6):
            for y in range(24, 27):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        for x in range(4, 6):
            for y in range(27, 30):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        
        # Shape 6
        for x in range(22, 26):
            for y in range(24, 27):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        for x in range(22, 24):
            for y in range(27, 30):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Shape 7
        for x in range(2, 12):
            for y in range(31, 34):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        for x in range(7, 9):
            for y in range(28, 31):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Shape 8
        for x in range(16, 26):
            for y in range(31, 34):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        for x in range(19, 21):
            for y in range(28, 31):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Shape 9
        for x in range(10, 18):
            for y in range(28, 30):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        for x in range(13, 15):
            for y in range(30, 34):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Home
        for y in range(14, 16):
            for x in range(11, 13):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
            for x in range(15, 17):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        for y in range(18, 20):
            for x in range(11, 17):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        for y in range(14, 20):
            self.walls.append(Wall(10*TILE_SIZE, y*TILE_SIZE))
            self.walls.append(Wall(17*TILE_SIZE, y*TILE_SIZE))
        
    def set_dots(self):
        for x in range(0, GRID_WIDTH):
            for y in range(0, GRID_HEIGHT):
                if self.get_access(x*TILE_SIZE, y*TILE_SIZE):
                    if not ((x >= 11 and x <= 16) and (y >= 14 and y <= 17)):
                        self.dots.append(Dot(x*TILE_SIZE, y*TILE_SIZE))
                
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == PLAYING:
                if event.key == pygame.K_UP:
                    self.pacman.set_direction(UP)
                elif event.key == pygame.K_DOWN:
                    self.pacman.set_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.pacman.set_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.pacman.set_direction(RIGHT)
                elif event.key == pygame.K_p:
                    self.state = PAUSED
            elif self.state == PAUSED and event.key == pygame.K_p:
                self.state = PLAYING

    def update(self, update_pacman=True, update_ghosts=True):
        if self.state != PLAYING and self.state != TRAINING:
            return
        
        if hasattr(self, 'ai'):
            self.ai.update()
            
        # Update Pacman
        if update_pacman: self.pacman.update(self)
        
        # Update ghosts
        if update_ghosts:
            if self.movement_count <= GHOST_FIRST_TARGET_MOVEMENT:
                self.inky.set_target(GHOST_FIRST_TARGET_TILE[0], GHOST_FIRST_TARGET_TILE[1], update=True, game=self)
                self.pinky.set_target(GHOST_FIRST_TARGET_TILE[0], GHOST_FIRST_TARGET_TILE[1], update=True, game=self)
                self.blinky.set_target(GHOST_FIRST_TARGET_TILE[0], GHOST_FIRST_TARGET_TILE[1], update=True, game=self)
                self.clyde.set_target(GHOST_FIRST_TARGET_TILE[0], GHOST_FIRST_TARGET_TILE[1], update=True, game=self)
                if self.movement_count == GHOST_FIRST_TARGET_MOVEMENT:
                    self.add_home_walls()
            else:
                self.inky.update(self)
                self.pinky.update(self)
                self.blinky.update(self)
                self.clyde.update(self)
        
        # Check for collisions and dots
        self.check_collisions()
        self.check_dots()
        
        self.movement_count += 1
    
    def check_collisions(self):
        # Check ghost collisions
        for ghost in self.ghosts:
            if self.pacman.rect.colliderect(ghost.rect):
                if ghost.state == 'frightened':
                    ghost.set_eaten()
                    self.score += 200
                elif ghost.state == 'normal':
                    self.lives -= 1
                    if self.lives <= 0:
                        self.state = GAME_OVER
                    else:
                        self.reset_game()

    def check_dots(self):
        if len(self.dots) == 0:
            self.level += 1
            self.update_level()
        if self.level == 30:
            self.state = GAME_WON

        # Check dots collisions
        for dot in self.dots:
            if self.pacman.rect.colliderect(dot.rect):
                self.score += 1
                self.dots.remove(dot)
    
    def reset_game(self):
        """Reset positions of Pacman and ghosts after losing a life"""
        self.pacman.rect.x = 13.5 * TILE_SIZE
        self.pacman.rect.y = 20 * TILE_SIZE
        self.pacman.direction = LEFT
        
        # Reset ghost positions
        self.blinky.rect.x, self.blinky.rect.y = 12 * TILE_SIZE, 17 * TILE_SIZE
        self.pinky.rect.x, self.pinky.rect.y = 13.5 * TILE_SIZE, 17* TILE_SIZE
        self.inky.rect.x, self.inky.rect.y = 15 * TILE_SIZE, 17 * TILE_SIZE
        self.clyde.rect.x, self.clyde.rect.y = 13.5 * TILE_SIZE, 16 * TILE_SIZE

        self.remove_home_walls()
        self.movement_count = 0
    
    def draw(self):
        if self.screen is None or self.state == TRAINING:
            return
            
        # Draw map
        self.screen.blit(self.map_surface, (0, 0))
        
        # Draw dots
        tmp = pygame.Surface((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE), pygame.SRCALPHA)
        for dot in self.dots:
            tmp.blit(dot.image, dot.rect)
        dot_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        pygame.transform.scale(tmp, (WINDOW_WIDTH, WINDOW_HEIGHT), dot_surface)
        self.screen.blit(dot_surface, (0, 0))

        # Draw walls
        #tmp = pygame.Surface((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE), pygame.SRCALPHA)
        #for wall in self.walls:
        #    tmp.blit(wall.image, wall.rect)
        #wall_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        #pygame.transform.scale(tmp, (WINDOW_WIDTH, WINDOW_HEIGHT), wall_surface)
        #self.screen.blit(wall_surface, (0, 0))

        # Draw access
        #tmp = pygame.Surface((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE), pygame.SRCALPHA)
        #for x in range(GRID_WIDTH*TILE_SIZE):
        #    for y in range(GRID_HEIGHT*TILE_SIZE):
        #        if self.get_access(x, y):
        #            #print("draw access", x, y)
        #            pygame.draw.rect(tmp, WHITE, (x, y, 1, 1))
        #access_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        #pygame.transform.scale(tmp, (WINDOW_WIDTH, WINDOW_HEIGHT), access_surface)
        #self.screen.blit(access_surface, (0, 0))

        # Draw all sprites
        tmp = pygame.Surface((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE), pygame.SRCALPHA)
        tmp.blit(self.pacman.image, self.pacman.rect)
        for ghost in self.ghosts:
            tmp.blit(ghost.image, ghost.rect)
        sprites_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        pygame.transform.scale(tmp, (WINDOW_WIDTH, WINDOW_HEIGHT), sprites_surface)
        self.screen.blit(sprites_surface, (0, 0))
        
        # Draw score and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        lives_text = font.render(f'Lives: {self.lives}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
        
        # Draw game state messages
        if self.state == GAME_OVER:
            game_over_text = font.render('GAME OVER', True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
        elif self.state == GAME_WON:
            game_won_text = font.render('GAME WON', True, GREEN)
            text_rect = game_won_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_won_text, text_rect)
