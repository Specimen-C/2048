# item imports
from argparse import ArgumentParser

# local item imports
from block import App, NoGraphicsApp

# when run as script
if __name__ == "__main__":
    # create argparser
    parser = ArgumentParser(
        prog="block.py",
        description="A 2048 game and simulator.",
    )
    parser.add_argument(
        "-g",
        "--no-graphics",
        help="use a no graphics simulation",
        action="store_true",
        dest="no_graphics",
    )
    parser.add_argument(
        "-n",
        "--board-size",
        help="size of the NxN board",
        default=4,
        type=int,
        dest="board_size",
    )
    parser.add_argument(
        "-p",
        "--player",
        help="allow user control",
        action="store_true",
        dest="player",
    )
    parser.add_argument(
        "-k",
        "--adversary-k",
        help="make adversary pick randomly from top k worst placements",
        default=5,
        type=int,
        dest="adversary_k",
    )
    parser.add_argument(
        "-d",
        "--max-depth",
        help="max depth to rollout",
        default=10,
        type=int,
        dest="max_depth",
    )
    parser.add_argument(
        "-i",
        "--max-iter",
        help="max number of iterations when simulating",
        default=50,
        type=int,
        dest="max_iter",
    )
    parser.add_argument(
        "-t",
        "--time-between-moves",
        help="max number of iterations when simulating",
        default=None,
        type=float,
        dest="time_between_moves",
    )

    # parse arguments
    args = parser.parse_args()
    board_size: int = args.board_size
    player: bool = args.player
    adversary_k: int = args.adversary_k
    no_graphics: bool = args.no_graphics
    max_depth: int = args.max_depth
    max_iter: int = args.max_iter
    time_between_moves: float | None = args.time_between_moves

    # ensure valid
    if no_graphics and player:
        parser.error("unable to run with no graphics as a player-game")

    # create & run app
    app: App | NoGraphicsApp
    if not no_graphics:
        app = App.new(
            board_size=board_size,
            player=player,
            adversary_k=adversary_k,
            max_depth=max_depth,
            max_iter=max_iter,
            time_between_moves=time_between_moves,
        )
    else:
        app = NoGraphicsApp.new(
            board_n=board_size,
            k=adversary_k,
        )

    # run
    app.run()
