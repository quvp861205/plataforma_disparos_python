from Library import *
from Explosion import *

class Grenade(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, direction, player, group_enemy):
        pygame.sprite.Sprite.__init__(self)

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
        self.group_enemy = group_enemy
        self.player = player
        self.yaExploto = False
        self.screen = screen


    def update(self):
        self.vel_y += self.gravity
        dx = self.direction * self.speed
        dy = self.vel_y

        # generamos el movimiento parabolo de una granada
        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom
            self.speed = 0.3 * self.direction                   

        self.rect.x += dx
        self.rect.y += dy

        # rebotamos en la pared
        if self.rect.left+dx<0 or self.rect.left+dx>SCREEN_WIDTH:
            self.direction *= -1

        # descontamos el temporizador de explosion
        self.timer -= 1

        # si temporizador agoto el tiempo
        if self.timer <= 0:
            # eliminamos el sprite de granada
            self.kill()

            # y creamos el sprite de explosion
            explosion = Explosion(self.screen, self.rect.x, self.rect.y, 0.5)
            explosion.update()            
            
            if self.yaExploto==False:
                if self.group_enemy!=None:
                    for enemy in self.group_enemy:
                        if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                            abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                            health = enemy.health
                            enemy.health -= self.damage
                            if self.damage>health:
                                self.damage -= health
                            else:
                                self.damage = 0

                            print('enemigo herido con granada, health['+str(health)+' -> '+str(enemy.health)+']')

                
                if abs(self.rect.centerx - self.player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - self.player.rect.centery) < TILE_SIZE * 2:
                    health = self.player.health
                    self.player.health -= self.damage
                    if self.damage>health:
                        self.damage -= health
                    else:
                        self.damage = 0

                        print('jugador herido con granada, health['+str(health)+' -> '+str(self.player.health)+']')

            self.yaExploto = True            
            

