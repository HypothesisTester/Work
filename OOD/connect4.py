import enum

class GridPosition(enum.Enum):
    EMPTY = 0,
    YELLOW = 1,
    RED = 2
    
class Grid:
    def __innit__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self.grid = None
        self.initGrid()
        
    def initGrid