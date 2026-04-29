# module imports
import argparse
import pygame

# item imports
from dataclasses import dataclass
from pygame import Clock, Font, Surface

# local imports
from action import Action
from gameState import GameState, Adversary
from tile import Tile
from agent import Agent

# types
type ColorTuple = tuple[int, int, int]

# color constants
COLOR_FG_DARK: ColorTuple = (120, 111, 101)
COLOR_FG_LIGHT: ColorTuple = (250, 246, 243)
COLOR_BOARD_BG: ColorTuple = (187, 174, 161)
COLOR_BG: ColorTuple = (250, 248, 239)

# key mappings
KEYBINDS: dict[int, Action] = {
    pygame.K_w: Action.UP,
    pygame.K_s: Action.DOWN,
    pygame.K_a: Action.LEFT,
    pygame.K_d: Action.RIGHT,
    pygame.K_UP: Action.UP,
    pygame.K_DOWN: Action.DOWN,
    pygame.K_LEFT: Action.LEFT,
    pygame.K_RIGHT: Action.RIGHT,
}


def get_tile_colors(tile: Tile | None) -> tuple[ColorTuple, ColorTuple]:
    # no tile
    if tile is None:
        return ((204, 193, 180), (204, 193, 180)) 

    # tile with value
    match tile.value:
        case -1:
            return ((120, 12, 12), COLOR_FG_LIGHT)
        case 2:
            return ((239, 229, 218), COLOR_FG_DARK)
        case 4:
            return ((237, 225, 200), COLOR_FG_DARK)
        case 8:
            return ((242, 177, 122), COLOR_FG_LIGHT)
        case 16:
            return ((245, 150, 100), COLOR_FG_LIGHT)
        case 32:
            return ((247, 124, 97), COLOR_FG_LIGHT)
        case 64:
            return ((247, 94, 60), COLOR_FG_LIGHT)
        case 128:
            return ((237, 207, 115), COLOR_FG_LIGHT)
        case 256:
            return ((238, 204, 99), COLOR_FG_LIGHT)
        case 512:
            return ((237, 201, 80), COLOR_FG_LIGHT)
        case 1024:
            return ((237, 197, 63), COLOR_FG_LIGHT)
        case 2048:
            return ((237, 194, 46), COLOR_FG_LIGHT)
        case _:
            return ((62, 57, 51), COLOR_FG_LIGHT)


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

    BOARD_PADDING: int
    """
    Padding on each side of the board.
    """

    BOARD_L: int
    """
    Length (width and height) of the board.
    """

    STATUS_H: int
    """
    Height of the status area where the score is displayed
    """

    WINDOW_PADDING: int
    """
    Padding around each side of the display.
    """

    WINDOW_W: int
    """
    Width of the display.
    """

    WINDOW_H: int
    """
    Height of the display.
    """

    @staticmethod
    def new(board_n: int) -> AppConfig:
        # constants
        BOARD_N: int = board_n
        CELL_L: int = 100
        CELL_PADDING: int = 5
        BLOCK_L: int = CELL_L - (2 * CELL_PADDING)
        BOARD_PADDING: int = 5
        BOARD_L: int = (CELL_L * BOARD_N) + (2 * BOARD_PADDING)
        STATUS_H: int = 50
        WINDOW_PADDING: int = 10
        WINDOW_W: int = BOARD_L + (2 * WINDOW_PADDING)
        WINDOW_H: int = BOARD_L + STATUS_H + (3 * WINDOW_PADDING)

        return AppConfig(
            BOARD_N=BOARD_N,
            CELL_L=CELL_L,
            CELL_PADDING=CELL_PADDING,
            BLOCK_L=BLOCK_L,
            BOARD_L=BOARD_L,
            BOARD_PADDING=BOARD_PADDING,
            STATUS_H=STATUS_H,
            WINDOW_PADDING=WINDOW_PADDING,
            WINDOW_W=WINDOW_W,
            WINDOW_H=WINDOW_H,
        )


@dataclass(kw_only=True, frozen=True)
class AppContext:
    """
    Collection of prerendered assets and other memoized values. These values
    should be initialized once and should not change.
    """

    block_text: dict[int, Surface]
    """
    Collection of rendered text surfaces associated with a given block value.
    This text is pre-rendered for preformance reasons.
    """

    score_font: Font
    """
    The font used to render the score.
    """

    @staticmethod
    def new(block_text_font: Font, score_font: Font) -> AppContext:
        # generate block text
        block_text: dict[int, Surface] = {}
        
        #Add special rendered block for bomb tiles
        block_text[-1] = block_text_font.render("B", True, get_tile_colors(Tile.newWithoutLocation(-1))[1])
        
        i = 2
        while i <= 8192:
            block_text[i] = block_text_font.render(
                str(i), True, get_tile_colors(Tile.newWithoutLocation(i))[1]
            )
            i *= 2

        # return generated context
        return AppContext(
            block_text=block_text,
            score_font=score_font,
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

    game: GameState
    """
    The 2048 game's board state.
    """

    clock: Clock
    """
    The game clock.
    """
    
    player: bool
    """
    True when there is a player, and false when the agent is playing.
    """
    
    adversaryK: int
    """
    Represents the number of worst options the adversary can choose from.
    """
    

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
    def new(board_n: int, player: bool, k: int) -> App:
        # init pygame
        pygame.init()

        # init config
        cfg = AppConfig.new(board_n=board_n)

        # init context
        ctx = AppContext.new(
            block_text_font=pygame.font.SysFont("Arial", 32),
            score_font=pygame.font.SysFont("Arial", 32),
        )

        # init state
        state = AppState(
            running=True,
            clock=pygame.time.Clock(),
            dt=0.0,
            game=GameState.startState(cfg.BOARD_N, Adversary(k)),
            player = player, 
            adversaryK = k
        )

        # window's surface
        display_surf = pygame.display.set_mode((cfg.WINDOW_W, cfg.WINDOW_H))

        return App(
            display_surf=display_surf,
            cfg=cfg,
            ctx=ctx,
            state=state,
        )

    def run(self) -> None:
        
        #instantiate an agent instance (Random for now):
        agent = Agent("")
        adversary = Adversary(app.state.adversaryK)
        # agent.setRandom()
        agent.setAgent("MonteCarlo")
        moveTimer = 0.0
        moveDelay = 0
        
        # game loop
        while self.state.running:
            # update time delta
            self.state.dt = self.state.clock.tick(60) / 1000
            
            if self.state.player:
                #Process pygame events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.state.running = False
                    elif event.type == pygame.KEYDOWN:
                        #print("User pressed key")
                        user_action = KEYBINDS.get(event.key)
                        self.state.game = self.state.game.takeTurn(user_action, adversary)
                
            else:   
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.state.running = False
                #play game based on action from agent
                if (not self.state.game.isLoss()):
                    moveTimer += self.state.dt

                    if (moveTimer >= moveDelay):
                        moveTimer = 0.0
                        action = agent.getAction(self.state.game, adversary)
                        
                        print("CHOSEN ACTION: ", action)
                        
                        if action is not None:
                            self.state.game = self.state.game.takeTurn(action, adversary)
                            
            #Handle a loss
            if self.state.game.isLoss():
                print("You lost\nFinal State = ")
                self.state.game.printGameState()
                self.state.running = False

            # fill screen with background
            self.display_surf.fill(COLOR_BG)

            # draw status area & score
            status = Surface((self.cfg.BOARD_L, self.cfg.STATUS_H))
            status.fill(COLOR_BG)
            score = self.ctx.score_font.render(
                str(self.state.game.score),
                True,
                COLOR_FG_DARK,
            )
            score_rect = score.get_rect(
                center=(self.cfg.BOARD_L / 2, self.cfg.STATUS_H / 2)
            )
            status.blit(score, score_rect)

            # draw status area onto screen
            self.display_surf.blit(
                status,
                (
                    self.cfg.WINDOW_PADDING,
                    self.cfg.WINDOW_PADDING,
                    # self.cfg.BOARD_L + (2 * self.cfg.WINDOW_PADDING),
                ),
            )

            # draw board
            board = Surface((self.cfg.BOARD_L, self.cfg.BOARD_L))
            board.fill(COLOR_BG)
            pygame.draw.rect(
                board,
                COLOR_BOARD_BG,
                (0, 0, self.cfg.BOARD_L, self.cfg.BOARD_L),
                border_radius=8,
            )
            inner_board = Surface(
                (self.cfg.CELL_L * self.cfg.BOARD_N, self.cfg.CELL_L * self.cfg.BOARD_N)
            )

            # draw blocks onto board
            for row_i in range(self.state.game.n):
                for col_i in range(self.state.game.n):
                    self._draw_block(
                        inner_board,
                        self.state.game.board[row_i][col_i],
                        row_i,
                        col_i,
                    )

            # draw inner board to board and board onto screen
            board.blit(inner_board, (self.cfg.BOARD_PADDING, self.cfg.BOARD_PADDING))
            self.display_surf.blit(
                board,
                (
                    self.cfg.WINDOW_PADDING,
                    self.cfg.STATUS_H + (2 * self.cfg.WINDOW_PADDING),
                ),
            )

            # draw to display
            pygame.display.flip()
            
        self.state.running = True
        
        while self.state.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state.running = False
                    
        # exit game
        pygame.quit()

    def _draw_block(
        self,
        board: Surface,
        tile: Tile | None,
        row: int,
        col: int,
    ) -> None:
        # block
        cell_x = col * self.cfg.CELL_L
        cell_y = row * self.cfg.CELL_L
        cell: Surface = Surface((self.cfg.CELL_L, self.cfg.CELL_L))
        cell.fill(COLOR_BOARD_BG)

        # get color
        colors = get_tile_colors(tile)

        # draw block onto cell
        block: Surface = Surface((self.cfg.BLOCK_L, self.cfg.BLOCK_L))
        block.fill(colors[0])
        cell.blit(block, (self.cfg.CELL_PADDING, self.cfg.CELL_PADDING))

        # draw text onto cell
        if tile is not None:
            text = self.ctx.block_text.get(
                tile.value, self.ctx.block_text.get(tile.value)
            )
            if text is not None:
                text_rect = text.get_rect(
                    center=(self.cfg.CELL_L / 2, self.cfg.CELL_L / 2)
                )
                cell.blit(text, text_rect)

        # draw cell onto board
        board.blit(cell, (cell_x, cell_y))


# when run as script
if __name__ == "__main__":
    # create argparser
    parser = argparse.ArgumentParser(
        prog="block.py",
        description="A 2048 game demo",
    )
    parser.add_argument(
        "-n",
        "--board-size",
        help="size of the NxN board",
        default=4,
        type=int,
    )

    parser.add_argument(
        "-p", 
        "--player", 
        help="Use flag -p to allow player control",
        default=False, 
        type=bool
    )
    
    parser.add_argument(
        "-k", 
        help="Adversary picks randomly from top k worst placements",
        default=5, 
        type=int
    )
    # parse arguments
    args = parser.parse_args()

    # create & run app
    app = App.new(board_n=args.board_size, player=args.player, k=args.k)
    app.run()
