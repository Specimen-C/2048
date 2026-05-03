# item imports
from dataclasses import dataclass

# local item imports
from game import AgentGame
from gameState import Adversary
from agent import Agent


@dataclass(kw_only=True)
class TestHarness:
    num_runs: int
    board_size: int
    adversary_k: int
    max_depth: int
    max_iter: int

    @staticmethod
    def new(
        num_runs: int,
        board_size: int,
        adversary_k: int,
        max_depth: int,
        max_iter: int,
    ) -> TestHarness:
        return TestHarness(
            num_runs=num_runs,
            board_size=board_size,
            adversary_k=adversary_k,
            max_depth=max_depth,
            max_iter=max_iter,
        )

    def run(self) -> None:
        # create and run games
        completed_games: list[AgentGame] = []
        for i in range(self.num_runs):
            # create game
            game = AgentGame.new(
                self.board_size,
                Agent(
                    maxDepth=self.max_depth,
                    maxIter=self.max_iter,
                    name=f"Agent {i}",
                ),
                Adversary(self.adversary_k),
            )

            # run game
            while not game.isLoss():
                print(f"Game {i}: {game.score}".ljust(40), end="\r", flush=True)
                game.advance()

            # print final and push
            print(f"Game {i}: {game.score} (complete)".ljust(40))
            completed_games.append(game)

        # compute and print final outputs
        scores: list[int] = [game.score for game in completed_games]
        max_tiles: list[int] = [game.highest_tile for game in completed_games]

        print("---")
        print("Options:")
        print(f"Board Size: {self.board_size}")
        print(f"Adversary K: {self.adversary_k}")
        print(f"Max Depth: {self.max_depth}")
        print(f"Max Iterations: {self.max_iter}")
        print("---")
        print("Stats:")
        print(f"Runs: {self.num_runs}")
        print(f"Avg Score: {sum(scores) / len(scores)}")
        print(f"Max Score: {max(scores)}")
        print(f"Min Score: {min(scores)}")
        print(f"Overall Max Tile Value: {max(max_tiles)}")
