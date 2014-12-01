'''
This exports the world class, which is responsible for actually running
iterations of the simulation.

Functions are largely self-explanatory. Right now, we will only be
supporting the random() world generation method.
'''

from constants import *
from tile import Tile
from agent import Agent
from random import choice
from gameMaster import gameMaster
import pdb, sys
from numpy import mean
from scipy.stats import rv_discrete as rvd

class World():
    def __init__(self):
        # note that all the relevant inputs to World() are defined in
        # the constants file.
        self.tiles = [[None for y in range(N_COLS)] for x in range(N_ROWS)]
        self.agents = []
        self.instantiateTiles()
        self.instantiateAgents()
        self.num_iterations = 0
        self.mean_fitness = []
        self.mean_trust = []
        self.die_offs = []
        self.mean_per_game_fitness = []
        self.tot_games_played = []
        self.cur_mean_fitness = 0
        self.initializeStatistics()
    def initializeStatistics(self):
        # creates the data structure that will hold tile-by-tile statistics
        statistic_names = ['num_agents','fitness','trust','per_game_fitness','tot_games'] + self.agents[0].stats.keys()
        global_statistic_names = self.agents[0].stats.keys()
        self.statistics = dict()
        self.global_statistics = dict()
        for i in statistic_names:
            self.statistics[i] = []
        for i in global_statistic_names:
            self.global_statistics[i] = []
    def updateStatistics(self):
        # updates all the per-tile statistics
        for i in self.global_statistics.keys():
            self.global_statistics[i].append(mean([x.stats[i][0]*1./x.stats[i][1] for x in self.agents if x.stats[i][1] > 0]))
        for i in self.statistics.keys():
            new_stats = [[0 for y in range(N_COLS)] for x in range(N_ROWS)]
            for x,row in enumerate(self.tiles):
                for y,tile in enumerate(row):
                    if i == 'num_agents':
                        new_stats[x][y] = len(tile.agents)
                    elif i == 'fitness':
                        new_stats[x][y] = mean([z.fitness for z in tile.agents])
                    elif i == 'trust':
                        new_stats[x][y] = mean([z.trust_parameter for z in tile.agents])
                    elif i == 'per_game_fitness':
                        if self.statistics['tot_games'][-1][x][y] > 0:
                            new_stats[x][y] = sum([z.fitness for z in tile.agents])*1./self.statistics['tot_games'][-1][x][y]
                    elif i != 'tot_games': # tot_games updated elsewhere
                        new_stats[x][y] = mean([z.stats[i][0]*1./z.stats[i][1] for z in tile.agents if z.stats[i][1] > 0])
            if i!='tot_games':
                self.statistics[i].append(new_stats)
    def instantiateTiles(self):
        # creates the tile world
        if not GRID_RANDOM:
            raise NotImplementedError("Must use random world: set GRID_RANDOM to true")
        printMsg('Creating %i-by-%i World'%(N_ROWS, N_COLS),1)
        # instantiate the tiles
        for x in range(N_ROWS):
            for y in range(N_COLS):
                self.tiles[x][y] = Tile((x,y),transProbFcn())
        # compute the tile's neighbors
        for x in range(N_ROWS):
            for y in range(N_COLS):
                neighbors = neighborCords((x, y))
                neighbs = [self.tiles[n[0]][n[1]] for n in neighbors]
                self.tiles[x][y].neighbors = neighbs
    def instantiateAgents(self):
        # populates the world with agents
        printMsg('Creating %i agents'%NUM_AGENTS, 1)
        _ = [self.createRandomAgent() for x in range(NUM_AGENTS)]
    def createRandomAgent(self):
        # creates a random agent and puts it in a randomly selected tile
        tile = choice(choice(self.tiles))
        next_agent = Agent(tile)
        self.agents.append(next_agent)
    def iterate(self,regen_children = True):
        # the main iteration function. iterates all of the agents
        # and all of the tiles.
        self.num_iterations += 1
        printMsg('Beginning iteration %i'%self.num_iterations, 2)
        for agent in self.agents:
            # move all the agents
            if MOVE:
                agent.move()
        tot_games = 0
        tile_tot_games = [[0 for y in range(N_COLS)] for x in range(N_ROWS)]
        for x,row in enumerate(self.tiles):
            for y,tile in enumerate(row):
                printMsg('Playing %i agents in tile %s'%(len(tile.agents), str(tile.location)), 1)
                # iterate the tile
                tile.iterate()
                # play the agents against each other
                while True:
                    agents = tile.getPlayers()
                    if agents == None:
                        break
                    [_, game_played] = gameMaster(agents[0], agents[1])
                    tot_games += game_played
                    tile_tot_games[x][y] += game_played
        self.statistics['tot_games'].append(tile_tot_games)
        self.tot_games_played.append(tot_games)
        self.mean_per_game_fitness.append(sum([x.fitness for x in self.agents]) * 1./tot_games)
        self.cur_mean_fitness = float(mean([x.fitness for x in self.agents]))
        self.mean_fitness.append(self.cur_mean_fitness)
        printMsg('Fitness for iteration %i is %.3f (%.3fpg)'%(self.num_iterations, self.cur_mean_fitness, self.mean_per_game_fitness[-1]),2)
        tot_above_avg_fitness = sum([x.fitness for x in self.agents if x.fitness >= self.cur_mean_fitness])
        below_avg_agents = sum([1 for x in self.agents if x.fitness < self.cur_mean_fitness])
        self.die_offs.append(below_avg_agents)
        self.updateStatistics()
        if regen_children:
            self.generateChildren()
        printMsg('Iteration %i Complete. %i agents below avg fitness'%(self.num_iterations, below_avg_agents), 2)
        printMsg('Average Trust: %.3f'%mean([x.trust_parameter for x in self.agents]), 2)
        self.mean_trust.append(mean([x.trust_parameter for x in self.agents]))
    def generateChildren(self):
        # Because of rounding errors, instead of directly generating children
        # sequentially, we have to create a discrete distribution and sample
        # from it. Which, while not being directly fair, works well enough.
        # current_mean_fitness - short version
        cmf = self.cur_mean_fitness
        # total_above_average_fitness - short version
        taaf = sum([(x.fitness - cmf) for x in self.agents if x.fitness >= cmf])
        #dist = [(x.fitness - cmf) * 1./taaf for x in self.agents if x.fitness >= cmf]
        # this method deals with negative numbers better.
        dist = [x.fitness for x in self.agents if x.fitness >= cmf]
        if sum(dist) <= 0:
            printMsg('Iteration %i has experienced negative or zero fitness!'%self.num_iterations, 3)
            dist = [1./len(self.agents) for x in self.agents]
        else:
            dist = [x*1./sum(dist) for x in dist]
        #good_agents = filter(lambda x: x.fitness >= cmf, self.agents)
        idx = [n for n,a in enumerate(self.agents) if a.fitness >= cmf]
        #r = rvd(values=(range(len(dist)), dist))
        r = rvd(values=(idx, dist))
        having_babies_IDX = r.rvs(size=NUM_AGENTS)
        # now that we've sampled from the parents, instruct them to each have
        # kids
        babies = []
        for x in having_babies_IDX:
            babies.append(self.agents[x].reproduce())
        for x in self.agents:
            x.die()
        self.agents = babies











