from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class Action(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


@dataclass
class Adversary(ABC):
    @abstractmethod
    def generateSuccessors(self, state: GameState) -> list[tuple[float, GameState]]:
        raise NotImplementedError

    @abstractmethod
    def getPlacement(self, state: GameState) -> GameState:
        raise NotImplementedError


@dataclass
class Agent(ABC):
    name: str
    gravestone: str
    born: datetime
    death: datetime

    @property
    def lifespan(self) -> timedelta:
        return self.death - self.born

    def evaluate(self, state: GameState) -> float:
        raise NotImplementedError

    def getAction(self, state: GameState) -> Action:
        raise NotImplementedError


@dataclass
class Tile:
    value: int
    location: tuple[int, int]


@dataclass
class GameState:
    board: list[list[Tile | None]]
    score: int

    @property
    def emptySpaces(self) -> int:
        raise NotImplementedError

    def generateSuccessors(
        self,
        adversary: Adversary,
    ) -> dict[Action, list[tuple[float, GameState]]]:
        raise NotImplementedError

    def move(self, action: Action, adversary: Adversary) -> GameState:
        raise NotImplementedError

    def _merge(self, tile1: Tile, tile2: Tile) -> None:
        raise NotImplementedError
