from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Tile:
    value: int 
    location: tuple[int, int] | None
    
    def __init__(self, value: int,  x: int, y: int):
        """
        Creates a new tile
        
        Fields:
            int value = The face value of a tile
            int x = The x location of a tile on the board
            int y = The y location of a tile on the board
        """
        self.value = value
        self.location = (x, y)
    
    def copy(self) -> Tile:
        """
        Returns a deep copy of the calling tile
        """
        return deepcopy(self)

    @property
    def x(self) -> int | None:
        if self.location is None:
            return None
        return self.location[0]

    @property
    def y(self) -> int:
        if self.location is None:
            return None
        return self.location[1]
    
    def updateValue(self, value: int):
        """
        Updates the value of the tile to value
        
        Fields:
            value: int = The value that we want to make the Tile
        """
        if value is None or type(value) != int:
            raise ValueError("Tile must be an int")
        if value < 0:
            raise ValueError("Tile cannot have a negative value")

        # Check if value is a power of two with bit masks.
        # Since a power of two has only one bit set to on, 
        # we can bitwise and with 1 - value, and that will
        # be 0 if only one bit was on
        if (value & (value - 1)) != 0:
            return ValueError("Tile must be a power of two")
        
        self.value = value
        return

    def __str__(self):
        return "Location = " + str(self.location) + ": " + str(self.value)