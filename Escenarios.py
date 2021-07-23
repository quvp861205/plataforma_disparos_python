from Library import *
from Soldier import *
from Enemy import *
from ItemBox import *
from HealthBar import *
from Decoration import *
from Water import *
from Exit import *

class Escenarios():
    def __init__(self, screen):
        
        self.obstacle_list = []
        self.world_data = []
        self.level = 1
        self.screen = screen

        #grupos de sprites
        self.player = {}
        self.health_bar = {}
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.grenade_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.item_box_group = pygame.sprite.Group()
        self.decoration_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()

        # creamos un mapa con -1
        for row in range(ROWS):
            r = [-1] * COLS
            self.world_data.append(r)
        
        # cargamos un nivel
        with open(f'levels/level{self.level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)
        
        # cargamos las imagenes
        self.img_list = []
        for x in range(TILE_TYPES):
            img = pygame.image.load(f'img/Tile/{x}.png')
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.img_list.append(img)
    
    # cargamos los sprites en base al mapa y las imagenes
    def process_data(self):
        img_list = self.img_list
        data = self.world_data

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)

                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        self.water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        self.decoration_group.add(decoration)
                    elif tile == 15:#create player
                        self.player = Soldier(self, 'player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20, 5)
                        self.health_bar = HealthBar(self, 10, 10)
                    elif tile == 16:#create enemies
                        enemy = Enemy(self, 'enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20)
                        self.enemy_group.add(enemy)
                    elif tile == 17:#create ammo box
                        item_box = ItemBox(self.player, 'Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        self.item_box_group.add(item_box)
                    elif tile == 18:#create grenade box
                        item_box = ItemBox(self.player, 'Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        self.item_box_group.add(item_box)
                    elif tile == 19:#create health box
                        item_box = ItemBox(self.player, 'Health', x * TILE_SIZE, y * TILE_SIZE)
                        self.item_box_group.add(item_box)
                    elif tile == 20:#create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        self.exit_group.add(exit)
    
    def draw(self):
        for tile in self.obstacle_list:
            self.screen.blit(tile[0], tile[1])

        self.enemy_group.update(self.screen, self.player)
        self.item_box_group.update()
        self.item_box_group.draw(self.screen)
        self.decoration_group.draw(self.screen)
        
        self.player.update(self.screen, self.enemy_group)
        self.health_bar.draw()

       
        

