from gameState import GameState
from action import Action
from random import choices
from gameState import Adversary

class MCTree:
    
    #root : GameState
    #q_table: dict[tuple[GameState, Action], float]
    #n_table: dict[tuple[GameState, Action], int]
    def __init__(self, root: tuple[GameState, Action] | None):
        self.root: tuple[GameState, Action] = root
        self.q_table: dict[tuple[GameState, Action], float] = {}
        self.n_table: dict[tuple[GameState, Action], int] = {}
        
        
        self.exploration_factor: float = 0.5
        self.discount_factor: float = 1
        self.depthLimit: int = 10
        self.iterAmount: int = 30
        
        self.adversary: Adversary = Adversary(5)
        
    def setRoot(self, state: GameState, action: Action | None):
        self.root = (state, action)
    
    #Tree Search
    def search(self, iterationLimit: int):
        #Run simulate iterationLimit number of times
        while iterationLimit > 0:
            self.simulate()
        
        #Then pick a move (Argmax of quality table)
        maxQ = float('-inf')
        maxAction = None
        
        for action in self.root.getLegalActions():
            qVal = self.q_table.get((self.root, action))
            if qVal > maxQ:
                maxQ = qVal
                maxAction = action
                
        if maxAction is None:
            raise Exception("Dumbass why'd you call search on a loss state?? ")
    
    #Add nodes to the tree
    #Simulate
    def simulate(self):
        #Start from the root
        state = self.root
        action = choices(state.getLegalActions())
        
        path: list[tuple[GameState, Action]] = []
        path.append((state, action))
        
        #Generate a random action until we find a leaf node
        while (state, action) in self.q_table:
            state = state.takeTurn(action, self.adversary)
            action = choices(state.getLegalActions())
            path.append((state, action))
        
        #Rollout from that leaf node
        quality: float = self.rollout(state)
        
        #Back propagate the quality update
        for saPair in reversed(path):
            n = self.n_table[saPair]
            self.q_table[saPair] = ((self.q_table[saPair] * n) + quality) / (n + 1)
            self.n_table[saPair] = n + 1
    
    #Randomly move till the depth cutoff
    #Rollout
    def rollout(self, root: GameState, agent: Agent) -> float:
        #Randomly moves till depth cutoff or loss, returns quality score
        node = root
        depth = 0
        
        while not node.isLoss() or depth > self.depthLimit:
            #Pick a move at random
            action = choices(node.getLegalActions())
            
            node = node.takeTurn(action, self.adversary)
            
        return agent.evaluate(node)
            
    
    #selectAction
        
    