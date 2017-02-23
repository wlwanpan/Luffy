from Screen import *
from Tuples import *
import spritesheet

class Environment:
    
    def __init__(self): 
        
        self.ObsSheet = spritesheet.spritesheet('sprites/Map/obstacle.png')
        self.IconSheet = spritesheet.spritesheet('sprites/Map/life1.png')
        self.testSheet = spritesheet.spritesheet('sprites/Map/test.png')

        self.IconDict = {}
        self.ObsLst = []
        
    def load(self, maplevel):
        
        with open("map/"+maplevel) as f:
            row = 0
            for lines in f.readlines():
                column = 0
                lines = lines.replace('\n', "")
            
                for pixel in lines: 
                    
                    if pixel != '-': 
                        
                        temp_im = self.ObsSheet.image_at(ObsDict[pixel], colorkey=(7, 103, 51))     
                        temp_im = pygame.transform.scale(temp_im, (20, 20))
                        self.ObsLst.append(Obstacle((column, row), temp_im))
                    
                    column += 20
                row += 20
                
        for icon in IconDict: 
            
            temp_im = self.IconSheet.image_at(IconDict[icon], colorkey=(255, 255, 255))
            self.IconDict.update({icon:temp_im})
            
        Image_lst['Icon'].append(Icon((0, 0), self.IconDict['health']))
        
        for t in test: # to remove
            
            tempim = self.testSheet.image_at(t, colorkey=(7, 103, 51))
            tempim = pygame.transform.scale(tempim, (800, 500))
            Image_lst["test"].append(tempim)

    def Run(self): 
        
        self.load("L1.txt")
        Image_lst["Obstacle"] = self.ObsLst
    
class Obstacle:
    
    def __init__(self, (x, y), image):
        
        self.rect, self.image = pygame.Rect((x, y, 20, 20)), image
        self.Indestructible = 1
    
class Icon:
    
    def __init__(self, posn, image):
        
        self.posn = posn
        self.image = image