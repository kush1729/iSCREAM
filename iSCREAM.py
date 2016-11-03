import pygame
from time import sleep, time
pygame.init()

#COLOURS------------------------
white = (255, 255, 255)
black = (0, 0, 0)
snow = (255, 250, 250)
light_blue = (0, 255, 255)
med_blue = (100, 100, 200)
yellow = (255, 255, 0)
red = (255, 0, 0)
orange = (255, 200, 0)
light_red = (255, 100, 0)
chocolate = (210, 105, 30)
green = (34, 177, 76)
light_green = (0, 255, 0)
#-------------------------------

FPS = 40
numRows = 17
numCols = 17
wall_loc = [(0, x) for x in range(numCols)] + [(x, 0) for x in range(numRows)]
wall_loc += [(numRows - 1, x) for x in range(numCols)] + [(x, numCols - 1) for x in range(numRows)]
wall_loc = list(set(wall_loc))

display_width = display_height = 595    #17 divides 595, to make block size 35x35 pixels
pygame.display.set_caption('iScream')
pygame.display.set_icon(pygame.image.load('icon.jpg'))
gameDisplay = pygame.display.set_mode((display_width, display_height))
gameDisplay.fill(white)
clock = pygame.time.Clock()
pygame.display.update()

#INITIALIZE CONTROLS-------------
SHOOT = pygame.K_SPACE
MOVE_LEFT = pygame.K_LEFT
MOVE_RIGHT = pygame.K_RIGHT
MOVE_UP = pygame.K_UP
MOVE_DOWN = pygame.K_DOWN
PAUSE = pygame.K_p
#--------------------------------

#GUI----------------------------
def button(text, x, y, width, height, inactiveColour, activeColour, action = None):
    global curLvl, lvl_no
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        if click[0] == 1 and action != None:
            if action == 'quit':
                pygame.quit()
                quit()
            if action == 'play':
                levelSelect()
            if action == 'start':
                gameStart()
            if action == 'instruct':
                instructions()
            else:
                if action[:3] == 'lvl':
                    lvl_no = int(action[-1])
                    reset()
                    if lvl_no == 1: curLvl = Level1()
                    elif lvl_no == 2: curLvl = Level2()
                    elif lvl_no == 3: curLvl = Level3()
                    gameLoop()
        pygame.draw.rect(gameDisplay, activeColour, (x, y, width, height))
    else:
        pygame.draw.rect(gameDisplay, inactiveColour, (x, y, width, height))
    text_to_button(text, black, x, y, width, height)

def text_objects(text, colour, size):
    if size == "small":
        textSurface = pygame.font.SysFont("comicsansms", 20).render(text, True, colour)
    elif size == "medium":
        textSurface = pygame.font.SysFont("comicsansms", 50).render(text, True, colour)
    elif size == 'med-large':
        textSurface = pygame.font.SysFont("comicsansms", 65).render(text, True, colour)
    elif size == "large":
        textSurface = pygame.font.SysFont("comicsansms", 75).render(text, True, colour)
    elif size == "x-large":
        textSurface = pygame.font.SysFont("comicsansms", 130).render(text, True, colour)
    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, btnx, btny, btnwidth, btnheight, size = "small"):
    textSurf , textRect = text_objects(msg, color, size)
    textRect.center = ((btnx + (btnwidth / 2)), (btny + (btnheight / 2)))
    gameDisplay.blit(textSurf, textRect)

def message_to_screen(msg, color, center_loc, size = "small"):
    textSurf , textRect = text_objects(msg, color, size)
    textRect.center = center_loc
    gameDisplay.blit(textSurf, textRect)
#-------------------------------

class Sprite:
    size = (display_width / numRows, display_height / numCols)
    image = pygame.image.load('player.png')
    loc = [1, 1]
    direction = 'up'
    
    def __init__(self):
        self.draw()

    def draw(self):
        x, y = gridLoc[self.loc[0]][self.loc[1]]
        gameDisplay.blit(self.image, (x + 1, y + 1))

    def move(self, x, y):
        #to prevent diagonal movement, giving priority to lateral rather than vertical movement
        future_move = (self.loc[0] + x, (self.loc[1] + y if x == 0 else self.loc[1]))
        if x < 0: self.direction = 'left'
        elif x > 0: self.direction = 'right'
        elif y < 0: self.direction = 'up'
        elif y > 0: self.direction = 'down'
        if cells.walls[future_move[0]][future_move[1]] != False:
            return
        if (numRows > future_move[0] >= 0) and x != 0:
            self.loc[0] += x 
        elif (numCols > future_move[1] >= 0):
            self.loc[1] += y

    def shoot(self):
        dirVal = {'left':(-1,0), 'right':(1, 0), 'up':(0, -1), 'down':(0, 1)}
        x_dir, y_dir = dirVal[self.direction]
        x, y = self.loc[0] + x_dir , self.loc[1] + y_dir
        cell_type = cells.walls[x][y]
        mon_loc = [monster.loc for monster in monsters]
        if cell_type == 'wall': return
        i = -1
        while 0 <= x + x_dir*i < numRows and 0 <= y + y_dir * i < numCols:
            i += 1
            x1, y1 = x + x_dir*i, y + y_dir * i
            if [x1, y1] in mon_loc:
                return 
            if cells.walls[x1][y1] == cell_type:
                if cell_type == 'ice': cells.walls[x1][y1] = False
                elif cell_type == False: cells.walls[x1][y1] = 'ice'
            else:
                return

    def collideMonsters(self):
        for monster in monsters:
            if self.loc == list(monster.loc):
                gameEnd(won = False)
    
    def collideFruit(self):
        for fruit in fruits:
            if self.loc == list(fruit.loc):
                fruits.remove(fruit)

class ChasingMonster:
    size = (display_width / numRows, display_height / numCols)
    image = pygame.image.load('chasing.png')
    loc = [0, 0]
    chasing = True
    timer = 0
    time_limit = int(1500*1.5//FPS)
    target_block = [0, 0]

    def __init__(self):
        self.draw()

    def draw(self):
        x, y = gridLoc[self.loc[0]][self.loc[1]]
        gameDisplay.blit(self.image, (x+1, y+1))

    def breaking(self):
        if self.timer == self.time_limit:
            cells.walls[self.target_block[0]][self.target_block[1]] = False
            self.chasing = True
            self.timer = 0
        else:
            self.timer += 1
            cells.walls[self.target_block[0]][self.target_block[1]] = 'breaking'

    def chase(self):
        self.timer = 0
        move = [0, 0]
        dx = player.loc[0] - self.loc[0]    #-ve means player to left, +ve means player to right
        dy = player.loc[1] - self.loc[1]    #-ve means player above, +ve means player below
        if abs(dx) <= abs(dy):
            if dy < 0: move[1] -= 1
            else: move[1] += 1
        else:
            if dx < 0: move[0] -= 1
            else: move[0] += 1
        if cells.walls[self.loc[0] + move[0]][self.loc[1] + move[1]] != False:
            self.chasing = False
            self.target_block = [self.loc[0] + move[0], self.loc[1] + move[1]]
            self.block_type = cells.walls[self.loc[0] + move[0]][self.loc[1] + move[1]]
        else:
            self.loc[0] += move[0]
            self.loc[1] += move[1]

    def move(self):
        if self.chasing:
            self.chase()
        else:
            self.breaking()

class PatrollingMonster: #Patrolling monster
    size = (display_width / numRows, display_height / numCols)
    image = pygame.image.load('patrolling.png')
    loc = [0, 0]
    clockwise = True
    
    def __init__(self):
        self.draw()

    def moveRect(self, rect):
        #rect = (top left corner x, top left corner y, width, height) in terms of matrix index
        x, y, width, height = rect
        move = [0, 0]
        if self.clockwise:
            if self.loc[0] == x and self.loc[1] > y: move[1] = -1
            elif self.loc[1] == y and self.loc[0] < x + width: move[0] = 1
            elif self.loc[1] == y + height and self.loc[0] > x: move[0] = -1
            elif self.loc[0] == x + width and self.loc[1] < y + width: move[1] = 1
        else:   #anti clockwise
            if self.loc[0] == x and self.loc[1] < y + width: move[1] = 1
            elif self.loc[1] == y and self.loc[0] > x: move[0] = -1
            elif self.loc[1] == y + height and self.loc[0] < width + x: move[0] = 1
            elif self.loc[0] == x + width and self.loc[1] > y: move[1] = -1
        if cells.walls[self.loc[0] + move[0]][self.loc[1] + move[1]] != False:
            self.clockwise = False if self.clockwise else True
            pass
        else:
            self.loc[0] += move[0]
            self.loc[1] += move[1]

    def moveLine(self, point1, point2):
        #end points of the line. x1 == x2 or y1 == y2 necessarily
        x1, y1 = point1
        x2, y2 = point2
        if x1 == x2:   
            if self.clockwise:
                if self.loc[1] < y2: self.loc[1] += 1
                else: self.clockwise = False
            else:
                if self.loc[1] > y1: self.loc[1] -= 1
                else: self.clockwise = True
        elif y1 == y2:
            if self.clockwise:
                if self.loc[0] < x2: self.loc[0] += 1
                else: self.clockwise = False
            else:
                if self.loc[0] > x1: self.loc[0] -= 1
                else: self.clockwise = True
    
    def draw(self):
        x, y = gridLoc[self.loc[0]][self.loc[1]]
        gameDisplay.blit(self.image, (x+1, y+1))

class Grid:
    size = (display_width / numRows, display_height / numCols)  #size of each individual cell
    colour = snow
    wall_colour = med_blue
    ice_colour = light_blue
    breaking_colour = red
    borderColour = black
    #to check for walls/obstacles. False - free space, True - obstacle/wall etc
    walls = [[False for y in range(numCols)] for x in range(numRows)]    
    def __init__(self):
        for x in range(numRows):
            for y in range(numCols):
                if (x, y) in wall_loc:
                    self.walls[x][y] = 'wall'
        self.draw(0)

    def draw(self, time_count): #take time_count as parameter for cool colouring effects that depend on time for the walls 
        for x in range(numRows):
            for y in range(numCols):
                if self.walls[x][y] == 'wall':
                    c = self.wall_colour
                elif self.walls[x][y] == 'ice':
                    c = self.ice_colour
                elif self.walls[x][y] == 'breaking':
                    c = self.breaking_colour if time_count%2==0 else self.ice_colour
                else:
                    c = self.colour
                pygame.draw.rect(gameDisplay, c, (x * self.size[0], y*self.size[1], self.size[0], self.size[1]))
                pygame.draw.rect(gameDisplay, self.borderColour, (x * self.size[0], y*self.size[1], self.size[0], self.size[1]), 1)

class Fruit:
    size = (display_width / numRows, display_height / numCols)
    colour = red
    loc = [8, 8]
    #note: the frozen counterparts are for images that don't have a transparent background.
    #if all images get a frozen background, then freeze() function is rendered useless
    apple = pygame.image.load('apple.jpg')
    banana = pygame.image.load('banana.png') #no need new image with blue background as current image has transparent background
    frozen_apple = pygame.image.load('frozen_apple.jpg')
    image = apple
    
    def __init__(self, typ = 'apple'):
        if typ == 'banana': self.image = self.banana
        self.draw()

    def draw(self):
        gameDisplay.blit(self.image, (self.loc[0] * self.size[0] + 1, self.loc[1] * self.size[1] + 1))

    def freeze(self):
        if cells.walls[self.loc[0]][self.loc[1]] == 'ice':
            if self.image == self.apple: self.image = self.frozen_apple
        else:
            if self.image == self.frozen_apple: self.image = self.apple

'''Level Creator:
Every level should have a class object
it should be of the form:
class Level<number>:
    startTime = 0
    
    def __init__(self):
        startTime = time()
        player.loc = [1, 1]
        #INTIALIZE WALLS

        #INTIALIZE ICE

        #INITIALIZE FRUITS
        global fruits
        fruits = [Fruit() for i in range(<number of fruits>)]

        #INITIALIZE MONSTERS
        global monsters

    def moveMonster(self):
        #make monsters move
This format should be strictly followed, taking care of uppercase and lowercase letters
This is because the level object is assigned to a variable and standard notations have been used with regard to this variable
Go through the code once before creating a level.'''

MAXLEVELS = 3   #UPDATE AFTER CREATION OF NEW LEVEL!!

class Level1:
    startTime = 0
    numFruitLvls = 1
    
    def __init__(self):
        self.startTime = time()
        player.loc = [3, 3]
        #INTIALIZE WALLS
        cells.walls[numRows//2][numCols//2] = 'wall'
        #INTIALIZE ICE
        for i in range(2, numRows-2):
            cells.walls[1][i] = 'ice'
            cells.walls[i][1] = 'ice'
            cells.walls[i][numCols - 2] = 'ice'
            cells.walls[numRows - 2][i] = 'ice'
        for i in range(5, numRows-5):
            cells.walls[i][5] = 'ice'
            cells.walls[5][i] = 'ice'
            cells.walls[i][numCols - 6] = 'ice'
            cells.walls[numRows - 6][i] = 'ice'
        cells.walls[2][numCols - 3] = 'ice'
        cells.walls[numRows - 3][2] = 'ice'
        for i in range(2, 5):
            for j in range(2, 5):
                cells.walls[i][j] = 'ice'
                cells.walls[numRows - i - 1][numCols - j - 1] = 'ice'
        cells.walls[3][3] = False
        #INITIALIZE FRUITS
        global fruits
        fruits = [Fruit() for i in range(13)]
        for f in fruits: f.image = Fruit.apple
        fruits[0].loc = [1 , 1]
        fruits[1].loc = [1 , numCols - 2]
        fruits[2].loc = [numRows - 2 , 1]
        fruits[3].loc = [numRows - 2, numCols - 2]
        fruits[4].loc = [numRows - 4, numCols - 4]
        m = numRows//2 
        fruits[5].loc = [m - 1, m - 1]
        fruits[6].loc = [m + 1, m - 1]
        fruits[7].loc = [m - 1, m + 1]
        fruits[8].loc = [m + 1, m + 1]
        fruits[9].loc = [m, m - 1]
        fruits[10].loc = [m - 1, m]
        fruits[11].loc = [m + 1, m]
        fruits[12].loc = [m, m + 1]
        #INITIALIZE MONSTERS
        global monsters
        monsters = [PatrollingMonster() for i in range(4)]
        monsters[0].loc = [numRows - 4, 3]
        monsters[1].loc = [3, numRows - 4]
        monsters[2].loc = [6, numRows - 7]
        monsters[3].loc = [numRows - 7, 6]

    def Monster0Move(self):
        m = monsters[0]
        move = [0, 0]
        if m.clockwise:
            if m.loc == [numRows - 4, 3]: move[0] += 1
            elif m.loc[0] == numRows - 3 and m.loc[1] != numCols - 6: move[1] += 1
            elif m.loc[1] == numCols - 6 and m.loc[0] != numRows - 5: move[0] -= 1
            elif m.loc[0] == numRows - 5 and m.loc[1] > 4: move[1] -= 1
            elif m.loc[1] == 4 and m.loc[0] != 5: move[0] -= 1
            elif m.loc[0] == 5 and m.loc[1] != 2: move[1] -= 1
            elif m.loc[1] == 2 and m.loc[0] != numRows - 4: move[0] += 1
            elif m.loc[0] == numRows - 4 and m.loc[1] != 3: move[1] += 1
        else:
            if m.loc == [numRows - 4, 3]: move[1] -= 1
            elif m.loc[1] == 2 and m.loc[0] != 5: move[0] -= 1
            elif m.loc[0] == 5 and m.loc[1] != 4: move[1] += 1
            elif m.loc[1] == 4 and m.loc[0] < numRows - 5: move[0] += 1
            elif m.loc[0] == numRows - 5 and 4 <= m.loc[1] < numCols - 6: move[1] += 1
            elif m.loc[1] == numCols - 6 and m.loc[0] != numRows - 3: move[0] += 1
            elif m.loc[0] == numRows - 3 and m.loc[1] != 3: move[1] -= 1
            elif m.loc == [numRows - 3, 3]: move[0] -= 1
        if cells.walls[m.loc[0] + move[0]][m.loc[1] + move[1]] == False:
            m.loc[0] += move[0]
            m.loc[1] += move[1]
        else:
            m.clockwise = (not m.clockwise)

    def Monster1Move(self):
        m = monsters[1]
        move = [0, 0]
        if not m.clockwise:
            if m.loc == [3, numRows - 4]: move[1] += 1
            elif m.loc[1] == numRows - 3 and m.loc[0] != numCols - 6: move[0] += 1
            elif m.loc[0] == numCols - 6 and m.loc[1] != numRows - 5: move[1] -= 1
            elif m.loc[1] == numRows - 5 and m.loc[0] > 4: move[0] -= 1
            elif m.loc[0] == 4 and m.loc[1] != 5: move[1] -= 1
            elif m.loc[1] == 5 and m.loc[0] != 2: move[0] -= 1
            elif m.loc[0] == 2 and m.loc[1] != numRows - 4: move[1] += 1
            elif m.loc[1] == numRows - 4 and m.loc[0] != 3: move[0] += 1
        else:
            if m.loc == [3, numRows - 4]: move[0] -= 1
            elif m.loc[0] == 2 and m.loc[1] != 5: move[1] -= 1
            elif m.loc[1] == 5 and m.loc[0] != 4: move[0] += 1
            elif m.loc[0] == 4 and m.loc[1] < numRows - 5: move[1] += 1
            elif m.loc[1] == numRows - 5 and 4 <= m.loc[0] < numCols - 6: move[0] += 1
            elif m.loc[0] == numCols - 6 and m.loc[1] != numRows - 3: move[1] += 1
            elif m.loc[1] == numRows - 3 and m.loc[0] != 3: move[0] -= 1
            elif m.loc[0] == numRows - 4 and m.loc[1] != 3: move[1] -= 1
            elif m.loc == [3, numRows - 3]: move[1] -= 1
        if cells.walls[m.loc[0] + move[0]][m.loc[1] + move[1]] == False:
            m.loc[0] += move[0]
            m.loc[1] += move[1]
        else:
            m.clockwise = (not m.clockwise)
    
    def moveMonster(self):
        self.Monster0Move()
        self.Monster1Move()
        monsters[2].moveRect((6, 6, numRows - 13, numCols - 13))
        monsters[3].moveRect((6, 6, numRows - 13, numCols - 13))
  
class Level2:
    startTime = 0
    numFruitLvls = 1
    
    def __init__(self): 
        self.startTime = time()
        player.loc = [1, 1]
        global fruits
        #INITIALIZE WALLS
        for i in range(numRows//2 - 1, numRows//2 + 2):
            for j in range(numCols//2 - 1, numCols//2 + 2):
                cells.walls[i][j] = 'wall'
        for i in range(5, numRows - 5):
            cells.walls[i][2] = 'wall'
            cells.walls[i][numCols - 3] = 'wall'
        #INITIALIZE ICE
        for i in range(4, numRows - 4):
            cells.walls[i][4] = 'ice'
            cells.walls[4][i] = 'ice'
            cells.walls[i][numCols - 5] = 'ice'
            cells.walls[numRows - 5][i] = 'ice'
        for i in range(2, numCols - 2, 2):
            cells.walls[2][i] = 'ice'
            cells.walls[numRows - 3][i] = 'ice'
        #INITIALIZE FRUITS
        fruits = [Fruit() for x in range(36)]
        fruits[0].loc = [6, 6]
        fruits[1].loc = [6, numCols - 7]
        fruits[2].loc = [numRows - 7, 6]
        fruits[3].loc = [numRows - 7, numCols - 7]
        c = 4
        for i in range(7, numRows - 7):
            fruits[c].loc = [i, 6]
            fruits[c+1].loc = [6, i]
            fruits[c+2].loc = [i, numCols - 7]
            fruits[c+3].loc = [numRows - 7, i]
            c += 4
        for i in range(3, numCols- 3, 2):
            fruits[c].loc = [2, i]
            fruits[c+1].loc = [numRows - 3, i]
            c += 2  
        for i in range(3, 5):
            fruits[c].loc = [i, 2]
            fruits[c+1].loc = [numRows - i - 1, 2]
            fruits[c+2].loc = [i, numCols - 3]
            fruits[c+3].loc = [numRows - i - 1, numCols - 3]
            c += 4
        #INITIALIZE MONSTERS
        global monsters
        monsters = [PatrollingMonster() for x in range(5)]
        monsters[0].loc = [numRows - 2, numCols - 2]
        monsters[1].loc = [3, numCols - 4]
        monsters[2].loc = [numRows - 4, 3]
        monsters[3].loc = [5, 5]
        monsters[4].loc = [numRows - 6, numCols - 6]
        for m in monsters:
            m.colour = yellow
            m.clockwise = True

    def moveMonster(self):
        monsters[0].moveRect((1, 1, numRows - 3, numCols - 3))
        monsters[1].moveRect((3, 3, numRows - 7, numCols - 7))
        monsters[2].moveRect((3, 3, numRows - 7, numCols - 7))
        monsters[3].moveRect((5, 5, numRows - 11, numCols - 11))
        monsters[4].moveRect((5, 5, numRows - 11, numCols - 11))

class Level3:
    startTime = 0
    numFruitLvls = 2
    
    def __init__(self):
        self.startTime = time()
        player.loc = [3, 3]
        #INTIALIZE ICE
        for i in range(2, numRows - 2):
            cells.walls[i][numCols//2] = 'ice'
            cells.walls[numRows//2][i] = 'ice'
        
        #INTIALIZE WALLS
        for i in range(numRows//2 - 1, numRows//2 + 2):
            for j in range(numCols//2 - 1, numCols//2 + 2):
                cells.walls[i][j] = 'wall'
        for i in range(2, 5):
            cells.walls[i][2] = 'wall'
            cells.walls[2][i] = 'wall'
            cells.walls[i][numCols - 3] = 'wall'
            cells.walls[numCols - 3][i] = 'wall'
            cells.walls[2][numCols - i - 1] = 'wall'
            cells.walls[numCols - i - 1][2] = 'wall'
            cells.walls[numRows - 3][numCols - i - 1] = 'wall'
            cells.walls[numRows - i - 1][numCols - 3] = 'wall'
        cells.walls[numRows//2][numCols//2] = False
        #INITIALIZE FRUITS
        global fruits
        fruits = [Fruit() for i in range(37)]
        c = 1
        fruits[0].loc = [numRows//2, numCols//2]
        for i in range(4, 7):
            for j in range(4, 7):
                fruits[c].loc = [i, j]
                fruits[c+1].loc = [numRows - i - 1, j]
                fruits[c+2].loc = [j, numCols - i - 1]
                fruits[c+3].loc = [numRows - i - 1, numCols - j - 1]
                c += 4
        #INITIALIZE MONSTERS
        global monsters
        monsters = [ChasingMonster()] 
        monsters[0].loc = [numRows//2, numCols//2]
        
    def moveMonster(self):
        monsters[0].move()

    def resetFruits(self):
        self.numFruitLvls -= 1
        global fruits
        fruits = [Fruit(typ = 'banana') for i in range(37)]
        c = 1
        fruits[0].loc = [numRows//2, numCols//2]
        for i in range(4, 7):
            for j in range(4, 7):
                fruits[c].loc = [i, j]
                fruits[c+1].loc = [numRows - i - 1, j]
                fruits[c+2].loc = [j, numCols - i - 1]
                fruits[c+3].loc = [numRows - i - 1, numCols - j - 1]
                c += 4
        
  
#INITIALIZE EVERYTHING---------------
cells = Grid()
lvl_no = 1
#gridLoc gives the actual pixel location of any cell relative to the matrix index of the cell
gridLoc = [[(x*cells.size[0], y*cells.size[1]) for y in range(numCols)] for x in range(numRows)]
player = Sprite()
curLvl = Level1()

def instructions():
    key_dict = {MOVE_UP:'UP', MOVE_DOWN:'DOWN', MOVE_LEFT:'LEFT', MOVE_RIGHT:'RIGHT', SHOOT:'SPACE', PAUSE:'P'}
    gameDisplay.fill(snow)
    message_to_screen('INSTRUCTIONS', chocolate, (display_width//2, 50) , 'med-large')
    message_to_screen('MOVE LEFT:- '+key_dict[MOVE_LEFT], med_blue, (display_width//2, 150), 'small')
    message_to_screen('MOVE RIGHT:- '+key_dict[MOVE_RIGHT], med_blue, (display_width//2, 200), 'small')
    message_to_screen('MOVE UP:- '+key_dict[MOVE_UP], med_blue, (display_width//2, 250), 'small')
    message_to_screen('MOVE DOWN:- '+key_dict[MOVE_DOWN], med_blue, (display_width//2, 300), 'small')
    message_to_screen('SHOOT/BREAK ICE:- '+key_dict[SHOOT], med_blue, (display_width//2, 350), 'small')
    message_to_screen('PAUSE:- '+key_dict[PAUSE], med_blue, (display_width//2, 400), 'small')
    pygame.display.update()
    sleep(0.2) 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
        button('PLAY', 50, 450, 225, 125, green, light_green, 'play')
        button('QUIT', display_width - 275, 450, 225, 125, red, light_red, 'quit')
        pygame.display.update()
        clock.tick(FPS)

def reset():
    global lvl_no
    for x in range(numRows):
        for y in range(numCols):
            if (x, y) in wall_loc:
                cells.walls[x][y] = 'wall'
            else:
                cells.walls[x][y] = False
    
def gameEnd(won):
    reset()
    
    #Find Time Taken to complete level
    endTime = int(time() - curLvl.startTime)
    minute = endTime // 60
    seconds = endTime % 60
    if 10 > seconds >= 0: seconds = '0'+str(seconds)
    else: seconds = str(seconds)

    gameDisplay.fill(snow)
    if won: msg = 'YOU WIN'
    else: msg = 'YOU DIED'
    message_to_screen(msg, red, (display_width//2, 150), "large")
    if lvl_no == MAXLEVELS and won:
        message_to_screen('GAME OVER', orange, (display_width//2, 300), "large")
        message_to_screen('TIME TAKEN:- %d:%s'%(minute, seconds), chocolate, (display_width//2, 425), "medium")
        pygame.display.update()
        sleep(1.50)
        gameStart()
        return
    pygame.display.update()
    if won: msg = ('NEXT LEVEL', 'lvl' + str(lvl_no + 1))
    else: msg = ('PLAY AGAIN', 'lvl' + str(lvl_no))
    message_to_screen('TIME TAKEN:- %d:%s'%(minute, seconds), chocolate, (display_width//2, 225), "medium")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
        button(msg[0], 50, 400, 125, 125, green, light_green, msg[1])
        button('MAIN MENU', (display_width - 175)//2, 400, 175, 125, orange, yellow, 'start')
        button('QUIT', display_width - 175, 400, 125, 125, red, light_red, 'quit')
        pygame.display.update()
        clock.tick(FPS)

def gameStart():
    gameDisplay.fill(snow)
    message_to_screen('WELCOME TO', light_red, (display_width//2, 75) , 'medium')
    message_to_screen('iSCREAM', chocolate, (display_width//2, 175), 'x-large')
    pygame.display.update()
    sleep(0.3) 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
        button('PLAY', 50, 350, 125, 125, green, light_green, 'play')
        button('INSTRUCTIONS', (display_width - 175)//2, 350, 175, 125, orange, yellow, 'instruct')
        button('QUIT', display_width - 175, 350, 125, 125, red, light_red, 'quit')
        pygame.display.update()
        clock.tick(FPS)

#For user to select levels. MUST UPDATE AFTER CREATING EVERY LEVEL!!
def levelSelect():
    gameDisplay.fill(snow)
    message_to_screen('CHOOSE LEVEL', light_red, (display_width//2, 75) , 'medium')
    pygame.display.update()
    sleep(0.3) 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
        row = 150
        btnSize = 80
        gap = 25
        n =(display_width - gap)//(btnSize + gap)
        x = gap
        y = 150
        for i in range(MAXLEVELS):
            if i % n == 0 and i != 0:
                x = gap
                y += btnSize + gap
            elif i % n != 0:
                x += btnSize + gap
            button('LEVEL %d'%(i+1), x, y, btnSize, btnSize, green, light_green, 'lvl'+str(i+1))
        pygame.display.update()
        clock.tick(FPS)

def gameLoop():
    pause = False
    time_count = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == SHOOT and not pause:
                    player.shoot()
                if event.key == PAUSE:
                    pause = not(pause)
        if pause: continue
        keystate = pygame.key.get_pressed()
        if time_count % 2 == 0:
            player.move((keystate[MOVE_RIGHT] - keystate[MOVE_LEFT]), (keystate[MOVE_DOWN] - keystate[MOVE_UP]))
        player.collideFruit()
        player.collideMonsters()
        if len(fruits) == 0:
            if curLvl.numFruitLvls > 1:
                curLvl.resetFruits()
            else:
                gameEnd(won = True)
        if time_count % 1.5 == 0:
            curLvl.moveMonster()
        gameDisplay.fill(white)
        cells.draw(time_count)
        for f in fruits:
            f.draw()
            f.freeze()
        for m in monsters: m.draw()
        player.draw()
        time_count += 1
        time_count = time_count % 12
        pygame.display.update()
        clock.tick(FPS)

gameStart()
