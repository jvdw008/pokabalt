# background.py
# Creates and draws a background

import upygame as pygame
import graphics

class Background:
    def __init__(self, startX, startY):
        self.x = startX
        self.y = startY

    # Pass in the image
    def draw(self, screen, bg):
        screen.blit(bg, self.x, self.y)
