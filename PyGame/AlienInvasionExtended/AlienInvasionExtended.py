
import pygame
import sys

def run_game():
    
    pygame.init()
    screen = pygame.display.set_mode((700,700))
    screen_rect = screen.get_rect()
    ship = pygame.image.load('images/ship.jpg')
    ship_rect = ship.get_rect()
    pygame.display.set_caption('Alien Invasion')
    bg_color = (230,230,230)

    #ship related
    ship_rect.centerx = screen_rect.centerx
    ship_rect.bottom = screen_rect.bottom

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RIGHT :
                    ship_rect.centerx +=2
                if event.key == pygame.K_LEFT:
                    ship_rect.centerx -=2
        screen.fill(bg_color)
        screen.blit(ship,ship_rect)
        pygame.display.flip()


run_game()
