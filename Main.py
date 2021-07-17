from Library import *
from Soldier import *

pygame.init()

# Tamaño de la pantalla del juego
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH*0.8)

#Configuramos la pantalla
screen =  pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

#para relentizar el juego
clock = pygame.time.Clock()
FPS = 60

#color de fondo
BG = (144,201,120)

def draw_background():
    screen.fill(BG)


x = 200
y = 200
scale = 2
player = Soldier("player", x, y, scale, 5)
enemy = Soldier("enemy", 400, y, scale, 5)

#Ciclo del juego y validacion de todos los eventos
run = True
while run:

    clock.tick(FPS) #relentizamos el juego a 60 frames por second

    draw_background() #pintamos el fondo

    player.draw(screen) #refrescamos en pantalla al jugador   
    enemy.draw(screen) 

    #Eventos del teclado
    for event in pygame.event.get():        
        if event.type==pygame.QUIT: #salir del juego
            run = False

        #presionando teclado
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_a:
                player.moving_left = True
            if event.key==pygame.K_d:
                player.moving_right = True
            if event.key==pygame.K_ESCAPE:
                run = False

        #liberando teclado
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_a:
                player.moving_left = False
            if event.key==pygame.K_d:
                player.moving_right = False

    pygame.display.update()

pygame.quit()