# shake.py
# This class is used to shake the whole screen.

import urandom as random

class Shake:
    def __init__(self):
        self.resetShake()
    
    def update(self):
        if self.shake:
            if self.shakeSpeed > 0:
                if random.getrandbits(1) == 1:
                    self.shakeSpeed -= 1
            else:
                self.shakeSpeed = self.shakeSpeedMax
                self.shakeAmount -= 1
            
            if self.shakeAmount <= 0:
                self.shakeAmount == self.shakeMax
                self.shake = False
                
        if self.shake:
            self.direction = -self.direction
            if self.direction == 1:
                return self.shakeAmount
            else:
                return -self.shakeAmount
        else:
            return 0
            
    # Set shake to start
    def setShake(self):
        self.shake = True
        self.shakeAmount = self.shakeMax
    
    # Is screen shaking?
    def isShaking(self):
        return self.shake
        
    # Reset shake
    def resetShake(self):
        self.shake = False
        self.direction = 1
        self.shakeMax = 3
        self.shakeAmount = self.shakeMax
        self.shakeSpeed = 4
        self.shakeSpeedMax = self.shakeSpeed