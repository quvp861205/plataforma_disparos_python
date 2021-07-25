from Library import *

class Exit(pygame.sprite.Sprite):
	def __init__(self, escenario, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.escenario = escenario
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
	
	def update(self):
		self.rect.x += self.escenario.screen_scroll

		if pygame.sprite.collide_rect(self.escenario.player, self):
			level = self.escenario.level+1
			self.escenario.inicializar(level)
			self.escenario.start_game = True