import pygame 

#button class
class Button():
	def __init__(self,x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	# PINTAMOS Y CAPTURAMOS EVENTOS DEL BOTON
	def draw(self, surface, pos_mouse):
		action = False

		# OBTENEMOS LA POSICION DEL MOUSE
		pos = pos_mouse

		# VALIDAMOS SI COLISIONA EL BOTON CON LA POSICION DEL MOUSE
		if self.rect.collidepoint(pos):
			# VALIDAMOS SI HIZO CLICK
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				print("Click sobre sprite ")
				action = True # ACTIVAMOS QUE FUE CLICKEADO
				self.clicked = True  # ACTIVAMOS QUE FUE CLICKEADO

		# SI CLICK FUE SOLTADO SE CANCELA EL CLICKIDO
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		# PINTAMOS EL BOTON
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action