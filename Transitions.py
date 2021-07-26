from Library import *


class Transitions():
    def __init__(self, escenario, direction, color, speed):
        self.escenario = escenario
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0        
    
    def fade(self):              
        finish_fade = False
        if self.fade_counter<SCREEN_WIDTH:
            self.fade_counter += self.speed
        else:
            finish_fade = True

        if self.direction==1 and finish_fade==False:
            pygame.draw.rect(self.escenario.screen, self.color, (0 - self.fade_counter, 0, SCREEN_WIDTH//2, SCREEN_HEIGHT))
            pygame.draw.rect(self.escenario.screen, self.color, (SCREEN_WIDTH//2+self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(self.escenario.screen, self.color, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT//2))
            pygame.draw.rect(self.escenario.screen, self.color, (0, SCREEN_HEIGHT//2+self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction==2:
            pygame.draw.rect(self.escenario.screen, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))

        return finish_fade
    
