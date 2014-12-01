'''
Exports a set of variables that govern the high-level behavior of the
simulation. Above each variable is an explanation of what that
variable is and what it does.

Also exports a set of functions that are required for initialization.


Note: All variables use _ to separate words. Since these variables are
to be global (i.e., constants), they are named in all UPPERCASE.
Functions use camelCase.

Created by NPD on 11/20/14
'''
########################################################################
# Game board options
########################################################################
# GRID_RANDOM indicates whether or not the game board is to be generated
# randomly or whether it is to be provided by GRID. If it is True, you
# will have to define N_COLS and N_ROWS and transProbFcn. If it is
# false, than GRID must be nonempty.
GRID_RANDOM = True

# N_COLS is an integers that returns the number of columns in the game
# board.
N_COLS = 10

# N_ROWS is an integer that returns the number of rows in the game
# board.
N_ROWS = 10

# transProbFcn returns a transition probability. It is called with no
# inputs (if you want to assign specific values to specific tiles, set
# GRID_RANDOM = False and define GRID).
def transProbFcn():
    return 0.25

# GRID is an n x m array (list of lists) of floats that specify the
# transition probabilities for each cell on the board, which are the
# probabilities that an agent will transition to that tile. Each entry
# represents a single tile. A value of 1 means that an agent is
# maximally likely to transition to it from an adjacent game board,
# whereas a value of 0 means that an agent will never transition to this
# tile. If GRID_RANDOM is False, then GRID may be empty.
GRID = []

# NUM_AGENTS is the number of agents that should be on the board at any
# given time.
NUM_AGENTS = 1000

# neighborCords defines the relational indices of the neighbors.
def neighborCords(location):
    loc_x, loc_y = location
    locs = [(loc_x+1, loc_y), (loc_x, loc_y+1),
            (loc_x-1, loc_y), (loc_x, loc_y-1)]
    return [(x[0]%N_ROWS, x[1]%N_COLS) for x in locs]

########################################################################
# Agent options
########################################################################
# MUTATION_PROB is the probability of any particular instruction
# changing across a generation.
MUTATION_PROB = 0.01

# ALWAYS_PLAY is a boolean that indicates whether or not the agent
# should *always* choose to play against any other agent. If False, it
# will use the trust parameter/learned trust algorithm.
ALWAYS_PLAY = False

# GENOME_TYPE dictates the kinds of event sequences stored in the
# genome. It can be 'unary', in which case the genome only stores the
# actions of the opponent, or 'binary', in which case the genome stores
# the actions of both players
GENOME_TYPE = 'unary'

# GENE_LENGTH is the number of past events to store responses to. For
# instance, of GENE_LENGTH is 1, then the genome, and the corresponding
# agent, will respond based on the previous action. If GENOME_TYPE is
# 'unary', then a GENE_LENGTH of n means that 2^(n+1)-1 genes are
# defiend, if GENOME_TYPE is 'binary', then (1/3)*(4^(n+1)-1) genes are
# defined.
GENE_LENGTH = 6

# NAME_LENGTH is the number of characters in the 'name' (a string that
# may or may not uniquely identify this agent). The name can be thought
# of as a phenotype.
NAME_LENGTH = 25

# N_POS_ACTIONS is the number of behaviors that the agent can undertake.
# It must be at least 2 (for cooperate / defect). The mapping from
# action number to action in performAction
N_POS_ACTIONS = 3

# MOVE indicates whether or not the agents can move
MOVE = True

# LEARN_TRUST is a boolean that indicates whether or not the agent
# should learn to trust via SGD or simply by (somewhat randomly)
# changing the trust parameter
LEARN_TRUST = True

# LEARNING_RATE is the SGD learning rate, which is used if LEARN_TRUST
# is true.
LEARNING_RATE = 0.05

# SAMPLE_ALL_AGENTS is a boolean that indicates whether or not only the
# top half of agents are to reproduce (false), or if we sample from
# all agents according to their contribution to the total fitness.
SAMPLE_ALL_AGENTS = False

# lossFunction defines the function to execute for updating the weights.
# it's not actually a true loss function, but is instead its gradient.
# The current one implemented is a squared loss function.
import numpy as np
#import pdb
def lossFunction(weights, opp_name, delta_fitness):
    #pdb.set_trace()
    opp_name = np.array([1] + [int(x) for x in opp_name])
    loss = (np.dot(weights, opp_name) - delta_fitness)
    return opp_name * loss

# defaultPerformAction performs the set of operations that are mapped
# to a given action value. The action set is currently:
#                   coop    def     quit
# no trust change   0       1       2
# increment trust   3       4       5
# decrement trust   6       7       8
#
# it is provided as input to the agent, which then sets it as a method.
def normalPerformAction(agent, action):
    if action > 5:
        # decrement trust parameter
        agent.decTrustParameter()
    elif action > 2:
        # increment trust parameter
        agent.incTrustParameter()
    if not (action) % 3:
        return agent.cooperate()
    elif not (action - 1) % 3:
        return agent.defect()
    elif not (action - 2) % 3:
        return agent.quit()

def onlyCDQ(agent, action):
    if action == 0:
        return agent.cooperate()
    elif action == 1:
        return agent.defect()
    elif action == 2:
        return agent.quit()

def onlyCD(agent, action):
    if not action:
        return agent.cooperate()
    else:
        return agent.defect()

def allD(agent, action):
    # always defect
    return agent.defect()

def allC(agent, action):
    # always cooperate (optimal play)
    return agent.cooperate()

if N_POS_ACTIONS == 2:
    #
    defaultPerformAction = onlyCD
if N_POS_ACTIONS == 3:
    # only cooperate / defect / quit
    defaultPerformAction = onlyCDQ
if N_POS_ACTIONS == 9:
    # with trust modifications
    defaultPerformAction == normalPerformAction

# returnRandomID returns a string of random numbers and characters
# that serve to uniquely ID an agent.
from random import choice
def returnRandomID(length = 20):
    chooseChar = lambda: choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    return ''.join([chooseChar() for x in range(length)])

'''
On trust:
When an agent encounters another agent, it will decide whether to play
with them in a semi-random manner. First, they will count the number of
ways in which this potential opponent is different from them, using
the opponent's name. If we let this number be N, then the probbility
that agent A will play agent B is given by:

P = 1 / (1 + exp((N - TRUST_PARAMETER)/TRUST_SCALE_FACTOR))

This is a logistic function that gets higher as N gets lower. As the
agent becomes less and less trustful, the curve slides closer and
closer to N = 0.
'''
# TRUST_PARAMETER relates how much a given agent trusts another agent
# with a different name / phenotype. This is the default value; agents
# can (and will) change this value as the game evolves. If the trust
# parameter is closer to the name length, then the agent will be more
# trusting.
TRUST_PARAMETER = 25

# TRUST_SCALE_FACTOR adjusts the trust falloff--higher values of
# TRUST_SCALE_FACTOR mean that the trust falloff curve is less steep.
TRUST_SCALE_FACTOR = 2.

# TRUST_INCREMENT_PARAMETER indicates how much to increase or decrease
# the trust parameter on each update.
TRUST_INCREMENT_PARAMETER = 0.5
########################################################################
# Prisoner's Dilemma options
########################################################################
# CONTINUE_PROB is the probability that a game of prisoner's dilemma
# will end after a given iteration. Keep in mind that if the
# probability of continuation is p, then the expected number of games is
# p / (1-p)
CONTINUE_PROB = 1

# EXPECTED_TURNS is the expected number of turns to be played, since
# CONTINUE_PROB is now depricated (turn probability is drawn from a
# poisson distibution)
EXPECTED_TURNS = 8

# HISTORY_LENGTH is merely the number of moves to record. It must be
# equal to GENE_LENGTH
HISTORY_LENGTH = GENE_LENGTH

# PAYOFF defines the payoff values for the 4 possible situations. If
# your opponent / confederate is player B, then...
# If you cooperate, and B cooperates, you recieve the 'reward' R
# If you cooperate, but B defects, you recieve the 'suckers' payoff S
# If you defect, and B cooperates, you recieve the 'temptation' payoff T
# If you defect, and B defects, you recieve the 'prisoners' payoff P
# Note that, in order for this to be a valid Prisoner's dilemma, we have
# that T > R > P > S
PAYOFF = {'t':5,'r':3,'p':0,'s':-3}

# GAMES_PER_ITER is the number of games each agent is allowed to gain
# fitness from each iteration.
GAMES_PER_ITER = 8.

# REFUSE_PENALTY dictates the cost of refusing to play with an opponent.
# If REFUSE_PENALTY is 1, then refusing to play is effectively like
# giving up an entire games worth of potential fitness.
#
# NOTE: This refers to a decrease in the number of potential games you
# can play, it does NOT refer to a decrease in fitness earned that
# round!
REFUSE_PENALTY = 0.5

# DENIED_PENALTY is the cost of being refused. I.e., if agent B refuses
# to play with you. In general, DENIED_PENALTY should be less than
# REFUSE_PENALTY.
#
# NOTE: This refers to a decrease in the number of potential games you
# can play, it does NOT refer to a decrease in fitness earned that
# round!
DENIED_PENALTY  = 0.25

# MOVE_COST is the cost of moving from one tile to another. If we later
# introduce the capacity for agents to move on their own, choosing when
# and where to move, then moving will have to incur a cost.
MOVE_COST = 0

# COOP_SIGNAL is the value to send to the game master when cooperating
COOP_SIGNAL = 1

# DEFECT_SIGNAL is the value to send to the game master when defecting
DEFECT_SIGNAL = 0

# QUIT_SIGNAL is the value to send to the game master when quitting
QUIT_SIGNAL = -1

# PAYOFF_MAP is an equivalent implementation of PAYOFF, but defines
# it in terms of a map that can be indexed into. I.e, the fitness update
# for A given A and B have actions aA and aB is given by PAYOFF_MAP[aA][aB]
PAYOFF_MAP = {DEFECT_SIGNAL:{COOP_SIGNAL:PAYOFF['t'],
                             DEFECT_SIGNAL:PAYOFF['p']},
              COOP_SIGNAL:{COOP_SIGNAL:PAYOFF['r'],
                           DEFECT_SIGNAL:PAYOFF['s']}}

# ACTION_LABELS is for convenience, it maps actions to natural language
# interpretations.
ACTION_LABELS = {DEFECT_SIGNAL:'DEFECT', COOP_SIGNAL:'COOPERATE'}

# PAYOFF_LABELS is the same as PAYOFF_MAP, only it indicates which
# statistic to increment in the agent's stats counters given a payoff
PAYOFF_LABELS = {DEFECT_SIGNAL:{COOP_SIGNAL:'traitor',
                             DEFECT_SIGNAL:'prisoner'},
              COOP_SIGNAL:{COOP_SIGNAL:'collaborator',
                           DEFECT_SIGNAL:'sucker'}}
########################################################################
# Other options
########################################################################
# OVERRIDE_ASSERTIONS is a boolean. If true, the assertions will not
# be checked for validity.
OVERRIDE_ASSERTIONS = False

# VERBOSITY is the verboseness of the output. It is an integer, where
# the integer indicates the priority of a given message required to
# print out. Higher values of VERBOSITY mean that less is printed.
VERBOSITY = 2

# printMsg accepts a string <msg> and a number <priority> and decides
# whether or not to print out that message based on the value of
# VERBOSITY. Note that lower values of <priority> indicate higher
# priority. (1 is the highest)
def printMsg(msg, priority = 0):
    if VERBOSITY < 0:
        return
    if priority >= VERBOSITY:
        print msg
########################################################################
# Assertions: If these fail, then your simulation will either fail or be
# invalid for some reason.
from constants_override import *

if not OVERRIDE_ASSERTIONS:
    assert PAYOFF['t'] > PAYOFF['r'], 'FIX PAYOFF, T > R > P > S'
    assert PAYOFF['r'] > PAYOFF['p'], 'FIX PAYOFF, T > R > P > S'
    assert PAYOFF['p'] > PAYOFF['s'], 'FIX PAYOFF, T > R > P > S'
    assert GRID_RANDOM and N_ROWS > 0 and N_COLS > 0, 'MUST HAVE POSITIVE ROWS / COLUMNS'
    assert GRID_RANDOM or len(GRID), 'MUST USE RANDOM GRID OR DEFINED GRID'
    assert GENOME_TYPE == 'unary' or GENOM_TYPE == 'binary', 'GENOME_TYPE MUST BE EITHER UNARY OR BINARY'
    assert GENE_LENGTH >= 0, 'CANNOT HAVE NEGATIVE GENE LENGTH'
    assert HISTORY_LENGTH == GENE_LENGTH, 'HISTORY_LENGTH AND GENE_LENGTH MUST BE EQUAL'





















