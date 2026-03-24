from copy import deepcopy


"""
Represents any one state of the 2048 game. 

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
        self.board = list()
        
        #Add 4 empty lists to our board
        for i in range(4):
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
    
    def move():
        pass
    
    def isLoss():
        pass
        
    def isWin():
        pass
    
    
