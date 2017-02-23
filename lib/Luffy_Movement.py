from Screen import *
import random, math, time

class Special:
    """
    Methods for luffys special attk moves
    """
    def rush(self, q):
	
	if self.Energy < 6: return

        for i in range(4):        
            q.get()
            if self.flip == 1:
                self.x -= 40
            else: self.x += 40
            self.Blit('rush', i) # Blit here
        x = self.x
        pygame.display.update()
        init_time = time.time()
        while q.get() != "MouseDown":
            x = pygame.mouse.get_pos()[0] - 6
            if time.time() - init_time >= 0.5: break
	    if x < self.x: self.flip = 1
	    else: self.flip = 0
        self.x = x - 10 # teleport self.x
        for i in range(3, 16):
            q.get()
            self.Blit('rush', i) # Blit here
	    # Update Damage according to animations ongoing
            if i == 9 or i == 10: self.DamageUpdater('rush')
            else: self.DamageUpdater(None)
	     
	    self.dmgArea('rush')    
	
	self.Energy -= 6
	
    def fist(self, q):
	if self.Energy < 2: return
	self.Energy -= 2
	for i in range(5):
	    cmd = q.get()
	    if cmd == "Fist":   
		self.fist(q)
		break
	    # Damage updater
	    elif cmd == "Right" or cmd == "Left": self.walk(cmd, q)
	    else: self.Blit('fist', i) # Blit here
	    if i == 2 or i == 3: self.DamageUpdater('fist')
	    else: self.DamageUpdater(None)
	    
	    self.dmgArea('fist')
    
    def kick(self, q):
		
	if self.Energy < 4: return

	for i in range(9):
	    cmd = q.get()
	    if cmd == "Right" or cmd == "Left":
		self.walk(cmd, q)
		break
	    self.Blit('kick', i) # Blit here
	    if i == 4 or i == 5: self.DamageUpdater('kick')
	    else: self.DamageUpdater(None)
	      
	    self.dmgArea('kick')
	self.Energy -= 4    
    

class Movement:
    """
    Callable methods for luffys basic movements: 
    walk, standby, fist, kick, jump, freefall
    """
    def walk(self, q):     
        for i in range(18):
            x = q.get()
	    self.collision(q)
	    if x == "Jump": self.jump(q)
            if i == 8:
                self.walk(q)  
                break
            if x == "STOP": break
            if self.direction == "Right" or x == "Right":
                self.move(10, 0)            
                self.flip = 0
		self.direction = "Right"
            elif self.direction == "Left" or x == "Left":
                self.move(-10, 0)
                self.flip = 1
		self.direction = "Left"

            self.Blit('walk', i/2)  # Blit here

    def standby(self, q): 
	
	self.Blit('standby', random.randint(0, 2))
	if self.Energy < self.EnergyCapacity: self.Energy += 0.2
	if self.Health < self.HealthCapacity: self.Health += 1
	self.direction = None
            
    def jump(self, q):

        x, y = pygame.mouse.get_pos()
	scaledX = 300
	if y >= self.y: return 0
	if x < scaledX: self.flip = 1
	else: self.flip = 0
        dx, dy = x - scaledX, y - self.y
        angle = math.atan2(dy, dx)
        dx0, dy0 = int(25*math.cos(angle)), int(25*math.sin(angle))  
	temp = []
        while 1:
	    cmd = q.get()
            temp.append(cmd)
            dy0 += 1.5
            self.move(dx0, dy0)
            if dy0 < 0: self.Blit('jump', 0) # going up image
	    elif dy0 >= -10 and dy0 <= 10: self.Blit('jump', 2)
            else: self.Blit('jump', 3) # down image

	    if self.collisionY(q) and dy0 >= 0: break
	    
	self.Blit('jump', 5)
	self.Blit('jump', 6)
    
	if "STOP" in temp: self.direction = None
	if self.direction == "Left" or self.direction == "Right": self.walk(q)
	else: self.standby(q)

    def freefall(self, q):
	temp = []
        while 1:

	    temp.append(q.get())
	    
	    if self.collisionY(q): break
		
            self.Blit('jump', 3)
	    if self.direction == "Right": self.move(5, 15)
	    elif self.direction == "Left": self.move(-5, 15)
	    else: self.move(0, 15)
	    
	if "STOP" in temp: q.put("STOP")
	    
	self.Blit('jump', 5)
	self.Blit('jump', 6)

	