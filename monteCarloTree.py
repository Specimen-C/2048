from agent import Agent
from gameState import GameState
from action import Action

class MCTree:
    
    def __init__(self, root: MCTreeNode):
        self.root: MCTreeNode = root
    
    def addNode(self, state: GameState, action: Action) -> None:
        pass
    
    def sample() -> Action:
        pass
    
    def updateRoot(self, newRoot: MCTreeNode) -> None:
        pass

class MCTreeNode:
    """
    Internal class used to make the tree easier to create. Basically just a wrapper
    for a tuple of state and action pairs. Feel free to change/remove
    """
    
    def __init__(self, state: GameState, action: Action):
        self.value: tuple[GameState, Action] = (state, action)
        self.children: list[MCTreeNode] = []
        
        
    def addChild(self, node: MCTreeNode) -> None:
        self.children.append(node)
        
    