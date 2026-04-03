import pygame
import random           #for random tiles

DIRECTIONS = ["left, right, up, down"]

#spawns a random tile between 2, 4, and 8 into the board (with probability 0.7, 0.25, 0.05 respectively)
# returns a true/false, if false, then it failed to generate a tile, which should be a lose-state
def spawn_tile(board):
    if not board:       #the board doesn't exist
        return False

    #This stores the list of empty spaces (location (r, c)'s) left on the baord
    empty_spaces = []

    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == 0:
                empty_spaces.append((r, c))

    if not empty_spaces:    # no empty cell left, so we failed to spawn a tile
        return False

    #Randomly choose a tile from empty_Spaces to add a tile to
    row, col = random.choice(empty_spaces)
    
    rand = random.uniform(0, 1)
    
    #geneerate the value of said tile; P(2) = 0.7, P(4) = 0.25, P(8) = 0.05. Change this as needed
    val = 0
    if rand <= 0.7:
        val = 2
    elif rand > 0.7 and rand <= 0.95:
        val = 4
    elif rand > 0.95:
        val = 8
    else:
        val = 0 #never happening but what if you know
    board[row][col] = val

    #Tile generation succeeded
    return True


#This method creates an empty nxn board, returned as a list [ [], [], [], [] ]
#If someone made this already just delete it
def create_board(n):
    board = []

    for r in range(n):
        row = [0] * n       #a list of 0 n times
        board.append(row)
        
    #spawn two initial tiles; we can move this to scale with the size of the board later
    spawn_tile(board)
    spawn_tile(board)
    
    return board

def main():
    pygame.init()
    
    # Screen size in pixels
    size: tuple[int, int] = (1000, 1000)
    
    # RGB color values
    black: tuple[int, int, int] = (0, 0, 0)
    white: tuple[int, int, int] = (255, 255, 255)
    
    # Create the game window
    screen = pygame.display.set_mode(size)
    
    #Fill the screen with a white background initially
    screen.fill(color=white)        
    
    screenCenter: tuple[float, float] = (500, 500)
    running: bool = True
    
    ballLocation: tuple[float, float] = screenCenter
    #ballLocation = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    
    pygame.draw.circle(radius=10, color = black, surface=screen, center=screenCenter)
    
    clock = pygame.time.Clock()
    
    # Right now it seems to run a program that has a ball in the center of the screen. Moves upon input WASD (Up, Left, Down, Right)
    while running:
        dt = clock.tick(60) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        
        keyAction: list = pygame.key.get_pressed()
        
        x: float = ballLocation[0]
        y: float = ballLocation[1]
        
        #added arrow key input functionality (it also allows movement diagonally if two keys held simulatenously, might be buggy for 2048?)
        if keyAction[pygame.K_d] or keyAction[pygame.K_RIGHT] == True:
            x += 300 * dt
        if keyAction[pygame.K_a] or keyAction[pygame.K_LEFT] == True:
            x -= 300 * dt
        if keyAction[pygame.K_s] or keyAction[pygame.K_DOWN] == True:
            y += 300 * dt
        if keyAction[pygame.K_w] or keyAction[pygame.K_UP] == True:
            y -= 300 * dt
            
        ballLocation =(x, y)
        
        screen.fill(color=white)
        
        pygame.draw.circle(radius=10, color = black, surface=screen, center=ballLocation)
        
        pygame.display.flip()
        
        pygame.event.clear()
        

main()