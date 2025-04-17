import pygame
from pygame.locals import *
import random

# Initializing
pygame.init()
pygame.display.set_caption('BrekTris')
pygame.display.set_icon(pygame.image.load("../BrekTris/resources/egg.png"))

# Game Grid (0 = Nothing, 1 = Egg, 2 = Pancake, 3 = Waffle, 4 = Plate)
gridHeight, gridWidth = 16, 6
grid = [[0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [4, 4, 4, 4, 4, 4],
        ]
nextBlock = [0,0]

# Screen Constants
X_DISPLAY, Y_DISPLAY = 320, 480
BG_COLOR = (100, 100, 255)
color1 = (50, 50, 150)
colorYellow = (255, 255, 0)
colorDarkYellow = (150, 150, 0)

#Setting Screen and PNGs
surface = pygame.display.set_mode((X_DISPLAY, Y_DISPLAY), pygame.NOFRAME, pygame.SCALED)

egg = pygame.image.load("../BrekTris/resources/egg.png").convert_alpha()
waffle = pygame.image.load("../BrekTris/resources/waffle.png").convert_alpha()
pancake = pygame.image.load("../BrekTris/resources/pancake.png").convert_alpha()
plate = pygame.image.load("../BrekTris/resources/plate.png").convert_alpha()
endScreen = pygame.image.load("../BrekTris/resources/endscreen.png").convert_alpha()
x = pygame.image.load("../BrekTris/resources/x.png").convert_alpha()
check = pygame.image.load("../BrekTris/resources/check.png").convert_alpha()

# Time Variables
currentTick = 0
lastTick = 0
timeSinceLastTick = 0
DROP_TIME = 375
DROP_TIME_FAST = 100
dropFast = False

#Game Mechanics
numBlocks = 0
difficulty = 0
gameState = 0
updateGameState = 0

# Scoring
playerScore = 0
highScore = 0
newHighScore = False
lossTicks = 0

#Reads the high score from a text file called 'high_score.txt'
def get_high_score():
    high_score_file = open("../BrekTris/resources/high_score.txt", "r")
    high_score = int(high_score_file.read())
    high_score_file.close()

    return high_score


#Writes the highscore to 'high_score.txt'
def save_high_score(new_high_score):
    high_score_file = open("../BrekTris/resources/high_score.txt", "w")
    high_score_file.write(str(new_high_score))
    high_score_file.close()


#Draws Starting Menu
def updateMenu():
    surface.fill(BG_COLOR)

    Font1 = pygame.font.SysFont('system', 70)
    Font2 = pygame.font.SysFont('system', 25)
    Font3 = pygame.font.SysFont('system', 20)
    letterbreaktris1 = Font1.render("BREAKTRIS", False, colorDarkYellow)
    letterbreaktris2 = Font1.render("BREAKTRIS", False, colorYellow)
    letterpressanybutton1 = Font2.render("PRESS ANY BUTTON TO START", False, colorDarkYellow)
    letterpressanybutton2 = Font2.render("PRESS ANY BUTTON TO START", False, colorYellow)
    letterGuide = Font3.render("Press [G] to open guide.", False, colorYellow)


    surface.blit(letterbreaktris1,(8, 69))  # nice
    surface.blit(letterbreaktris2,(11, 72))
    surface.blit(letterpressanybutton1,(29, 389))
    surface.blit(letterpressanybutton2,(30, 390))
    surface.blit(letterGuide, (80, 410))
    
    surface.blit(plate,(95,300))
    surface.blit(plate,(145,300))
    surface.blit(plate,(195,300))
    surface.blit(egg,(95,299))
    surface.blit(egg,(145,297))
    surface.blit(waffle,(195,297))
    surface.blit(waffle,(95,282))
    surface.blit(waffle,(195,282))
    surface.blit(pancake,(145,277))
    surface.blit(pancake,(145,262))
    surface.blit(egg,(195,182))
    surface.blit(pancake,(145,182))


#Update Guide Menu
def updateGuide():
    surface.fill(BG_COLOR)

    Font1 = pygame.font.SysFont('system', 70)
    Font2 = pygame.font.SysFont('system', 20)
    Font3 = pygame.font.SysFont('system', 15)
    
    title1 = Font1.render("BREAKTRIS", False, colorDarkYellow)
    title2 = Font1.render("BREAKTRIS", False, colorYellow)

    instructions1 = Font3.render("During the game food will fall from", False, colorYellow)
    instructions11 = Font3.render("the top of the screen in pairs.", False, colorYellow) 
    instructions2 = Font3.render("Matching 3 like food will make them disappear", False, colorYellow)
    instructions21 = Font3.render("and add 10 points to your score.", False, colorYellow)
    instructions3 = Font3.render("If the food stacks too high you will lose the game.", False, colorYellow)

    controls1 = Font3.render("[RightArrow] = Move Food Left", False, colorYellow)
    controls2 = Font3.render("[LeftArrow] = Move Food Right", False, colorYellow)
    controls3 = Font3.render("[UpArrow] = Flip Food Position", False, colorYellow)
    controls4 = Font3.render("[DownArrow] = Toggle Fast Drop", False, colorYellow)

    pressanybutton = Font2.render("Press [Esc] to return to menu.", False, colorYellow)

    #Text
    surface.blit(title1,(8, 69))
    surface.blit(title2,(11, 72))

    surface.blit(instructions1,(75,135))
    surface.blit(instructions11,(87,148))
    surface.blit(instructions2,(45,170))
    surface.blit(instructions21,(87,183))
    surface.blit(instructions3,(40,205))
    surface.blit(controls1,(80,350))
    surface.blit(controls2,(80,362))
    surface.blit(controls3,(80,374))
    surface.blit(controls4,(80,386))

    surface.blit(pressanybutton, (70, 410))

    #Diagrams
    surface.blit(egg,(96,290))
    surface.blit(egg,(96,275))
    surface.blit(egg,(96,260))
    surface.blit(check,(96,237))

    surface.blit(waffle,(193,290))
    surface.blit(egg,(193,280))
    surface.blit(waffle,(193,260))
    surface.blit(x,(193,240))

# Draws the UI when called
def updateUI():
    surface.fill(BG_COLOR)

    pygame.draw.rect(surface, color1, pygame.Rect(0, 0, 320, 40))
    pygame.draw.rect(surface, color1, pygame.Rect(0, 0, 108, 120))
    pygame.draw.rect(surface, color1, pygame.Rect(212, 0, 320, 120))
    pygame.draw.rect(surface, colorYellow, pygame.Rect(0, 170, 320, 2))


    if(nextBlock[0] == 1):
        surface.blit(egg, (120,60))
    elif(nextBlock[0] == 2):
        surface.blit(pancake, (120,60))
    elif(nextBlock[0] == 3):
        surface.blit(waffle, (120,60))

    if(nextBlock[1] == 1):
        surface.blit(egg, (165,60))
    elif(nextBlock[1] == 2):
        surface.blit(pancake, (165,60))
    elif(nextBlock[1] == 3):
        surface.blit(waffle, (165,60))

    Font = pygame.font.SysFont('commando', 30)
    letter1 = Font.render("SCORE " + "{:04d}".format(playerScore), False, colorYellow)
    letter2 = Font.render("NEXT", False, colorYellow)
    letter3 = Font.render("BLOCK", False, colorYellow)
    letter4 = Font.render("LEVEL", False, colorYellow)
    letter6 = Font.render("{:03d}".format(difficulty + 1), False, colorYellow)
    letter7 = Font.render("HIGH " + "{:04d}".format(highScore), False, colorYellow)

    surface.blit(letter1, (10, 12))
    surface.blit(letter2, (30, 60))
    surface.blit(letter3, (20, 80))
    surface.blit(letter4, (238, 60))
    surface.blit(letter6, (252, 80))
    surface.blit(letter7, (210, 12))


# Draws the end screen after death
def updateEndScreen():

    Font1 = pygame.font.SysFont('system', 35)
    Font2 = pygame.font.SysFont('commando', 20)
    Font3 = pygame.font.SysFont('system', 80)

    surface.blit(endScreen, (0,0))
    surface.blit(Font3.render("You Lost", False, colorYellow), (40, 40))

    surface.blit(Font1.render("Highscore:  " + "{:04d}".format(highScore), False, colorYellow), (60, 110))
    if(playerScore < highScore):
        surface.blit(Font1.render("Your Score: " + "{:04d}".format(playerScore), False, colorYellow), (60, 135))
    elif(playerScore >= highScore):
        surface.blit(Font1.render("New Highscore!!!", False, colorYellow), (59, 135))

    surface.blit(Font2.render("Press [Esc] to return to menu.", False, colorYellow), (65, 410))
    surface.blit(Font2.render("Press any button to restart game.", False, colorYellow), (55, 390))


# Returns a number 1-3
def getRandomNum():
    return random.randrange(1, 4)


#Next Blocks up in queue
def getNewBlocks():
    nextBlock[0] = getRandomNum()
    nextBlock[1] = getRandomNum()


def newBlocksToGrid():
    grid[0][2] = nextBlock[0]
    grid[0][3] = nextBlock[1]   


# Draws the grid to the screen in order from bottom to top
def drawBlocks():
    i = gridHeight - 1
    while i >= 0:
        j = 0
        while j < gridWidth:
            if grid[i][j] == 1:
                surface.blit(egg, (5 + ((j + 1) * 32) + ((j - 1) * 18), 150 + ((i * 20))))
            if grid[i][j] == 2:
                surface.blit(pancake, (5 + ((j + 1) * 32) + ((j - 1) * 18), 150 + ((i * 20))))
            if grid[i][j] == 3:
                surface.blit(waffle, (5 + ((j + 1) * 32) + ((j - 1) * 18), 150 + ((i * 20))))
            if grid[i][j] == 4:
                surface.blit(plate, (5 + ((j + 1) * 32) + ((j - 1) * 18), 138 + ((i * 20))))
            j += 1
        i -= 1
    

# Drops all blocks on the screen
def dropBlocks():
    i = gridHeight - 1
    while i >= 1:
        j = 0
        while j < gridWidth:
            if grid[i][j] == 0 and grid[i - 1][j] != 0:
                grid[i][j] = grid[i - 1][j]
                grid[i - 1][j] = 0
            j += 1
        i -= 1


# Moves both the blocks to the left
def moveLeft():
    i = 0
    while i < gridHeight:
        j = 0
        while j < gridWidth:
            if (j != 0) and (grid[i][j] == 1 or grid[i][j] == 2 or grid[i][j] == 3) and (grid[i][j - 1] == 0) and (
            grid[i + 1][j]) == 0:
                grid[i][j - 1] = grid[i][j]
                grid[i][j] = 0
            j += 1
        i += 1


# Moves both the blocks to the right
def moveRight():
    i = 0
    while i < gridHeight:
        j = gridWidth - 1
        while j >= 0:
            if (j != gridWidth - 1) and (grid[i][j] == 1 or grid[i][j] == 2 or grid[i][j] == 3) and (
                    grid[i][j + 1] == 0) and (grid[i + 1][j]) == 0:
                grid[i][j + 1] = grid[i][j]
                grid[i][j] = 0
            j -= 1
        i += 1


# Changes the moving blocks positions
def switchBlocks():
    i = 0
    while i < gridHeight:
        j = 0
        while j < gridWidth - 1:
            if (grid[i][j] == 1 or grid[i][j] == 2 or grid[i][j] == 3):
                if (grid[i + 1][j] == 0 and grid[i][j + 1] != 0):
                    temp = grid[i][j]
                    grid[i][j] = grid[i][j + 1]
                    grid[i][j + 1] = temp
            j += 1
        i += 1


# Detect if all the blocks are not moving
def detectNewBlocks():
    i = 0
    while i < gridHeight - 1:
        j = 0
        while j < gridWidth:
            if (grid[i][j] == 1 or grid[i][j] == 2 or grid[i][j] == 3) and grid[i + 1][j] == 0:
                return False
            j += 1
        i += 1
    return True


# Detects collision between the blocks and detect if there are more than three stacked
def detectCollision(playerScore):
    i = 0
    while i < gridHeight - 2:
        j = 0
        while j < gridWidth:
            if (grid[i][j] != 0) and (grid[i + 1][j] == grid[i][j]) and (grid[i + 2][j] == grid[i][j]):
                grid[i + 2][j] = 0
                grid[i + 1][j] = 0
                grid[i][j] = 0
                playerScore += 10
            j += 1
        i += 1
    return playerScore


#Returns an empty Grid
def resetGrid():
    return [[0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [4, 4, 4, 4, 4, 4],
        ]


# MAIN GAME LOOP
gameState = 1
highScore = get_high_score()

while gameState != 0:
    # BEFORE GAME MENU
    if (gameState == 1):  #main menu
        updateMenu()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    gameState = 0
                    updateGameState = 1
                if event.key == K_g:
                    gameState = 4
                    updateGameState = 1
                if (event.key != pygame.K_ESCAPE) and (updateGameState == 0):
                    getNewBlocks()
                    newBlocksToGrid()
                    gameState = 2  

    # GUIDE SCREEN
    if (gameState == 4):  #how to play
        updateGuide()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    gameState = 1  
                    updateGameState = 0 

    # DURING GAME STUFF
    if (gameState == 2):  #Main game
        # Detect the amount of time since the last time the block has dropped
        lastTick = currentTick
        currentTick = pygame.time.get_ticks()
        timeSinceLastTick += (currentTick - lastTick)

        # Detect and use inputs
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    gameState = 0
                if event.key == K_LEFT:
                    moveLeft()
                if event.key == K_RIGHT:
                    moveRight()
                if event.key == K_DOWN:
                    if (dropFast):
                        dropFast = False
                    else:
                        dropFast = True
                if event.key == K_UP:
                    switchBlocks()

        if (dropFast and (timeSinceLastTick >= 50)) or (timeSinceLastTick >= 1000 / (2 * (difficulty + 1))):
            timeSinceLastTick = 0
            dropBlocks()

            if grid[0][2] != 0 or grid[0][3] != 0:
                lossTicks += 1
            if (lossTicks >= 1):
                gameState = 3
                lossTicks = 0

        if detectNewBlocks():
            newBlocksToGrid()
            getNewBlocks()
            dropFast = False
            numBlocks += 1
            if numBlocks >= 10:
                numBlocks = 0
                difficulty += 1

        # Updating Screen
        updateUI()
        drawBlocks()
        playerScore = detectCollision(playerScore)

        if (playerScore > highScore):
            highScore = playerScore
            save_high_score(highScore)
            newHighScore = True

    # AFTER GAME STUFF
    if (gameState == 3):  #Death Screen
        updateEndScreen()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    gameState = 1
                    difficulty = 0
                    grid = resetGrid()
                    getNewBlocks()
                    newBlocksToGrid()
                if event.key != pygame.K_ESCAPE:
                    playerScore = 0
                    gameState = 2
                    grid = resetGrid()
                    getNewBlocks()
                    newBlocksToGrid()
                    difficulty = 0
    
    pygame.display.flip()