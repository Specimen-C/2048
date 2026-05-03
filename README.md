## Scope increase ideas

- Larger board
- Additional mechanics (Random tile swaps/Tile value changes)
- Adversary mechanics (A minimizing agent that attempts to add specific tiles to
  mess the player up)
- Increasing randomness by having larger domain for random tile adds
- Bomb tiles (Merging tiles deletes them, but also lowers score)
- Beer tiles (Merging a beer tile makes your next move have a probability of
  going in a different direction)

## Project Structure

- `action.py`
  - `Action`: enum of possible actions
- `agent.py`
  - `Agent`: 2048-playing agent
  - `AgentMode`: enum of modes (policies) for the agent
- `app.py`
  - `App`: class containing the ui app logic
- `game.py`
  - `AgentGame`: 2048 played by an agent
  - `PlayerGame`: 2048 played by a user
- `gameState.py`
  - `Adversary`: adversary which places new tiles on the board
  - `GameState`: representation of the game board
- `main.py`: entry into the program
- `test.py`
  - `TestHarness`: class supporting running tests
- `tile.py`
  - `Tile`: class representing a tile on the board


## Running the Program

This project manages dependencies with [`uv`](https://docs.astral.sh/uv/). Make
sure this is installed before running the program. The `main.py` file is the
entrypoint to the program. Start a player-controlled game with the following
command:

```
uv run main.py run -p
```

A number of options can be added to customize the game, agent, and adversary. for example:

```
uv run main.py -n 4 -k 5 -d 10 -i 50 run
```

Use the `--help` option for more info.

```
uv run main.py --help
```

The testing harness can run multiple games in sequence and report stats:

```
uv run main.py -n 4 -k 5 -d 10 -i 50 test -r 5
```

## TODO 4/9 Meeting

- Update and integrate `gameState.py` = (Max, Mack)
  - Create bomb tiles
  - Create tile classes
- Add an adversary = (YG)
  - Scores positions for new tiles
  - Picks randomly from the top `k` places
- Agent class (can be random for now) = (Han)
  - Evaluation function for gameState

## TODO 4/30 Meeting

- Create a MCT class so it is persistent (Mack)
- Update bomb tiles so they're usable (Max)
- Update evaluation (YG)
- ~~Make a testing harness for finding average scores (Han)~~
  - ~~Make a no graphics option~~
- Tinker with c value (Exploration bonus) (YG)
- Start report (Sadness)
