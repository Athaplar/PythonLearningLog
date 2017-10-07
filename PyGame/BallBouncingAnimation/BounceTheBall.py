import pygame
import sys

def bounce():
    
    pygame.init()
    move_offset = [2,2]
    screen_size = screen_width,screen_height = 900 ,900
    screen = pygame.display.set_mode(screen_size)
    ball_surface = pygame.image.load('ball.png')
    ball_surface_rect = ball_surface.get_rect()
    
    while True:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
 
        ball_surface_rect = ball_surface_rect.move(move_offset)  
        if ball_surface_rect.left < 0 or ball_surface_rect.right > screen_width:
            move_offset[0] = -move_offset[0]
        if ball_surface_rect.top < 0 or ball_surface_rect.bottom > screen_height:
            move_offset[1] = -move_offset[1]
    
        screen.fill((0,0,0))
        screen.blit(ball_surface,ball_surface_rect)
        pygame.display.flip()