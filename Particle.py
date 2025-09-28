import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size, dx, dy, lifetime, zigzag=False):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx
        self.dy = dy
        self.lifetime = lifetime
        self.age = 0
        self.zigzag = zigzag
        import math
        self.zigzag_phase = random.uniform(0, 2 * math.pi) if zigzag else 0
        self.zigzag_amp = random.uniform(0.2, 1.2) if zigzag else 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.zigzag:
            import math
            self.rect.x += int(math.sin(self.age * 0.35 + self.zigzag_phase) * self.zigzag_amp * 2)
            self.rect.y += int(math.cos(self.age * 0.25 + self.zigzag_phase) * self.zigzag_amp)
        self.age += 1
        if self.age > self.lifetime:
            self.kill()
