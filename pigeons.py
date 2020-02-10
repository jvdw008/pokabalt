# pigeons.py
# Traditional class object, but we won't delete them, we'll only ever have 5-10 objects and reset their positions when they leave the screen

import upygame as pygame
import graphics
import urandom as random

class Pigeon:
    def __init__(self, x, y, staticImg):
        self.image = staticImg
        self.reset(x, y)
        self.animCreated = False
        self.flyingMovement = 0 # Used to adjust horizontal movement
        
    # Update position
    def update(self, scrollSpeed):
        if self.x > - 10:
            self.x -= 1 + scrollSpeed
            
        if self.x < 60:
            self.flying = True
            
        if self.flying:
            self.y -= random.getrandbits(3) + 2
            self.x += self.flyingMovement
            
        
    # Only draw stationary bird when not flying and in screen viewport
    def draw(self, screen, shake):
        if not self.flying and self.x > -10:
            screen.blit(self.image, self.x, self.y + shake)
            
    # Get flight status
    def getStatus(self):
        return self.flying
        
    # Get direction
    def getDirection(self):
        return self.direction
        
    # Reset this pigeon after leaving screen
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.direction = random.getrandbits(1)
        self.flying = False
        self.animCreated = False
        self.flyingMovement = random.getrandbits(3) - 1
        
    # Set animation status created
    def setAnim(self):
        self.animCreated = True
        
    # Get anim status
    def getAnim(self):
        return self.animCreated
        
    # Get pos
    def getPosition(self):
        return [self.x, self.y]
    