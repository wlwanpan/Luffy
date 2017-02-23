"""
Class file for class Luffy and loading of Sprites 
"""

from Luffy_Movement import *
import spritesheet
from Tuples import *

class Sprites:
        
    def LoadSprites(self, Lib):
        omitVal = (7, 103, 51)
        for Name in Lib:
            tup_coor = Lib[Name]
            filename = 'sprites/Luffy/'+Name+'.png'
            sheet = spritesheet.spritesheet(filename)
            tups = ((i[0], i[1], i[2]-i[0], i[3]) for i in tup_coor)
            array = sheet.images_at(tups, colorkey=omitVal)
            self.Database.update({Name:array}) 

class Luffy(Sprites, Movement, Special):
    
    def __init__(self):
        
        self.x, self.y, self.fixedX = 150, 150, 300
        self.fall, self.direction = 1, None
        self.width, self.height = 40, 69
        self.Damage, self.flip = 0, 0
        self.Energy, self.EnergyCapacity = 0, 10
        self.Health, self.HealthCapacity = 10, 100
        self.Image, DisplayPosn = None, ()
        
        self.DamageZone = []
        # Dictionary name: {name:tup}
        self.SheetNames = {'walk':walk, 'standby':standby, 'jump':jump, 
                           'fist':fist, 'kick':kick, 
                           'rush':rush}
        self.Database = {} # storage of sprite

        # Damage database {Name:[int dmg, [Rect]]}
        self.DamageDict = {'fist':[5, [42, 20, 25, 25]], 
                           'kick':[10, [49, 24, 93, 47]], 
                           'rush':[25, [38, 0, 68, 70]]}
        
        self.LoadSprites(self.SheetNames)  # Load Movement Sprites
        
    def Run(self, queue):
    
        while 1:
            clock.tick(30)
            if not queue.empty():
                tmp_cmd = queue.get() 
                if tmp_cmd == "Right" or tmp_cmd == "Left":
		    self.direction = tmp_cmd
                    self.walk(queue)
                elif tmp_cmd == "Jump": self.jump(queue)
                elif tmp_cmd == "Fist": self.fist(queue)
                elif tmp_cmd == "Kick": self.kick(queue)
                elif tmp_cmd == "Rush": self.rush(queue)
                    
                else: self.standby(queue)  
	    self.collision(queue)
		
    def move(self, x, y): 
    
	self.x += x
	self.y += y
        
    def Blit(self, Name, i):
        
        tups, image = (self.SheetNames[Name])[i], (self.Database[Name])[i]
        height, width = tups[3], tups[2] - tups[0]

        if height < self.height: y = self.y + (self.height - height)
        else: y = self.y
        
        if self.flip == 1:
            image = pygame.transform.flip(image, True, False)
            x = self.x - (width - self.width)
        else: x = self.x
        self.Image = image # updating player image
	self.DisplayPosn = (x, y)
        Render(self) # blit all image object from the list
	
    def collisionY(self, q):
	
	jumpscale = 5
	scaledX = 2
	
	for obs in Image_lst["Obstacle"]: 
	    x, y = obs.rect[0], obs.rect[1]
	    if self.x-scaledX >= x and self.x+scaledX <= (x+obs.rect[2]) \
	       or self.x-scaledX + self.width >= x and self.x+scaledX + self.width <= (x+obs.rect[2]):
		
		if self.y + self.height >= y - jumpscale and \
		   self.y + self.height <= y + obs.rect[3] + jumpscale:
		    self.y = y - self.height
		    return True
	return False
    
    def collisionX(self, q): 
	rangeX = 50
	boundaryL, boundaryR = self.x - rangeX, self.x + self.width + rangeX
	for obs in Image_lst["Obstacle"]: 
	    x, y, w, h= obs.rect[0], obs.rect[1], obs.rect[2], obs.rect[3]
	    if x >= boundaryL and x + w <= boundaryR: 
		
		if self.y <= y + w:
		    if self.x + self.width >= x and self.x + self.width <= x + w: self.x = x
		    return True 
	    
	return False
		
    def collision(self, q): 
	
	if not(self.collisionY(q)): self.freefall(q)
        
    def DamageUpdater(self, move):
        
        if move == None:
            self.Damage = 0
            self.DamageZone = []
        else: 
            data = self.DamageDict[move]
            rect = data[1]
            self.Damage = data[0]
            
            if self.flip == 1: corr = [0, rect[1], -rect[2], rect[3]]
            else: corr = rect
            self.DamageZone = (corr[0]+self.x, corr[1]+self.y, corr[2], corr[3])
    
            pygame.display.update()
            
    def dmgArea(self, move):
	    
	rect = self.DamageDict[move][1]
	
	if self.flip == 0: corr = [rect[0]+self.fixedX, rect[1]+self.y, rect[2], rect[3]]
	elif self.flip == 1: corr = [self.fixedX-rect[2], rect[1]+self.y, rect[2], rect[3]]
	
	pygame.draw.rect(screen, Red, corr, 1)
    
	dmg = self.DamageDict[move][0]
	label = front.render(str(dmg), 1, Red)  	
	
	screen.blit(label, (self.fixedX, self.y))
	
	pygame.display.update()	    
