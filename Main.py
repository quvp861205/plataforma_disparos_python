from Library import *
from Soldier import *
from Enemy import *
from ItemBox import *
from HealthBar import *
from Escenarios import *

pygame.init()


#Configuramos la pantalla
screen =  pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

#para relentizar el juego
clock = pygame.time.Clock()
FPS = 60

#color de fondo
BG = (144,201,120)
RED = (255,0,0)

def draw_background():
    screen.fill(BG)


escena = Escenarios(screen)
escena.process_data()


#Ciclo del juego y validacion de todos los eventos
run = True
while run:

    clock.tick(FPS) #relentizamos el juego a 60 frames por second

    draw_background() #pintamos el fondo

    escena.draw()

    #Eventos del teclado
    for event in pygame.event.get():        
        if event.type==pygame.QUIT: #salir del juego con la ventana
            run = False       

        #salir del juego con escape    
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                run = False 

        #detectamos eventos teclado del jugador
        escena.player.detection_keyboard(event)
        

    pygame.display.update()

pygame.quit()