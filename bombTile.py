from tile import Tile

class BombTile(Tile):
    
    def __init__(self, value, x, y):
        super().__init__(value, x, y)
    
    def __str__(self):
        return "Bomb" + super().__str__()
    