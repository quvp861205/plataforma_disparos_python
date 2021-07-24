from Library import *
from Explosion import *

class Grenade(pygame.sprite.Sprite):
    def __init__(self, escenario, x, y, direction):
        pygame.sprite.Sprite.__init__(self)

        self.escenario = escenario
        self.bullet_img = pygame.image.load(f'img/icons/grenade.png')

        self.timer = 100
        self.vel_y = -11
        self.speed = 7

        self.image = self.bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.gravity = 0.75
        self.angle = 2
        self.damage = 35

        self.direction = direction
        self.yaExploto = False
        self.screen = self.escenario.screen

        self.width = self.image.get_width()
        self.height = self.image.get_height()


    def update(self):
        self.vel_y += self.gravity
        dx = self.direction * self.speed
        dy = self.vel_y         

        
        #validamos la colision con el escenario
        for tile in self.escenario.obstacle_list:
            # colision con paredes
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            # colision con el eje vertical y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                # validamos si ya llego a un suelo
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # validamos si sigue cayendo
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom	

        # aplicamos el movimiento validado
        self.rect.x += dx
        self.rect.y += dy

        # descontamos el temporizador de explosion
        self.timer -= 1

        # si temporizador agoto el tiempo
        if self.timer <= 0:
            # eliminamos el sprite de granada
            self.kill()

            # y creamos el sprite de explosion
            explosion = Explosion(self.escenario, self.rect.x, self.rect.y, 0.5)
            explosion.update()            
            
            if self.yaExploto==False:
                if self.escenario.enemy_group!=None:
                    for enemy in self.escenario.enemy_group:
                        if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                            abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                            health = enemy.health
                            enemy.health -= self.damage
                            if self.damage>health:
                                self.damage -= health
                            else:
                                self.damage = 0

                            print('enemigo herido con granada, health['+str(health)+' -> '+str(enemy.health)+']')

                
                if abs(self.rect.centerx - self.escenario.player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - self.escenario.player.rect.centery) < TILE_SIZE * 2:
                    health = self.escenario.player.health
                    self.escenario.player.health -= self.damage
                    if self.damage>health:
                        self.damage -= health
                    else:
                        self.damage = 0

                        print('jugador herido con granada, health['+str(health)+' -> '+str(self.escenario.player.health)+']')

            self.yaExploto = True  

        self.rect.x += self.escenario.screen_scroll          
            

