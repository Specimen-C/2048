# module imports
import math
import random

# item imports
from action import Action
from dataclasses import InitVar, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from gameState import Adversary, GameState, MutableGameState, Tile


class AgentMode(Enum):
    RANDOM = "random"
    MONTE_CARLO = "mc"


@dataclass(kw_only=True)
class Agent:
    # values passed into post init
    maxDepth: InitVar[int]
    maxIter: InitVar[int]
    explorationFactor: InitVar[float]

    # required values
    name: str

    # values with defaults
    gravestone: str = "Did their best."
    mode: AgentMode = AgentMode.MONTE_CARLO

    # set in post init
    born: datetime = field(init=False)
    tree: MCTree = field(init=False)
    death: datetime | None = field(init=False)

    def __post_init__(
        self,
        maxDepth: int,
        maxIter: int,
        explorationFactor: float,
    ) -> None:
        self.death = None
        self.born = datetime.now()
        self.tree = MCTree(
            maxDepth=maxDepth,
            maxIter=maxIter,
            explorationFactor=explorationFactor,
        )

    def evaluate(self, gameState: GameState) -> float:
        return evaluate_02(self, gameState)

    def getAction(self, state: GameState, adversary: Adversary) -> Action:
        """
        Given a gamestate, choose the next action.
        """

        # legal actions
        legalActions = state.legal_actions()
        if not legalActions:
            raise Exception("No legal actions available")

        match self.mode:
            case AgentMode.RANDOM:
                return random.choice(list(legalActions))
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
        for action in state.legal_actions():
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
            state = state.take_turn(action, adversary)
            if len(state.legal_actions()) != 0:
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
        legalActions = list(state.legal_actions())
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
        mutstate = MutableGameState.from_state(state)
        prevAction: Action | None = None
        while depth > 0 and not mutstate.is_loss():
            action = rollout_action_02(mutstate, agent, adversary, prevAction)
            mutstate.mut_take_turn(action, adversary)
            depth -= 1

        return agent.evaluate(mutstate)


def rollout_action_01(
    state: GameState,
    agent: Agent,
    adversary: Adversary,
) -> Action:
    return max(
        state.legal_actions(),
        key=lambda a: agent.evaluate(GameState.take_turn(state, a, adversary)),
    )


def rollout_action_02(
    state: GameState,
    agent: Agent,
    adversary: Adversary,
    prevAction: Action | None,
) -> Action:
    legalActions = state.legal_actions()
    wantedAction = Action.LEFT if prevAction is Action.UP else Action.UP
    if wantedAction in legalActions:
        return wantedAction
    else:
        orderedActions = [Action.UP, Action.LEFT, Action.RIGHT, Action.DOWN]
        for action in orderedActions:
            if action in legalActions:
                return action
    raise Exception("No avlaibile actions")


def evaluate_01(_: Agent, state: GameState) -> float:
    val = 0.0
    board = state.board()
    numTiles = 0
    sizeTiles = 0
    n = len(board)

    # find the max tile in board
    maxtile = Tile(0)
    for r in range(n):
        for c in range(n):
            tile: Tile = board[r, c]
            if tile > maxtile:
                maxtile = tile
            if tile != 0:
                numTiles += 1
            sizeTiles += 1

    # Reward max tile in corner
    if board[0, 0] == maxtile:
        val += state.score() * 200
    if board[0, n - 1] == maxtile:
        val += state.score() * 200
    if board[n - 1, 0] == maxtile:
        val += state.score() * 200
    if board[n - 1, n - 1] == maxtile:
        val += state.score() * 200

    # Reward monotonicity: tiles should decrease as you move away from max tile
    # Check rows (left-to-right and right-to-left)
    for r in range(n):
        for c in range(n - 1):
            left: Tile = board[r, c]
            right: Tile = board[r, c + 1]
            if left >= right:
                val += 1000
            if right >= left:
                val += 1000

    # Check columns (top-to-bottom and bottom-to-top)
    for c in range(n):
        for r in range(n - 1):
            top: Tile = board[r, c]
            bottom: Tile = board[r + 1, c]
            if top >= bottom:
                val += 1000
            if bottom >= top:
                val += 1000

    # Penalize trapped tiles (tiles not adjacent to similar values)
    for r in range(n):
        for c in range(n):
            tile = board[r, c]
            if tile == 0:
                continue

            # Check if this tile has any mergeable neighbors
            hasMatchingNeighbor = False
            neighbors: list[Tile] = []

            # Check all 4 directions
            if r > 0:  # Up
                neighbors.append(board[r - 1, c])
            if r < n - 1:  # Down
                neighbors.append(board[r + 1, c])
            if c > 0:  # Left
                neighbors.append(board[r, c - 1])
            if c < n - 1:  # Right
                neighbors.append(board[r, c + 1])

            # Check if any neighbor is same value (can merge) or empty (can move)
            for neighbor in neighbors:
                if neighbor == 0:  # Empty space means not trapped
                    hasMatchingNeighbor = True
                    break
                if neighbor == tile:  # Can merge
                    hasMatchingNeighbor = True
                    break

            # Penalize trapped tiles (bigger tiles get bigger penalties)
            if not hasMatchingNeighbor:
                val -= tile * 0.5  # Scale penalty with tile value

    # Incentivize empty tiles (more empty = better)
    emptyTiles = sizeTiles - numTiles
    val += emptyTiles * state.score() * 100000

    # Penalty for full board
    if numTiles == sizeTiles:
        val -= 200

    return val + state.score()


def evaluate_02(_: Agent, state: GameState) -> float:
    if state.is_loss():
        return -100_000_000 + (1 / math.log2(state.score()))
    else:
        return math.log2(state.score() if state.score() > 0 else 1)
