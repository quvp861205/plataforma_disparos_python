from Library import *
from Soldier import *
from Enemy import *
from ItemBox import *
from HealthBar import *
from Decoration import *
from Water import *
from Exit import *
from MainMenu import *

class Escenarios():
    def __init__(self, screen):

        self.screen = screen  
        self.obstacle_list = []
        self.world_data = []
        self.level_length = 0
        self.level = 1
        self.start_game = False
        self.list_background = []
        self.img_list = []

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

        self.scroll_thresh = 200
        self.screen_scroll = 0
        self.bg_scroll = 0

        self.mainMenu = MainMenu(self)
        
        
    def inicializar(self, level):
        self.obstacle_list = []
        self.world_data = []
        self.level_length = 0
        self.level = level
        self.start_game = False        

        self.list_background = []
        for bg in os.listdir(f"img/background"):
            image = pygame.image.load(f"img/background/{bg}").convert_alpha() # carga imagen de fondo            
            self.list_background.append(image) 

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
        
        self.scroll_thresh = 200
        self.screen_scroll = 0
        self.bg_scroll = 0

        self.mainMenu = MainMenu(self)

        self.process_data()
    

    def draw_background(self):
        sky = self.list_background[3] #sky
        mountain = self.list_background[0]
        pine1 = self.list_background[1]
        pine2 = self.list_background[2]

        # movemos el fondo
        self.bg_scroll -= self.screen_scroll

        # se agrega un color base
        self.screen.fill(WHITE)

        # se agregan 5 veces los fondos uno al lado del otro para que abarque todo el mapa
        width = sky.get_width()
        for x in range(5):            
            self.screen.blit(sky, ((x*width) - self.bg_scroll*0.3,0))
            self.screen.blit(mountain, ((x*width) - self.bg_scroll*0.5, SCREEN_HEIGHT - mountain.get_height() - 300))
            self.screen.blit(pine1, ((x*width) - self.bg_scroll*0.6, SCREEN_HEIGHT - pine1.get_height() - 150))      
            self.screen.blit(pine2, ((x*width) - self.bg_scroll*0.7, SCREEN_HEIGHT - pine2.get_height() ))            


    # cargamos los sprites en base al mapa y las imagenes
    def process_data(self):
        img_list = self.img_list
        data = self.world_data

        # para limitar el scroll del juego
        self.level_length = len(data[0])

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
                        water = Water(self, img, x * TILE_SIZE, y * TILE_SIZE)
                        self.water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(self, img, x * TILE_SIZE, y * TILE_SIZE)
                        self.decoration_group.add(decoration)
                    elif tile == 15:#create player
                        self.player = Soldier(self, 'player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20, 5)
                        self.health_bar = HealthBar(self, 10, 10)
                    elif tile == 16:#create enemies
                        enemy = Enemy(self, 'enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20)
                        self.enemy_group.add(enemy)
                    elif tile == 17:#create ammo box
                        item_box = ItemBox(self, 'Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        self.item_box_group.add(item_box)
                    elif tile == 18:#create grenade box
                        item_box = ItemBox(self,  'Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        self.item_box_group.add(item_box)
                    elif tile == 19:#create health box
                        item_box = ItemBox(self, 'Health', x * TILE_SIZE, y * TILE_SIZE)
                        self.item_box_group.add(item_box)
                    elif tile == 20:#create exit
                        exit = Exit(self, img, x * TILE_SIZE, y * TILE_SIZE)
                        self.exit_group.add(exit)
    
    def draw(self):

        if self.start_game==False:
            # pintamos el menu
            self.screen.fill(BG)
            self.mainMenu.update()

        else:
            self.draw_background()       

            self.player.update()
            
            for tile in self.obstacle_list:
                tile[1].x += self.screen_scroll
                self.screen.blit(tile[0], tile[1])

            self.enemy_group.update()           

            self.decoration_group.update()
            self.decoration_group.draw(self.screen)

            self.water_group.update()
            self.water_group.draw(self.screen)

            self.exit_group.update()
            self.exit_group.draw(self.screen)     

            self.item_box_group.update()
            self.item_box_group.draw(self.screen)   
            
            self.health_bar.draw()

        

       
        

