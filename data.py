# local item import
from agent import AgentMode
from test import TestHarness

# constants
N = 10
K = 10

# do script
if __name__ == "__main__":
    for max_iter in [50, 100, 200, 400, 800]:
        for max_depth in [1, 5, 10, 20, 50]:
            for exploration_factor in [0.2, 0.8, 1.4, 2.0]:
                harness = TestHarness.new(
                    num_runs=N,
                    board_size=4,
                    agent_mode=AgentMode.MONTE_CARLO,
                    adversary_k=K,
                    max_depth=max_depth,
                    max_iter=max_iter,
                    exploration_factor=exploration_factor,
                )
                harness.run()
