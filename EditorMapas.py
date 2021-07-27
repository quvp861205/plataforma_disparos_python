import pygame
import button
import csv
import pickle


pygame.init()

#para relentizar el juego
clock = pygame.time.Clock()
FPS = 60

#TAMAÑOS DE LA PANTALLA
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300


# CONFIGURAMOS LA PANTALLA
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

# DEFINIMOS VARIABLES
ROWS = 16 # REGISTROS CUADRICULA
MAX_COLS = 150 # MAXIMO DE COLUMNAS
TILE_SIZE = SCREEN_HEIGHT // ROWS # TAMAÑO DE CADA CUADRITO
TILE_TYPES = 21 # NUMERO DE SPRITES
level = 1 # LEVEL ACTUAL
current_tile = 0 # UBICACION ACTUAL EN EL MAPA
scroll_left = False # SCROLL IZQUIERDA
scroll_right = False # SCROLL DERECHA
scroll = 0
scroll_speed = 1 # VELOCIDAD DEL SCROLL

# CARGAMOS EL FONDO
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()


# CARGAMOS LOS PRITES PARA el MAPA
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)



# DEFINIMOS LOS COLORES QUE VAMOS A USAR
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# DEFINIMOS LA FUENTE
font = pygame.font.SysFont('Futura', 30)

# CREAMOS UNA MATRIZ CON PUROS -1
world_data = []
for row in range(ROWS):
	r = [-1] * MAX_COLS
	world_data.append(r)

# CREAMOS EL SUELO
for tile in range(0, MAX_COLS):
	world_data[ROWS - 1][tile] = 0

# PINTAMOS EL FONDO
def draw_bg():
	screen.fill(GREEN)
	width = sky_img.get_width()
	for x in range(4):
		screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
		screen.blit(mountain_img, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
		screen.blit(pine1_img, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
		screen.blit(pine2_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))


# PINTAMOS LA GRILLA O MAPA PARA EDITAR
def draw_grid():
	# LINEAS VERTICALES CONSIDERANDO EL SCROLL
	for c in range(MAX_COLS + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
	# LINEAS HORIZONTALES
	for c in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

# PINTA LOS SPRITES DEL MAPA EN LA GRILLA CONSIDERANDO EL SCROLL
def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


# CREAMOS LOS BOTONES DE SPRITES PARA EDITAR LE MAPA
# CARGAMOS LAS IMAGENES DE GRABAR Y CARGAR
save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img = pygame.image.load('img/load_btn.png').convert_alpha()
# BOTONES PARA GRABAR Y CARGAR MAPAS EN LA PARTE DE ABAJO DE LA PANTALLA
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)

button_list = [] # LISTA DE BOTONES SPRITES
button_col = 0 # CONTADOR DE COLUMNAS DE LOS BOTONES
button_row = 0 # CONTADOR DE FILAS DE LOS BOTONES

# RECOREMOS LA LISTA DE SPRITES QUE CARGAMOS ANTERIORMENTE
for i in range(len(img_list)):
    # CREAMOS UN BOTON CON LA CLASE BUTTON DANDO UBICACION Y LA IMAGEN
	tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
	button_list.append(tile_button) # LO AGREGAMOS A LA LISTA
	button_col += 1
	if button_col == 3: # LIMITAMOS A 3 BOTONES POR FILA
		button_row += 1
		button_col = 0


#Ciclo del juego y validacion de todos los eventos
run = True
while run:

    clock.tick(FPS) # RELENTIZA EL JUEGO A 60 FOTOGRAMAS POR SEGUNDO

    # OBTENEMOS LA POSICION DEL MOUSE
    pos_mouse = pygame.mouse.get_pos()

    draw_bg() # PINTA EL FONDO
    draw_grid() # PINTA LA GRILLA DEL MAPA
    draw_world() # PINTA LOS SPRITES DEL MAPA

    nivel_actual = font.render('Nivel actual: '+str(level) , True , WHITE)
    screen.blit(nivel_actual , (SCREEN_WIDTH+SIDE_MARGIN - 160, SCREEN_HEIGHT+LOWER_MARGIN - 30))

    # BOTON GRABAR
    if save_button.draw(screen, pos_mouse):
        
        # GRABAMOS EL NIVEL ACTUAL
        with open(f'levels/level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)

    # BOTON CARGAR NIVEL ACTUAL
    if load_button.draw(screen, pos_mouse):
         
        scroll = 0 # RESETEAMOS EL SCROLL

        # CARGAMOS EL MAPA EN EL NIVEL ACTUAL DESDE EL ARCHIVO
        with open(f'levels/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    # PINTAMOS EL FONDO DEL PANEL DONDE VAN A ESTAR LOS SPRITES SELECCIONABLES
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    

    # PINTAMOS LOS SPRITES EDITORES DE MAPA
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen, pos_mouse):
            current_tile = button_count

    # RESALTAMOS EL BOTON CLICKEADO
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # CONTROLAMOS EL SCROLL DEL MAPA
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    # AGREGAMOS NUEVOS SPRITES AL MAPA	
    #pos = pygame.mouse.get_pos() # OBTENEMOS POSICION DEL MOUSE
    pos = pos_mouse
    # OBTENEMOS LA POSICION EN X Y DEL MAPA CONSIDERANDO EL SCROLL
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE    

    # VALIDAMOS SI LAS COORDENADAS DEL MOUSE ESTAN DENTRO DE UN SPRITE EN EL MAPA
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
                
        if pygame.mouse.get_pressed()[0] == 1: # SI MOUSE HIZO CLICK
            if world_data[y][x] != current_tile: # SI SPRITES ES DIFERENTE ANTERIOR EN EL MAPA
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1: # SI MOUSE HIZO CLICK DERECHO ELIMINAMOS
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        # EVENTOS DEL TECLADO
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()