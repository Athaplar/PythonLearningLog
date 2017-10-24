
import pygame
import sys
from math import fabs

def run_game():
    
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    gameState = GameState()
    ships = init_ships(screen, ai_settings, gameState)
    pygame.display.set_caption(ai_settings.game_Caption)
    bullets =[]
    score = Score(screen,ai_settings)
    ship = ships[0]
    ship.set_status(ShipStatus.ON)
    fleet_of_alien = Fleet_Of_Alien(screen,ai_settings,gameState)
    fleet_of_alien.spawn_alien_fleet()
	
    while True:
        update_game_state(gameState)
        ship.do_update()
        fleet_of_alien.do_update()
        if gameState.bullet_fired and len(bullets) < ai_settings.max_allowed_bullets:
            bullet = Bullet(ship,screen,ai_settings)
            bullets.append(bullet)
            		
        for bullet in bullets:
            bullet.do_update()
            
			
        bullets_copy = bullets.copy()
        for bullet in bullets:
            collison = fleet_of_alien.has_collided_with(bullet.rect)
            if collison:
                score.score = score.score + 1
                bullet.make_bullet_disappear_from_Screen()
            if bullet.y < 0 or collison:
                bullets_copy.remove(bullet)	
		
	
        alien_ship_collison = fleet_of_alien.has_collided_with(ship.rect)
        alien_has_moved_beyond_bottom_of_screen = fleet_of_alien.any_alien_moved_beyond_bottom_of_screen()		
        screen.fill(ai_settings.GRAY)  #fill seem to be hiding all drawing below.Need to figure out what is happening 
        
        if alien_ship_collison or alien_has_moved_beyond_bottom_of_screen:
            #display_hit(screen,ai_settings)
            ship.set_status(ShipStatus.CRASHED)
            ship = next_ship_life(ships,screen,ai_settings)
            ship.set_status(ShipStatus.ON)
            fleet_of_alien.spawn_alien_fleet()
            #alien_has_moved_beyond_bottom_of_screen = False
      
        draw(ships, screen, ai_settings)  
        score.draw()
        draw(fleet_of_alien.alien_fleet, screen, ai_settings)
        
      
        for bullet in bullets:
            bullet.draw()   
        bullets = bullets_copy
		
        #if is_hit:
        #    display_hit(screen,ai_settings)
		
        pygame.display.flip()



def next_ship_life(ships, screen, ai_settings):
    for ship in ships:
        if ship.status is ShipStatus.OFF:
            ship.status = ShipStatus.ON
            return ship


def draw(items, screen, ai_settings):
    for item in items:
        item.draw()
        #display_hit(screen,ai_settings)
	
def init_ships(screen, ai_settings, gameState):
    #ships = [ Ship(screen,ai_settings,gameState) for _ in range(ai_settings.num_of_ships)]
    ships = [Ship(screen,ai_settings,gameState),Ship(screen,ai_settings,gameState),Ship(screen,ai_settings,gameState)]
    width = ships[0].rect.width
    height = ships[0].rect.height
    x_screen = ai_settings.screen_width - 100 - ai_settings.num_of_ships * width# 100 because score object is draw at right most place
    y_screen = 10 # + ai_settings.space_btw_ships
    index =0
    for ship in ships:
        ship.x_screen = x_screen +   index * width # + ai_settings.space_btw_ships 
        ship.y_screen = y_screen
        ship.set_status(ShipStatus.OFF)
        index+=1
    return ships	
	
    

def display_hit(screen,ai_settings): 
    basicfont = pygame.font.SysFont(None, 30)
    text = basicfont.render('Condition met!', True, ai_settings.BLACK, ai_settings.GREEN)
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery
    screen.blit(text, text_rect)

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

			
class Fleet_Of_Alien():
    """
    Takes care of Alien motion (downwards/side ways)
    Knows the screen dimension and number of aliens to spawn
    """
    def __init__(self, screen, ai_settings,gameState):
        self.screen = screen
        self.ai_settings = ai_settings
        self.alien_fleet = None
        self.gameState = gameState
		
    def do_update(self):
        for alien in self.alien_fleet:
            alien.do_update()
            if alien.x < 1:
                self.gameState.alien_x_direction = MoveDirection.RIGHT
            elif alien.x > 	self.ai_settings.useable_screen_width:
                self.gameState.alien_x_direction = MoveDirection.LEFT


    def spawn_alien_fleet(self):
        first_alien = Alien(self.screen,self.ai_settings,self.gameState)
        num_of_aliens_in_a_row = self.ai_settings.useable_screen_width / (first_alien.rect.width + self.ai_settings.space_btw_ships)
        self.alien_fleet = [Alien(self.screen,self.ai_settings,self.gameState) for _ in range(int(num_of_aliens_in_a_row))]
        index=0
        for alien in self.alien_fleet:
            alien.x = first_alien.rect.width * index
            alien.rect.x = alien.x
            index+=1
       
	
    def has_collided_with(self,rect):
        has_collided_with = False
        for alien in self.alien_fleet:
            if alien.has_collided_with(rect):
                alien.make_disappear_from_Screen()
                has_collided_with = True
        return has_collided_with

    def any_alien_moved_beyond_bottom_of_screen(self):
        for alien in self.alien_fleet:
            if alien.has_moved_beyond_bottom_of_screen():
                return True
        return False
	

class Alien():
    
    def __init__(self,screen,ai_settings,gameState):
	
        self.alien = pygame.image.load(ai_settings.alien_image_location)
        self.rect = self.alien.get_rect()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.y = 0
        self.x = 0
        self.gameState = gameState
        self.crashed = False
		#self.rect.top = 0
    def do_update(self):
	    
        if self.crashed:
             return

        speed = self.ai_settings.alien_x_speed
        x = self.x
        self.x = x - speed if self.gameState.alien_x_direction is MoveDirection.LEFT else x + speed
        self.rect.x = self.x
		
        self.y = self.y + self.ai_settings.alien_vertical_speed
        self.rect.y = self.y
		
    def draw(self):
        self.screen.blit(self.alien,self.rect)

    def has_moved_beyond_bottom_of_screen(self):
        return self.rect.bottom > self.screen_rect.bottom
		
    def has_collided_with(self,rect):
        deltay = fabs(self.rect.centery - rect.centery)
        deltax = fabs(self.rect.centerx - rect.centerx)
        return deltay < rect.height and deltax < rect.width	
		
    def make_disappear_from_Screen(self):
        self.rect.x = -100
        self.rect.y = -100
        self.crashed = True

		
class Settings():
 
    def __init__(self):
        self.screen_width = 1200

        self.screen_height = 700
        self.useable_screen_width = .8 * self.screen_width
        self.GRAY = (230,230,230)
        self.GREEN = (0,255,0)
        self.BLACK = (0,0,0)
        self.bullet_width = 100
        self.bullet_height = 10
        self.bullet_color = self.BLACK
        self.game_Caption = 'Alien Invasion'
        self.image_location = 'images/ship.bmp'
        self.alien_image_location = 'images/alien.bmp'
        self.bullet_speed = 1
        self.max_allowed_bullets = 3
        self.alien_vertical_speed = .1
        self.alien_x_speed = .1
        self.alien_image_location = 'images/alien.bmp'
        self.num_of_ships = 3
        self.space_btw_ships = 5
        self.space_btw_aliens = 0
		
		

class Bullet():
     
    def __init__(self, ship, screen, ai_settings):
        self.ship = ship
        self.screen = screen
        self.ai_settings = ai_settings
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = self.ship.rect.centerx
        self.rect.top = self.ship.rect.top
        self.y = float(self.ship.rect.y)
        self.x = float(self.ship.rect.x)
        #self.bullet_rect.top = 30
        #pygame.draw.rect(self.screen,self.ai_settings.GREEN,self.bullet_rect)
		
    def do_update(self):    
        self.y = self.y - self.ai_settings.bullet_speed
        self.rect.y = self.y
	
    def make_bullet_disappear_from_Screen(self):
        self.rect.x = -1 #Making bullet disappear by drawing it out side of the screen in next frame
        self.rect.y = -1 
		
    def draw(self): 
        pygame.draw.rect(self.screen,self.ai_settings.bullet_color,self.rect)    
	
class GameState():
    
    def __init__(self):
        self.ship_move_right = False
        self.ship_move_left = False
        self.bullet_fired = False
        self.alien_x_direction = MoveDirection.RIGHT
		
		

class Score():
    def __init__(self,screen,ai_settings):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.score = 0
        self.ai_settings = ai_settings
		#draw score top right
    def draw(self):
        basicfont = pygame.font.SysFont(None, 30)
        text = basicfont.render('Score:'+str(self.score), True, self.ai_settings.BLACK, self.ai_settings.GREEN)
        text_rect = text.get_rect()
        text_rect.x = self.screen_rect.width-100
        text_rect.y = 10
        self.screen.blit(text, text_rect)

class Ship():

    def __init__(self,screen,ai_settings,gameState):
        self.screen=screen
        self.ship=pygame.image.load(ai_settings.image_location)
        self.gameState = gameState
        self.rect = self.ship.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.x_screen = 0
        self.y_screen = 0
        self.status = ShipStatus.OFF
		
    def set_status(self,status_update):
	
        if status_update is ShipStatus.ON:
            self.rect.centerx = self.screen_rect.centerx
            self.rect.bottom = self.screen_rect.bottom
        else:
            self.rect.x = self.x_screen
            self.rect.y = self.y_screen
        self.status = status_update

    def do_update(self):
            if self.gameState.ship_move_right and self.rect.right < self.screen_rect.right:
                self.rect.centerx += 1
            if self.gameState.ship_move_left and self.rect.left > self.screen_rect.left:
                self.rect.centerx -= 1
       
			
    def make_ship_disappear_from_Screen(self):
        self.rect.x = -100
        self.rect.y = -100
        
    def draw(self):
        self.screen.blit(self.ship,self.rect)

from enum import Enum
class ShipStatus(Enum):
    ON = 1
    OFF = 2
    CRASHED = 3
	
class MoveDirection(Enum):
    LEFT = 1
    RIGHT = 2
    TOP = 3
    DOWN = 4
	
run_game()




