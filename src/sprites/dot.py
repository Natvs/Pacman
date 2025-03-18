import pygame
from utils.constants import *

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y, is_power_pellet=False):
        super().__init__()
        self.is_power_pellet = is_power_pellet
        
        # Create the dot surface
        size = TILE_SIZE // 2 if not is_power_pellet else TILE_SIZE
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw the dot
        dot_color = WHITE
        dot_radius = size // 2
        pygame.draw.circle(
            self.image,
            dot_color,
            (dot_radius, dot_radius),
            dot_radius
        )
        
        # Set up the rect
        self.rect = self.image.get_rect()
        self.rect.centerx = x + TILE_SIZE // 2
        self.rect.centery = y + TILE_SIZE // 2
