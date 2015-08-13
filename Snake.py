import pygame
import random

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Snake")

myIcon = pygame.image.load('images/myIcon.png')
pygame.display.set_icon(myIcon)

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,150,0)
lightGreen = (0,255,0)
blue = (0,0,255)
orange = (230,92,0)
lightOrange = (255,165,5)

block_size = 10

clock = pygame.time.Clock()

img = pygame.image.load("images/snake.png")
ratImg = pygame.image.load("images/angryBird.png")


def displayScore(score):
    myFont = pygame.font.Font(None, 25)
    textSurface = myFont.render("Score: " + str(score), True, blue)
    gameDisplay.blit(textSurface, [0,0])


def message(msg,color,size,height=0):
    myFont = pygame.font.SysFont("arial",size)
    textSurface = myFont.render(msg, True, color)
    textRect = textSurface.get_rect()
    textRect.center = (display_width/2, display_height/2 + height)
    gameDisplay.blit(textSurface, textRect)


def snake(block_size, snakeList, headDirection):
    if headDirection == "right":
        head = pygame.transform.rotate(img, 270)
    elif headDirection == "left":
        head = pygame.transform.rotate(img, 90)
    elif headDirection == "up":
        head = img
    elif headDirection == "down":
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    for XnY in snakeList[:-1]:
        gameDisplay.fill(green, rect=[XnY[0],XnY[1],block_size,block_size])


def apple(randAppleX,randAppleY,block_size):
    gameDisplay.blit(ratImg, (randAppleX, randAppleY))


def pause():
    gamePaused = True
    message("Game Paused", green, 25)
    message("Press C to Play or Q to Quit.",black,20,50)
    pygame.display.update()
    while gamePaused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_c:
                    gamePaused = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

            clock.tick(5)

def button(msg, x, y, width, height, color, hoverColor):
    mousePos =  pygame.mouse.get_pos()
    mouseClick = pygame.mouse.get_pressed()
    print mouseClick

    if x <= mousePos[0] <= x+width and y <= mousePos[1] <= y+height:
        pygame.draw.rect(gameDisplay, hoverColor, [x,y,width,height])
        if mouseClick[0]== 1:
            if msg == "Quit":
                pygame.quit()
                quit()
            elif msg == "Play!!":
                gameLoop()
    else:
        pygame.draw.rect(gameDisplay, color, [x,y,width,height])

    myFont = pygame.font.SysFont("arial",25)
    textSurface = myFont.render(msg, True, black)
    textRect = textSurface.get_rect()
    textRect.center = (x + width/2, y + height/2)
    gameDisplay.blit(textSurface, textRect)


def gameIntro():
    intro = True

    gameDisplay.fill(white)
    message("Welcome to the Snake Game!!",green,25,-50)
    message("The objective of the game is to eat Birds",black,25)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_c:
                    intro = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Play!!", 200, 400, 100, 50, green, lightGreen)
        button("Quit", 500, 400, 100, 50, orange, lightOrange)

        pygame.display.update()
        clock.tick(5)


def gameLoop():
    gameExit = False
    gameOver = False
    lead_x = display_width / 2
    lead_y = display_height / 2
    change_x = 0
    change_y = 0
    direction = "right"

    score = 0
    score_inc = 10
    score_gap = 200

    fps = 10
    fps_change = 5

    randAppleX = random.randrange(0,display_width-block_size,block_size)
    randAppleY = random.randrange(0,display_height-block_size,block_size)

    snakeList = []
    snakeSize = 1

    while gameExit == False:
        while gameOver == True:
            message("Game Over!!", red,25)
            message("Press C to Continue or Q to Quit.", black,20,100)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
                elif event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False

            clock.tick(5)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    change_x = - block_size
                    change_y = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    change_x = block_size
                    change_y = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    change_x = 0
                    change_y = - block_size
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    change_x = 0
                    change_y = block_size
                elif event.key == pygame.K_SPACE:
                    pause()

        lead_x = lead_x + change_x
        lead_y = lead_y + change_y

        gameDisplay.fill(white)
        apple(randAppleX,randAppleY,block_size)

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)

        if snakeHead in snakeList:
            gameOver = True
        
        snakeList.append(snakeHead)
        snake(block_size, snakeList, direction)
        displayScore(score)

        pygame.display.update()
        clock.tick(fps)

        if lead_x < 0 or lead_x > display_width or lead_y < 0 or lead_y > display_height:
            gameOver = True

        if lead_x >= randAppleX and lead_x <= randAppleX + 20:
            if lead_y >= randAppleY and lead_y <= randAppleY + 20:
                snakeSize += 1
                score += score_inc
                score_gap = score_gap - score_inc
                if score_gap - score_inc < 0:
                    score_gap = 200
                    fps += fps_change
                randAppleX = random.randrange(0,display_width-block_size,10)
                randAppleY = random.randrange(0,display_height-block_size,10)
            else:
                snakeList.pop(0)
        else:
            snakeList.pop(0)

    pygame.quit()
    quit()


##Call to the gameIntro.
##GameIntro will in turn call gameLoop depending upon input.
gameIntro()
