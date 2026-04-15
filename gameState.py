# module imports
import random

# item imports
from copy import deepcopy

# local item imports
from abc import ABC, abstractmethod
from action import Action
from dataclasses import dataclass
from tile import Tile


'''@dataclass
class Adversary(ABC):
    @abstractmethod
    #float = "score" of tile

    def generateSuccessors(self, state: GameState) -> list[tuple[float, GameState]]:
        successors = []
        
        # get all empty cells
        emptyCells = [
            (rowIdx, colIdx)
            for rowIdx in range(state.n)
            for colIdx in range(state.n)
            if state.board[rowIdx][colIdx] is None
        ]
        if len(emptyCells) == 0:
            return state
        return emptyCells

        # raise NotImplementedError

    @abstractmethod
    def getPlacement(self, state: GameState) -> GameState:
        #stolen from han
        # create copy of state
        # state = deepcopy(state)

        # # get all empty cells
        # emptyCells = [
        #     (rowIdx, colIdx)
        #     for rowIdx in range(state.n)
        #     for colIdx in range(state.n)
        #     if state.board[rowIdx][colIdx] is None
        # ]

        # # skip adding if board is full
        # if len(emptyCells) == 0:
        #     return state

        # # pick random cell, value
        # rowIdx, colIdx = random.choice(emptyCells)
        # tileValueChoices = [2,4]
        # tileValue = random.choice(tileValueChoices)

        # # place a block from the domain here
        # state.board[rowIdx][colIdx] = Tile(value=tileValue, row=rowIdx, col=colIdx)

        # return state

        raise NotImplementedError'''
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
        # state.

        #check all values in same column
        for r in range(0, state.n):
            if state.board[r][tile.col] is not None :
                
                if state.board[r][tile.col].value == value and r != tile.row:
                    numConflicts+=1

        for c in range(0, state.n):
            if state.board[tile.row][c] is not None :
                if state.board[tile.row][c].value == value and c != tile.col:
                    numConflicts+=1

        return numConflicts

    def manhattanDistance(self, xy1, xy2):
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
                    clutterSum += self.manhattanDistance((tile.row, tile.col), (rowIdx, colIdx))
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
            options[(cell[0], cell[1])] = (self.checkMerge(state, tile) + (self.clutterFactor(state, tile) / (state.n*state.n)))
        
        returnList = []

        for rowIdx in range(state.n):
            for colIdx in range(state.n):
                if state.board[rowIdx][colIdx] is not None:
                    #zero probability to place tile in spot that already has tile
                    returnList.append((0, state))
                else:
                    tile = Tile(value, rowIdx, colIdx)
                    state.board[rowIdx][colIdx] = Tile(value=value, row=rowIdx, col=colIdx)
                    returnList.append((options[tile.row, tile.col], state))
        # print(returnList)
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

    # @abstractmethod
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
        # for i in range(len(tileValueChoices)):
        #     choices.append(self.generateSuccessors(state,tileValueChoices[i] ))
        choices = self.generateSuccessors(state,tileValueChoices[0] )
        # print(choices)
        # print("length?", len(choices))
        for choice in choices:
            print("inside cforst c/hoice ")
            print("choice[0]", choice[0])
            if choice[0] != 0 or choice[0] != 0.0:
                print("inside choice ")
                actualChoices.append(choice)
        # # place a block from the domain here
        # print(choices[1][1])
        # print("huh", choices[1])

        # state.board[actualChoices[1].][choices[1][1]] = Tile(value=tileValueChoices[0], row=choices[1][0], col=choices[1][1])
        # retValue = actualChoices[0]
        # return state #choices[1][1]
        if len(actualChoices) == 0:
            return choices[0][1]
        return actualChoices[0][1]



# @dataclass(init=False)
# class DummyAdversary(Adversary):
#     def generateSuccessors(self, state: GameState) -> list[tuple[float, GameState]]:
#         raise NotImplementedError

#     def getPlacement(self, state: GameState) -> GameState:
#         # create copy of state
#         state = deepcopy(state)

#         # get all empty cells
#         emptyCells = [
#             (rowIdx, colIdx)
#             for rowIdx in range(state.n)
#             for colIdx in range(state.n)
#             if state.board[rowIdx][colIdx] is None
#         ]

#         # skip adding if board is full
#         if len(emptyCells) == 0:
#             return state

#         # pick random cell
#         rowIdx, colIdx = random.choice(emptyCells)

#         # place a block from the domain here
#         state.board[rowIdx][colIdx] = Tile(value=2, row=rowIdx, col=colIdx)

#         return state


@dataclass(init=False)
class GameState:
    """
    Represents any one state of the 2048 game.
    """

    #
    # fields
    #

    board: list[list[Tile | None]]
    """
    Nested lists containing the tile objects.
    """

    score: int
    """
    Total score of the current board.
    """

    n: int
    """
    Size of the NxN board.
    """

    #
    # dynamic properties
    #

    @property
    def emptySpaces(self) -> int:
        """
        Number of empty spaces on the board.
        """
        count: int = 0
        for row in self.board:
            for tile in row:
                if tile is None:
                    count += 1
        return count

    #
    # constructors
    #

    def __init__(self, n: int) -> None:
        """
        Default initializer. Instantiates all class variables for a empty
        GameState of size n.
        """
        # Create original list
        self.board = list()
        for i in range(n):
            # Add n empty lists to each list in list
            self.board.append(list())
            for _ in range(n):
                self.board[i].append(None)

        # instance vars
        self.score = 0
        self.n = n

    @staticmethod
    def startState(n: int, adversary: Adversary) -> GameState:
        """
        Create a new random start state.
        """
        state = GameState(n)
        state = adversary.getPlacement(state)
        return state

    #
    # api methods
    #

    def generateSuccessors(
        self,
        adversary: Adversary,
    ) -> dict[Action, list[tuple[float, GameState]]]:
        # TODO: implement
        raise NotImplementedError

    def move(self, action: Action, adversary: Adversary) -> GameState:
        """
        Generate a new GameState from a given action. New tile(s) are then
        placed by the given adversary.
        """

        # create copy of new state
        newState = self._copy()

        # merge based on action
        match action:
            case Action.UP:
                for colIdx in range(newState.n):
                    # generate col
                    col = [
                        newState.board[rowIdx][colIdx] for rowIdx in range(newState.n)
                    ]

                    # merge
                    col, addScore = GameState._mergeLine(col)

                    # write back to grid
                    newState.score += addScore
                    for rowIdx in range(newState.n):
                        newState.board[rowIdx][colIdx] = col[colIdx]
            case Action.DOWN:
                for colIdx in range(self.n):
                    # generate reverse col
                    col = [
                        newState.board[rowIdx][colIdx] for rowIdx in range(newState.n)
                    ]
                    col.reverse()

                    # merge and rereverse
                    col, addScore = GameState._mergeLine(col)
                    col.reverse()

                    # write back to grid
                    newState.score += addScore
                    for rowIdx in range(newState.n):
                        newState.board[rowIdx][colIdx] = col[rowIdx]
            case Action.LEFT:
                for rowIdx in range(self.n):
                    # generate row
                    row = [
                        newState.board[rowIdx][colIdx] for colIdx in range(newState.n)
                    ]

                    # merge
                    row, addScore = GameState._mergeLine(row)

                    # write back to grid
                    newState.score += addScore
                    for colIdx in range(newState.n):
                        newState.board[rowIdx][colIdx] = row[colIdx]
            case Action.RIGHT:
                for rowIdx in range(self.n):
                    # generate reverse row
                    row = [
                        newState.board[rowIdx][colIdx] for colIdx in range(newState.n)
                    ]
                    row.reverse()

                    # merge and rereverse
                    row, addScore = GameState._mergeLine(row)
                    row.reverse()

                    # write back to grid
                    newState.score += addScore
                    for colIdx in range(newState.n):
                        newState.board[rowIdx][colIdx] = row[colIdx]

        # update locations
        for rowIdx in range(newState.n):
            for colIdx in range(newState.n):
                # get tile
                tile = newState.board[rowIdx][colIdx]
                if tile is None:
                    continue

                # update tile
                tile.location = (rowIdx, colIdx)

        # add tile
        newState = adversary.getPlacement(newState)
        newState
        return newState

    def isLoss(self) -> bool:
        if self.emptySpaces == 0:
            return False

        for action in self.getLegalActions():
            # TODO Get real adversary or add movement logic here
            newState = self.move(action, DummyAdversary())
            if newState != self:
                return False

        return True

    def getLegalActions(self) -> list[Action]:
        raise NotImplementedError

    def printGameState(self) -> None:
        print("Current score = " + str(self.score))
        for row in self.board:
            for tile in row:
                print(" | " + str(tile) + " | ")
            print("\n")

    def __eq__(self, state: object) -> bool:

        if not isinstance(state, GameState):
            raise TypeError("Can only compare GameStates to other GameStates")

        if self.score != state.score:
            return False

        for rowIndex, row in enumerate(self.board):
            for colIndex, tile in enumerate(row):
                if tile != state.board[rowIndex][colIndex]:
                    return False

        return True

    #
    # helper methods
    #

    def _copy(self) -> GameState:
        """
        Create another instance of GameState from this GameState.
        """
        return deepcopy(self)

    #
    # helper functions
    #

    @staticmethod
    def _mergeLine(line: list[Tile | None]) -> tuple[list[Tile | None], int]:
        """
        Merge tiles in line and return the new line and the amount of score
        gained.
        """

        # derive values
        n = len(line)
        score = 0

        # remove empty blocks
        line = [tile for tile in line if tile is not None]

        # merge adjacents
        for i in range(1, len(line)):
            if line[i - 1] is not None and line[i - 1].value == line[i].value:  # type: ignore
                newTile: Tile = deepcopy(line[i - 1])  # type: ignore
                newTile.value *= 2
                newTile.location = None
                line[i - 1] = newTile
                line[i] = None
                score += newTile.value

        # remove empty blocks again
        line = [tile for tile in line if tile is not None]

        # pad with empties
        for _ in range(n - len(line)):
            line.append(None)

        return (line, score)
