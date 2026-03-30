from copy import deepcopy
import tileClass

"""
Represents any one state of the 2048 game. 
s
Fields:
    list[list] board = nested lists containing the tile classes
    int score = Total score of the current board
    int freeSpaces = Number of board spaces not containing a tile
"""
class gameState:
    """
    Default initializer. Instantiates all class variables for a empty gameState 
    """
    def __init__(self):
        #Create original list
        self.board: list[
                        list: tileClass, 
                        list: tileClass, 
                        list: tileClass,
                        list: tileClass] = list()
        
        #Add 4 empty lists to our board
        for i in range(len(self.board)):
            #Add 4 empty lists to each list in list
            self.board.append(list())
            for n in range(4):
                self.board[i].append(None)
        
        self.score = 0
        self.freeSpaces = 16
        return None
    
    """
    Create a gameState from another gameState. 
    Might not be necessary or should be copy function
    """
    def __init__(self, gameState):
        self.board = deepcopy(gameState.board)
        self.score = gameState.score
        self.freeSpaces = gameState.freeSpaces
    
    def move(self, direction):
        if direction not in ["up", "down", "left", "right"]:
            return
        
        if self.checkLegal(direction) == False:
            return
        
        for row in self.board:
            for tile in row:
                if self.checkConflict(tile, direction) == False:
                    
                    
        
        
        
    def checkLegal(self, direction):
        if direction not in ["up", "down", "left", "right"]:
            return
        
    def checkConflict(self, tile, direction):
        #Find the first non empty slot
        if direction == "up":
            #Check top of column to tile (1, 2, TILE)
            for gridY in range(tile.gridY).__reversed__:
                tileToCheck = self.board[tile.gridX][gridY]
                if tileToCheck is not None and tileToCheck.value == tile.value: 
                    return True
            return False
        elif direction == "down":
            #Check tile + 1 to bottom of column (Tile, 3, 4)
            for gridY in range(tile.gridY + 1, len(self.board[tile.gridX])):
                tileToCheck = self.board[tile.gridX][gridY]
                if tileToCheck is not None and tileToCheck.value == tile.value: 
                    return True
            return False
            
        elif direction == "left":
            #Check leftmost column to TILE (1, 2, Tile)
            for gridY in range(tile.gridX).__reversed__:
                tileToCheck = self.board[tile.gridX][gridY]
                if tileToCheck is not None and tileToCheck.value == tile.value: 
                    return True
            return False
        elif direction == "right":
            #Check TILE + 1 to end of row (Tile, 3, 4)
            for gridY in range(tile.gridX + 1, len(self.board[tile.gridY])):
                tileToCheck = self.board[tile.gridX][gridY]
                if tileToCheck is not None and tileToCheck.value == tile.value: 
                    return True
            return False
        
    
    def isLoss():
        pass
        
    def isWin():
        pass
    
    
