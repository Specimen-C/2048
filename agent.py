# module imports
import math
import random

# item imports
from action import Action
from dataclasses import InitVar, dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from gameState import GameState, Adversary


class AgentMode(Enum):
    RANDOM = auto()
    MONTE_CARLO = auto()


@dataclass(kw_only=True)
class Agent:
    # values passed into post init
    maxDepth: InitVar[int]
    maxIter: InitVar[int]

    # required values
    name: str

    # values with defaults
    gravestone: str = "Did their best."
    mode: AgentMode = AgentMode.MONTE_CARLO

    # set in post init
    born: datetime = field(init=False)
    tree: MCTree = field(init=False)
    death: datetime | None = field(init=False)

    def __post_init__(self, maxDepth: int, maxIter: int) -> None:
        self.death = None
        self.born = datetime.now()
        self.tree = MCTree(
            maxDepth=maxDepth,
            maxIter=maxIter,
        )

    def evaluate(self, gameState: GameState):
        val = 0
        board = gameState.board
        numTiles = 0
        sizeTiles = 0
        n = len(board)

        # find the max tile in board
        maxtile = 0
        for r in range(n):
            for c in range(n):
                tile = board[r][c]
                if tile != None and tile.value > maxtile:
                    maxtile = tile.value
                if tile != None:
                    numTiles += 1
                sizeTiles += 1

        # Reward max tile in corner
        if board[0][0] != None and board[0][0].value == maxtile:
            val += gameState.score * 200
        if board[0][n - 1] != None and board[0][n - 1].value == maxtile:
            val += gameState.score * 200
        if board[n - 1][0] != None and board[n - 1][0].value == maxtile:
            val += gameState.score * 200
        if board[n - 1][n - 1] != None and board[n - 1][n - 1].value == maxtile:
            val += gameState.score * 200

        # Reward monotonicity: tiles should decrease as you move away from max tile
        # Check rows (left-to-right and right-to-left)
        for r in range(n):
            for c in range(n - 1):
                left = board[r][c].value if board[r][c] != None else 0
                right = board[r][c + 1].value if board[r][c + 1] != None else 0
                if left >= right:
                    val += 1000
                if right >= left:
                    val += 1000

        # Check columns (top-to-bottom and bottom-to-top)
        for c in range(n):
            for r in range(n - 1):
                top = board[r][c].value if board[r][c] != None else 0
                bottom = board[r + 1][c].value if board[r + 1][c] != None else 0
                if top >= bottom:
                    val += 1000
                if bottom >= top:
                    val += 1000

        # Penalize trapped tiles (tiles not adjacent to similar values)
        for r in range(n):
            for c in range(n):
                tile = board[r][c]
                if tile == None:
                    continue

                # Check if this tile has any mergeable neighbors
                hasMatchingNeighbor = False
                neighbors = []

                # Check all 4 directions
                if r > 0:  # Up
                    neighbors.append(board[r - 1][c])
                if r < n - 1:  # Down
                    neighbors.append(board[r + 1][c])
                if c > 0:  # Left
                    neighbors.append(board[r][c - 1])
                if c < n - 1:  # Right
                    neighbors.append(board[r][c + 1])

                # Check if any neighbor is same value (can merge) or empty (can move)
                for neighbor in neighbors:
                    if neighbor == None:  # Empty space means not trapped
                        hasMatchingNeighbor = True
                        break
                    if neighbor.value == tile.value:  # Can merge
                        hasMatchingNeighbor = True
                        break

                # Penalize trapped tiles (bigger tiles get bigger penalties)
                if not hasMatchingNeighbor:
                    val -= tile.value * 0.5  # Scale penalty with tile value

        # Incentivize empty tiles (more empty = better)
        emptyTiles = sizeTiles - numTiles
        val += emptyTiles * gameState.score * 100000

        # Penalty for full board
        if numTiles == sizeTiles:
            val -= 200

        return val + gameState.score

    def getAction(self, state: GameState, adversary: Adversary) -> Action:
        """
        Given a gamestate, choose the next action.
        """

        # legal actions
        legalActions = state.getLegalActions()
        if not legalActions:
            raise Exception("No legal actions available")

        match self.mode:
            case AgentMode.RANDOM:
                return random.choice(state.getLegalActions())
            case AgentMode.MONTE_CARLO:
                return self.tree.search(state, self, adversary)

    @property
    def lifespan(self) -> timedelta | None:
        if self.death:
            return self.death - self.born
        else:
            return None


@dataclass(kw_only=True)
class MCTree:
    # values with defaults
    explorationFactor: float = 1.414
    maxDepth: int = 30
    maxIter: int = 100

    # set in post init
    qTable: dict[tuple[GameState, Action | None], float] = field(init=False)
    nTable: dict[tuple[GameState, Action | None], int] = field(init=False)

    def __post_init__(self) -> None:
        self.qTable = {}
        self.nTable = {}

    def search(self, state: GameState, agent: Agent, adversary: Adversary) -> Action:
        """
        Perform simulations and pick a next action given the current state.
        """
        
        self.qTable = {}
        self.nTable = {}

        # simulate forward a configured number of times
        for _ in range(self.maxIter):
            self.simulate(state, agent, adversary)

        # pick argmax from q table
        maxQ = float("-inf")
        maxAction: Action | None = None
        for action in state.getLegalActions():
            curQ = self.qTable.get((state, action), float("-inf"))
            if curQ >= maxQ:
                maxQ = curQ
                maxAction = action

        # ensure maxAction is not None
        if maxAction is None:
            raise Exception("Why'd you call search on a loss state, dumbass??")

        return maxAction

    def simulate(self, state: GameState, agent: Agent, adversary: Adversary) -> None:
        """
        Perform a simulation forward from the given state.
        """

        # choose first legal action
        action: Action | None = self.selectActionUCB(state)
        path: list[tuple[GameState, Action | None]] = []
        path.append((state, action))

        # simulate forward until a leaf node
        while action is not None and (state, action) in self.qTable:
            state = state.takeTurn(action, adversary)
            if len(state.getLegalActions()) != 0:
                action = self.selectActionUCB(state)
            else:
                action = None

            path.append((state, action))

        # rollout from that leaf node
        quality: float = self.rollout(state, agent, adversary)

        # back propagate the quality update
        for saPair in reversed(path):
            n = self.nTable.get(saPair, 0)
            self.qTable[saPair] = ((self.qTable.get(saPair, 0) * n) + quality) / (n + 1)
            self.nTable[saPair] = n + 1

    def selectActionUCB(self, state: GameState) -> Action:
        """
        Select an action for the given state using the UCB1 algorithm.
        """

        # all legal actions
        legalActions = state.getLegalActions()
        if not legalActions:
            raise Exception("No legal actions avalible")

        # if an action hasn't been tried, try it
        for action in legalActions:
            if (state, action) not in self.nTable:
                return action

        # ucb
        bestScore = float("-inf")
        bestAction = legalActions[0]
        totalVisits = sum(self.nTable.get((state, a), 0) for a in legalActions)

        # calculate ucb1 for each action
        for action in legalActions:
            q = self.qTable.get((state, action), 0)
            n = self.nTable.get((state, action), 1)

            # UCB1 formula: Q(s,a) + c * sqrt(ln(N) / n(s,a))
            score = q + self.explorationFactor * math.sqrt(
                math.log(totalVisits + 1) / n
            )

            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction

    def rollout(self, state: GameState, agent: Agent, adversary: Adversary) -> float:
        """
        Move randomly from the current state until the depth cutoff and return
        the q-score.
        """

        depth = self.maxDepth
        while depth > 0 and not state.isLoss():
            action = random.choice(state.getLegalActions())
            state = state.takeTurn(action, adversary)
            depth -= 1

        return agent.evaluate(state)
