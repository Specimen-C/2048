# item imports
from argparse import ArgumentParser, Namespace

# local item imports
from agent import AgentMode
from app import App
from test import TestHarness


def run(args: Namespace) -> None:
    # parser
    parser: ArgumentParser = args.parser

    # global args
    board_size: int = args.board_size
    adversary_k: int = args.adversary_k
    max_depth: int = args.max_depth
    max_iter: int = args.max_iter
    agent_mode: AgentMode = AgentMode(args.agent_mode)

    # run args
    no_graphics: bool = args.no_graphics
    player: bool = args.player
    time_between_moves: float | None = args.time_between_moves

    # ensure valid
    if no_graphics and player:
        parser.error("unable to run with no graphics as a player-game")

    # create and run app
    app = App.new(
        board_size=board_size,
        player=player,
        agent_mode=agent_mode,
        adversary_k=adversary_k,
        max_depth=max_depth,
        max_iter=max_iter,
        time_between_moves=time_between_moves,
    )
    app.run()


def test(args: Namespace) -> None:
    # global args
    board_size: int = args.board_size
    adversary_k: int = args.adversary_k
    max_depth: int = args.max_depth
    max_iter: int = args.max_iter
    agent_mode: AgentMode = AgentMode(args.agent_mode)

    # test args
    num_runs: int = args.num_runs

    # create and run test harness
    harness = TestHarness.new(
        num_runs=num_runs,
        board_size=board_size,
        agent_mode=agent_mode,
        adversary_k=adversary_k,
        max_depth=max_depth,
        max_iter=max_iter,
    )
    harness.run()


# when run as script
if __name__ == "__main__":
    # create argparser
    parser = ArgumentParser(
        prog="block.py",
        description="A 2048 game and simulator.",
    )
    parser.add_argument(
        "-n",
        "--board-size",
        help="size of the NxN board (default: 4)",
        default=4,
        type=int,
        dest="board_size",
    )
    parser.add_argument(
        "-k",
        "--adversary-k",
        help="make adversary pick randomly from top k worst placements (default: 5)",
        default=5,
        type=int,
        dest="adversary_k",
    )
    parser.add_argument(
        "-d",
        "--max-depth",
        help="max depth to rollout (default: 10)",
        default=10,
        type=int,
        dest="max_depth",
    )
    parser.add_argument(
        "-i",
        "--max-iter",
        help="max number of iterations when simulating (default: 50)",
        default=50,
        type=int,
        dest="max_iter",
    )
    parser.add_argument(
        "-a",
        "--agent-mode",
        help="the mode for the agent to run in (default: mc)",
        default="mc",
        choices=["mc", "random"],
        dest="agent_mode",
    )
    subparsers = parser.add_subparsers(
        required=True,
        dest="command",
    )

    # run command
    run_parser = subparsers.add_parser("run", help="run 2048 with a player or agent")
    run_parser.add_argument(
        "-g",
        "--no-graphics",
        help="use a no graphics simulation",
        action="store_true",
        dest="no_graphics",
    )
    run_parser.add_argument(
        "-p",
        "--player",
        help="allow user control",
        action="store_true",
        dest="player",
    )
    run_parser.add_argument(
        "-t",
        "--time-between-moves",
        help="min number of seconds between turns (default: none)",
        default=None,
        type=float,
        dest="time_between_moves",
    )
    run_parser.set_defaults(func=run)
    run_parser.set_defaults(parser=run_parser)

    # test command
    test_parser = subparsers.add_parser("test", help="run the testing harness")
    test_parser.add_argument(
        "-r",
        "--num-runs",
        help="number of tests to perform (default: 5)",
        default=5,
        type=int,
        dest="num_runs",
    )
    test_parser.set_defaults(func=test)
    test_parser.set_defaults(parser=test_parser)

    # parse args & run associated
    args = parser.parse_args()
    args.func(args)
