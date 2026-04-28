from tile import Tile

class BombTile(Tile):
    
    def __init__(self, value, row, col):
        super().__init__(value, row, col)
    
    def __str__(self):
        return "Bomb" + super().__str__()
    