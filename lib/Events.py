import pygame, os
from pygame.locals import *

# Simul Thread with Run() Update and retrieve Commands
def Commands(queue):
    clock = pygame.time.Clock()
    while 1:
        clock.tick(30)
        command = "0"
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                os.system("exit")  # < - - - - - - - - - - -  
            elif event.type == pygame.KEYDOWN:
                queue.put("STOP")
                if event.key == K_a:
                    command = "Left"
                elif event.key == K_d:
                    command = "Right"
                elif event.key == K_SPACE:
                    command = "Jump"
                elif event.key == K_f:
                    command = "Fist"
                elif event.key == K_g:
                    command = "Kick"
                elif event.key == K_1:
                    command = "Rush"
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                queue.put("MouseDown")
            elif event.type == pygame.MOUSEBUTTONUP:
                queue.put("MouseUp")

            elif event.type == KEYUP and event.key != K_SPACE:
                command = "STOP"
        
        queue.put(command)  