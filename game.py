import pygame
import random
import sys
import time

def drawFloor():
    screen.blit(floorSurface, (floorXPosition, 900))
    screen.blit(floorSurface, (floorXPosition + 576, 900))

def createPipe():
    randomPipePosition = random.choice(pipeHeights)
    bottomPipe = pipeSurface.get_rect(midtop = (700, randomPipePosition))
    topPipe = pipeSurface.get_rect(midbottom = (700, randomPipePosition - 375))

    return bottomPipe, topPipe

def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5

    return pipes

def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipeSurface, pipe)
        else:
            flipPipe = pygame.transform.flip(pipeSurface, False, True)
            screen.blit(flipPipe, pipe)

def checkCollision(pipes):
    for pipe in pipes:
        if dogRectangle.colliderect(pipe):
            robertSound = str(random.choice(robertSounds))
            deathSound = pygame.mixer.Sound(f"sounds/{robertSound}")
            deathSound.play()
            return False

    if dogRectangle.top <= -100 or dogRectangle.bottom >= 900:
        return False

    return True

def rotateDog(dog):
    newDog = pygame.transform.rotozoom(dog, dogMovement * -2, 1)

    return newDog

def scoreDisplay(gameState):
    if gameState == "mainGame":
        scoreSurface = gameFont.render(str(int(score)), True, (255, 255, 255))
        scoreRectangle = scoreSurface.get_rect(center = (288, 100))
        screen.blit(scoreSurface, scoreRectangle)

    if gameState == "gameOver":
        scoreSurface = gameFont.render(f"Score: {str(int(score))}", True, (255, 255, 255))
        scoreRectangle = scoreSurface.get_rect(center=(288, 100))
        screen.blit(scoreSurface, scoreRectangle)

        highscoreSurface = gameFont.render(f"High score: {str(int(highscore))}", True, (255, 255, 255))
        highscoreRectangle = highscoreSurface.get_rect(center = (288, 850))
        screen.blit(highscoreSurface, highscoreRectangle)

def updateScore(score, highscore):
    if score > highscore:
        highscore = score

    return highscore

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1,  buffer = 512)
pygame.init()
pygame.display.set_caption("FlappyTara")
screen = pygame.display.set_mode((576, 1024)) # this sets the size format of the window
clock = pygame.time.Clock()
gameFont = pygame.font.Font('04B_19.TTF', 40)

gameIcon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(gameIcon)

# game variables
gravity = 0.25
dogMovement = 0
gameActive = True
score = 0
highscore = 0

hour = int(time.localtime().tm_hour)

if hour >= 20 and hour <= 5:
    backgroundSurface = pygame.image.load("assets/background-night.png").convert()  # this loads an image
    backgroundSurface = pygame.transform.scale2x(backgroundSurface)  # this scales up an image by 2 times
else:
    backgroundSurface = pygame.image.load("assets/background-day.png").convert()  # this loads an image
    backgroundSurface = pygame.transform.scale2x(backgroundSurface)  # this scales up an image by 2 times

floorSurface = pygame.image.load("assets/base.png").convert()
floorSurface = pygame.transform.scale2x(floorSurface)
floorXPosition = 0

dogSurface = pygame.image.load("assets/dog.png").convert_alpha()
dogRectangle = dogSurface.get_rect(center = (100, 512))

pipeSurface = pygame.image.load("assets/kurtos-pipes.png")
pipeSurface = pygame.transform.scale2x(pipeSurface)
pipeList = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

pipeHeights = [400, 600, 800]

gameOverSurface = pygame.image.load("assets/message.png").convert_alpha()
gameOverSurface = pygame.transform.scale2x(gameOverSurface)
gameOverRectangle = gameOverSurface.get_rect(center = (288, 512))

robertSounds = ["sfx_braila.wav", "sfx_lugoj.wav", "sfx_testamentul.wav", "sfx_satulBarateaz.wav", "sfx_samir.wav", "sfx_mediumRight.wav", "sfx_mediumLeft.wav", "sfx_concentrateSamir.wav"]

barkSound = pygame.mixer.Sound("sounds/sfx_bark.wav")
scoreSound = pygame.mixer.Sound("sounds/sound_sfx_point.wav")
scoreSoundCoundown = 100

while True:
    # here you can draw or add anything that will appear on the canvas

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # this verifies if you pressed the quit button
            pygame.quit()
            sys.exit() # here exits the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameActive == True:
                dogMovement = 0
                dogMovement -= 12
                barkSound.play()

            if event.key == pygame.K_SPACE and gameActive == False:
                gameActive = True
                pipeList.clear()
                dogRectangle.center = (100, 512)
                dogMovement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipeList.extend(createPipe())

    screen.blit(backgroundSurface, (0, 0)) # this shows the image on the main canvas, at the (0, 0) coordonates

    if gameActive:
        # dog movement
        dogMovement += gravity
        rotatedDog = rotateDog(dogSurface)
        dogRectangle.centery += dogMovement
        screen.blit(rotatedDog, dogRectangle)
        gameActive = checkCollision(pipeList)

        # pipes movement
        pipeList = movePipes(pipeList)
        drawPipes(pipeList)

        score += 0.01
        scoreDisplay("mainGame")
        scoreSoundCoundown -= 1
        if scoreSoundCoundown == 0:
            scoreSound.play()
            scoreSoundCoundown = 100
    else:
        screen.blit(gameOverSurface, gameOverRectangle)

        highscore = updateScore(score, highscore)
        scoreDisplay("gameOver")

    # floor movement
    floorXPosition -= 1
    drawFloor()
    if floorXPosition <= -576:
        floorXPosition = 0

    pygame.display.update() # this actually edits the canvas, what is above this line, it is actually a "frame"
    clock.tick(120) # this sets the framerate to 120 fps
