#imports
import random
from action import Action 
from datetime import datetime

#for now, defines an agent that quite literally chooses a move at randome
class Agent:
    
    #typehints
    agent: str
    gravestone: str
    born: datetime
    death: datetime
    
    def __init__(self, agentName: str, wtfisagravestone: str, birth: datetime, death: datetime):
        self.agentName = agentName          #sting
        self.gravestone = wtfisagravestone  #a string
        self.born = birth                   #datetime obj
        self.death = death                  #datetime obj

    #returns a float, evaluates a given game state
    def evaluate(self, gameState):
        #lowkey i dont wanna hardcode corners but i might idk
        pass

    #returns an action given a game state. Use eval function.
    def getAction(self, gameState):
        #list of possible actions (legal)
        Actions = gameState.getLegalActions()
        
        #if there is no gamestate, return a random move
        if (gameState == None):
            return random.choice(Actions)
        
        #ill do the rest tmr
        curBestEval = 0
        act = None
        for m in Actions:
            action, evalScore = gameState.generateSuccessors(m)
            if (evalScore > curBestEval):
                curBestEval = evalScore
                act = action
        return act
        
    
    # returns the wall-clock time (float? or int ig idk) of an agent
#    @returns infinity (if alive), wall-clock time otherwise.
    def lifespan(self):
        if(self.death == None): return float('inf')
        else:
            return (self.death - self.born)