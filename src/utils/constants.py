# Window dimensions (28x36 tiles of 8x8 pixels)
TILE_SIZE = 8
GRID_WIDTH = 28
GRID_HEIGHT = 36
WINDOW_WIDTH = GRID_WIDTH * TILE_SIZE * 2
WINDOW_HEIGHT = GRID_HEIGHT * TILE_SIZE * 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Game settings
FPS = 30
PACMAN_SPEED = 2
GHOST_SPEED = 1

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game states
PLAYING = 'playing'
PAUSED = 'paused'
GAME_OVER = 'game_over'

# Sprite paths
PACMAN_SPRITE = 'resources/images/pacman.png'
BLINKY_SPRITE = 'resources/images/Blinky.png'
PINKY_SPRITE = 'resources/images/Pinky.png'
INKY_SPRITE = 'resources/images/Inky.png'
CLYDE_SPRITE = 'resources/images/Clyde.png'
MAP_SPRITE = 'resources/images/map.png'
