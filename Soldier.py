"""
Clase para representar al jugador
"""

from Library import *
from Bullet import *
from Grenade import *

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, ammo_grenade):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True #esta vivo
        self.health = 100
        self.max_health = self.health

        self.char_type = char_type #elegir el tipo de soldado imagen

        #variables relacionadas al brinco
        self.jump = False #esta brincando
        self.vel_y = 0 #velocidad de brinco
        self.gravity = 0.75
        self.in_air = True

        self.animation_list = [] #lista de imagenes del soldado
        self.frame_index = 0 #indicador de la animacion actual
        self.image = {} #imagen actual
        self.action = 0 #cual es la accion del jugador
        self.temp_list = [] #asignar animacion de acuerdo a la accion

        #variables para el disparo
        self.bullet_group = pygame.sprite.Group() #grupo para balas
        self.shoot = False
        self.shoot_cooldown = 20
        self.ammo = ammo
        self.start_ammo = self.ammo

        #variables para granada
        self.grenade = False
        self.grenade_group = pygame.sprite.Group()
        self.grenade_cooldown = 50
        self.ammo_grenade = ammo_grenade
        self.start_ammo_grenade = self.ammo_grenade

        self.animation_types = ["Idle", "Run", "Jump", "Death"] #tipos de animaciones

        #cargamos todas las animaciones
        for animation in self.animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"img/{self.char_type}/{animation}"))

            #cargamos todas las imagenes del soldado moviendose estatico
            for i in range(num_of_frames):
                self.image = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png') #carga la imagen del monito
                self.image = pygame.transform.scale(self.image, (self.image.get_width()*scale, self.image.get_height()*scale)) #hace al monito mas grande
                temp_list.append(self.image)
            self.animation_list.append(temp_list)       
     
        #asignamos la animacion por default
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.animation_list[self.action][self.frame_index].get_rect() #obtiene los limites del monito
        self.rect.center = (x,y) #asigna las coordenadas del monito en pantalla
            
        self.update_time = pygame.time.get_ticks() #reloj de animacion
        self.direction = 1 #saber hacia donde se mueve
        self.flip = False #para saber a donde esta viendo el soldado
        self.moving_left = False #moviendose a la izquierda
        self.moving_right = False #moviendose a la derecha
        self.speed = speed #velocidad del movimiento

    #actualizamos la animacion
    def update_animation(self):
        #duracion entre cada fotograma
        self.ANIMATION_COOLDOWN = 100

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time>self.ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index +=1            

        if self.frame_index>=len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #actualizamos a las nuevas coordenadas
    def move(self):
        dx = 0
        dy = 0
        presionando_tecla = False
        
        if self.moving_left and self.alive: #hacia la izquierda
            dx = -self.speed
            self.flip = True
            self.direction = -1       
            self.update_action(1)   #run  
            presionando_tecla = True
            
        if self.moving_right and self.alive: #hacia la derecha
            dx = self.speed
            self.flip = False
            self.direction = 1
            self.update_action(1)   #run
            presionando_tecla = True

        if self.jump and self.in_air==False and self.alive:   #brincando
            self.vel_y = -11 
            self.jump = False
            self.update_action(2)   #jump
            presionando_tecla = True    
            self.in_air = True          
        
        
        if presionando_tecla==False:
            self.update_action(0)   #idle 

        #aplicamos brinco y gravedad
        self.vel_y += self.gravity
        if self.vel_y>10:
            self.vel_y
        dy += self.vel_y

        #verificamos colision
        if self.rect.bottom+dy>400:
            dy = 0
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy
    
    def detection_keyboard(self, event):
       
        #presionando teclado
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_a:
                self.moving_left = True
            if event.key==pygame.K_d:
                self.moving_right = True
            if event.key==pygame.K_w:
                self.jump = True  
            if event.key==pygame.K_SPACE:
                self.shoot = True   
            if event.key==pygame.K_q:
                self.grenade = True            

        #liberando teclado
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_a:
                self.moving_left = False
            if event.key==pygame.K_d:
                self.moving_right = False
            if event.key==pygame.K_w:
                self.jump = False
            if event.key==pygame.K_SPACE:
                self.shoot = False 
            if event.key==pygame.K_q:
                self.grenade = False 

    #acccion disparar
    def update_shoot(self, screen, group_enemy):    

        #vamos retrociendo el temporizador entre cada bala, es de 20 ciclos
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        #si temporizador paso 20 ciclos y hay balas,entonces agregamos una nueva bala
        if self.shoot and self.shoot_cooldown==0 and self.ammo>0: 
            self.shoot_cooldown = 20            
            bullet = Bullet(self.rect.centerx + (0.6*self.rect.size[0]*self.direction), self.rect.centery, self.direction)
            self.bullet_group.add(bullet)
            self.ammo -= 1

        #actualizamos cada bala
        self.bullet_group.update()
        #pintamos cada bala
        self.bullet_group.draw(screen)    

        #colision de soldado y bala
        if pygame.sprite.spritecollide(group_enemy, self.bullet_group, True):
             group_enemy.health -= 20

    def update_grenade(self, screen, group_enemy):
        #vamos retrociendo el temporizador entre cada bala, es de 20 ciclos
        if self.grenade_cooldown > 0:
            self.grenade_cooldown -= 1

        #si temporizador paso 20 ciclos y hay balas,entonces agregamos una nueva bala
        if self.grenade and self.grenade_cooldown==0 and self.ammo_grenade>0: 
            self.grenade_cooldown = 100            
            grenade = Grenade(self.rect.centerx + (0.5*self.rect.size[0]*self.direction), self.rect.top, self.direction)
            self.grenade_group.add(grenade)
            self.ammo_grenade -= 1

        #actualizamos cada bala
        self.grenade_group.update()
        #pintamos cada bala
        self.grenade_group.draw(screen)    

        #colision de soldado y bala
        if pygame.sprite.spritecollide(group_enemy, self.grenade_group, True):
             group_enemy.health -= 50

    
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def update(self, screen, group_enemy):
        self.update_animation() #actualizamos la animacion del monito
        self.check_alive() #verificamos si estamos vivos
        self.update_shoot(screen, group_enemy) #verificamos los disparos
        self.update_grenade(screen, group_enemy) #verificamos las granadas
        
        self.move() #movemos a las nuevas coordenadas
        
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) #pinta al monito en la pantalla