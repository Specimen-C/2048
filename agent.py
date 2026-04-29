#imports
import random
from action import Action
from datetime import datetime
from gameState import GameState as gameState, Adversary

#for now, defines an agent that quite literally chooses a move at randome
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
        self.depth = 5                     #default depth is 10

    #returns a float, evaluates a given game state
    def evaluate(self, gameState: gameState):
        val = 0
        board = gameState.board
        numTiles = 0
        sizeTiles = 0

        #find the max tile in board
        maxtile = 0
        for r in range(len(board)):
            for c in range(len(board[r])):
                tile = board[r][c]
                if (tile != None and tile.value > maxtile):
                    maxtile = tile.value
                if (tile != None):
                    numTiles += 1
                sizeTiles += 1

        #   Sloppy but it works for looking at corners.
        #   If the biggest tile is in corner (if not None), add points to eval function
        #NOTE: possible edge case of multiple "max tiles" and it doesnt want to merge
        if (board[0][0] != None):
            if (board[0][0].value == maxtile):
                val += 100
        elif (board[0][len(board) - 1] != None):
            if (board[0][len(board) - 1].value == maxtile):
                val += 100
        elif (board[len(board) - 1][0] != None):
            if (board[len(board) - 1][0].value == maxtile):
                val += 100
        elif (board[len(board) - 1][len(board) - 1] != None):
            if (board[len(board) - 1][len(board) - 1].value == maxtile):
                val += 100

        #   Incentivise less tiles in board
        #   made up BS lowkey, cant simulate this until the thingy actually works
        if(numTiles <= 2*len(board)):
            val += 100
        elif(numTiles <= 2.5*len(board)):
            val += 80
        elif(numTiles <= 3*len(board)):
            val += 50
        elif(numTiles <= 3.5*len(board)):
            val += 30
        elif(numTiles <= 4*len(board)):
            val += 10
        elif(numTiles == sizeTiles):
            val -= 100

        return val

    #returns an action given a game state. Use eval function.
    #I have to add an adversary bc otherwise i cant use the generate successors function properly
    def getAction(self, gameState, adversary):
        #if random agent just return a random move
        if (self.mode == "Random"):
            return random.choice(gameState.getLegalActions())
        
        if (self.mode == "MonteCarlo"):
            return self.UCT(gameState, adversary)

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
        


    #Clarifications:
        """
        s = current state.
        d = remaining depth or horizon (so recursion doesn't go on forever; allows for finite-horizon search).
        pi_0 = default policy used during rollout (random or some heuristic policy)
        A(s) = legal action set from state s 
        T = set of states already added to the search tree.
        N(s, a) = visit count for taking action a from state s.
        Q(s, a) = current estimated value of taking action a from state s.
        N(s) = the total number of visits to state s,
            the sum of N(s, a) over all actions from s.
        c is the exploration constant in the UCB/UCT formula.
        G(s, a) is the generative model or simulator:
            given a state and action, it produces a next state and reward. 
        s` is the next state.
        r is the immediate reward.
        The symbol ~ means “sampled from.”
            So when it says (s', r) ~ G(s, a), it means the simulator samples a transition and reward from that state-action pair.
        y = the discount factor
        """
        
    def UCT(self, gameState: gameState, adversary: Adversary):
        import math         #for sqrt and logs
        
        #general stuff we need for MCTS:
        T = set()           #T states in search tree; for rollout vs continuous simualtion
        Q = {}              #Q(s, a): estimated return/value for taking that action from that state; running average of all sampled q-values seen for that (s, a)
        N = {}              #N(s, a): number of times that action was chosen from that state;      used both for UCT exploration and for updating Q by incremental average.
        gamma = 1.0         #simulate finite number of states, so no need to discount (i think?)
        c = 1.1             #how much you value "uncertainty". large = explore more than exploit; small = trust current Q(s,a) value. Explore for now.
        d = self.depth

        #!!!!!!  Monte Carlo Tree Method helpers:
        def A(s: gameState):
            #print("Legal Actions: ", s.getLegalActions())
            return s.getLegalActions()
        
        #explore randomly (choose moves to simulate at random for MCTS)
        def pi_0(s: gameState):
            actions = A(s)
            #print("ACTIONS: ", actions)
            if (len(actions) == 0):
                return None
            return random.choice(actions)
        
        # N(s, a) = visit count for taking action a from state s (for all actions a).
        def N_s(s: gameState):
            tot = 0
            for a in A(s):
                key = stateKey(s)
                tot += N.get((key, a), 0)       #default 0
            return tot
        
        #makes a state hashable 
        def stateKey(s: gameState):
            key = []

            for row in s.board:
                for tile in row:
                    if (tile == None):
                        key.append(0)
                    else:
                        key.append(tile.value)

            return tuple(key)
        
        # take the current state and one chosen action, 
        # look up that action inside s.generateSuccessors(adversary), 
        # sample one successor according to the probabilities, and 
        # return (s_prime, r).
        def G(s: gameState, a: Action):
            actions = s.generateSuccessors(adversary)
            actionStates = actions[a]           #list of tuples of (float, gameState)s
            
            #the prob selected
            prob = random.uniform(0, 1)
            original_score = s.score
            counter = 0.0       #ramping counter for which bucket based on dist
            newS = actionStates[-1][1]         #s'; default is just the LAST gameState (maybe 1 is never reached for ex)
            
            for state in actionStates:
                curProb = state[0]
                counter += curProb
                
                #met the right "bucket"
                if (prob <= counter):
                    newS = state[1]
                    break
            
            reward = (newS.score - original_score)      #might change later but for now just score delta
            return (newS, reward)
                
        #Debugs for Monte Carlo Process
        def debugMCT():
            pass

        """
        function selectAction(s, d):
            loop
                Simulate(s, d, pi_0)
            return argmax_a Q(s, a)         #yeah
        """

        def selectActions(state: gameState, depth: int):
            bestAction = None
            bestScore = -99999999
            key = stateKey(state)
            
            for d in range(self.depth):
                Simulate(state, depth, pi_0)
        
            for a in A(state):
                score = Q.get((key, a), 0.0)
                
                if (score > bestScore):
                    bestScore = score 
                    bestAction = a

            return bestAction

        """
        function Simulate(s, d, pi_0):
            if (d == 0):
                return 0
            if (s not in T):
                for a in A(s)
                    (N(s, a), Q(s, a)) = (N_0(s, a), Q_0(s, a))
                T = T union {s}
                return rollout(s, d, pi_0)

            if a in A(s):
                a = argmax_a (Q(s, a) + (c * math.sqrt( (math.log( N(s)) / N(s, a) ) )
            (s', r) ~ G(s, a)
            q = r + y*Simulate(s', d - 1, pi_0)
            N(s, a) = N(s, a) + 1
            Q(s, a) = Q(s, a) + (q - Q(s, a) / N(s, a))

            return q
        """

        def Simulate(state: gameState, depth: int, pi_0):
            if (depth == 0):
                return 0
            
            key = stateKey(state)
            
            if (key not in T):
                for a in A(state):
                    #initialize tables for all actions for that state not in the visited tree
                    key = stateKey(state)
                    
                    N[(key, a)] = 0
                    Q[(key, a)] = 0.0
                    
                T.add(stateKey(state))
                return Rollout(state, depth, pi_0)
            
            #early return
            if len(A(state)) == 0:
                return 0
            
            a = None 
            bestMCTS = -9999999
            
            #iterate through all possible actions from cur state
            for action in A(state):
                key = stateKey(state)
                
                #get num time this state has been visited 
                visits = N[key, action]
                
                #if never visited, it's a candidate automatically
                if (visits == 0):
                    a = action
                    break
                
                score = Q[(key, action)] + (c * math.sqrt( (math.log(N_s(state)) / N[(key, action)])))
                
                if (score > bestMCTS):
                    bestMCTS = score
                    a = action
                
            
            #lowkey i have no idea what this does i just followed the pseudocode
            (newState, reward) = G(state, a)
            q = reward + gamma*Simulate(newState, depth-1, pi_0)
            N[(key, a)] = N[(key, a)] + 1
            Q[(key, a)] = Q[(key, a)] + (q - Q[(key, a)]) / (N[(key, a)])
            return q
        
        
        """
        function Rollout(s, d, pi_0):
            if d == 0:
                return 0

            a ~ pi_0(s)
            (s', r) ~ G(s, a)
            return r + y * Rollout(s', d - 1, pi_0)
        """
        #@returns a number, unsure if float or int
        def Rollout(state: gameState, depth: int, pi_0):
            if depth == 0:
                return 0
            
            #sample a random legal action (from current exploration algo)
            a = pi_0(state)
            
            #if there are no states, it's the same as hittign the depth limit
            if (a == None):
                return 0
            
            #continue rolling out
            (newS, r) = G(state, a)
            return r + gamma * Rollout(newS, depth - 1, pi_0)
        
        return selectActions(gameState, self.depth)