# gameinput Module
#imports pygame module, and joystick module
#source: https://magpi.raspberrypi.org/articles/code-pac-man-in-python
from pygame import joystick, key
from pygame.locals import *

joystick.init()
joystick_count = joystick.get_count()

if(joystick_count > 0):
    joyin = joystick.Joystick(0)
    joyin.init()

#defines variable p as player and assigns controlls to different variables
def checkInput(p):
    global joyin, joystick_count
    xaxis = yaxis = 0
    if joystick_count > 0:
        xaxis = joyin.get_axis(0)
        yaxis = joyin.get_axis(1)
    if key.get_pressed()[K_LEFT] or xaxis < -0.8:
        p.angle = 180
        p.movex = -20
    if key.get_pressed()[K_RIGHT] or xaxis > 0.8:
        p.angle = 0
        p.movex = 20
    if key.get_pressed()[K_UP] or yaxis < -0.8:
        p.angle = 90
        p.movey = -20
    if key.get_pressed()[K_DOWN] or yaxis > 0.8:
        p.angle = 270
        p.movey = 20    

#initialisez input function
# inside update() function

    if player.movex or player.movey:
        inputLock()
        animate(player, pos=(player.x + player.movex, player.y + player.movey), duration=1/SPEED, tween='linear', on_finished=inputUnLock)

# outside update() function

def inputLock():
    global player
    player.inputActive = False

def inputUnLock():
    global player
    player.movex = player.movey = 0
    player.inputActive = True

# gamemaps module
#inputs images, assignes direction and then reutrns direction
from pygame import image, Color
moveimage = image.load('images/pacmanmovemap.png')
dotimage = image.load('images/pacmandotmap.png')

def checkMovePoint(p):
    global moveimage
    if p.x+p.movex < 0: p.x = p.x+600
    if p.x+p.movex > 600: p.x = p.x-600
    if moveimage.get_at((int(p.x+p.movex), int(p.y+p.movey-80))) != Color('black'):
        p.movex = p.movey = 0

def checkDotPoint(x,y):
    global dotimage
    if dotimage.get_at((int(x), int(y))) == Color('black'):
        return True
    return False

def getPossibleDirection(g):
    global moveimage
    if g.x-20 < 0:
        g.x = g.x+600
    if g.x+20 > 600:
        g.x = g.x-600
    directions = [0,0,0,0]
    if g.x+20 < 600:
        if moveimage.get_at((int(g.x+20), int(g.y-80))) == Color('black'): directions[0] = 1
    if g.x < 600 and g.x >= 0:
        if moveimage.get_at((int(g.x), int(g.y-60))) == Color('black'): directions[1] = 1
    if g.x-20 >= 0:
        if moveimage.get_at((int(g.x-20), int(g.y-80))) == Color('black'): directions[2] = 1
    if g.x < 600 and g.x >= 0:
        if moveimage.get_at((int(g.x), int(g.y-100))) == Color('black'): directions[3] = 1
    return directions
#Creates game map
# gamemaps module
from pygame import image, Color
moveimage = image.load('images/pacmanmovemap.png')

def checkMovePoint(p):
    global moveimage
    if p.x+p.movex < 0: p.x = p.x+600
    if p.x+p.movex > 600: p.x = p.x-600
    if moveimage.get_at((int(p.x+p.movex), int(p.y+p.movey-80))) != Color('black'):
        p.movex = p.movey = 0
#creates player image and gives sets speed and entity images
def getPlayerImage():
    global player
    # we need to import datetime at the top of our code
    dt = datetime.now()
    a = player.angle
    # this next line will give us a number between
    # 0 and 5 depending on the time and SPEED
    tc = dt.microsecond%(500000/SPEED)/(100000/SPEED)
    if tc > 2.5 and (player.movex != 0 or player.movey !=0):
        # this is for the closed mouth images
        if a != 180:
            player.image = "pacman_c"
        else:
            # reverse image if facing left
            player.image = "pacman_cr"
    else:
        # this is for the open mouth images
        if a != 180:
            player.image = "pacman_o"
        else:
            player.image = "pacman_or"
    # set the angle on the player actor
    player.angle = a

def initDots():
    global pacDots
    pacDots = []
    a = x = 0
    while x < 30:
        y = 0
        while y < 29:
            if gamemaps.checkDotPoint(10+x*20, 10+y*20):
                pacDots.append(Actor("dot",(10+x*20, 90+y*20)))
                pacDots[a].status = 0
                a += 1
            y += 1
        x += 1

# This goes in the gamemaps module file.

dotimage = image.load('images/pacmandotmap.png')

def checkDotPoint(x,y):
    global dotimage
    if dotimage.get_at((int(x), int(y))) == Color('black'):
        return True
    return False

# This bit goes in the draw() function.

    pacDotsLeft = 0
    for a in range(len(pacDots)):
        if pacDots[a].status == 0:
            pacDots[a].draw()
            pacDotsLeft += 1
        if pacDots[a].collidepoint((player.x, player.y)):
            pacDots[a].status = 1
    # if there are no dots left, the player has won
    if pacDotsLeft == 0: player.status = 2

import pgzrun
import gameinput
import gamemaps
from random import randint
from datetime import datetime
WIDTH = 600
HEIGHT = 660

player = Actor("pacman_o") # Load in the player Actor image
SPEED = 3

def draw(): # Pygame Zero draw function
    global pacDots, player
    screen.blit('header', (0, 0))
    screen.blit('colourmap', (0, 80))
    pacDotsLeft = 0
    for a in range(len(pacDots)):
        if pacDots[a].status == 0:
            pacDots[a].draw()
            pacDotsLeft += 1
        if pacDots[a].collidepoint((player.x, player.y)):
            pacDots[a].status = 1
    if pacDotsLeft == 0: player.status = 2
    drawGhosts()
    getPlayerImage()
    player.draw()
    if player.status == 1: screen.draw.text("GAME OVER" , center=(300, 434), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=40)
    if player.status == 2: screen.draw.text("YOU WIN!" , center=(300, 434), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=40)

def update(): # Pygame Zero update function
    global player, moveGhostsFlag, ghosts
    if player.status == 0:
        if moveGhostsFlag == 4: moveGhosts()
        for g in range(len(ghosts)):
            if ghosts[g].collidepoint((player.x, player.y)):
                player.status = 1
                pass
        if player.inputActive:
            gameinput.checkInput(player)
            gamemaps.checkMovePoint(player)
            if player.movex or player.movey:
                inputLock()
                animate(player, pos=(player.x + player.movex, player.y + player.movey), duration=1/SPEED, tween='linear', on_finished=inputUnLock)

def init():
    global player
    initDots()
    initGhosts()
    player.x = 290
    player.y = 570
    player.status = 0
    inputUnLock()

def getPlayerImage():
    global player
    dt = datetime.now()
    a = player.angle
    tc = dt.microsecond%(500000/SPEED)/(100000/SPEED)
    if tc > 2.5 and (player.movex != 0 or player.movey !=0):
        if a != 180:
            player.image = "pacman_c"
        else:
            player.image = "pacman_cr"
    else:
        if a != 180:
            player.image = "pacman_o"
        else:
            player.image = "pacman_or"
    player.angle = a

def drawGhosts():
    for g in range(len(ghosts)):
        if ghosts[g].x > player.x:
            ghosts[g].image = "ghost"+str(g+1)+"r"
        else:
            ghosts[g].image = "ghost"+str(g+1)
        ghosts[g].draw()

def moveGhosts():
    global moveGhostsFlag
    dmoves = [(1,0),(0,1),(-1,0),(0,-1)]
    moveGhostsFlag = 0
    for g in range(len(ghosts)):
        dirs = gamemaps.getPossibleDirection(ghosts[g])
        if ghostCollided(ghosts[g],g) and randint(0,3) == 0: ghosts[g].dir = 3
        if dirs[ghosts[g].dir] == 0 or randint(0,50) == 0:
            d = -1
            while d == -1:
                rd = randint(0,3)
                if dirs[rd] == 1:
                    d = rd
            ghosts[g].dir = d
        animate(ghosts[g], pos=(ghosts[g].x + dmoves[ghosts[g].dir][0]*20, ghosts[g].y + dmoves[ghosts[g].dir][1]*20), duration=1/SPEED, tween='linear', on_finished=flagMoveGhosts)

def flagMoveGhosts():
    global moveGhostsFlag
    moveGhostsFlag += 1

def ghostCollided(ga,gn):
    for g in range(len(ghosts)):
        if ghosts[g].colliderect(ga) and g != gn:
            return True
    return False
    
def initDots():
    global pacDots
    pacDots = []
    a = x = 0
    while x < 30:
        y = 0
        while y < 29:
            if gamemaps.checkDotPoint(10+x*20, 10+y*20):
                pacDots.append(Actor("dot",(10+x*20, 90+y*20)))
                pacDots[a].status = 0
                a += 1
            y += 1
        x += 1

def initGhosts():
    global ghosts, moveGhostsFlag
    moveGhostsFlag = 4
    ghosts = []
    g = 0
    while g < 4:
        ghosts.append(Actor("ghost"+str(g+1) ,(270+(g*20), 370)))
        ghosts[g].dir = randint(0, 3)
        g += 1

def inputLock():
    global player
    player.inputActive = False

def inputUnLock():
    global player
    player.movex = player.movey = 0
    player.inputActive = True
    
init()
pgzrun.go()