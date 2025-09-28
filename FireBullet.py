import pygame
import random
from Particle import Particle

class FireBullet(pygame.sprite.Sprite):
    def __init__(self, escenario, x, y, direction, speed=12, damage=20):
        super().__init__()
        self.escenario = escenario
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.base_width = 18
        self.base_height = 8
        self.x = x
        self.y = y
        self.image = pygame.Surface((self.base_width, self.base_height), pygame.SRCALPHA)
        self.particles = pygame.sprite.Group()
        # Dibuja una base pequeña, casi invisible (el "origen" del lanzallamas)
        pygame.draw.ellipse(self.image, (255, 120, 0, 80), [0, 0, self.base_width, self.base_height])
        self.rect = self.image.get_rect(center=(x, y))
        self.flame_anim_frame = 0
        self.distance_travelled = 0
        self.max_distance = self.escenario.screen.get_width() // 2  # media pantalla



    def update(self):
        # Calcular distancia recorrida este frame
        prev_x = self.rect.x
        self.rect.x += self.speed * self.direction
        self.distance_travelled += abs(self.rect.x - prev_x)
        self.particles.update()
        # Solo generar partículas si no ha superado la distancia máxima
        if self.distance_travelled < self.max_distance:
            for i in range(14):
                spread = random.uniform(-0.22, 0.22)
                base_speed = random.uniform(7, 13)
                dx = base_speed * self.direction * (1 + 0.15 * random.random()) * (1 + 0.1 * abs(spread))
                dy = base_speed * spread
                if abs(spread) < 0.08:
                    color = (255, random.randint(120,180), random.randint(60,90), random.randint(180, 255))
                elif abs(spread) < 0.16:
                    color = (255, random.randint(60,100), random.randint(0,40), random.randint(120, 200))
                else:
                    color = (220+random.randint(0,35), random.randint(0,60), random.randint(0,30), random.randint(100, 180))
                size = random.randint(4, 8) if abs(spread) < 0.12 else random.randint(2, 5)
                lifetime = random.randint(18, 32)
                # Generar partículas justo en la boca del lanzallamas (posición actual de la bala)
                px = self.rect.centerx
                py = self.rect.centery
                self.particles.add(Particle(px, py, color, size, dx, dy, lifetime))
        # Eliminar si sale de pantalla o supera la distancia máxima
        if self.rect.right < 0 or self.rect.left > self.escenario.screen.get_width() or self.distance_travelled >= self.max_distance:
            # Detener sonido de lanzallamas al finalizar la bala
            if hasattr(self.escenario, 'music') and hasattr(self.escenario.music, 'fuego_fx'):
                self.escenario.music.fuego_fx.stop()
            self.kill()
        # Dibujar base y partículas
        self.escenario.screen.blit(self.image, self.rect)
        for particle in self.particles:
            self.escenario.screen.blit(particle.image, particle.rect)
        # Eliminar si sale de pantalla
        if self.rect.right < 0 or self.rect.left > self.escenario.screen.get_width():
            self.kill()
        # Dibujar base y partículas
        self.escenario.screen.blit(self.image, self.rect)
        for particle in self.particles:
            self.escenario.screen.blit(particle.image, particle.rect)
