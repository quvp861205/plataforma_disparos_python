"""
Clase para representar al jugador
"""

from Library import *

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)

        self.char_type = char_type

        self.image = pygame.image.load(f'img/{self.char_type}/Idle/0.png') #carga la imagen del monito
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*scale, self.image.get_height()*scale)) #hace al monito mas grande
        self.rect = self.image.get_rect() #obtiene los limites del monito
        self.rect.center = (x,y) #asigna las coordenadas del monito en pantalla

        
        self.direction = 1
        self.flip = False
        self.moving_left = False
        self.moving_right = False
        self.speed = speed

    def move(self):
        dx = 0
        dy = 0

        if self.moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if self.moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):        
        self.move()
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) #pinta al monito en la pantalla