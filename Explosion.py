from Library import *
import pygame
import random
import math
from Particle import Particle

class Explosion(pygame.sprite.Sprite):
    def __init__(self, escenario, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.escenario = escenario
        self.particles = pygame.sprite.Group()
        self.x = x
        self.y = y
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
        self.escenario.music.grenade_fx.play()
        # Efecto de destello blanco
        self.flash_surface = pygame.Surface((int(120*scale), int(120*scale)), pygame.SRCALPHA)
        pygame.draw.circle(self.flash_surface, (255,255,255,120), (self.flash_surface.get_width()//2, self.flash_surface.get_height()//2), int(60*scale))
        self.flash_counter = 0
        # Crear partículas de fuego (más densas y menos dispersas)
        for _ in range(420):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.1, 2.7)  # menor velocidad para menos dispersión
            dx = speed * math.cos(angle) * random.uniform(0.5, 0.85) + random.uniform(-0.3, 0.3)
            dy = speed * math.sin(angle) * random.uniform(0.5, 0.85) + random.uniform(-0.3, 0.3)
            # Mezcla de naranja y amarillo
            if random.random() < 0.5:
                color = (255, random.randint(180,255), 0, 230)  # amarillo intenso
            else:
                color = (255, random.randint(80,160), 0, 230)   # naranja intenso
            size = random.randint(7, 14)
            lifetime = random.randint(45, 80)
            self.particles.add(Particle(x, y, color, size, dx, dy, lifetime, zigzag=True))
        # Crear partículas de humo (más densas y menos dispersas)
        for _ in range(220):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.7, 1.7)
            dx = speed * math.cos(angle) * random.uniform(0.5, 0.85) + random.uniform(-0.2, 0.2)
            dy = speed * math.sin(angle) * random.uniform(0.5, 0.85) + random.uniform(-0.2, 0.2)
            color = (80, 80, 80, 170)  # humo gris más denso
            size = random.randint(10, 20)
            lifetime = random.randint(70, 130)
            self.particles.add(Particle(x, y, color, size, dx, dy, lifetime, zigzag=True))


    def update(self):
        EXPLOSION_SPEED = 4  # velocidad normal de animación
        self.counter += 1
        self.particles.update()
        # Avanzar animación de explosión
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                # Usar un Surface vacío para evitar errores con Group.draw
                self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
            else:
                self.image = self.images[self.frame_index]
        self.rect.x += self.escenario.screen_scroll
        # Solo dibujar la animación si no es Surface vacío
        if self.frame_index < len(self.images):
            self.screen.blit(self.image, self.rect)
        # Dibujar destello blanco solo en los primeros frames
        if self.flash_counter < 7:
            flash_rect = self.flash_surface.get_rect(center=self.rect.center)
            self.screen.blit(self.flash_surface, flash_rect)
            self.flash_counter += 1
        # Dibujar partículas de fuego y humo
        for particle in self.particles:
            self.screen.blit(particle.image, particle.rect)
        # Si ya no hay partículas y la animación terminó, eliminar sprite
        if self.frame_index >= len(self.images) and len(self.particles) == 0:
            self.kill()

