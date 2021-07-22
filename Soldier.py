"""
Clase para representar al jugador
"""

from Library import *

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True #esta vivo
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

        self.animation_types = ["Idle", "Run", "Jump"] #tipos de animaciones

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

        #liberando teclado
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_a:
                self.moving_left = False
            if event.key==pygame.K_d:
                self.moving_right = False
            if event.key==pygame.K_w:
                self.jump = False

    def draw(self, screen):
        self.update_animation() #actualizamos la animacion
        self.move() #movemos a las nuevas coordenadas
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) #pinta al monito en la pantalla