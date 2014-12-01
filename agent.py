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
        # self.statistics = self.genome.statistics
        self.name = self.genome.name
        self.available_moves = GAMES_PER_ITER
        self.fitness = 0
        self.ID = returnRandomID()
        self.parents = []
        self.games_played = 0
        if tile != None:
            tile.acceptAgent(self)
        self.initializeStatistics()
    def initializeStatistics(self):
        # instantiates the data structure to hold the statistics
        # in lieu of the old (gene-centric) way of computing statistics,
        # now they are updated by gameMaster based on actions that were
        # actually executed, as well as by the decideAction() function.
        # Each statistic is intended to be displayed as a ratio, where
        # the first value is the number of times that situation happend
        # versus the number of times that situation COULD have happened
        stats = dict()
        stats['popular'] = [0, 0] # the frequency with which other agents agree to play with this agent
        stats['selective'] = [0, 0] # the frequency with which this agent agrees to play with other agents
        stats['cooperator'] = [0, 0] # the fraction of the time the agent cooperates.
        stats['defector'] = [0, 0] # the fraction of the time the agent defects
        stats['quitter'] = [0, 0] # the fraction of the time the agent quits
        stats['collaborator'] = [0, 0] # cooperated with a cooperator
        stats['sucker'] = [0, 0] # cooperated against a defector
        stats['traitor'] = [0, 0] # defected against a cooperator
        stats['prisoner'] = [0, 0] # defected against a defector
        stats['cruel'] = [0, 0] # defected following a cooperation
        stats['nice'] = [0, 0] # cooperated following a cooperation
        stats['forgiving'] = [0, 0] # cooperated following a defection
        stats['vengeful'] = [0, 0] # defected following a defection
        stats['timid'] = [0, 0] # quit following a cooperation
        stats['retreating'] = [0, 0] # quit following a defection
        self.stats = stats
        # stats_to_increment is a map of stats whose total must be
        # incremented given the opponent's previous action
        self.stats_to_increment = {COOP_SIGNAL:['cruel','nice','timid'], DEFECT_SIGNAL:['forgiving','vengeful','retreating']}
        # stat_update_map is a dict() where
        # stat_update_map[preceeding_opponent_move][your_signal] = the
        # stat to increment.
        stat_update_map = dict()
        coop_d = {COOP_SIGNAL:'nice',DEFECT_SIGNAL:'cruel',QUIT_SIGNAL:'timid'}
        defe_d = {COOP_SIGNAL:'forgiving',DEFECT_SIGNAL:'vengeful',QUIT_SIGNAL:'retreating'}
        stat_update_map[COOP_SIGNAL] = coop_d
        stat_update_map[DEFECT_SIGNAL] = defe_d
        self.stat_update_map = stat_update_map
    def decideAction(self, history):
        # decides on what action to take given the game's current history
        action_code = self.genome.getAction(history)
        signal = self.performAction(self, action_code)
        self.stats['cooperator'][1] += 1
        self.stats['defector'][1] += 1
        self.stats['quitter'][1] += 1
        if signal == COOP_SIGNAL:
            self.stats['cooperator'][0] += 1
        if signal == DEFECT_SIGNAL:
            self.stats['defector'][0] += 1
        if signal == QUIT_SIGNAL:
            self.stats['quitter'][0] += 1
        if len(history):
            opp_move = int(history[-1])
            for cur_stat in self.stats_to_increment[opp_move]:
                self.stats[cur_stat][1] += 1
            self.stats[self.stat_update_map[opp_move][signal]][0]+=1
        return signal
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
    def die(self):
        # 'kills' the agent
        self.tile.removeAgent(self)
        # the World class will handle removing all the agents from its
        # records each iteration.














