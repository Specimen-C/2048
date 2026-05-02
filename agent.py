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
    mode: AgentMode = AgentMode.RANDOM

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

    def evaluate(self, state: GameState) -> float:
        """
        Score a given gamestate.
        """

        if state.isLoss():
            return float(state.score) ** -1
        else:
            return float(state.score)

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
    explorationFactor: float = 0.5
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
