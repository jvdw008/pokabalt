# Copyright 2020 by Blackjet
# Graphics done using Aseprite
# Sfx done using BFXR and Audacity
# Code, music, sfx, graphics by Jaco van der Walt

# The source code in this file is released under the GNU GPL V3 license.
# Go to https://choosealicense.com/licenses/gpl-3.0/ for the full license details.

import upygame as pygame
import urandom as random
import umachine                             # For on-screen text
import graphics		                        # Graphics
import sounds                               # Sfx
from audio import Audio                     # Audio class to play sounds
from background import Background           # Background (aquarium)
from player import Player                   # Player class
from animation import Animation as Anim     # Animation cass for fish, coins, player etc
from shake import Shake                     # Screen shake
from buildings import Building              # Create building objects
from objects import Object                  # boxes/bombs etc
from pigeons import Pigeon                  # Birds, obvs

# Game specific imports below

# Check RAM use
import gc
gc.collect()

# Setup the screen buffer
pygame.display.init(False)

# Set colours in RGB formatted tuples
pygame.display.set_palette_16bit([
    000000, 0xffff, 0xad77, 0x8432, 0x5b2e, 0x52cd, 0x4a4b, 0x31a7, 0x0000, 0xf800, 0x9000, 0x0020, 0xa554
    
]);

# default mode of 110x88 @16 cols
screen = pygame.display.set_mode()

# Init audio
g_sound = pygame.mixer.Sound()

# Test for real h/w to prevent simulator from hanging
gpioPin = umachine.Pin ( umachine.Pin.EXT2, umachine.Pin.ANALOG_IN )
gpioPinValue = gpioPin.value()
if(gpioPinValue == 0):
    isThisRealHardware = False
    gameSong = ""
else:
    isThisRealHardware = True
    gameSong = "music/pokabalt.wav"

# Version number of current game build
version = 20

# States
STATE_MENU = 1
STATE_GAME = 2
STATE_PAUSE = 3
STATE_GAMEOVER = 4

######################################
# Variables
######################################
waitOnLoad = 50                 # Use this to prevent A starting the game before player
gameState = STATE_MENU          # Menu or game
gameOver = False
startGame = False               # Boolean for starting the game
showInstructions = False        # For showing instructions on menu screen
level = 1                       # The level of the game
score = 0                       # Player score
scoreCtr = 0                    # Used to count the framerate and update score 
playerPos = []                  # Player position
playerX = 5
playerY = 0
deathReason = ["a wall", "a pavement", "a bomb", "a deadend"] # How you died
deathCause = ""
playerHeight = 16               # For hit detection
playerWidth = 11
upPressed = False               # Modifiers for dpad
downPressed = False             # As above
aPressed = False                # As above
bPressed = False                # As above
cPressed = False                # As above
highscore = 500                 # Default highscore
shakeY = 0
gravity = 5                     # Strength of gravity - affects player and dropped objects like bombs
bombDrop = False
bombPos = [0, 0, 0]             # x, y, visibility
bombTimer = 100                 # Frequency of drops
scrollSpeed = 3                 # Start scroll speed of runner
buildingList = []               # Building objects (should never be more than 3 on screen anyway)
objectList = []                 # List of objects on screen - boms, boxes etc
pigeonList = []                 # List of birds
monsterPos = [110, 3, False, 30 + random.getrandbits(4)]# Monster x/y pos, shooting bool and shooting timer
smokePos = [50, 0, 5]           # Smoke plume, smoke speed
scoreSaved = False
gameOverY = -88                 # Start pos for game over bg pos
sfxPlaying = False              # Used for checking sfx is playing
sfxTimer = 23                   # Timer for sfx

# Init classes
player = Player(playerX, playerY, playerHeight)
audio = Audio(g_sound, isThisRealHardware)
shake = Shake()

# Animation setup - Array of graphic images and the speed of the animation (lower = faster)
playerAnim = Anim([graphics.g_player.man01, graphics.g_player.man02, graphics.g_player.man03, graphics.g_player.man04], 1)
birdAnimList = []

######################################
# Sprites, images, objects
######################################
logo = graphics.g_logo.logo
gameBg = graphics.g_background.gameBg
gameBg2 = graphics.g_background.gameBg2
gameOverBg = graphics.g_background.gameOver
floors = [graphics.g_tiles.floor01, graphics.g_tiles.floor02, graphics.g_tiles.floor03, graphics.g_tiles.floor04]
walls = [graphics.g_tiles.wall01, graphics.g_tiles.wall02, graphics.g_tiles.wall03, graphics.g_tiles.wall04]
windows = [graphics.g_tiles.window01, graphics.g_tiles.window02]
buildingBg = [graphics.g_tiles.bg01, graphics.g_tiles.bg02, graphics.g_tiles.bg03]
bomb = graphics.g_tiles.bomb
blocks = [graphics.g_tiles.block01, graphics.g_tiles.block02]
pigeonImg = graphics.g_pigeon.bird00
birdAnimImages = [graphics.g_pigeon.bird01, graphics.g_pigeon.bird02, graphics.g_pigeon.bird03, graphics.g_pigeon.bird04]
monsterImg = graphics.g_tiles.monster
smoke = graphics.g_tiles.smoke

######################################
# Start music
######################################
audio.playMusic(gameSong)

# Initialize the cookie.
myCookieDataSize = 10
myCookieData = bytearray(myCookieDataSize)
myCookie = umachine.Cookie("pokabalt", myCookieData)

######################################
# save/load highscore to EEPROM
######################################
def updateScore(action, val):
    if action == "save":
        data =  val.to_bytes(3,'big')
        for i in range(len(data)): myCookieData[i]=data[i]
        
        # Save myCookieData to EEPROM.
        myCookie.save()
        
    if action == "load":
        # Load myCookieData from EEPROM.
        myCookie.load()
        
        # Parse the scores and the names from myCookieData.
        pos = 0
        highscr, pos = getIntFromByteArray(myCookieData, 0, 3)
        return highscr
        
# Gets a fixed size string from a byte array 
def getStringFromByteArray(dataBuf, pos, length):
    data = bytearray(length)
    for i in range(length): data[i]=dataBuf[i+pos]
    return str(data, "utf-8"), pos+length

# Gets an integer from a byte array 
def getIntFromByteArray(dataBuf, pos, length):
    data = bytearray(length)
    for i in range(length): data[i]=dataBuf[i+pos]
    return int.from_bytes(data, 'big'), pos+length
		
######################################
# Center text
######################################
def centerText(text, yPos, col):
    fontWidth = 7
    tmpText = text
    width = len(tmpText)
    screenWidth = 15    # Max chars
    leftPos = screenWidth - width
    leftPos *= fontWidth // 2
    #print (str(leftPos) + " " + str(screenWidth) + " " + str(width))
    umachine.draw_text(leftPos + 12, yPos, str(tmpText), col)

######################################
# Detect hitboxes
# onject x/y is single pixel that must be inside the "zone" to be a hit
######################################
def detectHit(objX, objY, targetX, targetY, obSize, targetSize): #x1, y1, x2, y2, size
    if objX + (obSize // 2) > targetX and objX + (obSize // 2) < targetX + targetSize[0]:
        if objY + obSize > targetY and objY + obSize < targetY + targetSize[1]:
            #print ("x: " + str(objX) + " y: " + str(objY) + " tX: " + str(targetX) + " tY: " + str(targetY) + " objSize: " + str(obSize) + " tSize: " + str(targetSize))
            return True
            
    return False
    
######################################
# Detect jump hits
######################################
def detectPlatform(objX, objY, targetX, targetY, targetSize): #x1, y1, x2, y2, size
    if objX > targetX and objX < targetX + targetSize:
        if objY >= targetY:
            return True
            
    return False

######################################
# Generate a new building in the matrix
######################################
def drawNewBuilding(x, theScore):
    global buildingList, objectList, scrollSpeed, bomb, walls, pigeonList
    
    startX = x
    startY = random.getrandbits(5) + 30
    if startY > 70:
        startY = 70
    
    wallId = random.getrandbits(3) + 1
    
    if wallId > 3:
        wallId = 3
        
    buildingLength = ((random.getrandbits(3) + 1) * 3) + 2
    if buildingLength < 10:
        buildingLength = 10
        wallId = 0
        
    spacing = random.getrandbits(2) + 1
    
    # Do we need birds
    if buildingLength > 15 and random.getrandbits(7) > 100:
        ctr = 4
        for bird in pigeonList:
	        bird.reset(startX + ctr + 20 + (spacing * 8), startY - 6)
	        ctr += 7
    
    floorId = random.getrandbits(3)
    if floorId > 3:
        floorId = 3
    
    # Create a box or bomb if building is long enough and not the first building
    if theScore > 100:
        # Don't do this on first building
        if x != 0:
            objType = random.getrandbits(1)

            if buildingLength > 15:
                if random.getrandbits(3) > 5:
                    # Crate
                    if objType == 0:
                        objectList.append(Object(blocks, startX + (buildingLength * 8) // 2, startY, objType, 14, 14))
                
                    # Bomb
                    else:
                        objectList.append(Object(bomb, startX + ((buildingLength - 3) * 8), startY, objType, 18, 11))
    
    windowId = random.getrandbits(1)
    
    if x == 0:
        spacing = 0
        
    buildingList.append(Building(startX, startY, buildingLength, spacing, floorId, wallId, windowId))

######################################
# Reset game to start
######################################
def reset():
	global scoreCtr, score, shakeY, bombDrop, bombPos, bombTimer, aPressed, cPressed, buildingList, scrollSpeed
	global player, playerY, gravity, playerHeight, gameOverY, objectList, pigeonList, smokePos, sfxPlaying, sfxTimer
	
	aPressed = False
	cPressed = False
	score = 0                       # Player score
	scoreCtr = 0                    # Used to count the framerate and update score 
	shakeY = 0
	shake.resetShake()
	buildingList = []
	objectList = []
	for bird in pigeonList:
	    bird.reset(120, -10)
	    
	scrollSpeed = 3
	player.setPlayerPos(playerY)
	player.setState(2)
	gameOverY = -88
	smokePos = [random.getrandbits(6), 0, 5]   # Reset smoke plume
	
	drawNewBuilding(0, 100)             # Set to first building
	
	sfxPlaying = False
	sfxTimer = 23
	
	gc.collect()
	
######################################
# Load the highscore if exists
######################################
tHighscore = updateScore("load", highscore)
if tHighscore > highscore:
    highscore = tHighscore

######################################
# Let's instantiate birds
######################################
for i in range(10):
    pigeonList.append(Pigeon(120, -10, pigeonImg))
    # Create anim
    birdAnimList.append(Anim(birdAnimImages, 1))

#print ("free",gc.mem_free())

######################################
# Update states
######################################
def updateGame():
    global gameState, scoreCtr, score, shakeY, bombDrop, bombPos, bombTimer, aPressed, cPressed, buildingList, scrollSpeed, monsterPos, smokePos, sfxPlaying, sfxTimer
    global gravity, playerHeight, playerWidth, deathReason, deathCause, objectList, playerAnim, waitOnLoad, pigeonList, birdAnimList, birdAnimImages
    
    playerState = player.getState()
    isPlayerDead = False
    buildingYPos = 0
    playerX = player.getPlayerPos()[0]
    playerY = player.getPlayerPos()[1]
    
    # Speed game up over time
    if scoreCtr % 250 == 0:
	    if scrollSpeed < 7:
	        scrollSpeed += 1
	        playerAnim.increaseAnimSpeed(1)
	
	# Update the score for player survival
	######################################
    scoreCtr += 1
    if scoreCtr % 5 == 0:
		score += scrollSpeed
		
    # Make sure player gravity kicks in if player not standing on a building and not jumping
    ######################################
    if len(buildingList) > 0:
	    if playerY + playerHeight < buildingList[0].getYPos() and playerState != 1:
	        player.setState(2)
	        
	# Is player running?
	######################################
    if playerState == 0:
        # Update player
        playerAnim.update()
        
        # Is player too low on screen
        ######################################
        if playerY +playerHeight > 85:
            isPlayerDead = True
            deathCause = deathReason[3]
        
        if aPressed:
            player.setState(1)  # Jump
            playerState = 1
        
    elif playerState == 1:
        # Jump
        player.updateJump(aPressed, gravity)
        
    else:
        # Fall
        isPlayerDead = player.updateFall(85) #70
        deathCause = deathReason[1]

	# Update other things
	######################################
    buildId = 0
    buildCtr = 0
    for building in buildingList:
        buildCtr +=1
        buildingLeft = building.getXPos()
        buildingRight = building.getRightMostX()
        buildingHeight = building.getYPos()    # player sprite height
        
        if playerX >= buildingLeft and playerX < buildingRight:
            # Has player landed?
            ######################################
            if playerState == 2:    # falling
                if playerY + playerHeight >= buildingHeight:
                    player.reset(gravity, buildingHeight, playerHeight)
                    break
            
            # If not jumping but inside building, then die
            ######################################
            if playerState < 2:
                if playerY + 8 >= buildingHeight:
                    isPlayerDead = True
                    deathCause = deathReason[0]
                    break
        
        # Update building
        ######################################
        isMovementComplete = building.update(scrollSpeed)
        if isMovementComplete:
	        buildId = buildCtr
	        break
            
    if buildId > 0:
	    del buildingList[buildId - 1]
	    gc.collect()
	    
	# Draw new building    
	######################################
    if len(buildingList) > 0:
        if buildingList[len(buildingList) - 1].getRightMostX() < 96:
            drawNewBuilding(110, score)
            
        # Check building coming up for shake and crumble
        ######################################
        if len(buildingList) > 1:
            if abs(buildingList[1].getRightMostX() - buildingList[1].getXPos()) // 8 <= 10:
                # Set building shake
                ######################################
                if not shake.isShaking():
                    if buildingList[1].getXPos() < 70:
                        shake.setShake()
                        
                # Play earthquake
                ######################################
                if not sfxPlaying:
                    audio.playSfx(sounds.earthquakeSnd)
                    sfxPlaying = True
                else:
                    # Countdown timer
                    if sfxTimer > 0:
                        sfxTimer -= 1
                    else:
                        sfxTimer = 23
                        sfxPlaying = False
	        
    ######################################
    # Update objects
    ######################################
    objCtr = 0
    objId = 0
    for obj in objectList:
        objCtr += 1
        obj.update(scrollSpeed, buildingList[len(buildingList) - 1].getYPos())
        
        # Shake when bomb lands
        ######################################
        if obj.getType() == 1 and obj.hasLanded() and not shake.isShaking():
            if obj.getPosition()[0] > 0 and obj.getPosition()[0] < 110:
                shake.setShake()
                # Play sfx
                audio.playSfx(sounds.bombSnd)
            
        # Check if player has hit it
        ######################################
        if detectHit(playerX, playerY, obj.getPosition()[0], obj.getPosition()[1], playerWidth, obj.getSize()) and not obj.getHit():
            obj.setHit()
            if obj.getType() == 0:
                # Play sound
                audio.playSfx(sounds.crateSnd)
                # Slow scrollSpeed
                ######################################
                if scrollSpeed > 1:
                    scrollSpeed -= 1
                    break
            else:
                # Kill player, as he hit bomb
                ######################################
                isPlayerDead = True
                deathCause = deathReason[2]
                break
            
    if objId > 0:
        del objectList[objId - 1]
        gc.collect()
	    
    ######################################
    # Update pigeons
    ######################################
    for bird in pigeonList:
        bird.update(scrollSpeed)
        # Check if bird is flying 
        if bird.getStatus():
            if not bird.getAnim():
                # Then set anim state
                bird.setAnim()
                
            # Check if out of screen to reset
            if bird.getPosition()[0] < -10 or bird.getPosition()[1] < - 10:
                bird.reset(120, -10)
    
    ######################################
    # bird anim
    ######################################
    if len(birdAnimList) > 0:
        for anim in birdAnimList:
            anim.update()
    
    ######################################
    # Update monster and actions
    ######################################
    if monsterPos[0] > -33:
        # Move left
        if random.getrandbits(7) > 120:
            monsterPos[0] -= 1
    else:
        # Reset position
        monsterPos[0] = 110 + random.getrandbits(4)
        
    if random.getrandbits(7) > 100:
        if random.getrandbits(1) == 1 and not monsterPos[2]:
            monsterPos[2] = True
            
    ######################################
    # Monster is shooting
    ######################################
    if monsterPos[2]:
        # Countdown shooting timer
        if monsterPos[3] > 0:
            monsterPos[3] -= 1
        else:
            # Reset shooting counter
            monsterPos[2] = False
            monsterPos[3] = 30 + random.getrandbits(4)
    
    ######################################
    # Update smoke plume
    ######################################
    if smokePos[1] > - 88:
        if smokePos[2] > 0:
            smokePos[2] -= 1
        else:
            smokePos[1] -= 1
            smokePos[2] = 5
    else:
        # Reset smoke plume
        smokePos[0] = monsterPos[0] - 40
        smokePos[1] = 50
    
    ######################################
    # Player has died
    ######################################
    if isPlayerDead:
        #print ("game over" + str(scoreCtr))
        gameState = STATE_GAMEOVER
        waitOnLoad = 50 # Add pause before player can press key
	
    if cPressed:
	    cPressed = False
	    gameState = STATE_PAUSE
    
######################################
# Pause state
######################################
def pauseGame():
    global gameState, aPressed
    
    if aPressed:
        aPressed = False
        gameState = STATE_GAME
        gc.collect()
      
######################################
# Game over state
######################################
def gameOverGame():
    global score, highscore, gameOverY, scoreSaved
    
    # Keep moving gameover gb down until fully exposed
    ######################################
    if gameOverY < -3:
        gameOverY += 3
    
    # Has player beat highscore?
    ######################################
    if score > highscore:
        if scoreSaved == False:
            updateScore("save", score)
            scoreSaved = True
            highscore = score
	else:
	    scoreSaved = False

######################################
# Render state
######################################
def render():
	
	######################################
	# Menu state
	######################################
	if gameState == STATE_MENU:
		# Logo
		screen.blit(logo, 0, 0 + shakeY)

		# Version
		modV = version % 10
		umachine.draw_text(83, 80, "v" + str(version // 10) + "." + str(modV), 2)

		# Info
		centerText("Use A to jump", 25, 3)
		
		# Text
		centerText("A: Start game", 35, 9)
		centerText("C: Pause game", 45, 9)

		# Scores
		centerText("Best distance:", 60, 2)
		centerText(str(highscore) + " meters", 70, 1)
	
	######################################
	# Game state
	######################################
	elif gameState == STATE_GAME:
	    
	    # Distant bg
	    screen.blit(gameBg2, 0, 5 + shakeY)
	    
	    # Smoke plume
	    if smokePos[0] > -32:
	        screen.blit(smoke, smokePos[0], smokePos[1] + shakeY)
	    
	    # Draw monster
	    screen.blit(monsterImg, monsterPos[0], monsterPos[1] + shakeY)
	    # And lasers
	    if monsterPos[2]:
	        pygame.draw.line(monsterPos[0] + 15, monsterPos[1] + 2 + shakeY, monsterPos[0] - 20, monsterPos[1] + 50 + shakeY, 3)
	        pygame.draw.line(monsterPos[0] + 15, monsterPos[1] + 2 + shakeY, monsterPos[0] - 40, monsterPos[1] + 40 + shakeY, 3)
	    
	    # Game bg
	    screen.blit(gameBg, 0, -10 + shakeY)
	    
	    # Draw buildings
		######################################
	    for building in buildingList:
	        building.drawBuilding(screen, floors, windows, walls, shakeY)
		
		# Display score
		######################################
	    umachine.draw_text(0, 1, str(score) + "m", 1)
	    
	    # Draw player anim
		######################################
	    playerAnim.draw(screen, player.getPlayerPos()[0], player.getPlayerPos()[1], shakeY)
	    
	    # Draw objects
	    for obj in objectList:
	        obj.draw(screen, shakeY)
	        
	        
	    # Draw pigeons
	    for bird in pigeonList:
	        if not bird.getStatus():
	            # Static sitting bird
	            bird.draw(screen, shakeY)
	        else:
        		# Anim birds
        		for anim in birdAnimList:
        		    anim.draw(screen, bird.getPosition()[0], bird.getPosition()[1], 0)
		    
	######################################
    # Pause state
    ######################################
	elif gameState == STATE_PAUSE:
	    centerText("Paused", 30, 1)
	    centerText("A: Continue", 50, 9)
	
	######################################
    # Game over state
    ######################################
	elif gameState == STATE_GAMEOVER:
	    screen.blit(gameOverBg, 0, gameOverY)
	    
	    centerText("Game over", 10, 1)
	    centerText("You reached:", 20, 1)
	    centerText(str(score) + " meters", 38, 1)
	    centerText("until you hit", 48, 1)
	    centerText(str(deathCause), 58, 1)
	    centerText("A: Menu", 78, 9)
    
# Main loop
while True:
    if waitOnLoad > 0:
        waitOnLoad -= 1
    else:
        # Mix random up
        random.getrandbits(7)
        
        eventtype = pygame.event.poll()
        
        if eventtype != pygame.NOEVENT:

					# Keydown events
			if eventtype.type == pygame.KEYDOWN:
				if (eventtype.key == pygame.BUT_A):
					if gameState == STATE_GAME:
					    aPressed = True

					if gameState == STATE_MENU:
						gameState = STATE_GAME
						reset()
						shake.setShake()
						audio.playSfx(sounds.earthquakeSnd)
					
					if gameState == STATE_GAMEOVER:
					    gameState = STATE_MENU
					    
					if gameState == STATE_PAUSE:
					    gameState = STATE_GAME
						
				if (eventtype.key == pygame.BUT_C):
				    cPressed = True
				    

			# Keyup events
			if eventtype.type == pygame.KEYUP:
				if (eventtype.key == pygame.BUT_A):
					aPressed = False
					
				if (eventtype.key == pygame.BUT_C):
					cPressed = False

	# Get screen shake amount (use on all x positions of objects!)
	######################################
    shakeY = shake.update()
    
    if gameState == STATE_GAME:
	    updateGame()
	    screen.fill(2)
	    
    if gameState == STATE_PAUSE:
	    pauseGame()
	    screen.fill(0)
	    
    if gameState == STATE_GAMEOVER:
	    gameOverGame()
	    screen.fill(0)
	
	# Render classes/objects
    render()

	# Sync screen
    pygame.display.flip()
