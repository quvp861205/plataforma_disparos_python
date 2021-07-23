from Library import *

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
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

        self.direction = direction


    def update(self):
        self.vel_y += self.gravity
        dx = self.direction * self.speed
        dy = self.vel_y

        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom
            self.speed = 0.3 * self.direction
            #self.image = pygame.transform.rotate(self.image, self.angle)
            
            

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.left+dx<0 or self.rect.left+dx>SCREEN_WIDTH:
            self.direction *= -1
