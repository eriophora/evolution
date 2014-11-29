'''
Exports the 'tile' class, which represents a single tile on the game
board. Tiles are expected to keep track of all the agents that are
present on the tile. Tiles also keep track of who their neighbors are,
and also allow or deny an agent's request to enter the tile.

Perhaps the most important function of the tile is to keep track
of the "Play Queue", which returns agents that are to be played against
each other, prioritizing agents who still have games left that they
can play.

Created by NPD on 11/23/14
'''

from random import random
from numpy.random import choice as npchoice
from random import choice
from constants import *

class Tile():
    def __init__(self, location, transition_prob = 1):
        # location dictates where on the game board this tile is.
        # transition_prob is the likelihood that an agent that attempts
        # to move to this tile will be able to, a float from 0 to 1.
        self.transition_prob = transition_prob
        self.location = location
        self.loc_x, self.loc_y = location
        self.agents = [] # array of agents currently on the tile
        self.neighbors = [] # array of neighboring tiles
        self.agents_to_play = [] # stores a list of agents that waiting
                               # to play this iteration.
    def _buildQueue(self):
        # constructs agents_to_play.
        self.agents_to_play = [x for x in self.agents]
    def iterate(self):
        # the iterate method effectively resets the queue. it
        # is to be called after each iteration is completed.
        # in the case of tiles, all that this does is rebuild the
        # playing queue.
        self._buildQueue()
    def acceptAgent(self, agent):
        # this decides whether or not to accept an agent onto this tile,
        # potentially be checking whether or not the agent is in a
        # neighboring tile.
        if agent.tile == None:
            agent.tile = self
            self.agents.append(agent)
        if random() <= self.transition_prob:
            if agent.tile != None:
                # then the agent may enter the tile.
                # remove the agent from the other tile
                agent.tile.removeAgent(agent)
            # change that agent's tile
            agent.tile = self
            # add this agent to the list of current agents
            self.agents.append(agent)
    def removeAgent(self, agent):
        # removes an agent from this tile.
        if agent in self.agents_to_play:
            self.agents_to_play.remove(agent)
        self.agents.remove(agent)
    def getPlayers(self):
        # returns two randomly chosen agents. If there are no such
        # agents remaining, simply return None.
        if len(self.agents) < 2:
            # only 0 or 1 agents -- that agent is, sadly, doomed to die
            # with no fitness.
            return None
        while True:
            rem_both = True
            if not len(self.agents_to_play):
                return None
            if len(self.agents_to_play) == 1:
                agent_a = self.agents_to_play[0]
                agent_b = choice(self.agents)
                rem_both = False
            else:
                agent_a, agent_b = npchoice(self.agents_to_play, 2, False)
            if agent_a.available_moves >= 1 or agent_b.available_moves >= 1:
                # i.e., if either have something left that they
                # can gain.
                break
            self.agents_to_play.remove(agent_a)
            if rem_both:
                self.agents_to_play.remove(agent_b)
        if agent_a.available_moves < 1:
            self.agents_to_play.remove(agent_a)
        if agent_b.available_moves < 1 and rem_both:
            self.agents_to_play.remove(agent_b)
        return (agent_a, agent_b)




