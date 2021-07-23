from Library import *
pygame.font.init()


class HealthBar():
    def __init__(self, screen, x, y, player):
        self.x = x
        self.y = y
        self.player = player
        self.screen = screen

        #bullet
        self.bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
        #grenade
        self.grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_ammo(self):
        
        #show ammo
        self.draw_text('AMMO: ', font, WHITE, 10, 35)
        for x in range(self.player.ammo):
            self.screen.blit(self.bullet_img, (90 + (x * 10), 40))
        #show grenades
        self.draw_text('GRENADES: ', font, WHITE, 10, 60)
        for x in range(self.player.ammo_grenade):
            self.screen.blit(self.grenade_img, (135 + (x * 15), 60))

    def draw(self):
        #update with new health
        self.health = self.player.health
        #calculate health ratio
        ratio = self.player.health / self.player.max_health
        pygame.draw.rect(self.screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(self.screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(self.screen, GREEN, (self.x, self.y, 150 * ratio, 20))

        self.draw_ammo()