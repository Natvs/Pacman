import pygame
from utils.constants import *

class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites=None):
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

    def update(self, game):
        # Try to change to next_direction if we're not already moving in that direction
        if self.next_direction != self.direction and self.can_move(self.next_direction, game):
            self.direction = self.next_direction

        # Update position based on direction if we can move
        move = self.can_move(self.direction, game)
        if move > 0:
            self.rect.x += self.direction[0] * move
            self.rect.y += self.direction[1] * move

            # When pacman is on a tile to teleport
            if self.rect.y >= TELEPORT_POS_Y*TILE_SIZE and self.rect.y <= (TELEPORT_POS_Y+1)*TILE_SIZE:
                if self.rect.x <= PACMAN_SPEED:
                    self.rect.x = (GRID_WIDTH*TILE_SIZE)-PACMAN_SPEED
                elif self.rect.x >= (GRID_WIDTH*TILE_SIZE)-PACMAN_SPEED:
                    self.rect.x = PACMAN_SPEED
         
        # Handle animation
        self.animation_timer += 1
        if self.animation_timer >= 6:  # Control animation speed
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 3
            self.image = self.sprites[self.direction][self.animation_frame]
    
    def set_direction(self, direction):
        self.next_direction = direction

    def can_move(self, direction, game):
        """Check if pacman can move in the given direction"""
        for i in range(self.speed, 0, -1):
            if game.get_access(self.rect.x + i*direction[0], self.rect.y + i*direction[1]):
                return i
        return 0
    
    def clone(self):
        new_pacman = Pacman(self.rect.x, self.rect.y, self.sprites)
        new_pacman.direction = self.direction
        new_pacman.next_direction = self.next_direction
        new_pacman.animation_frame = self.animation_frame
        new_pacman.animation_timer = self.animation_timer
        new_pacman.speed = self.speed
        return new_pacman
