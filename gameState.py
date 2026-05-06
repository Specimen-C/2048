# module imports
import numpy as np
import random

# local item imports
from action import Action
from dataclasses import dataclass

# type definitions
Tile = np.uint32


@dataclass(frozen=True)
class AdversaryPlacement:
    tile: Tile
    pos: tuple[int, int]


@dataclass(frozen=True)
class AdversarySuccessor:
    score: float
    placement: AdversaryPlacement


@dataclass(kw_only=True)
class Adversary:
    k: int
    domain: set[Tile]

    #
    # general helpers
    #

    @staticmethod
    def _check_merge(
        state: GameState,
        tile: Tile,
        col: int,
        row: int,
    ) -> int:
        # count
        conflicts = 0

        # check values in col
        for val in state.col(col):
            if val == tile:
                conflicts += 1

        # check values in row
        for val in state.row(row):
            if val == tile:
                conflicts += 1

        return conflicts

    @staticmethod
    def _manhattan_dist(xy1: tuple[int, int], xy2: tuple[int, int]) -> int:
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

    @staticmethod
    def _clutter_factor(state: GameState, xy: tuple[int, int]) -> float:
        factor = 0.0
        for row_idx in range(state.n()):
            for col_idx in range(state.n()):
                if state.board()[row_idx, col_idx] != 0:
                    factor += Adversary._manhattan_dist(xy, (row_idx, col_idx))
        return factor / (state.n() * state.n())

    #
    # constructors
    #

    @staticmethod
    def new(
        k: int,
        domain: set[Tile],
    ) -> Adversary:
        return Adversary(
            k=k,
            domain=domain,
        )

    #
    # main public api functionality
    #

    def possible_placements(
        self,
        state: GameState,
    ) -> list[AdversaryPlacement]:
        # empties
        empties = state.empty_positions()
        if not empties:
            return []

        # score canidate successors
        candidates: list[AdversarySuccessor] = []
        for x, y in empties:
            for tile in self.domain:
                merge_penalty = Adversary._check_merge(state, tile, y, x)
                clutter_factor = Adversary._clutter_factor(state, (x, y))
                score = merge_penalty + clutter_factor
                candidates.append(
                    AdversarySuccessor(score, AdversaryPlacement(tile, (x, y)))
                )

        # sort highest first
        candidates.sort(key=lambda x: x.score, reverse=True)

        # keep only top-k
        candidates = candidates[: self.k] if self.k > 0 else candidates
        return [x.placement for x in candidates]

    def get_placement(
        self,
        state: GameState,
    ) -> AdversaryPlacement | None:
        # get k-placements
        placements = self.possible_placements(state)
        if not placements:
            return None

        # pick one
        return random.choice(placements)


@dataclass(kw_only=True)
class GameState:
    # state values
    _board: np.ndarray[tuple[int, int], np.dtype[Tile]]
    _score: int
    _n: int

    # cached values
    _legal_actions: set[Action] | None = None
    _hash: int | None = None

    #
    # general helpers
    #

    def _row(self, r: int) -> np.ndarray[tuple[int], np.dtype[Tile]]:
        """
        A view of a single row in the board.
        """
        return self._board[r]

    def _col(self, c: int) -> np.ndarray[tuple[int], np.dtype[Tile]]:
        """
        A view of a single column in the board.
        """
        return self._board[:, c]

    def _rows(self) -> list[np.ndarray[tuple[int], np.dtype[Tile]]]:
        """
        Views of each row in the board.
        """
        return [self._row(n) for n in range(self._n)]

    def _cols(self) -> list[np.ndarray[tuple[int], np.dtype[Tile]]]:
        """
        Views of each column in the board.
        """
        return [self._col(n) for n in range(self._n)]

    def _line_would_change(
        self,
        line: np.ndarray[tuple[int], np.dtype[Tile]],
    ) -> bool:
        seen_empty: bool = False
        prev_tile: Tile | None = None
        for tile in line:
            if tile == 0:
                seen_empty = True
            else:
                # tile can move into empty
                if seen_empty:
                    return True

                # adjacent tiles can merge
                if prev_tile is not None and prev_tile == tile:
                    return True

                # update prev_tile
                prev_tile = tile

        # no changes
        return False

    #
    # cache helpers
    #

    def _calc_legal_actions(self) -> set[Action]:
        legal: set[Action] = set()
        for action in Action:
            match action:
                case Action.LEFT:
                    if any(self._line_would_change(row) for row in self._rows()):
                        legal.add(action)
                case Action.RIGHT:
                    if any(self._line_would_change(row[::-1]) for row in self._rows()):
                        legal.add(action)
                case Action.UP:
                    if any(self._line_would_change(col) for col in self._cols()):
                        legal.add(action)
                case Action.DOWN:
                    if any(self._line_would_change(col[::-1]) for col in self._cols()):
                        legal.add(action)
        return legal

    #
    # mutation helpers (ONLY USE IN CONSTRUCTOR FUNCTIONS)
    #

    @staticmethod
    def _mut_merge_line(
        view: np.ndarray[tuple[int], np.dtype[Tile]],
    ) -> int:
        # derive values
        n = len(view)
        score = 0

        # remove empty blocks
        line: list[Tile] = [tile for tile in view if tile != 0]

        # merge adjacents
        for i in range(1, len(line)):
            if line[i - 1] != 0 and line[i - 1] == line[i]:
                new_tile = line[i - 1] * 2
                line[i - 1] = new_tile
                line[i] = Tile(0)
                score += int(new_tile)

        # remove empty blocks again
        line = [tile for tile in line if tile != 0]

        # pad with empties
        for _ in range(n - len(line)):
            line.append(Tile(0))

        # write back to view
        for i in range(n):
            view[i] = line[i]

        return score

    def _mut_perform_move(self, action: Action) -> None:
        # update based on action
        match action:
            case Action.UP:
                for col in self._cols():
                    # merge
                    self._score += GameState._mut_merge_line(col)
            case Action.DOWN:
                for col in self._cols():
                    # reverse & merge
                    self._score += GameState._mut_merge_line(col[::-1])
            case Action.LEFT:
                for row in self._rows():
                    # merge
                    self._score += GameState._mut_merge_line(row)
            case Action.RIGHT:
                for row in self._rows():
                    # reverse & merge
                    self._score += GameState._mut_merge_line(row[::-1])

        self._legal_actions = None
        self._hash = None

    def _mut_place_tile(self, adversary: Adversary) -> None:
        # get adversary placement
        placement = adversary.get_placement(self)
        if placement is None:
            return

        # make placement
        self._board[placement.pos[0], placement.pos[1]] = placement.tile

    #
    # constructors
    #

    @staticmethod
    def new_empty(n: int) -> GameState:
        return GameState(
            _board=np.zeros((n, n), dtype=Tile),
            _score=0,
            _n=n,
        )

    @staticmethod
    def new(n: int, adversary: Adversary) -> GameState:
        state = GameState.new_empty(n)
        state._mut_place_tile(adversary)
        return state

    #
    # general public api methods
    #

    def score(self) -> int:
        return self._score

    def n(self) -> int:
        return self._n

    def board(self) -> np.ndarray[tuple[int, int], np.dtype[Tile]]:
        """
        A read-only view of the board.
        """
        view = self._board.view()
        view.flags.writeable = False
        return view

    def row(self, r: int) -> np.ndarray[tuple[int], np.dtype[Tile]]:
        """
        A read-only view of a single row in the board.
        """
        view = self._board[r]
        view.flags.writeable = False
        return view

    def col(self, c: int) -> np.ndarray[tuple[int], np.dtype[Tile]]:
        """
        A read-only view of a single column in the board.
        """
        view = self._board[:, c]
        view.flags.writeable = False
        return view

    def rows(self) -> list[np.ndarray[tuple[int], np.dtype[Tile]]]:
        """
        Read-only views of each row in the board.
        """
        return [self.row(n) for n in range(self._n)]

    def cols(self) -> list[np.ndarray[tuple[int], np.dtype[Tile]]]:
        """
        Read-only views of each column in the board.
        """
        return [self.col(n) for n in range(self._n)]

    def empty_positions(self) -> list[tuple[int, int]]:
        return [
            (x, y)
            for x in range(self._n)
            for y in range(self._n)
            if self._board[x][y] == 0
        ]

    def is_loss(self) -> bool:
        # skip expensive comp if needed
        if len(self.empty_positions()) != 0:
            return False

        # do expensive comp action
        return len(self.legal_actions()) == 0

    def take_turn(
        self,
        action: Action,
        adversary: Adversary,
    ) -> GameState:
        # create new state
        new_state = GameState(
            _board=self._board.copy(),
            _score=self._score,
            _n=self._n,
        )

        # do move and place tile
        new_state._mut_perform_move(action)
        new_state._mut_place_tile(adversary)

        return new_state

    #
    # cached public api methods
    #

    def legal_actions(self) -> set[Action]:
        # calc if needed
        if not self._legal_actions:
            self._legal_actions = self._calc_legal_actions()

        # return cached
        return self._legal_actions

    #
    # magic methods
    #

    def __eq__(self, state: object) -> bool:
        if not state:
            return False

        if not isinstance(state, GameState):
            raise TypeError(
                f"Cannot compare an object of type {state.__class__.__name__} to {self.__class__.__name__}"
            )

        return hash(self) == hash(state)

    def __hash__(self) -> int:
        if not self._hash:
            self._hash = hash((self._board.tobytes(), self._score, self._n))
        return self._hash


class MutableGameState(GameState):
    #
    # constructors
    #

    @staticmethod
    def from_state(state: GameState) -> MutableGameState:
        return MutableGameState(
            _board=state._board.copy(),
            _score=state._score,
            _n=state._n,
        )

    #
    # methods
    #

    def mut_take_turn(
        self,
        action: Action,
        adversary: Adversary,
    ) -> None:
        self._mut_perform_move(action)
        self._mut_place_tile(adversary)

    #
    # magic methods
    #

    def __hash__(self) -> int:
        raise TypeError("Cannot hash a mutable game state!")
