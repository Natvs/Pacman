import pygame
from utils.constants import *
from sprites.wall import Wall
from sprites.pacman import Pacman
from sprites.ghosts.blinky import Blinky
from sprites.ghosts.pinky import Pinky
from sprites.ghosts.inky import Inky
from sprites.ghosts.clyde import Clyde

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.state = PLAYING
        self.score = 0
        self.lives = 3
        
        self.walls = []
        
        # Initialize game map
        self.map_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.load_map()
        
        # Create Pacman
        self.pacman = Pacman(0.5*GRID_WIDTH * TILE_SIZE, 0.55 * GRID_HEIGHT * TILE_SIZE)
        
        # Create ghosts
        self.blinky = Blinky(0.5*GRID_WIDTH * TILE_SIZE, 0.45*GRID_WIDTH * TILE_SIZE)
        self.pinky = Pinky(0.5*GRID_WIDTH * TILE_SIZE, 0.5*GRID_WIDTH * TILE_SIZE)
        self.inky = Inky(0.4*GRID_WIDTH * TILE_SIZE, 0.5*GRID_WIDTH * TILE_SIZE)
        self.clyde = Clyde(0.6*GRID_WIDTH * TILE_SIZE, 0.5*GRID_WIDTH * TILE_SIZE)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
    
    def load_map(self):
        # Load and scale the map image
        map_image = pygame.image.load(MAP_SPRITE).convert()
        self.map_surface = pygame.transform.scale(map_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # TODO: Create wall collision boxes based on the map image
        # This would involve analyzing the map image to create wall sprites
        # For now, we'll just add boundary walls
        self.create_boundary_walls()
    
    def create_boundary_walls(self):
        """Create the boundary walls of the map"""
        # Create wall sprites for the boundaries
        
        # Top and bottom walls
        for x in range(0, GRID_WIDTH*TILE_SIZE, TILE_SIZE):
            self.walls.append(Wall(x, 0))
            self.walls.append(Wall(x, (GRID_HEIGHT - 1)*TILE_SIZE))
        
        # Left and right walls
        for y in range(0, GRID_HEIGHT*TILE_SIZE, TILE_SIZE):
            self.walls.append(Wall(0, y))
            self.walls.append(Wall((GRID_WIDTH - 1)*TILE_SIZE, y))
        
    
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
            
        # Update Pacman
        self.pacman.update(self.walls)
        
        # Update ghosts
        self.inky.update(self.walls, self.pacman, self.blinky)
        self.pinky.update(self.walls, self.pacman)
        self.blinky.update(self.walls, self.pacman)
        self.clyde.update(self.walls, self.pacman)
        
        # Check for collisions
        self.check_collisions()
    
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
    
    def reset_positions(self):
        """Reset positions of Pacman and ghosts after losing a life"""
        self.pacman.rect.x = 14 * TILE_SIZE
        self.pacman.rect.y = 23 * TILE_SIZE
        self.pacman.direction = LEFT
        
        # Reset ghost positions
        self.blinky.rect.x, self.blinky.rect.y = 14 * TILE_SIZE, 11 * TILE_SIZE
        self.pinky.rect.x, self.pinky.rect.y = 14 * TILE_SIZE, 14 * TILE_SIZE
        self.inky.rect.x, self.inky.rect.y = 12 * TILE_SIZE, 14 * TILE_SIZE
        self.clyde.rect.x, self.clyde.rect.y = 16 * TILE_SIZE, 14 * TILE_SIZE
    
    def draw(self):
        # Draw map
        self.screen.blit(self.map_surface, (0, 0))
        
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
            game_over_text = font.render('GAME OVER', True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
