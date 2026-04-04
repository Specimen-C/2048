# module imports
import pygame
import random

# item imports
from dataclasses import dataclass
from pygame import Clock, Font, Surface

# types
type BlockValue = int
type ColorTuple = tuple[int, int, int]

# color constants
COLOR_FG_DARK: ColorTuple = (120, 111, 101)
COLOR_FG_LIGHT: ColorTuple = (250, 246, 243)
COLOR_BG: ColorTuple = (187, 174, 161)

# key mappings
MOVE_KEYS: dict[str, list[int]] = {
    "up": [pygame.K_w, pygame.K_UP],
    "down": [pygame.K_s, pygame.K_DOWN],
    "left": [pygame.K_a, pygame.K_LEFT],
    "right": [pygame.K_d, pygame.K_RIGHT],
}

# color mappings
BLOCK_COLORS: dict[BlockValue | None, tuple[ColorTuple, ColorTuple]] = {
    0: ((204, 193, 180), (204, 193, 180)),
    2: ((239, 229, 218), COLOR_FG_DARK),
    4: ((237, 225, 200), COLOR_FG_DARK),
    8: ((242, 177, 122), COLOR_FG_LIGHT),
    16: ((245, 150, 100), COLOR_FG_LIGHT),
    32: ((247, 124, 97), COLOR_FG_LIGHT),
    64: ((247, 94, 60), COLOR_FG_LIGHT),
    128: ((237, 207, 115), COLOR_FG_LIGHT),
    256: ((238, 204, 99), COLOR_FG_LIGHT),
    512: ((237, 201, 80), COLOR_FG_LIGHT),
    1024: ((237, 197, 63), COLOR_FG_LIGHT),
    2048: ((237, 194, 46), COLOR_FG_LIGHT),
    None: ((62, 57, 51), COLOR_FG_LIGHT),
}


@dataclass(kw_only=True, frozen=True)
class AppConfig:
    """
    Configuration given at application start via command line arguments and not
    changed throughout the app lifecycle.
    """

    BOARD_N: int
    """
    The size of the NxN board
    """

    CELL_L: int
    """
    Length (width and height) of a cell.
    """

    CELL_PADDING: int
    """
    Amount of inner padding on each side of a cell.
    """

    BLOCK_L: int
    """
    Length (width and height) of a block.
    """

    BOARD_L: int
    """
    Length (width and height) of the board.
    """

    WINDOW_PADDING: int
    """
    Padding around each side of the display.
    """

    WINDOW_L: int
    """
    Length (width and height) of the display.
    """

    @staticmethod
    def new(board_n: int) -> AppConfig:
        # constants
        BOARD_N: int = board_n
        CELL_L: int = 100
        CELL_PADDING: int = 5
        BLOCK_L: int = CELL_L - (2 * CELL_PADDING)
        BOARD_L: int = CELL_L * BOARD_N
        WINDOW_PADDING: int = 10
        WINDOW_L: int = BOARD_L + (2 * WINDOW_PADDING)

        return AppConfig(
            BOARD_N=BOARD_N,
            CELL_L=CELL_L,
            CELL_PADDING=CELL_PADDING,
            BLOCK_L=BLOCK_L,
            BOARD_L=BOARD_L,
            WINDOW_PADDING=WINDOW_PADDING,
            WINDOW_L=WINDOW_L,
        )


@dataclass(kw_only=True, frozen=True)
class AppContext:
    """
    Collection of prerendered assets and other memoized values. These values
    should be initialized once and should not change.
    """

    block_text: dict[BlockValue | None, Surface]
    """
    Collection of rendered text surfaces associated with a given block value.
    This text is pre-rendered for preformance reasons.
    """

    @staticmethod
    def new(block_text_font: Font) -> AppContext:
        # generate block text
        block_text: dict[BlockValue | None, Surface] = {}
        for key, val in BLOCK_COLORS.items():
            block_text[key] = block_text_font.render(str(key), True, val[1])

        # return generated context
        return AppContext(
            block_text=block_text,
        )


@dataclass(kw_only=True)
class AppState:
    """
    Collection of all mutable app state.
    """

    running: bool
    """
    Whether the application is running or not. When `False` the program should
    exit.
    """

    dt: float
    """
    The amount of time in seconds since the last frame was rendered.
    """

    board: BoardState
    """
    The 2048 game's board state.
    """

    clock: Clock
    """
    The game clock.
    """


@dataclass(kw_only=True)
class BoardState:
    """
    State of the 2048 board.
    """

    n: int
    """
    The width of the square board.
    """

    board: list[list[BlockValue]]
    """
    A 2D array representing the values on the board. Indexed with
    `board[row][col]`.
    """

    @staticmethod
    def new(n: int) -> BoardState:
        state = BoardState(
            n=n,
            board=[[0 for _ in range(n)] for _ in range(n)],
        )
        state._add_tile()
        state._add_tile()
        return state

    def move_up(self) -> None:
        for col_i in range(self.n):
            # generate column without empty blocks
            col = [
                self.board[row_i][col_i]
                for row_i in range(self.n)
                if self.board[row_i][col_i] != 0
            ]

            # merge adjacents
            for i in range(1, len(col)):
                if col[i - 1] == col[i]:
                    col[i - 1] *= 2
                    col[i] = 0

            # remove empty blocks from merge
            col = [val for val in col if val != 0]

            # pad with 0s
            for _ in range(self.n - len(col)):
                col.append(0)

            # write back to grid
            for row_i in range(self.n):
                self.board[row_i][col_i] = col[row_i]

        # add tile
        self._add_tile()

    def move_down(self) -> None:
        for col_i in range(self.n):
            # generate reverse column without empty blocks
            col = [
                self.board[row_i][col_i]
                for row_i in range(self.n)
                if self.board[row_i][col_i] != 0
            ]
            col = list(reversed(col))

            # merge adjacents
            for i in range(1, len(col)):
                if col[i - 1] == col[i]:
                    col[i - 1] *= 2
                    col[i] = 0

            # remove empty blocks from merge
            col = [val for val in col if val != 0]

            # pad with 0s
            for _ in range(self.n - len(col)):
                col.append(0)

            # re-reverse col
            col = list(reversed(col))

            # write back to grid
            for row_i in range(self.n):
                self.board[row_i][col_i] = col[row_i]

        # add tile
        self._add_tile()

    def move_left(self) -> None:
        for row_i in range(self.n):
            # generate row without empty blocks
            row = [
                self.board[row_i][col_i]
                for col_i in range(self.n)
                if self.board[row_i][col_i] != 0
            ]

            # merge adjacents
            for i in range(1, len(row)):
                if row[i - 1] == row[i]:
                    row[i - 1] *= 2
                    row[i] = 0

            # remove empty blocks from merge
            row = [val for val in row if val != 0]

            # pad with 0s
            for _ in range(self.n - len(row)):
                row.append(0)

            # write back to grid
            for col_i in range(self.n):
                self.board[row_i][col_i] = row[col_i]

        # add tile
        self._add_tile()

    def move_right(self) -> None:
        for row_i in range(self.n):
            # generate row without empty blocks
            row = [
                self.board[row_i][col_i]
                for col_i in range(self.n)
                if self.board[row_i][col_i] != 0
            ]
            row = list(reversed(row))

            # merge adjacents
            for i in range(1, len(row)):
                if row[i - 1] == row[i]:
                    row[i - 1] *= 2
                    row[i] = 0

            # remove empty blocks from merge
            row = [val for val in row if val != 0]

            # pad with 0s
            for _ in range(self.n - len(row)):
                row.append(0)

            # re-reverse rol
            row = list(reversed(row))

            # write back to grid
            for col_i in range(self.n):
                self.board[row_i][col_i] = row[col_i]

        # add tile
        self._add_tile()

    def _add_tile(self) -> None:
        # get all empty cells
        empty_cells = [
            (row_i, col_i)
            for row_i in range(self.n)
            for col_i in range(self.n)
            if self.board[row_i][col_i] == 0
        ]

        # skip adding if board is full
        if len(empty_cells) == 0:
            return

        # pick random cell
        row_i, col_i = random.choice(empty_cells)

        # place a 2 block here
        self.board[row_i][col_i] = 2


@dataclass(kw_only=True)
class App:
    """
    All logic pertaining to running of the application.
    """

    cfg: AppConfig
    """
    Static application configuration.
    """

    ctx: AppContext
    """
    Static assets and other memoized values.
    """

    state: AppState
    """
    Mutable application state.
    """

    display_surf: Surface
    """
    The root display surface.
    """

    @staticmethod
    def new(board_n: int) -> App:
        # init pygame
        pygame.init()

        # init config
        cfg = AppConfig.new(board_n=board_n)

        # init context
        ctx = AppContext.new(
            block_text_font=pygame.font.SysFont("Arial", 32),
        )

        # init state
        state = AppState(
            running=True,
            clock=pygame.time.Clock(),
            dt=0.0,
            board=BoardState.new(cfg.BOARD_N),
        )

        # window's surface
        display_surf = pygame.display.set_mode((cfg.WINDOW_L, cfg.WINDOW_L))

        return App(
            display_surf=display_surf,
            cfg=cfg,
            ctx=ctx,
            state=state,
        )

    def run(self) -> None:
        # game loop
        while self.state.running:
            # update time delta
            self.state.dt = self.state.clock.tick(60) / 1000

            # process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in MOVE_KEYS["up"]:
                        self.state.board.move_up()
                    elif event.key in MOVE_KEYS["down"]:
                        self.state.board.move_down()
                    elif event.key in MOVE_KEYS["left"]:
                        self.state.board.move_left()
                    elif event.key in MOVE_KEYS["right"]:
                        self.state.board.move_right()

            # fill screen with background
            self.display_surf.fill(COLOR_BG)

            # draw board
            board = Surface((self.cfg.BOARD_L, self.cfg.BOARD_L))
            board.fill(COLOR_BG)

            # draw blocks onto board
            for row_i in range(self.state.board.n):
                for col_i in range(self.state.board.n):
                    self._draw_block(
                        board,
                        self.state.board.board[row_i][col_i],
                        row_i,
                        col_i,
                    )

            # draw board onto screen
            self.display_surf.blit(
                board, (self.cfg.WINDOW_PADDING, self.cfg.WINDOW_PADDING)
            )

            # draw to display
            pygame.display.flip()

        # exit game
        pygame.quit()

    def _draw_block(
        self,
        board: Surface,
        value: BlockValue,
        row: int,
        col: int,
    ) -> None:
        # block
        cell_x = col * self.cfg.CELL_L
        cell_y = row * self.cfg.CELL_L
        cell: Surface = Surface((self.cfg.CELL_L, self.cfg.CELL_L))
        cell.fill(COLOR_BG)

        # get color
        colors = BLOCK_COLORS.get(value, BLOCK_COLORS[None])

        # draw block onto cell
        block: Surface = Surface((self.cfg.BLOCK_L, self.cfg.BLOCK_L))
        block.fill(colors[0])
        cell.blit(block, (self.cfg.CELL_PADDING, self.cfg.CELL_PADDING))

        # draw text onto cell
        text = self.ctx.block_text.get(value, self.ctx.block_text[None])
        text_rect = text.get_rect(center=(self.cfg.CELL_L / 2, self.cfg.CELL_L / 2))
        cell.blit(text, text_rect)

        # draw cell onto board
        board.blit(cell, (cell_x, cell_y))


# when run as script
if __name__ == "__main__":
    app = App.new(4)
    app.run()
