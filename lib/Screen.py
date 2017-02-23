import pygame, os

pygame.init()
# Global identifier
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Luffy')
clock = pygame.time.Clock()

front = pygame.font.SysFont("monospace", 15)

Red = (255, 0, 0)
Green = (10, 200, 5)

LeftBoundary, RightBoundary = -20, 800

# agrs(Player, [Image], [Enemy_obs]) 
Image_lst = {"Obstacle":[], "Icon":[], "test":[]}
# ------------------- #         
        
def Render(p):

    screen.fill((0, 0, 0))
    
    scaledX = p.x - p.fixedX
    
    for icon in Image_lst["Icon"]: screen.blit(icon.image, icon.posn)
        
    for block in Image_lst["Obstacle"]: 
        correctedX = block.rect[0] - scaledX
        if correctedX >= LeftBoundary and correctedX <= RightBoundary: screen.blit(block.image, (correctedX, block.rect[1]))
    
    if p.Image != None: screen.blit(p.Image, (p.fixedX, p.DisplayPosn[1])) 
    
    # health bar indicator
    shade = (255*(p.Energy)/p.EnergyCapacity)
    if shade > 255: shade = 255
    pygame.draw.rect(screen, (128+shade/2, shade, 0), (47, 30, 48*p.Energy/p.EnergyCapacity, 3), 0)
    # -------------------
    shade = (255*(p.Health)/p.HealthCapacity)
    pygame.draw.rect(screen, (128+shade/2, 0, 0), (47, 20, (88*p.Health/p.HealthCapacity), 6), 0)
    
    #for i in Image_lst["test"]:
        #clock.tick(15)
        #screen.blit(i, (0, 0))
        #pygame.display.update()

    pygame.display.update()    
