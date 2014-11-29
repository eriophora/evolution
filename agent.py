'''
Exports the 'agent' class, which represents an individual agent, i.e.,
the main object of simulation in this project.

Agents can play games, move about the game board, reproduce, and die.

At the end of each iteration, if an agent's share of the fitness is
greater than average given the population, it reproduces and produces
offspring. the number of offspring produced is given by the surplus
fitness that the agent generated in the previous round.

Created by NPD on 11/23/14
'''

from random import random
from random import choice
from genome import Genome
from trust import Trust
from constants import *
from math import exp

class Agent():
    def __init__(self, tile = None, genome = None, trust_parameter = None, performAction = None):
        self.performAction = performAction
        if performAction == None:
            self.performAction = defaultPerformAction
        if trust_parameter == None:
            trust_parameter = TRUST_PARAMETER
        self.trust_parameter = trust_parameter
        if LEARN_TRUST:
            self.trust = Trust()
        self.genome = genome
        self.tile = None
        if genome == None:
            # then generate your own genome
            self.genome = Genome()
        self.statistics = self.genome.statistics
        self.name = self.genome.name
        self.available_moves = GAMES_PER_ITER
        self.fitness = 0
        self.ID = returnRandomID()
        self.parents = []
        self.games_played = 0
        tile.acceptAgent(self)
    def reproduce(self):
        # returns a child of this agent.
        child = Agent(self.tile, None, self.trust_parameter, self.performAction)
        childGenome = self.genome.mutate()
        child.genome = childGenome
        child.name = child.genome.name
        child.parents = [x for x in self.parents]
        child.parents.append((self.ID, self.fitness))
        if LEARN_TRUST:
            child.trust = self.trust.reproduce() # no more telepathy!
        return child
    def cooperate(self):
        # returns the cooperate signal
        return COOP_SIGNAL
    def defect(self):
        # returns the defect signal
        return DEFECT_SIGNAL
    def quit(self):
        # returns the quit signal
        return QUIT_SIGNAL
    def move(self):
        # moves the agent. The agent randomly selects a tile from the
        # set of neighboring tiles (including the current tile) and then
        # asks the tile if it can move there. if the tile accepts, the
        # tile-side funciton ('acceptAgent') handles all the
        # modifications to the source tile, the target tile, and the
        # agent itself.
        if self.tile == None:
            return
        target = choice([self.tile] + self.tile.neighbors)
        target.acceptAgent(self)
    def trustFunction(self, agent):
        # this returns the probability of playing with the agent
        # specified by 'agent'. It is given by a modified logistic
        # function, where the agent has control over point where this
        # probability crosses 0.5. The scale parameter, however,
        # is hard-coded
        #
        # first, compute the number of different characters between
        # names.
        name_diffs = sum([x[0]!=x[1] for x in zip(self.name, agent.name)])
        return 1./(1+exp((name_diffs - self.trust_parameter)*1./TRUST_SCALE_FACTOR))
    def updateTrust(self, agent, delta_fitness):
        # updates the agent's trust in accordance with the trust object.
        self.trust.updateWeights(agent.name, delta_fitness)
    def decideToPlay(self, agent):
        # accepts an agent as input and decides whether or not to play
        # with them
        if ALWAYS_PLAY:
            return True
        if LEARN_TRUST:
            return self.trust.decideToPlay(agent.name)
        else:
            p = self.trustFunction(agent)
            return random() <= p
    def incTrustParameter(self):
        # increments the trust parameter
        self.trust_parameter += TRUST_INCREMENT_PARAMETER
    def decTrustParameter(self):
        # decrements the trust parameter
        self.trust_parameter -= TRUST_INCREMENT_PARAMETER
    def decideAction(self, history):
        # decides on what action to take given the game's current history
        action_code = self.genome.getAction(history)
        return self.performAction(self, action_code)
    def die(self):
        # 'kills' the agent
        self.tile.removeAgent(self)
        # the World class will handle removing all the agents from its
        # records each iteration.














