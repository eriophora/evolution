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
from constants import *
from math import exp

class agent():
    def __init__(self, tile = None, genome = None, trust_parameter = TRUST_PARAMETER):
        self.trust_parameter = trust_parameter
        self.genome = genome
        if genome == None:
             # then generate your own genome
             self.genome = Genome()
        self.name = self.genome.name
        self.tile = tile
        self.available_moves = GAMES_PER_ITER
        self.fitness = 0
        self.move()
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
        return 1./(1+exp((name_diffs - self.trust_parameter)*1./SCALE_PARAMETER))
