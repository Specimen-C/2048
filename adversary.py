from abc import ABC, abstractmethod
from dataclasses import dataclass
from gameState import GameState


@dataclass
class Adversary(ABC):
    @abstractmethod
    def generateSuccessors(self, state: GameState) -> list[tuple[float, GameState]]:
        raise NotImplementedError

    @abstractmethod
    def getPlacement(self, state: GameState) -> GameState:
        raise NotImplementedError
