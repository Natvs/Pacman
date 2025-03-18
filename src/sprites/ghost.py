import pygame
from utils.constants import *
import math

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path):
        super().__init__()
        self.sprite_path = sprite_path
        self.load_sprites()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = LEFT
        self.speed = GHOST_SPEED
        self.state = 'normal'  # normal, frightened, eaten
        self.target_tile = None
        
    def load_sprites(self):
        sprite_sheet = pygame.image.load(self.sprite_path).convert_alpha()
        self.image = pygame.transform.scale(sprite_sheet, (TILE_SIZE, TILE_SIZE))
        
    def get_tile_pos(self):
        """Convert pixel position to tile position"""
        return (self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE)
        
    def set_target(self, target_x, target_y):
        """Set the target tile for the ghost to move towards"""
        self.target_tile = (target_x, target_y)
        
    def get_next_direction(self, wall_group):
        """Determine the next direction based on available paths and target"""
        if not self.target_tile:
            return self.direction
            
        possible_directions = []
        for direction in [UP, DOWN, LEFT, RIGHT]:
            if self.can_move(direction, wall_group):
                possible_directions.append(direction)
                
        if not possible_directions:
            return self.direction
            
        # Remove opposite direction unless it's the only option
        opposite = (-self.direction[0], -self.direction[1])
        if len(possible_directions) > 1 and opposite in possible_directions:
            possible_directions.remove(opposite)
            
        # Choose direction that gets closest to target
        current_tile = self.get_tile_pos()
        best_direction = possible_directions[0]
        best_distance = float('inf')
        
        for direction in possible_directions:
            next_tile = (
                current_tile[0] + direction[0],
                current_tile[1] + direction[1]
            )
            distance = math.sqrt(
                (next_tile[0] - self.target_tile[0]) ** 2 +
                (next_tile[1] - self.target_tile[1]) ** 2
            )
            if distance < best_distance:
                best_distance = distance
                best_direction = direction
                
        return best_direction
        
    def update(self, wall_group):
        if self.state == 'normal':
            self.direction = self.get_next_direction(wall_group)
            
        # Update position
        if self.can_move(self.direction, wall_group):
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed
            
    def can_move(self, direction, wall_group):
        """Check if the ghost can move in the given direction"""
        next_rect = self.rect.copy()
        next_rect.x += direction[0] * self.speed
        next_rect.y += direction[1] * self.speed
        
        for wall in wall_group:
            if next_rect.colliderect(wall.rect):
                return False
        return True
        
    def set_frightened(self):
        """Set ghost to frightened state"""
        self.state = 'frightened'
        self.speed = GHOST_SPEED * 0.5
        
    def set_normal(self):
        """Return ghost to normal state"""
        self.state = 'normal'
        self.speed = GHOST_SPEED
        
    def set_eaten(self):
        """Set ghost to eaten state"""
        self.state = 'eaten'
        self.speed = GHOST_SPEED * 2
