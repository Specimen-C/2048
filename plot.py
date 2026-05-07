# module imports
import json
import matplotlib.pyplot as plt
import pandas as pd

# item imports
from pathlib import Path

# constants
DATA_DIR = Path("tests")

# do script
if __name__ == "__main__":
    # create dataframes from each file
    frames = []
    for file in DATA_DIR.glob("*.json"):
        # get data
        with open(file) as f:
            data = json.load(f)

        # delete separate game scores
        del data["game_scores"]

        # load into dataframe and append
        df = pd.DataFrame([data])
        frames.append(df)

    # combine dataframes and filter
    df = pd.concat(frames, ignore_index=True)
    df = df[df["board_size"] == 4]
    df = df[df["agent_mode"] == "mc"]
    df = df[df["adversary_k"] == 10]
    df = df[df["num_runs"] == 10]

    # save csv of highest by avg
    sdf = df.sort_values("avg_score")
    sdf.to_csv("tmp.csv")
    print(sdf)

    # exploration factor, given d=5
    fig, ax = plt.subplots()
    for i in [50, 100, 200]:
        # filter df
        fdf = df[df["max_depth"] == 5]
        fdf = fdf[fdf["max_iter"] == i]

        # get x and y
        x = fdf["exploration_factor"]
        y = fdf["avg_score"]

        # plot
        ax.scatter(x, y, label=f"i={i}", alpha=0.6)
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.title("Average Score given Exploration Factor (d=5)")
    plt.xlabel("Exploration Factor")
    plt.xticks([0.2, 0.8, 1.4, 2.0])
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.savefig("plots/explortion-factor.png")
    plt.show()

    # depth, given C=0.8
    fig, ax = plt.subplots()
    for i in [50, 100, 200]:
        # filter df
        fdf = df[df["max_iter"] == i]
        fdf = fdf[fdf["exploration_factor"] == 0.8]
        fdf = fdf.groupby("max_depth", as_index=False)["avg_score"].mean()

        # get x and y
        x = fdf["max_depth"]
        y = fdf["avg_score"]

        # plot
        ax.scatter(x, y, label=f"i={i}", alpha=0.6)
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.title("Average Score given Depth (C=0.8)")
    plt.xlabel("Max Depth")
    plt.xticks([1, 5, 10, 20, 50])
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.savefig("plots/depth.png")
    plt.show()

    # iterations, given d=5
    fig, ax = plt.subplots()
    for c in [0.2, 0.8, 1.4, 2.0]:
        # filter df
        fdf = df[df["exploration_factor"] == c]
        fdf = fdf[fdf["max_depth"] == 5]

        # get x and y
        x = fdf["max_iter"]
        y = fdf["avg_score"]

        # plot
        plt.scatter(x, y, label=f"C={c}", alpha=0.6)
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.title("Average Score given Iterations (d=5)")
    plt.xlabel("Max Iteration")
    plt.xticks([50, 100, 200])
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.savefig("plots/iterations.png")
    plt.show()

    # model scores vs random scores
    with open("tests/2026-05-07T091403.json") as f:
        random_data = json.load(f)
    with open("tests/2026-05-07T093955.json") as f:
        best_data = json.load(f)

    random_df = pd.DataFrame(random_data)
    best_df = pd.DataFrame(best_data)

    # plot
    fig, ax = plt.subplots()
    plt.scatter(random_df.index, random_df["game_scores"], label="random", alpha=0.6)
    plt.plot(random_df.index, random_df["avg_score"], linestyle=":")
    plt.scatter(best_df.index, best_df["game_scores"], label="best", alpha=0.6)
    plt.plot(best_df.index, best_df["avg_score"], linestyle=":")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.title("Scores")
    plt.xlabel("Game")
    plt.ylabel("Score")
    plt.tight_layout()
    plt.savefig("plots/best.png")
    plt.show()
