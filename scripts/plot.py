# module imports
import json
import matplotlib.pyplot as plt
import numpy as np
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

    # combine dataframes
    df = pd.concat(frames, ignore_index=True)

    # exploration factor
    fig, ax = plt.subplots()
    for max_iter in [50, 100, 200, 400, 800]:
        for max_depth in [1, 5, 10, 20, 50]:
            # filter df
            fdf = df[df["max_depth"] == max_depth]
            fdf = fdf[fdf["max_iter"] == max_iter]

            # get x and y
            x = fdf["exploration_factor"]
            y = fdf["avg_score"]

            # plot
            ax.scatter(
                x,
                y,
                label=f"i={max_iter},d={max_depth}",
            )
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()

    # depth, given exploration factor = 0.8
    fig, ax = plt.subplots()
    for max_iter in [50, 100, 200, 400, 800]:
        # filter df
        fdf = df[df["max_iter"] == max_iter]
        fdf = fdf[fdf["exploration_factor"] == 0.8]

        # get x and y
        x = fdf["max_depth"]
        y = fdf["avg_score"]

        # plot
        ax.scatter(x, y, label=f"i={max_iter}")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.title("Average Score per Depth, C = 0.8")
    plt.xlabel("Max Depth")
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.show()

    # iterations, given exploration factor = 0.8
    fig, ax = plt.subplots()
    for max_depth in [1, 5, 10, 20, 50]:
        # filter df
        fdf = df[df["max_depth"] == max_depth]
        fdf = fdf[fdf["exploration_factor"] == 0.8]

        # get x and y
        x = fdf["max_iter"]
        y = fdf["avg_score"]

        # plot
        plt.scatter(x, y, label=f"d={max_depth}")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.title("Average Score per Iteration, C = 0.8")
    plt.xlabel("Max Iteration")
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.show()

    # hist of avg score across all
    plt.hist(df["avg_score"])
    plt.show()
