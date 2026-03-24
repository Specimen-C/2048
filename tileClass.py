
"""
Class to represent a tile on the board. Basically just a wrapper for int with some helpers

Fields:
    value: Represents the value of a tile
"""
class tileClass:
    """
    Creates a new tile with default value of 2
    """    
    def __init__(self):
        self.value = 2
        
    """
    Creates a new tile with value val
    """    
    def __init__(self, val):
        self.value = val
        
    """
    Combines two tileClasses into one 
    """
    def merge(self, tileClass):
        pass