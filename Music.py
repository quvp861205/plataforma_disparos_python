from Library import *


class Music():
    def __init__(self):

        pygame.mixer.music.load("audio/music2.mp3")
        pygame.mixer.music.set_volume(0.1)

        self.jump_fx = pygame.mixer.Sound("audio/jump.wav")
        self.jump_fx.set_volume(0.2)

        self.shoot_fx = pygame.mixer.Sound("audio/shot.wav")
        self.shoot_fx.set_volume(0.2)

        self.grenade_fx = pygame.mixer.Sound("audio/grenade.wav")
        self.grenade_fx.set_volume(0.2)        

    def playBackground(self):
        pygame.mixer.music.play(-1, 0.0, 5000)