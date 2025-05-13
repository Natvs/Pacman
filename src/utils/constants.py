# Windo dimensions (28x36 tiles of 8x8 pixels)
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
FPS = 60
PACMAN_SPEED = 3
GHOST_SPEED = 2
GHOST_FIRST_TARGET_MOVEMENT = 100
GHOST_FIRST_TARGET_TILE = (14, 10)
TELEPORT_POS_Y = 16


# IA
PACMAN_IA_ITERATIONS = 3000
PACMAN_IA_DEPTH = 4  # Reduced depth for faster decisions
PACMAN_IA_MEMORY = 0  # Disabled position memory to allow backtracking
PACMAN_IA_AVOID_AREA = 2 * TILE_SIZE  # Reduced ghost avoidance area

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game states
TRAINING = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
GAME_WON = 4

# Sprite paths
PACMAN_SPRITE = 'resources/images/pacman.png'
BLINKY_SPRITE = 'resources/images/Blinky.png'
PINKY_SPRITE = 'resources/images/Pinky.png'
INKY_SPRITE = 'resources/images/Inky.png'
CLYDE_SPRITE = 'resources/images/Clyde.png'
MAP_SPRITE = 'resources/images/map.png'
