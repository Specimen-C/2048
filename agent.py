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
    
    #sets the agent to a randomly moving agent
    def setRandom(self):
        self.agent = "Random"
    
    def __init__(self, agent: str, wtfisagravestone: str, birth: datetime, death: datetime):
        self.agent = agent                  #sting
        self.gravestone = wtfisagravestone  #a string
        self.born = birth                   #datetime obj
        self.death = death                  #datetime obj

    #returns a float, evaluates a given game state
    def evaluate(self, gameState):
        #lowkey i dont wanna hardcode corners but i might idk
        pass

    #returns an action given a game state. Use eval function.
    #I have to add an adversary bc otherwise i cant use the generate successors function properly
    def getAction(self, gameState, adversary):
        #if random agent just return a random move
        if (self.agent == "Random"):
            return random.choice(gameState.getLegalActions())
        
        #list of possible actions (legal)
        Actions = gameState.getLegalActions()
        
        #if there is no gamestate, return a random move
        if (gameState == None):
            return random.choice(Actions)
        

        curBestEval = 0
        act = None
        
        #for every legal action
        for a in Actions:
            successorDict = gameState.generateSuccessors(adversary)     #returns all possible successors for all actions
            actionDict = successorDict[a]   #gets all possible successors for the given action, 
            
            #actionDict = list[tuple(float, gameState)]
            for states in actionDict:
                
                state = states[1]   #this is the gameState object
                
                #This might be problematic, but we can go with this for now;
                #calls the evaluation fuction, which returns a value of "how good" a game state is, 
                #   and multiplies it by the probbaility of that state happening
                
                #problematic b/c some horrid state with chance of 100% might be chosen over something with a better outcome with lower probability
                evalScore = self.evaluate(state) * states[0]
                
                if (evalScore > curBestEval):
                    curBestEval = evalScore
                    act = a
                
        return act
        
    
    # returns the wall-clock time (float? or int ig idk) of an agent
#    @returns infinity (if alive), wall-clock time otherwise.
    def lifespan(self):
        if(self.death == None): return float('inf')
        else:
            return (self.death - self.born)
        
        
    #empty body but method idea outlined for monte-carlo tree search
    def UCT():
        import math         #for sqrt and logs 
        
        """
        
        function selectAction(s, d):        #wtf is s, d????
            loop
                Simulate(s, d, pi_0)        #pi0?????
            return argmax_a Q(s, a)         #yeah
            
        function Simulate(s, d, pi_0):      #wtf is s, d????
            if (d == 0):
                return 0
            if (s not in T):
                for a in A(s)               #tf is A(s)??
                    (N(s, a), Q(s, a)) = (N_0(s, a), Q_0(s, a))
                T = T union {s}
                return rollout(s, d, pi_0)
            
                if a in A(s):
                    a = argmax_a (Q(s, a) + (c * math.sqrt( (math.log( N(s)) / N(s, a) ) )
                (s', r) ~ G(s, a)           #what does ~ mean
                q = r = y*Simulate(s', d - 1, pi_0)
                N(s, a) = N(s, a) + 1
                Q(s, a) = Q(s, a) + (q - Q(s, a) / N(s, a))
                
            return q
        
        function Rollout(s, d, pi_0):
            if d == 0:
                return 0

            a ~ pi_0(s)
            (s', r) ~ G(s, a)
            return r + y * Rollout(s', d - 1, pi_0)
        
        """