from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Tile:
    value: int
    """
    Tile's numeric value.
    """

    location: tuple[int, int] | None
    """
    Tile's location on the board (if it has one). This is the index of the row
    followed by the index of the column.
    """

    def __init__(self, value: int, row: int, col: int):
        """
        Creates a new tile

        Fields:
            int value = The face value of a tile
            int row = The row index of a tile on the board
            int col = The column index of a tile on the board
        """
        self.value = value
        self.location = (row, col)

    @staticmethod
    def newWithoutLocation(value: int) -> Tile:
        tile = Tile(value, 0, 0)
        tile.location = None
        return tile

    def copy(self) -> Tile:
        """
        Returns a deep copy of the calling tile
        """
        return deepcopy(self)

    @property
    def row(self) -> int | None:
        if self.location is None:
            return None
        return self.location[0]

    @property
    def col(self) -> int | None:
        if self.location is None:
            return None
        return self.location[1]

    def updateValue(self, value: int) -> None:
        """
        Updates the value of the tile to value

        Fields:
            value: int = The value that we want to make the Tile
        """
        if value is None or type(value) is not int:
            raise ValueError("Tile must be an int")
        if value < 0:
            raise ValueError("Tile cannot have a negative value")

        # Check if value is a power of two with bit masks.
        # Since a power of two has only one bit set to on,
        # we can bitwise and with 1 - value, and that will
        # be 0 if only one bit was on
        if (value & (value - 1)) != 0:
            raise ValueError("Tile must be a power of two")

        self.value = value

    def __str__(self) -> str:
        return "Tile Location = " + str(self.location) + ": " + str(self.value)

    def __eq__(self, tile: object) -> bool:
        if tile is None:
            return False
        # ensure input in another tile
        if not isinstance(tile, Tile):
            #return False
            raise TypeError("You tried to compare a " + str(type(tile)) + ". Can only compare tiles to other tiles!")

        # check values
        if tile.location != self.location:
            return False
        if tile.value != self.value:
            return False

        return True
