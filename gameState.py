from __future__ import annotations

from copy import deepcopy

# local item imports
from action import Action
from adversary import Adversary
from tile import Tile


class GameState:
    """
    Represents any one state of the 2048 game.
    Fields:
        list[list] board = nested lists containing the tile classes
        int score = Total score of the current board
        int freeSpaces = Number of board spaces not containing a tile
    """

    def __init__(self, n: int) -> None:
        """
        Default initializer. Instantiates all class variables for a empty
        GameState.
        """
        # Create original list
        board: list[list[Tile | None]] = list()
        for i in range(n):
            # Add n empty lists to each list in list
            self.board.append(list())
            for _ in range(n):
                self.board[i].append(None)

        # instance vars
        self.board: list[list[Tile | None]] = board
        self.score: int = 0
        self.n: int = n

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

    def _copy(self) -> GameState:
        """
        Create another instance of GameState from this GameState.
        """
        return deepcopy(self)

    def generateSuccessors(
        self,
        adversary: Adversary,
    ) -> dict[Action, list[tuple[float, GameState]]]:
        # TODO: implement
        raise NotImplementedError

    def move(self, action: Action, adversary: Adversary) -> GameState:
        # TODO: implement
        raise NotImplementedError

        for row in self.board:
            for tile in row:
                if not self.checkConflict(tile, action):
                    ...

    def _merge(self, tile1: Tile, tile2: Tile) -> None:
        # TODO: implement
        raise NotImplementedError

    def checkConflict(self, tile: Tile, action: Action) -> bool:
        # Find the first non empty slot
        if action is Action.UP:
            # Check top of column to tile (1, 2, TILE)
            for gridY in reversed(range(tile.y)):
                tileToCheck = self.board[tile.x][gridY]
                if tileToCheck is not None and tileToCheck.value == tile.value:
                    return True
            return False
        elif action is Action.DOWN:
            # Check tile + 1 to bottom of column (Tile, 3, 4)
            for gridY in range(tile.y + 1, len(self.board[tile.x])):
                tileToCheck = self.board[tile.x][gridY]
                if tileToCheck is not None and tileToCheck.value == tile.value:
                    return True
            return False
        elif action is Action.LEFT:
            # Check leftmost column to TILE (1, 2, Tile)
            for gridY in reversed(range(tile.x)):
                tileToCheck = self.board[tile.x][gridY]
                if tileToCheck is not None and tileToCheck.value == tile.value:
                    return True
            return False
        elif action is Action.RIGHT:
            # Check TILE + 1 to end of row (Tile, 3, 4)
            for gridY in range(tile.x + 1, len(self.board[tile.y])):
                tileToCheck = self.board[tile.x][gridY]
                if tileToCheck is not None and tileToCheck.value == tile.value:
                    return True
            return False

    def isLoss(self) -> bool:
        raise NotImplementedError

    def isWin(self) -> bool:
        raise NotImplementedError
