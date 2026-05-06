# module imports
import json

# item imports
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

# local item imports
from agent import Agent, AgentMode
from game import AgentGame
from gameState import Adversary


@dataclass
class TestResult:
    # stats
    board_size: int
    agent_mode: str
    adversary_k: int
    max_depth: int
    max_iter: int
    num_runs: int
    avg_score: float
    max_score: int
    min_score: int
    max_tile: int

    # games
    game_scores: list[int]

    @staticmethod
    def new(
        board_size: int,
        agent_mode: AgentMode,
        adversary_k: int,
        max_depth: int,
        max_iter: int,
        num_runs: int,
        games: list[AgentGame],
    ) -> TestResult:
        scores: list[int] = [game.score for game in games]
        max_tiles: list[int] = [game.highest_tile for game in games]
        return TestResult(
            board_size=board_size,
            agent_mode=agent_mode.value,
            adversary_k=adversary_k,
            max_depth=max_depth,
            max_iter=max_iter,
            num_runs=num_runs,
            avg_score=sum(scores) / len(scores),
            max_score=max(scores),
            min_score=min(scores),
            max_tile=max(max_tiles),
            game_scores=scores,
        )

    def save(self) -> Path:
        testfile = Path(f"tests/{datetime.now().strftime('%Y-%m-%dT%H%M%S')}.json")
        testfile.parent.mkdir(parents=True, exist_ok=True)
        with open(testfile, "x") as file:
            json.dump(asdict(self), file)
        return testfile

    def print(self) -> None:
        print("Options:")
        print(f"Board Size: {self.board_size}")
        print(f"Agent Mode: {self.agent_mode}")
        print(f"Adversary K: {self.adversary_k}")
        print(f"Max Depth: {self.max_depth}")
        print(f"Max Iterations: {self.max_iter}")
        print("---")
        print("Stats:")
        print(f"Runs: {self.num_runs}")
        print(f"Avg Score: {self.avg_score}")
        print(f"Max Score: {self.max_score}")
        print(f"Min Score: {self.min_score}")
        print(f"Overall Max Tile Value: {self.max_tile}")


@dataclass(kw_only=True)
class TestHarness:
    num_runs: int
    board_size: int
    agent_mode: AgentMode
    adversary_k: int
    max_depth: int
    max_iter: int

    @staticmethod
    def new(
        num_runs: int,
        board_size: int,
        agent_mode: AgentMode,
        adversary_k: int,
        max_depth: int,
        max_iter: int,
    ) -> TestHarness:
        return TestHarness(
            num_runs=num_runs,
            board_size=board_size,
            agent_mode=agent_mode,
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
                    mode=self.agent_mode,
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
        res = TestResult.new(
            self.board_size,
            self.agent_mode,
            self.adversary_k,
            self.max_depth,
            self.max_iter,
            self.num_runs,
            completed_games,
        )
        print("---")
        res.print()
        testfile = res.save()
        print("---")
        print(f"Results saved to {testfile}")
