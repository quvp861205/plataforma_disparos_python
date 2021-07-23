"""
Clase para representar al jugador
"""

from Library import *
from Bullet import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True #esta vivo
        self.health = 20 #salud actual
        self.max_health = self.health #salud maxima
        self.TIME_DEATH_COOLDOWN = 100 #duracion del enemigo ya muerto antes que dezaparesca

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

        #asignamos el fotograma del indice
        self.image = self.animation_list[self.action][self.frame_index]

        #validamos si ya paso el tiempo para actualizar el fotograma
        if pygame.time.get_ticks() - self.update_time>self.ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks() #volvemos a reiniciar el temporizador
            self.frame_index +=1 #cambiamos al siguiente fotograma

        if self.frame_index>=len(self.animation_list[self.action]): #validar que no se salga de los limites
            if self.alive==False: #si ya no esta vivo, solo se ejecuta 1 vez la animacion
                self.frame_index -= 1
                self.kill()
            else:
                self.frame_index = 0 # vuelve hacer loop la animacion

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #actualizamos a las nuevas coordenadas
    def move(self):
        dx = 0
        dy = 0
        sin_movimiento = False
        
        if  self.alive==True:
            if self.moving_left: #hacia la izquierda
                dx = -self.speed
                self.flip = True
                self.direction = -1       
                self.update_action(1)   #run  
                sin_movimiento = True
                
            if self.moving_right: #hacia la derecha
                dx = self.speed
                self.flip = False
                self.direction = 1
                self.update_action(1)   #run
                sin_movimiento = True

            if self.jump and self.in_air==False:   #brincando
                self.vel_y = -11 
                self.jump = False
                self.update_action(2)   #jump
                sin_movimiento = True    
                self.in_air = True   
            
            if sin_movimiento==False:
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
    
    def check_alive(self):
        if self.health <= 0 and self.alive==True:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)            
        
        if self.TIME_DEATH_COOLDOWN>0 and self.health <= 0:
            self.TIME_DEATH_COOLDOWN-=1

    def update(self, screen):
        if self.TIME_DEATH_COOLDOWN>0: 
            self.update_animation() #actualizamos la animacion del monito
            self.check_alive() #verificamos si estamos vivos          
            self.move() #movemos a las nuevas coordenadas
        
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) #pinta al monito en la pantalla
            