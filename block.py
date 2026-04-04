# module imports
import pygame

# item imports
from dataclasses import dataclass
from pygame import Clock, Font, Surface

# types
type BlockValue = int
type ColorTuple = tuple[int, int, int]

# config
BOARD_N: int = 4

# size constants
CELL_L: int = 100
CELL_PADDING: int = 5
BLOCK_L: int = CELL_L - (2 * CELL_PADDING)
BOARD_L: int = CELL_L * BOARD_N
WINDOW_PADDING: int = 10
WINDOW_L: int = BOARD_L + (2 * WINDOW_PADDING)

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


def draw_block(
    ctx: AppContext,
    board: Surface,
    value: BlockValue,
    row: int,
    col: int,
) -> None:
    # block
    cell_x = col * CELL_L
    cell_y = row * CELL_L
    cell: Surface = Surface((CELL_L, CELL_L))
    cell.fill(COLOR_BG)

    # get color
    colors = BLOCK_COLORS.get(value, BLOCK_COLORS[None])

    # draw block onto cell
    block: Surface = Surface((BLOCK_L, BLOCK_L))
    block.fill(colors[0])
    cell.blit(block, (CELL_PADDING, CELL_PADDING))

    # draw text onto cell
    text = ctx.block_text.get(value, ctx.block_text[None])
    text_rect = text.get_rect(center=(CELL_L / 2, CELL_L / 2))
    cell.blit(text, text_rect)

    # draw cell onto board
    board.blit(cell, (cell_x, cell_y))


def main() -> None:
    # init pygame
    pygame.init()

    # window's surface
    screen: Surface = pygame.display.set_mode((WINDOW_L, WINDOW_L))

    # initialize contect
    context = AppContext.new(
        block_text_font=pygame.font.SysFont("Arial", 32),
    )

    # initialize state
    state = AppState(
        running=True,
        clock=pygame.time.Clock(),
        dt=0.0,
        board=BoardState(
            n=4,
            board=[
                [2, 0, 0, 2],
                [0, 4, 32, 0],
                [0, 0, 8, 16],
                [2, 0, 8, 0],
            ],
        ),
    )

    # game loop
    while state.running:
        # update time delta
        state.dt = state.clock.tick(60) / 1000

        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in MOVE_KEYS["up"]:
                    state.board.move_up()
                elif event.key in MOVE_KEYS["down"]:
                    state.board.move_down()
                elif event.key in MOVE_KEYS["left"]:
                    state.board.move_left()
                elif event.key in MOVE_KEYS["right"]:
                    state.board.move_right()

        # fill screen with background
        screen.fill(COLOR_BG)

        # draw board
        board = Surface((BOARD_L, BOARD_L))
        board.fill(COLOR_BG)

        # draw blocks onto board
        for row_i in range(state.board.n):
            for col_i in range(state.board.n):
                draw_block(
                    context,
                    board,
                    state.board.board[row_i][col_i],
                    row_i,
                    col_i,
                )

        # draw board onto screen
        screen.blit(board, (WINDOW_PADDING, WINDOW_PADDING))

        # draw to display
        pygame.display.flip()

    # exit game
    pygame.quit()


# when run as script
if __name__ == "__main__":
    main()
