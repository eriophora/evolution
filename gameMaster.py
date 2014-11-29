'''
gameMaster is a function that manages the play between two agents.

gameMaster also manages those agent's number of available games, and
also updates their fitness.
'''

from constants import *
from random import random

def gameMaster(agent_a, agent_b):
    agent_a_actions = ''
    agent_b_actions = ''
    agent_a_delta = 0
    agent_b_delta = 0
    # check if either player refuses to play, act accordingly
    history = []
    printMsg('Playing agent %s (%s) [agent A] against agent %s (%s) [agent B]'%(agent_a.name, agent_a.ID, agent_b.name, agent_b.ID))
    history.append('Playing agent %s (%s) [agent A] against agent %s (%s) [agent B]'%(agent_a.name, agent_a.ID, agent_b.name, agent_b.ID))
    if not agent_a.decideToPlay(agent_b):
        printMsg('Agent A has refused to play!')
        history.append('Agent A has refused to play!')
        agent_a.available_moves -= REFUSE_PENALTY
        agent_b.available_moves -= DENIED_PENALTY
        return
    if not agent_b.decideToPlay(agent_a):
        printMsg('Agent B has refused to play!')
        history.append('Agent B has refused to play!')
        agent_b.available_moves -= REFUSE_PENALTY
        agent_a.available_moves -= DENIED_PENALTY
        return
    num_rounds = 0
    printMsg('Game start. Agent A fitness %i, Agent B fitness %i'%(agent_a.fitness, agent_b.fitness))
    history.append('Game start. Agent A fitness %i, Agent B fitness %i'%(agent_a.fitness, agent_b.fitness))
    while True:
        if random() > CONTINUE_PROB:
            printMsg('Game is over after %i rounds'%num_rounds)
            history.append('Game is over after %i rounds'%num_rounds)
            break
        # decide if another round is to occur
        act_a = agent_a.decideAction(agent_b_actions)
        act_b = agent_b.decideAction(agent_a_actions)
        if act_a == QUIT_SIGNAL:
            printMsg('Agent A has quit the game.')
            history.append('Agent A has quit the game.')
            break
        if act_b == QUIT_SIGNAL:
            printMsg('Agent B has quit the game.')
            history.append('Agent B has quit the game.')
            break
        num_rounds += 1
        printMsg('Round %i: Agent A decides to %s, Agent B decides to %s'%(num_rounds, ACTION_LABELS[act_a], ACTION_LABELS[act_b]))
        history.append('Round %i: Agent A decides to %s, Agent B decides to %s'%(num_rounds, ACTION_LABELS[act_a], ACTION_LABELS[act_b]))
        agent_a_actions += str(act_a)
        agent_b_actions += str(act_b)
        agent_a_actions = agent_a_actions[-HISTORY_LENGTH:]
        agent_b_actions = agent_b_actions[-HISTORY_LENGTH:]
        if agent_a.available_moves >= 1:
            agent_a.fitness += PAYOFF_MAP[act_a][act_b]
            agent_a_delta += PAYOFF_MAP[act_a][act_b]
            agent_a.games_played += 1
            if LEARN_TRUST:
                # have agent A update their trust
                agent_a.updateTrust(agent_b, agent_a_delta)
        if agent_b.available_moves >= 1:
            agent_b.fitness += PAYOFF_MAP[act_b][act_a]
            agent_b_delta += PAYOFF_MAP[act_b][act_a]
            agent_b.games_played += 1
            if LEARN_TRUST:
                # have agent B update their trust
                agent_b.updateTrust(agent_a, agent_b_delta)
    printMsg('Game over after %i rounds. Agent A fitness gain %i, Agent B fitness gain %i'%(num_rounds, agent_a_delta, agent_b_delta))
    history.append('Game over after %i rounds. Agent A fitness gain %i, Agent B fitness gain %i'%(num_rounds, agent_a_delta, agent_b_delta))
    agent_a.available_moves -= 1
    agent_b.available_moves -= 1
    return history

