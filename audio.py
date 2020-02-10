# audio.py
# This class plays audio

import upygame as pygame
import sounds               # The sound data

class Audio:
    def __init__(self, g_sound, isThisRealHardware):
        self.sound = g_sound
        self.isThisRealHardware = isThisRealHardware

		# Play sfx
    def playSfx(self, snd):
        self.sound.play_sfx(snd, len(snd), False)

    # Music
    def playMusic(self, song):
        if (self.isThisRealHardware):
            self.sound.play_from_sd(song)
