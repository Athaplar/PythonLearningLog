
import pygame
import sys

def run_game():
    
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    gameState = GameState()
    ship = Ship(screen,ai_settings,gameState)
    pygame.display.set_caption(ai_settings.game_Caption)
    bullets =[]
	
    while True:
        update_game_state(gameState)
        ship.do_update()
		
        if gameState.bullet_fired and len(bullets) < ai_settings.max_allowed_bullets:
            bullet = Bullet(ship,screen,ai_settings)
            bullets.append(bullet)
            		
        for bullet in bullets:
            bullet.do_update()
        bullets_copy = bullets.copy()
        for bullet in bullets:
            if bullet.y < 0:
                bullets_copy.remove(bullet)			
		
        screen.fill(ai_settings.GRAY)  #fill seem to be hiding all drawing below.Need to figure out what is happening 
        ship.draw()
        for bullet in bullets:
            bullet.draw()   
        bullets = bullets_copy			
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
        self.bullet_speed = 1
        self.max_allowed_bullets = 3

class Bullet():
     
    def __init__(self, ship, screen, ai_settings):
        self.ship = ship
        self.screen = screen
        self.ship_rect = ship.ship.get_rect()
        self.ai_settings = ai_settings
        self.bullet_rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.bullet_rect.centerx = self.ship.ship_rect.centerx
        self.bullet_rect.top = self.ship.ship_rect.top
        self.y = float(self.ship.ship_rect.y)
        #self.bullet_rect.top = 30
        #pygame.draw.rect(self.screen,self.ai_settings.GREEN,self.bullet_rect)
		
    def do_update(self):    
        self.y = self.y - self.ai_settings.bullet_speed
        self.bullet_rect.y = self.y

    def draw(self): 
        pygame.draw.rect(self.screen,self.ai_settings.bullet_color,self.bullet_rect)    
	
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
			
    def draw(self):
        self.screen.blit(self.ship,self.ship_rect)
		
run_game()




