from action import Action 
from agent import Agent
from gameState import GameState
from tile import Tile
from abc import ABC, abstractmethod
from dataclasses import dataclass


'''- Add an adversary = (YG)
    - Scores positions for new tiles
    - Picks randomly from the top `k` places'''

'''

'''

@dataclass
class Adversary(ABC):
    # @abstractmethod
    #float = "score" of tile
    #list of probabilities and 
    def getEmpty(self, state:GameState) -> list:
        emptyCells = [
            (rowIdx, colIdx)
            for rowIdx in range(state.n)
            for colIdx in range(state.n)
            if state.board[rowIdx][colIdx] is None
        ]

        # skip adding if board is full
        if len(emptyCells) == 0:
            return []
        return emptyCells

    def evaluateState(self, state: GameState):
        options = getEmpty(self, state)

    #checks if same tile exists in 
    def checkMerge(self, state:GameState, tile: Tile) -> int:
        value = tile.value
        location = tile.location
        numConflicts = 0

        #check all values in same column
        for r in range( state.n):
            if state.board[r][tile.col] == value and r != tile.row:
                numConflicts+=1

        for c in range( state.n):
            if state.board[tile.row][c] == value and c != tile.col:
                numConflicts+=1

        return numConflicts

    def manhattanDistance(xy1, xy2):
        "Returns the Manhattan distance between points xy1 and xy2"
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

    #returns sum of manhattan distance to every other tile on board
    #iterate through all tile spaces on board. if not none, then find manhattan distance and sum to total
    def clutterFactor(self, state:GameState, tile:Tile) -> int:
        location = tile.location
        clutterSum = 0
        for rowIdx in range(state.n):
            for colIdx in range(state.n):
                if state.board[rowIdx][colIdx] is not None:
                    clutterSum += manhattanDistance(tile.location, (rowIdx, colIdx))
        return clutterSum


    #list of tuples:(probabilities, states)
    def generateSuccessors(self, state: GameState , value:int ) -> list[tuple[float, GameState]]:
        state = deepcopy(state)

        #stolen from han
        # create copy of state
        # state = deepcopy(state)
        

        # get all empty cells
        emptyCells = [
            (rowIdx, colIdx)
            for rowIdx in range(state.n)
            for colIdx in range(state.n)
            if state.board[rowIdx][colIdx] is None
        ]
        options = {}
        lowest = -1
        clutterOptions = []
        
        # skip adding if board is full
        if len(emptyCells) == 0:
            return state

        for cell in emptyCells:
            tile = Tile(value, cell[0], cell[1])
            options[(cell[0], cell[1])] = (checkMerge(state, tile) + (clutterFactor(state, tile) / (n*n)))
        
        returnList = []

        for rowIdx in range(state.n):
            for colIdx in range(state.n):
                if state.board[rowIdx][colIdx] is not None:
                    #zero probability to place tile in spot that already has tile
                    returnList.append(0, state)
                else:
                    tile = Tile(value, rowIdx, colIdx)
                    state.board[rowIdx][colIdx] = Tile(value=tileValue, row=rowIdx, col=colIdx)
                    returnList.append(options[tile.row, tile.col], state)
        return returnList
        #     if (lowest > options[cell]):
        #         lowest = options[cell]
        # print(options)
        # for cell in emptyCells:
        #     if options[cell] == lowest:
        #         clutterOptions.append(cell)

        
        #what makes a choice to place a tile?
        #evaluate the current score
        #evaluate the empty spaces and where the most tiles are clustered?
        # raise NotImplementedError

    @abstractmethod
    def getPlacement(self, state: GameState) -> GameState:
        #stolen from han
        #this is what is actually called to place a tile in the gameboard
        # create copy of state
        state = deepcopy(state)

        # get all empty cells
        emptyCells = [
            (rowIdx, colIdx)
            for rowIdx in range(state.n)
            for colIdx in range(state.n)
            if state.board[rowIdx][colIdx] is None
        ]

        # skip adding if board is full
        if len(emptyCells) == 0:
            return state

        # pick random cell, value
        rowIdx, colIdx = random.choice(emptyCells)

        #THIS GETS REPLACED WITH THE "TOP" K CHOICES FROM GENERATESUCCESSORS?
        tileValueChoices = [2,4]

        #tileValue = random.choice(tileValueChoices)
        choices = []
        actualChoices = []
        for i in range(len(tileValueChoices)):
            choices.append(self.generateSuccessors(state,tileValueChoices[i] ))

        for choice in choices:
            if choice[0] != 0:
                actualChoices.append(choice)
        # place a block from the domain here
        #state.board[rowIdx][colIdx] = Tile(value=tileValue, row=rowIdx, col=colIdx)
        retValue = random.choice(actualChoices)
        return retValue[1]

        #raise NotImplementedError

