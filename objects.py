# objects.py
# This class is used for boxes and bombs etc

import upygame as pygame
import graphics
import urandom as random

class Object:
    def __init__(self, img, startX, startY, objectType, objHeight, objWidth):
        self.x = startX
        self.type = objectType
        self.landed = False
        self.hit = False
        
        if objectType == 0:
            self.y = startY - objHeight
            self.image = img[random.getrandbits(1)]
        else:
            self.y = -objHeight
            self.image = img
            
        self.height = objHeight
        self.width = objWidth
        
    # Update position
    def update(self, speed, buildingY):
        if self.hit:
            self.y += 4
            self.x += speed
            
        # Move item based on scroll speed
        self.x -= 1 + speed
        
        if self.type == 1:
            if self.x < 95:
                if self.y + self.height < buildingY:
                    self.y += 8
                else:
                    self.landed = True
        
        # Has object left screen?
        if self.x < -20:
            return True
        else:
            return False
            
    # Return type for blocker or killer
    def getType(self):
        return self.type
        
    # Get position
    def getPosition(self):
        return [self.x, self.y]
    
    # Get Size
    def getSize(self):
        return [self.width, self.height]
        
    # Has bomb landed
    def hasLanded(self):
        return self.landed
    
    # Draw
    def draw(self, screen, shake):
        screen.blit(self.image, self.x, self.y + shake)
        
    # Set object as being hit, ie crate
    def setHit(self):
        self.hit = True
        
    # Check if already hit
    def getHit(self):
        return self.hit