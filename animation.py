# animation.py
# This class is used to animate images

class Animation:
    def __init__(self, images, speed):
        self.images = images                    # The list of images in an array
        self.frames = len(images) - 1           # How many frames are there
        self.framesCounter = len(images) - 1    # Counter for resetting the frames
        self.speed = speed                      # The speed of the animation
        self.speedCounter = speed               # The top speed for resetting the counter

    # Update the image frame
    def update(self):
        if (self.speed > 0):
            self.speed -= 1
        else:
            # Reset timer counter
            self.speed = self.speedCounter
            if (self.frames < self.framesCounter):
                self.frames += 1
            else:
                # Reset frame counter
                self.frames = 0

    # Update anim speed
    def increaseAnimSpeed(self, speed):
        if self.speed > 0:
            self.speed -= speed
            self.speedCounter -= speed
    
    # Draw the image
    def draw(self, screen, x, y, shake):
        screen.blit(self.images[self.frames], x, y + shake)
