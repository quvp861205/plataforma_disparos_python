from pygame.locals import *
from pygame.rect import *
from pygame.sprite import *
from pygame.font import *
from pygame.mixer import *
import random as rand 
import csv
import os


# Tamaño de la pantalla del juego
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH*0.8)

GRAVITY = 0.75

BG = (144, 201, 120)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255,0,0)
PINK = (235, 65, 54)

COLS = 150 # numero de columnas que divide la pantalla
ROWS = 16 # numero de registros que divide la pantalla
TILE_SIZE = SCREEN_HEIGHT // ROWS # tamaño de cada regilla

TILE_TYPES = 22


pygame.font.init()
font = pygame.font.SysFont('Futura', 30, bold=False, italic=False)