# player.py
# Handle player control and management

import upygame as pygame
import graphics

class Player:
    def __init__(self, startX, startY, size):
        self.playerX = startX		# Start X
        self.playerY = startY		# Start Y
        self.startY = startY        # Value to return to for player to land back
        self.state = 0              # 0 = run, 1 = jump, 2 = fall
        self.jumpDirection = 1      # 1 for up, -1 for down
        self.jumpSpeed = 7         # Speed of jump
        self.gravity = 0            # Gets set on jump
        self.size = size            # Physical size for hitbox detection
        self.buttonPressedTime = 2
        self.buttonMax = 2         # These are used so player press doesn't add too much to jump

    # Draw player
    #def draw(self, screen, image, shakeX):
    #    screen.blit(image, self.playerX + shakeX, self.playerY)
    
    def draw(self, shake):
        pygame.draw.rect(pygame.Rect(self.playerX, self.playerY + shake, self.size, self.size), True, 1)

    # Check if player jumping
    def updateJump(self, keyPressed, gravity):
        if self.playerY > -20:
            self.gravity = gravity
            self.playerY -= self.jumpSpeed
            self.jumpSpeed -= 1
            
            #print (str(self.buttonPressedTime))
            
            if self.jumpSpeed <= 0:
                self.state = 2
            if self.jumpDirection == 1:
                if keyPressed and self.jumpSpeed > 0:
                    if self.buttonPressedTime > 0:
                        self.jumpSpeed += 1
                        self.buttonPressedTime -= 1
                    
        else:
            # Player has gone too high, so fall down
            self.state = 2
        
    # Do gravity
    def updateFall(self, bottomY):
        self.playerY += self.gravity
        self.gravity += 1
        if self.playerY >= bottomY:
            return True
        else:
            return False
        
    # Do run
    def update(self, yPos):
        self.playerY = yPos
    
    # Reset jump stats
    def reset(self, gravity, yPos, playerHeight):
        self.jumpDirection = 1
        self.jumpState = False
        self.jumpSpeed = 7
        self.gravity = gravity
        self.state = 0
        self.playerY = yPos - playerHeight
        self.startY = yPos - playerHeight
        self.buttonPressedTime = self.buttonMax
    
    # Set Y Pos for new platform heights
    def setHeight(self, yPos):
        print ("set ply height: " + str(yPos))
        self.startY = yPos
    
    # Set jumpstate 
    def setState(self, state):
        self.state = state
        
    # Get jumpstate
    def getState(self):
        return self.state
        
    # Set player x/y pos
    def setPlayerPos(self, y):
        self.playerY = y
    
    # Get player x/y pos
    def getPlayerPos(self):
        return (self.playerX, self.playerY)
        
    
