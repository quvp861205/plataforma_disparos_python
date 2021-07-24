from Library import *

class Water(pygame.sprite.Sprite):
	def __init__(self, escenario, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.escenario = escenario
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
	
	def update(self):
		self.rect.x += self.escenario.screen_scroll