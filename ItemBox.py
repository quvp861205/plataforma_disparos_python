from Library import *

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, escenario, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.escenario = escenario


        self.item_type = item_type
        self.x = x 
        self.y = y
        self.player = self.escenario.player        

        #pick up boxes
        health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
        ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
        grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
        item_boxes = {
            'Health'	: health_box_img,
            'Ammo'		: ammo_box_img,
            'Grenade'	: grenade_box_img
        }

        self.item_type = item_type
        self.image = item_boxes[item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE //2, y + (TILE_SIZE-self.image.get_height()))


    def update(self):
        # verifica si ya fue recolectado por el jugador
        if pygame.sprite.collide_rect(self, self.player):
            #check what kind of box it was
            if self.item_type == 'Health':
                self.player.health += 25
                if self.player.health > self.player.max_health:
                    self.player.health = self.player.max_health
                print("Recolecto +25 "+self.item_type)
            elif self.item_type == 'Ammo':
                self.player.ammo += 15
                print("Recolecto +15 "+self.item_type)
            elif self.item_type == 'Grenade':
                self.player.ammo_grenade += 3
                print("Recolecto +3 "+self.item_type)
            #delete the item box
            self.kill()

        self.rect.x += self.escenario.screen_scroll
            

