import pygame
from utils.constants import *
# Définition de la classe Pacman
class Pacman2:
    def __init__(self, x, y):
        super().__init__()
        self.load_sprites()
        self.image = self.sprites[LEFT][0]  # Default sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = LEFT
        self.next_direction = LEFT
        self.animation_frame = 0
        self.animation_timer = 0
        self.speed = PACMAN_SPEED
        
    def load_sprites(self):
        sprite_sheet = pygame.image.load(PACMAN_SPRITE).convert_alpha()
        
        # Create base frame
        base_frame = pygame.transform.scale(sprite_sheet, (TILE_SIZE, TILE_SIZE))
        
        # Create animation frames (open and closed mouth)
        self.sprites = {
            LEFT: [
                base_frame,
                pygame.transform.rotate(base_frame, 30),
                pygame.transform.rotate(base_frame, -30)
            ],
            RIGHT: [
                pygame.transform.rotate(base_frame, 180),
                pygame.transform.rotate(base_frame, 150),
                pygame.transform.rotate(base_frame, 210)
            ],
            UP: [
                pygame.transform.rotate(base_frame, 90),
                pygame.transform.rotate(base_frame, 60),
                pygame.transform.rotate(base_frame, 120)
            ],
            DOWN: [
                pygame.transform.rotate(base_frame, 270),
                pygame.transform.rotate(base_frame, 240),
                pygame.transform.rotate(base_frame, 300)
            ]
        }

    def update(self, walls):
        # Update position based on direction if we can move
        if self.can_move(self.direction, walls):
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed
        if self.rect.y >= 17*TILE_SIZE and self.rect.y <= 18*TILE_SIZE:
            if self.rect.x < 0:
                self.rect.x = GRID_WIDTH*TILE_SIZE
            elif self.rect.x > GRID_WIDTH*TILE_SIZE:
                self.rect.x = 0
        
        # Try to change to next_direction if we're not already moving in that direction
        if self.next_direction != self.direction and self.can_move(self.next_direction, walls):
            self.direction = self.next_direction
        
        # Handle animation
        self.animation_timer += 1
        if self.animation_timer >= 6:  # Control animation speed
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 3
            self.image = self.sprites[self.direction][self.animation_frame]
    
    def set_direction(self, direction):
        self.next_direction = direction
        
    def can_move(self, direction, walls):
        # Create a temporary rect for checking the next position
        next_rect = self.rect.copy()
        next_rect.x += direction[0] * self.speed
        next_rect.y += direction[1] * self.speed
        
        # Check collision with walls
        for wall in walls:
            if next_rect.colliderect(wall.rect):
                return False
        return True
    def get_position(self):
        # Retourne la position (x, y) de Pacman
        return self.rect.x, self.rect.y
    def move(self):
        # Met à jour la position de Pacman en fonction de la direction
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]