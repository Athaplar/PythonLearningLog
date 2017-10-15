
import pygame
import sys

def run_game():
    
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    gameState = GameState()
    ship = Ship(screen,ai_settings,gameState)
    pygame.display.set_caption(ai_settings.game_Caption)
    
    while True:
        update_game_state(gameState)
        ship.do_update()
        if gameState.bullet_fired:
            bullet = Bullet(ship,screen,ai_settings)
            bullet.do_update()
        #screen.fill(bg_color)  fill seem to be hiding all drawing below.Need to figure out what is happening 
        
        pygame.display.flip()

def update_game_state(gameState):

    gameState.bullet_fired = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                gameState.ship_move_right = True
            elif event.key == pygame.K_LEFT:
                gameState.ship_move_left = True
            elif event.key == pygame.K_SPACE:
                gameState.bullet_fired = True
        elif event.type == pygame.KEYUP:
            gameState.ship_move_left = False
            gameState.ship_move_right = False
				
class Settings():
 
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 700
        self.GRAY = (230,230,230)
        self.GREEN = (0,255,0)
        self.BLACK = (0,0,0)
        self.bullet_width = 10
        self.bullet_height = 10
        self.bullet_color = self.BLACK
        self.game_Caption = 'Alien Invasion'
        self.image_location = 'images/ship.bmp'

class Bullet():
     
    def __init__(self, ship, screen, ai_settings):
        self.ship = ship
        self.screen = screen
        self.ship = ship
        self.ai_settings = ai_settings
        self.bullet_rect = pygame.Rect(0,0,30,30)
    
    def do_update(self):    
            self.bullet_rect.centerx = self.ship.ship_rect.centerx
            #bullet_rect.top = ship_rect.top
            pygame.draw.rect(self.screen,self.ai_settings.GREEN,self.bullet_rect) 
	
class GameState():
    
    def __init__(self):
        self.ship_move_right = False
        self.ship_move_left = False
        self.bullet_fired = False
 		

class Ship():

    def __init__(self,screen,ai_settings,gameState):
        self.screen=screen
        self.ship=pygame.image.load(ai_settings.image_location)
        self.gameState = gameState
        self.ship_rect = self.ship.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.ship_rect.centerx = self.screen_rect.centerx
        self.ship_rect.bottom = self.screen_rect.bottom
		
    def do_update(self):
	
        if self.gameState.ship_move_right and self.ship_rect.right < self.screen_rect.right:
            self.ship_rect.centerx += 1
        if self.gameState.ship_move_left and self.ship_rect.left > self.screen_rect.left:
            self.ship_rect.centerx -= 1
			
        self.screen.blit(self.ship,self.ship_rect)
		
run_game()




