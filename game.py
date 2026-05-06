# module imports
import numpy as np

# item imports
from abc import ABC
from dataclasses import dataclass

# local item imports
from action import Action
from agent import Agent
from gameState import Adversary, GameState, Tile


@dataclass(kw_only=True)
class Game(ABC):
    adversary: Adversary
    state: GameState

    @property
    def score(self) -> int:
        return self.state.score()

    @property
    def n(self) -> int:
        return self.state.n()

    @property
    def board(self) -> np.ndarray[tuple[int, int], np.dtype[Tile]]:
        return self.state.board()

    @property
    def highest_tile(self) -> Tile:
        return max([tile for list in self.state.board() for tile in list if tile])

    def isLoss(self) -> bool:
        return self.state.is_loss()


@dataclass(kw_only=True)
class AgentGame(Game):
    agent: Agent

    @staticmethod
    def new(n: int, agent: Agent, adversary: Adversary) -> AgentGame:
        return AgentGame(
            agent=agent,
            adversary=adversary,
            state=GameState.new(n, adversary),
        )

    def advance(self) -> None:
        """
        Make the agent choose and execute a next action.
        """
        action = self.agent.getAction(self.state, self.adversary)
        self.state = self.state.take_turn(action, self.adversary)


@dataclass(kw_only=True)
class PlayerGame(Game):
    adversary: Adversary
    state: GameState

    @staticmethod
    def new(n: int, adversary: Adversary) -> PlayerGame:
        return PlayerGame(
            adversary=adversary,
            state=GameState.new(n, adversary),
        )

    def move(self, action: Action) -> None:
        """
        Take the given action.
        """
        self.state = self.state.take_turn(action, self.adversary)
