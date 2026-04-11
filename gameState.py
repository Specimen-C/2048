# module imports
import random

# item imports
from copy import deepcopy

# local item imports
from abc import ABC, abstractmethod
from action import Action
from dataclasses import dataclass
from tile import Tile


@dataclass
class Adversary(ABC):
    @abstractmethod
    def generateSuccessors(self, state: GameState) -> list[tuple[float, GameState]]:
        raise NotImplementedError

    @abstractmethod
    def getPlacement(self, state: GameState) -> GameState:
        raise NotImplementedError


@dataclass
class DummyAdversary(Adversary):
    def generateSuccessors(self, state: GameState) -> list[tuple[float, GameState]]:
        raise NotImplementedError

    def getPlacement(self, state: GameState) -> GameState:
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

        # pick random cell
        rowIdx, colIdx = random.choice(emptyCells)

        # place a block from the domain here
        state.board[rowIdx][colIdx] = Tile(value=2, row=rowIdx, col=colIdx)

        return state


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
