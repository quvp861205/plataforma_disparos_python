"""
Clase para representar al jugador
"""

import pygame
from Library import *
from Bullet import *
from Grenade import *

class Enemy(pygame.sprite.Sprite):
    # Efecto de muerte por fuego se inicializa en __init__
    def burn_by_fire(self, duration=60):
        self.burning = True
        self.burn_time = duration
        self.health = 1  # Deja 1 de vida para muerte lenta
        self.speed = 0
        self.alive = False
        self.update_action(3)
    def __init__(self, escenario, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)

        self.escenario = escenario
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

        #variables para granada
        self.grenade = False
        self.grenade_group = pygame.sprite.Group()        
        self.grenade_cooldown = 50
        self.ammo_grenade = 3
        self.start_ammo_grenade = self.ammo_grenade

        self.animation_types = ["Idle", "Run", "Jump", "Death"] #tipos de animaciones

        #cargamos todas las animaciones
        for animation in self.animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"img/{self.char_type}/{animation}"))

            #cargamos todas las imagenes del soldado moviendose estatico
            for i in range(num_of_frames):
                self.image = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png') #carga la imagen del monito
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*scale), int(self.image.get_height()*scale))) #hace al monito mas grande
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

        # Efecto de muerte por fuego
        self.burning = False
        self.burn_particles = pygame.sprite.Group()
        self.burn_time = 0

        #variables para la inteligencia artificial
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        self.width = self.image.get_width()
        self.height = self.image.get_height()


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
                # Apagar sonido de lanzallamas si está sonando
                if hasattr(self.escenario, 'music') and hasattr(self.escenario.music, 'fuego_fx'):
                    self.escenario.music.fuego_fx.stop()
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

            #checar por colisiones
            for tile in self.escenario.obstacle_list:
                #check collision in the x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    self.direction *= -1 # enemigo topa con pared, hacemos que se gire
                    self.move_counter = 0
                #check for collision in the y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground, i.e. jumping
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    #check if above the ground, i.e. falling
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom

             # colisiones con agua
            if pygame.sprite.spritecollide(self, self.escenario.water_group, False):
                self.health = 0

            # colisiones al vacio
            if self.rect.bottom>SCREEN_HEIGHT:
                self.health = 0


            self.rect.x += dx
            self.rect.y += dy 
    
    #acccion disparar
    def update_shoot(self):    

        #vamos retrociendo el temporizador entre cada bala, es de 20 ciclos
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        #si temporizador paso 20 ciclos y hay balas,entonces agregamos una nueva bala
        if self.shoot and self.shoot_cooldown==0 and self.ammo>0: 
            self.shoot_cooldown = 20 
            
            bullet = Bullet(self.escenario, self.rect.centerx + (0.6*self.rect.size[0]*self.direction), self.rect.centery, self.direction, self)
            self.bullet_group.add(bullet)
            self.ammo -= 1
            self.escenario.music.shoot_fx.play()


        #actualizamos cada bala
        self.bullet_group.update()
        #pintamos cada bala
        self.bullet_group.draw(self.escenario.screen) 

    def update_grenade(self):
        #vamos retrociendo el temporizador entre cada bala, es de 20 ciclos
        if self.grenade_cooldown > 0:
            self.grenade_cooldown -= 1

        #si temporizador paso 20 ciclos y hay balas,entonces agregamos una nueva bala
        if self.grenade and self.grenade_cooldown==0 and self.ammo_grenade>0: 
            self.grenade_cooldown = 100 

           
            grenade = Grenade(self.escenario, self.rect.centerx + (0.5*self.rect.size[0]*self.direction), self.rect.top, self.direction)
            self.grenade_group.add(grenade)
            self.ammo_grenade -= 1
            

        #actualizamos cada granada
        self.grenade_group.update()
        #pintamos cada granada
        self.grenade_group.draw(self.escenario.screen)
    
    def check_alive(self):
        if self.burning:
            if self.burn_time > 0:
                self.burn_time -= 1
                # Generar muchas partículas pequeñas de fuego y humo
                import random
                from Particle import Particle
                for _ in range(10):  # Menos cantidad, pero más variación
                    base = random.random()
                    if base < 0.3:
                        color = (255, random.randint(120,180), 0, random.randint(180, 230))
                        size = random.randint(2, 4)
                    elif base < 0.7:
                        color = (255, random.randint(80,120), 0, random.randint(100, 160))
                        size = random.randint(4, 7)
                    else:
                        color = (255, random.randint(180,220), random.randint(60,100), random.randint(120, 200))
                        size = random.randint(3, 6)
                    dx = random.uniform(-0.7, 0.7)
                    dy = random.uniform(-0.18, -0.65)
                    lifetime = random.randint(22, 38)
                    # Bajar la posición de las partículas (más cerca de la base del enemigo)
                    self.burn_particles.add(Particle(self.rect.centerx + random.randint(-14,14), self.rect.bottom - random.randint(8, 24), color, size, dx, dy, lifetime))
                # Partículas de humo grises que suben lentamente y desaparecen
                for _ in range(7):
                    color = (random.randint(120,180), random.randint(120,180), random.randint(120,180), random.randint(60,120))
                    size = random.randint(6, 14)
                    dx = random.uniform(-1.2, 1.2)
                    dy = random.uniform(-0.4, -1.0)
                    lifetime = random.randint(32, 54)
                    self.burn_particles.add(Particle(self.rect.centerx + random.randint(-18,18), self.rect.centery - random.randint(0, 18), color, size, dx, dy, lifetime))
                for _ in range(5):
                    color = (80, 80, 80, 90)
                    size = random.randint(2, 7)
                    dx = random.uniform(-0.7, 0.7)
                    dy = random.uniform(-0.2, -0.7)
                    lifetime = random.randint(22, 38)
                    self.burn_particles.add(Particle(self.rect.centerx + random.randint(-12,12), self.rect.centery + random.randint(-8,8), color, size, dx, dy, lifetime))
                self.burn_particles.update()
            else:
                self.health = 0
                self.burning = False
        if self.health <= 0 and self.alive==True:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
        if self.TIME_DEATH_COOLDOWN>0 and self.health <= 0:
            self.TIME_DEATH_COOLDOWN-=1

    def ai(self):
        if self.alive:
            
            # poner al enemigo en modo parado aleatoriamente
            if rand.randint(1,10000)>=9970 and self.idling==False:
                self.idling = True
                self.idling_counter = rand.randrange(50, 200)
                self.moving_left = False
                self.moving_right = False
                self.update_action(0)
            
            #validamos si la vision del enemigo alcanza a la del jugador y dispara
            if self.vision.colliderect(self.escenario.player.rect):
                self.idling = True
                self.idling_counter = rand.randrange(20, 40)
                self.moving_left = False
                self.moving_right = False
                self.update_action(0)
                self.shoot = True

            # si el enemigo esta caminando
            if self.idling==False:

                # asignar el movimiento izquierda o derecha dependiendo de la direccion
                if self.direction==1:
                    self.moving_right = True
                else:
                    self.moving_right = False
                self.moving_left = not self.moving_right

                # asignar brinco aleatoriamente
                if rand.randrange(1,100,1)>=99:
                    self.jump = True
                else:
                    self.jump = False

                self.move() #movemos a las nuevas coordenadas
                
                self.jump = False

                # contador para cambiar de direccion al enemigo
                self.move_counter += 1

                # asignamos un rectangulo como la vista del enemigo
                self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                #pygame.draw.rect(screen, RED, self.vision)              

                # cambiar direccion del enemigo
                if self.move_counter > rand.randint(TILE_SIZE, TILE_SIZE*2):
                    self.direction *= -1
                    self.move_counter *= -1

            # si enemigo esta parado nomas
            else:
                
                # conteo del temporizador para que vuelva a caminar
                self.idling_counter -=1

                self.move() # movemos a las nuevas coordenadas
                
                # se cancela el descanso del enemigo
                if self.idling_counter<=0:
                    self.idling = False
            
            # disparo aleatorio
            if abs(self.escenario.player.rect.x - self.rect.x)< 400:
                if rand.randint(1,10000)>=9980:
                    self.shoot = True
            
            # granada aleatoria
            if abs(self.escenario.player.rect.x - self.rect.x)< 100:
                if rand.randint(1,10000)>=9980:
                    self.grenade = True
            
            self.update_shoot() 
            self.update_grenade()
            self.shoot = False
            self.grenade = False
        
        
        # aplicamos el scroll al enemigo
        self.rect.x += self.escenario.screen_scroll
        # Las partículas de quemadura mantienen su posición original para un efecto de fuego más realista


    def update(self):
        if self.TIME_DEATH_COOLDOWN>0:
            self.update_animation()
            self.check_alive()
            self.ai()
            self.escenario.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
            # Dibujar partículas de quemadura
            if self.burning:
                for particle in self.burn_particles:
                    self.escenario.screen.blit(particle.image, particle.rect)
            