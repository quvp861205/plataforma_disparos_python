from Library import *
from Soldier import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, group_enemy):
        pygame.sprite.Sprite.__init__(self)

        self.grenade_img = pygame.image.load(f'img/icons/bullet.png')

        self.speed = 10
        self.damage = 15
        self.image = self.grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        self.explosion = False
        self.group_enemy = group_enemy


    def update(self):
        #colision de soldado y bala

        if str(type(self.group_enemy))=="<class 'Soldier.Soldier'>":
            player = self.group_enemy
            self.group_enemy = pygame.sprite.Group()
            self.group_enemy.add(player)

        for enemy in self.group_enemy:            
            if pygame.sprite.collide_rect(enemy, self):
                
                if enemy.health>0:
                    health =  enemy.health

                    #descontamos sangre al enemigo
                    enemy.health -= self.damage
                    print('enemigo herido con bala, health['+str(health)+' -> '+str(enemy.health)+']')

                    #descontamos potencia a la bala
                    if self.damage>health:
                        self.damage -= health 
                    else: 
                        self.damage = 0
                    
                    if self.damage<=0:
                        self.explosion = True
                                            

        if self.explosion==False:
            self.rect.x += (self.direction * self.speed)

            if self.rect.right<0 or self.rect.left>SCREEN_WIDTH:
                self.kill()  
        else:
            self.kill()
