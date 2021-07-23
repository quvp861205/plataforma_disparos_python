from pygame.locals import *
from pygame.rect import *
from pygame.sprite import *
from pygame.font import *
import random as rand 
import os

# Tamaño de la pantalla del juego
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH*0.8)

GRAVITY = 0.75
TILE_SIZE = 40

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255,0,0)

pygame.font.init()
font = pygame.font.SysFont('Futura', 30, bold=False, italic=False)