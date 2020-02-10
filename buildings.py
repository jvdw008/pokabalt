# buildings.py
# This class holds the data for a building to be spawned

import upygame as pygame
import graphics

class Building:
    def __init__(self, startX, startY, buildingLength, spacing, floorId, wallId, windowId):
        self.startY = startY
        self.currentY = startY
        self.startX = startX + (spacing * 8)
        self.length = buildingLength
        self.floorId = floorId
        self.wallId = wallId
        self.windowId = windowId
    
    # Update position of building
    def update(self, scrollSpeed):
        self.startX -= 1 + scrollSpeed
        
        # Crumble down if short building
        if self.length <= 10 and self.startX < 80:
            if self.startY < 50:
                self.currentY += 1
        
        # Check if building off screen to allow for deletion
        if self.startX + (self.length * 8) <= 0:
            # Building off screen
            return True
        else:
            # Building still on screen
            return False
        
    # For now, jsut draw floors
    def drawBuilding(self, screen, floorImages, windowImages, wallImages, shakeY):
        drawX = 0
        drawY = 0
        for col in range(self.length):
            # Only draw what's in scren viewport
            if self.startX + drawX > -8 and self.startX + drawX <= 110:
                screen.blit(floorImages[self.floorId], self.startX + drawX, self.currentY + drawY + shakeY)
            
            # Move to next tile in column
            drawX += 8
            
        # draw rest of building
        drawY += 8
        drawX = 0
        # Draw one floor of windows
        for col in range(self.length):
            # Only draw what's in scren viewport
            if self.startX + drawX > -8 and self.startX + drawX <= 110:
                screen.blit(windowImages[self.windowId], self.startX + drawX, self.currentY + drawY + shakeY)
            
            # Move to next tile in column
            drawX += 8
        
        # Then floors
        drawX = 0
        drawY += 8
        if drawY < 88:
            for col in range(self.length):
                # Only draw what's in scren viewport
                if self.startX + drawX > -8 and self.startX + drawX <= 110:
                    screen.blit(wallImages[self.wallId], self.startX + drawX, self.currentY + drawY + shakeY)
            
                # Move to next tile in column
                drawX += 8
                    
        # Then anotehr set of windows
        drawY += 8
        drawX = 0
        # Draw one floor of windows
        if drawY < 88:
            for col in range(self.length):
                # Only draw what's in scren viewport
                if self.startX + drawX > -8 and self.startX + drawX <= 110:
                    screen.blit(windowImages[self.windowId], self.startX + drawX, self.currentY + drawY + shakeY)
                
                # Move to next tile in column
                drawX += 8
                
        # Then the rest of the floors
        for row in range(4):
            drawX = 0
            drawY += 8
            if drawY < 88:
                for col in range(self.length):
                    # Only draw what's in scren viewport
                    if self.startX + drawX > -8 and self.startX + drawX <= 110:
                        screen.blit(wallImages[self.wallId], self.startX + drawX, self.currentY + drawY + shakeY)
                
                    # Move to next tile in column
                    drawX += 8
                
                
    # Get length
    def getRightMostX(self):
        return self.startX + (self.length * 8)
    
    # Get Y position of building fopr player
    def getYPos(self):
        return self.currentY
    
    # Get startX to match underneath player
    def getXPos(self):
        return self.startX