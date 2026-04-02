
"""
Class to represent a tile on the board. Basically just a wrapper for int with some helpers

Fields:
    value: Represents the value of a tile
"""
@type
class TileClass:
    """
    Creates a new tile with default value of 2
    """    
    def __init__(self):
        self.value = 2
        
    """
    Creates a new tile with value val
    """    
    def __init__(self, val, gridX, gridY):
        self.value: int = val
        self.gridLocation: tuple[int, int] = (gridX, gridY)
        
    """
    Updates the value of the tile to value
    """
    def updateVal(self, value: int):
        self.value = value
        return
    
    """
    Moves the tile in the appropriate direction 
    """
    def move(self, direction):
        if direction == "up":
            self.gridY -= 1
        elif direction == "down":
            self.gridY += 1
        elif direction == "left":
            self.gridX -= 1
        elif direction == "right":
            self.gridY += 1
    