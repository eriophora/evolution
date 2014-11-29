# for testing stuff

from agent import Agent
from gameMaster import gameMaster
from constants import *

agent_a = Agent()
agent_b = Agent()

gameMaster(agent_a, agent_b)


#############

import world
reload(world)
import pdb, sys
w = world.World()
for i in range(1000000):
    w.iterate()
    plt.scatter(i, w.cur_mean_fitness)
    #plt.scatter(i, w.mean_trust[-1])
    if not i % 100:
        plt.draw()
        pause(0.05)

from random import choice
a = choice(w.agents)
b = choice(w.agents)
a.available_moves = 500
b.available_moves = 500
h = gameMaster(a,b)
print h


t = []
for i in range(10000):
    c = 0
    while True:
        if random() > CONTINUE_PROB:
            break
        c+=1
    t.append(c)


z = []
fig = plt.figure()
for i in range(1000):
    z.append(random())
    plt.plot(z)
    plt.draw()
    pause(0.05)

# let's make sure that the agents and the tiles agree on whether the
# agent is.
badAgents = []
for agent in w.agents:
    if agent not in agent.tile.agents:
        badAgents.append(agent)

z = dict()
for agent in badAgents:
    z[agent.ID] = []

for row in w.tiles:
    for tile in row:
        for agent in badAgents:
            if agent in tile.agents:
                z[agent.ID].append(tile.location)

babies = []
round_babies = []
int_babies = []
tot_above_avg_fitness = sum([x.fitness for x in w.agents if x.fitness >= w.cur_mean_fitness])
for agent in w.agents:
    if agent.fitness >= w.cur_mean_fitness:
        babies.append(NUM_AGENTS * agent.fitness * 1./tot_above_avg_fitness)
round_babies = [round(x) for x in babies]
int_babies = [int(x) for x in round_babies]


from scipy.stats import rv_discrete as rvd
cmf = mean([x.fitness for x in w.agents])
taaf = sum([(x.fitness - cmf) for x in w.agents if x.fitness >= cmf])
dist = [(x.fitness - cmf) * 1./taaf for x in w.agents if x.fitness >= cmf]
gagents = [x for x in w.agents if x.fitness >= cmf]
idx = [n for n,a in enumerate(w.agents) if a.fitness >= cmf]
r = rvd(values=(idx, dist))
tohavekids = r.rvs(size=1000)

dist = [(x.fitness - cmf) * 1./taaf for x in w.agents if x.fitness >= cmf]

tot_agents = 0
for row in w.tiles:
    for tile in row:
        tot_agents += len(tile.agents)
