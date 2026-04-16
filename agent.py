#imports
import random
from action import Action
from datetime import datetime
from gameState import GameState as gameState

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

    def __init__(self, agent: str):
        self.agent = agent                  #sting
        self.gravestone = None  #a string
        self.born = datetime.now()                   #datetime obj
        self.death = None                  #datetime obj

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

    def setGravestoneMessage(self, message: str):
        self.gravestone = message

    def setAgent(self, agentType: str):
        self.agent = agentType

    #empty body but method idea outlined for monte-carlo tree search
    def UCT():
        import math         #for sqrt and logs


        #Clarifications:
        """
        s = current state.
        d = remaining depth or horizon (so the recursion does not go on forever, and so the planner can do finite-horizon search).
        pi_0 = default policy used during rollout (random or some heuristic policy)
        A(s) = action set (legal actions available from state s)
        T = set of states already added to the search tree.
        N(s, a) = visit count for taking action a from state s.
        Q(s, a) = current estimated value of taking action a from state s.
        N(s) = the total number of visits to state s,
            the sum of N(s, a) over all actions from s.
        c is the exploration constant in the UCB/UCT formula.
        G(s, a) is the generative model or simulator:
            given a state and action, it produces a next state and reward. s′ is the next state.
        r is the immediate reward.
        The symbol ~ means “sampled from.”
            So when it says (s', r) ~ G(s, a), it means the simulator samples a transition and reward from that state-action pair.
        y = the discount factor
        """



        """

        function selectAction(s, d):
            loop
                Simulate(s, d, pi_0)
            return argmax_a Q(s, a)         #yeah

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

        function Rollout(s, d, pi_0):
            if d == 0:
                return 0

            a ~ pi_0(s)
            (s', r) ~ G(s, a)
            return r + y * Rollout(s', d - 1, pi_0)

        """

        def selectActions(state: gameState, depth: int):
            pass

        def Simulate(state: gameState, depth: int, pi_0):
            pass

        #@returns a number, unsure if float or int
        def Rollout(state: gameState, depth: int, pi_0):
            pass
