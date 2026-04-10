from dataclasses import dataclass


@dataclass
class Tile:
    value: int
    location: tuple[int, int]

    @property
    def x(self) -> int:
        return self.location[0]

    @property
    def y(self) -> int:
        return self.location[1]
