# item imports
from abc import ABC
from dataclasses import dataclass

# local item imports
from action import Action
from agent import Agent
from gameState import GameState, Adversary
from tile import Tile


@dataclass(kw_only=True)
class Game(ABC):
    adversary: Adversary
    state: GameState

    @property
    def score(self) -> int:
        return self.state.score

    @property
    def n(self) -> int:
        return self.state.n

    @property
    def board(self) -> list[list[Tile | None]]:
        return self.state.board

    def isLoss(self) -> bool:
        return self.state.isLoss()


@dataclass(kw_only=True)
class AgentGame(Game):
    agent: Agent

    @staticmethod
    def new(n: int, agent: Agent, adversary: Adversary) -> AgentGame:
        return AgentGame(
            agent=agent,
            adversary=adversary,
            state=GameState.startState(n, adversary),
        )

    def advance(self) -> None:
        """
        Make the agent choose and execute a next action.
        """
        action = self.agent.getAction(self.state, self.adversary)
        self.state = self.state.takeTurn(action, self.adversary)


@dataclass(kw_only=True)
class PlayerGame(Game):
    adversary: Adversary
    state: GameState

    @staticmethod
    def new(n: int, adversary: Adversary) -> PlayerGame:
        return PlayerGame(
            adversary=adversary,
            state=GameState.startState(n, adversary),
        )

    def move(self, action: Action) -> None:
        """
        Take the given action.
        """
        self.state = self.state.takeTurn(action, self.adversary)
