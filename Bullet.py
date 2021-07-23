from Library import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)

        self.grenade_img = pygame.image.load(f'img/icons/bullet.png')

        self.speed = 10
        self.image = self.grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction


    def update(self):
        self.rect.x += (self.direction * self.speed)

        if self.rect.right<0 or self.rect.left>SCREEN_WIDTH:
            self.kill()  
