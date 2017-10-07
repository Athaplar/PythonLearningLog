import pygame
import sys
import random

def bounce():
    
    pygame.init()
    move_offset = [2,1]
    screen_size = screen_width,screen_height = 900 ,900
    screen = pygame.display.set_mode(screen_size)
    bg_field_surface = pygame.image.load('field.jpeg')
    screen.blit(bg_field_surface,(0,0))
    ball_surface = pygame.image.load('ball.png')
    ball_surface_rect = ball_surface.get_rect()
    pygame.display.update()
    direction_sing = [1,1]
	
    while True:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
				
        screen.blit(bg_field_surface,ball_surface_rect,ball_surface_rect) # erase 
        ball_surface_rect = ball_surface_rect.move(move_offset)
        direction_changed = False
		
        if ball_surface_rect.left < 0 or ball_surface_rect.right > screen_width:
            direction_sing[0] = -direction_sing[0]
            direction_changed = True

        if ball_surface_rect.top < 0 or ball_surface_rect.bottom > screen_height:
            direction_sing[1] = -direction_sing[1]
            direction_changed = True
			
        if direction_changed:
            move_offset[0] = random.randint(1,3) * direction_sing[0]
            move_offset[1] = random.uniform(1,2) * direction_sing [1]
    
       # screen.fill((0,0,0))
        screen.blit(ball_surface,ball_surface_rect)
        pygame.time.delay(10)
        #pygame.display.flip()
        pygame.display.update()