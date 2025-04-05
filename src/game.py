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

    def __init__(self, screen):
        self.level = 1
        self.screen = screen
        self.state = PLAYING
        self.score = 0
        self.lives = 3
        
        self.walls = []
        self.dots = []
        
        # Initialize game map
        self.map_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.load_map()
        
        # Create Pacman
        self.pacman = Pacman(13.5 * TILE_SIZE, 20*TILE_SIZE)
        
        # Create ghosts
        self.blinky = Blinky(12* TILE_SIZE, 16.5 * TILE_SIZE)
        self.pinky = Pinky(13.5 * TILE_SIZE, 16.5 * TILE_SIZE)
        self.inky = Inky(15 * TILE_SIZE, 16.5 * TILE_SIZE)
        self.clyde = Clyde(13.5 * TILE_SIZE, 16.5 * TILE_SIZE)
        self.ghosts = []

        self.set_walls()
        self.reset_positions()
        self.set_dots()
        self.update_level()
    
    def update_level(self):
        if (self.level == 1):
            self.ghosts.append(self.blinky)
        elif (self.level == 5):
            self.ghosts.append(self.pinky)
        elif (self.level == 10):
            self.ghosts.append(self.inky)
        elif (self.level == 15):
            self.ghosts.append(self.clyde)
        self.reset_positions()
        self.set_dots()
    
    def load_map(self):
        # Load and scale the map image
        map_image = pygame.image.load(MAP_SPRITE).convert()
        self.map_surface = pygame.transform.scale(map_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    
    def set_walls(self):
        """Create the walls of the map"""
        # Create wall sprites for the boundaries
        
        # Top and bottom walls
        for x in range(0, GRID_WIDTH*TILE_SIZE, TILE_SIZE):
            self.walls.append(Wall(x, 0))
            self.walls.append(Wall(x, (GRID_HEIGHT - 1)*TILE_SIZE))
        
        # Left and right walls
        for y in range(0, GRID_HEIGHT*TILE_SIZE, TILE_SIZE):
            if y < 17 * TILE_SIZE or y >= 18*TILE_SIZE:
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
            for y in range(10, 17):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))
        
        # Rectangle 7
        for x in range(22, 27):
            for y in range(10, 17):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Rectangle 8
        for x in range(1, 6):
            for y in range(18, 23):
                self.walls.append(Wall(x*TILE_SIZE, y*TILE_SIZE))

        # Rectangle 9
        for x in range(22, 27):
            for y in range(18, 23):
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
                if not self.is_wall(x*TILE_SIZE, y*TILE_SIZE):
                    if not ((x >= 11 and x <= 16) and (y >= 14 and y <= 17)):
                        self.dots.append(Dot(x*TILE_SIZE, y*TILE_SIZE))
                    
    def is_wall(self, x, y):
        for wall in self.walls:
            if (wall.rect.x == x and wall.rect.y == y):
                return True
        return False
            

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
    
    def update(self):
        if self.state != PLAYING:
            return
        
        if hasattr(self, 'ai'):
            self.ai.update()
            
        # Update Pacman
        self.pacman.update(self.walls)
        
        # Update ghosts
        self.inky.update(self.walls, self.pacman, self.blinky)
        self.pinky.update(self.walls, self.pacman)
        self.blinky.update(self.walls, self.pacman)
        self.clyde.update(self.walls, self.pacman)
        
        # Check for collisions and dots
        self.check_collisions()
        self.check_dots()
    
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
                        self.reset_positions()

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
    
    def reset_positions(self):
        """Reset positions of Pacman and ghosts after losing a life"""
        self.pacman.rect.x = 13.5 * TILE_SIZE
        self.pacman.rect.y = 20 * TILE_SIZE
        self.pacman.direction = LEFT
        
        # Reset ghost positions
        self.blinky.rect.x, self.blinky.rect.y = 12 * TILE_SIZE, 17 * TILE_SIZE
        self.pinky.rect.x, self.pinky.rect.y = 13.5 * TILE_SIZE, 17* TILE_SIZE
        self.inky.rect.x, self.inky.rect.y = 15 * TILE_SIZE, 17 * TILE_SIZE
        self.clyde.rect.x, self.clyde.rect.y = 13.5 * TILE_SIZE, 16 * TILE_SIZE
    
    def draw(self):
        # Draw map
        self.screen.blit(self.map_surface, (0, 0))
        
        # Draw walls
        """tmp = pygame.Surface((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE), pygame.SRCALPHA)
        for wall in self.walls:
            pygame.draw.rect(tmp, BLUE, wall.rect)
        walls_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        pygame.transform.scale(tmp, (WINDOW_WIDTH, WINDOW_HEIGHT), walls_surface)
        self.screen.blit(walls_surface, (0, 0))"""

        # Draw dots
        tmp = pygame.Surface((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE), pygame.SRCALPHA)
        for dot in self.dots:
            tmp.blit(dot.image, dot.rect)
        dot_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        pygame.transform.scale(tmp, (WINDOW_WIDTH, WINDOW_HEIGHT), dot_surface)
        self.screen.blit(dot_surface, (0, 0))

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
        
        if self.state == GAME_OVER:
            print("game over")
            game_over_text = font.render('GAME OVER', True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
        elif self.state == GAME_WON:
            print("game won")
            game_won_text = font.render('GAME WON', True, GREEN)
            text_rect = game_won_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_won_text, text_rect)
