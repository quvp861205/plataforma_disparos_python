from Library import *
from Soldier import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, escenario, x, y, direction, origen):
        pygame.sprite.Sprite.__init__(self)

        self.escenario = escenario
        self.origen = origen # permite saber quien esta disparando para que no se dañe asi mismo

        self.grenade_img = pygame.image.load(f'img/icons/bullet.png')

        self.speed = 10
        self.damage = 15
        self.image = self.grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        self.explosion = False
        self.group_enemy = self.escenario.enemy_group
        self.width = self.image.get_width()
        self.height = self.image.get_height()


    def update(self):

        # validacion de colision bala y jugador
        player = self.escenario.player
        if pygame.sprite.collide_rect(player, self) and player!=self.origen:
                
            if player.health>0:
                health = player.health

                #descontamos sangre al jugador
                player.health -= self.damage
                print(player.char_type+ ' herido con bala, health['+str(health)+' -> '+str(player.health)+']')

                # descontamos potencia a la bala
                if self.damage>health:
                    self.damage -= health 
                else: 
                    self.damage = 0
                
                if self.damage<=0:
                    self.explosion = True

        # validacion de colision bala y enemigo
        if self.explosion==False:
            for enemy in self.group_enemy:            
                if pygame.sprite.collide_rect(enemy, self) and enemy!=self.origen:
                    
                    if enemy.health>0:
                        health = enemy.health

                        #descontamos sangre al enemigo
                        enemy.health -= self.damage
                        print(enemy.char_type+ ' herido con bala, health['+str(health)+' -> '+str(enemy.health)+']')

                        #descontamos potencia a la bala
                        if self.damage>health:
                            self.damage -= health 
                        else: 
                            self.damage = 0
                        
                        if self.damage<=0:
                            self.explosion = True
        
        if self.explosion==False:
            for obstacle in self.escenario.obstacle_list:            
                if obstacle[1].colliderect(self.rect.x,\
                     self.rect.y, self.width, self.height):

                     self.explosion = True
                     self.damage = 0   
                                            

        if self.explosion==False:
            self.rect.x += (self.direction * self.speed) + self.escenario.screen_scroll

            if self.rect.right<0 or self.rect.left>SCREEN_WIDTH:
                self.kill()  
        else:
            self.kill()
