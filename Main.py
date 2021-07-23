from Library import *
from Soldier import *
from Enemy import *
from ItemBox import *
from HealthBar import *

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

#jugador
player = Soldier("player", x, y, scale, 5, 10, 5)

#grupo de enemigos
group_enemy = pygame.sprite.Group()
group_enemy.add(Enemy("enemy", 400, y, scale, 5, 100))
group_enemy.add(Enemy("enemy", 420, y, scale, 5, 100))

#Items para aumentar ammo, health and grenades
item_box_group = pygame.sprite.Group()
item_box = ItemBox(player, 'Health', 100, 260)
item_box_group.add(item_box)
item_box = ItemBox(player, 'Ammo', 400, 260)
item_box_group.add(item_box)
item_box = ItemBox(player, 'Grenade', 500, 260)
item_box_group.add(item_box)


#barras de puntuaciones
health_bar = HealthBar(screen, 10, 10, player)


#Ciclo del juego y validacion de todos los eventos
run = True
while run:

    clock.tick(FPS) #relentizamos el juego a 60 frames por second

    draw_background() #pintamos el fondo

    player.update(screen, group_enemy) #refrescamos en pantalla al jugador     
    group_enemy.update(screen)
    item_box_group.update()
    item_box_group.draw(screen)
    health_bar.draw()
 
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