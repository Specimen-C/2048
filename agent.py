#imports
import random
from action import Action
from datetime import datetime
from gameState import GameState, Adversary

#for now, defines an agent that quite literally chooses a move at random
class Agent:

    #typehints
    agent: str
    gravestone: str
    born: datetime
    death: datetime
    mode: str
    depth: int
    
    def __init__(self, agentName: str):
        self.agent = agentName              #string
        self.gravestone = None              #string
        self.born = datetime.now()          #datetime obj
        self.death = None                   #datetime obj
        self.mode = "Random"                #default make the agent be random
        self.depth = 10                    #default depth is 10
        self.tree = MCTree(None, self)

    # #returns a float, evaluates a given game state
    # def evaluate(self, gameState: GameState):
        
    #     val = 0
    #     board = gameState.board
    #     numTiles = 0
    #     sizeTiles = 0
    #     n = len(board)

    #     #find the max tile in board
    #     maxtile = 0
    #     for r in range(n):
    #         for c in range(n):
    #             tile = board[r][c]
    #             if (tile != None and tile.value > maxtile):
    #                 maxtile = tile.value
    #             if (tile != None):
    #                 numTiles += 1
    #             sizeTiles += 1

    #     # Reward max tile in corner
    #     if (board[0][0] != None and board[0][0].value == maxtile):
    #         val += gameState.score * 200
    #     if (board[0][n - 1] != None and board[0][n - 1].value == maxtile):
    #         val += gameState.score * 200
    #     if (board[n - 1][0] != None and board[n - 1][0].value == maxtile):
    #         val += gameState.score * 200
    #     if (board[n - 1][n - 1] != None and board[n - 1][n - 1].value == maxtile):
    #         val += gameState.score * 200

    #     # Reward monotonicity: tiles should decrease as you move away from max tile
    #     # Check rows 
    #     for r in range(n):
    #         for c in range(n - 1):
    #             left = board[r][c].value if board[r][c] != None else 0
    #             right = board[r][c + 1].value if board[r][c + 1] != None else 0
    #             if left >= right:
    #                 val += gameState.score * 1000
    #             if right >= left:
    #                 val += gameState.score *1000
        
    #     # Check columns 
    #     for c in range(n):
    #         for r in range(n - 1):
    #             top = board[r][c].value if board[r][c] != None else 0
    #             bottom = board[r + 1][c].value if board[r + 1][c] != None else 0
    #             if top >= bottom:
    #                 val += gameState.score * 1000
    #             if bottom >= top:
    #                 val += gameState.score * 1000

    #     # Penalize trapped tiles (tiles not adjacent to similar values)
    #     for r in range(n):
    #         for c in range(n):
    #             tile = board[r][c]
    #             if tile == None:
    #                 continue
                
    #             # Check if this tile has any mergeable neighbors
    #             hasMatchingNeighbor = False
    #             neighbors = []
                
    #             # Check all 4 directions
    #             if r > 0:  # Up
    #                 neighbors.append(board[r-1][c])
    #             if r < n - 1:  # Down
    #                 neighbors.append(board[r+1][c])
    #             if c > 0:  # Left
    #                 neighbors.append(board[r][c-1])
    #             if c < n - 1:  # Right
    #                 neighbors.append(board[r][c+1])
                
    #             # Check if any neighbor is same value (can merge) or empty (can move)
    #             for neighbor in neighbors:
    #                 if neighbor == None:  # Empty space means not trapped
    #                     hasMatchingNeighbor = True
    #                     break
    #                 if neighbor.value == tile.value:  # Can merge
    #                     hasMatchingNeighbor = True
    #                     break
                
    #             # Penalize trapped tiles (bigger tiles get bigger penalties)
    #             if not hasMatchingNeighbor:
    #                 val -= gameState.score * tile.value  # Scale penalty with tile value

    #     # Incentivize empty tiles (more empty = better)
    #     emptyTiles = sizeTiles - numTiles
    #     val += emptyTiles * gameState.score * 100000

    #     # Penalty for full board
    #     if numTiles == sizeTiles:
    #         val -= gameState.score * 200

    #     return val + gameState.score
    
    def evaluate(self, gameState: GameState):
        # Make loss punished a lot
        if gameState.isLoss():
            return float('-inf') 
        
        val = 0
        board = gameState.board
        n = len(board)
        
        # Count tiles and find max
        numTiles = 0
        maxTile = 0
        for row in range(n):
            for col in range(n):
                tile = board[row][col]
                if tile is not None:
                    numTiles += 1
                    if tile.value > maxTile:
                        maxTile = tile.value
        
        # Reward max tile in corner
        corners = [(0, 0), (0, n-1), (n-1, 0), (n-1, n-1)]
        for row, col in corners:
            if board[row][col] is not None and board[row][col].value == maxTile:
                val += 10000
                break
        
        # Reward decreasing left-to-right
        for row in range(n):
            for col in range(n - 1):
                left = board[row][col].value if board[row][col] is not None else 0
                right = board[row][col + 1].value if board[row][col + 1] is not None else 0
                if left >= right:
                    val += 100
        
        for col in range(n):
            for row in range(n - 1):
                top = board[row][col].value if board[row][col] is not None else 0
                bottom = board[row + 1][col].value if board[row + 1][col] is not None else 0
                if top >= bottom:
                    val += 100
        
        # Reward empty tiles
        emptyTiles = (n * n) - numTiles
        val += emptyTiles * 500
        
        # Reward tiles that can merge
        mergePotential = 0
        for row in range(n):
            for col in range(n):
                if board[row][col] is None:
                    continue
                tile = board[row][col].value
                
                # Check neighbors for merge opportunities
                neighbors = []
                if row > 0: neighbors.append(board[row-1][col])
                if row < n-1: neighbors.append(board[row+1][col])
                if col > 0: neighbors.append(board[row][col-1])
                if col < n-1: neighbors.append(board[row][col])
                
                for neighbor in neighbors:
                    if neighbor is not None and neighbor.value == tile:
                        mergePotential += tile
        
        val += mergePotential * 10
        
        val += gameState.score * 2
        
        return val
    
    #returns an action given a game state. Use eval function.
    #I have to add an adversary bc otherwise i cant use the generate successors function properly
    def getAction(self, gameState: GameState, adversary):
        
        #if random agent just return a random move
        if (self.mode == "Random"):
            return random.choice(GameState.getLegalActions())
        
        if (self.mode == "MonteCarlo"):
            if self.tree.root == None:
                self.tree.setRoot(gameState, None)
            
            action =  self.tree.search(20)
            
        return action
            

    # returns the wall-clock time (float? or int ig idk) of an agent
#    @returns infinity (if alive), wall-clock time otherwise.
    def lifespan(self):
        if(self.death == None): return float('inf')
        else:
            return (self.death - self.born)

    def setGravestoneMessage(self, message: str):
        self.gravestone = message

    #currently supports: "Random" and "MonteCarlo"
    def setAgent(self, agentType: str):
        self.mode = agentType
        
    #sets the agent to a randomly moving agent
    def setRandom(self):
        self.mode = "Random"
        
    def setDepth(self, d: int):
        self.depth = d
        

class MCTree:
    
    #root : GameState
    #q_table: dict[tuple[GameState, Action], float]
    #n_table: dict[tuple[GameState, Action], int]
    def __init__(self, root: tuple[GameState, Action] | None, agent: Agent):
        self.root: tuple[GameState, Action] = root
        self.q_table: dict[tuple[GameState, Action], float] = {}
        self.n_table: dict[tuple[GameState, Action], int] = {}
        
        
        self.exploration_factor: float = 0.5
        self.discount_factor: float = 1
        self.depthLimit: int = 70
        self.iterAmount: int = 200
        
        self.adversary: Adversary = Adversary(5)
        self.agent: Agent = agent
        
    def setRoot(self, state: GameState, action: Action | None):
        self.root = (state, action)
    
    #Tree Search
    def search(self, iterationLimit: int):
        #print("Simulating " + str(iterationLimit) + " number of moves")
        #Run simulate iterationLimit number of times
        while iterationLimit > 0:
            #print("Simulating... iteration = " + str(iterationLimit))
            self.simulate()
            iterationLimit -= 1
        
        #Then pick a move (Argmax of quality table)
        maxQ = float('-inf')
        maxAction = None
        
        #self.root[0].printGameState()
        
        for action in self.root[0].getLegalActions():
            qVal = self.q_table.get((self.root[0], action), 0)
            if qVal >= maxQ:
                maxQ = qVal
                maxAction = action
            
                
        if maxAction is None:
            raise Exception("Dumbass why'd you call search on a loss state?? ")
        
        return maxAction
    
    #Add nodes to the tree
    #Simulate
    def simulate(self):
        #print("Simulating from the root")
        
        #Start from the root
        state = self.root[0]
        #print("State = " + str(state) + " and has type " + str(type(state)))
        action = random.choice(state.getLegalActions())
        
        path: list[tuple[GameState, Action]] = []
        path.append((state, action))
        
        #Generate a random action until we find a leaf node
        while action is not None and (state, action) in self.q_table:
            #print("Checking out a new state action pair in our table")
            state = state.takeTurn(action, self.adversary)
            if len(state.getLegalActions()) != 0:
                action = self.selectActionUCB(state)
            else :
                action = None
            path.append((state, action))
        
        #print("Found a leaf node!")
        
        #Rollout from that leaf node
        quality: float = self.rollout(state)
        
        #Back propagate the quality update
        for saPair in reversed(path):
            n = self.n_table.get(saPair, 0)
            self.q_table[saPair] = ((self.q_table.get(saPair, 0) * n) + quality) / (n + 1)
            self.n_table[saPair] = n + 1
            
    def selectActionUCB(self, state: GameState) -> Action:
        """Select action using Upper Confidence Bound (UCB1)"""
        import math
        
        legalActions = state.getLegalActions()
        
        # If any action hasn't been tried yet, try it
        for action in legalActions:
            if (state, action) not in self.n_table:
                return action
        
        # Otherwise, use UCB formula
        bestScore = float('-inf')
        bestAction = None
        
        # Total visits to this state
        totalVisits = sum(self.n_table.get((state, a), 0) for a in legalActions)
        
        for action in legalActions:
            q = self.q_table.get((state, action), 0)  # Exploitation term
            n = self.n_table.get((state, action), 1)  # Avoid division by zero
            
            # UCB1 formula: Q(s,a) + c * sqrt(ln(N) / n(s,a))
            ucb_score = q + self.exploration_factor * math.sqrt(math.log(totalVisits + 1) / n)
            
            if ucb_score > bestScore:
                bestScore = ucb_score
                bestAction = action
        
        return bestAction
    
    #Randomly move till the depth cutoff
    #Rollout
    def rollout(self, root: GameState) -> float:
        #print("Rolling out!")
        #Randomly moves till depth cutoff or loss, returns quality score
        node = root
        depth = 0
        
        while not node.isLoss() and depth < self.depthLimit:
            #print("Picking a move at random!")
            #Pick a move at random
            action = random.choice(node.getLegalActions())
            
            node = node.takeTurn(action, self.adversary)
            
            depth += 1
            
        return self.agent.evaluate(node)
            
    
    #selectAction
        
    