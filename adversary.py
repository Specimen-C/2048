from action import Action 
from agent import Agent


'''- Add an adversary = (YG)
    - Scores positions for new tiles
    - Picks randomly from the top `k` places'''

'''

'''
@dataclass
class Adversary(Adversary):
    @abstractmethod
    #float = "score" of tile

    def generateSuccessors(self, state: GameState) -> list[tuple[float, GameState]]:
        # state.

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

        # skip adding if board is full
        if len(emptyCells) == 0:
            return state


        #what makes a choice to place a tile?
        #evaluate the current score
        #evaluate the empty spaces and where the most tiles are clustered?
        raise NotImplementedError

    @abstractmethod
    def getPlacement(self, state: GameState) -> GameState:
        #stolen from han
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

        tileValue = random.choice(tileValueChoices)

        # place a block from the domain here
        state.board[rowIdx][colIdx] = Tile(value=tileValue, row=rowIdx, col=colIdx)

        return state

        #raise NotImplementedError

