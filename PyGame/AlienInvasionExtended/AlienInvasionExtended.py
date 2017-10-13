
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
    right_direction, left_direction = False, False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right_direction = True
                if event.key == pygame.K_LEFT:
                    left_direction = True
            elif event.type == pygame.KEYUP:
                right_direction = False
                left_direction = False

        if right_direction and ship_rect.right < screen_rect.right:
            ship_rect.centerx += 2
        if left_direction and ship_rect.left > screen_rect.left:
            ship_rect.centerx -= 2
     
			
        screen.fill(bg_color)
        screen.blit(ship,ship_rect)
        pygame.display.flip()


run_game()
