from Library import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, escenario, x, y, scale):
        pygame.sprite.Sprite.__init__(self)

        self.escenario = escenario

        self.images = []

        #cargamos imagenes
        for num in range(1, 6):
            img = pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0

        #asignamos el primer fotograma
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        self.screen = self.escenario.screen


    def update(self):
        EXPLOSION_SPEED = 1000000
		#contador de tiempo
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            #if the animation is complete then delete the explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]
        
        self.rect.x += self.escenario.screen_scroll

        self.screen.blit(self.image, self.rect)

