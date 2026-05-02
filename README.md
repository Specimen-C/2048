## Scope increase ideas

- Larger board
- Additional mechanics (Random tile swaps/Tile value changes)
- Adversary mechanics (A minimizing agent that attempts to add specific tiles to mess the player up)
- Increasing randomness by having larger domain for random tile adds
- Bomb tiles (Merging tiles deletes them, but also lowers score)
- Beer tiles (Merging a beer tile makes your next move have a probability of going in a different direction)

## TODO 4/9 meeting

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
