from Library import *
from Soldier import *
from Enemy import *

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


x = 200
y = 200
scale = 2
player = Soldier("player", x, y, scale, 5, 10)
enemy = Enemy("enemy", 400, y, scale, 5, 100)


#Ciclo del juego y validacion de todos los eventos
run = True
while run:

    clock.tick(FPS) #relentizamos el juego a 60 frames por second

    draw_background() #pintamos el fondo

    player.update(screen, enemy) #refrescamos en pantalla al jugador     
    enemy.update(screen)
 
    pygame.draw.line(screen, RED, (0,400),(SCREEN_WIDTH,400))

    #Eventos del teclado
    for event in pygame.event.get():        
        if event.type==pygame.QUIT: #salir del juego con la ventana
            run = False       

        #salir del juego con escape    
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                run = False 

        #detectamos eventos teclado del jugador
        player.detection_keyboard(event)
        

    pygame.display.update()

pygame.quit()