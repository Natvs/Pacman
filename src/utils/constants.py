# Window dimensions (28x36 tiles of 8x8 pixels)
TILE_SIZE = 6
GRID_WIDTH = 28
GRID_HEIGHT = 36
WINDOW_WIDTH = GRID_WIDTH * TILE_SIZE * 2.5
WINDOW_HEIGHT = GRID_HEIGHT * TILE_SIZE * 2.5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 150, 0)

# Game settings
FPS = 30
PACMAN_SPEED = 3
GHOST_SPEED = 2
GHOST_FIRST_TARGET_MOVEMENT = 100
GHOST_FIRST_TARGET_TILE = (14, 10)
TELEPORT_POS_Y = 16

PACMAN_DEFAULT_POS = (13 * TILE_SIZE, 20 * TILE_SIZE)
BLINKY_DEFAULT_POS = (12 * TILE_SIZE, 17*TILE_SIZE)
PINKY_DEFAULT_POS = (13 * TILE_SIZE, 17*TILE_SIZE)
INKY_DEFAULT_POS = (15 * TILE_SIZE, 17*TILE_SIZE)
CLYDE_DEFAULT_POS = (14 * TILE_SIZE, 16*TILE_SIZE)

# Look-ahead
PACMAN_IA_ITERATIONS = 5000
PACMAN_IA_DEPTH = 5
PACMAN_IA_MEMORY = 5
PACMAN_IA_LOOKAHEAD = 4
PACMAN_IA_BACKCOUNTDOWN = 3
PACMAN_IA_AVOID_AREA = 3 * TILE_SIZE

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game states
TRAINING = 'training'
PLAYING = 'playing'
PAUSED = 'paused'
GAME_OVER = 'game_over'
GAME_WON = "game_won"

# Ghost settings
FRIGHTENED_DURATION = 400  # Number of frames (about 6-7 seconds at 60 FPS)

# Sprite paths
PACMAN_SPRITE = 'resources/images/pacman.png'
BLINKY_SPRITE = 'resources/images/Blinky.png'
PINKY_SPRITE = 'resources/images/Pinky.png'
INKY_SPRITE = 'resources/images/Inky.png'
CLYDE_SPRITE = 'resources/images/Clyde.png'
MAP_SPRITE = 'resources/images/map.png'
