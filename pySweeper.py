import pygame
import random

#initializing window
pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("pySweeper")
running = True


#BUTTON CLASS
class SquareButton:
    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def getColor(self):
        return self.color


#FILLS GRID WITH SPECIFIED AMOUNT OF BOMBS
def fillGrid(grid, bombsAmt):
    #fill grid with bomb amount
    for _ in range(bombsAmt):
        x = random.randint(0,len(grid)-1)
        y = random.randint(0,len(grid[0])-1)
        
        #if nothing in pos then put bomb (-1)
        if grid[x][y] == None:
            grid[x][y] = -1
        #else, find a pos without a bomb (-1) and put one there
        else:
            while(grid[x][y]):
                x = random.randint(0,len(grid)-1)
                y = random.randint(0,len(grid[0])-1)
            grid[x][y] = -1
            
    
    #total surrounding bombs
    totalSBombs = 0
    #each pos in grid filled with amount of bombs (-1) in 3x3 surrounding area
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            #if pos not a bomb (-1)
            if grid[x][y] != -1:
                #checks total bombs in 3x3 grid
                for sX in range(x-1, x+2):
                    for sY in range(y-1, y+2):
                        #if (sX, sY) not out of bounds and is a bomb
                        if((sX>=0 and sX<len(grid)) and (sY>=0 and sY<len(grid[0])) and grid[sX][sY] == -1):
                            totalSBombs+=1
            
                grid[x][y]=totalSBombs                          
            #reset total surrounding bombs                
            totalSBombs = 0        
         
            
#IF NUMBER CLICKED AND THAT AMOUNT OF FLAGS PLACED AROUND THEN DELETE ALL BLOCKS
def numberClicked(buttonGrid, grid, x, y):
    numFlags = 0
    
    #find num of flags placed in surrounding 3x3 grid
    for sX in range(x-1, x+2):
        for sY in range(y-1, y+2):
            if(sX>=0 and sX<len(grid)) and (sY>=0 and sY<len(grid[0])) and (buttonGrid[sX][sY]) and (buttonGrid[sX][sY].getColor() == "red"):
                numFlags+=1
    
    lost = False
    #if num flags is = to num of bombs
    if numFlags==grid[x][y]:
        for sX in range(x-1, x+2):
            for sY in range(y-1, y+2):
                if(sX>=0 and sX<len(grid)) and (sY>=0 and sY<len(grid[0])) and (buttonGrid[sX][sY]) and (buttonGrid[sX][sY].getColor() == "grey"):
                    lost = spotClicked(buttonGrid, grid, sX, sY)
                    if lost==True:
                        return lost
    return lost
            
            
#IF SPACE CLICKED, RETURN TRUE IF BOMB, FALSE ELSE
def spotClicked(buttonGrid, grid, x, y):
    #bomb case
    if grid[x][y] == -1:
        return True
    #non-empty spot case
    elif grid[x][y]!= 0:
        buttonGrid[x][y]=None
        return False
    #empty spot case
    else:
        buttonGrid[x][y]=None
        setEmptySpots(buttonGrid, grid, x, y)
        return False
        

#RECURSIVE FUNCTION, IF YOU CLICK AN EMPTY SPACE ALL NON BOMBS SURROUNDING DELETED
def setEmptySpots(buttonGrid, grid, x, y):
    #base case, if all spots around are not empty then return
    if ((x+1>=0 and x+1<len(grid)) and grid[x+1][y]!=0 ) and ((x-1>=0 and x-1<len(grid)) and grid[x-1][y]!=0 ) and ((y+1>=0 and y+1<len(grid)) and grid[x][y+1]!=0) and  ((y-1>=0 and y-1<len(grid)) and grid[x][y-1]!=0):
        isEmptySpot(buttonGrid, grid, x, y)
        return

    
    #checks each direction, if empty continues in that direction
    if (x+1>=0 and x+1<len(grid)) and isEmptySpot(buttonGrid,grid, x+1, y):
        buttonGrid[x+1][y] = None
        grid[x][y]=None
        setEmptySpots(buttonGrid, grid, x+1, y)
    if (x-1>=0 and x-1<len(grid)) and isEmptySpot(buttonGrid,grid, x-1, y):
        buttonGrid[x-1][y] = None
        grid[x][y]=None
        setEmptySpots(buttonGrid, grid, x-1, y)
    if (y+1>=0 and y+1<len(grid[0])) and isEmptySpot(buttonGrid,grid, x, y+1):
        buttonGrid[x][y+1] = None
        grid[x][y]=None
        setEmptySpots(buttonGrid, grid, x, y+1)
    if (y-1>=0 and y-1<len(grid[0])) and isEmptySpot(buttonGrid,grid, x, y-1):
        buttonGrid[x][y-1] = None
        grid[x][y]=None
        setEmptySpots(buttonGrid, grid, x, y-1)
    #corners    
    if (x-1>=0 and x-1<len(grid)) and (y-1>=0 and y-1<len(grid[0])) and grid[x-1][y-1] == 0:
        buttonGrid[x-1][y-1]=None
        grid[x][y]=None
        setEmptySpots(buttonGrid, grid, x-1, y-1)
    if (x-1>=0 and x-1<len(grid)) and (y+1>=0 and y+1<len(grid[0])) and grid[x-1][y+1] == 0:
        buttonGrid[x-1][y+1]=None
        grid[x][y]=None
        setEmptySpots(buttonGrid, grid, x-1, y+1)
    if (x+1>=0 and x+1<len(grid)) and (y-1>=0 and y-1<len(grid[0])) and grid[x+1][y-1] == 0:
        buttonGrid[x+1][y-1]=None
        grid[x][y]=None
        setEmptySpots(buttonGrid, grid, x+1, y-1)
    if (x+1>=0 and x+1<len(grid)) and (y+1>=0 and y+1<len(grid[0])) and grid[x+1][y+1] == 0:
        buttonGrid[x+1][y+1]=None     
        grid[x][y]=None
        setEmptySpots(buttonGrid, grid, x+1, y+1) 
        
        
        
#CHECKS IF SPECIFIED SPOT IN GRID IS EMPTY
def isEmptySpot(buttonGrid, grid, x, y):
    if grid[x][y]!=0:
        buttonGrid[x][y]=None
        if (x-1>=0 and x-1<len(grid)) and (y>=0 and y<len(grid[0])) and grid[x-1][y] != -1 and (((y+1>=0 and y+1<len(grid[0])) and buttonGrid[x-1][y+1]==None) or ((y-1>=0 and y-1<len(grid[0])) and buttonGrid[x-1][y-1]==None)):
            buttonGrid[x-1][y]=None
        if (x+1>=0 and x+1<len(grid)) and (y>=0 and y<len(grid[0])) and grid[x+1][y] != -1 and (((y+1>=0 and y+1<len(grid[0])) and buttonGrid[x+1][y+1]==None) or ((y-1>=0 and y-1<len(grid[0])) and buttonGrid[x+1][y-1]==None)):
            buttonGrid[x+1][y]=None
            
        return False
    else:
        #orthagonal
        if (x+1>=0 and x+1<len(grid)) and grid[x+1][y] != -1:
            buttonGrid[x+1][y]=None
        if (x-1>=0 and x-1<len(grid)) and grid[x-1][y] != -1:
            buttonGrid[x-1][y]=None
        if (y+1>=0 and y+1<len(grid[0])) and grid[x][y+1] != -1:
            buttonGrid[x][y+1]=None
        if (y-1>=0 and y-1<len(grid[0])) and grid[x][y-1] != -1:
            buttonGrid[x][y-1]=None
        #corners
        if (x-1>=0 and x-1<len(grid)) and (y-1>=0 and y-1<len(grid[0])) and grid[x-1][y-1] != -1:
            buttonGrid[x-1][y-1]=None
        if (x-1>=0 and x-1<len(grid)) and (y+1>=0 and y+1<len(grid[0])) and grid[x-1][y+1] != -1:
            buttonGrid[x-1][y+1]=None
        if (x+1>=0 and x+1<len(grid)) and (y-1>=0 and y-1<len(grid[0])) and grid[x+1][y-1] != -1:
            buttonGrid[x+1][y-1]=None
        if (x+1>=0 and x+1<len(grid)) and (y+1>=0 and y+1<len(grid[0])) and grid[x+1][y+1] != -1:
            buttonGrid[x+1][y+1]=None  
        print("\n")
        return True
     
    
#GAME LOOP
def gameLoop(grid, buttonGrid, flagsPlaced):
    lost, won = False, False
    running=True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #left mouse click
            buttonClicked = False
            if event.button == 1: 
                for x in range(len(buttonGrid)):
                    for y in range(len(buttonGrid[0])):
                        if(buttonGrid[x][y]):
                            if buttonGrid[x][y].rect.collidepoint(event.pos) and buttonGrid[x][y].getColor() == "grey":
                                buttonClicked = True
                                lost = spotClicked(buttonGrid, grid, x, y)
                if buttonClicked==False:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    lost = numberClicked(buttonGrid, grid, mouseX//buttonSize, mouseY//buttonSize)
                
                                
            #right mouse click
            elif event.button == 3:
                for x in range(len(buttonGrid)):
                    for y in range(len(buttonGrid[0])):
                        if(buttonGrid[x][y]):
                            if buttonGrid[x][y].rect.collidepoint(event.pos):
                                if(buttonGrid[x][y].getColor() == "grey" and flagsPlaced<bombsAmt):
                                    buttonGrid[x][y] = SquareButton(x*buttonSize, y*buttonSize, buttonSize, ("red"))
                                    flagsPlaced+=1
                                elif(buttonGrid[x][y].getColor() == "red"):
                                    buttonGrid[x][y] = SquareButton(x*buttonSize, y*buttonSize, buttonSize, ("grey"))
                                    flagsPlaced-=1

    screen.fill("black")
        
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if(grid[x][y]!=0 and grid[x][y]!=None):
                screen.blit(font.render(str(grid[x][y]), True, "blue"), (x*buttonSize + buttonSize/3, y*buttonSize + buttonSize/4))
        
    #display buttons
    buttonsLeft=0
    for buttonRow in buttonGrid:
        for button in buttonRow:
            if(button):
                button.draw()
                buttonsLeft+=1
        
    #if all non bomb spots cleared then win
    if buttonsLeft == bombsAmt:
        won = True
        
    #draw grid            
    for x in range(0, width, buttonSize):
        pygame.draw.line(screen, "white", (x, 0), (x, height))
    for y in range(0, height, buttonSize):
        pygame.draw.line(screen, "white", (0, y), (width, y))
        
    pygame.display.flip()
    clock.tick(fps)
    return running, lost, won, flagsPlaced
    
    
#WINNING SCREEN    
def winner():
    won = True
    lost = False
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            won, lost = False, True
    
    screen.fill("black")
    
    winningText = font.render("WINNER!!!", True, "blue")
    screen.blit(winningText, winningText.get_rect(center=(width//2, height//3)))
    
    clickAnywhereText = font.render("click anywhere to reset", True, "blue")     
    screen.blit(clickAnywhereText, clickAnywhereText.get_rect(center=(width//2, height//2)))
    
    pygame.display.flip()
    clock.tick(fps)
            
    return running, won, lost 
    
    
#MAIN FUNCTION
if __name__ == "__main__":
    #initialize runtime vars
    fps = 30
    won = False 
    lost = False
    
    #initialize grids
    rows,cols = 16,16
    bombsAmt = 40
    flagsPlaced = 0
    grid = []
    buttonGrid = []
    for _ in range(rows):
        grid.append([None]*cols)
        buttonGrid.append([None]*cols)
    
    buttonSize = 50
    for x in range(rows):
        for y in range(cols):
            buttonGrid[x][y] = SquareButton(x*buttonSize, y*buttonSize, buttonSize, ("grey"))
    
    font = pygame.font.Font(None, buttonSize)
        
    fillGrid(grid, bombsAmt)    
    
    ####################################
    #ONLY FOR TESTING, COMMENT OUT LATER
    #for row in grid:
        #print(row)
    ####################################
    
    while running:
        if (lost==False and won==False):
            running, lost, won, flagsPlaced = gameLoop(grid, buttonGrid, flagsPlaced)
        elif(lost==True):
            #reset grid
            for x in range(rows):
                for y in range(cols):
                    buttonGrid[x][y] = SquareButton(x*buttonSize, y*buttonSize, buttonSize, ("grey"))
                    grid[x][y] = None
            fillGrid(grid, bombsAmt)
            lost=False
            flagsPlaced=0
        elif(won==True):
            running, won, lost = winner()
            flagsPlaced=0
        
    pygame.quit()
