from Library import *


class MainMenu(pygame.sprite.Sprite):
	def __init__(self, escenario):
		pygame.sprite.Sprite.__init__(self)

		self.escenario = escenario

		#button images
		self.start_img = pygame.image.load('img/start_btn.png').convert_alpha()
		self.exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
		self.restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
		self.bg = pygame.image.load('img/bg.png')

		# white color
		self.color = (16,84,36)
		self.color_light = (34,177,76)		
		self.color_dark = (24,131,56)

		self.smallfont = pygame.font.SysFont('consolas',35)
		self.iniciar_juego_text = self.smallfont.render('Iniciar Juego' , True , self.color)
		self.despues_jugar_text = self.smallfont.render('Despues' , True , self.color)
		self.volver_jugar_text = self.smallfont.render('Volver a intentar' , True , self.color)

		self.width_button = 400
		self.height_button = 80
	
	def update(self):
		self.escenario.screen.blit(self.bg, (0, 0))

		posX1 = SCREEN_WIDTH//2 - self.width_button//2
		posY1 = SCREEN_HEIGHT//2 - 200	

		mouse = pygame.mouse.get_pos()

		if posX1 <= mouse[0] <= posX1+self.width_button and posY1 <= mouse[1] <= posY1+self.height_button:
			pygame.draw.rect(self.escenario.screen,self.color_light,[posX1, posY1, self.width_button,self.height_button])
			self.escenario.screen.blit(self.iniciar_juego_text , ((posX1+self.width_button//2) - 120, posY1+30))
		else:
			pygame.draw.rect(self.escenario.screen,self.color_dark,[posX1, posY1, self.width_button,self.height_button])
			self.escenario.screen.blit(self.iniciar_juego_text , ((posX1+self.width_button//2) - 120, posY1+30))

		posX2 = SCREEN_WIDTH//2 - self.width_button//2
		posY2 = SCREEN_HEIGHT//2
		

		if posX2 <= mouse[0] <= posX2+self.width_button and posY2 <= mouse[1] <= posY2+self.height_button:
			pygame.draw.rect(self.escenario.screen,self.color_light,[posX2, posY2, self.width_button,self.height_button])
			self.escenario.screen.blit(self.despues_jugar_text , ((posX2+self.width_button//2) - 60, posY2+30))
		else:
			pygame.draw.rect(self.escenario.screen,self.color_dark,[posX2, posY2, self.width_button,self.height_button])
			self.escenario.screen.blit(self.despues_jugar_text , ((posX2+self.width_button//2) - 60, posY2+30))

		for ev in pygame.event.get():
          
			if ev.type == pygame.QUIT:
				pygame.quit()
				
			# validamos el click
			if ev.type == pygame.MOUSEBUTTONDOWN:

				# iniciamos el juego
				if posX1 <= mouse[0] <= posX1+self.width_button and posY1 <= mouse[1] <= posY1+self.height_button:
					self.escenario.level = 1					
					self.escenario.inicializar(1)
					self.escenario.start_game = True
				
				# finalizamos el juego
				if posX2 <= mouse[0] <= posX2+self.width_button and posY2 <= mouse[1] <= posY2+self.height_button:
					pygame.quit()
	

	def updateRestart(self):
		posX1 = SCREEN_WIDTH//2 - self.width_button//2
		posY1 = SCREEN_HEIGHT//2 - 200	

		mouse = pygame.mouse.get_pos()

		if posX1 <= mouse[0] <= posX1+self.width_button and posY1 <= mouse[1] <= posY1+self.height_button:
			pygame.draw.rect(self.escenario.screen,self.color_light,[posX1, posY1, self.width_button,self.height_button])
			self.escenario.screen.blit(self.volver_jugar_text , ((posX1+self.width_button//2) - 150, posY1+30))
		else:
			pygame.draw.rect(self.escenario.screen,self.color_dark,[posX1, posY1, self.width_button,self.height_button])
			self.escenario.screen.blit(self.volver_jugar_text , ((posX1+self.width_button//2) - 150, posY1+30))

		# iniciamos el juego
		for ev in pygame.event.get():
          
			if ev.type == pygame.QUIT:
				pygame.quit()
				
			# validamos el click
			if ev.type == pygame.MOUSEBUTTONDOWN:
				if posX1 <= mouse[0] <= posX1+self.width_button and posY1 <= mouse[1] <= posY1+self.height_button:
					self.escenario.inicializar(self.escenario.level)				
					self.escenario.start_game = True